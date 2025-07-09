import os

class Board:
    def __init__(self, hidden=False):
        self.size = 10
        self.grid = [['~'] * self.size for _ in range(self.size)]
        self.hidden = hidden  # se True, oculta navios ao imprimir

    def __str__(self):
        cabeçalho = "   " + " ".join(str(i) for i in range(self.size)) + "\n"
        linhas = ""
        for i, row in enumerate(self.grid):
            linha = chr(ord('A') + i) + "  "
            for cell in row:
                if self.hidden and cell == 'N':
                    linha += "~ "
                else:
                    linha += cell + " "
            linhas += linha + "\n"
        return cabeçalho + linhas

    def can_place(self, length, row, col, orient):
        """Verifica se navio de dado tamanho cabe e não sobrepõe outros."""
        dr, dc = (0, 1) if orient == 'H' else (1, 0)
        for i in range(length):
            r, c = row + dr * i, col + dc * i
            if not (0 <= r < self.size and 0 <= c < self.size):
                return False
            if self.grid[r][c] == 'N':
                return False
        return True

    def place_ship(self, length, row, col, orient):
        """Posiciona o navio assumindo que can_place já retornou True."""
        dr, dc = (0, 1) if orient == 'H' else (1, 0)
        for i in range(length):
            self.grid[row + dr * i][col + dc * i] = 'N'

    def place_ships_interactive(self, ship_sizes):
        print("[*] Posicione os navios no tabuleiro:")
        print(self)
        for size in ship_sizes:
            while True:
                inp = input(f"Navio de tamanho {size} (ex: H B2): ").strip().upper().split()
                if len(inp) != 2 or inp[0] not in ('H', 'V'):
                    print("  → Formato inválido. Digite: <H/V> <Coord>, ex: H B2")
                    continue
                orient, coord = inp
                if len(coord) < 2 or not coord[0].isalpha() or not coord[1:].isdigit():
                    print("  → Coordenada inválida. Use letra A–J e número 0–9, ex: B2")
                    continue
                row = ord(coord[0]) - ord('A')
                col = int(coord[1:])
                if not (0 <= row < self.size and 0 <= col < self.size):
                    print("  → Fora do tabuleiro.")
                    continue
                if not self.can_place(size, row, col, orient):
                    print("  → Não cabe ou sobrepõe outro navio.")
                    continue
                # tudo ok: coloca
                self.place_ship(size, row, col, orient)
                print(self)
                break

    def receive_attack(self, coord):
        try:
            row = ord(coord[0]) - ord('A')
            col = int(coord[1:])
            if not (0 <= row < self.size and 0 <= col < self.size):
                return "Fora do tabuleiro!"
            cell = self.grid[row][col]
            if cell == 'N':
                self.grid[row][col] = 'X'
                return "Acertou!"
            if cell == '~':
                self.grid[row][col] = 'O'
                return "Água!"
            return "Já atirou aqui!"
        except:
            return "Erro de coordenada!"
    
    def todos_navios_afundados(self):
        for linha in self.grid:
            if 'N' in linha:
                return False
        return True
