# src/Hero.py
"""
Classe Hero - Personnage joueur avec système XP/niveaux, inventaire et loots.
Hérite de Personnage (vie, combat, arme/armure).
Diagramme: Hero -> inventaire(Inventaire), expPourProchainNiveau, monterNiveau.
Compatible tests pytest + documentation officielle.
"""

<<<<<<< HEAD
from src.Personnage import Personnage
=======
from .Personnage import Personnage  # Héritage ABC (doit implémenter donner_recompenses)
from .Inventaire import Inventaire  # Diagramme: Hero possède Inventaire
from .Objet import Equipement  # Pour arme/armure (bonusforce)
>>>>>>> 225a29c45a1850b0120d909a4ade80f3f55f158a
import random
import math

uniform = random.uniform


class Hero(Personnage):
    """
    Représente le héros principal (joueur). Hérite de Personnage(ABC).
    
    Constructeur (diagramme + doc officielle):
        Hero(nom: str, vie_max: int, force: int, arme: Equipement=None, armure: Equipement=None)
    
    Attributs spécifiques (diagramme):
        - niveau: int = 1
        - exp: int = 0 (cumulatif)
        - exp_pour_prochain_niveau: calculé dynamiquement
        - inventaire: Inventaire (gère objets/équipements)
    
    Inherited (Personnage): initnom, viemax, vie, force, arme, armure, estvivant
    """

    def __init__(self, nom: str, vie_max: int, force: int, arme: Equipement = None, armure: Equipement = None):
        """
        Initialise héros avec stats Personnage + système niveaux/inventaire (diagramme).
        arme/armure: Equipement (bonusforce/bonusdefense).
        """
        super().__init__(nom, vie_max, force, arme, armure)  # Appelle Personnage.__init__
        self.niveau = 1
        self.exp = 0
        self.inventaire = Inventaire()  # Diagramme: Hero -> Inventaire (composition)

    def donner_recompenses(self, hero: 'Hero') -> None:
        """
        Implémente méthode abstraite Personnage (diagramme: donnerRecompenses(hero: Hero)).
        Logique Hero: ne donne rien (pas de loots), ou partage inventaire ?
        Pour cohérence avec Ennemi (qui donne exp/objets).
        """
        print(f"{self.initnom} n'a pas de récompenses à donner (pas d'ennemi).")
        # Option: self.inventaire.partager(hero.inventaire) si besoin

    @staticmethod
    def uniform(a: float, b: float) -> float:
        """
        Aléatoire pour tests (monkeypatch-able pytest).
        """
        return uniform(a, b)

    def exp_pour_prochain_niveau(self) -> int:
        """
        Formule officielle (diagramme: exppourprochainniveau int).
        100 * niveau^2 + 100 * niveau
        Ex: niv1=200, niv2=600, niv3=1200
        """
        n = self.niveau
        return 100 * n * n + 100 * n

    def monter_niveau(self) -> None:
        """
        Monte niveau (diagramme: monterniveaugagnerexpexp).
        Boost aléatoire vie_max/force, reset vie=vie_max.
        """
        self.niveau += 1
        pct_boost = self.uniform(1, 10) / 100
        boost = 1 + pct_boost
        
        self.viemax = math.ceil(self.viemax * boost)  # vie_max → viemax (cohérent Personnage)
        self.force = math.ceil(self.force * boost)
        self.vie = self.viemax  # Reset vie courante

    def gagner_exp(self, exp: int) -> None:
        """
        Gagne XP + monte niveau si seuil atteint (diagramme: système exp/niveau).
        Ignore exp <= 0.
        """
        if exp <= 0:
            return
        
        self.exp += exp  # Ajoute à l'XP total
        
        # Monte autant de niveaux que possible
        while self.exp >= self.exp_pour_prochain_niveau():
            self.monter_niveau()
            print(f"{self.initnom} → Niveau {self.niveau} ! (XP restants: {self.exp})")

