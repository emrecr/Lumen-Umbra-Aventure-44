from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from src.personnages.Hero import Hero
    from src.personnages.Ennemi import Ennemi
    from src.Salle import Salle
    from src.objets.objet import Consommable


class Action(ABC):
    """Classe abstraite représentant une action du joueur.

    Attributes:
        hero (Hero): Le héros qui effectue l'action.
        salle_courante (Salle): La salle où se trouve le héros.
    """

    def __init__(self, hero: "Hero", salle_courante: "Salle") -> None:
        """Initialise une action.

        Args:
            hero (Hero): Héros actif.
            salle_courante (Salle): Salle dans laquelle se trouve le héros.
        """
        self.hero = hero
        self.salle_courante = salle_courante

    @abstractmethod
    def est_possible(self) -> bool:
        """Indique si l'action peut être réalisée dans l'état courant.

        Returns:
            bool: True si l'action est disponible.
        """

    @abstractmethod
    def executer(self) -> None:
        """Exécute l'action et met à jour le modèle."""


# ---------------------------------------------------------------------------
# Observer
# ---------------------------------------------------------------------------

class Observer(Action):
    """Observe la salle courante (affiche sa description).

    Disponible uniquement lorsqu'il n'y a aucun ennemi dans la salle.
    """

    def est_possible(self) -> bool:
        """Possible si aucun ennemi n'est présent.

        Returns:
            bool: True si la salle ne contient pas d'ennemi.
        """
        return len(self.salle_courante.ennemis) == 0

    def executer(self) -> None:
        """Ne modifie pas le modèle (l'affichage est géré par la vue)."""
        pass


# ---------------------------------------------------------------------------
# SeDeplacer
# ---------------------------------------------------------------------------

class SeDeplacer(Action):
    """Déplace le héros vers une salle adjacente.

    Attributes:
        destination (Salle): Salle cible du déplacement.
    """

    def __init__(self, hero: "Hero", salle_courante: "Salle", destination: "Salle") -> None:
        """Initialise l'action de déplacement.

        Args:
            hero (Hero): Héros actif.
            salle_courante (Salle): Salle de départ.
            destination (Salle): Salle d'arrivée souhaitée.
        """
        super().__init__(hero, salle_courante)
        self.destination = destination

    def est_possible(self) -> bool:
        """Possible si aucun ennemi et destination accessible.

        Returns:
            bool: True si la salle peut être quittée vers cette destination.
        """
        return (
            len(self.salle_courante.ennemis) == 0
            and self.destination in self.salle_courante.sorties.values()
        )

    def executer(self) -> None:
        """Le déplacement effectif est géré par le contrôleur (ui/interface.py)."""
        pass


# ---------------------------------------------------------------------------
# Attaquer
# ---------------------------------------------------------------------------

class Attaquer(Action):
    """Le héros attaque un ennemi de la salle.

    Attributes:
        cible (Ennemi): Ennemi visé par l'attaque.
    """

    def __init__(self, hero: "Hero", salle_courante: "Salle", cible: "Ennemi") -> None:
        """Initialise l'action d'attaque.

        Args:
            hero (Hero): Héros attaquant.
            salle_courante (Salle): Salle du combat.
            cible (Ennemi): Ennemi à attaquer.
        """
        super().__init__(hero, salle_courante)
        self.cible = cible

    def est_possible(self) -> bool:
        """Possible si la cible est dans la salle et encore en vie.

        Returns:
            bool: True si la cible est présente et vivante.
        """
        return (
            self.cible in self.salle_courante.ennemis
            and self.cible.est_vivant()
        )

    def executer(self) -> None:
        """Attaque la cible. Si elle meurt, retire-la de la salle et transfère récompenses/XP."""
        self.hero.attaquer(self.cible)
        if not self.cible.est_vivant():
            self.salle_courante.ennemis.remove(self.cible)
            self.cible.donner_exp(self.hero)
            self.cible.donner_recompenses(self.hero)


# ---------------------------------------------------------------------------
# Ramasser
# ---------------------------------------------------------------------------

class Ramasser(Action):
    """Le héros ramasse tous les objets présents dans la salle."""

    def est_possible(self) -> bool:
        """Possible si aucun ennemi et au moins un objet au sol.

        Returns:
            bool: True si la salle est sûre et contient des objets.
        """
        return (
            len(self.salle_courante.ennemis) == 0
            and len(self.salle_courante.objets) > 0
        )

    def executer(self) -> None:
        """Ramasse tous les objets de la salle et les ajoute à l'inventaire."""
        objets = self.salle_courante.recuperer_objets()
        for objet in objets:
            self.hero.inventaire.ajouter_objet(objet)


# ---------------------------------------------------------------------------
# SeReposer
# ---------------------------------------------------------------------------

class SeReposer(Action):
    """Le héros se repose dans un lit pour récupérer tous ses PV."""

    def est_possible(self) -> bool:
        """Possible si aucun ennemi et la salle possède un lit.

        Returns:
            bool: True si sûr et lit présent.
        """
        return (
            len(self.salle_courante.ennemis) == 0
            and self.salle_courante.a_lit
        )

    def executer(self) -> None:
        """Restaure complètement les PV du héros."""
        self.hero.vie = self.hero.vie_max


# ---------------------------------------------------------------------------
# Fuir
# ---------------------------------------------------------------------------

class Fuir(Action):
    """Le héros fuit le combat vers la salle précédente.

    Attributes:
        salle_precedente (Salle | None): Salle vers laquelle fuir.
    """

    def __init__(self, hero: "Hero", salle_courante: "Salle", salle_precedente: Optional["Salle"]) -> None:
        """Initialise l'action de fuite.

        Args:
            hero (Hero): Héros fuyant.
            salle_courante (Salle): Salle actuelle (avec ennemis).
            salle_precedente (Salle | None): Salle vers laquelle fuir.
        """
        super().__init__(hero, salle_courante)
        self.salle_precedente = salle_precedente

    def est_possible(self) -> bool:
        """Possible si des ennemis sont présents et une retraite est disponible.

        Returns:
            bool: True si la fuite est envisageable.
        """
        return (
            len(self.salle_courante.ennemis) > 0
            and self.salle_precedente is not None
        )

    def executer(self) -> None:
        """Le déplacement effectif est géré par le contrôleur (ui/interface.py)."""
        pass


# ---------------------------------------------------------------------------
# Utiliser
# ---------------------------------------------------------------------------

class Utiliser(Action):
    """Le héros utilise un objet consommable de son inventaire.

    Attributes:
        objet (Consommable): Consommable à utiliser.
        cible: Personnage ciblé (le héros lui-même par défaut).
    """

    def __init__(self, hero: "Hero", salle_courante: "Salle", objet: "Consommable", cible=None) -> None:
        """Initialise l'action d'utilisation.

        Args:
            hero (Hero): Héros actif.
            salle_courante (Salle): Salle courante.
            objet (Consommable): Objet à utiliser.
            cible: Cible de l'effet (défaut : le héros lui-même).
        """
        super().__init__(hero, salle_courante)
        self.objet = objet
        self.cible = cible if cible is not None else hero

    def est_possible(self) -> bool:
        """Possible si le héros possède au moins une unité de cet objet.

        Returns:
            bool: True si l'objet est dans l'inventaire du héros.
        """
        return self.hero.inventaire.get_quantite(self.objet) > 0

    def executer(self) -> None:
        """Utilise le consommable sur la cible et le retire de l'inventaire."""
        self.hero.inventaire.utiliser_consommable(self.objet, self.cible)
