import json
import os
import tempfile
import pytest

from src.Donjon import Donjon
from src.Salle import Salle
from src.objets.objet import PotionSoin, Bombe, Equipement
from src.personnages.Ennemi import Ennemi


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _ecrire_json(data: dict) -> str:
    """Écrit un dictionnaire dans un fichier JSON temporaire et retourne son chemin."""
    f = tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False, encoding="utf-8"
    )
    json.dump(data, f, ensure_ascii=False)
    f.close()
    return f.name


DONJON_MINIMAL = {
    "salle_depart": "s1",
    "salles": {
        "s1": {
            "nom": "Salle A",
            "description": "Desc A",
            "a_lit": False,
            "objets": [],
            "ennemis": [],
            "sorties": {"nord": "s2"}
        },
        "s2": {
            "nom": "Salle B",
            "description": "Desc B",
            "a_lit": True,
            "objets": [
                {"type": "PotionDeSoin", "nom": "Potion", "description": "...", "quantite": 30}
            ],
            "ennemis": [
                {
                    "nom": "Gobelin",
                    "vie_max": 30,
                    "force": 8,
                    "arme": {"nom": "Dague", "description": "...", "bonus": 3},
                    "armure": {},
                    "exp": 20,
                    "recompenses": []
                }
            ],
            "sorties": {"sud": "s1"}
        }
    }
}


# ---------------------------------------------------------------------------
# Tests de chargement
# ---------------------------------------------------------------------------

def test_charger_donjon_minimal():
    """Le donjon minimal est chargé sans erreur."""
    chemin = _ecrire_json(DONJON_MINIMAL)
    try:
        d = Donjon()
        d.charger_depuis_fichier(chemin)
        assert len(d.catalogue_salles) == 2
    finally:
        os.unlink(chemin)


def test_charger_donjon_noms_corrects():
    """Les noms des salles sont correctement chargés."""
    chemin = _ecrire_json(DONJON_MINIMAL)
    try:
        d = Donjon()
        d.charger_depuis_fichier(chemin)
        noms = {s.nom for s in d.catalogue_salles}
        assert "Salle A" in noms
        assert "Salle B" in noms
    finally:
        os.unlink(chemin)


def test_charger_donjon_lit():
    """L'attribut a_lit est correctement chargé."""
    chemin = _ecrire_json(DONJON_MINIMAL)
    try:
        d = Donjon()
        d.charger_depuis_fichier(chemin)
        salle_b = next(s for s in d.catalogue_salles if s.nom == "Salle B")
        assert salle_b.a_lit is True
    finally:
        os.unlink(chemin)


def test_charger_sorties_bidirectionnelles():
    """Les sorties sont bien reliées dans les deux sens."""
    chemin = _ecrire_json(DONJON_MINIMAL)
    try:
        d = Donjon()
        d.charger_depuis_fichier(chemin)
        entree = d.generer_entree()
        assert "nord" in entree.sorties
        voisin = entree.sorties["nord"]
        assert "sud" in voisin.sorties
        assert voisin.sorties["sud"] is entree
    finally:
        os.unlink(chemin)


def test_charger_objets_dans_salle():
    """Les objets dans une salle sont correctement instanciés."""
    chemin = _ecrire_json(DONJON_MINIMAL)
    try:
        d = Donjon()
        d.charger_depuis_fichier(chemin)
        salle_b = next(s for s in d.catalogue_salles if s.nom == "Salle B")
        assert len(salle_b.objets) == 1
        assert isinstance(salle_b.objets[0], PotionSoin)
        assert salle_b.objets[0].valeursoin == 30
    finally:
        os.unlink(chemin)


def test_charger_ennemis_dans_salle():
    """Les ennemis dans une salle sont correctement instanciés."""
    chemin = _ecrire_json(DONJON_MINIMAL)
    try:
        d = Donjon()
        d.charger_depuis_fichier(chemin)
        salle_b = next(s for s in d.catalogue_salles if s.nom == "Salle B")
        assert len(salle_b.ennemis) == 1
        assert isinstance(salle_b.ennemis[0], Ennemi)
        assert salle_b.ennemis[0].nom == "Gobelin"
        assert salle_b.ennemis[0].arme == 3  # bonus arme depuis JSON
    finally:
        os.unlink(chemin)


# ---------------------------------------------------------------------------
# Tests generer_entree
# ---------------------------------------------------------------------------

def test_generer_entree_correcte():
    """generer_entree() retourne bien la salle de départ."""
    chemin = _ecrire_json(DONJON_MINIMAL)
    try:
        d = Donjon()
        d.charger_depuis_fichier(chemin)
        entree = d.generer_entree()
        assert isinstance(entree, Salle)
        assert entree.nom == "Salle A"
    finally:
        os.unlink(chemin)


def test_generer_entree_donjon_vide_leve_erreur():
    """generer_entree() sur un donjon non chargé lève ValueError."""
    d = Donjon()
    with pytest.raises(ValueError):
        d.generer_entree()


# ---------------------------------------------------------------------------
# Test avec le vrai fichier donjon.json
# ---------------------------------------------------------------------------

def test_charger_donjon_json_reel():
    """Vérifie que le fichier donjon.json fourni est valide et complet."""
    chemin = os.path.join(os.path.dirname(__file__), "..", "donjon.json")
    if not os.path.exists(chemin):
        pytest.skip("donjon.json introuvable")

    d = Donjon()
    d.charger_depuis_fichier(chemin)
    assert len(d.catalogue_salles) >= 1
    entree = d.generer_entree()
    assert isinstance(entree, Salle)