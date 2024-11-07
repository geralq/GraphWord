import os
import nltk
from nltk.corpus import stopwords
from collections import Counter


class TextAnalyzer:
    def __init__(self, filename):
        """
        Initializes the class with the filename and loads its content.

        Args:
            filename (str): Path to the text file.
        """
        self.filename = filename
        self.text = self._load_text_file(filename)

    def _load_text_file(self, filename):
        """
        Loads a text file and returns its content as a string.

        Args:
            filename (str): Path to the text file.

        Returns:
            str: Content of the text file.
        """
        if not os.path.isfile(filename):
            print(f"Error: The file '{filename}' does not exist.")
            return ''
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                text = file.read()
        except UnicodeDecodeError:
            try:
                with open(filename, 'r', encoding='latin-1') as file:
                    text = file.read()
            except Exception as e:
                print(f"Error: Could not read the file: {e}")
                return ''
        except Exception as e:
            print(f"Error: Could not read the file: {e}")
            return ''
        return text

    def _clean_text(self, text=None):
        """
        Cleans the text by converting it to lowercase and removing non-alphabetic characters.
        This is a private function and should not be called directly outside the class.

        Args:
            text (str, optional): Text to clean. If not provided, the loaded text will be cleaned.

        Returns:
            str: Cleaned text.
        """
        if text is None:
            text = self.text
        lowered_text = text.lower()
        cleaned_text = ''.join(char if char.isalpha() or char.isspace() else ' ' for char in lowered_text)
        return cleaned_text

    def extract_n_letter_vocabulary(self, n):
        """
        Extracts a vocabulary of words of length 'n' from the text and counts their occurrences.

        Args:
            n (int): Length of the words to extract.

        Returns:
            Counter: Counter object with the words of length 'n' as keys and their occurrences as values.
        """
        text = self._clean_text()
        words = nltk.word_tokenize(text)
        stop_words = set(stopwords.words('english'))
        n_letter_words = [word for word in words if len(word) == n]

        # Filters the words by removing stopwords and those with repeated characters
        n_letter_words_without_stopwords = [word for word in n_letter_words if
                                            word not in stop_words and len(set(word)) > 1]

        return Counter(n_letter_words_without_stopwords)
