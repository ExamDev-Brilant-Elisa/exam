import socket as modsocket
import datetime

def ddos():

    if (datetime.date == 2019, 11, 7) and (datetime.time == 11, 59):
        print("potentielle attaque ddos".encode("utf-8"))
    else:
        print("error".encode("utf-8"))

s = modsocket.socket(modsocket.AF_INET, modsocket.SOCK_STREAM)
server_addr = ("192.168.56.1", 60000)
slave = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

slave.connect(server_addr)

attaque = (slave.recv(1024))
if attaque == "attc":
    ddos()
    slave.send("le slave a lancé le ddos".encode("utf-8"))
else:
    slave.send("euh problème".encode("utf-8"))

slave.close()
