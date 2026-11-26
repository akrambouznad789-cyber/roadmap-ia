"""Charte « Route de nuit » des figures : polices, couleurs par rôle, export clair et sombre.

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
STYLE_CLAIR = [DOSSIER_STYLE / "route-de-nuit-clair.mplstyle"]
STYLE_SOMBRE = [DOSSIER_STYLE / "route-de-nuit-clair.mplstyle", DOSSIER_STYLE / "route-de-nuit-sombre.mplstyle"]

# Couleurs par rôle. « accent » = ce qu'on veut montrer ; « neutre » = le contexte (bases, comparaisons) ;
# « trait » = lignes et contours secondaires. Accent, second et troisième (ambre, sarcelle, bleu : l'ordre fixe
# des séries) validés pour les daltoniens avec le validateur de la compétence dataviz, sur blanc et sur le fond sombre.
COULEURS = {
    "clair": {"accent": "#A8700F", "second": "#00917F", "troisieme": "#3A6FD8", "neutre": "#C9CDD6", "trait": "#6B7380",
              "texte": "#2A2F37", "secondaire": "#5F6773"},
    "sombre": {"accent": "#CB9027", "second": "#2FAE9D", "troisieme": "#5E8FE6", "neutre": "#4E5866", "trait": "#AAB2BE",
               "texte": "#ECE7DD", "secondaire": "#AAB2BE"},
}


def charger_charte():
    """Fait connaître les polices (Hanken Grotesk, IBM Plex) à matplotlib et applique le thème clair aux figures du carnet."""
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
