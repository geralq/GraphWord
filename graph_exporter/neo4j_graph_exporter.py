from neo4j import GraphDatabase
from BaseExporter import GraphExporter


class Neo4jGraphExporter(GraphExporter):
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def export_graph(self, graph):
        """
        Exports a graph to Neo4j.
        """
        with self.driver.session() as session:
            for node, data in graph.nodes(data=True):
                session.run(
                    "MERGE (w:Word {text: $text, count: $count})",
                    text=node, count=data.get('count', 0)
                )
            for u, v, data in graph.edges(data=True):
                session.run(
                    """
                    MATCH (w1:Word {text: $word1}), (w2:Word {text: $word2})
                    MERGE (w1)-[:RELATES {weight: $weight}]->(w2)
                    """,
                    word1=u, word2=v, weight=data.get('weight', 1)
                )

    def close(self):
        """
        Close the connection with Neo4j.
        """
        self.driver.close()
