#master, programme du hackeur, que j'ai assimilé comme étant un serveur. il sait recevoir et envoyer des messages au slave
import socket as modsocket

server_addr = ("192.168.56.1", 60000)


master = modsocket.socket(modsocket.AF_INET, modsocket.SOCK_STREAM)
master.bind((server_addr))
print("le maître est démarré...")

master.listen()
print("en écoute...")

slave, addr = master.accept()
print("Connection accepted for : ", addr)

slave.send(b"attc")
print(slave.recv(1024))

master.close()







