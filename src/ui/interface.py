from __future__ import annotations
from typing import List, Optional

from src.Salle import Salle
from src.Donjon import Donjon
from src.personnages.Hero import Hero
from src.personnages.Ennemi import Ennemi
from src.objets.objet import Consommable, PotionSoin, Bombe
from src.actions.action import (
    Action, Observer, SeDeplacer, Attaquer,
    Ramasser, SeReposer, Fuir, Utiliser,
)

# ---------------------------------------------------------------------------
# Affichage
# ---------------------------------------------------------------------------

def afficher_etat_hero(hero: Hero) -> None:
    """Affiche le résumé des statistiques du héros.

    Args:
        hero (Hero): Héros à afficher.
    """
    print(
        f"{hero.nom}  |  Niveau {hero.niveau}  |  "
        f"PV : {hero.vie}/{hero.vie_max}  |  "
        f"Force : {hero.force}  |  "
        f"XP : {hero.exp}/{hero.exp_pour_prochain_niveau()}"
    )


def afficher_etat_salle(salle: Salle) -> None:
    """Affiche le nom, les ennemis, les objets et les sorties de la salle.

    Args:
        salle (Salle): Salle à afficher.
    """
    print("─" * 50)
    print(f"emplacement :{salle.nom}")
    print("─" * 50)
    if salle.ennemis:
        print(f"Ennemis : {', '.join(e.nom for e in salle.ennemis)}")
    else:
        print("Aucun ennemi.")
    sorties = ", ".join(salle.sorties.keys()) if salle.sorties else "aucune"
    print(f"Sorties : {sorties}")
    if salle.objets:
        print(f"Objets : {', '.join(o.nom for o in salle.objets)}")
    if salle.a_lit:
        print("Cette salle possède un lit.")
    print("─" * 50)


# ---------------------------------------------------------------------------
# Construction des actions disponibles
# ---------------------------------------------------------------------------

def construire_actions(
    hero: Hero,
    salle: Salle,
    salle_precedente: Optional[Salle],
) -> List[Action]:
    """Construit la liste de toutes les actions réalisables dans l'état courant.

    Args:
        hero (Hero): Héros actif.
        salle (Salle): Salle courante.
        salle_precedente (Salle | None): Salle précédente (pour Fuir).

    Returns:
        list[Action]: Actions dont est_possible() est True.
    """
    candidats: List[Action] = [
        Observer(hero, salle),
        SeReposer(hero, salle),
        Ramasser(hero, salle),
    ]
    for dest in salle.sorties.values():
        candidats.append(SeDeplacer(hero, salle, dest))
    for e in salle.ennemis:
        candidats.append(Attaquer(hero, salle, e))
    candidats.append(Fuir(hero, salle, salle_precedente))
    for objet in hero.inventaire.lister_objets():
        if isinstance(objet, Consommable):
            candidats.append(Utiliser(hero, salle, objet))

    return [a for a in candidats if a.est_possible()]


def _libelle(action: Action, salle: Salle) -> str:
    """Retourne un libellé lisible pour une action.

    Args:
        action (Action): Action à décrire.
        salle (Salle): Salle courante.

    Returns:
        str: Libellé affiché dans le menu.
    """
    if isinstance(action, Observer):
        return "Observer la salle"
    if isinstance(action, SeReposer):
        return "Se reposer (soin complet)"
    if isinstance(action, Ramasser):
        return f"Ramasser les objets ({len(salle.objets)} au sol)"
    if isinstance(action, SeDeplacer):
        direction = next(
            (d for d, s in salle.sorties.items() if s is action.destination), "?"
        )
        return f"Se déplacer vers {action.destination.nom} ({direction})"
    if isinstance(action, Attaquer):
        return f"Attaquer {action.cible.nom} (PV: {action.cible.vie}/{action.cible.vie_max})"
    if isinstance(action, Fuir):
        return f"Fuir vers {action.salle_precedente.nom}"
    if isinstance(action, Utiliser):
        qte = action.hero.inventaire.get_quantite(action.objet)
        return f"Utiliser {action.objet.nom} ×{qte}"
    return type(action).__name__


def choisir_action(
    hero: Hero,
    salle: Salle,
    salle_precedente: Optional[Salle],
) -> Optional[Action]:
    """Affiche le menu des actions et retourne le choix du joueur.

    Args:
        hero (Hero): Héros actif.
        salle (Salle): Salle courante.
        salle_precedente (Salle | None): Salle précédente.

    Returns:
        Action | None: Action choisie, ou None si aucune disponible.
    """
    actions = construire_actions(hero, salle, salle_precedente)
    if not actions:
        print("  Aucune action disponible.")
        return None

    print("\n  Que voulez-vous faire ?")
    for i, action in enumerate(actions, start=1):
        print(f"  [{i}] {_libelle(action, salle)}")

    while True:
        try:
            choix = int(input("  > "))
            if 1 <= choix <= len(actions):
                return actions[choix - 1]
        except (ValueError, EOFError):
            pass
        print(f"  Entrez un nombre entre 1 et {len(actions)}.")


