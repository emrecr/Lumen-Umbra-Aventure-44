# tests/test_combat.py
import pytest

from src.Hero import Hero
from src.Ennemi import Ennemi
from src.main import combat_tour_par_tour

# --- Fixtures utilitaires -----------------------------------------------------

@pytest.fixture(autouse=True)
def deterministic_damage(monkeypatch):
    """
    Rends le calcul des dégâts déterministe:
    Personnage.calcul_degats_sur() utilise uniform(), on force uniform()=1.0 -> multiplicateur = 1.0
    """
    monkeypatch.setattr("src.Personnage.uniform", lambda a, b: 1.0)


@pytest.fixture
def hero_factory():
    def make(nom="Héro", vie_max=20, force=10, arme=0, armure=0, exp=0, niveau=1):
        h = Hero(nom=nom, vie_max=vie_max, force=force, arme=arme, armure=armure)
        h.exp = exp
        h.niveau = niveau
        return h
    return make


@pytest.fixture
def ennemi_factory():
    def make(nom="Gobelin", vie_max=12, force=4, arme=0, armure=0, exp=50):
        return Ennemi(nom=nom, vie_max=vie_max, force=force, arme=arme, armure=armure, exp=exp)
    return make

# --- Tests --------------------------------------------------------------------

def test_joueur_gagne_et_prend_xp(hero_factory, ennemi_factory, capsys):
    """
    Le joueur commence, tue l’ennemi, et gagne exactement ennemi.exp points.
    On vérifie aussi que des logs sont bien produits (log=True).
    """
    joueur = hero_factory(vie_max=20, force=10, arme=0, armure=0, exp=0)
    # Ennemi faible: 12 PV, 0 armure => dégâts du joueur = ceil((10+0-0)*1.0)=10
    # -> 1er tour: PV passe à 2, 2e tour: meurt
    ennemi = ennemi_factory(vie_max=12, force=3, armure=0, exp=42)

    gagnant = combat_tour_par_tour(joueur, ennemi, log=True)
    out = capsys.readouterr().out

    assert gagnant is joueur
    assert not ennemi.est_vivant()
    assert joueur.est_vivant()
    assert joueur.exp >= 42  # modèle d’XP cumulatif; au minimum +42

    # Un peu de robustesse sur les logs:
    assert f"{joueur.nom} inflige" in out
    assert f"{ennemi.nom} est vaincu" in out
    assert f"gagne {ennemi.exp} XP" in out


def test_ennemi_gagne(hero_factory, ennemi_factory, capsys):
    """
    Ennemi plus fort: le joueur meurt pendant le tour de l’ennemi.
    """
    # Joueur fragile, force faible
    joueur = hero_factory(vie_max=10, force=2, armure=0)
    # Ennemi costaud: dégâts = ceil((9+0-0)*1.0)=9 -> tue en 2 tours (10 -> 1 -> 0)
    ennemi = ennemi_factory(nom="Orc", vie_max=30, force=9, armure=0, exp=99)

    gagnant = combat_tour_par_tour(joueur, ennemi, log=True)
    out = capsys.readouterr().out

    assert gagnant is ennemi
    assert not joueur.est_vivant()
    assert ennemi.est_vivant()
    assert f"{joueur.nom} est vaincu" in out


def test_log_false_ne_produit_aucune_sortie(hero_factory, ennemi_factory, capsys):
    """
    Quand log=False, aucune sortie standard ne doit être produite.
    """
    joueur = hero_factory(vie_max=20, force=10)
    ennemi = ennemi_factory(vie_max=10, force=1)

    _ = combat_tour_par_tour(joueur, ennemi, log=False)
    captured = capsys.readouterr()
    assert captured.out == ""


def test_initiative_joueur(hero_factory, ennemi_factory):
    """
    Le joueur frappe TOUJOURS en premier. Ici les deux pourraient s'entre-tuer
    si l’ennemi jouait d’abord, mais l’initiative donne la victoire au joueur.
    """
    # Joueur inflige au moins 10 par coup, ennemi a 10 PV -> meurt avant d'attaquer
    joueur = hero_factory(vie_max=5, force=10, arme=0)
    ennemi = ennemi_factory(vie_max=10, force=99, arme=0)  # très dangereux, mais n’attaquera pas

    gagnant = combat_tour_par_tour(joueur, ennemi, log=False)

    assert gagnant is joueur
    assert joueur.est_vivant()
    assert not ennemi.est_vivant()
