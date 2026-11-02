# Station 0 : mon premier LLM local

**Question :** à quelle vitesse un LLM tourne-t-il sur un portable sans carte graphique dédiée ?

## Mesurer
1. Installer [Ollama](https://ollama.com/download/windows).
2. Télécharger un petit modèle : `ollama pull llama3.2:3b`
3. Depuis la racine du dépôt : `python outils/mesurer_llm_local.py --modele llama3.2:3b --repetitions 3`

Les mesures s'ajoutent à `resultats.csv`.

## Lire le résultat
- **Jetons par seconde :** la vitesse à laquelle le modèle écrit sa réponse.
- **Chargement :** le temps pour mettre le modèle en mémoire, surtout à la première répétition.
- **Médiane :** elle exclut cette première répétition pour décrire le régime normal.

La consigne, la graine et le nombre de jetons sont fixes, afin de pouvoir comparer des modèles entre eux.
