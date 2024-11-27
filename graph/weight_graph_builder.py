from graph_builder import GraphBuilder
import networkx as nx


class WeightGraphBuilder(GraphBuilder):

    def build_graph(self, word_count):
        """
        Build an optimized graph where nodes are words and edges connect words that differ by one letter.
        Edge weights are based on the average occurrences of the connected words.

        This method reduces time complexity by grouping words by common patterns.

        Args:
            word_count (Counter): Counter with words as keys and their occurrences as values.

        Returns:
            nx.Graph: The constructed graph with weighted edges.
        """

        graph = nx.Graph()

        # Add nodes with occurrence attribute
        for word, count in word_count.items():
            graph.add_node(word, count=count)

        # Create a dictionary to group words by patterns with one letter replaced by '_'
        patterns = {}
        for word in word_count:
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
                    count1 = word_count[word1]
                    count2 = word_count[word2]
                    weight = (count1 + count2) / 2
                    graph.add_edge(word1, word2, weight=weight)

        return graph
