import string
import os
from collections import Counter

import nltk
from nltk.corpus import stopwords
import networkx as nx
import matplotlib.pyplot as plt

# Download necessary NLTK resources (only the first time)
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)


def extract_vocabulary(filename, remove_stopwords=True):
    """
    Extract a vocabulary of three-letter words from a text file and count their occurrences.

    Args:
        filename (str): Path to the text file.
        remove_stopwords (bool): Whether to remove English stopwords.

    Returns:
        Counter: A Counter object with three-letter words as keys and their occurrences as values.
    """
    if not os.path.isfile(filename):
        print(f"Error: The file '{filename}' does not exist.")
        return Counter()

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            text = file.read()
    except UnicodeDecodeError:
        try:
            with open(filename, 'r', encoding='latin-1') as file:
                text = file.read()
        except Exception as e:
            print(f"Error: Unable to read the file: {e}")
            return Counter()
    except Exception as e:
        print(f"Error: Unable to read the file: {e}")
        return Counter()

    text = text.lower()
    text = ''.join(char if char.isalpha() or char.isspace() else ' ' for char in text)
    words = nltk.word_tokenize(text)
    three_letter_words = [word for word in words if len(word) == 3]

    if remove_stopwords:
        stop_words = set(stopwords.words('english'))
        three_letter_words = [word for word in three_letter_words if word not in stop_words]

    return Counter(three_letter_words)


def differ_by_one_letter(word_a, word_b):
    """
    Check if two three-letter words differ by exactly one letter.

    Args:
        word_a (str): First three-letter word.
        word_b (str): Second three-letter word.

    Returns:
        bool: True if they differ by one letter, False otherwise.
    """
    differing_letters = sum(1 for a, b in zip(word_a, word_b) if a != b)
    return differing_letters == 1


def build_weight_graph(word_counts):
    """
    Build an optimized graph where nodes are words and edges connect words that differ by one letter.
    Edge weights are based on the average occurrences of the connected words.

    This method reduces time complexity by grouping words by common patterns.

    Args:
        word_counts (Counter): Counter with words as keys and their occurrences as values.

    Returns:
        nx.Graph: The constructed graph with weighted edges.
    """
    graph = nx.Graph()

    # Add nodes with occurrence attribute
    for word, count in word_counts.items():
        graph.add_node(word, count=count)

    # Create a dictionary to group words by patterns with one letter replaced by '_'
    patterns = {}
    for word in word_counts:
        for i in range(3):
            pattern = word[:i] + '_' + word[i + 1:]
            patterns.setdefault(pattern, set()).add(word)

    # Add edges based on shared patterns
    for group in patterns.values():
        group = list(group)
        n = len(group)
        for i in range(n):
            for j in range(i + 1, n):
                word1 = group[i]
                word2 = group[j]
                count1 = word_counts[word1]
                count2 = word_counts[word2]
                weight = (count1 + count2) / 2
                graph.add_edge(word1, word2, weight=weight)

    return graph


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


def hamming_distance(word1, word2):
    """
    Calculate the Hamming distance between two words of equal length.

    Args:
        word1 (str): First word.
        word2 (str): Second word.

    Returns:
        int: Number of positions at which the corresponding letters are different.
    """
    return sum(c1 != c2 for c1, c2 in zip(word1, word2))


def calculate_shortest_path(graph, origin, destination, algorithm='dijkstra'):
    """
    Calculate the shortest path between two words in the graph using Dijkstra or A* algorithm.

    Args:
        graph (nx.Graph): The graph to search.
        origin (str): Origin word.
        destination (str): Destination word.
        algorithm (str): Algorithm to use ('dijkstra' or 'astar').

    Returns:
        list or None: List of words forming the shortest path, or None if no path exists.
    """
    if origin not in graph.nodes:
        print(f"Error: The origin word '{origin}' is not in the graph.")
        return None
    if destination not in graph.nodes:
        print(f"Error: The destination word '{destination}' is not in the graph.")
        return None
    if algorithm not in ['dijkstra', 'astar']:
        print("Error: The algorithm must be 'dijkstra' or 'astar'.")
        return None

    try:
        if algorithm == 'dijkstra':
            path = nx.dijkstra_path(graph, origin, destination, weight='weight')
        elif algorithm == 'astar':
            path = nx.astar_path(
                graph,
                origin,
                destination,
                heuristic=lambda u, v: hamming_distance(u, v),
                weight='weight'
            )
        return path
    except nx.NetworkXNoPath:
        print(f"No path exists between '{origin}' and '{destination}'.")
        return None
    except Exception as e:
        print(f"Error while calculating the path: {e}")
        return None


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
    filename = r'C:\Users\gerar\OneDrive\Escritorio\Cuarto\TSCD\GraphWord\Datalake\pg74507.txt'

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
