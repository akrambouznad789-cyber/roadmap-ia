"""Vérifie tout ce qui deviendrait public avant une publication sur GitHub.

Usage :
    python outils/verifier_avant_publication.py

Fichiers examinés : ceux que git publierait, soit tout sauf ce que `.gitignore` exclut.
La liste des mots privés reste dans `contexte/mots_interdits.txt`, un fichier non publié : la mettre
ici publierait justement ce qu'elle protège. Sur GitHub Actions, ce fichier n'existe pas et seuls les
motifs génériques s'appliquent.
"""
import os
import re
import subprocess
import sys
from pathlib import Path

RACINE_DEPOT = Path(__file__).resolve().parent.parent
FICHIER_MOTS_INTERDITS = RACINE_DEPOT / "contexte" / "mots_interdits.txt"
REPERE_TEXTE_A_ECRIRE = "À ÉCRIRE PAR AKRAM"
REPERE_GABARIT_NON_REMPLI = "{{"
SECTIONS_OBLIGATOIRES_PARCELLE = ("regarde", "demo", "main", "mots", "sources")
TAILLE_MAX_FICHIER_OCTETS = 5 * 1024 * 1024
EXTENSIONS_TEXTE = {
    ".css", ".csv", ".html", ".ini", ".js", ".json", ".md", ".py", ".svg", ".toml", ".txt", ".yaml", ".yml",
}
# Des données de recherche ou des modèles n'ont rien à faire dans un dépôt public.
EXTENSIONS_INTERDITES = {
    ".accdb", ".db", ".gguf", ".gpkg", ".parquet", ".pdf", ".pt", ".pth", ".safetensors", ".sqlite", ".xlsx", ".zip",
}
MOTIFS_GENERIQUES = {
    "numéro de téléphone": re.compile(r"(?<![\d.])\d{3}[-. ]\d{3}[-. ]\d{4}(?![\d.])"),
    "chemin local Windows": re.compile(r"[A-Za-z]:[\\/]Users[\\/]"),
    "chemin local Git Bash": re.compile(r"/[a-z]/Users/"),
}
MOTIF_LIEN_LOCAL = re.compile(r"""(?:href|src)\s*=\s*["']([^"'#?]+)""", re.IGNORECASE)
PREFIXES_LIEN_EXTERNE = ("http://", "https://", "mailto:", "tel:", "data:", "//")


def lire_mots_interdits(chemin=FICHIER_MOTS_INTERDITS):
    """Renvoie les mots privés, ou None si la liste est absente sur GitHub Actions."""
    if not chemin.exists():
        if os.environ.get("CI"):
            return None
        raise FileNotFoundError(f"Liste de mots interdits introuvable : {chemin}")
    lignes = chemin.read_text(encoding="utf-8").splitlines()
    return [ligne.strip() for ligne in lignes if ligne.strip() and not ligne.startswith("#")]


def lister_fichiers_publics(racine):
    """Liste les fichiers que git publierait, en tenant compte de `.gitignore`."""
    resultat = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=racine, capture_output=True, check=True,
    )
    chemins = resultat.stdout.decode("utf-8").split("\0")
    return [Path(chemin) for chemin in chemins if chemin and (racine / chemin).is_file()]


def verifier_texte(chemin_relatif, texte, mots_interdits):
    problemes = []
    for nom_motif, motif in MOTIFS_GENERIQUES.items():
        if motif.search(texte):
            problemes.append(f"{chemin_relatif} : {nom_motif} détecté")
    texte_minuscule = texte.casefold()
    for mot in mots_interdits or []:
        if mot.casefold() in texte_minuscule:
            problemes.append(f"{chemin_relatif} : mot privé détecté ({mot})")
    return problemes


def verifier_page_html(racine, chemin_relatif, texte):
    problemes = []
    if not re.search(r"<html[^>]*\blang=", texte, re.IGNORECASE):
        problemes.append(f"{chemin_relatif} : attribut lang manquant sur <html>")
    if not re.search(r"<title>\s*\S", texte, re.IGNORECASE):
        problemes.append(f"{chemin_relatif} : <title> vide ou absent")
    if REPERE_TEXTE_A_ECRIRE in texte:
        problemes.append(f"{chemin_relatif} : il reste un texte à écrire par Akram")
    if REPERE_GABARIT_NON_REMPLI in texte:
        problemes.append(f"{chemin_relatif} : gabarit non rempli ({REPERE_GABARIT_NON_REMPLI})")
    for lien in MOTIF_LIEN_LOCAL.findall(texte):
        lien_local = lien.strip()
        if not lien_local or lien_local.lower().startswith(PREFIXES_LIEN_EXTERNE):
            continue
        cible = (racine / chemin_relatif).parent / lien_local
        if lien_local.endswith("/"):
            cible = cible / "index.html"
        if not cible.exists():
            problemes.append(f"{chemin_relatif} : lien brisé vers {lien_local}")
    return problemes


def verifier_parcelle(chemin_relatif, texte):
    problemes = []
    for section in SECTIONS_OBLIGATOIRES_PARCELLE:
        if not re.search(rf"""\bid\s*=\s*["']{section}["']""", texte):
            problemes.append(f"{chemin_relatif} : section #{section} manquante")
    return problemes


def est_page_parcelle(chemin_relatif):
    parties = chemin_relatif.parts
    return (
        len(parties) == 4
        and parties[:2] == ("docs", "parcelles")
        and chemin_relatif.name == "index.html"
    )


def verifier_depot(racine, mots_interdits):
    """Renvoie la liste des problèmes trouvés ; une liste vide autorise la publication."""
    problemes = []
    for chemin_relatif in lister_fichiers_publics(racine):
        chemin_absolu = racine / chemin_relatif
        extension = chemin_relatif.suffix.lower()
        if extension in EXTENSIONS_INTERDITES:
            problemes.append(f"{chemin_relatif} : type de fichier interdit dans un dépôt public")
            continue
        if chemin_absolu.stat().st_size > TAILLE_MAX_FICHIER_OCTETS:
            problemes.append(f"{chemin_relatif} : fichier de plus de 5 Mo")
        if extension not in EXTENSIONS_TEXTE:
            continue
        texte = chemin_absolu.read_text(encoding="utf-8", errors="replace")
        problemes += verifier_texte(chemin_relatif, texte, mots_interdits)
        if extension == ".html" and chemin_relatif.parts[0] == "docs":
            problemes += verifier_page_html(racine, chemin_relatif, texte)
        if est_page_parcelle(chemin_relatif):
            problemes += verifier_parcelle(chemin_relatif, texte)
    return problemes


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    mots_interdits = lire_mots_interdits()
    if mots_interdits is None:
        print("Note : liste de mots privés absente, seuls les motifs génériques s'appliquent.")
    problemes = verifier_depot(RACINE_DEPOT, mots_interdits)
    if problemes:
        print(f"Publication bloquée : {len(problemes)} problème(s).")
        for probleme in problemes:
            print(f"  - {probleme}")
        return 1
    print("Aucun problème : le contenu public peut être publié.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
