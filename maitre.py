# lis d'abord le bot.py
# içi le serveur reçois  normalement le message 'Hello World'
# je pense que sa t'aidera avec ton code pour la date

import socket as modsocket

def ecoute():
    #ligne de code de base pour une communication serveur-client
    s = modsocket.socket(modsocket.AF_INET, modsocket.SOCK_STREAM)
    s.bind(("localhost", 5000))
    print("Le maitre est démarré...")


    s.listen()
    print("En écoute...")
    conn, addr = s.accept()

    while 1:
        #ces içi que le maitre reçois le message en provenance du bot
        data = conn.recv(1024)
        print(data)
        #si il y a aucun message envoyé le maitre s'arrête
        if not data:
            break
        #reenvoie ce que le maitre a reçus au bot
        conn.sendall(data)

    conn.close()
    s.close()

ecoute()
