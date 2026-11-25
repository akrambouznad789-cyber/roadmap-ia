# Roadmap IA

Un parcours public en intelligence artificielle : deux classes intensives de 140 jours, menées en parallèle, et les projets faits avant elles.

**Site : https://akrambouznad789-cyber.github.io/roadmap-ia/**

## Les deux classes

| Classe | En bref | Langue | Liens |
|---|---|---|---|
| Intensive AI Engineering Class | Construire avec des modèles : des données jusqu'à un modèle de langage ouvert mis en service en local, en 9 phases | français | [route](https://akrambouznad789-cyber.github.io/intensive-ai-engineering-class/) · [dépôt](https://github.com/akrambouznad789-cyber/intensive-ai-engineering-class) |
| Intensive Inference Engineering Class | Faire tourner les modèles sur sa propre machine : mémoire, quantification, service, jusqu'à une appliance privée, en 6 phases | anglais | [route](https://akrambouznad789-cyber.github.io/intensive-inference-engineering-class/) · [dépôt](https://github.com/akrambouznad789-cyber/intensive-inference-engineering-class) |

Les deux classes avancent au même numéro de jour, environ une heure chacune par jour. Une journée suit toujours le même ordre : la théorie d'abord (un schéma, un mini-exemple chiffré, un pseudo-code), une démo interactive, une pratique qui produit une figure ou une mesure, puis quelques phrases sur ce qui a été compris. Chaque projet vise un modèle qui tourne en local.

## Avant les classes

### Projets d'application

Chaque projet porte le nom de ses méthodes ; le jeu de données n'est que le cas pratique. Le projet P4 (tokenisation BPE et mini-Transformer) se termine pendant la phase 3 de l'Intensive AI Engineering Class.

| Projet | Question | Méthodes |
|---|---|---|
| [P1 · Boosting, validation et fuites](projets/P1-boosting-validation/) | Au moment de la commande, peut-on prédire qu'une livraison sera en retard ? | Boosting de gradient, validation temporelle, détection de fuite |
| [P2 · Clustering et différence de différences](projets/P2-clustering-did/) | Les stations BIXI ont-elles des profils d'usage ? Le REV Saint-Denis a-t-il pris des cyclistes à la piste Brébeuf ? | K-moyennes, ACP, différence de différences |
| [P3 · Réseau PyTorch et plongements](projets/P3-pytorch-plongements/) | Un réseau qui apprend la durée des trajets BIXI redessine-t-il la carte de Montréal dans ses plongements de stations ? | Réseau PyTorch, plongements, boosting de gradient, validation temporelle, mesure en local |

### Stations

| Station | Exemple | Page |
|---|---|---|
| 1 · Réseaux de neurones : perceptron multicouche | Estimation du débit à la 30e heure à partir des débits de circulation publics du Québec | [Voir](https://akrambouznad789-cyber.github.io/roadmap-ia/parcelles/01-reseau-neurones/) |
| 2 · Rétropropagation et différentiation automatique | Un moteur de rétropropagation maison entraîne un petit réseau sur 200 sections de route du Québec, avec les mêmes pertes que PyTorch | [Voir](https://akrambouznad789-cyber.github.io/roadmap-ia/parcelles/02-retropropagation/) |

Le code de chaque station est rangé dans [`archives/stations/`](archives/stations/).

## Contenu du dépôt

| Dossier | Contenu |
|---|---|
| `docs/` | Le site : la page d'accueil des deux classes et les pages des stations |
| `projets/` | Les projets d'application, un dossier par projet : carnets, résultats et README |
| `style/` | La charte commune des figures |
| `archives/stations/` | Le code et les résultats de chaque station |
| `outils/`, `tests/` | Outils de mesure et de vérification des pages avant publication, avec leurs tests |
| `gabarits/` | Le modèle des pages de station |

## Données

Les données brutes ne sont pas versionnées, seulement les résultats. Chaque source est créditée sur la page de son exemple.
