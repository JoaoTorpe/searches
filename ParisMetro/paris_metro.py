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
    
    
   
    
    return path, lines, total_time

def a_star(start: Station, end: Station) -> Tuple[List[Station], List[str], float]:
    
    open_set = []
    closed_set = set()
    best_nodes = {}
    
   
    initial_h = heuristic(start, end)
    initial_line = get_lines(start)[0] if get_lines(start) else None
    initial_node = Node(start, 0, initial_h, None, initial_line)
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
            
          
            new_line = get_common_line(current_node.station, neighbor_station, current_node.current_line)
            line_change_penalty = 0

            if new_line is None:
                possible_lines = get_lines(neighbor_station)
                if possible_lines:
                    new_line = possible_lines[0]
                    line_change_penalty = 5  
                else:
                    new_line = None
            elif new_line != current_node.current_line:
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


def test_all_combinations():
    """Testa todas combinações com tratamento robusto de encoding"""
    all_stations = list(Station)
    total = len(all_stations) * (len(all_stations) - 1)
    tested = 0
    errors = 0
    
    print("\n Testando todas combinações (arquivo 'resultados_metro.log')...")
    
    try:
        with open("resultados_metro.log", "w", encoding="utf-8") as log_file:
            log_file.write("RELATÓRIO DE TESTES - METRÔ PARIS\n")
            log_file.write("="*50 + "\n\n")
            
            for start in all_stations:
                for end in all_stations:
                    if start == end:
                        continue
                    
                    tested += 1
                    print(f"Progresso: {tested}/{total} | Erros: {errors}", end="\r")
                    
                    try:
                        path, lines, time = a_star(start, end)
                        
                     
                        log_file.write(f"[OK] {start.name} -> {end.name} ({time:.1f} min)\n")
                        log_file.write(" -> ".join(f"{s.name}({l})" for s,l in zip(path,lines)) + "\n")
                        
                      
                        has_error = False
                        for i, station in enumerate(path):
                            if i < len(lines) and station not in LINES.get(lines[i], set()):
                                has_error = True
                                break
                        
                        if has_error:
                            errors += 1
                            log_file.write("[ERRO] Atribuição incorreta de linhas:\n")
                            for i, station in enumerate(path):
                                line = lines[i] if i < len(lines) else "?"
                                valid = "(OK)" if station in LINES.get(line, set()) else f"(ERRO: válidas {get_lines(station)})"
                                log_file.write(f"  {station.name}: {line} {valid}\n")
                    
                    except ValueError as e:
                        errors += 1
                        log_file.write(f"[FALHA] {start.name} -> {end.name}: {str(e)}\n")
    
    except Exception as e:
        print(f"\n Erro ao escrever arquivo: {str(e)}")
        return


    print(f"\nTeste concluído!")
    print(f"Total testado: {tested}")
    print(f"Rotas com problemas: {errors}")
    print(f"Arquivo completo: resultados_metro.log")
    
    if errors > 0:
        print("\nDica: Use um editor como Notepad++ ou VS Code para ver o arquivo .log")

def print_path(path: List[Station], lines: List[str], total_time: float):
    
    print("\nCaminho encontrado:")
    for i, station in enumerate(path):
        line_info = ""
        if i < len(lines):
            line_info = f" (Linha: {lines[i]})"
        print(f"{station.name}{line_info}")
    
    print(f"\nTempo total da viagem: {total_time:.1f} minutos")


if __name__ == "__main__":
   
   test_all_combinations()