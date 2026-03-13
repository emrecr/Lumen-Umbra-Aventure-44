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
    def charger_depuis_fichier(self, chemin: str) -> None:
        """Charge le donjon depuis un fichier JSON.

        Args:
            chemin (str): Chemin vers le fichier JSON.

        Raises:
            FileNotFoundError: Si le fichier n'existe pas.
            json.JSONDecodeError: Si le JSON est mal formé.
        """
        with open(chemin, "r", encoding="utf-8") as f:
            data = json.load(f)

        self._salle_depart_id = data["salle_depart"]
        salles_data = data["salles"]

        # Première passe : créer toutes les salles
        for identifiant, salle_data in salles_data.items():
            salle = Salle(
                nom=salle_data["nom"],
                description=salle_data["description"],
                a_lit=salle_data.get("a_lit", False),
            )
            for obj_data in salle_data.get("objets", []):
                try:
                    salle.objets.append(_creer_objet(obj_data))
                except (ValueError, KeyError):
                    pass
            for ennemi_data in salle_data.get("ennemis", []):
                salle.ennemis.append(_creer_ennemi(ennemi_data))

            self._index[identifiant] = salle
            self.catalogue_salles.append(salle)

        # Deuxième passe : relier les sorties
        for identifiant, salle_data in salles_data.items():
            salle_source = self._index[identifiant]
            for direction, id_dest in salle_data.get("sorties", {}).items():
                if id_dest in self._index:
                    salle_source.ajouter_sortie(direction, self._index[id_dest])

    def generer_entree(self) -> Salle:
        """Retourne la salle de départ du donjon.

        Returns:
            Salle: La salle initiale.

        Raises:
            ValueError: Si le donjon n'a pas encore été chargé.
        """
        if self._salle_depart_id not in self._index:
            raise ValueError("Donjon vide ou non chargé.")
        return self._index[self._salle_depart_id]

    def __repr__(self) -> str:
        return f"Donjon({len(self.catalogue_salles)} salle(s))"