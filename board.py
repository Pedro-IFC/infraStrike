class Board:
    def __init__(self, hidden=False):
        self.grid = [['~'] * 10 for _ in range(10)]
        self.hidden = hidden  # se True, oculta os navios ('N') ao imprimir

    def place_ships(self):
        # Navio horizontal de 3 posições em B2, B3, B4
        self.grid[1][1] = 'N'
        self.grid[1][2] = 'N'
        self.grid[1][3] = 'N'

        # Navio vertical de 2 posições em E5, F5
        self.grid[4][4] = 'N'
        self.grid[5][4] = 'N'

    def receive_attack(self, coord):
        try:
            row = ord(coord[0]) - ord('A')
            col = int(coord[1])

            if not (0 <= row < 10 and 0 <= col < 10):
                return "Fora do tabuleiro!"

            if self.grid[row][col] == 'N':
                self.grid[row][col] = 'X'
                return "Acertou!"
            elif self.grid[row][col] == '~':
                self.grid[row][col] = 'O'
                return "Água!"
            elif self.grid[row][col] in ['X', 'O']:
                return "Já atirou aqui!"
            else:
                return "Coordenada inválida!"
        except:
            return "Erro de coordenada!"

    def __str__(self):
        out = "  " + " ".join(str(i) for i in range(10)) + "\n"
        for i, row in enumerate(self.grid):
            linha = chr(ord('A') + i) + " "
            for cell in row:
                if self.hidden and cell == 'N':
                    linha += "~ "
                else:
                    linha += cell + " "
            out += linha + "\n"
        return out
