"""Figures du README de P3, à la charte du dépôt (style/charte.py) : chaque figure en deux PNG, clair et sombre.

Lit seulement les petits CSV de resultats/, tirés des sorties du carnet P3_duree_trajets.ipynb.
La carte apprise (carte_apprise_*.png) est produite par le carnet lui-même.

    python projets/P3-pytorch-plongements/figures.py
"""
import sys
from pathlib import Path

import matplotlib.patheffects as effets
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import FancyBboxPatch, Rectangle

DOSSIER_PROJET = Path(__file__).resolve().parent
DOSSIER_RESULTATS = DOSSIER_PROJET / "resultats"
sys.path.insert(0, str(DOSSIER_PROJET.parent.parent / "style"))
from charte import charger_charte, en_francais, sauver_clair_et_sombre  # noqa: E402

NOMS_DES_MOIS = ["janv.", "févr.", "mars", "avr.", "mai", "juin", "juil.", "août", "sept.", "oct.", "nov.", "déc."]


def virgule(nombre, decimales=2):
    """3.28 devient « 3,28 » ; les milliers prennent une espace insécable fine."""
    texte = f"{nombre:,.{decimales}f}".replace(",", " ").replace(".", ",")
    return texte


def halo():
    """Contour de la couleur du fond, pour qu'un texte reste lisible par-dessus un trait."""
    return [effets.withStroke(linewidth=3, foreground=plt.rcParams["axes.facecolor"])]


def boite(ax, x, y, largeur, hauteur, texte, couleurs, role="neutre", taille=9.5, gras=False):
    """Boîte à coins arrondis : « accent » = ce qu'on montre, « neutre » = le contexte."""
    bord = couleurs["accent"] if role == "accent" else couleurs["trait"]
    fond = couleurs["accent"] if role == "accent" else couleurs["neutre"]
    ax.add_patch(FancyBboxPatch((x, y), largeur, hauteur, boxstyle="round,pad=0,rounding_size=1.2",
                                facecolor=fond, alpha=0.16 if role == "accent" else 0.35, edgecolor="none"))
    ax.add_patch(FancyBboxPatch((x, y), largeur, hauteur, boxstyle="round,pad=0,rounding_size=1.2",
                                facecolor="none", edgecolor=bord, linewidth=1.1))
    ax.text(x + largeur / 2, y + hauteur / 2, texte, ha="center", va="center", fontsize=taille,
            color=couleurs["texte"], fontweight="semibold" if gras else "normal", linespacing=1.35)


def fleche(ax, depart, arrivee, couleurs):
    ax.annotate("", xy=arrivee, xytext=depart,
                arrowprops=dict(arrowstyle="-|>", color=couleurs["trait"], linewidth=1.1, shrinkA=0, shrinkB=0,
                                mutation_scale=11))


def mini_table(ax, x, y, colonnes, ligne_choisie, couleur_choisie, couleurs, lignes=5, cote=1.25, ecart=0.35):
    """Une table de plongements dessinée en petit : des lignes de cases, dont une ligne lue."""
    for ligne in range(lignes):
        for colonne in range(colonnes):
            choisie = ligne == ligne_choisie
            ax.add_patch(Rectangle((x + colonne * (cote + ecart), y + (lignes - 1 - ligne) * (cote + ecart)), cote, cote,
                                   facecolor=couleur_choisie if choisie else couleurs["neutre"],
                                   edgecolor="none", alpha=1 if choisie else 0.6))


# ---------------------------------------------------------------------------------------------------------------------
def tracer_trajets_par_mois(couleurs):
    mois = pd.read_csv(DOSSIER_RESULTATS / "trajets_par_mois.csv")
    couleur_du_role = {"entrainement": couleurs["accent"], "validation": couleurs["second"],
                       "test": couleurs["troisieme"], "hors etude": couleurs["neutre"]}
    figure, ax = plt.subplots(figsize=(9, 4.2))
    ax.bar(mois["mois"], mois["trajets"] / 1e6, color=mois["role"].map(couleur_du_role), width=0.72)
    ax.set_xticks(mois["mois"], NOMS_DES_MOIS)
    ax.yaxis.set_major_formatter(en_francais(1))
    ax.set_ylabel("trajets (millions)")
    ax.grid(axis="x", visible=False)
    millions = mois.set_index("mois")["trajets"] / 1e6
    for debut, fin, texte, couleur in [(4, 8, "Entraînement\n1 000 000 trajets tirés", "accent"),
                                       (9, 9, "Validation\n200 000", "second"),
                                       (10, 10, "Test scellé\n200 000", "troisieme")]:
        hauteur = millions.loc[debut:fin].max() + 0.12
        ax.plot([debut - 0.36, fin + 0.36], [hauteur, hauteur], color=couleurs[couleur], linewidth=2, solid_capstyle="butt")
        ax.text((debut + fin) / 2, hauteur + 0.06, texte, ha="center", va="bottom", fontsize=9, color=couleurs["texte"])
    ax.set_ylim(0, millions.max() + 0.75)
    return figure


