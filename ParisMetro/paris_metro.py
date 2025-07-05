from station import *

class Node:
    __slots__ = ['station', 'g_cost', 'h_cost', 'parent', 'current_line', 'line_changes']
    
    def __init__(self, station: Station, g_cost: float, h_cost: float, parent: 'Node' = None, 
                 current_line: str = None, line_changes: int = 0):
        self.station = station
        self.g_cost = g_cost  
        self.h_cost = h_cost 
        self.parent = parent
        self.current_line = current_line
        self.line_changes = line_changes
    
    @property
    def f_cost(self) -> float:
        return self.g_cost + self.h_cost
    
    def __lt__(self, other: 'Node') -> bool:
        return self.f_cost < other.f_cost

def heuristic(a: Station, b: Station) -> float:
    
    return DISTANCES[a.value - 1][b.value - 1]

def get_neighbors(station: Station) -> List[Tuple[Station, int]]:
    
    neighbors = []
    for conn in REAL_CONNECTIONS:
        if conn[0] == station:
            neighbors.append((conn[1], conn[2]))
        elif conn[1] == station:
            neighbors.append((conn[0], conn[2]))
    return neighbors

def reconstruct_path(node: Node) -> Tuple[List[Station], List[str], int]:
   
    path = []
    lines = []
    current = node
    total_time = current.g_cost  
    
    while current is not None:
        path.append(current.station)
        if current.current_line:
            lines.append(current.current_line)
        current = current.parent
    
    path.reverse()
    lines.reverse()
    
    
    simplified_lines = []
    for line in lines:
        if not simplified_lines or line != simplified_lines[-1]:
            simplified_lines.append(line)
    
    return path, simplified_lines, total_time

def a_star(start: Station, end: Station) -> Tuple[List[Station], List[str], float]:
    
    open_set = []
    closed_set = set()
    
 
    best_nodes = {}
    
   
    initial_h = heuristic(start, end)
    initial_node = Node(start, 0, initial_h, None, get_line(start))
    heapq.heappush(open_set, initial_node)
    best_nodes[start] = initial_node
    
    while open_set:
        current_node = heapq.heappop(open_set)
        
   
        if current_node.station == end:
            return reconstruct_path(current_node)
        
        closed_set.add(current_node.station)
        
        for neighbor_station, distance in get_neighbors(current_node.station):
            if neighbor_station in closed_set:
                continue
            
           
            speed_kmh = 30 
            speed_km_min = speed_kmh / 60 
            time_minutes = distance / speed_km_min
            
          
            new_line = get_common_line(current_node.station, neighbor_station,current_node.current_line)
            line_change_penalty = 0
            if new_line is None:
                
                new_line = get_line(neighbor_station)
                line_change_penalty = 5  
            
            new_line_changes = current_node.line_changes + (1 if line_change_penalty > 0 else 0)
            
           
            new_g_cost = current_node.g_cost + time_minutes + line_change_penalty
            new_h_cost = heuristic(neighbor_station, end) / speed_km_min  
            new_node = Node(
                neighbor_station, 
                new_g_cost, 
                new_h_cost, 
                current_node, 
                new_line,
                new_line_changes
            )
            
            
            if neighbor_station in best_nodes:
                existing_node = best_nodes[neighbor_station]
                if new_node.g_cost < existing_node.g_cost:
                    best_nodes[neighbor_station] = new_node
                    heapq.heappush(open_set, new_node)
            else:
                best_nodes[neighbor_station] = new_node
                heapq.heappush(open_set, new_node)
    
    raise ValueError(f"Não foi possível encontrar um caminho de {start} para {end}")

def print_path(path: List[Station], lines: List[str], total_time: float):
    
    print("\nCaminho encontrado:")
    for i, station in enumerate(path):
        line_info = ""
        if i < len(lines):
            line_info = f" (Linha: {lines[i]})"
        print(f"{station.name}{line_info}")
    
    print(f"\nTempo total da viagem: {total_time:.1f} minutos")
    print(f"Número de mudanças de linha: {len(lines)-1}")

def main():
    print("Sistema de Navegação do Metrô de Paris")
    print("Estações disponíveis: E1, E2, E3, E4, E5, E6, E7, E8, E9, E10, E11, E12, E13, E14")
    
    while True:
        try:
            start = Station.from_str(input("\nDigite a estação de origem (ex: E1): "))
            end = Station.from_str(input("Digite a estação de destino (ex: E14): "))
            
            if start == end:
                print("Origem e destino são iguais. Não é necessária viagem.")
                continue
                
            path, lines, total_time = a_star(start, end)
            print_path(path, lines, total_time)
            
        except ValueError as e:
            print(f"Erro: {e}")
        
        again = input("\nDeseja consultar outra rota? (s/n): ").lower()
        if again != 's':
            break

if __name__ == "__main__":
    main()