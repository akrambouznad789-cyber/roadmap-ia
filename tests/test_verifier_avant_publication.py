import subprocess

import pytest

from verifier_avant_publication import lire_mots_interdits, verifier_depot

# Assemblés ici pour que ce fichier public ne déclenche pas lui-même la vérification.
FAUX_TELEPHONE = "514" + "-555-" + "0199"
FAUX_CHEMIN_LOCAL = "C:" + "\\Users\\quelquun\\fichier.txt"

PAGE_PARCELLE_VALIDE = """<!doctype html>
<html lang="fr"><head><title>Parcelle</title></head><body>
<section id="regarde"></section><section id="demo"></section><section id="main"></section>
<section id="mots">Mon explication.</section><section id="sources"></section>
</body></html>"""


@pytest.fixture
def depot(tmp_path):
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    (tmp_path / ".gitignore").write_text("prive/\n", encoding="utf-8")
    return tmp_path


def ecrire(depot, chemin_relatif, contenu):
    chemin = depot / chemin_relatif
    chemin.parent.mkdir(parents=True, exist_ok=True)
    chemin.write_text(contenu, encoding="utf-8")


def test_un_depot_propre_passe(depot):
    ecrire(depot, "docs/parcelles/00-test/index.html", PAGE_PARCELLE_VALIDE)
    assert verifier_depot(depot, []) == []


def test_detecte_un_numero_de_telephone(depot):
    ecrire(depot, "README.md", f"Appelle-moi au {FAUX_TELEPHONE}")
    assert any("numéro de téléphone" in probleme for probleme in verifier_depot(depot, []))


def test_les_dates_ne_passent_pas_pour_un_telephone(depot):
    ecrire(depot, "resultats.csv", "2026-10-31,llama3.2:3b,1,128,5.25\n")
    assert verifier_depot(depot, []) == []


def test_detecte_un_chemin_local(depot):
    ecrire(depot, "README.md", FAUX_CHEMIN_LOCAL)
    assert any("chemin local" in probleme for probleme in verifier_depot(depot, []))


def test_detecte_un_mot_prive_sans_tenir_compte_de_la_casse(depot):
    ecrire(depot, "docs/note.md", "Mon employeur SECRET")
    assert any("mot privé" in probleme for probleme in verifier_depot(depot, ["secret"]))


def test_ignore_ce_que_git_ne_publierait_pas(depot):
    ecrire(depot, "prive/notes.md", f"Tel : {FAUX_TELEPHONE}, employeur secret")
    assert verifier_depot(depot, ["secret"]) == []


def test_refuse_les_fichiers_de_donnees(depot):
    ecrire(depot, "parcelles/donnees.gpkg", "contenu")
    assert any("type de fichier interdit" in probleme for probleme in verifier_depot(depot, []))


def test_bloque_une_page_avec_un_texte_a_ecrire(depot):
    page = PAGE_PARCELLE_VALIDE.replace("Mon explication.", "À ÉCRIRE PAR AKRAM")
    ecrire(depot, "docs/parcelles/00-test/index.html", page)
    assert any("texte à écrire" in probleme for probleme in verifier_depot(depot, []))


def test_bloque_un_gabarit_non_rempli(depot):
    page = PAGE_PARCELLE_VALIDE.replace("Mon explication.", "{{TITRE}}")
    ecrire(depot, "docs/parcelles/00-test/index.html", page)
    assert any("gabarit non rempli" in probleme for probleme in verifier_depot(depot, []))


def test_exige_toutes_les_sections_d_une_parcelle(depot):
    page = PAGE_PARCELLE_VALIDE.replace('id="mots"', 'id="autre"')
    ecrire(depot, "docs/parcelles/00-test/index.html", page)
    assert any("section #mots manquante" in probleme for probleme in verifier_depot(depot, []))


def test_detecte_un_lien_brise(depot):
    page = PAGE_PARCELLE_VALIDE.replace("</body>", '<a href="absent.html">x</a></body>')
    ecrire(depot, "docs/parcelles/00-test/index.html", page)
    assert any("lien brisé" in probleme for probleme in verifier_depot(depot, []))


def test_accepte_un_lien_vers_un_dossier_avec_index(depot):
    ecrire(depot, "docs/parcelles/00-test/index.html", PAGE_PARCELLE_VALIDE)
    accueil = '<html lang="fr"><title>Accueil</title><a href="parcelles/00-test/">x</a></html>'
    ecrire(depot, "docs/index.html", accueil)
    assert verifier_depot(depot, []) == []


def test_les_liens_externes_ne_sont_pas_verifies(depot):
    page = '<html lang="fr"><title>A</title><a href="https://exemple.org/absent">x</a></html>'
    ecrire(depot, "docs/index.html", page)
    assert verifier_depot(depot, []) == []


def test_une_liste_absente_est_une_erreur_en_local(tmp_path, monkeypatch):
    monkeypatch.delenv("CI", raising=False)
    with pytest.raises(FileNotFoundError):
        lire_mots_interdits(tmp_path / "absent.txt")


def test_une_liste_absente_est_toleree_sur_github_actions(tmp_path, monkeypatch):
    monkeypatch.setenv("CI", "true")
    assert lire_mots_interdits(tmp_path / "absent.txt") is None


def test_la_liste_ignore_les_commentaires_et_les_lignes_vides(tmp_path):
    chemin = tmp_path / "mots.txt"
    chemin.write_text("# commentaire\n\nmot un\n  mot deux  \n", encoding="utf-8")
    assert lire_mots_interdits(chemin) == ["mot un", "mot deux"]
