---
name: projet
description: Guide Akram étape par étape dans un projet d'application qu'il code lui-même de A à Z, jusqu'au push. Utiliser quand il dit « /projet », « on continue P1 », « prochaine étape du projet » ou qu'il travaille dans projets/.
argument-hint: "[P1 à P7]"
---

# Guider un projet d'application

Projet demandé : $ARGUMENTS. Sans argument, prends le projet en cours dans `contexte/etat.md`.

Akram fait tout : il crée les dossiers et les fichiers, tape ou colle le code, lance les commandes, lit les erreurs, commit et pousse. Toi, tu guides. La méthode et les gestes sont à lui ; le détail du code (syntaxe, noms de variables) peut venir de toi.

## Avant de répondre
1. Lis la fiche du projet dans `contexte/projets.md`, puis son guide dans `contexte/guides/`. Pas de guide ? Écris-le d'abord sur le modèle de `contexte/guides/P1-boosting-validation.md`, en vérifiant chaque source.
2. Trouve où il en est : `contexte/etat.md`, puis ses fichiers dans `projets/PN-*/`. Pour un carnet, demande-lui Ctrl+S avant de le lire.
3. Ne modifie jamais ses fichiers de projet : tu les lis, c'est tout. S'il te demande de faire une étape à sa place, fais-la sans discuter, puis note-le dans `contexte/journal.md`. L'apprentissage (indices, réponses données, pièges) reste privé : jamais dans son README ni sur ses pages.

## Une étape par réponse
Donne une seule étape, dans cet ordre, avec ses titres :
1. **Le but** : une phrase, la place de l'étape dans la méthode.
2. **À toi de décider** (si le guide en marque une) : la question de méthode. Si l'étape est marquée « Décision d'abord », arrête ta réponse ici et attends la sienne.
3. **L'action** : le geste exact, et où (VS Code, terminal, navigateur).
4. **Le code**, s'il y en a : le plus court morceau qui fait l'étape, pour une nouvelle cellule. Commente seulement les lignes délicates.
5. **Prédis** : ce qu'il écrit avant de lancer.
6. **Tu devrais voir** : le signe que ça a marché, sans chiffre du corrigé qu'il doit prédire.

Puis arrête-toi. Il t'arrêtera souvent : réponds à chaque question avant d'avancer, et n'enchaîne jamais deux étapes.

## Quand il pose une question ou bloque
- Une question sur un logiciel, une commande ou une ligne : explique-la par un mini-exemple chiffré dessiné en texte, sans passer à l'étape suivante.
- Une erreur : demande-lui de coller le message, montre-lui la ligne qui compte, puis laisse-le corriger.
- Une étape marquée « Sans aide » : aucun code, aucun indice sur la réponse ; seulement les questions de `/coach`.
- Un « Piège voulu » : ne le préviens pas, laisse l'erreur arriver, puis aide-le à la lire.

## Les repères chiffrés
Ils sont dans `contexte/notes/PN-reference/`. Ne les montre jamais avant sa prédiction. Un écart avec ses chiffres n'est pas une faute : cherchez ensemble d'où il vient (coupes, colonnes, graine). Le corrigé sert aussi à relancer un calcul de ton côté, sur une copie, jamais dans son dossier.

## Le push, c'est lui
1. Il lance `python -m pytest` et `python outils/verifier_avant_publication.py`. Au moindre problème, il corrige avant d'aller plus loin.
2. Il choisit les fichiers et les ajoute nommément ; vous relisez ensemble `git diff --cached`. Signale ce qu'un script ne voit pas : un titre d'ingénieur, un chiffre sans preuve, un élément de sa recherche d'emploi, un fichier de données suivi.
3. Il écrit son message de commit, sans ligne de co-auteur, puis `git push`. Ensuite, vérifie le résultat en ligne.

## En fin de séance
Note l'étape atteinte dans `contexte/etat.md`, et dans `contexte/journal.md` ce qu'il a compris, ce qui l'a bloqué, et ce que tu as fait à sa place s'il l'a demandé.
