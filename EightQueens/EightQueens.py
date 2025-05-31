# Problema das 8 rainhas: Colocar 8 rainhas no tabuleiro de forma que uma não ataque a outra.
# Formule o problema e utilize o algoritmo de busca em profundidade. O problema pode receber o
# tabuleiro em banco ou com algumas rainhas no tabuleiro, desde que essas rainhas não estejam
# em ataque. Ao final indique quantos nós foram criados para encontrar um tabuleiro com 8 rainhas
# de forma que uma não ataque a outra e indique o tabuleiro sem ataques.


class EightQueensDFS:
    def __init__(self, initial_board=None):
        self.size = 8
        self.nodes_created = 0
        if initial_board is None:
            self.initial_board = [-1] * self.size  
        else:
            self.initial_board = initial_board.copy()
    
    def is_safe(self, board, row, col):
       
        for i in range(col):
            if board[i] == row or abs(board[i] - row) == abs(i - col):
                return False
        return True
    
    def solve(self):
       
        self.nodes_created = 0
        solution = self.dfs(self.initial_board.copy(), 0)
        return solution, self.nodes_created
    
    def dfs(self, board, col):
       
        self.nodes_created += 1
        
        if col >= self.size:
            return board
        
        if board[col] != -1:
            return self.dfs(board, col + 1)
        
        for row in range(self.size):
            if self.is_safe(board, row, col):
                board[col] = row
                result = self.dfs(board, col + 1)
                if result is not None:
                    return result
                board[col] = -1
        
        return None
    
    def print_board(self, board):
        
        for row in range(self.size):
            line = ""
            for col in range(self.size):
                if board[col] == row:
                    line += "Q "
                else:
                    line += ". "
            print(line)
        print()


def test_queens_scenarios():
    print("\n=== Tabuleiro Vazio ===")
    solver1 = EightQueensDFS()
    solution1, nodes1 = solver1.solve()
    if solution1:
        print(f"Solução encontrada em {nodes1} nós!")
        solver1.print_board(solution1)
    else:
        print("Nenhuma solução encontrada.")

    print("\n=== Tabuleiro com 1 Rainha ===")
    board2 = [-1] * 8
    board2[0] = 3  
    solver2 = EightQueensDFS(board2)
    solution2, nodes2 = solver2.solve()
    if solution2:
        print(f"Solução encontrada em {nodes2} nós!")
        solver2.print_board(solution2)
    else:
        print("Nenhuma solução encontrada.")

    print("\n=== Tabuleiro com 2 Rainhas ===")
    board3 = [-1] * 8
    board3[0] = 1  
    board3[1] = 3  
    solver3 = EightQueensDFS(board3)
    solution3, nodes3 = solver3.solve()
    if solution3:
        print(f"Solução encontrada em {nodes3} nós!")
        solver3.print_board(solution3)
    else:
        print("Nenhuma solução encontrada.")

    print("\n=== Tabuleiro com 3 Rainhas ===")
    board4 = [-1] * 8
    board3[0] = 0  
    board3[1] = 4
    board4[2] = 7  
    solver4 = EightQueensDFS(board4)
    solution4, nodes4 = solver4.solve()
    if solution4:
        print(f"Solução encontrada em {nodes4} nós!")
        solver4.print_board(solution4)
    else:
        print("Nenhuma solução encontrada.")


if __name__ == "__main__":
    test_queens_scenarios()