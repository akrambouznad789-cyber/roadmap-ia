"""Regroupe les sections par saisonnalité (DJME / DJMH) pour montrer les familles de facteurs du ministère.

Usage :
    .venv/Scripts/python parcelles/01-reseau-neurones/analyser_familles.py

Écrit `familles_saisonnalite.csv` : des comptes et des médianes agrégés, jamais les sections elles-mêmes.
"""
from pathlib import Path

import pandas as pd

DOSSIER_STATION = Path(__file__).resolve().parent
LARGEUR_TRANCHE = 0.05
# Une tranche plus petite n'apparaît pas dans le fichier : une médiane sur une poignée de sections ne dit rien.
NOMBRE_MINIMAL_SECTIONS = 20


def main():
    sections = pd.read_csv(DOSSIER_STATION / "donnees" / "sections_2025.csv")
    sections["saisonnalite"] = sections["djme"] / sections["djmh"]
    sections["ratio_pointe"] = sections["trentieme_heure"] / sections["djma"]
    sections["tranche_saisonnalite"] = (sections["saisonnalite"] / LARGEUR_TRANCHE).round() * LARGEUR_TRANCHE

    familles = (
        sections.groupby("tranche_saisonnalite")
        .agg(nombre_sections=("ratio_pointe", "size"), ratio_pointe_median=("ratio_pointe", "median"))
        .reset_index()
    )
    familles = familles[familles["nombre_sections"] >= NOMBRE_MINIMAL_SECTIONS].round(3)
    chemin_sortie = DOSSIER_STATION / "familles_saisonnalite.csv"
    familles.to_csv(chemin_sortie, index=False)
    print(familles.to_string(index=False))
    print(f"{familles['nombre_sections'].sum()} sections sur {len(sections)} dans ces tranches -> {chemin_sortie}")


if __name__ == "__main__":
    main()
