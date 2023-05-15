import datetime
import time
import requests
import json
import os
import subprocess
import socket
import os
import threading

nb_joueur = 0
url_self = ""
joueurs = []
ip_server = ""
url_joueurs = []
self = -1
nb_manche = 10
repo_name = 'FlashCode-Tournament'

banner = """   _____________________
  /                 `   \\
  |  .-----------.  |   |-----.
  |  |           |  |   |-=---|
  |  | Flashcode |  |   |-----|
  |  |           |  |   |-----|
  |  |  Server   |  |   |-----|
  |  `-----------'  |   |-----'/\\
   \________________/___'     /  \\
      /                      / / /
     / //               //  / / /
    /                      / / /
   / _/_/_/_/_/_/_/_/_/_/ /   /
  / _/_/_/_/_/_/_/_/_/_/ /   /
 / _/_/_/_______/_/_/_/ / __/
/______________________/ /    
\______________________\/ EthanPasquier\n                          ReneMarceau\n\n"""

def ft_help():
    os.system('clear')
    print("\033[1;32mBienvenue dans FlashCode !\033[0m")
    print("\033[1;34m\nVoici les règles du jeu :\n\033[0m")
    print("1 - Vous allez coder un script dans le terminal.")
    print("2 - Toutes les 10 minutes, les scripts seront échangés entre les joueurs.")
    print("3 - Vous devrez continuer le script d'un autre joueur.")
    print("4 - Le serveur du jeu s'appelle \"flashcode.py\" et le client s'appelle \"client.py\". Notez que \"flashcode.py\" n'est pas un joueur, il héberge le jeu.")
    print("5 - N'écrivez jamais sur la fenêtre du terminal du programme lorsque celui-ci est en cours d'exécution, à moins qu'il ne vous demande explicitement d'écrire quelque chose.")
    print("6 - Le programme générera automatiquement un dossier toutes les 10 minutes dans le répertoire actuel. Vous devrez simplement entrer dans le dossier et y trouver le script d'un autre joueur.\033[0m")
    
    print("\nVoici quelques instructions pour vous aider à jouer :\n")
    print("\033[1;32m1 - Exécutez le script \"client.py\" pour rejoindre le jeu.")
    print("2 - Attendez que tous les joueurs soient prêts pour que la partie commence.")
    print("3 - Lorsque vous recevez le script d'un autre joueur, entrez dans le dossier généré par le programme.")
    print("(Note : Si c'est la première manche, il n'y aura pas de script, vous devrez donc en créer un dans le nouveau répertoire.)")
    print("4 - Ouvrez le script avec un éditeur de texte et continuez à coder la suite.")
    print("5 - Enregistrez le script modifié.")
    print("6 - Quittez le dossier et attendez le prochain échange.")
    print("7 - Répétez les étapes précédentes jusqu'à la fin du jeu.\033[0m")
    
    print("\nBonne chance et amusez-vous bien dans FlashCode !")
    helps = input("\033[1;34m[Appuyez sur entrer pour continuer]\033[0m")

def get_local_ip():
    """
    Retourne l'adresse IP locale du système.
    """
    # Crée une socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # Tente de se connecter à une adresse IP de référence, dans ce cas-ci, Google Public DNS
        sock.connect(("8.8.8.8", 80))

        # Récupère l'adresse IP locale associée à la socket
        local_ip = sock.getsockname()[0]

        return local_ip
    except socket.error:
        print("Impossible de récupérer l'adresse IP locale.")
    finally:
        # Ferme la socket
        sock.close()

class ChatServer:
    def game(self):
        print("\033[1;32mLa partie va commencer")
    def __init__(self):
        self.clients = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        ip = get_local_ip()
        self.server_socket.bind((ip, 12345))
        local_ip = self.server_socket.getsockname()[0]
        print("Adresse IP locale :", ip)
        self.server_socket.listen()

    def broadcast(self, message):
        for client in self.clients:
            client.send(message.encode())

    def handle_client(self, client_socket, client_address,isvalid):
        print(f"\033[1;32mNew connection from \033[1;31m{client_address}\033[1;30m")
        self.clients.append(client_socket)
        i = len(self.clients) # Index of the current client
        if(i == nb_joueur):
            self.game()
            for manche in range(0, nb_manche):
                self.broadcast("fgt48rgtg8trg54484tg78grtg879g4th87hrth4tr78trhh78trh4rh785rh7rt8rh75678rthr")
                print("\033[1;32mManche "+str(manche+1)+"\033[1;30m")
                time.sleep(605)
            self.broadcast("szad4zede78rr5tgtyj7yui4urfer7z4dax4e78rcerthj7y4t4t41rr15qx6568zrg")
        while True:
            try:
                message = client_socket.recv(1024).decode()
                if message:
                    text = str(message)
                    print(f"\033[1;30m Player["+str(i)+f"] commit : {message}\n")
                    next_index = (i + 1) % len(self.clients)  # Get the index of the next client
                    next_client = self.clients[next_index]
                    next_client.send(message.encode())  # Send the message to the next client
                else:
                    raise Exception("Disconnected")
            except:
                self.clients.remove(client_socket)
                print(f"Connection closed from {client_address}")
                client_socket.close()
                break

    def start(self):
        isvalid = 0
        print("\033[1;34mLe serveur est en attente de connexion")
        while True:
            client_socket, client_address = self.server_socket.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address , isvalid))
            client_thread.start()


print("\033[1;32m"+banner)
helps = input("\033[1;34m[Appuyez sur entrer pour continuer ou faite 'h' pour help] : \033[0m")


if (helps == "h"):
    ft_help()
    os.system('clear')
    print("\033[1;32m"+banner)
    print("\033[1;34m[Appuyez sur entrer pour continuer ou faite 'h' pour help] : \033[0mh")
nb_joueur = int(input("\033[1;34mEntrez le nombre de joueur [min 3]: \033[1;31m"))
if nb_joueur < 3:
    print("\033[1;31mLe nombre de joueur doit être supérieur ou égale à 2")
    exit()
nb_manche = int(input("\033[1;34mEntrez le nombre de manche [min 1]: \033[1;31m"))
if nb_manche < 1:
    print("\033[1;31mLe nombre de manche doit être supérieur ou égale à 1")
    exit()

server = ChatServer()
server.start()