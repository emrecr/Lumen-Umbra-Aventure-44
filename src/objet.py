from abc import ABC, abstractmethod
from Personnage import Personnage

class Objet(ABC):
    """
    Classe abstraite représentant un objet générique du jeu (diagramme: Objet).
    Sert de base à Consommable et Equipement.
    """
    def __init__(self, nom: str, description: str):
        """
        Initialise un objet avec nom et description (attributs du diagramme).
        :param nom: Nom de l'objet (str)
        :param description: Description textuelle (str)
        """
        self.nom = nom
        self.description = description

class Consommable(Objet):
    """
    Hérite d'Objet pour les objets utilisables une fois (ex: potions, bombes).
    Diagramme: Consommable -> utiliser(cible: Personnage).
    """
    def __init__(self, nom: str, description: str):
        super().__init__(nom, description)

    @abstractmethod
    def utiliser(self, cible: Personnage) -> int:
        """
        Applique l'effet du consommable sur la cible et retourne l'effet appliqué.
        :param cible: Personnage à affecter (Hero ou Ennemi)
        :return: Valeur de l'effet (soin ou dégâts)
        """

class PotionSoin(Consommable):
    """
    Potion qui soigne un Personnage (ex: PotionSoin du diagramme).
    """
    def __init__(self, nom: str, description: str, valeursoin: int):
        super().__init__(nom, description)
        self.valeursoin = valeursoin  # Quantité de PV restaurés

    def utiliser(self, cible: Personnage) -> int:
        """
        Soigne la cible via Personnage.soigner().
        Diagramme: utilise soigner(valeur) sur cible.
        :param cible: Personnage à soigner
        :return: Valeur de soin appliquée
        """
        cible.soigner(self.valeursoin)
        return self.valeursoin

class Bombe(Consommable):
    """
    Bombe qui inflige des dégâts à un Personnage (ex: Bombe du diagramme).
    """
    def __init__(self, nom: str, description: str, degats: int):
        super().__init__(nom, description)
        self.degats = degats  # Dégâts infligés

    def utiliser(self, cible: Personnage) -> int:
        """
        Inflige des dégâts à la cible via Personnage.subir_degats().
        :param cible: Personnage à endommager
        :return: Valeur de dégâts infligés
        """
        cible.subir_degats(self.degats)
        return self.degats

class Equipement(Objet):
    """
    Équipement offrant des bonus (Arme/Armure du diagramme).
    Peut être équipé sur Hero/Personnage (arme/armure).
    """
    def __init__(self, nom: str, description: str, bonusforce: int = 0, bonusdefense: int = 0):
        """
        Initialise avec bonus (utilisés dans calcul_degats_sur_cible).
        :param bonusforce: Bonus à la force (attaque)
        :param bonusdefense: Bonus à la défense (réduire dégâts futurs?)
        """
        super().__init__(nom, description)
        self.bonusforce = bonusforce
        self.bonusdefense = bonusdefense  # À utiliser dans subir_degats si besoin
