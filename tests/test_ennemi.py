"""
Tests unitaires pour la classe Ennemi.
Couvre : initialisation, donner_exp, donner_recompenses, decision_action.
"""
import pytest
from src.personnages.Ennemi import Ennemi
from src.personnages.Hero import Hero
from src.objets.objet import PotionSoin

@pytest.fixture
def hero():
    return Hero("Gustave", vie_max=100, force=20)


@pytest.fixture
def ennemi_vivant():
    return Ennemi("Gobelin", vie_max=50, force=10, exp=30)


@pytest.fixture
def ennemi_mort():
    e = Ennemi("Zombie", vie_max=20, force=5, exp=10)
    e.subir_degats(20)  # le tue
    return e


# ---------------------------------------------------------------------------
# Initialisation
# ---------------------------------------------------------------------------

def test_ennemi_init_attributs():
    """Vérifie que tous les attributs sont correctement initialisés."""
    e = Ennemi("Orc", vie_max=80, force=15, arme=5, armure=3, exp=60)
    assert e.nom == "Orc"
    assert e.vie_max == 80
    assert e.vie == 80
    assert e.force == 15
    assert e.arme == 5
    assert e.armure == 3
    assert e.exp == 60
    assert isinstance(e.recompenses, dict)


def test_ennemi_init_valeurs_defaut():
    """Les valeurs par défaut (arme=0, armure=0, exp=50) sont respectées."""
    e = Ennemi("Rat", vie_max=10, force=2)
    assert e.arme == 0
    assert e.armure == 0
    assert e.exp == 50


# ---------------------------------------------------------------------------
# donner_exp
# ---------------------------------------------------------------------------

def test_donner_exp_si_mort(hero, ennemi_mort):
    """Un ennemi mort donne bien son XP au héros."""
    xp_avant = hero.exp
    ennemi_mort.donner_exp(hero)
    assert hero.exp == xp_avant + ennemi_mort.exp


def test_donner_exp_si_vivant(hero, ennemi_vivant):
    """Un ennemi vivant ne donne aucune XP."""
    xp_avant = hero.exp
    ennemi_vivant.donner_exp(hero)
    assert hero.exp == xp_avant


# ---------------------------------------------------------------------------
# donner_recompenses
# ---------------------------------------------------------------------------

def test_donner_recompenses_transfère_objets(hero, ennemi_mort):
    """Les récompenses sont transférées dans l'inventaire du héros."""
    potion = PotionSoin("Potion", "Soin", 20)
    ennemi_mort.recompenses[potion] = 2

    ennemi_mort.donner_recompenses(hero)

    assert hero.inventaire.get_quantite(potion) == 2


def test_donner_recompenses_vide_apres_transfert(hero, ennemi_mort):
    """Après le transfert, recompenses est vide (pas de double don)."""
    potion = PotionSoin("Potion", "Soin", 20)
    ennemi_mort.recompenses[potion] = 1
    ennemi_mort.donner_recompenses(hero)

    assert len(ennemi_mort.recompenses) == 0


def test_donner_recompenses_ennemi_vivant_ne_donne_rien(hero, ennemi_vivant):
    """Un ennemi encore vivant ne donne aucune récompense."""
    potion = PotionSoin("Potion", "Soin", 20)
    ennemi_vivant.recompenses[potion] = 1

    ennemi_vivant.donner_recompenses(hero)

    assert hero.inventaire.get_quantite(potion) == 0


# ---------------------------------------------------------------------------
# decision_action
# ---------------------------------------------------------------------------

def test_decision_action_retourne_valeur_valide(ennemi_vivant):
    """decision_action retourne 'attaque' ou 'fuit'."""
    for _ in range(20):
        action = ennemi_vivant.decision_action()
        assert action in ("attaque", "fuit")


def test_decision_action_faible_favorise_fuite(monkeypatch):
    """Quand vie < 20 %, random.random() < 0.7 → fuit."""
    e = Ennemi("Gobelin faible", vie_max=100, force=5)
    e.vie = 15  # 15 % → mode fuite
    monkeypatch.setattr("src.personnages.Ennemi.random.random", lambda: 0.5)  # < 0.7
    assert e.decision_action() == "fuit"


def test_decision_action_fort_attaque(monkeypatch):
    """Quand vie >= 20 % et random < 0.8 → attaque."""
    e = Ennemi("Orc fort", vie_max=100, force=10)
    e.vie = 80  # 80 % → mode normal
    monkeypatch.setattr("src.personnages.Ennemi.random.random", lambda: 0.5)  # < 0.8
    assert e.decision_action() == "attaque"
