# game.py
def iniciar_jogo(sock, eh_primeiro):
    # ... código anterior ...
    meu_tab       = Board(hidden=False)
    tab_oponente  = Board(hidden=True)

    # posicionar navios
    meu_tab.place_ships_interactive(ship_sizes)

    while True:
        dado = sock.recv(1024).decode().strip()
        if not dado:
            print("Conexão encerrada.")
            break

        if dado == "SEU_TURNO":
            # mostrar tabuleiro do oponente
            print(tab_oponente)
            coord = input("Seu ataque (ex: A5): ").strip().upper()
            sock.sendall(coord.encode())

            resposta = sock.recv(1024).decode()
            print(f"Resultado do ataque: {resposta}")

            # atualizar tabuleiro do oponente
            row = ord(coord[0]) - ord('A')
            col = int(coord[1:])
            if resposta == "Acertou!":
                tab_oponente.grid[row][col] = 'X'
            elif resposta == "Água!":
                tab_oponente.grid[row][col] = 'O'
            elif resposta == "VITORIA":
                tab_oponente.grid[row][col] = 'X'
                print("✅ Você venceu o jogo!")
                break
        elif dado == "DERROTA":
            print("❌ Você perdeu o jogo.")
            break
        else:
            # ataque do oponente
            coord = dado
            resultado = meu_tab.receive_attack(coord)

            if meu_tab.todos_navios_afundados():
                sock.sendall("VITORIA".encode())  # sinaliza que venceu
                print(f"Inimigo atacou {coord}: {resultado}")
                print("❌ Todos os seus navios foram destruídos. Você perdeu.")
                break
            else:
                sock.sendall(resultado.encode())
                print(f"Inimigo atacou {coord}: {resultado}")
