import networkx as nx
import math
import re
import os

# === Coordinate geografiche ===
coord = {
    "doha": (25.3, 51.5), "londra": (51.5, -0.1), "berlino": (52.5, 13.4),
    "tokyo": (35.7, 139.7), "seoul": (37.6, 126.9), "atene": (37.9, 23.7),
    "roma": (41.9, 12.5), "milano": (45.5, 9.2), "budapest": (47.5, 19.0),
    "varsavia": (52.2, 21.0), "newyork": (40.7, -74.0), "helsinki": (60.2, 24.9),
    "copenaghen": (55.7, 12.6), "toronto": (43.7, -79.4), "zurigo": (47.4, 8.5),
    "vienna": (48.2, 16.4), "praga": (50.1, 14.4), "sydney": (-33.9, 151.2),
    "boston": (42.3, -71.1), "cairo": (30.0, 31.2), "oslo": (59.9, 10.7),
    "parigi": (48.8, 2.3), "lisbona": (38.7, -9.1), "dublino": (53.3, -6.3),
    "amsterdam": (52.4, 4.9), "madrid": (40.4, -3.7), "bruxelles": (50.8, 4.4),
    "dubai": (25.2, 55.3), "losangeles": (34.0, -118.2), "stoccolma": (59.3, 18.1),
    "chicago": (41.8781, -87.6298),"mumbai": (19.0760, 72.8777),"beijing": (39.9042, 116.4074),
    "moscow": (55.7558, 37.6176),"singapore": (1.3521, 103.8198),
}

# === Distanza geografica (haversine) ===
def distanza_geografica(c1, c2):
    if c1 not in coord or c2 not in coord:
        return 0
    lat1, lon1 = coord[c1]
    lat2, lon2 = coord[c2]
    R = 6371
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

# === Euristica per A* ===
def euristica(u, v):
    return distanza_geografica(u, v)

# === Caricamento grafo da file .pl ===

def carica_voli_da_pl(file_name):
    G = nx.DiGraph()
    pattern = re.compile(r"flight\((\w+),\s*(\w+),\s*(\d+),\s*(\d+),\s*(\w+)\)\.")
    
    # Percorso assoluto del file rispetto alla posizione di questo script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, file_name)
    
    with open(file_path, "r") as f:
        for line in f:
            match = pattern.match(line.strip().lower())
            if match:
                part, arr, costo, durata, comp = match.groups()
                distanza = distanza_geografica(part, arr)
                G.add_edge(part, arr, costo=int(costo), durata=int(durata), compagnia=comp, distanza=float(distanza))
    return G


partenza_corrente = None
arrivo_corrente = None

def peso_con_scali(u, v, data):
    if u == partenza_corrente and v == arrivo_corrente:
        return data["distanza"]
    return data["distanza"] * 1.10  # penalità per scali

# === Algoritmo A* ===
def percorso_astar(G, partenza, arrivo):

    global partenza_corrente, arrivo_corrente
    partenza_corrente = partenza
    arrivo_corrente = arrivo

    try:
        percorso = nx.astar_path(G, partenza, arrivo, heuristic=euristica, weight=peso_con_scali)
        costo = sum(G[u][v]['costo'] for u, v in zip(percorso[:-1], percorso[1:]))
        durata = int(sum(G[u][v]['durata'] for u, v in zip(percorso[:-1], percorso[1:])))
        return percorso, costo, durata
    except nx.NetworkXNoPath:
        return None
