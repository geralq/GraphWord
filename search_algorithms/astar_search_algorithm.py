from search_algorithm import SearchAlgorithm


class AstarSearchAlgorithm(SearchAlgorithm):
    def search(self, start, goal, graph):
        if start not in graph.nodes:
            print(f"Error: The start word '{start}' is not in the graph.")
            return None
        if goal not in graph.nodes:
            print(f"Error: The goal word '{goal}' is not in the graph.")
            return None

        try:
            path = nx.astar_path(
                graph,
                start,
                goal,
                heuristic=lambda u, v: self._hamming_distance(u, v),
                weight='weight'
            )
            return path
        except nx.NetworkXNoPath:
            print(f"No path exists between '{start}' and '{goal}'.")
            return None
        except Exception as e:
            print(f"Error while calculating the path: {e}")
            return None

    def _hamming_distance(self, wordA, wordB):
        """
        Calculate the Hamming distance between two words of equal length.

        Args:
            wordA (str): First word.
            wordB (str): Second word.

        Returns:
            int: Number of positions at which the corresponding letters are different.
        """
        return sum(c1 != c2 for c1, c2 in zip(wordA, wordB))
