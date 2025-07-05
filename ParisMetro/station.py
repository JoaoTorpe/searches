from enum import Enum
import heapq
from typing import List, Dict, Tuple, Optional

class Station(Enum):
    E1 = 1
    E2 = 2
    E3 = 3
    E4 = 4
    E5 = 5
    E6 = 6
    E7 = 7
    E8 = 8
    E9 = 9
    E10 = 10
    E11 = 11
    E12 = 12
    E13 = 13
    E14 = 14

    @classmethod
    def from_str(cls, s: str) -> 'Station':
        try:
            return cls[s.upper()]
        except KeyError:
            raise ValueError(f"Estação inválida: {s}")

DISTANCES = [
    [0, 11, 20, 27, 40, 43, 39, 28, 18, 10, 18, 30, 30, 32],  # E1
    [11, 0, 9, 16, 29, 32, 28, 19, 11, 4, 17, 23, 21, 24],    # E2
    [20, 9, 0, 7, 20, 22, 19, 15, 10, 11, 21, 21, 13, 18],    # E3
    [27, 16, 7, 0, 13, 16, 12, 13, 13, 18, 26, 21, 11, 17],   # E4
    [40, 29, 20, 13, 0, 3, 2, 21, 25, 31, 38, 27, 16, 20],    # E5
    [43, 32, 22, 16, 3, 0, 4, 23, 28, 33, 41, 30, 17, 20],    # E6
    [39, 28, 19, 12, 2, 4, 0, 22, 25, 29, 38, 28, 13, 17],    #E7
    [28, 19, 15, 13, 21, 23, 22, 0, 9, 22, 18, 7, 25, 30],    # E8
    [18, 11, 10, 13, 25, 28, 25, 9, 0, 13, 12, 12, 23, 28],   # E9
    [10, 4, 11, 18, 31, 33, 29, 22, 13, 0, 20, 27, 20, 23],   #E10
    [18, 17, 21, 26, 38, 41, 38, 18, 12, 20, 0, 15, 35, 39],  # E11
    [30, 23, 21, 21, 27, 30, 28, 7, 12, 27, 15, 0, 31, 37],   # E12
    [30, 21, 13, 11, 16, 17, 13, 25, 23, 20, 35, 31, 0, 5],   # E13
    [32, 24, 18, 17, 20, 20, 17, 30, 28, 23, 39, 37, 5, 0]    #  E14
]

LINES = {
    'Linha 1': {Station.E1, Station.E2, Station.E3, Station.E4, Station.E5, Station.E6},
    'Linha 2': {Station.E10, Station.E2, Station.E9, Station.E8, Station.E5,Station.E7},
    'Linha 3': {Station.E11, Station.E9, Station.E3, Station.E13},
    'Linha 4': {Station.E12, Station.E8, Station.E4,Station.E13, Station.E14},
}

REAL_CONNECTIONS = [
    (Station.E1, Station.E2, 11),
    (Station.E2, Station.E3, 9),
    (Station.E2, Station.E9, 11),
    (Station.E2, Station.E10, 4),
    (Station.E3, Station.E4, 7),
    (Station.E3, Station.E9, 10),
    (Station.E3, Station.E13, 19),  
    (Station.E4, Station.E5, 14),
    (Station.E4, Station.E8, 16),
    (Station.E4, Station.E13, 12),
    (Station.E5, Station.E6, 3),
    (Station.E5, Station.E7, 2),
    (Station.E5, Station.E8, 33),
    (Station.E8, Station.E9, 10),
    (Station.E8, Station.E12, 7),
    (Station.E9, Station.E11, 14),
    (Station.E13, Station.E14, 5)
]

def get_line(station: Station) -> str:
   
    for line, stations in LINES.items():
        if station in stations:
            return line
    return "Desconhecida"

def get_common_line(station1: Station, station2: Station,current_line_str: str) -> Optional[str]:

    if current_line_str:
        current_line_stations = LINES.get(current_line_str, set())
        if station1 in current_line_stations and station2 in current_line_stations:
            return current_line_str
    
    for line, stations in LINES.items():
        if station1 in stations and station2 in stations:
            return line
    return None
