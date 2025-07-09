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
    vez = 0  # 0: conn1 joga, 1: conn2 joga

    try:
        while True:
            atacante = conns[vez]
            defensor = conns[1 - vez]

            atacante.sendall("SEU_TURNO".encode())
            ataque = atacante.recv(1024)
            if not ataque:
                break

            defensor.sendall(ataque)
            resposta = defensor.recv(1024)
            if not resposta:
                break

            atacante.sendall(resposta)

            if resposta.decode() == "VITORIA":
                defensor.sendall("DERROTA".encode())
                break

            vez = 1 - vez  # troca o turno
    except Exception as e:
        print(f"[!] Erro: {e}")
    finally:
        conn1.close()
        conn2.close()
        print("[*] Conexões encerradas.")


HOST = '0.0.0.0'
PORT = int(SERVER_PORT) 
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"[*] Servidor ouvindo na porta {PORT}")
    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_cliente, args=(conn, addr)).start()