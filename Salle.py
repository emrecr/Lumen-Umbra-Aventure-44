"""
Module Salle.py
===============
Représente une salle du donjon : description, présence d'un lit,
sorties vers d'autres salles, objets au sol et ennemis.
"""

from __future__ import annotations
from typing import Dict, List, Optional


class Salle:
    """Représente une pièce du donjon.

    Une salle possède un nom, une description, peut contenir des objets
    et des ennemis, dispose de sorties vers d'autres salles et peut offrir
    un lit permettant au héros de se reposer.

    Attributes:
        nom (str): Nom affiché de la salle.
        description (str): Texte de description affiché au joueur.
        a_lit (bool): ``True`` si la salle contient un lit (soin complet).
        sorties (dict[str, Salle]): Mapping direction → salle destination.
        objets (list): Objets présents au sol dans la salle.
        ennemis (list): Ennemis présents dans la salle.
    """

    def __init__(
        self,
        nom: str,
        description: str,
        a_lit: bool = False,
    ) -> None:
        """Initialise une salle vide (sans sorties, sans objets, sans ennemis).

        Args:
            nom (str): Nom de la salle.
            description (str): Description textuelle.
            a_lit (bool, optional): Présence d'un lit. Défaut ``False``.
        """
        self.nom: str = nom
        self.description: str = description
        self.a_lit: bool = a_lit
        self.sorties: Dict[str, "Salle"] = {}
        self.objets: list = []
        self.ennemis: list = []

    # ------------------------------------------------------------------
    # Gestion des sorties
    # ------------------------------------------------------------------

    def ajouter_sortie(self, direction: str, destination: "Salle") -> None:
        """Ajoute une sortie dans la direction donnée.

        Args:
            direction (str): Direction (ex. ``"nord"``, ``"sud"``…).
            destination (Salle): Salle vers laquelle mène cette sortie.
        """
        self.sorties[direction] = destination

    def peut_quitter(self) -> bool:
        """Indique si la salle possède au moins une sortie.

        Returns:
            bool: ``True`` s'il existe au moins une sortie.
        """
        return len(self.sorties) > 0

    # ------------------------------------------------------------------
    # Gestion des objets
    # ------------------------------------------------------------------

    def recuperer_objets(self) -> list:
        """Retourne la liste des objets présents et vide la salle.

        Returns:
            list[Objet]: Objets ramassés.
        """
        ramasses = list(self.objets)
        self.objets = []
        return ramasses

    # ------------------------------------------------------------------
    # Représentation
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return f"Salle(nom={self.nom!r}, sorties={list(self.sorties.keys())})"