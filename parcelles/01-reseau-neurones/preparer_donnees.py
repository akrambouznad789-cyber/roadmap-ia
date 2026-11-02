"""Extrait des débits de circulation du MTQ un tableau simple pour entraîner un réseau de neurones.

Usage :
    python parcelles/01-reseau-neurones/preparer_donnees.py C:/chemin/vers/DebitCirculation.gpkg

Garde les sections qui ont, pour l'année la plus récente, un DJMA, un DJME, un DJMH et un débit à la 30e heure.
Le CSV produit va dans `donnees/`, que git ignore : les données ne vont jamais dans le dépôt.
"""
import argparse
import csv
import sqlite3
import sys
from pathlib import Path

DOSSIER_DONNEES = Path(__file__).resolve().parent / "donnees"
COLONNES_SORTIE = ["numero_section", "numero_route", "djma", "djme", "djmh", "pourcentage_camions", "trentieme_heure"]


def lire_nombre(valeur):
    """Les débits sont stockés en texte ; une case vide veut dire « pas de mesure »."""
    if valeur in (None, ""):
        return None
    return float(valeur)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    analyseur = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    analyseur.add_argument("chemin_geopackage", type=Path)
    arguments = analyseur.parse_args()
    if not arguments.chemin_geopackage.exists():
        sys.exit(f"GeoPackage introuvable : {arguments.chemin_geopackage}")

    connexion = sqlite3.connect(f"file:{arguments.chemin_geopackage.as_posix()}?mode=ro", uri=True)
    lignes = connexion.execute(
        "select num_sectn_trafc, djma_annee_1, val_djma_annee_1, val_djme_annee_1, val_djmh_annee_1, "
        "val_cam_annee_1, val_30e_heure from circulation_routier"
    ).fetchall()

    # La colonne « année 1 » est la plus récente. Le script refuse un mélange d'années plutôt que de le cacher.
    annees_trouvees = {annee for _, annee, *_ in lignes}
    if len(annees_trouvees) != 1:
        sys.exit(f"Plusieurs années dans la colonne de l'année 1 : {sorted(annees_trouvees)}")
    annee_mesure = int(annees_trouvees.pop())

    sections_completes = []
    for numero_section, _, djma, djme, djmh, pourcentage_camions, trentieme_heure in lignes:
        valeurs_obligatoires = [lire_nombre(valeur) for valeur in (djma, djme, djmh, trentieme_heure)]
        if any(valeur is None for valeur in valeurs_obligatoires):
            continue
        djma, djme, djmh, trentieme_heure = valeurs_obligatoires
        sections_completes.append({
            "numero_section": numero_section,
            # Les 5 premiers chiffres du numéro de section donnent le numéro de route (00073 pour l'A-73).
            "numero_route": numero_section[:5],
            "djma": djma,
            "djme": djme,
            "djmh": djmh,
            "pourcentage_camions": lire_nombre(pourcentage_camions),
            "trentieme_heure": trentieme_heure,
        })

    DOSSIER_DONNEES.mkdir(exist_ok=True)
    chemin_sortie = DOSSIER_DONNEES / f"sections_{annee_mesure}.csv"
    with chemin_sortie.open("w", newline="", encoding="utf-8") as fichier:
        ecrivain = csv.DictWriter(fichier, fieldnames=COLONNES_SORTIE)
        ecrivain.writeheader()
        ecrivain.writerows(sections_completes)
    print(f"{len(sections_completes)} sections complètes sur {len(lignes)}, année {annee_mesure} -> {chemin_sortie}")


if __name__ == "__main__":
    main()
