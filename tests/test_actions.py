import pytest

from src.Salle import Salle
from src.personnages.Hero import Hero
from src.personnages.Ennemi import Ennemi
from src.objets.objet import PotionSoin, Bombe
from src.actions.action import (
    Observer, SeDeplacer, Attaquer, Ramasser, SeReposer, Fuir, Utiliser
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def hero():
    return Hero(nom="Gustave", vie_max=100, force=20, arme=0, armure=0)


@pytest.fixture
def salle_vide():
    return Salle("Crypte", "Une crypte vide.", a_lit=False)


@pytest.fixture
def salle_avec_lit():
    return Salle("Dortoir", "Une salle avec un lit.", a_lit=True)


@pytest.fixture
def ennemi():
    return Ennemi("Gobelin", vie_max=30, force=5, exp=20)


@pytest.fixture
def salle_avec_ennemi(ennemi):
    s = Salle("Arène", "Une salle dangereuse.")
    s.ennemis.append(ennemi)
    return s


@pytest.fixture
def salle_avec_objets():
    s = Salle("Réserve", "Une salle pleine d'objets.")
    s.objets.append(PotionSoin("Potion", "Soin", 20))
    s.objets.append(Bombe("Bombe", "Explose", 15))
    return s


# ===========================================================================
# Observer
# ===========================================================================

class TestObserver:
    def test_possible_sans_ennemi(self, hero, salle_vide):
        assert Observer(hero, salle_vide).est_possible() is True

    def test_impossible_avec_ennemi(self, hero, salle_avec_ennemi):
        assert Observer(hero, salle_avec_ennemi).est_possible() is False

    def test_executer_ne_modifie_rien(self, hero, salle_vide):
        vie_avant = hero.vie
        Observer(hero, salle_vide).executer()
        assert hero.vie == vie_avant


# ===========================================================================
# SeDeplacer
# ===========================================================================

class TestSeDeplacer:
    def test_possible_sans_ennemi(self, hero, salle_vide):
        dest = Salle("Nord", "Salle nord.")
        salle_vide.ajouter_sortie("nord", dest)
        assert SeDeplacer(hero, salle_vide, dest).est_possible() is True

    def test_impossible_avec_ennemi(self, hero, salle_avec_ennemi, salle_vide):
        salle_avec_ennemi.ajouter_sortie("nord", salle_vide)
        assert SeDeplacer(hero, salle_avec_ennemi, salle_vide).est_possible() is False

    def test_impossible_destination_non_accessible(self, hero, salle_vide):
        autre = Salle("Ailleurs", "...")
        assert SeDeplacer(hero, salle_vide, autre).est_possible() is False

    def test_executer_ne_change_pas_salle_courante(self, hero, salle_vide):
        dest = Salle("Nord", "...")
        salle_vide.ajouter_sortie("nord", dest)
        action = SeDeplacer(hero, salle_vide, dest)
        action.executer()
        assert action.salle_courante is salle_vide  # le contrôleur gère le changement


# ===========================================================================
# Attaquer
# ===========================================================================

class TestAttaquer:
    def test_possible_ennemi_present(self, hero, salle_avec_ennemi, ennemi):
        assert Attaquer(hero, salle_avec_ennemi, ennemi).est_possible() is True

    def test_impossible_ennemi_absent(self, hero, salle_vide):
        e = Ennemi("Fantôme", 20, 5)
        assert Attaquer(hero, salle_vide, e).est_possible() is False

    def test_impossible_ennemi_mort(self, hero, salle_avec_ennemi, ennemi):
        ennemi.subir_degats(ennemi.vie_max)
        assert Attaquer(hero, salle_avec_ennemi, ennemi).est_possible() is False

    def test_executer_reduit_vie_ennemi(self, hero, salle_avec_ennemi, ennemi):
        vie_avant = ennemi.vie
        Attaquer(hero, salle_avec_ennemi, ennemi).executer()
        assert ennemi.vie < vie_avant

    def test_executer_retire_ennemi_mort_de_la_salle(self, hero, salle_avec_ennemi, ennemi):
        hero.force = 9999
        Attaquer(hero, salle_avec_ennemi, ennemi).executer()
        assert ennemi not in salle_avec_ennemi.ennemis

    def test_executer_transfere_exp_apres_mort(self, hero, salle_avec_ennemi, ennemi):
        hero.force = 9999
        xp_avant = hero.exp
        Attaquer(hero, salle_avec_ennemi, ennemi).executer()
        assert hero.exp >= xp_avant + ennemi.exp


# ===========================================================================
# Ramasser
# ===========================================================================

class TestRamasser:
    def test_possible_avec_objets(self, hero, salle_avec_objets):
        assert Ramasser(hero, salle_avec_objets).est_possible() is True

    def test_impossible_salle_vide(self, hero, salle_vide):
        assert Ramasser(hero, salle_vide).est_possible() is False

    def test_impossible_avec_ennemi(self, hero, salle_avec_ennemi):
        salle_avec_ennemi.objets.append(PotionSoin("P", "...", 10))
        assert Ramasser(hero, salle_avec_ennemi).est_possible() is False

    def test_executer_ajoute_objets_inventaire(self, hero, salle_avec_objets):
        Ramasser(hero, salle_avec_objets).executer()
        assert len(hero.inventaire.lister_objets()) > 0

    def test_executer_vide_la_salle(self, hero, salle_avec_objets):
        Ramasser(hero, salle_avec_objets).executer()
        assert salle_avec_objets.objets == []


# ===========================================================================
# SeReposer
# ===========================================================================

class TestSeReposer:
    def test_possible_lit_sans_ennemi(self, hero, salle_avec_lit):
        assert SeReposer(hero, salle_avec_lit).est_possible() is True

    def test_impossible_sans_lit(self, hero, salle_vide):
        assert SeReposer(hero, salle_vide).est_possible() is False

    def test_impossible_avec_ennemi(self, hero, salle_avec_ennemi):
        salle_avec_ennemi.a_lit = True
        assert SeReposer(hero, salle_avec_ennemi).est_possible() is False

    def test_executer_restaure_vie_max(self, hero, salle_avec_lit):
        hero.vie = 10
        SeReposer(hero, salle_avec_lit).executer()
        assert hero.vie == hero.vie_max


# ===========================================================================
# Fuir
# ===========================================================================

class TestFuir:
    def test_possible_avec_ennemi_et_precedente(self, hero, salle_avec_ennemi, salle_vide):
        assert Fuir(hero, salle_avec_ennemi, salle_vide).est_possible() is True

    def test_impossible_sans_ennemi(self, hero, salle_vide):
        assert Fuir(hero, salle_vide, Salle("Retour", "...")).est_possible() is False

    def test_impossible_sans_salle_precedente(self, hero, salle_avec_ennemi):
        assert Fuir(hero, salle_avec_ennemi, None).est_possible() is False

    def test_executer_ne_modifie_pas_ennemis(self, hero, salle_avec_ennemi, salle_vide):
        ennemis_avant = list(salle_avec_ennemi.ennemis)
        Fuir(hero, salle_avec_ennemi, salle_vide).executer()
        assert salle_avec_ennemi.ennemis == ennemis_avant


# ===========================================================================
# Utiliser
# ===========================================================================

class TestUtiliser:
    @pytest.fixture
    def potion(self):
        return PotionSoin("Potion", "Soin", 30)

    @pytest.fixture
    def hero_avec_potion(self, hero, potion):
        hero.inventaire.ajouter_objet(potion, 2)
        hero.vie = 50
        return hero

    def test_possible_avec_consommable(self, hero_avec_potion, salle_vide, potion):
        assert Utiliser(hero_avec_potion, salle_vide, potion).est_possible() is True

    def test_impossible_sans_objet(self, hero, salle_vide):
        potion = PotionSoin("P", "...", 10)
        assert Utiliser(hero, salle_vide, potion).est_possible() is False

    def test_executer_soigne_hero(self, hero_avec_potion, salle_vide, potion):
        vie_avant = hero_avec_potion.vie
        Utiliser(hero_avec_potion, salle_vide, potion).executer()
        assert hero_avec_potion.vie > vie_avant

    def test_executer_retire_objet_inventaire(self, hero_avec_potion, salle_vide, potion):
        qte_avant = hero_avec_potion.inventaire.get_quantite(potion)
        Utiliser(hero_avec_potion, salle_vide, potion).executer()
        assert hero_avec_potion.inventaire.get_quantite(potion) == qte_avant - 1

    def test_executer_bombe_blesse_ennemi(self, hero, salle_avec_ennemi, ennemi):
        bombe = Bombe("Bombe", "Boom", 10)
        hero.inventaire.ajouter_objet(bombe)
        vie_avant = ennemi.vie
        Utiliser(hero, salle_avec_ennemi, bombe, cible=ennemi).executer()
        assert ennemi.vie < vie_avant


# ===========================================================================
# Tests d'intégration : liste des actions disponibles selon l'état
# ===========================================================================

class TestListeActionsDisponibles:
    """Vérifie que les combinaisons d'actions disponibles sont correctes."""

    def _possibles(self, hero, salle, salle_prec=None):
        potion = PotionSoin("P", "...", 10)
        hero.inventaire.ajouter_objet(potion)
        candidats = [
            Observer(hero, salle),
            SeReposer(hero, salle),
            Ramasser(hero, salle),
            Fuir(hero, salle, salle_prec),
            Utiliser(hero, salle, potion),
        ]
        for dest in salle.sorties.values():
            candidats.append(SeDeplacer(hero, salle, dest))
        for e in salle.ennemis:
            candidats.append(Attaquer(hero, salle, e))
        return {type(a) for a in candidats if a.est_possible()}

    def test_salle_sans_ennemi(self, hero):
        salle = Salle("S", "desc")
        types = self._possibles(hero, salle)
        assert Observer in types
        assert Attaquer not in types
        assert Fuir not in types

    def test_salle_avec_ennemi_sans_retour(self, hero):
        e = Ennemi("G", 20, 5)
        salle = Salle("S", "desc")
        salle.ennemis.append(e)
        types = self._possibles(hero, salle, salle_prec=None)
        assert Attaquer in types
        assert Observer not in types
        assert Fuir not in types

    def test_salle_avec_ennemi_avec_retour(self, hero):
        e = Ennemi("G", 20, 5)
        salle = Salle("S", "desc")
        salle.ennemis.append(e)
        types = self._possibles(hero, salle, salle_prec=Salle("Prec", "..."))
        assert Attaquer in types
        assert Fuir in types

    def test_salle_avec_lit(self, hero):
        salle = Salle("Dortoir", "desc", a_lit=True)
        types = self._possibles(hero, salle)
        assert SeReposer in types

    def test_utiliser_disponible_si_consommable(self, hero, salle_vide):
        potion = PotionSoin("P", "...", 10)
        hero.inventaire.ajouter_objet(potion)
        assert Utiliser(hero, salle_vide, potion).est_possible() is True
