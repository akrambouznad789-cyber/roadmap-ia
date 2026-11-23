"""Charte « Quiet Light indigo » des figures : polices, couleurs par rôle, export clair et sombre.

Usage dans un carnet de projets/PN-nom/ :
    import sys
    sys.path.insert(0, "../../style")
    from charte import charger_charte, sauver_clair_et_sombre, en_francais
    charger_charte()

Chaque figure s'écrit comme une fonction `tracer(couleurs)` qui renvoie la figure ;
`sauver_clair_et_sombre` la trace deux fois et enregistre `<nom>_clair.png` et `<nom>_sombre.png`,
à fond transparent. Le README les affiche avec une balise <picture> : GitHub montre la version
qui correspond au thème du lecteur.
"""

from pathlib import Path

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

DOSSIER_STYLE = Path(__file__).resolve().parent
STYLE_CLAIR = [DOSSIER_STYLE / "quiet-light.mplstyle"]
STYLE_SOMBRE = [DOSSIER_STYLE / "quiet-light.mplstyle", DOSSIER_STYLE / "quiet-light-sombre.mplstyle"]

# Couleurs par rôle. « accent » = ce qu'on veut montrer ; « neutre » = le contexte (bases, comparaisons) ;
# « trait » = lignes et contours secondaires. Accent, second et troisième (indigo, orange, sarcelle : l'ordre fixe
# des séries) validés pour les daltoniens (script dataviz).
COULEURS = {
    "clair": {"accent": "#4F4FC4", "second": "#C0702A", "troisieme": "#008B7E", "neutre": "#C9C9D6", "trait": "#6B6B7E",
              "texte": "#333333", "secondaire": "#6B6B7E"},
    "sombre": {"accent": "#7C7CE8", "second": "#C47A38", "troisieme": "#2FA898", "neutre": "#4A4A5E", "trait": "#A3A3B5",
               "texte": "#E6E6EE", "secondaire": "#A3A3B5"},
}


def charger_charte():
    """Fait connaître les polices IBM Plex à matplotlib et applique le thème clair aux figures du carnet."""
    for police in (DOSSIER_STYLE / "polices").glob("*.ttf"):
        fm.fontManager.addfont(police)
    plt.style.use(STYLE_CLAIR)


def en_francais(decimales):
    """Graduations avec une virgule décimale : 0.75 devient 0,75."""
    return FuncFormatter(lambda valeur, _position: f"{valeur:.{decimales}f}".replace(".", ","))


def pourcentage(valeur):
    """0.7054 devient « 70,5 % » (espace insécable avant le signe)."""
    return f"{100 * valeur:.1f} %".replace(".", ",")


def sauver_clair_et_sombre(tracer, chemin_sans_extension):
    """Enregistre la figure en deux versions transparentes ; seule la version claire reste affichée."""
    for theme, styles in (("sombre", STYLE_SOMBRE), ("clair", STYLE_CLAIR)):
        with plt.style.context(styles):
            figure = tracer(COULEURS[theme])
            figure.savefig(f"{chemin_sans_extension}_{theme}.png", transparent=True)
        if theme == "sombre":
            plt.close(figure)
