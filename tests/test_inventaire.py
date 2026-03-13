import pytest
from src.personnages.Hero import Hero
from src.objets.objet import PotionSoin

def test_ajouter_objet_inventaire():
    """Vérifie l'ajout d'objets (Cahier des charges p.1)"""
    hero = Hero("Gustave", 100, 20)
    potion = PotionSoin("Potion", "Soin", 20)
    
    # Test de la méthode ajouter_objet du diagramme
    hero.inventaire.ajouter_objet(potion, 3)
    assert hero.inventaire.get_quantite(potion) == 3
def test_retirer_objet_inventaire():
    """Vérifie le retrait d'objets (Diagramme: retirer_objet)"""
    hero = Hero("Gustave", 100, 20)
    potion = PotionSoin("Potion", "Soin", 20)
    
    hero.inventaire.ajouter_objet(potion, 5)
    hero.inventaire.retirer_objet(potion, 2)
    assert hero.inventaire.get_quantite(potion) == 3