def ddos():
    year = str(input("Année du lancement du DDOS [2019-2021] : "))
    month = str(input("Mois du lancement du DDOS [1-12]: "))
    day = str(input("Jour du lancement du DDOS [1-31]: "))
    hour = str(input("Heure du lancement du DDOS [1-24]: "))
    minutes = str(input("Minutes du lancement du DDOS [0-60]: "))
    datetime = year+"-"+month+"-"+day+" "+hour+":"+minutes
    ip = str(input("Entrez l'IP que vous souhaitez attaquer : "))
    #on a plus qu'à send l'ip et le datetime


