import socket
import time
import os
from colorama import Fore, Style
import threading

repo_name = 'FlashCode-Tournament'
path = './FlashCode-Tournament/'
file_names = []
file_contents = []
banner = "                         ______                     \n _________        .------      ------.              \n:______.- :      :  .--------------.  :             \n| ______  |      | :                : |             \n|:______B:|      | |    Client.py : | |             \n|:______B:|      | |                | |             \n|:______B:|      | |  Power found   | |             \n|         |      | |  with succes.  | |             \n|:_____:  |      | |                | |             \n|    ==   |      | :                : |             \n|       O |      :   --------------   :             \n|       o |      : ---...______...---               \n|       o |-._.-i___/              \._              \n| -.____o_|    -.    -...______...-   `-._          \n:_________:      `.____________________   `-.___.-. \n                 . .eeeeeeeeeeeeeeeeee. .      :___:\nEthanPasquier  . .eeeeeeeeeeeeeeeeeeeeee. .         \nReneMarceau   :____________________________:\n\n"
succes = "\033[1;32mSUCCES\033[1;33m"



def ft_help():
    os.system('clear')
    print(Fore.GREEN + "Bienvenue dans FlashCode !" + Style.RESET_ALL)
    print(Fore.GREEN + "\nVoici les règles du jeu :\n"+ Style.RESET_ALL)
    print(Fore.YELLOW + "1 - Vous allez coder un script dans le terminal.")
    print("2 - Toutes les 10 minutes, les scripts seront échangés entre les joueurs.")
    print("3 - Vous devrez continuer le script d'un autre joueur.")
    print("4 - Le serveur du jeu s'appelle \"flashcode.py\" et le client s'appelle \"client.py\". Notez que \"flashcode.py\" n'est pas un joueur, il héberge le jeu.")
    print("5 - N'écrivez jamais sur la fenêtre du terminal du programme lorsque celui-ci est en cours d'exécution, à moins qu'il ne vous demande explicitement d'écrire quelque chose.")
    print("6 - Le programme générera automatiquement un dossier toutes les 10 minutes dans le répertoire actuel. Vous devrez simplement entrer dans le dossier et y trouver le script d'un autre joueur." + Style.RESET_ALL)
    
    print("\nVoici quelques instructions pour vous aider à jouer :\n")
    print(Fore.CYAN + "1 - Exécutez le script \"client.py\" pour rejoindre le jeu.")
    print("2 - Attendez que tous les joueurs soient prêts pour que la partie commence.")
    print("3 - Lorsque vous recevez le script d'un autre joueur, entrez dans le dossier généré par le programme.")
    print("(Note : Si c'est la première manche, il n'y aura pas de script, vous devrez donc en créer un dans le nouveau répertoire.)")
    print("4 - Ouvrez le script avec un éditeur de texte et continuez à coder la suite.")
    print("5 - Enregistrez le script modifié.")
    print("6 - Quittez le dossier et attendez le prochain échange.")
    print("7 - Répétez les étapes précédentes jusqu'à la fin du jeu." + Style.RESET_ALL)
    
    print("\nBonne chance et amusez-vous bien dans FlashCode !")
    helps = input("\033[1;34m[Appuyez sur entrer pour continuer]\033[0m")

def send_messages(client_socket):
    while True:
        message = input()
        client_socket.send(message.encode())

def ft_sync(message):
    file_index = message.find("FILE:")
    if file_index != -1:
        file_index += len("FILE:")
        end_index = message.find("\n", file_index)
        if end_index != -1:
            file_name = message[file_index:end_index].strip()
            rest = message[end_index+1:]
        else:
            file_name = message[file_index:].strip()
            rest = ""
    else:
        file_name = ""
        rest = message
    print("reçu "+file_name)
    os.system("touch "+file_name)
    with open(file_name, 'w') as file:
        file.write(rest)
    

def start(client_socket):
    os.system("clear")
    print("\033[1;34m --- Commencement de la Manche !!! ---\033[0m\n")
    print("\033[1;32m[Vous avez 10 minutes pour coder votre programme dans le dossier \033[1;34m"+repo_name+"\033[1;32m]\033[0m")
    start_time = time.monotonic()
    end_time = start_time + 30
    while time.monotonic() < end_time:
        remaining_time = end_time - time.monotonic()
        print(f"\033[1;31mTemps restant : {int(remaining_time/30)} minutes")
        time.sleep(5)
    os.system("clear")
    print("\033[1;31mRecuperation des fichiers ...")
    files_and_folders = os.listdir(path)
    for select_file in files_and_folders:
        path_file = path+select_file
        if os.path.isfile(path_file):
            file_names.append(path_file)
            with open(path_file, 'r') as f:
                contents = f.read()
                file_contents.append(contents)
    
    os.system("rm -rf "+repo_name)
    index = 0
    os.system("mkdir "+repo_name)
    os.system("clear")
    print("\033[1;34mNouveau dossier ["+repo_name+"] en creation. ["+succes+"]")
    time.sleep(2)
    os.system("clear")
    print("\033[1;34mEnvoie des fichiers ...")
    for filename in file_names:
        filename = "FILE:"+filename+"\n"+file_contents[index]
        client_socket.send(filename.encode())
        index += 1
    
    

def receive_messages(client_socket):
    while True:
        message = client_socket.recv(1024).decode()
        text = str(message)
        if (text.startswith("fgt48rgtg8trg54484tg78grtg879g4th87hrth4tr78trhh78trh4rh785rh7rt8rh75678rthr")):
            os.system("mkdir "+repo_name)
            start(client_socket)
        if (text.startswith("FILE:")):
            ft_sync(text)
        if (text.startswith("szad4zede78rr5tgtyj7yui4urfer7z4dax4e78rcerthj7y4t4t41rr15qx6568zrg")):
            os.system("clear")
            print("La partie est fini ;)")
            print("Merci d'avoir jouer a FlashCode")
            client_socket.close()
            exit()


if __name__ == '__main__':
    print("\033[1;32m"+banner+"\033[0m")
    helps = input("\033[1;34m[Appuyez sur entrer pour continuer ou faite 'h' pour help] : \033[0m")
    if (helps == "h"):
        ft_help()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    os.system('clear')
    print("\033[1;34m --- Connected to chat server ["+succes+"\033[1;34m]---\n\033[0m\n")
    print("\033[1;34mQuand tout les joueurs seront present , la partie commencera ...\n\033[0m\n")
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()
    send_thread = threading.Thread(target=send_messages, args=(client_socket,))
    send_thread.start()