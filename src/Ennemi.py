# src/Ennemi.py  

from src import Personnage
import random


class Ennemi(Personnage):

    def __init__(self, nom: str, vie_max: int, force: int, exp: int):
        super().__init__(nom, vie_max, force)
        self.exp = exp

    def decision_action(self) -> str:
        if self.vie / self.vie_max < 0.2:
            return 'fuit' if random.random() < 0.7 else 'attaque'
        else:
            return 'attaque' if random.random() < 0.8 else 'fuit'

    def donner_exp(self, hero) -> int:
        if not self.est_vivant():
            hero.gagner_exp(self.exp)
            return self.exp
        return 0