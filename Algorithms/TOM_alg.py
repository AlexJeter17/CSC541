from TOP_alg import top_multiple_flows
import networkx as nx

def compute_migration_cost(graph, p, m, migration_coeff):
    
    # Compute the migration cost for moving VNFs from current placement to new placement.
    # Args:
    #     graph:            NetworkX graph representing the PPDC.
    #     p:                Current VNF placement (dict {VNF: current_switch}).
    #     m:                New VNF placement (dict {VNF: new_switch}).
    #     migration_coeff:  Migration cost coefficient (µ).
    # Returns:
    #     migration_cost:   Total migration cost.
    
    migration_cost = 0
    for vnf in p:
        current = p[vnf]
        new = m[vnf]
        path_cost = nx.shortest_path_length(graph, current, new, weight="weight")
        migration_cost += migration_coeff * path_cost
    return migration_cost

def migrate_vnfs(graph, p, p_prime, migration_coeff):
    
    # Perform VNF migration using parallel migration frontiers.
    # Args:
    #     graph:            NetworkX graph representing the PPDC.
    #     p:                Current VNF placement (dict {VNF: current_switch}).
    #     p_prime:          New VNF placement (dict {VNF: new_switch}).
    #     migration_coeff:  Migration cost coefficient (µ).
    # Returns:
    #     total_cost:       Total cost after migration.
    #     final_placement:  Updated VNF placement.
    
    # Initialize migration process
    migration_path = {vnf: [p[vnf]] for vnf in p}  # Record migration paths
    current_placement = p.copy()
    total_migration_cost = 0

    while current_placement != p_prime:
        # For each VNF, move one step closer to its target
        for vnf in p:
            if current_placement[vnf] != p_prime[vnf]:
                # Get shortest path to target and move one step
                path = nx.shortest_path(graph, current_placement[vnf], p_prime[vnf], weight="weight")
                next_step = path[1]  # Take the next step
                step_cost = migration_coeff * graph[current_placement[vnf]][next_step]["weight"]
                total_migration_cost += step_cost
                current_placement[vnf] = next_step
                migration_path[vnf].append(next_step)

    return total_migration_cost, current_placement, migration_path

def traffic_optimal_vnf_migration(graph, vm_flows, num_vnfs, migration_coeff):
    
    # Solve the Traffic-Optimal VNF Migration (TOM) problem.
    # Args:
    #     graph:            NetworkX graph representing the PPDC.
    #     vm_flows:         List of VM flow tuples [(v1, v1'), (v2, v2'), ...].
    #     num_vnfs:         Number of VNFs to place and migrate.
    #     migration_coeff:  Migration cost coefficient (µ).
    # Returns:
    #     final_placement:  Final VNF placement after migration.
    #     total_cost:       Total cost including migration and communication.
    
    # Compute initial VNF placement using TOP
    print("Computing initial VNF placement...")
    initial_placement, comm_cost_initial = top_multiple_flows(graph, vm_flows, num_vnfs)

    # Simulate a traffic change and compute new placement
    print("Simulating traffic change and computing new placement...")
    new_placement, comm_cost_new = top_multiple_flows(graph, vm_flows[::-1], num_vnfs)  # Simulate traffic flip

    # Perform VNF migration from initial to new placement
    print("Performing VNF migration...")
    migration_cost, final_placement, migration_paths = migrate_vnfs(graph, initial_placement, new_placement, migration_coeff)

    # Total cost = Communication cost after migration + Migration cost
    total_cost = comm_cost_new + migration_cost

    return final_placement, total_cost, migration_paths
