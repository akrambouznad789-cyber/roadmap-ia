import json
import subprocess
import sys
from pathlib import Path

import pytest

from garde_git_push import (
    CODE_SORTIE_AUTORISER,
    CODE_SORTIE_BLOQUER,
    commande_publie,
    decider,
    nettoyer_le_chemin,
    trouver_la_racine_du_depot,
    trouver_les_dossiers_publies,
)

SCRIPT_GARDE = Path(__file__).resolve().parent.parent / "outils" / "garde_git_push.py"


@pytest.fixture
def depot(tmp_path):
    racine = tmp_path / "depot"
    (racine / ".git").mkdir(parents=True)
    (racine / "docs").mkdir()
    return racine


@pytest.mark.parametrize(
    "commande",
    [
        "git push",
        "git push origin main",
        "git add . && git push",
        "git -C parcours-ia push",
        'git -C "C:/depots/Une Classe" -c core.quotepath=off push -u origin main',
        "cd x; if ($?) { git push }",
        "& git.exe push 2>&1 | Out-String",
    ],
)
def test_reconnait_une_publication(commande):
    assert commande_publie(commande)


@pytest.mark.parametrize(
    "commande",
    [
        "git status",
        "git add . && git commit -m x",
        "python -m pytest",
        "Set-Content notes.md 'après le premier `git push`, activer Pages'",
        "git log --grep push",
    ],
)
def test_laisse_passer_le_reste(commande):
    assert not commande_publie(commande)


def test_le_dossier_publie_par_defaut_est_le_dossier_courant(tmp_path):
    assert trouver_les_dossiers_publies("git push", tmp_path) == [tmp_path]


def test_le_dossier_publie_suit_l_option_c_de_git(tmp_path):
    commande = 'git -C "C:/depots/Une Classe" push origin main'
    assert trouver_les_dossiers_publies(commande, tmp_path) == [Path("C:/depots/Une Classe")]


@pytest.mark.parametrize(
    "commande",
    ["cd 'C:/autre depot'; git push", 'Set-Location -Path "C:/autre depot" ; git add x && git push'],
)
def test_le_dossier_publie_suit_un_cd_place_avant(tmp_path, commande):
    assert trouver_les_dossiers_publies(commande, tmp_path) == [Path("C:/autre depot")]


def test_un_chemin_de_git_bash_devient_un_chemin_windows():
    assert nettoyer_le_chemin('"/c/depots/Une Classe"') == "c:/depots/Une Classe"


def test_trouve_la_racine_depuis_un_sous_dossier(depot):
    assert trouver_la_racine_du_depot(depot / "docs") == depot


def test_ne_verifie_le_depot_que_pour_un_push(depot):
    def verification_interdite(racine):
        raise AssertionError("La vérification n'aurait pas dû tourner.")

    assert decider("git status", depot, verification_interdite) == (CODE_SORTIE_AUTORISER, "")


def test_autorise_un_push_sans_probleme(depot):
    assert decider("git push", depot, lambda racine: []) == (CODE_SORTIE_AUTORISER, "")


def test_verifie_le_depot_vise_et_non_le_dossier_courant(depot, tmp_path):
    racines_verifiees = []

    def noter_la_racine(racine):
        racines_verifiees.append(racine)
        return []

    decider(f'git -C "{depot / "docs"}" push', tmp_path, noter_la_racine)
    assert racines_verifiees == [depot.resolve()]


def test_bloque_un_push_et_nomme_le_probleme(depot):
    code_sortie, message = decider("git push", depot, lambda racine: ["docs/index.html : lien brisé"])
    assert code_sortie == CODE_SORTIE_BLOQUER
    assert "[depot] docs/index.html : lien brisé" in message


def test_bloque_un_push_hors_d_un_depot(tmp_path):
    code_sortie, message = decider("git push", tmp_path / "nulle-part", lambda racine: [])
    assert code_sortie == CODE_SORTIE_BLOQUER
    assert "dépôt introuvable" in message


def test_le_script_lit_le_format_de_claude_code():
    charge_utile = json.dumps({"tool_name": "Bash", "tool_input": {"command": "git status"}})
    resultat = subprocess.run(
        [sys.executable, str(SCRIPT_GARDE)], input=charge_utile.encode("utf-8"), capture_output=True
    )
    assert resultat.returncode == CODE_SORTIE_AUTORISER
