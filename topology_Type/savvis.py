import networkx as nx
import numpy as np
import random
import matplotlib.pyplot as plt

# Step 1: Define the Network Topology Functions
def create_ring_topology(num_nodes):
    G = nx.Graph()
    for i in range(num_nodes):
        G.add_edge(i, (i + 1) % num_nodes)
    return G

def create_star_topology(num_nodes):
    G = nx.Graph()
    for i in range(1, num_nodes):
        G.add_edge(0, i)
    return G

def create_bus_topology(num_nodes):
    G = nx.Graph()
    for i in range(num_nodes - 1):
        G.add_edge(i, i + 1)
    return G

def create_erdos_renyi_topology(num_nodes, connection_prob):
    G = nx.erdos_renyi_graph(num_nodes, connection_prob, seed=42)
    while not nx.is_connected(G):
        G = nx.erdos_renyi_graph(num_nodes, connection_prob, seed=random.randint(0, 1000))
    return G

def create_savvis_topology(num_nodes):
    G = nx.Graph()
    # Combine star, ring, and mesh topology components
    # Star topology core
    for i in range(1, num_nodes // 3):
        G.add_edge(0, i)
    # Ring topology segment
    for i in range(num_nodes // 3, 2 * num_nodes // 3):
        G.add_edge(i, (i + 1) % (2 * num_nodes // 3 - num_nodes // 3) + num_nodes // 3)
    # Mesh topology segment
    for i in range(2 * num_nodes // 3, num_nodes):
        for j in range(i + 1, num_nodes):
            if random.random() < 0.3:  # Connection probability
                G.add_edge(i, j)
    return G

# Step 2: Compute Latencies
def compute_latencies(G):
    return dict(nx.all_pairs_shortest_path_length(G))

# Step 3: Place Controllers
def place_controllers(G, num_controllers):
    all_nodes = list(G.nodes)
    best_placement = None
    min_max_latency = float('inf')

    # Heuristic: Randomly select controller placements and evaluate
    for _ in range(1000):
        controllers = random.sample(all_nodes, num_controllers)
        max_latency = compute_max_latency(G, controllers)
        
        if max_latency < min_max_latency:
            min_max_latency = max_latency
            best_placement = controllers

    if best_placement is None:
        # Fallback to default placement if no optimal placement found
        best_placement = random.sample(all_nodes, num_controllers)
        min_max_latency = compute_max_latency(G, best_placement)

    return best_placement, min_max_latency

def compute_max_latency(G, controllers):
    latencies = compute_latencies(G)
    max_latency = 0
    for node in G.nodes:
        min_latency_to_controller = min(latencies[node].get(controller, float('inf')) for controller in controllers)
        max_latency = max(max_latency, min_latency_to_controller)
    return max_latency

# Simulation Parameters
num_nodes = 50
connection_prob = 0.1
num_controllers = 3

# Choose the topology type
topology_type = 'savvis'  # Change this to 'ring', 'bus', 'erdos_renyi', or 'savvis'

if topology_type == 'ring':
    G = create_ring_topology(num_nodes)
elif topology_type == 'star':
    G = create_star_topology(num_nodes)
elif topology_type == 'bus':
    G = create_bus_topology(num_nodes)
elif topology_type == 'erdos_renyi':
    G = create_erdos_renyi_topology(num_nodes, connection_prob)
elif topology_type == 'savvis':
    G = create_savvis_topology(num_nodes)

# Simulation Execution
controllers, min_max_latency = place_controllers(G, num_controllers)

print("Optimal Controller Placement:", controllers)
print("Minimum Maximum Latency:", min_max_latency)

# Visualization
pos = nx.spring_layout(G)
hosts = [node for node in G.nodes if node not in controllers]
switches = [node for node in G.nodes if node not in controllers and node in hosts]

nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10)
nx.draw_networkx_nodes(G, pos, nodelist=hosts, node_color='green', node_size=500, label='Hosts')
nx.draw_networkx_nodes(G, pos, nodelist=switches, node_color='blue', node_size=500, label='Switches')
nx.draw_networkx_nodes(G, pos, nodelist=controllers, node_color='red', node_size=700, label='Controllers')
nx.draw_networkx_edges(G, pos)
plt.legend(scatterpoints=1)
plt.show()
