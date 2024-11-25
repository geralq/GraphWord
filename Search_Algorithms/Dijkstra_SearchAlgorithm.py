from SearchAlgorithm import SearchAlgorithm
import networkx as nx


class Dijkstra_SearchAlgorithm(SearchAlgorithm):
    def search(self, start, goal, graph):
        try:

            path = nx.dijkstra_path(graph, origin, destination, weight='weight')

            return path
        except nx.NetworkXNoPath:
            print(f"No path exists between '{origin}' and '{destination}'.")
            return None
        except Exception as e:
            print(f"Error while calculating the path: {e}")
            return None
