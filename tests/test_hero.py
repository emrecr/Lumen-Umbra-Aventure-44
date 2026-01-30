from src.Hero import Hero


class HeroStub(Hero):
    def __init__(self, vie_max=10, force=5):
        super().__init__("Stub", vie_max, force)

def test_exp_threshold_formula():
    h = HeroStub()
    assert h.niveau == 1
    assert h.exp_pour_prochain_niveau() == 200  # 100*1^2 + 100*1
    h.niveau = 2
    assert h.exp_pour_prochain_niveau() == 600  # 100*4 + 200
    h.niveau = 3
    assert h.exp_pour_prochain_niveau() == 1200 # 100*9 + 300

def test_monter_niveau_avec_aleatoire_min(monkeypatch):
    # Fige l'aléatoire à +1% pour vérifier précisément les boosts et les effets de bord.
    monkeypatch.setattr("src.Hero.uniform", lambda a, b: 1)

    h = HeroStub(vie_max=100, force=50)
    h.monter_niveau()
    assert h.niveau == 2
    # +1% arrondi, minimum +1
    # vie_max: ceil(100*1.01) = 101 (>= 100+1), force: ceil(50*1.01) = 51
    assert h.vie_max == 101
    assert h.force == 51
    # La vie est restaurée à vie_max
    assert h.vie == h.vie_max

def test_gagner_exp_cumulatif_un_seul_niveau(monkeypatch):
    monkeypatch.setattr("src.Hero.uniform", lambda a, b: 10)
    h = HeroStub()
    seuil = h.exp_pour_prochain_niveau()  # 200 au niveau 1

    # Presque au seuil
    h.exp = seuil - 5
    h.gagner_exp(4)
    assert h.niveau == 1
    assert h.exp == seuil - 1  # cumulatif, rien n'est consommé

    # On atteint juste le seuil -> montée unique
    h.gagner_exp(1)
    assert h.niveau == 2
    # L'XP reste cumulée
    assert h.exp == seuil
    # Le nouveau seuil (niveau 2) est plus élevé, donc la boucle s'arrête
    assert h.exp < h.exp_pour_prochain_niveau()

def test_gagner_exp_plusieurs_niveaux_en_chaine(monkeypatch):
    monkeypatch.setattr("src.Hero.uniform", lambda a, b: 1)  # boosts minimaux, résultats déterministes
    h = HeroStub(vie_max=10, force=5)

    h.gagner_exp(5000)
    assert h.niveau > 1
    assert h.exp < h.exp_pour_prochain_niveau()  # condition d'arrêt correcte

    # Invariants utiles
    assert 1 <= h.vie <= h.vie_max

def test_gagner_exp_ignore_non_positif():
    h = HeroStub()
    h.gagner_exp(0)
    assert h.exp == 0 and h.niveau == 1
    h.gagner_exp(-50)
    assert h.exp == 0 and h.niveau == 1