def tracer_schema_reseau(couleurs):
    figure, ax = plt.subplots(figsize=(11, 4.9))
    ax.set_xlim(0, 110)
    ax.set_ylim(-5.5, 52)
    ax.set_axis_off()

    # 1. Le trajet : des adresses et une mesure
    entrees = [("départ", "station n° 388"), ("arrivée", "station n° 172"), ("heure", "8 h"), ("jour", "mardi"),
               ("distance", "1,2 km")]
    hauteurs = [43, 33, 23, 15, 5]
    ax.text(9, 50.5, "1 · Le trajet", ha="center", fontsize=10, fontweight="semibold", color=couleurs["texte"])
    for (nom, valeur), y in zip(entrees, hauteurs):
        boite(ax, 1, y - 2.6, 16, 5.2, f"{nom}\n{valeur}", couleurs, taille=8.5)

    # 2. Les tables : chaque adresse va chercher sa ligne
    ax.text(37, 50.5, "2 · Quatre tables apprises", ha="center", fontsize=10, fontweight="semibold", color=couleurs["texte"])
    tables = [("Départs", "1 172 × 8", 8, couleurs["accent"]), ("Arrivées", "1 172 × 8", 8, couleurs["accent"]),
              ("Heures", "24 × 4", 4, couleurs["trait"]), ("Jours", "7 × 3", 3, couleurs["trait"])]
    for (nom, taille, colonnes, couleur), y in zip(tables, hauteurs[:4]):
        mini_table(ax, 25, y - 4.0, colonnes, 2, couleur, couleurs, cote=1.15, ecart=0.32)
        ax.text(38.5, y + 0.9, nom, fontsize=9, color=couleurs["texte"], fontweight="semibold", va="center")
        ax.text(38.5, y - 1.9, taille, fontsize=8.5, color=couleurs["secondaire"], va="center")
        fleche(ax, (17.5, y), (24.2, y), couleurs)
    ax.text(31, 5, "telle quelle", ha="center", va="center", fontsize=8.5, color=couleurs["secondaire"], style="italic")
    fleche(ax, (17.5, 5), (24.5, 5), couleurs)

    # 3. Le collage : 24 nombres
    ax.text(57, 50.5, "3 · Collés", ha="center", fontsize=10, fontweight="semibold", color=couleurs["texte"])
    morceaux = [couleurs["accent"]] * 16 + [couleurs["trait"]] * 7 + [couleurs["second"]]
    cote = 1.5
    for k, couleur in enumerate(morceaux):
        ax.add_patch(Rectangle((55.5, 46 - k * (cote + 0.25) - cote), cote * 2, cote, facecolor=couleur, edgecolor="none",
                               alpha=0.9))
    ax.text(57, 1.6, "24 nombres", ha="center", fontsize=8.5, color=couleurs["secondaire"])
    for y in hauteurs[:4]:
        fleche(ax, (49, y), (54.5, min(y, 45)), couleurs)
    fleche(ax, (37.5, 5), (54.5, 5.5), couleurs)

    # 4. Les couches : 64, 32, 1
    ax.text(77, 50.5, "4 · Trois couches", ha="center", fontsize=10, fontweight="semibold", color=couleurs["texte"])
    colonnes_de_points = [(68, 14, "64"), (78, 9, "32"), (87, 1, "1")]
    positions = []
    for x, nombre, etiquette in colonnes_de_points:
        ys = [25] if nombre == 1 else [44 - k * (38 / (nombre - 1)) for k in range(nombre)]
        positions.append([(x, y) for y in ys])
        ax.text(x, 1.6, etiquette, ha="center", fontsize=8.5, color=couleurs["secondaire"])
    for gauche, droite in zip(positions, positions[1:]):
        for a in gauche:
            for b in droite:
                ax.plot([a[0], b[0]], [a[1], b[1]], color=couleurs["trait"], linewidth=0.4, alpha=0.25)
    for colonne in positions:
        for x, y in colonne:
            ax.add_patch(plt.Circle((x, y), 0.75, facecolor=plt.rcParams["axes.facecolor"], edgecolor=couleurs["trait"],
                                    linewidth=0.9, zorder=3))
    for y in (44, 30, 16):
        fleche(ax, (59.5, y), (66.6, y), couleurs)
    ax.text(77, -0.8, "ReLU entre les couches", ha="center", fontsize=8, color=couleurs["secondaire"])

    # 5. La sortie
    ax.text(100, 50.5, "5 · La durée", ha="center", fontsize=10, fontweight="semibold", color=couleurs["texte"])
    fleche(ax, (88.2, 25), (92.6, 25), couleurs)
    boite(ax, 93, 21.5, 14, 7, "log de la durée", couleurs, taille=8.5)
    fleche(ax, (100, 21.1), (100, 14.9), couleurs)
    ax.text(101.2, 18, "exp", va="center", fontsize=8.5, color=couleurs["secondaire"])
    boite(ax, 93, 7.5, 14, 7, "minutes", couleurs, role="accent", taille=9.5, gras=True)
    ax.text(1, -3.6, "Appris pendant l'entraînement : les quatre tables et les poids des couches, "
            "soit 22 582 paramètres, dont 83 % dans les deux tables de stations.",
            fontsize=8.5, color=couleurs["secondaire"])
    return figure


