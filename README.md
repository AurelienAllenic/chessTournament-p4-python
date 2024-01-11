# Système de gestion de tournois d'échecs

## Description
Ce projet Python est conçu pour que l'utilisateur / organisateur de tournoi puisse entrer les informations de chaque évènement ainsi que les joueurs inscrits.
A chaque round, l'organisateur renseigne le gagnant de la partie ou bien l'égalité. 

## Fonctionnalités

### Création de tournoi :
Création d'un tournoi incluant le nom, lieu, date, nombre de rounds, et nombre de participants.
Création de joueurs en renseignant le nom, prénom, date de naissance et identifiant.

### Matching :
Les joueurs s'affrontent d'abord aléatoirement puis en fonction de leur classement.
Si un nombre impair de joueurs ayant le même nombre de points joue, alors l'un d'entre eux affrontera un autre joueur n'ayant pas le même nombre de fois.
Si le nombre de joueurs est impair, alors un joueur, une fois par tournoi si possible, ne joue pas et reçoit 0.5 point. 
Une victoire vaut 1 point, unde défaite 0 et une égalité 0.5 point.

### Affichage des résultats :
Les résultats sont affichés en console sous la forme joueur1.prenom joueur1.nom is at the x place with x points

### Notation des résultats
Tous les résultats de chaque tournoi sont stockés dans un objet tournament dans data.json à l'issue de chaque tournoi.

## Prérequis
Python 3.11.3
Bibliothèques Python : requests, BeautifulSoup, pandas, voir le fichier requirements.
Un fichier data.json contenant ce code :
```python 
{
    "tournaments": [

    ]
}
```

## Installation

### Clonez ce dépôt en utilisant :

git clone https://github.com/AurelienAllenic/chessTournament-p4-python

### Installez les dépendances nécessaires :

pip install -r requirements.txt

## Usage

Pour lancer le script, exécutez :
python controller.py || éxécutez le script via votre IDE avec le fichier controller.py ouvert

## Structure du Projet
controller.py : Le script principal pour l'éxécution du script.
model.py : fichier contenant les différentes class de mon application.
view.py : fichier d'affichages de vues, de messages et d'input destinés à l'utilisateur.
requirements.txt : Fichier contenant les dépendances nécessaires.

## Générer un fichier flake8-html

Pour installer fleke8 et flake8-html, exécutez les commandes suivantes:

pip install flake8
pip install flake8-html

Pour générer un rapport complet au format HTML, exécutez la commande suivante en remplaçant votre_projet par le dossier contenant le projet:

flake8 --format=html --htmldir=rapport_flake8 votre_projet/

## Licence
Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.