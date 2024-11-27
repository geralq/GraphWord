from abc import ABC, abstractmethod


class GraphExporter(ABC):
    @abstractmethod
    def export_graph(self, graph):
        """
        Exports a graph to a specific database.
        Args:
            graph (networkx.Graph): graph to export.
        """
        pass
