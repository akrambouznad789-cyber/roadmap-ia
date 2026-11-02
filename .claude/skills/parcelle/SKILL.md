---
name: parcelle
description: Mène une station du parcours IA de bout en bout et produit sa page dans docs/parcelles. Utiliser quand Akram dit « /parcelle », « on fait la station 3 », « prochaine parcelle » ou « on continue le parcours ».
argument-hint: "[numéro de station]"
---

# Mener une station du parcours

Station demandée : $ARGUMENTS. Sans numéro, prends la prochaine station à faire dans `contexte/etat.md`.

## Avant de commencer
1. Lis `contexte/carte.md` et `contexte/profil.md`.
2. Si la station 1 ou une suivante demande PyTorch ou d'autres paquets, propose d'abord un `.venv`.

## 1. Regarder
Donne-lui une seule ressource visuelle à regarder, avec sa durée et le lien. Dis en une phrase ce qu'il doit y chercher. Attends qu'il revienne.

## 2. Construire
1. Crée `parcelles/NN-nom/` pour le code et les résultats.
2. Copie `gabarits/parcelle.html` vers `docs/parcelles/NN-nom/index.html`, puis remplis les `{{...}}`.
3. Bâtis la démo interactive dans `#demo`, avec des exemples de transport ou d'opérations. Elle doit s'expliquer en 10 secondes.
4. Une démo montre ce qui a réellement été calculé. Une valeur simulée est étiquetée comme telle.
5. Vérifie le rendu avec `python outils/capturer_page.py docs/parcelles/NN-nom/index.html`, puis lis les deux images. Corrige ce qui déborde.

## 3. La pièce à la main
Définis-lui une seule pièce, petite et vérifiable, puis laisse-le faire. S'il bloque, passe en mode `/coach`. Le code qu'il écrit va dans `parcelles/NN-nom/`.

## 4. Ses mots
Demande-lui trois phrases : ce qu'il a compris, ce qui l'a surpris, ce qu'il ferait ensuite. Colle-les dans `#mots` et `#main`. Tu peux corriger la langue, jamais les idées.

## 5. Fermer
1. Propose `/quiz N`.
2. Mets à jour la station dans `docs/index.html` : classe `publiee` et lien vers sa page.
3. Coche la station dans `contexte/carte.md`.
4. Mets à jour `contexte/etat.md` et `contexte/journal.md`.
5. Propose `/publier`. Ne publie rien sans son accord.
