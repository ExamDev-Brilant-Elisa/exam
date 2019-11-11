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
