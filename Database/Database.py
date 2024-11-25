from abc import ABC, abstractmethod


class Database(ABC):
    @abstractmethod
    def create_database(self):
        pass

    @abstractmethod
    def add_data(self, filepaths):
        pass

    @abstractmethod
    def extract_data(self, filename, output_directory):
        pass
