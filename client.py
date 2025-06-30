import socket
from dotenv import load_dotenv
import os

load_dotenv()

SERVER_IP = os.getenv("SERVER_IP")
SERVER_PORT = os.getenv("SERVER_PORT")

from game import iniciar_jogo

HOST = SERVER_IP
PORT = int(SERVER_PORT) 
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    acao = input("1 - Criar sala\n2 - Entrar em sala\n> ")

    if acao == "1":
        s.sendall("CRIAR".encode())
        resp = s.recv(1024).decode()
        codigo = resp.split(":")[1]
        print(f"[+] Sala criada. Código: {codigo}")
        print("[*] 2r...")
        eh_primeiro = True
    else:
        codigo = input("Código da sala: ")
        s.sendall(f"ENTRAR:{codigo}".encode())
        resp = s.recv(1024).decode()
        if resp == "ENTROU":
            print("[+] Conectado com outro jogador.")
            eh_primeiro = False
        else:
            print("[!] Sala inválida ou cheia.")

    iniciar_jogo(s, eh_primeiro)
