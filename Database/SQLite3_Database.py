from Database import Database
import sqlite3


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
            with open(filepath, 'r') as file:
                content = file.read()
                filename = os.path.basename(filepath)
                cursor.execute('INSERT INTO files (filename, content) VALUES (?, ?)', (filename, content))
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
        output_path = os.path.join(output_directory, filename)
        with open(output_path, 'w') as file:
            file.write(content)

        return output_path
