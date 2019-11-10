#client recevant les messages du master
#bon, ça fonctionne mais j'ai un problème avec mon datetime

import socket
import datetime

server_addr = ("192.168.56.1", 60000)

def ddos():
    attaque = (slave.recv(1024))
    if attaque == b"attc":
        print("signal reçu")
        if (datetime.date == 2019, 11, 7) and (datetime.time == 14, 19):
            slave.sendall(b"potentielle attaque ddos")
        else:
            slave.sendall(b"donnees incorrectes")
    else:
        slave.sendall(b"euh probleme")

slave = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
slave.connect(server_addr)
print("slave connecté au serveur")

ddos()

slave.close()
