# Database/SQLite3_Database.py
import os
import sqlite3
from .Database import Database  # Ensure this imports the Database class

class SQLite3_Database(Database):

    def create_database(self):
        """
        Creates the SQLite3 database and the table to store the files.
        """
        conn = sqlite3.connect('file_database.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT,
                content TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def add_data(self, filepaths):
        """
        Adds the content of the specified files to the database.
        :param filepaths: List of file paths to add to the database.
        """
        conn = sqlite3.connect('file_database.db')
        cursor = conn.cursor()
        for filepath in filepaths:
            try:
                with open(filepath, 'r', encoding='utf-8') as file:  # Specify utf-8 encoding here
                    content = file.read()
                    filename = os.path.basename(filepath)
                    cursor.execute('INSERT INTO files (filename, content) VALUES (?, ?)', (filename, content))
            except (IOError, OSError) as e:
                print(f"Error reading file {filepath}: {e}")
            except UnicodeDecodeError as e:
                print(f"Error decoding file {filepath}: {e}")
        conn.commit()
        conn.close()

    def extract_data(self, filename, output_directory):
        """
        Extracts a file from the database and saves it to the specified output directory.

        Args:
            filename (str): The name of the file to extract.
            output_directory (str): The directory to save the extracted file.

        Returns:
            str: The path to the extracted file.
        """
        conn = sqlite3.connect('file_database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT content FROM files WHERE filename = ?', (filename,))
        result = cursor.fetchone()
        conn.close()

        if result is None:
            print(f"Error: The file '{filename}' does not exist in the database.")
            return None

        content = result[0]
        if not os.path.exists(output_directory):
            try:
                os.makedirs(output_directory)
            except OSError as e:
                print(f"Error creating directory {output_directory}: {e}")
                return None

        output_path = os.path.join(output_directory, filename)
        try:
            with open(output_path, 'w', encoding='utf-8') as file:  # Specify utf-8 encoding here
                file.write(content)
        except (IOError, OSError) as e:
            print(f"Error writing file {output_path}: {e}")
            return None

        return output_path
