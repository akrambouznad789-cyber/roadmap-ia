import csv
import json
import threading
from datetime import date
from http.server import BaseHTTPRequestHandler, HTTPServer

import pytest

from mesurer_llm_local import (
    ErreurOllama,
    Mesure,
    ajouter_au_csv,
    appeler_ollama,
    extraire_mesure,
    mediane_hors_demarrage,
)

REPONSE_OLLAMA_EXEMPLE = {
    "eval_count": 100,
    "eval_duration": 20_000_000_000,
    "load_duration": 3_000_000_000,
    "total_duration": 24_000_000_000,
}


class FauxOllama(BaseHTTPRequestHandler):
    """Reproduit la réponse d'Ollama sans télécharger de modèle."""

    def do_POST(self):
        longueur = int(self.headers["Content-Length"])
        requete = json.loads(self.rfile.read(longueur))
        modele_connu = requete["model"] == "petit-modele"
        corps = REPONSE_OLLAMA_EXEMPLE if modele_connu else {"error": "model not found"}
        self.send_response(200 if modele_connu else 404)
        self.end_headers()
        self.wfile.write(json.dumps(corps).encode("utf-8"))

    def log_message(self, *arguments):
        pass


@pytest.fixture
def url_faux_ollama():
    serveur = HTTPServer(("127.0.0.1", 0), FauxOllama)
    fil = threading.Thread(target=serveur.serve_forever, daemon=True)
    fil.start()
    yield f"http://127.0.0.1:{serveur.server_port}"
    serveur.shutdown()
    serveur.server_close()


def mesure_a(jetons_par_seconde):
    return Mesure(10, jetons_par_seconde, 0.0, 1.0)


def test_convertit_les_nanosecondes_en_jetons_par_seconde():
    mesure = extraire_mesure(REPONSE_OLLAMA_EXEMPLE)
    assert mesure == Mesure(100, 5.0, 3.0, 24.0)


def test_refuse_une_duree_de_generation_nulle():
    with pytest.raises(ErreurOllama, match="durée de génération nulle"):
        extraire_mesure({**REPONSE_OLLAMA_EXEMPLE, "eval_duration": 0})


def test_la_mediane_ignore_le_demarrage_a_froid():
    assert mediane_hors_demarrage([mesure_a(1.0), mesure_a(8.0), mesure_a(10.0)]) == 9.0


def test_la_mediane_garde_une_mesure_unique():
    assert mediane_hors_demarrage([mesure_a(4.0)]) == 4.0


def test_appelle_ollama_et_lit_les_durees(url_faux_ollama):
    reponse = appeler_ollama(url_faux_ollama, "petit-modele", "Bonjour", 8)
    assert reponse["eval_count"] == 100


def test_un_modele_absent_donne_la_commande_a_lancer(url_faux_ollama):
    with pytest.raises(ErreurOllama, match="ollama pull inconnu"):
        appeler_ollama(url_faux_ollama, "inconnu", "Bonjour", 8)


def test_un_service_arrete_donne_une_erreur_claire():
    with pytest.raises(ErreurOllama, match="ne répond pas"):
        appeler_ollama("http://127.0.0.1:9", "petit-modele", "Bonjour", 8)


def test_le_csv_garde_un_seul_en_tete_et_cumule_les_mesures(tmp_path):
    chemin = tmp_path / "sous_dossier" / "resultats.csv"
    ajouter_au_csv(chemin, "petit-modele", [mesure_a(1.0), mesure_a(2.0)], date(2026, 10, 31))
    ajouter_au_csv(chemin, "petit-modele", [mesure_a(3.0)], date(2026, 11, 1))
    with chemin.open(encoding="utf-8", newline="") as fichier:
        lignes = list(csv.DictReader(fichier))
    assert [ligne["repetition"] for ligne in lignes] == ["1", "2", "1"]
    assert lignes[2]["date"] == "2026-11-01"
    assert lignes[2]["jetons_par_seconde"] == "3.0"
