"""Entraîne le même petit réseau avec micrograd et avec PyTorch, sur les débits de la station 1, puis compare les pertes.

Usage, depuis la racine du dépôt :
    .venv/Scripts/python archives/stations/02-retropropagation/comparer_avec_pytorch.py

Mêmes sections, mêmes poids de départ, même pas d'apprentissage : si les deux moteurs font le même calcul,
leurs deux courbes de perte se superposent. Écrit `comparaison_pertes.csv` à côté du script.
"""
import csv
import math
import random
import sys
import time
from pathlib import Path

import torch

from moteur_micrograd import MLP

DOSSIER_STATION = Path(__file__).resolve().parent
CHEMIN_DONNEES = DOSSIER_STATION.parent / "01-reseau-neurones" / "donnees" / "sections_2025.csv"
CHEMIN_RESULTATS = DOSSIER_STATION / "comparaison_pertes.csv"

COLONNES_ENTREE = ["djma", "djme", "djmh"]
COLONNE_CIBLE = "trentieme_heure"
# micrograd crée une Value par opération : 200 sections suffisent pour comparer sans attendre des heures.
NOMBRE_SECTIONS = 200
TAILLES_DES_COUCHES = [4, 4, 1]
PAS_APPRENTISSAGE = 0.1
NOMBRE_EPOQUES = 200
GRAINE = 0


def lire_sections():
    if not CHEMIN_DONNEES.exists():
        sys.exit(f"Données introuvables : {CHEMIN_DONNEES}. Lancer d'abord archives/stations/01-reseau-neurones/preparer_donnees.py.")
    with open(CHEMIN_DONNEES, encoding="utf-8") as fichier:
        sections = list(csv.DictReader(fichier))
    random.Random(GRAINE).shuffle(sections)
    return sections[:NOMBRE_SECTIONS]


def preparer_entrees_et_cibles(sections):
    # Logarithme : les débits vont d'une centaine à des dizaines de milliers de véhicules.
    # Sans lui, les autoroutes écraseraient tout le reste dans la perte, comme à la station 1.
    entrees_log = [[math.log10(float(section[colonne])) for colonne in COLONNES_ENTREE] for section in sections]
    cibles_log = [math.log10(float(section[COLONNE_CIBLE])) for section in sections]

    # Entrées centrées-réduites, colonne par colonne : même changement d'unités qu'à la station 1.
    moyennes = [sum(ligne[k] for ligne in entrees_log) / len(entrees_log) for k in range(len(COLONNES_ENTREE))]
    ecarts_types = [
        math.sqrt(sum((ligne[k] - moyennes[k]) ** 2 for ligne in entrees_log) / (len(entrees_log) - 1))
        for k in range(len(COLONNES_ENTREE))
    ]
    entrees = [[(ligne[k] - moyennes[k]) / ecarts_types[k] for k in range(len(COLONNES_ENTREE))] for ligne in entrees_log]

    # La dernière couche finit par tanh, qui ne sort qu'entre -1 et 1 : la cible est ramenée entre -0,9 et 0,9.
    minimum, maximum = min(cibles_log), max(cibles_log)
    cibles = [-0.9 + 1.8 * (valeur - minimum) / (maximum - minimum) for valeur in cibles_log]
    return entrees, cibles


def copier_vers_pytorch(reseau_micrograd):
    """Construit le même réseau en PyTorch, avec exactement les poids de départ tirés par micrograd."""
    couches = []
    for couche in reseau_micrograd.layers:
        nombre_entrees, nombre_neurones = len(couche.neurons[0].w), len(couche.neurons)
        lineaire = torch.nn.Linear(nombre_entrees, nombre_neurones, dtype=torch.float64)
        with torch.no_grad():
            # Une ligne de la matrice = les poids d'un Neuron.
            lineaire.weight.copy_(torch.tensor([[w.data for w in neurone.w] for neurone in couche.neurons], dtype=torch.float64))
            lineaire.bias.copy_(torch.tensor([neurone.b.data for neurone in couche.neurons], dtype=torch.float64))
        couches += [lineaire, torch.nn.Tanh()]
    return torch.nn.Sequential(*couches)


