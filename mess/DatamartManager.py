import string
import os
import matplotlib.pyplot as plt


def visualize_graph_with_weights(graph):
    """
    Visualize the graph using matplotlib, adjusting edge thickness based on their weights
    and node sizes based on their counts.

    Args:
        graph (nx.Graph): The graph to visualize.
    """
    plt.figure(figsize=(15, 15))

    # Get edge weights
    weights = [data['weight'] for _, _, data in graph.edges(data=True)]

    # Normalize weights for edge thickness
    max_weight = max(weights) if weights else 1
    min_weight = min(weights) if weights else 1
    if max_weight == min_weight:
        widths = [1 for _ in weights]
    else:
        widths = [1 + 4 * ((weight - min_weight) / (max_weight - min_weight)) for weight in weights]

    pos = nx.spring_layout(graph, k=0.15, iterations=20, seed=42)

    # Get counts for node sizes
    counts = [graph.nodes[node]['count'] for node in graph.nodes()]
    max_count = max(counts) if counts else 1
    min_count = min(counts) if counts else 1
    if max_count == min_count:
        sizes = [300 for _ in counts]
    else:
        sizes = [
            300 + 700 * ((count - min_count) / (max_count - min_count)) for count in counts
        ]

    # Draw nodes with sizes
    nx.draw_networkx_nodes(graph, pos, node_size=sizes, node_color='blue', alpha=0.7)

    # Draw edges with normalized widths
    nx.draw_networkx_edges(graph, pos, width=widths, alpha=0.5)

    plt.title("Three-Letter Words Graph with Weighted Edges and Scaled Nodes")
    plt.axis('off')
    plt.show()


def visualize_path(graph, path):
    """
    Visualize the graph and highlight the specified path.

    Args:
        graph (nx.Graph): The graph to visualize.
        path (list): List of words forming the path to highlight.
    """
    plt.figure(figsize=(15, 15))

    # Get edge weights
    weights = [data['weight'] for _, _, data in graph.edges(data=True)]

    # Normalize weights for edge thickness
    max_weight = max(weights) if weights else 1
    min_weight = min(weights) if weights else 1
    if max_weight == min_weight:
        widths = [1 for _ in weights]
    else:
        widths = [1 + 4 * ((weight - min_weight) / (max_weight - min_weight)) for weight in weights]

    pos = nx.spring_layout(graph, k=0.15, iterations=20, seed=42)

    # Draw all nodes
    nx.draw_networkx_nodes(graph, pos, node_size=50, node_color='blue', alpha=0.7)

    # Draw all edges with normalized widths
    nx.draw_networkx_edges(graph, pos, width=widths, alpha=0.3)

    # Highlight the path if it exists
    if path:
        # Create a list of edges in the path
        path_edges = list(zip(path, path[1:]))
        # Draw path edges with higher thickness and red color
        nx.draw_networkx_edges(
            graph,
            pos,
            edgelist=path_edges,
            width=4,
            edge_color='red'
        )
        # Draw path nodes with larger size and red color
        nx.draw_networkx_nodes(
            graph,
            pos,
            nodelist=path,
            node_size=100,
            node_color='red',
            alpha=0.9
        )

    plt.title("Three-Letter Words Graph with Highlighted Path")
    plt.axis('off')
    plt.show()


def main():
    """
    Main function to execute the script.
    """
    # Specify the path to the text file
    filename = r'pg74507.txt'

    # Optionally, print the current directory to verify relative paths
    print(f"Current directory: {os.getcwd()}")

    # Extract the three-letter words vocabulary
    word_counts = extract_vocabulary(filename, remove_stopwords=True)

    if word_counts:
        print(f"\nTotal unique three-letter words: {len(word_counts)}")
        print("Sample three-letter words and their counts:")
        for word, count in list(word_counts.items())[:10]:
            print(f"{word}: {count}")

        # Build the graph using the optimized method
        graph = build_weight_graph(word_counts)
        print(f"\nTotal nodes in the graph: {graph.number_of_nodes()}")
        print(f"Total edges in the graph: {graph.number_of_edges()}")

        # Optionally, print some edges with their weights
        print("\nSample edges with weights:")
        for u, v, data in list(graph.edges(data=True))[:10]:
            print(f"{u} - {v}: Weight = {data['weight']}")

        # Visualize the graph with improved visualization
        visualize_graph_with_weights(graph)

        # Interactive loop for finding the shortest paths
        while True:
            print("\n--- Shortest Path Calculation ---")
            origin = input("Enter the origin word (or 'exit' to quit): ").lower()
            if origin == 'exit':
                break
            destination = input("Enter the destination word (or 'exit' to quit): ").lower()
            if destination == 'exit':
                break
            algorithm = input("Select the algorithm ('dijkstra' or 'astar'): ").lower()
            if algorithm not in ['dijkstra', 'astar']:
                print("Invalid algorithm. Please choose 'dijkstra' or 'astar'.")
                continue

            # Calculate the shortest path
            path = calculate_shortest_path(graph, origin, destination, algorithm=algorithm)

            if path:
                print(
                    f"\nShortest path between '{origin}' and '{destination}' using {algorithm.capitalize()}:")
                print(" -> ".join(path))

                # Visualize the path on the graph
                visualize_path(graph, path)
            else:
                print("Could not find a path between the specified words.")
    else:
        print("Failed to extract vocabulary due to a previous error.")


if __name__ == "__main__":
    main()
