# j'ai fais un code ou un maitre et un bot communique ensemble, le bot envoie le message 'Hello World au serveur
#je pense que sa t'aidera avec ton code pour la date

import socket as modsocket

def connexion():
    s = modsocket.socket(modsocket.AF_INET, modsocket.SOCK_STREAM)

    s.connect(("localhost", 5000))

    s.sendall(b"Hello, world")
    data = s.recv(1024)
    s.close()
    print ("Received", repr(data))

connexion()
