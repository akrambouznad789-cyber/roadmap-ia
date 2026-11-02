---
name: expliquer
description: Explique un concept d'IA à Akram de façon visuelle, à partir de ce qu'il connaît déjà. Utiliser quand il dit « /expliquer », « je comprends pas », « c'est quoi » ou qu'il pose une question sur un concept d'IA, de ML ou d'agents.
argument-hint: "[concept]"
---

# Expliquer un concept

Concept demandé : $ARGUMENTS.

Akram est très visuel et n'aime pas les longs textes.

1. Dis le concept en **une phrase simple**, sans jargon.
2. Relie-le à ce qu'il connaît : trafic, graphes de réseau, forêts aléatoires, chaînes de montage.
3. Montre-le : un schéma en texte pour une idée courte, ou une petite page HTML interactive quand le concept bouge ou se manipule. Sauvegarde cette page dans `.captures/` : elle n'est pas publique.
4. Donne un seul exemple chiffré, assez petit pour se faire à la main.
5. Dis ce que le concept **ne fait pas**, ou l'erreur classique.
6. Termine par une seule question qui vérifie qu'il a compris.

Si une ressource de `contexte/carte.md` couvre bien le concept, donne le lien. Ne cite que des faits vérifiés, et dis-le quand tu n'es pas sûr.
