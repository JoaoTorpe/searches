from collections import deque

# 1. Problema 9-puzzle: Colocar o quadro branco na primeira posição e os 8 seguintes de forma
# ordenada. Formule o problema, ou utilize a formulação vista em sala de aula para dado uma
# configuração inicial do tabuleiro exibir a sequência de passos que devem ser realizados para
# resolver o puzzle e a quantidade total de passos. Utilize a busca em largura com poda de estados
# já avaliados.


from collections import deque

class Puzzle:
    def __init__(self, initial_state):
        self.initial_state = initial_state
        self.goal_state = [0, 1, 2, 3, 4, 5, 6, 7, 8]  
        self.visited_states = set()
        self.size = 3  # A dimensao do tabuleiro é 3x3
        self.moves =  [(-1, 0), (1, 0), (0, -1), (0, 1)] # Movimentos possiveis

    def is_goal(self, state):
        return state == self.goal_state

    def get_empty_position(self, state):
       
        return state.index(0)

    def get_neighbors(self, state):
        neighbors = []
        empty_pos = self.get_empty_position(state)
        row, col = divmod(empty_pos,3)

        for dr, dc in self.moves:
            new_row, new_col = row + dr, col + dc
            
            if 0 <= new_row < self.size and 0 <= new_col < self.size:
                new_pos = new_row * self.size + new_col
                
                new_state = state.copy()
                new_state[empty_pos], new_state[new_pos] = new_state[new_pos], new_state[empty_pos]
                neighbors.append(new_state)

        return neighbors

    def solve(self):
       
        queue = deque([(self.initial_state, [])])
        
        self.visited_states.add(tuple(self.initial_state))

        while queue:
            current_state, path = queue.popleft()

            if self.is_goal(current_state):
                return path, len(path)

            for neighbor in self.get_neighbors(current_state):
                neighbor_tuple = tuple(neighbor)
                if neighbor_tuple not in self.visited_states:
                    self.visited_states.add(neighbor_tuple)
                    queue.append((neighbor, path + [neighbor]))

        return None, 0  

    def print_solution(self, solution_path):
        """Exibe a solução passo a passo"""
        if not solution_path:
            print("Não foi encontrada solução")
            return

        print("Estado Inicial:")
        print(self.initial_state)
        print("\nPassos para a solução:")

        for step, state in enumerate(solution_path, 1):
            print(f"\nPasso {step}:")
            print(state)

        print(f"\nTotal de passos: {len(solution_path)}")

    

if __name__ == "__main__":
  
    initial_state_1 = [4, 6, 2, 8, 1, 3, 7, 5, 0] # Esse nao tem solução U_U
    initial_state_2 = [6, 4, 2, 8, 1, 3, 7, 5, 0]
    initial_state_3 = [1, 2, 3, 4, 5, 0, 6, 7, 8]
    initial_state_4 = [8, 7, 6, 5, 4, 3, 2, 1, 0]

    puzzle = Puzzle(initial_state_1)
    solution_path, steps = puzzle.solve()
    puzzle.print_solution(solution_path)