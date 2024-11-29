import networkx as nx
import matplotlib.pyplot as plt

def create_graph():
    
    # Create a PPDC graph with hosts and switches.
    # Returns:
    #     G: NetworkX graph with nodes and edges.
    
    G = nx.Graph()

    # Add hosts
    hosts = ["h1", "h2", "h3", "h4"]
    switches = ["s1", "s2", "s3", "s4", "s5"]
    
    # Add nodes
    for host in hosts:
        G.add_node(host, type="host")
    for switch in switches:
        G.add_node(switch, type="switch")
    
    # Add edges with weights (example weights as delays)
    edges = [
        ("h1", "s1", 1), ("h2", "s2", 1),
        ("s1", "s2", 2), ("s2", "s3", 2),
        ("s3", "s4", 3), ("s4", "s5", 3),
        ("h3", "s3", 1), ("h4", "s5", 1)
    ]
    for u, v, weight in edges:
        G.add_edge(u, v, weight=weight)
    
    return G

### Example usage ###
# G = create_graph()
# print("Nodes:", G.nodes(data=True))
# print("Edges:", G.edges(data=True))


def dp_top1(graph, s, t, n):
    
    # Solve the TOP-1 problem using dynamic programming.
    # Args:
    #     graph:    NetworkX graph representing the PPDC.
    #     s:        Source node (e.g., host of v1).
    #     t:        Destination node (e.g., host of v1').
    #     n:        Number of VNFs to traverse.
    # Returns:
    #     cost:     Minimum communication cost.
    #     path:     List of nodes representing the stroll.
    
    # Initialize DP table
    dp = {}
    predecessor = {}
    nodes = list(graph.nodes)
    for u in nodes:
        for e in range(1, n + 2):  # Edge count
            dp[(u, e)] = float('inf')
            predecessor[(u, e)] = None

    # Base case: Single edge from s to t
    dp[(s, 1)] = 0

    # Fill DP table
    for e in range(2, n + 2):  # Increasing edge count
        for u in nodes:
            for v in graph.neighbors(u):
                weight = graph[u][v]["weight"]
                if dp[(v, e - 1)] + weight < dp[(u, e)]:
                    dp[(u, e)] = dp[(v, e - 1)] + weight
                    predecessor[(u, e)] = v

    # Find optimal stroll
    cost = float('inf')
    end_node = None
    for u in nodes:
        if dp[(u, n + 1)] < cost:
            cost = dp[(u, n + 1)]
            end_node = u

    # Reconstruct path
    path = []
    e = n + 1
    while end_node:
        path.append(end_node)
        end_node = predecessor[(end_node, e)]
        e -= 1

    return cost, path[::-1]

### Example usage ###
# cost, path = dp_top1(G, "h1", "h4", 3)
# print("Minimum Cost:", cost)
# print("Optimal Path:", path)

def top_multiple_flows(graph, vm_flows, n):
    
    # Solve the general TOP problem for multiple VM flows.
    # Args:
    #     graph:        NetworkX graph representing the PPDC.
    #     vm_flows:     List of VM flow tuples [(v1, v1'), (v2, v2'), ...].
    #     n:            Number of VNFs to place.
    # Returns:
    #     placements:   Dictionary mapping flows to their VNF placement.
    #     total_cost:   Total communication cost.
    
    total_cost = 0
    placements = {}

    for v1, v1_prime in vm_flows:
        # Solve TOP-1 for each flow
        cost, path = dp_top1(graph, v1, v1_prime, n)
        total_cost += cost
        placements[(v1, v1_prime)] = path

    return placements, total_cost

### Example usage with multiple flows ###
# vm_flows = [("h1", "h4"), ("h2", "h3")]
# placements, total_cost = top_multiple_flows(G, vm_flows, 3)
# print("Placements:", placements)
# print("Total Cost:", total_cost)


def visualize_graph(graph, placements):
    
    # Visualize the graph and VNF placements.
    # Args:
    #     graph:        NetworkX graph.
    #     placements:   Dictionary of VM flows and their placements.
    
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_size=700, font_size=10)
    for flow, path in placements.items():
        edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
        nx.draw_networkx_edges(graph, pos, edgelist=edges, edge_color='r', width=2)
    plt.show()

# Example visualization
# visualize_graph(G, placements)