
from __future__ import annotations
import json
from typing import List, Optional

from src.Salle import Salle
from src.objets.objet import PotionSoin, Bombe, Equipement
from src.personnages.Ennemi import Ennemi

"""
Module Donjon.py
================
Gère l'ensemble du donjon : catalogue des salles, chargement depuis un
fichier JSON et génération de la salle de départ.
"""


# Correspondance type JSON → classe objet
_TYPE_OBJET = {
    "PotionDeSoin": lambda d: PotionSoin(d["nom"], d["description"], d["quantite"]),
    "Bombe":        lambda d: Bombe(d["nom"], d["description"], d["degats"]),
    "Arme":         lambda d: Equipement(d["nom"], d["description"], bonusforce=d.get("bonus", 0)),
    "Armure":       lambda d: Equipement(d["nom"], d["description"], bonusdefense=d.get("bonus", 0)),
}


def _creer_objet(data: dict):
    """Instancie un objet à partir de son dictionnaire JSON.

    Args:
        data (dict): Dictionnaire avec au minimum la clé ``"type"``.

    Returns:
        Objet: Instance de la classe correspondante.

    Raises:
        ValueError: Si le type est inconnu.
    """
    type_str = data.get("type", "")
    fabrique = _TYPE_OBJET.get(type_str)
    if fabrique is None:
        raise ValueError(f"Type d'objet inconnu : '{type_str}'")
    return fabrique(data)


def _creer_ennemi(data: dict) -> Ennemi:
    """Instancie un ennemi à partir de son dictionnaire JSON.

    Args:
        data (dict): Dictionnaire décrivant l'ennemi.

    Returns:
        Ennemi: Instance configurée.
    """
    arme_bonus = 0
    armure_bonus = 0
    if data.get("arme"):
        arme_bonus = data["arme"].get("bonus", 0)
    if data.get("armure"):
        armure_bonus = data["armure"].get("bonus", 0)

    ennemi = Ennemi(
        nom=data["nom"],
        vie_max=data["vie_max"],
        force=data["force"],
        arme=arme_bonus,
        armure=armure_bonus,
        exp=data.get("exp", 0),
    )

    # Récompenses de l'ennemi
    for obj_data in data.get("recompenses", []):
        try:
            ennemi.recompenses[_creer_objet(obj_data)] = obj_data.get("qte", 1)
        except (ValueError, KeyError):
            pass  # Objet inconnu ignoré silencieusement

    return ennemi


class Donjon:
    """Représente l'ensemble du donjon.

    Le donjon est un graphe de salles reliées par des sorties. Il peut être
    chargé depuis un fichier JSON dont le format est décrit dans le sujet.

    Attributes:
        catalogue_salles (list[Salle]): Toutes les salles du donjon.
        _salle_depart_id (str): Identifiant de la salle de départ.
        _index (dict[str, Salle]): Mapping identifiant → salle (usage interne).
    """

    def __init__(self) -> None:
        """Crée un donjon vide."""
        self.catalogue_salles: List[Salle] = []
        self._salle_depart_id: str = ""
        self._index: dict = {}