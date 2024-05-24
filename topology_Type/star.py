import networkx as nx
import numpy as np
import random
import matplotlib.pyplot as plt

# Step 1: Define the Network Topology Functions
def create_ring_topology(num_switches, num_hosts):
    G = nx.Graph()
    switch_nodes = range(num_switches)
    host_nodes = range(num_switches, num_switches + num_hosts)
    
    # Create ring of switches
    for i in switch_nodes:
        G.add_edge(i, (i + 1) % num_switches)
    
    # Connect each host to a random switch
    for host in host_nodes:
        connected_switch = random.choice(switch_nodes)
        G.add_edge(host, connected_switch)
    
    return G

def create_star_topology(num_switches, num_hosts):
    G = nx.Graph()
    switch_nodes = range(num_switches)
    host_nodes = range(num_switches, num_switches + num_hosts)
    
    # Create star topology with one central switch
    central_switch = 0
    for i in switch_nodes:
        if i != central_switch:
            G.add_edge(central_switch, i)
    
    # Connect each host to a random switch
    for host in host_nodes:
        connected_switch = random.choice(switch_nodes)
        G.add_edge(host, connected_switch)
    
    return G

def create_bus_topology(num_switches, num_hosts):
    G = nx.Graph()
    switch_nodes = range(num_switches)
    host_nodes = range(num_switches, num_switches + num_hosts)
    
    # Create bus topology
    for i in range(num_switches - 1):
        G.add_edge(i, i + 1)
    
    # Connect each host to a random switch
    for host in host_nodes:
        connected_switch = random.choice(switch_nodes)
        G.add_edge(host, connected_switch)
    
    return G

def create_erdos_renyi_topology(num_switches, num_hosts, connection_prob):
    G = nx.erdos_renyi_graph(num_switches, connection_prob, seed=42)
    switch_nodes = list(G.nodes)
    host_nodes = range(num_switches, num_switches + num_hosts)
    
    # Ensure the graph is connected
    while not nx.is_connected(G):
        i, j = random.sample(switch_nodes, 2)
        G.add_edge(i, j)
    
    # Connect each host to a random switch
    for host in host_nodes:
        G.add_node(host, type='host')
        connected_switch = random.choice(switch_nodes)
        G.add_edge(host, connected_switch)
    
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

    return best_placement, min_max_latency

def compute_max_latency(G, controllers):
    latencies = compute_latencies(G)
    max_latency = 0
    for node in G.nodes:
        min_latency_to_controller = min(latencies[node][controller] for controller in controllers)
        max_latency = max(max_latency, min_latency_to_controller)
    return max_latency

# Simulation Parameters
num_switches = 10
num_hosts = 40
connection_prob = 0.2
num_controllers = 3

# Choose the topology type
topology_type = 'star'  # Change this to 'ring', 'bus', or 'erdos_renyi'

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

print("Optimal Controller Placement:", controllers)
print("Minimum Maximum Latency:", min_max_latency)

# Visualization
pos = nx.spring_layout(G)
switch_nodes = [node for node in range(num_switches)]
host_nodes = [node for node in range(num_switches, num_switches + num_hosts)]

nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10)
nx.draw_networkx_nodes(G, pos, nodelist=switch_nodes, node_color='blue', node_size=500)
nx.draw_networkx_nodes(G, pos, nodelist=host_nodes, node_color='green', node_size=300)
nx.draw_networkx_nodes(G, pos, nodelist=controllers, node_color='red', node_size=700)
plt.show()