#commande de base pour une communication entre le maitre et ces slave
#pour ameliorer ce programme ont peut implementer du multiThreading afin que plusieurs pc slave puisse se connecter au maitre
#içi seulement un seul pc slave a la fois peut communiquer avec le maitre

import socket as modSocket

s = modSocket.socket(modSocket.AF_INET, modSocket.SOCK_STREAM)

s.bind(("localhost", 5000))

s.listen()
conn, addr = s.accept()

print ("Connexion avec l'adresse: ", addr)

def start_log(conn):

    conn.send("Execute".encode("utf-8"))
    print(conn.recv(1024).decode("utf-8"))

start_log(conn)
s.close()
