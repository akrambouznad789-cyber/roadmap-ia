"""Hook PreToolUse de Claude Code : bloque `git push` tant que le contenu public a un problème.

Claude Code envoie la commande en JSON sur l'entrée standard. Le code de sortie 2 refuse la commande
et renvoie le message d'erreur à Claude, qui peut alors corriger le problème.
"""
import json
import re
import sys
from pathlib import Path

CODE_SORTIE_AUTORISER = 0
CODE_SORTIE_BLOQUER = 2
MOTIF_GIT_PUSH = re.compile(r"\bgit\b[^;&|\n]*\bpush\b")


def commande_publie(commande):
    return bool(MOTIF_GIT_PUSH.search(commande))


def decider(commande, trouver_problemes):
    """Renvoie (code de sortie, message). `trouver_problemes` n'est appelé que pour un push."""
    if not commande_publie(commande):
        return CODE_SORTIE_AUTORISER, ""
    problemes = trouver_problemes()
    if not problemes:
        return CODE_SORTIE_AUTORISER, ""
    details = "\n".join(f"  - {probleme}" for probleme in problemes)
    return CODE_SORTIE_BLOQUER, f"Publication bloquée, à corriger d'abord :\n{details}"


def trouver_problemes_du_depot():
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from verifier_avant_publication import RACINE_DEPOT, lire_mots_interdits, verifier_depot

    return verifier_depot(RACINE_DEPOT, lire_mots_interdits())


def main():
    sys.stderr.reconfigure(encoding="utf-8")
    charge_utile = json.loads(sys.stdin.buffer.read())
    commande = charge_utile.get("tool_input", {}).get("command", "")
    code_sortie, message = decider(commande, trouver_problemes_du_depot)
    if message:
        print(message, file=sys.stderr)
    return code_sortie


if __name__ == "__main__":
    sys.exit(main())
