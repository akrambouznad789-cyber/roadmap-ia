import json
import subprocess
import sys
from pathlib import Path

import pytest

from garde_git_push import CODE_SORTIE_AUTORISER, CODE_SORTIE_BLOQUER, commande_publie, decider

SCRIPT_GARDE = Path(__file__).resolve().parent.parent / "outils" / "garde_git_push.py"


@pytest.mark.parametrize(
    "commande",
    ["git push", "git push origin main", "git add . && git push", "git -C parcours-ia push"],
)
def test_reconnait_une_publication(commande):
    assert commande_publie(commande)


@pytest.mark.parametrize("commande", ["git status", "git add . && git commit -m x", "python -m pytest"])
def test_laisse_passer_le_reste(commande):
    assert not commande_publie(commande)


def test_ne_verifie_le_depot_que_pour_un_push():
    def verification_interdite():
        raise AssertionError("La vérification n'aurait pas dû tourner.")

    assert decider("git status", verification_interdite) == (CODE_SORTIE_AUTORISER, "")


def test_autorise_un_push_sans_probleme():
    assert decider("git push", lambda: []) == (CODE_SORTIE_AUTORISER, "")


def test_bloque_un_push_et_nomme_le_probleme():
    code_sortie, message = decider("git push", lambda: ["docs/index.html : lien brisé"])
    assert code_sortie == CODE_SORTIE_BLOQUER
    assert "docs/index.html : lien brisé" in message


def test_le_script_lit_le_format_de_claude_code():
    charge_utile = json.dumps({"tool_name": "Bash", "tool_input": {"command": "git status"}})
    resultat = subprocess.run(
        [sys.executable, str(SCRIPT_GARDE)], input=charge_utile.encode("utf-8"), capture_output=True
    )
    assert resultat.returncode == CODE_SORTIE_AUTORISER
