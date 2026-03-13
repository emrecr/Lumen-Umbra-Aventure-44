# src/Ennemi.py
"""
Classe Ennemi - Adversaire RPG avec IA basique et récompense XP.
Hérite de Personnage. Compatible fixture pytest ennemi_factory().
"""

from .Personnage import Personnage  # Import relatif (corrige circulaire)
import random


class Ennemi(Personnage):
    """
    Ennemi contrôlé par IA simple.
    
    Constructeur étendu (compatible fixture) :
        Ennemi(nom, vie_max, force, arme, armure, exp)
    
    Attributs spécifiques:
        - exp (int): XP donnée au héros quand vaincu
    """
    
    def __init__(self, nom: str, vie_max: int, force: int, arme: int = 0, armure: int = 0, exp: int = 50):
        """
        Initialise ennemi avec TOUS les params de la fixture.
        
        Args:
            nom (str): Nom ennemi
            vie_max (int): Vie maximum
            force (int): Force base
            arme (int): Bonus dégâts arme (défaut 0)
            armure (int): Réduction dégâts (défaut 0)
            exp (int): XP récompense (défaut 50)
        """
        super().__init__(nom, vie_max, force, arme, armure)  # Passe arme/armure à Personnage
        self.exp = exp

    def decision_action(self) -> str:
        """
        IA ennemi :
        - Faible (<20% vie) → 70% FUIR
        - Fort → 80% ATTAQUER, 20% FUIR
        """
        ratio_vie = self.vie / self.vie_max
        if ratio_vie < 0.2:
            return 'fuit' if random.random() < 0.7 else 'attaque'
        return 'attaque' if random.random() < 0.8 else 'fuit'

    def donner_exp(self, hero) -> int:
        """
        Donne XP au héros si ennemi mort.
        Utilise hero.gagner_exp() → gère niveaux automatiquement.
        """
        if not self.est_vivant():
            hero.gagner_exp(self.exp)
            return self.exp
        return 0