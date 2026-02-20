import pytest

from src.Objet import Objet, Consommable, PotionSoin, Bombe, Equipement
from src.Personnage import Personnage


# ---------------------
# Classes de support
# ---------------------
class FauxPersonnage(Personnage):
    """Personnage simplifié pour tester les consommables/équipements."""
    def __init__(self, nom="Test", vie_max=20, force=5, arme=0, armure=0):
        super().__init__(nom=nom, vie_max=vie_max, force=force, arme=arme, armure=armure)


# ----------------------
# Tests Objet (base)
# ----------------------
def test_objet_init_attributs():
    class ObjetConcret(Objet):
        """Petite sous-classe concrète pour tester l'init de Objet."""
        pass

    o = ObjetConcret("Épée rouillée", "Une vieille épée toute abîmée")
    assert o.nom == "Épée rouillée"
    assert o.description == "Une vieille épée toute abîmée"


# ----------------------
# Tests Consommable / PotionSoin
# ----------------------
def test_potionsoin_init_attributs():
    p = PotionSoin("Petite potion", "Rend quelques PV", valeursoin=10)
    assert p.nom == "Petite potion"
    assert p.description == "Rend quelques PV"
    assert p.valeursoin == 10


def test_potionsoin_utiliser_soigne_cible(monkeypatch):
    cible = FauxPersonnage(vie_max=30, force=5)
    cible.vie = 10  # cible blessée
    potion = PotionSoin("Potion", "Soigne 8 PV", valeursoin=8)

    # on espionne Personnage.soigner pour vérifier qu'elle est bien appelée
    appels = {}

    def faux_soigner(self, valeur):
        appels["valeur"] = valeur
        # comportement réaliste : ajouter des PV sans dépasser vie_max
        self.vie = min(self.vie + valeur, self.vie_max)

    monkeypatch.setattr(Personnage, "soigner", faux_soigner)

    effet = potion.utiliser(cible)
    assert effet == 8
    assert appels["valeur"] == 8
    assert cible.vie == 18  # 10 + 8


# ----------------------
# Tests Bombe
# ----------------------
def test_bombe_init_attributs():
    b = Bombe("Bombe basique", "Inflige 12 dégâts", degats=12)
    assert b.nom == "Bombe basique"
    assert b.description == "Inflige 12 dégâts"
    assert b.degats == 12


def test_bombe_utiliser_inflige_degats(monkeypatch):
    cible = FauxPersonnage(vie_max=25, force=5)
    cible.vie = 20
    bombe = Bombe("Bombe", "Explose fort", degats=7)

    appels = {}

    def faux_subir_degats(self, valeur):
        appels["valeur"] = valeur
        # comportement réaliste : retirer des PV sans passer sous 0
        perdu = min(self.vie, max(0, valeur))
        self.vie -= perdu
        return perdu

    monkeypatch.setattr(Personnage, "subir_degats", faux_subir_degats)

    effet = bombe.utiliser(cible)
    assert effet == 7
    assert appels["valeur"] == 7
    assert cible.vie == 13  # 20 - 7


# ----------------------
# Tests Equipement
# ----------------------
def test_equipement_init_defauts():
    e = Equipement("Anneau neutre", "Aucun bonus")
    assert e.nom == "Anneau neutre"
    assert e.description == "Aucun bonus"
    assert e.bonusforce == 0
    assert e.bonusdefense == 0


def test_equipement_init_avec_bonus():
    e = Equipement("Épée de bois", "Petit bonus d'attaque", bonusforce=3, bonusdefense=1)
    assert e.bonusforce == 3
    assert e.bonusdefense == 1
