# Station 2 · Un moteur de rétropropagation maison, vérifié contre PyTorch

Un moteur de rétropropagation reproduit à partir de micrograd d'Andrej Karpathy entraîne un petit réseau (3 → 4 → 4 → 1, 41 paramètres) sur 200 sections de route du Québec. Le même réseau, construit en PyTorch avec les mêmes poids de départ, obtient les mêmes pertes à chaque époque. [Page de l'exemple](https://akrambouznad789-cyber.github.io/roadmap-ia/archives/stations/02-retropropagation/)

## Fichiers

| Fichier | Rôle |
|---|---|
| [`micrograd_a_la_main.ipynb`](micrograd_a_la_main.ipynb) | Dérivées par petits pas, gradients calculés à la main, première classe `Value` |
| [`micrograd_pytorch.ipynb`](micrograd_pytorch.ipynb) | Classe `Value` complète, vérification d'un neurone avec PyTorch, puis `Neuron`, `Layer`, `MLP` et la boucle d'entraînement |
| [`moteur_micrograd.py`](moteur_micrograd.py) | Les classes du notebook, copiées telles quelles pour être importées par un script |
| [`comparer_avec_pytorch.py`](comparer_avec_pytorch.py) | Entraîne le même réseau avec micrograd et avec PyTorch, puis compare les pertes et les durées |
| [`comparaison_pertes.csv`](comparaison_pertes.csv) | Perte des deux moteurs à chacune des 200 époques |
| [`LICENCE-micrograd.txt`](LICENCE-micrograd.txt) | Licence MIT du code d'Andrej Karpathy |

## Données

[Débit de circulation](https://www.donneesquebec.ca/recherche/dataset/debit-de-circulation), ministère des Transports et de la Mobilité durable du Québec, licence CC BY 4.0. Le script lit le CSV préparé à la station 1 (`archives/stations/01-reseau-neurones/donnees/sections_2025.csv`), qui n'est pas versionné : le produire d'abord avec `archives/stations/01-reseau-neurones/preparer_donnees.py`.

## Reproduire

Depuis la racine du dépôt, avec Python et PyTorch :

```
python archives/stations/02-retropropagation/comparer_avec_pytorch.py
```

Les sections et les poids de départ sont tirés avec une graine fixe : les pertes sont identiques d'une exécution à l'autre. Les durées dépendent de la machine.

## Licence du code repris

Les classes `Value`, `Neuron`, `Layer` et `MLP` reproduisent le code d'Andrej Karpathy ([micrograd](https://github.com/karpathy/micrograd), [nn-zero-to-hero](https://github.com/karpathy/nn-zero-to-hero)), sous licence MIT : voir [`LICENCE-micrograd.txt`](LICENCE-micrograd.txt).
