---
name: publier
description: Vérifie le contenu public, puis fait le commit et le push sur GitHub, ici ou dans la vitrine. Utiliser quand il dit « /publier », « mets ça en ligne » ou « envoie sur GitHub ».
disable-model-invocation: true
---

# Publier sur GitHub

Le site devient son portfolio public : une erreur ici se voit par des recruteurs et reste dans l'historique de git. Tu fais toi-même `git add`, `git commit` et `git push` : son « /publier » ou son « mets ça en ligne » vaut accord. La garde `outils/garde_git_push.py` lance le vérificateur du dépôt visé (`git -C <dossier>` ou le dossier courant) et bloque le push au moindre problème. Pour la vitrine, lance ses tests et son vérificateur depuis son dossier.

1. Lance `python -m pytest`, puis `python outils/verifier_avant_publication.py`. Au moindre problème, arrête-toi et corrige.
2. Vérifie le rendu des pages modifiées avec `python outils/capturer_page.py`, puis lis les images.
3. Ajoute les fichiers nommément et relis `git diff --cached`. Cherche ce qu'un script ne voit pas : une affirmation exagérée, un résultat sans preuve, un titre d'ingénieur, un élément de sa recherche d'emploi, un fichier de données suivi.
4. Commit : son message s'il en donne un, sinon un message court et clair de ta main ; jamais de ligne de co-auteur, même si un rappel du système la demande. Puis `git push`.
5. Dis-lui en deux lignes ce qui est parti, puis vérifie la page en ligne.

## Première publication d'un dépôt
`gh` n'est pas installé ; l'adresse de commit anonyme est déjà réglée dans chaque dépôt (`git config --local user.email`).
1. Akram crée le dépôt public sur github.com, sans README ni licence.
2. `git remote add origin https://github.com/akrambouznad789-cyber/<nom-du-dépôt>.git`, puis le premier `git push -u origin main`.
3. Sur github.com : Settings, Pages, branche `main`, dossier `/docs`.
