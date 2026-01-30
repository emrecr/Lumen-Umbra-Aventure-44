from random import uniform

class Personnage:
    """
    Classe de base représentant un combattant dans le jeu.
    
    Attributes:
        nom (str): Nom du personnage.
        vie_max (int): Points de vie maximum autorisés.
        vie (int): Points de vie actuels du personnage.
        force (int): Force brute utilisée pour le calcul des dégâts.
        arme (int): Valeur d'attaque de l'arme équipée.
        armure (int): Valeur de défense réduisant les dégâts subis.
    """

    def __init__(self, nom: str, vie_max: int, force: int, arme: int, armure: int):
        """
        Initialise un nouveau personnage avec ses statistiques de base.
        """
        self.nom = nom
        self.vie_max = vie_max
        self.vie = vie_max
        self.force = force
        self.arme = arme
        self.armure = armure

    def est_vivant(self) -> bool:
        """
        Vérifie si le personnage est toujours en vie.
        
        Returns:
            bool: True si les points de vie sont supérieurs à 0, False sinon.
        """
        return self.vie > 0

    def subir_degats(self, valeur: int) -> int:
        """
        Applique un montant de dégâts aux points de vie du personnage.
        
        Args:
            valeur (int): Le montant de dégâts à infliger.
            
        Returns:
            int: Le montant réel de dégâts déduits (ne peut pas être négatif).
        """
        degats_reels = max(0, valeur)
        self.vie -= degats_reels
        if self.vie < 0:
            self.vie = 0
        return degats_reels

    def calcul_degats_sur(self, cible) -> int:
        """
        Calcule les dégâts infligés à une cible avant application.
        
        La formule utilise un multiplicateur aléatoire via random.uniform.
        
        Args:
            cible (Personnage): Le personnage subissant l'attaque.
            
        Returns:
            int: Le montant des dégâts calculés (Force + Arme) * Aléa - Armure.
        """
        multiplicateur = uniform(0.8, 1.2)
        degats = (self.force + self.arme) * multiplicateur - cible.armure
        return int(max(0, degats))

    def attaquer(self, cible) -> int:
        """
        Effectue une attaque complète sur une cible.
        
        Args:
            cible (Personnage): La cible à attaquer.
            
        Returns:
            int: Les dégâts réels infligés après défense de la cible.
        """
        degats = self.calcul_degats_sur(cible)
        return cible.subir_degats(degats)