def entrainer_micrograd(reseau, entrees, cibles):
    pertes = []
    for _ in range(NOMBRE_EPOQUES):
        predictions = [reseau(x) for x in entrees]
        perte = sum((prediction - cible) ** 2 for prediction, cible in zip(predictions, cibles)) * (1 / len(cibles))
        for parametre in reseau.parameters():
            parametre.grad = 0.0
        perte.backward()
        for parametre in reseau.parameters():
            parametre.data += -PAS_APPRENTISSAGE * parametre.grad
        pertes.append(perte.data)
    return pertes


def entrainer_pytorch(reseau, entrees, cibles):
    tenseur_entrees = torch.tensor(entrees, dtype=torch.float64)
    tenseur_cibles = torch.tensor(cibles, dtype=torch.float64).unsqueeze(1)
    optimiseur = torch.optim.SGD(reseau.parameters(), lr=PAS_APPRENTISSAGE)
    pertes = []
    for _ in range(NOMBRE_EPOQUES):
        perte = ((reseau(tenseur_entrees) - tenseur_cibles) ** 2).mean()
        optimiseur.zero_grad()
        perte.backward()
        optimiseur.step()
        pertes.append(perte.item())
    return pertes


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    entrees, cibles = preparer_entrees_et_cibles(lire_sections())

    random.seed(GRAINE)
    reseau_micrograd = MLP(len(COLONNES_ENTREE), TAILLES_DES_COUCHES)
    # Copie AVANT l'entraînement : les deux moteurs partent des mêmes poids.
    reseau_pytorch = copier_vers_pytorch(reseau_micrograd)
    # Passage à blanc sur une copie jetable : au tout premier appel, PyTorch charge des modules
    # pendant quelques secondes, ce qui fausserait le chronomètre.
    entrainer_pytorch(copier_vers_pytorch(reseau_micrograd), entrees, cibles)

    debut = time.perf_counter()
    pertes_micrograd = entrainer_micrograd(reseau_micrograd, entrees, cibles)
    duree_micrograd = time.perf_counter() - debut

    debut = time.perf_counter()
    pertes_pytorch = entrainer_pytorch(reseau_pytorch, entrees, cibles)
    duree_pytorch = time.perf_counter() - debut

    ecart_maximal = max(abs(a - b) for a, b in zip(pertes_micrograd, pertes_pytorch))
    with open(CHEMIN_RESULTATS, "w", newline="", encoding="utf-8") as fichier:
        ecrivain = csv.writer(fichier)
        ecrivain.writerow(["epoque", "perte_micrograd", "perte_pytorch"])
        for epoque, (perte_micrograd, perte_pytorch) in enumerate(zip(pertes_micrograd, pertes_pytorch), start=1):
            ecrivain.writerow([epoque, f"{perte_micrograd:.10f}", f"{perte_pytorch:.10f}"])

    print(f"{len(cibles)} sections, réseau 3 → {' → '.join(map(str, TAILLES_DES_COUCHES))}, "
          f"{len(reseau_micrograd.parameters())} paramètres, {NOMBRE_EPOQUES} époques, pas {PAS_APPRENTISSAGE}")
    print(f"Perte micrograd : {pertes_micrograd[0]:.4f} → {pertes_micrograd[-1]:.4f}  en {duree_micrograd:.1f} s")
    print(f"Perte PyTorch   : {pertes_pytorch[0]:.4f} → {pertes_pytorch[-1]:.4f}  en {duree_pytorch:.2f} s")
    print(f"Plus grand écart entre les deux pertes : {ecart_maximal:.1e}")
    print(f"Résultats : {CHEMIN_RESULTATS}")


if __name__ == "__main__":
    main()
