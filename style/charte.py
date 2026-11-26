"""Charte « Carte d'étude » des figures : polices, couleurs par rôle, export clair et sombre.

Usage dans un carnet (adapter le chemin vers style/) :
    import sys
    sys.path.insert(0, "../../../style")
    from charte import charger_charte, sauver_clair_et_sombre
    charger_charte()

Chaque figure s'écrit comme une fonction `tracer(couleurs)` qui renvoie la figure ;
`sauver_clair_et_sombre` la trace deux fois et enregistre `<nom>_clair.png` et `<nom>_sombre.png`,
à fond transparent. Les pages des sites, toujours sombres, affichent `_sombre` ; un README sur GitHub
affiche les deux avec une balise <picture>, selon le thème du lecteur.
Étiquettes en anglais et nombres au format anglais ; `en_francais` et `pourcentage` ne servent plus
qu'aux anciennes figures en français.
"""

from pathlib import Path

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

DOSSIER_STYLE = Path(__file__).resolve().parent
STYLE_CLAIR = [DOSSIER_STYLE / "carte-d-etude-clair.mplstyle"]
STYLE_SOMBRE = [DOSSIER_STYLE / "carte-d-etude-clair.mplstyle", DOSSIER_STYLE / "carte-d-etude-sombre.mplstyle"]

# Couleurs par rôle. « accent » = ce qu'on veut montrer ; « neutre » = le contexte (bases, comparaisons) ;
# « trait » = lignes et contours secondaires. Accent, second et troisième (saumon, menthe, bleu : l'ordre fixe
# des séries) validés pour les daltoniens avec le validateur de la compétence dataviz, sur blanc et sur le fond sombre.
COULEURS = {
    "clair": {"accent": "#A23B33", "second": "#1B9C77", "troisieme": "#3B6FC4", "neutre": "#C9C9CF", "trait": "#6B6B75",
              "texte": "#1F1F23", "secondaire": "#5E5E68"},
    "sombre": {"accent": "#C95A50", "second": "#41B490", "troisieme": "#6E9EE2", "neutre": "#55555F", "trait": "#ABABB3",
               "texte": "#F2F2F2", "secondaire": "#ABABB3"},
}


def charger_charte():
    """Fait connaître les polices (Overpass, IBM Plex) à matplotlib et applique le thème clair aux figures du carnet."""
    for police in (DOSSIER_STYLE / "polices").glob("*.ttf"):
        fm.fontManager.addfont(police)
    plt.style.use(STYLE_CLAIR)


def en_francais(decimales):
    """Graduations avec une virgule décimale : 0.75 devient 0,75 (anciennes figures en français)."""
    return FuncFormatter(lambda valeur, _position: f"{valeur:.{decimales}f}".replace(".", ","))


def pourcentage(valeur):
    """0.7054 devient « 70,5 % » (anciennes figures en français ; espace insécable avant le signe)."""
    return f"{100 * valeur:.1f} %".replace(".", ",")


def sauver_clair_et_sombre(tracer, chemin_sans_extension):
    """Enregistre la figure en deux versions transparentes ; seule la version claire reste affichée dans le carnet."""
    for theme, styles in (("sombre", STYLE_SOMBRE), ("clair", STYLE_CLAIR)):
        with plt.style.context(styles):
            figure = tracer(COULEURS[theme])
            figure.savefig(f"{chemin_sans_extension}_{theme}.png", transparent=True)
        if theme == "sombre":
            plt.close(figure)
