"""
Tests unitaires pour la classe Salle.
Couvre : initialisation, sorties, objets, peut_quitter.
"""
import pytest
from src.Salle import Salle
from src.objets.objet import PotionSoin, Bombe


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def salle_simple():
    return Salle("Crypte", "Une crypte humide.", a_lit=False)


@pytest.fixture
def salle_avec_lit():
    return Salle("Dortoir", "Une salle avec un vieux lit.", a_lit=True)


# ---------------------------------------------------------------------------
# Initialisation
# ---------------------------------------------------------------------------

def test_salle_init_attributs(salle_simple):
    """Les attributs sont correctement initialisés."""
    assert salle_simple.nom == "Crypte"
    assert salle_simple.description == "Une crypte humide."
    assert salle_simple.a_lit is False
    assert salle_simple.sorties == {}
    assert salle_simple.objets == []
    assert salle_simple.ennemis == []


def test_salle_avec_lit(salle_avec_lit):
    """Une salle avec lit a bien a_lit=True."""
    assert salle_avec_lit.a_lit is True


# ---------------------------------------------------------------------------
# Sorties
# ---------------------------------------------------------------------------

def test_ajouter_sortie(salle_simple):
    """Une sortie est correctement ajoutée."""
    dest = Salle("Couloir", "Un long couloir.")
    salle_simple.ajouter_sortie("nord", dest)
    assert "nord" in salle_simple.sorties
    assert salle_simple.sorties["nord"] is dest


def test_peut_quitter_sans_sortie(salle_simple):
    """Sans sortie, peut_quitter() retourne False."""
    assert salle_simple.peut_quitter() is False


def test_peut_quitter_avec_sortie(salle_simple):
    """Avec au moins une sortie, peut_quitter() retourne True."""
    salle_simple.ajouter_sortie("sud", Salle("Autre", "..."))
    assert salle_simple.peut_quitter() is True


def test_multiples_sorties(salle_simple):
    """Plusieurs sorties peuvent être ajoutées."""
    for direction in ("nord", "sud", "est", "ouest"):
        salle_simple.ajouter_sortie(direction, Salle(direction, "..."))
    assert len(salle_simple.sorties) == 4


# ---------------------------------------------------------------------------
# Objets
# ---------------------------------------------------------------------------

def test_recuperer_objets_vide(salle_simple):
    """Récupérer des objets dans une salle vide retourne liste vide."""
    assert salle_simple.recuperer_objets() == []


def test_recuperer_objets_non_vide(salle_simple):
    """Les objets sont récupérés et la salle est ensuite vide."""
    potion = PotionSoin("Potion", "Soin", 20)
    bombe = Bombe("Bombe", "Explose", 15)
    salle_simple.objets = [potion, bombe]

    ramasses = salle_simple.recuperer_objets()

    assert len(ramasses) == 2
    assert potion in ramasses
    assert bombe in ramasses
    # La salle est maintenant vide
    assert salle_simple.objets == []


def test_recuperer_objets_vide_apres_appel(salle_simple):
    """Appeler recuperer_objets deux fois : le second appel retourne []."""
    salle_simple.objets = [PotionSoin("P", "...", 10)]
    salle_simple.recuperer_objets()
    assert salle_simple.recuperer_objets() == []
