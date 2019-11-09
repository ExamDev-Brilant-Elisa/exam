import socket as modsocket

def connexion():
    s = modsocket.socket(modsocket.AF_INET, modsocket.SOCK_STREAM)

    s.connect(("localhost", 5000))

    s.sendall(b"Hello, world")
    data = s.recv(1024)
    s.close()
    print ("Received", repr(data))

connexion()