from random import seed
from src.Hero import Hero
from src.Ennemi import Ennemi
from src.Personnage import Personnage

def combat_tour_par_tour(joueur: Hero, ennemi: Ennemi, log: bool = True) -> Personnage:
    """
    Simule un combat au tour par tour entre un héros et un ennemi.
    
    Le joueur a toujours l'initiative. Le combat s'arrête dès qu'un 
    combattant n'a plus de points de vie.
    
    Args:
        joueur (Hero): Le héros contrôlé par le joueur.
        ennemi (Ennemi): L'adversaire à affronter.
        log (bool): Si True, affiche le déroulement du combat dans la console.
        
    Returns:
        Personnage: L'instance du vainqueur (joueur ou ennemi).
    """
    tour = 1
    while joueur.est_vivant() and ennemi.est_vivant():
        if log:
            print(f"--- Tour {tour} ---")
        
        # Phase d'attaque du joueur
        dmg_joueur = joueur.attaquer(ennemi)
        if log:
            print(f"{joueur.nom} inflige {dmg_joueur} dégâts à {ennemi.nom} (PV {ennemi.vie}/{ennemi.vie_max})")
        
        # Vérification de la mort de l'ennemi
        if not ennemi.est_vivant():
            if log:
                print(f"{ennemi.nom} est vaincu ! {joueur.nom} gagne {ennemi.exp} XP.")
            joueur.gagner_exp(ennemi.exp)
            return joueur
            
        # Phase d'attaque de l'ennemi
        dmg_ennemi = ennemi.attaquer(joueur)
        if log:
            print(f"{ennemi.nom} inflige {dmg_ennemi} dégâts à {joueur.nom} (PV {joueur.vie}/{joueur.vie_max})")
            
        # Vérification de la mort du joueur
        if not joueur.est_vivant():
            if log:
                print(f"{joueur.nom} est vaincu !")
            return ennemi
            
        tour += 1
    
    return joueur if joueur.est_vivant() else ennemi

if __name__ == "__main__":
    # Configuration pour la reproductibilité
    seed(44)
    
    # Initialisation des personnages selon le cahier des charges
    mon_hero = Hero(nom="Gustave", vie_max=300, force=60, arme=20, armure=10)
    mon_ennemi = Ennemi(nom="Dualliste", vie_max=200, force=40, arme=10, armure=0, exp=250)
    
    # Lancement du combat
    vainqueur = combat_tour_par_tour(mon_hero, mon_ennemi, log=True)
    
    # Affichage du bilan final
    print(f"Vainqueur : {vainqueur.nom}")
    print(f"{mon_hero.nom} - Niveau {mon_hero.niveau}, XP {mon_hero.exp}/{mon_hero.exp_pour_prochain_niveau()}")