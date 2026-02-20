from typing import Dict, List
from src.Objet import Objet, Consommable
from src.Personnage import Personnage

class Inventaire:
    def __init__(self):
        self.contenus: Dict[Objet, int] = {}

    def ajouter_objet(self, objet: Objet, quantite: int = 1):
        if objet in self.contenus:
            self.contenus[objet] += quantite
        else:
            self.contenus[objet] = quantite

    def retirer_objet(self, objet: Objet, quantite: int = 1):
        if objet in self.contenus:
            self.contenus[objet] -= quantite
            if self.contenus[objet] <= 0:
                del self.contenus[objet]

    def get_quantite(self, objet: Objet) -> int:
        return self.contenus.get(objet, 0)

    def utiliser_consommable(self, objet: Consommable, cible: Personnage):
        if isinstance(objet, Consommable) and objet in self.contenus and self.contenus[objet] > 0:
            effet = objet.utiliser(cible)
            self.retirer_objet(objet, 1)
            return effet
        return 0

    def lister_objets(self) -> List[Objet]:
        return list(self.contenus.keys())