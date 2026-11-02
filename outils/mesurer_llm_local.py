"""Mesure la vitesse d'un LLM local servi par Ollama et ajoute le résultat à un fichier CSV.

Usage :
    python outils/mesurer_llm_local.py --modele llama3.2:3b --repetitions 3

La première répétition charge le modèle en mémoire (démarrage à froid). Elle est écrite dans le CSV,
mais exclue de la médiane, qui doit décrire le régime normal.
"""
import argparse
import csv
import json
import statistics
import sys
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path

URL_OLLAMA_PAR_DEFAUT = "http://localhost:11434"
CHEMIN_RESULTATS_PAR_DEFAUT = (
    Path(__file__).resolve().parent.parent / "parcelles" / "00-llm-local" / "resultats.csv"
)
CONSIGNE_PAR_DEFAUT = "Explique ce qu'est un jumeau numérique en 3 phrases."
NOMBRE_MAX_JETONS_PAR_DEFAUT = 128
GRAINE_ALEATOIRE = 42
DELAI_MAX_REPONSE_SECONDES = 600
NANOSECONDES_PAR_SECONDE = 1_000_000_000
COLONNES_CSV = (
    "date",
    "modele",
    "repetition",
    "jetons_generes",
    "jetons_par_seconde",
    "duree_chargement_s",
    "duree_totale_s",
)


class ErreurOllama(RuntimeError):
    """Ollama est injoignable ou a refusé la demande."""


@dataclass(frozen=True)
class Mesure:
    jetons_generes: int
    jetons_par_seconde: float
    duree_chargement_s: float
    duree_totale_s: float


def appeler_ollama(url_base, modele, consigne, nombre_max_jetons):
    """Demande une réponse complète à Ollama et renvoie son JSON, durées comprises."""
    corps_requete = {
        "model": modele,
        "prompt": consigne,
        "stream": False,
        "options": {
            "temperature": 0,
            "seed": GRAINE_ALEATOIRE,
            "num_predict": nombre_max_jetons,
        },
    }
    requete = urllib.request.Request(
        f"{url_base}/api/generate",
        data=json.dumps(corps_requete).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(requete, timeout=DELAI_MAX_REPONSE_SECONDES) as reponse:
            return json.load(reponse)
    except urllib.error.HTTPError as erreur:
        detail = erreur.read().decode("utf-8", "replace")
        if erreur.code == 404:
            raise ErreurOllama(
                f"Modèle introuvable : {modele}. Télécharge-le avec `ollama pull {modele}`."
            ) from erreur
        raise ErreurOllama(f"Ollama a répondu {erreur.code} : {detail}") from erreur
    except urllib.error.URLError as erreur:
        raise ErreurOllama(
            f"Ollama ne répond pas à {url_base}. Ouvre l'application Ollama, puis réessaie."
        ) from erreur


def extraire_mesure(reponse_ollama):
    """Convertit les compteurs d'Ollama, donnés en nanosecondes, en une mesure lisible."""
    jetons_generes = reponse_ollama["eval_count"]
    duree_generation_ns = reponse_ollama["eval_duration"]
    if duree_generation_ns <= 0:
        raise ErreurOllama("Ollama a renvoyé une durée de génération nulle : mesure impossible.")
    return Mesure(
        jetons_generes=jetons_generes,
        jetons_par_seconde=round(jetons_generes * NANOSECONDES_PAR_SECONDE / duree_generation_ns, 2),
        duree_chargement_s=round(reponse_ollama["load_duration"] / NANOSECONDES_PAR_SECONDE, 2),
        duree_totale_s=round(reponse_ollama["total_duration"] / NANOSECONDES_PAR_SECONDE, 2),
    )


def mediane_hors_demarrage(mesures):
    """Médiane des jetons par seconde, sans le démarrage à froid quand il reste d'autres mesures."""
    mesures_utiles = mesures[1:] if len(mesures) > 1 else mesures
    return statistics.median(mesure.jetons_par_seconde for mesure in mesures_utiles)


def ajouter_au_csv(chemin_csv, modele, mesures, date_mesure=None):
    """Ajoute les mesures à la suite du CSV, et crée le fichier avec son en-tête au besoin."""
    chemin_csv.parent.mkdir(parents=True, exist_ok=True)
    ecrire_en_tete = not chemin_csv.exists()
    date_texte = (date_mesure or date.today()).isoformat()
    with chemin_csv.open("a", encoding="utf-8", newline="") as fichier:
        ecrivain = csv.DictWriter(fichier, fieldnames=COLONNES_CSV)
        if ecrire_en_tete:
            ecrivain.writeheader()
        for numero_repetition, mesure in enumerate(mesures, start=1):
            ecrivain.writerow(
                {"date": date_texte, "modele": modele, "repetition": numero_repetition, **asdict(mesure)}
            )


def analyser_arguments():
    analyseur = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    analyseur.add_argument("--modele", required=True, help="Nom du modèle Ollama, par exemple llama3.2:3b")
    analyseur.add_argument("--repetitions", type=int, default=3)
    analyseur.add_argument("--consigne", default=CONSIGNE_PAR_DEFAUT)
    analyseur.add_argument("--nombre-max-jetons", type=int, default=NOMBRE_MAX_JETONS_PAR_DEFAUT)
    analyseur.add_argument("--url-ollama", default=URL_OLLAMA_PAR_DEFAUT)
    analyseur.add_argument("--sortie", type=Path, default=CHEMIN_RESULTATS_PAR_DEFAUT)
    return analyseur.parse_args()


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    arguments = analyser_arguments()
    if arguments.repetitions < 1:
        sys.exit("Il faut au moins une répétition.")
    mesures = []
    try:
        for numero_repetition in range(1, arguments.repetitions + 1):
            reponse = appeler_ollama(
                arguments.url_ollama, arguments.modele, arguments.consigne, arguments.nombre_max_jetons
            )
            mesure = extraire_mesure(reponse)
            mesures.append(mesure)
            print(
                f"Répétition {numero_repetition} : {mesure.jetons_par_seconde} jetons/s, "
                f"{mesure.jetons_generes} jetons, chargement {mesure.duree_chargement_s} s, "
                f"total {mesure.duree_totale_s} s"
            )
    except ErreurOllama as erreur:
        sys.exit(str(erreur))
    ajouter_au_csv(arguments.sortie, arguments.modele, mesures)
    print(f"Médiane hors démarrage à froid : {mediane_hors_demarrage(mesures)} jetons/s")
    print(f"Résultats ajoutés à {arguments.sortie}")


if __name__ == "__main__":
    main()
