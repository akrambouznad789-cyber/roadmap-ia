"""Hook PreToolUse de Claude Code : bloque `git push` tant que le contenu public du dépôt visé a un problème.

Claude Code envoie la commande en JSON sur l'entrée standard. Le code de sortie 2 refuse la commande
et renvoie le message d'erreur à Claude, qui peut alors corriger le problème.

L'assistant IA a le droit de pousser lui-même ; cette garde est le filet.
Le dépôt visé est celui de `git -C <dossier>`, sinon celui du dernier `cd <dossier>` placé avant dans la
commande, sinon le dossier courant de la session. On y lance son propre `outils/verifier_avant_publication.py` :
le cerveau, les deux classes et la vitrine ont chacun le leur. Fichier commun au cerveau et aux deux classes.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

CODE_SORTIE_AUTORISER = 0
CODE_SORTIE_BLOQUER = 2
DELAI_MAX_DU_VERIFICATEUR_SECONDES = 50  # le hook lui-même a 60 s dans .claude/settings.json
MOTIF_SEPARATEUR_DE_COMMANDES = re.compile(r"&&|\|\||[;\n]")
MOTIF_CHEMIN = r"(?:\"[^\"]+\"|'[^']+'|[^\s\"';&|]+)"
# Un vrai `git push` : `git` en tête de commande (ou après `{`, `(`, `&`), ses options, puis `push`.
# Un texte qui parle de « git push » dans une chaîne ne déclenche donc pas la garde.
MOTIF_GIT_PUSH = re.compile(
    r"(?:^|[{(&]\s*)git(?:\.exe)?"
    r"(?:\s+-C\s+(?P<dossier>" + MOTIF_CHEMIN + r")|\s+-c\s+\S+|\s+--?[\w-]+(?:=\S+)?)*"
    r"\s+push\b",
    re.IGNORECASE,
)
MOTIF_CHANGEMENT_DE_DOSSIER = re.compile(
    r"^(?:cd|Set-Location|pushd)\s+(?:-(?:Literal)?Path\s+)?(" + MOTIF_CHEMIN + ")", re.IGNORECASE
)
MOTIF_CHEMIN_DE_GIT_BASH = re.compile(r"^/([a-zA-Z])(/|$)")


def decouper_en_commandes(commande):
    return [morceau.strip() for morceau in MOTIF_SEPARATEUR_DE_COMMANDES.split(commande)]


def commande_publie(commande):
    return any(MOTIF_GIT_PUSH.search(morceau) for morceau in decouper_en_commandes(commande))


def nettoyer_le_chemin(chemin):
    """Enlève les guillemets et traduit un chemin de Git Bash (/c/depots/...) en chemin Windows (c:/depots/...)."""
    return MOTIF_CHEMIN_DE_GIT_BASH.sub(r"\1:/", chemin.strip("\"'"))


def trouver_les_dossiers_publies(commande, dossier_courant):
    """Renvoie le dossier d'où part chaque `git push` de la commande, dans l'ordre."""
    dossier = Path(dossier_courant)
    dossiers_publies = []
    for morceau in decouper_en_commandes(commande):
        changement = MOTIF_CHANGEMENT_DE_DOSSIER.match(morceau)
        if changement:
            dossier = dossier / nettoyer_le_chemin(changement.group(1))
            continue
        publication = MOTIF_GIT_PUSH.search(morceau)
        if publication:
            option_c = publication.group("dossier")
            dossiers_publies.append(dossier / nettoyer_le_chemin(option_c) if option_c else dossier)
    return dossiers_publies


def trouver_la_racine_du_depot(dossier):
    """Remonte jusqu'au dossier qui contient `.git` ; None hors d'un dépôt."""
    for candidat in [dossier, *dossier.parents]:
        if (candidat / ".git").exists():
            return candidat
    return None


def lancer_le_verificateur_du_depot(racine):
    """Lance le vérificateur propre au dépôt ; renvoie la liste des problèmes (vide si tout va bien)."""
    verificateur = racine / "outils" / "verifier_avant_publication.py"
    if not verificateur.exists():
        return [f"{racine} n'a pas de outils/verifier_avant_publication.py : rien n'a été vérifié"]
    resultat = subprocess.run(
        [sys.executable, str(verificateur)],
        cwd=racine,
        capture_output=True,
        timeout=DELAI_MAX_DU_VERIFICATEUR_SECONDES,
    )
    if resultat.returncode == 0:
        return []
    lignes = (resultat.stdout + resultat.stderr).decode("utf-8", errors="replace").splitlines()
    sortie = "\n".join(ligne for ligne in lignes if ligne.strip())
    return [sortie or f"le vérificateur de {racine} a échoué sans message (code {resultat.returncode})"]


def decider(commande, dossier_courant, verifier_un_depot):
    """Renvoie (code de sortie, message). `verifier_un_depot(racine)` n'est appelé que pour un push."""
    problemes = []
    for dossier in trouver_les_dossiers_publies(commande, dossier_courant):
        racine = trouver_la_racine_du_depot(dossier.resolve())
        if racine is None:
            problemes.append(
                f"dépôt introuvable pour « {dossier} » : lance le push depuis le dossier du dépôt ou avec git -C <chemin>"
            )
            continue
        problemes += [f"[{racine.name}] {probleme}" for probleme in verifier_un_depot(racine)]
    if not problemes:
        return CODE_SORTIE_AUTORISER, ""
    details = "\n".join(f"  - {probleme}" for probleme in problemes)
    return CODE_SORTIE_BLOQUER, f"Publication bloquée, à corriger d'abord :\n{details}"


def main():
    sys.stderr.reconfigure(encoding="utf-8")
    charge_utile = json.loads(sys.stdin.buffer.read())
    commande = charge_utile.get("tool_input", {}).get("command", "")
    dossier_courant = charge_utile.get("cwd") or str(Path.cwd())
    code_sortie, message = decider(commande, dossier_courant, lancer_le_verificateur_du_depot)
    if message:
        print(message, file=sys.stderr)
    return code_sortie


if __name__ == "__main__":
    sys.exit(main())
