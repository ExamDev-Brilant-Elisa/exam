import socket as modsocket

def ecoute():

    s = modsocket.socket(modsocket.AF_INET, modsocket.SOCK_STREAM)
    s.bind(("localhost", 5000))
    print("Le maitre est démarré...")


    s.listen()
    print("En écoute...")
    conn, addr = s.accept()

    while 1:
        data = conn.recv(1024)
        print(data)
        if not data:
            break
        conn.sendall(data)

    conn.close()
    s.close()

ecoute()