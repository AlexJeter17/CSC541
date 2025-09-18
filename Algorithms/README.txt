Traffic-Optimal VNF Placement and Migration


Test edit 

This project implements two key algorithms for optimizing Virtual Network Function (VNF) placement and migration in cloud-based Policy-Preserving Data Centers (PPDCs).
Algorithms

    Traffic-Optimal VNF Placement (TOP):
        Finds the optimal placement of VNFs to minimize total communication costs between Virtual Machines (VMs).
        Includes:
            Single Flow Placement (TOP-1): Optimizes placement for a single VM flow.
            Multiple Flow Placement: Extends the optimization to multiple VM flows.

    Traffic-Optimal VNF Migration (TOM):
        Dynamically adjusts VNF placements in response to changing traffic patterns.
        Balances between:
            Communication costs after migration.
            Migration costs for moving VNFs.

Functions

    create_graph():
        Creates a sample PPDC graph with hosts, switches, and weighted edges representing communication delays.

    dp_top1(graph, s, t, n):
        Solves the single flow placement (TOP-1) problem using dynamic programming.
        Inputs:
            graph: PPDC graph.
            s, t: Source and target nodes.
            n: Number of VNFs to traverse.
        Outputs:
            cost: Minimum communication cost.
            path: Optimal path for the flow.

    top_multiple_flows(graph, vm_flows, n):
        Solves the general VNF placement problem for multiple VM flows.
        Inputs:
            graph: PPDC graph.
            vm_flows: List of VM flow pairs (source, target).
            n: Number of VNFs to place.
        Outputs:
            placements: Dictionary mapping VM flows to their optimal paths.
            total_cost: Total communication cost.

    compute_migration_cost(graph, p, m, migration_coeff):
        Calculates the migration cost of moving VNFs from the current placement to a new placement.
        Inputs:
            graph: PPDC graph.
            p: Current placement.
            m: New placement.
            migration_coeff: Migration cost coefficient.
        Output:
            migration_cost: Total migration cost.

    migrate_vnfs(graph, p, p_prime, migration_coeff):
        Migrates VNFs step-by-step using parallel migration frontiers.
        Inputs:
            graph: PPDC graph.
            p: Current VNF placement.
            p_prime: New VNF placement.
            migration_coeff: Migration cost coefficient.
        Outputs:
            total_cost: Total migration cost.
            final_placement: Final VNF placement after migration.
            migration_path: Paths taken by each VNF during migration.

    traffic_optimal_vnf_migration(graph, vm_flows, num_vnfs, migration_coeff):
        Combines TOP and TOM to handle dynamic traffic changes.
        Inputs:
            graph: PPDC graph.
            vm_flows: List of VM flows.
            num_vnfs: Number of VNFs to place/migrate.
            migration_coeff: Migration cost coefficient.
        Outputs:
            final_placement: Final placement after migration.
            total_cost: Total cost (communication + migration).
            migration_paths: Migration paths for VNFs.

    visualize_graph(graph, placements):
        Visualizes the graph and highlights VNF placements or migration paths.

How to Use

    Import the functions into your Python script.
    Call the create_graph() function to generate a sample PPDC graph.
    Use dp_top1 or top_multiple_flows for VNF placement.
    Use traffic_optimal_vnf_migration for placement and migration with dynamic traffic.
    Visualize the results with visualize_graph.