def afficher_resultat_action(
    action: Action,
    hero: Hero,
    salle: Salle,
    nouvelle_salle: Optional[Salle] = None,
) -> None:
    """Affiche le résultat d'une action exécutée.

    Args:
        action (Action): Action exécutée.
        hero (Hero): Héros (état post-exécution).
        salle (Salle): Salle courante avant déplacement éventuel.
        nouvelle_salle (Salle | None): Nouvelle salle après déplacement.
    """
    if isinstance(action, Observer):
        print(f"\n Description de la salle : {salle.description}")
    elif isinstance(action, SeReposer):
        print(f"\n{hero.nom} se repose… PV restaurés ({hero.vie}/{hero.vie_max}).")
    elif isinstance(action, Ramasser):
        print(f"\n Objets ramassés et ajoutés à l'inventaire.")
    elif isinstance(action, (SeDeplacer, Fuir)) and nouvelle_salle:
        print(f"\n {hero.nom} se déplace vers {nouvelle_salle.nom}.")
    elif isinstance(action, Attaquer):
        e = action.cible
        if e.est_vivant():
            print(f"\n {hero.nom} attaque {e.nom}. PV ennemis : {e.vie}/{e.vie_max}.")
        else:
            print(
                f"\n {e.nom} est vaincu ! "
                f"XP : {hero.exp}/{hero.exp_pour_prochain_niveau()}"
            )
    elif isinstance(action, Utiliser):
        objet = action.objet
        cible = action.cible
        if isinstance(objet, PotionSoin):
            print(f"\n {hero.nom} utilise {objet.nom}. PV : {cible.vie}/{cible.vie_max}.")
        elif isinstance(objet, Bombe):
            print(f"\n {hero.nom} lance {objet.nom} sur {cible.nom}. PV ennemis : {cible.vie}/{cible.vie_max}.")
        else:
            print(f"\n {hero.nom} utilise {objet.nom}.")


# ---------------------------------------------------------------------------
# Boucle principale
# ---------------------------------------------------------------------------

def demarrer_jeu(chemin_donjon: str = "donjon.json") -> None:
    """Lance la boucle principale du jeu.

    Args:
        chemin_donjon (str): Chemin vers le fichier JSON du donjon.
    """
    donjon = Donjon()
    donjon.charger_depuis_fichier(chemin_donjon)
    salle_courante: Salle = donjon.generer_entree()

    print("\n  ╔══════════════════════════════════════╗")
    print("  ║   LUMEN-UMBRA : AVENTURE 44          ║")
    print("  ╚══════════════════════════════════════╝\n")
    nom = input("  Entrez le nom de votre héros : ").strip() or "Héros"
    hero = Hero(nom=nom, vie_max=100, force=15, arme=0, armure=0)

    salle_precedente: Optional[Salle] = None

    while hero.est_vivant():
        print()
        afficher_etat_hero(hero)
        afficher_etat_salle(salle_courante)

        action = choisir_action(hero, salle_courante, salle_precedente)
        if action is None:
            break

        nouvelle_salle: Optional[Salle] = None
        if isinstance(action, SeDeplacer):
            nouvelle_salle = action.destination
        elif isinstance(action, Fuir):
            nouvelle_salle = action.salle_precedente

        action.executer()

        if isinstance(action, (SeDeplacer, Fuir)) and nouvelle_salle:
            salle_precedente = salle_courante
            salle_courante = nouvelle_salle

        afficher_resultat_action(action, hero, salle_courante, nouvelle_salle)

        # Tour des ennemis
        for ennemi in list(salle_courante.ennemis):
            if not hero.est_vivant():
                break
            if not ennemi.est_vivant():
                continue
            if ennemi.decision_action() == "attaque":
                degats = ennemi.attaquer(hero)
                print(
                    f"{ennemi.nom} attaque {hero.nom} ! "
                    f"Dégâts : {degats}. PV : {hero.vie}/{hero.vie_max}."
                )
            else:
                print(f"{ennemi.nom} recule !")
                salle_courante.ennemis.remove(ennemi)

    print("\n" + "═" * 50)
    if hero.est_vivant():
        print(f"  Aventure terminée. Niveau final : {hero.niveau}.")
    else:
        print(f"{hero.nom} est tombé au combat. Game Over.")
    print("═" * 50)
 
 
if __name__ == "__main__":
    import os
    chemin = os.path.join(os.path.dirname(__file__), "..", "..", "donjon.json")
    demarrer_jeu(chemin)