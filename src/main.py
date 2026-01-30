from random import seed
from src.Hero import Hero
from src.Ennemi import Ennemi
from src.Personnage import Personnage

def combat_tour_par_tour(joueur: Hero, ennemi: Ennemi, log: bool = True) -> Personnage:
    """
    Simule un combat entre le joueur et l'ennemi.
    Renvoie le vainqueur.
    """
    tour = 1
    while joueur.est_vivant() and ennemi.est_vivant():
        if log:
            print(f"--- Tour {tour} ---")
        
        # Le joueur attaque l'ennemi
        degats_joueur = joueur.attaquer(ennemi)
        if log:
            print(f"{joueur.nom} inflige {degats_joueur} dégâts à {ennemi.nom} (PV {ennemi.vie}/{ennemi.vie_max})")
        
        if not ennemi.est_vivant():
            if log:
                print(f"{ennemi.nom} est vaincu ! {joueur.nom} gagne {ennemi.exp} XP.")
            joueur.gagner_exp(ennemi.exp)
            return joueur
            
        # L'ennemi attaque le joueur
        degats_ennemi = ennemi.attaquer(joueur)
        if log:
            print(f"{ennemi.nom} inflige {degats_ennemi} dégâts à {joueur.nom} (PV {joueur.vie}/{joueur.vie_max})")
            
        tour += 1
    return joueur if joueur.est_vivant() else ennemi

if __name__ == "__main__":
    seed(44)
    hero = Hero(nom="Gustave", vie_max=300, force=60, arme=20, armure=10)
    adversaire = Ennemi(nom="Dualliste", vie_max=200, force=40, arme=10, armure=0, exp=250)
    
    vainqueur = combat_tour_par_tour(hero, adversaire, log=True)
    
    print(f"Vainqueur : {vainqueur.nom}")
    print(f"{hero.nom} - Niveau {hero.niveau}, XP {hero.exp}/{hero.exp_pour_prochain_niveau()}")