import networkx as nx
import numpy as np
import random
import matplotlib.pyplot as plt
import math

# Step 1: Define the Network Topology Functions
def create_ring_topology(num_switches, num_hosts):
    G = nx.Graph()
    switch_nodes = range(num_switches)
    host_nodes = range(num_switches, num_switches + num_hosts)
    
    # Create ring of switches
    for i in switch_nodes:
        G.add_edge(i, (i + 1) % num_switches, latency=random.uniform(1, 10))
    
    # Connect each host to a random switch
    for host in host_nodes:
        connected_switch = random.choice(switch_nodes)
        G.add_edge(host, connected_switch, latency=random.uniform(1, 10))
    
    return G

def create_star_topology(num_switches, num_hosts):
    G = nx.Graph()
    switch_nodes = range(num_switches)
    host_nodes = range(num_switches, num_switches + num_hosts)
    
    # Create star topology with one central switch
    central_switch = 0
    for i in switch_nodes:
        if i != central_switch:
            G.add_edge(central_switch, i, latency=random.uniform(1, 10))
    
    # Connect each host to a random switch
    for host in host_nodes:
        connected_switch = random.choice(switch_nodes)
        G.add_edge(host, connected_switch, latency=random.uniform(1, 10))
    
    return G

def create_bus_topology(num_switches, num_hosts):
    G = nx.Graph()
    switch_nodes = range(num_switches)
    host_nodes = range(num_switches, num_switches + num_hosts)
    
    # Create bus topology
    for i in range(num_switches - 1):
        G.add_edge(i, i + 1, latency=random.uniform(1, 10))
    
    # Connect each host to a random switch
    for host in host_nodes:
        connected_switch = random.choice(switch_nodes)
        G.add_edge(host, connected_switch, latency=random.uniform(1, 10))
    
    return G

def create_erdos_renyi_topology(num_switches, num_hosts, connection_prob):
    G = nx.erdos_renyi_graph(num_switches, connection_prob, seed=42)
    switch_nodes = list(G.nodes)
    host_nodes = range(num_switches, num_switches + num_hosts)
    
    # Ensure the graph is connected
    while not nx.is_connected(G):
        i, j = random.sample(switch_nodes, 2)
        G.add_edge(i, j, latency=random.uniform(1, 10))
    
    # Connect each host to a random switch
    for host in host_nodes:
        G.add_node(host, type='host')
        connected_switch = random.choice(switch_nodes)
        G.add_edge(host, connected_switch, latency=random.uniform(1, 10))
    
    return G

# Step 2: Compute Latencies in Time Units
def compute_latencies(G):
    return dict(nx.all_pairs_dijkstra_path_length(G, weight='latency'))

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

    return best_placement, min_max_latency

def compute_max_latency(G, controllers):
    latencies = compute_latencies(G)
    max_latency = 0
    for node in G.nodes:
        min_latency_to_controller = min(latencies[node][controller] for controller in controllers)
        max_latency = max(max_latency, min_latency_to_controller)
    return max_latency

# Parameters
min_nodes = 20
max_nodes = 100
connection_prob = 0.1

# Generate a random number of nodes
num_nodes = random.randint(min_nodes, max_nodes)
num_switches = int(num_nodes * 0.2)
num_hosts = num_nodes - num_switches

# Decide number of controllers based on 10% of total nodes (rounded up)
num_controllers = math.ceil(num_nodes * 0.1)

# List of topology functions
topologies = ['ring', 'star', 'bus', 'erdos_renyi']

# Randomly select a topology
topology_type = random.choice(topologies)

if topology_type == 'ring':
    G = create_ring_topology(num_switches, num_hosts)
elif topology_type == 'star':
    G = create_star_topology(num_switches, num_hosts)
elif topology_type == 'bus':
    G = create_bus_topology(num_switches, num_hosts)
elif topology_type == 'erdos_renyi':
    G = create_erdos_renyi_topology(num_switches, num_hosts, connection_prob)

# Simulation Execution
controllers, min_max_latency = place_controllers(G, num_controllers)

print("Number of Nodes:", num_nodes)
print("Number of Controllers:", num_controllers)
print("Selected Topology:", topology_type)
print("Optimal Controller Placement:", controllers)
print("Minimum Maximum Latency:", min_max_latency, "ms")

# Visualization
pos = nx.spring_layout(G)
switch_nodes = [node for node in range(num_switches)]
host_nodes = [node for node in range(num_switches, num_switches + num_hosts)]

nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10)
nx.draw_networkx_nodes(G, pos, nodelist=switch_nodes, node_color='blue', node_size=500)
nx.draw_networkx_nodes(G, pos, nodelist=host_nodes, node_color='green', node_size=300)
nx.draw_networkx_nodes(G, pos, nodelist=controllers, node_color='red', node_size=700)
plt.show()
