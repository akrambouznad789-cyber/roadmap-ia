"""Capture le rendu réel d'une page HTML avec Chrome ou Edge, sans ouvrir de fenêtre.

Usage :
    python outils/capturer_page.py docs/index.html

Écrit `.captures/<nom>_bureau.png` et `.captures/<nom>_etroit.png`, qu'on peut ensuite lire comme des images.
"""
import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

RACINE_DEPOT = Path(__file__).resolve().parent.parent
DOSSIER_CAPTURES = RACINE_DEPOT / ".captures"
NAVIGATEURS_CANDIDATS = (
    Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
    Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
    Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
)
# Chrome sans interface refuse les fenêtres de moins de 500 px environ : c'est donc la vue étroite.
LARGEURS_PAR_FORMAT = {"bureau": 1280, "etroit": 500}
DELAI_RENDU_MILLISECONDES = 3000
DELAI_MAX_CAPTURE_SECONDES = 60


def trouver_navigateur():
    for chemin in NAVIGATEURS_CANDIDATS:
        if chemin.exists():
            return chemin
    raise FileNotFoundError("Ni Chrome ni Edge n'ont été trouvés aux emplacements habituels.")


def capturer(navigateur, chemin_page, chemin_image, largeur, hauteur):
    # Un profil temporaire évite le conflit avec une fenêtre Chrome déjà ouverte.
    with tempfile.TemporaryDirectory() as dossier_profil:
        subprocess.run(
            [
                str(navigateur),
                "--headless=new",
                "--disable-gpu",
                "--hide-scrollbars",
                "--no-first-run",
                "--no-default-browser-check",
                f"--user-data-dir={dossier_profil}",
                f"--window-size={largeur},{hauteur}",
                f"--virtual-time-budget={DELAI_RENDU_MILLISECONDES}",
                f"--screenshot={chemin_image}",
                chemin_page.resolve().as_uri(),
            ],
            check=True, capture_output=True, timeout=DELAI_MAX_CAPTURE_SECONDES,
        )
    if not chemin_image.exists():
        raise RuntimeError(f"Le navigateur n'a pas écrit la capture {chemin_image}.")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    analyseur = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    analyseur.add_argument("page", type=Path)
    analyseur.add_argument("--hauteur", type=int, default=1800)
    arguments = analyseur.parse_args()
    if not arguments.page.exists():
        sys.exit(f"Page introuvable : {arguments.page}")
    navigateur = trouver_navigateur()
    DOSSIER_CAPTURES.mkdir(exist_ok=True)
    nom_page = arguments.page.parent.name if arguments.page.stem == "index" else arguments.page.stem
    for nom_format, largeur in LARGEURS_PAR_FORMAT.items():
        chemin_image = DOSSIER_CAPTURES / f"{nom_page}_{nom_format}.png"
        capturer(navigateur, arguments.page, chemin_image, largeur, arguments.hauteur)
        print(chemin_image)


if __name__ == "__main__":
    main()
