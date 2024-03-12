# Memory Game

Ce projet est un jeu de mémoire simple réalisé en utilisant PySide6, qui est une bibliothèque Python pour créer des interfaces graphiques utilisant le framework Qt.

## Fonctionnalités actuelles

- Affiche une grille de cartes mélangées au démarrage du jeu.
- Les joueurs peuvent cliquer sur les cartes pour les retourner.
- Les cartes retournées affichent leur valeur et leur couleur de texte est modifiée en noir.
- Si deux cartes retournées ne correspondent pas, elles sont retournées face cachée après un court délai.

## Utilisation

Assurez-vous d'avoir Python installé sur votre système. Ensuite, installez les dépendances requises en exécutant la commande suivante :

pip install PySide6
Ensuite, exécutez le jeu en utilisant la commande :

python memory.py

## Fonctionnalités futures
Jeu multijoueur : Ajouter la possibilité de jouer en multijoueur sur le même appareil ou en réseau.
Choix de set d'images : Permettre aux joueurs de choisir parmi différents sets d'images pour les cartes du jeu, par exemple des animaux, des fruits, etc.
Système de score : Ajouter un système de score pour suivre les tentatives et le temps.
Écran de fin de partie : Implémenter un écran de fin de partie avec un message de victoire lorsque toutes les paires sont trouvées.
Différents niveaux de difficulté : Permettre aux joueurs de choisir différents niveaux de difficulté avec plus de cartes.