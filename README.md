# Roadmap IA

Apprentissage de l'intelligence artificielle par étapes, des réseaux de neurones jusqu'aux agents, appliqué au transport et aux données.

**Site : https://akrambouznad789-cyber.github.io/roadmap-ia/**

## Méthode

À chaque étape, une recherche de ressources théoriques en ligne, combinée à l'intelligence agentique, permet de cerner les concepts. Viennent ensuite une exploration par le code sur un vrai cas, le lancement du code sur un cas pratique, puis la documentation des résultats et une analyse rétroactive.

## Survol du parcours

| Station | Thème | État |
|---|---|---|
| 1 | Le réseau de neurones | Publiée |
| 2 | La rétropropagation | À venir |
| 3 | Des mots aux nombres | À venir |
| 4 | L'attention et le Transformer | À venir |
| 5 | Utiliser un LLM avec rigueur | À venir |
| 6 | Le RAG | À venir |
| 7 | Les agents et leurs outils | En cours |
| 8 | L'évaluation | En cours |
| 9 | Déployer pour de vrai | En cours |

## Exemples pratiques

| Station | Exemple | Page |
|---|---|---|
| 1 | Estimation du débit à la 30e heure à partir des débits de circulation publics du Québec | [Voir](https://akrambouznad789-cyber.github.io/roadmap-ia/parcelles/01-reseau-neurones/) |

## Codes des exemples

**Station 1**, dans [`parcelles/01-reseau-neurones/`](parcelles/01-reseau-neurones/) :

| Fichier | Rôle |
|---|---|
| [`preparer_donnees.py`](parcelles/01-reseau-neurones/preparer_donnees.py) | Extrait des débits du ministère le tableau d'entraînement |
| [`reseau_neurones_30e_heure.py`](parcelles/01-reseau-neurones/reseau_neurones_30e_heure.py) | Entraîne le réseau, puis le compare à une règle simple et à une forêt aléatoire |
| [`analyser_familles.py`](parcelles/01-reseau-neurones/analyser_familles.py) | Regroupe les sections de route par saisonnalité |
| [`resultats.csv`](parcelles/01-reseau-neurones/resultats.csv), [`courbe_apprentissage.csv`](parcelles/01-reseau-neurones/courbe_apprentissage.csv), [`familles_saisonnalite.csv`](parcelles/01-reseau-neurones/familles_saisonnalite.csv) | Résultats obtenus |

## Contenu du dépôt

| Dossier | Contenu |
|---|---|
| `docs/` | Le site |
| `parcelles/` | Le code et les résultats de chaque station |
| `outils/`, `tests/` | Outils de mesure et de vérification des pages avant publication, avec leurs tests |
| `gabarits/` | Modèle de page des stations |

## Données

Les données brutes ne sont pas versionnées, seulement les résultats. Chaque source est créditée sur la page de sa station.
