# src/Hero.py
"""
Classe Hero - Personnage principal avec système de niveaux et XP
Hérite de Personnage pour les mécaniques de combat de base.
Respecte strictement l'architecture du diagramme de classes fourni.
"""

from src.Personnage import Personnage
import random
import math


class Hero(Personnage):
    """
    Représente le héros principal du jeu RPG.
    
    Héritage:
        - Personnage (vie, force, attaques, etc.)
    
    Attributs spécifiques:
        - niveau (int) : niveau actuel, commence à 1
        - exp (int)    : expérience cumulée
    
    Méthodes principales:
        - exp_pour_prochain_niveau() : formule 100*n² + 100*n
        - monter_niveau() : boost stats +1-10%, vie restaurée
        - gagner_exp() : XP cumulatif avec montées multiples
    """
    
    def __init__(self, nom: str, vie_max: int, force: int):
        """
        Initialise le héros avec stats de base + système de niveau.
        
        Args:
            nom (str): Nom du héros
            vie_max (int): Vie maximum initiale
            force (int): Force initiale
        """
        super().__init__(nom, vie_max, force)
        self.niveau = 1
        self.exp = 0

    @staticmethod
    def uniform(a: float, b: float) -> float:
        """
        Génère un float aléatoire entre a et b (pour boosts de niveau).
        
        NOTE: Méthode dédiée pour faciliter monkeypatch dans les tests.
        """
        return random.uniform(a, b)

    def exp_pour_prochain_niveau(self) -> int:
        """
        Calcule l'XP nécessaire pour le niveau suivant.
        
        Formule exacte (validée par tests):
            100 * niveau² + 100 * niveau
            
        Exemples:
            - Niv. 1 → 200 XP
            - Niv. 2 → 600 XP  
            - Niv. 3 → 1200 XP
        
        Returns:
            int: XP seuil pour prochain niveau
        """
        n = self.niveau
        return 100 * n * n + 100 * n

    def monter_niveau(self):
        """
        Passe au niveau suivant :
        1. niveau += 1
        2. Boost vie_max et force : +1% à +10% (arrondi ceil)
        3. Restaure vie = vie_max complète
        
        Exemple (monkeypatch uniform=0.01):
            vie_max=100 → 101
            force=50 → 51
            vie=vie_max
        """
        self.niveau += 1
        boost = 1 + self.uniform(0.01, 0.1)  # 1.01 à 1.10
        self.vie_max = math.ceil(self.vie_max * boost)
        self.force = math.ceil(self.force * boost)
        self.vie = self.vie_max  # vie entièrement restaurée

    def gagner_exp(self, quantite: int):
        """
        Ajoute de l'XP et monte les niveaux en chaîne si nécessaire.
        
        Logique:
        - Ignore quantite <= 0
        - exp += quantite (cumulatif)
        - while exp >= seuil: monter_niveau()
        
        Cas multiples niveaux: boucle while gère tout (ex: 5000 XP)
        
        Args:
            quantite (int): XP à gagner
        """
        if quantite <= 0:
            return
        self.exp += quantite
        while self.exp >= self.exp_pour_prochain_niveau():
            self.monter_niveau()
