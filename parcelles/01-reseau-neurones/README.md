# Station 1 · Estimation du débit à la 30e heure

Un perceptron multicouche (3 → 32 → 16 → 1) estime le débit à la 30e heure d'une section de route à partir de son DJMA, de son DJME et de son DJMH. Il est comparé à une règle simple (ratio médian × DJMA) et à une forêt aléatoire. [Page de l'exemple](https://akrambouznad789-cyber.github.io/roadmap-ia/parcelles/01-reseau-neurones/)

## Fichiers

| Fichier | Rôle |
|---|---|
| [`preparer_donnees.py`](preparer_donnees.py) | Extrait du GeoPackage du ministère les sections complètes de l'année la plus récente |
| [`reseau_neurones_30e_heure.py`](reseau_neurones_30e_heure.py) | Entraîne le réseau, puis compare les trois modèles sur l'échantillon de test |
| [`analyser_familles.py`](analyser_familles.py) | Regroupe les sections par saisonnalité (DJME / DJMH) |
| [`resultats.csv`](resultats.csv) | Erreur moyenne de chaque modèle, en véhicules et en % |
| [`courbe_apprentissage.csv`](courbe_apprentissage.csv) | Coût d'entraînement et de test toutes les 10 époques |
| [`familles_saisonnalite.csv`](familles_saisonnalite.csv) | Nombre de sections et ratio de pointe médian par tranche de saisonnalité |

## Données

[Débit de circulation](https://www.donneesquebec.ca/recherche/dataset/debit-de-circulation), ministère des Transports et de la Mobilité durable du Québec, licence CC BY 4.0. Le GeoPackage n'est pas versionné : le télécharger depuis Données Québec.

## Reproduire

Depuis la racine du dépôt, avec Python, PyTorch, pandas et scikit-learn :

```
python parcelles/01-reseau-neurones/preparer_donnees.py chemin/vers/DebitCirculation.gpkg
python parcelles/01-reseau-neurones/reseau_neurones_30e_heure.py
python parcelles/01-reseau-neurones/analyser_familles.py
```

La graine est fixée : les résultats sont identiques d'une exécution à l'autre.
