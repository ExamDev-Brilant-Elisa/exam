#importation du module socket afin de permetttre une communication réseau
import socket as modSocket

"""
création de l'objet communication
avec le champ conn.
"""
class Communication():

    def __init__(self, conn):
        self.conn = conn


#on choisi la famille AF_NET pour utiliser l'ipv4, en mode TCP
#on bind grace au nom de la machine sur un port non existant
s = modSocket.socket(modSocket.AF_INET, modSocket.SOCK_STREAM)
s.bind(("localhost", 5000))
#boucle infini pour laisser le slave tout le temps allumer et en attente de connexion
while True:
    try:
        s.listen()
        conn, addr = s.accept()
        print("Connecion acceptée avec : ", addr)

        b = Communication(conn)
    except ConnectionAbortedError:
        print("Connexion interrompue avec la machine : ", addr)

s.close()