def tracer_erreurs_modeles(couleurs):
    erreurs = pd.read_csv(DOSSIER_RESULTATS / "erreurs_validation_test.csv", index_col=0)["test (octobre)"]
    erreurs = erreurs.sort_values(ascending=False)
    role = {"Médiane": "neutre", "Distance ÷ vitesse": "neutre", "Boosting": "trait",
            "Réseau, distance donnée": "accent", "Réseau carte": "accent"}
    figure, ax = plt.subplots(figsize=(8, 3.6))
    barres = ax.barh(erreurs.index, erreurs.values, color=[couleurs[role[nom]] for nom in erreurs.index], height=0.62)
    for barre, nom in zip(barres, erreurs.index):
        if nom == "Réseau carte":
            barre.set_alpha(0.55)
    for y, valeur in enumerate(erreurs.values):
        ax.text(valeur + 0.08, y, f"{virgule(valeur)} min", va="center", fontsize=9.5, color=couleurs["texte"])
    ax.set_xlim(0, erreurs.max() * 1.18)
    ax.xaxis.set_major_formatter(en_francais(0))
    ax.set_xlabel("erreur absolue moyenne sur le test d'octobre (minutes)")
    ax.grid(axis="y", visible=False)
    ax.tick_params(axis="y", length=0)
    return figure


