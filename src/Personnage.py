from random import uniform

class Personnage:
    """
    Classe de base représentant un combattant dans le jeu.
    """

    # CORRECTION 1 : Ajout de valeurs par défaut pour arme et armure (=0)
    def __init__(self, nom: str, vie_max: int, force: int, arme: int = 0, armure: int = 0):
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
        """
        return self.vie > 0

            self.vie = 0
            
        # CORRECTION : On retourne ce qu'on a vraiment perdu
        return vie_avant - self.vie


    def calcul_degats_sur(self, cible) -> int:
        """
        Calcule les dégâts infligés à une cible avant application.
        """
        multiplicateur = uniform(0.8, 1.2)
        degats = (self.force + self.arme) * multiplicateur - cible.armure
        
        # CORRECTION 2 : Utilisation de round() pour arrondir au lieu de tronquer
        return int(round(max(0, degats)))

    def attaquer(self, cible) -> int:
        """
        Effectue une attaque complète sur une cible.
        """
        # CORRECTION 3 : Vérifier que tout le monde est vivant avant d'attaquer
        if not self.est_vivant() or not cible.est_vivant():
            return 0
            
        degats = self.calcul_degats_sur(cible)
        return cible.subir_degats(degats)
