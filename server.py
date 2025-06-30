import socket
import threading
import uuid
from dotenv import load_dotenv
import os

load_dotenv()

SERVER_PORT = os.getenv("SERVER_PORT")

salas = {}  

def handle_cliente(conn, addr):
    print(f"[+] Conexão de {addr}")
    try:
        op = conn.recv(1024).decode()

        if op == "CRIAR":
            codigo = str(uuid.uuid4())[:8]
            salas[codigo] = [conn]
            conn.sendall(f"SALA:{codigo}".encode())
            print(f"[*] Sala criada: {codigo}")
        elif op.startswith("ENTRAR:"):
            codigo = op.split(":")[1]
            if codigo in salas and len(salas[codigo]) == 1:
                salas[codigo].append(conn)
                conn.sendall("ENTROU".encode())
                print(f"[+] Sala {codigo} pronta para jogar")
                threading.Thread(target=iniciar_jogo, args=(salas[codigo],)).start()
            else:
                conn.sendall("INVALIDO".encode())
    except Exception as e:
        print(f"[!] Erro: {e}")

def iniciar_jogo(conns):
    conn1, conn2 = conns
    addr1 = conn1.getpeername()
    addr2 = conn2.getpeername()
    print(f"[*] Iniciando jogo entre {addr1} e {addr2}")

    vez = 0  # 0: conn1 ataca, 1: conn2 ataca

    try:
        while True:
            atacante = conns[vez]
            defensor = conns[1 - vez]
            addr_atacante = atacante.getpeername()
            addr_defensor = defensor.getpeername()

            atacante.sendall("SEU_TURNO".encode())
            print(f"[>] Esperando ataque de {addr_atacante}")
            ataque = atacante.recv(1024)
            if not ataque:
                print("[!] Conexão encerrada pelo atacante.")
                break
            print(f"[{addr_atacante} → {addr_defensor}] {ataque.decode()}")

            defensor.sendall(ataque)

            print(f"[<] Esperando resposta de {addr_defensor}")
            resposta = defensor.recv(1024)
            if not resposta:
                print("[!] Conexão encerrada pelo defensor.")
                break
            print(f"[{addr_defensor} → {addr_atacante}] {resposta.decode()}")

            atacante.sendall(resposta)

            vez = 1 - vez  # alterna o turno
    except Exception as e:
        print(f"[!] Erro durante o jogo: {e}")
    finally:
        conn1.close()
        conn2.close()
        print("[*] Jogo encerrado.")

HOST = '0.0.0.0'
PORT = int(SERVER_PORT) 
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"[*] Servidor ouvindo na porta {PORT}")
    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_cliente, args=(conn, addr)).start()