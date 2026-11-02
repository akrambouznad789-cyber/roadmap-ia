---
name: publier
description: Vérifie le contenu public, montre ce qui va partir, puis publie sur GitHub avec l'accord d'Akram. Utiliser quand il dit « /publier », « mets ça en ligne » ou « envoie sur GitHub ».
disable-model-invocation: true
---

# Publier sur GitHub

Le site devient son portfolio public : une erreur ici se voit par des recruteurs et reste dans l'historique de git.

1. Lance `python -m pytest`, puis `python outils/verifier_avant_publication.py`. Au moindre problème, arrête-toi et corrige.
2. Vérifie le rendu des pages modifiées avec `python outils/capturer_page.py`, puis lis les images.
3. Relis ce qui change avec `git status` et `git diff`. Cherche ce qu'un script ne voit pas : une affirmation exagérée, un résultat sans preuve, un titre d'ingénieur, un élément de sa recherche d'emploi.
4. Montre à Akram, en quelques lignes, ce qui va partir et où. **Attends son accord explicite.**
5. Crée le commit, avec un message clair, en suivant les règles d'attribution de la session.
6. Fais le `git push`, puis vérifie la page en ligne.

## Première publication
Il n'y a pas encore de dépôt distant, et `gh` n'est pas installé.
1. Akram crée le dépôt public `roadmap-ia` sur github.com, sans README.
2. `git remote add origin https://github.com/akrambouznad789-cyber/roadmap-ia.git`
3. Après le premier push : Settings, Pages, branche `main`, dossier `/docs`.
4. Le site sera à https://akrambouznad789-cyber.github.io/roadmap-ia/
