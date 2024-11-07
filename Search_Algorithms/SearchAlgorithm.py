from abc import ABC, abstractmethod


class SearchAlgorithm(ABC):
    @abstractmethod
    def search(self, start, goal, graph):
        pass
