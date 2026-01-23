# Lumen-Umbra : Aventure 44

Prototype de jeu de rôle au tour par tour de type rogue-like développé pour le studio RainFall Interactive. Ce projet simule un système de combat entre un héros et des créatures ennemies, sans interface graphique, servant de base pour le développement du jeu complet.

## Prérequis

- Python 3.10+
- Git

## Installation

```bash
git clone https://github.com/emrecr/Lumen-Umbra-Aventure-44.git
cd Lumen-Umbra-Aventure-44
```

Les dépendances nécessaires sont :
- `pdoc` : génération automatique de la documentation
- `pytest` : exécution des tests unitaires
- `coverage` : calcul du taux de couverture des tests

## Utilisation

En cours...

## Fonctionnalités prévues

- **Système de personnages** : Héros et ennemis avec caractéristiques (PV, force, arme, armure)
- **Combat au tour par tour** : Simulation de combats avec calcul de dégâts
- **Système de progression** : Gain d'expérience et montée de niveau pour le héros
- **Formule de dégâts** : `(Force + Bonus arme - Armure adversaire) × Facteur aléatoire [1.00-1.10]`
- **Progression XP** : `exp_suivant = 100 × (niveau² + niveau)`

## Tests

Pour exécuter les tests unitaires :

```bash
coverage run -m pytest
```

Pour afficher le rapport de couverture :

```bash
coverage report -m
```

## Documentation

Pour générer la documentation HTML à partir des docstrings :

```bash
pdoc -o docs/ src
```

La documentation sera disponible dans le dossier `docs/` et consultable dans un navigateur.

## Auteurs

- **CHAIBI NASSIM** — Développeur — @na2s-lab
- **RAKEB SOUSSI ISMAIL** — Développeur — @ismail-190
- **CINAR Emre** — Développeur — @emrecr
- **Lucien Mousin** — Encadrant — @lucienmousin

## Contexte pédagogique

Projet réalisé dans le cadre du cours de Développement d'Application (L2 SdN).

**Objectifs pédagogiques :**
- Programmation orientée objet en Python
- Versionning avec Git et GitHub
- Test Driven Development (TDD)
- Documentation de code
- Travail collaboratif en binôme