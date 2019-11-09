import socket

master = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
master.bind(("192.168.56.1", 60000))

master.listen()
slave, addr = master.accept()

print("Connection accepted for : ", addr)

slave.send("attc".encode("utf-8"))

print(slave.recv(1024).decode("utf-8"))

master.close()



