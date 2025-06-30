from board import Board

def iniciar_jogo(sock, eh_primeiro):
    tab = Board()
    tab.place_ships()
    print("[*] Tabuleiro pronto.")

    while True:
        dado = sock.recv(1024).decode().strip()

        if dado == "SEU_TURNO":
            coord = input("Ataque (ex: A5): ").strip().upper()
            sock.sendall(coord.encode())

            resposta = sock.recv(1024).decode()
            print(f"Resultado: {resposta}")
        else:
            # Considera que é um ataque do inimigo
            coord = dado
            resultado = tab.receive_attack(coord)
            sock.sendall(resultado.encode())
            print(f"Inimigo atacou {coord}: {resultado}")

