import networkx as nx
from TOP_alg import create_graph, dp_top1, top_multiple_flows, visualize_graph
from TOM_alg import traffic_optimal_vnf_migration


################################
######### TOP Alg Test #########
################################

# def main():
#     # Create the graph
#     print("Creating PPDC graph...")
#     G = create_graph()
#     print("Nodes:", G.nodes(data=True))
#     print("Edges:", G.edges(data=True))
    
#     # Solve TOP-1 for a single flow
#     print("\nSolving TOP-1 for a single VM flow...")
#     source = "h1"
#     target = "h4"
#     num_vnfs = 3
#     cost, path = dp_top1(G, source, target, num_vnfs)
#     print(f"Single Flow (source: {source}, target: {target}, VNFs: {num_vnfs})")
#     print(f"Minimum Cost: {cost}")
#     print(f"Optimal Path: {path}")
    
#     # Solve general TOP for multiple flows
#     print("\nSolving general TOP for multiple VM flows...")
#     vm_flows = [("h1", "h4"), ("h2", "h3")]
#     placements, total_cost = top_multiple_flows(G, vm_flows, num_vnfs)
#     print("Multiple Flows Placements:")
#     for flow, placement in placements.items():
#         print(f"Flow {flow}: Path {placement}")
#     print(f"Total Cost for Multiple Flows: {total_cost}")
    
#     # Visualize the graph and placements
#     print("\nVisualizing the graph and VNF placements...")
#     visualize_graph(G, placements)
#     print("Visualization complete!")

# if __name__ == "__main__":
#     main()

################################
######### TOM Alg Test #########
################################
def main():
    # Create the graph
    print("Creating PPDC graph...")
    G = create_graph()
    print("Nodes:", G.nodes(data=True))
    print("Edges:", G.edges(data=True))

    # Define VM flows and parameters
    vm_flows = [("h1", "h4"), ("h2", "h3")]
    num_vnfs = 3
    migration_coeff = 10  # Example migration cost coefficient

    # Solve TOM
    print("\nSolving Traffic-Optimal VNF Migration (TOM)...")
    final_placement, total_cost, migration_paths = traffic_optimal_vnf_migration(G, vm_flows, num_vnfs, migration_coeff)
    
    # Print results
    print("Final VNF Placement:", final_placement)
    print("Total Cost:", total_cost)
    print("Migration Paths:")
    for vnf, path in migration_paths.items():
        print(f"VNF {vnf}: Path {path}")

    # Visualize
    print("\nVisualizing the migration paths...")
    visualize_graph(G, migration_paths)
    print("Visualization complete!")

if __name__ == "__main__":
    main()
