from random import uniform
from abc import ABC, abstractmethod

class Personnage(ABC):
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
        self.estvivant = True

    def est_vivant(self) -> bool:
        """
        Vérifie si le personnage est toujours en vie.
        """
        return self.vie > 0

    def subir_degats(self, valeur: int):
        """
        Applique des dégâts à ce Personnage (diagramme: subirDegats(valeur: int)).
        Gère la mort (vie <=0 -> estvivant=False).
        :param valeur: Quantité de dégâts à subir (int >0)
        Exemple: bombe.utiliser(self) appelle ça avec degats.
        """
        self.vie -= valeur
        if self.vie <= 0:
            self.vie = 0  # Pas de vie négative
            self.estvivant = False  # Déclenche fin de combat?

    def calcul_degats_sur(self, cible) -> int:
        """
        Calcule les dégâts infligés à une cible avant application.
        """
        multiplicateur = uniform(0.8, 1.2)
        degats = (self.force + self.arme) * multiplicateur - cible.armure
        
        # CORRECTION 2 : Utilisation de round() pour arrondir au lieu de tronquer
        return int(round(max(0, degats)))

    def attaquer(self, cible) :
        """
        Effectue une attaque complète sur une cible.
        """
        if not self.estvivant:
            return
        degats = self.calcul_degats_sur_cible(cible)
        cible.subir_degats(degats)

    def soigner(self, valeur: int):
        """
        Restaure de la vie sur ce Personnage (diagramme: soigner(valeur: int)).
        Ne dépasse pas viemax (cap à vieMax).
        :param valeur: Quantité de PV à ajouter (int >0)
        Exemple: PotionSoin.utiliser(self) appelle ça.
        Cas limite: si vie == viemax, aucun effet (silencieux).
        """
        self.vie += valeur
        if self.vie > self.viemax:
            self.vie = self.viemax  # Overflow protection
    
    @abstractmethod
    def donner_recompenses(self, hero: 'Hero'):
        pass  # Implémenté dans Hero/Ennemi