def tracer_pas_apprentissage(couleurs):
    epoques = pd.read_csv(DOSSIER_RESULTATS / "erreurs_par_epoque.csv")
    validation = pd.read_csv(DOSSIER_RESULTATS / "erreurs_validation_test.csv", index_col=0)["validation (septembre)"]
    figure, (gauche, droite) = plt.subplots(1, 2, figsize=(11, 4), gridspec_kw={"width_ratios": [1, 1.15]})

    une_epoque = epoques[epoques["epoque"] == 1].set_index("reglage")["erreur_validation_min"]
    ordre = ["adam 0,0001", "sgd 0,01", "adam 0,003", "adam 0,1"]
    etiquettes = {"adam 0,0001": "Adam, pas de 0,0001", "sgd 0,01": "SGD, pas de 0,01",
                  "adam 0,003": "Adam, pas de 0,003", "adam 0,1": "Adam, pas de 0,1"}
    valeurs = une_epoque.loc[ordre]
    gauche.barh([etiquettes[r] for r in ordre], valeurs.values, height=0.6,
                color=[couleurs["accent"] if r == "adam 0,003" else couleurs["neutre"] for r in ordre])
    for y, valeur in enumerate(valeurs.values):
        gauche.text(valeur + 0.15, y, virgule(valeur), va="center", fontsize=9, color=couleurs["texte"])
    mediane = validation["Médiane"]
    gauche.axvline(mediane, color=couleurs["second"], linewidth=1.2, linestyle=(0, (4, 3)))
    gauche.text(mediane + 0.15, 3.42, f"règle de la médiane\n{virgule(mediane)} min", fontsize=8.5,
                color=couleurs["second"], va="center")
    gauche.set_xlim(0, valeurs.max() * 1.15)
    gauche.set_title("Après une époque")
    gauche.set_xlabel("erreur de validation (minutes)")
    gauche.grid(axis="y", visible=False)
    gauche.tick_params(axis="y", length=0)
    gauche.xaxis.set_major_formatter(en_francais(0))

    for reglage, couleur, nom in [("adam 0,003", couleurs["accent"], "pas de 0,003"),
                                  ("adam 0,1", couleurs["second"], "pas de 0,1")]:
        courbe = epoques[epoques["reglage"] == reglage]
        droite.plot(courbe["epoque"], courbe["erreur_validation_min"], color=couleur, marker="o", markersize=4.5)
        droite.text(5.12, courbe["erreur_validation_min"].iloc[-1], nom, color=couleur, fontsize=9, va="center")
    boosting = validation["Boosting"]
    droite.axhline(boosting, color=couleurs["trait"], linewidth=1, linestyle=(0, (4, 3)))
    droite.text(1, boosting - 0.035, f"boosting : {virgule(boosting)}", fontsize=8.5, color=couleurs["trait"], va="top")
    droite.set_xticks(range(1, 6))
    droite.set_xlim(0.8, 5.9)
    droite.set_ylim(boosting - 0.12, 4.12)
    droite.yaxis.set_major_formatter(en_francais(1))
    droite.set_title("Adam sur cinq époques")
    droite.set_xlabel("époque")
    droite.set_ylabel("erreur de validation (minutes)")
    figure.tight_layout(w_pad=3)
    return figure


def tracer_deux_architectures(couleurs):
    cartes = pd.read_csv(DOSSIER_RESULTATS / "cartes_apprises.csv", index_col=0)
    test = pd.read_csv(DOSSIER_RESULTATS / "erreurs_validation_test.csv", index_col=0)["test (octobre)"]
    figure, ax = plt.subplots(figsize=(11, 5.8))
    ax.set_xlim(0, 110)
    ax.set_ylim(0, 59)
    ax.set_axis_off()

    def resultat(y, ressemblance, erreur, couleur_du_chiffre, detail=None):
        ax.text(80, y + 5.2, "ressemblance avec la vraie carte", fontsize=8.5, color=couleurs["secondaire"])
        ax.text(80, y, virgule(ressemblance), fontsize=18, fontweight="semibold", color=couleur_du_chiffre)
        ax.text(93, y + 0.3, f"erreur sur le test\n{virgule(erreur)} min", fontsize=8.5, color=couleurs["secondaire"])
        if detail:
            ax.text(80, y - 4.2, detail, fontsize=8.5, color=couleurs["secondaire"])

    # A · la distance est donnée : le réseau n'a pas besoin de savoir où sont les stations
    ax.text(1, 56, "A · La distance est donnée", fontsize=10.5, fontweight="semibold", color=couleurs["texte"])
    entrees_a = [("départ → 8 nombres", "neutre", 47.5), ("arrivée → 8 nombres", "neutre", 42),
                 ("heure, jour", "neutre", 36.5), ("distance (km)", "accent", 31)]
    for texte, role, y in entrees_a:
        boite(ax, 1, y, 19, 4.4, texte, couleurs, role=role, taille=8.5, gras=role == "accent")
        fleche(ax, (20.5, y + 2.2), (42.5, 41), couleurs)
    boite(ax, 43, 37.5, 15, 7, "couches\n64 · 32 · 1", couleurs, taille=8.5)
    fleche(ax, (58.5, 41), (62.5, 41), couleurs)
    boite(ax, 63, 37.5, 10, 7, "durée", couleurs, taille=9)
    resultat(39.5, cartes.loc["distance donnee", "spearman_distances_entre_stations"], test["Réseau, distance donnée"],
             couleurs["texte"])

    ax.plot([1, 109], [27.5, 27.5], color=couleurs["neutre"], linewidth=0.8)

    # B · la distance est retirée : il doit placer chaque station sur sa propre carte
    ax.text(1, 24, "B · Pas de distance : une seule table de positions (x, y)", fontsize=10.5, fontweight="semibold",
            color=couleurs["texte"])
    boite(ax, 1, 15.5, 19, 4.4, "départ → (x, y)", couleurs, taille=8.5)
    boite(ax, 1, 10, 19, 4.4, "arrivée → (x, y)", couleurs, taille=8.5)
    boite(ax, 1, 2, 19, 4.4, "heure, jour", couleurs, taille=8.5)
    boite(ax, 24, 11.5, 14, 7, "écart entre les\ndeux positions", couleurs, role="accent", taille=8.5, gras=True)
    fleche(ax, (20.5, 17.7), (23.5, 15.8), couleurs)
    fleche(ax, (20.5, 12.2), (23.5, 14.2), couleurs)
    fleche(ax, (38.5, 15), (42.5, 14.5), couleurs)
    fleche(ax, (20.5, 4.2), (42.5, 12.5), couleurs)
    boite(ax, 43, 10, 15, 7, "couches\n32 · 1", couleurs, taille=8.5)
    fleche(ax, (58.5, 13.5), (62.5, 13.5), couleurs)
    boite(ax, 63, 10, 10, 7, "durée", couleurs, taille=9)
    resultat(12, cartes.loc["carte", "spearman_distances_entre_stations"], test["Réseau carte"], couleurs["accent"],
             f"distance au centre : {virgule(cartes.loc['carte', 'spearman_distance_au_centre'])}")
    return figure


