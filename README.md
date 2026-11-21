# Roadmap IA

Apprentissage de l'intelligence artificielle par étapes, des réseaux de neurones jusqu'à l'affinage d'un modèle de langage ouvert qui tourne en local.

**Site : https://akrambouznad789-cyber.github.io/roadmap-ia/**

## Projets d'application

Chaque projet porte le nom de ses méthodes ; le jeu de données n'est que le cas pratique.

| Projet | Question | Méthodes |
|---|---|---|
| [P1 · Boosting, validation et fuites](projets/P1-boosting-validation/) | Au moment de la commande, peut-on prédire qu'une livraison sera en retard ? | Boosting de gradient, validation temporelle, détection de fuite |
| [P2 · Clustering et différence de différences](projets/P2-clustering-did/) | Les stations BIXI ont-elles des profils d'usage ? Le REV Saint-Denis a-t-il pris des cyclistes à la piste Brébeuf ? | K-moyennes, ACP, différence de différences |

## Méthode

À chaque étape, une recherche de ressources théoriques en ligne, combinée à l'intelligence agentique, permet de cerner les concepts. Viennent ensuite une exploration par le code sur un vrai cas, le lancement du code sur un cas pratique, puis la documentation des résultats et une analyse rétroactive.

## Survol du parcours

| Station | Thème | État |
|---|---|---|
| | **Fondements de l'apprentissage profond** | |
| 1 | Réseaux de neurones : perceptron multicouche | Publiée |
| 2 | Rétropropagation et différentiation automatique | Publiée |
| | **Modèles de langage** | |
| 3 | Modélisation du langage et plongements vectoriels | À venir |
| 4 | Mécanisme d'attention et architecture Transformer | À venir |
| | **Modèles ouverts : exécution et évaluation** | |
| 5 | Exécution locale de modèles ouverts | À venir |
| 6 | Intégration des LLM : prompts et sorties structurées | À venir |
| 7 | Évaluation des LLM | À venir |
| | **Spécialisation d'un modèle ouvert** | |
| 8 | Affinage supervisé : LoRA et QLoRA | À venir |
| 9 | Déploiement d'un modèle affiné | À venir |

## Exemples pratiques

| Station | Exemple | Page |
|---|---|---|
| 1 | Estimation du débit à la 30e heure à partir des débits de circulation publics du Québec | [Voir](https://akrambouznad789-cyber.github.io/roadmap-ia/parcelles/01-reseau-neurones/) |
| 2 | Un moteur de rétropropagation maison entraîne un petit réseau sur 200 sections de route du Québec, avec les mêmes pertes que PyTorch | [Voir](https://akrambouznad789-cyber.github.io/roadmap-ia/parcelles/02-retropropagation/) |

## Codes des exemples

Le code de chaque exemple est rangé par station dans [`archives/stations/`](archives/stations/).

## Contenu du dépôt

| Dossier | Contenu |
|---|---|
| `projets/` | Les projets d'application, un dossier par projet : carnets, résultats et README |
| `style/` | La charte commune des figures |
| `docs/` | Le site |
| `archives/stations/` | Le code et les résultats de chaque exemple, par station |
| `outils/`, `tests/` | Outils de mesure et de vérification des pages avant publication, avec leurs tests |
| `gabarits/` | Modèle de page des exemples |

## Données

Les données brutes ne sont pas versionnées, seulement les résultats. Chaque source est créditée sur la page de son exemple.