def tracer_compromis_local(couleurs):
    mesures = pd.read_csv(DOSSIER_RESULTATS / "mesures_locales.csv", index_col=0)
    test = pd.read_csv(DOSSIER_RESULTATS / "erreurs_validation_test.csv", index_col=0)["test (octobre)"]
    panneaux = [
        ("Erreur sur le test (min)", test["Boosting"], test["Réseau, distance donnée"], 2),
        ("Taille du modèle (Ko)", mesures.loc["taille_ko", "boosting"], mesures.loc["taille_ko", "reseau"], 0),
        ("Prédire un trajet (ms)", mesures.loc["predire_1_trajet_ms", "boosting"], mesures.loc["predire_1_trajet_ms", "reseau"], 2),
        ("Prédire 200 000 trajets (s)", mesures.loc["predire_200000_trajets_s", "boosting"],
         mesures.loc["predire_200000_trajets_s", "reseau"], 3),
        ("Entraînement (s)", mesures.loc["entrainement_s", "boosting"], mesures.loc["entrainement_s", "reseau"], 1),
    ]
    figure, axes = plt.subplots(1, len(panneaux), figsize=(11, 3.4))
    for ax, (titre, boosting, reseau, decimales) in zip(axes, panneaux):
        ax.bar([0, 1], [boosting, reseau], color=[couleurs["neutre"], couleurs["accent"]], width=0.62)
        for x, valeur in enumerate((boosting, reseau)):
            ax.text(x, valeur * 1.03, virgule(valeur, decimales), ha="center", va="bottom", fontsize=9.5,
                    color=couleurs["texte"])
        ax.set_xticks([0, 1], ["boosting", "réseau"])
        ax.set_ylim(0, max(boosting, reseau) * 1.25)
        ax.set_yticks([])
        ax.spines["left"].set_visible(False)
        ax.grid(False)
        ax.tick_params(axis="x", length=0)
        ax.set_title(titre, fontsize=9.5, loc="center")
    figure.tight_layout(w_pad=2)
    figure.text(0.5, -0.04, "Plus bas = mieux, sur les cinq mesures. Processeur seul (Intel Core i5 de 11e génération, "
                "4 cœurs), aucun GPU.", ha="center", fontsize=9, color=couleurs["secondaire"])
    return figure


FIGURES = {
    "trajets_par_mois": tracer_trajets_par_mois,
    "schema_reseau": tracer_schema_reseau,
    "erreurs_modeles": tracer_erreurs_modeles,
    "pas_apprentissage": tracer_pas_apprentissage,
    "deux_architectures": tracer_deux_architectures,
    "compromis_local": tracer_compromis_local,
}

if __name__ == "__main__":
    charger_charte()
    for nom, tracer in FIGURES.items():
        sauver_clair_et_sombre(tracer, str(DOSSIER_RESULTATS / nom))
        print(f"resultats/{nom}_clair.png et _sombre.png")
