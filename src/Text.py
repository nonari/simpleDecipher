import unicodedata
from typing import List, Tuple, Set

# Class for handling ciphered text processing


class Text:

    def __init__(self, text: str):
        self._text = text
        self._space_symbol = None

    def set_space(self, symbol: str) -> None:
        self._space_symbol = symbol

    @staticmethod
    def _ascii_bytes_to_str(ascii_text: bytes) -> str:
        string = ''
        for i in ascii_text:
            string += chr(i)
        return string

    @staticmethod
    def _remove_grouped_spaces(text: str) -> str:
        was_space = False
        filtered_text = ''
        for char in text:
            if ord(char) == 32:
                if not was_space:
                    filtered_text += ' '
                was_space = True
            else:
                was_space = False
                filtered_text += char
        return filtered_text

    # Convert non [a-z] symbols
    def normalize_text(self) -> None:
        # Normalize non ASCII characters, returns bytes
        normalized_text = unicodedata.normalize('NFKD', self._text).encode('ascii', 'ignore')
        # Lower case text
        # self._text = self._text.lower()
        self._text = self._ascii_bytes_to_str(normalized_text)
        self._text = self._remove_grouped_spaces(self._text)

    # Convert non [a-z] symbols in key
    def normalize_key(self) -> None:
        keys = set()
        for char in self._text:
            if char != self._space_symbol:
                keys.add(char)
        # If key is non [a-z] replace it by a symbol not already in keys
        # Sort keys for a deterministic behaviour when replacing the non [a-z] key
        keys_list = list(keys)
        keys_list.sort()
        for key in keys_list:
            if ord(key) < 96:
                # Remove the non [a-z] symbol
                keys.remove(key)
                # Search for an [a-z] symbol not in keys
                for code in range(97, 123):
                    char = chr(code)
                    if char not in keys:
                        keys.add(char)
                        # Replace the symbol by the new one
                        self._text = self._text.replace(key, char)
                        break

    # Remove . , : ;
    def remove_stops(self) -> None:
        self._text = self._text.replace(',', ' ')
        self._text = self._text.replace('.', ' ')
        self._text = self._text.replace(':', ' ')
        self._text = self._text.replace(';', ' ')
        self._text = self._remove_grouped_spaces(self._text)

    # Returns the set of text symbols
    def check_symbols(self) -> Set[str]:
        symbols = set()
        for char in self._text:
            symbols.add(char)
        return symbols

    # Reduces key length to one
    def reduce_key(self) -> bool:
        reduced_text = ''
        key = {}
        key_len = 0
        # Check a range of key lengths
        for key_len in range(2, 60):
            key = {}
            pos = 0
            next_char = 0
            for i in range(int(len(self._text) / key_len)):
                if self._text[pos:pos + key_len] not in key:
                    key[self._text[pos:pos + key_len]] = chr(next_char + 97)
                    next_char += 1
                pos += key_len
                # If there are more than 27 symbols in key check next length
                if key.__len__() > 27:
                    # TODO spurious solutions?
                    break
            # If there are less than 27 symbols, key is found
            if key.__len__() < 27:
                break
        # If loops finish with a bad key, return void string
        if key_len > 27:
            return False
        # If key is found, reduce text
        else:
            pos = 0
            # Replace each occurrence of the keys with a single symbol
            for i in range(int(len(self._text) / key_len)):
                reduced_text += key[self._text[pos:pos + key_len]]
                pos += key_len
            self._text = reduced_text
            return True

    # Replace each occurrence of the space symbol by an actual space
    def space_text(self) -> None:
        text = ''
        for char in self._text:
            if char == self._space_symbol:
                text += ' '
        self._text = text

    # Extract possible words
    def extract_words(self) -> List[str]:
        if self._space_symbol is not None:
            words = []
            for word in self._text.split(self._space_symbol):
                if len(word) > 5:
                    words.append(word)
        else:
            words = []
            text_length = self._text.__len__()
            max_word_len = 15
            upper_limit = max_word_len if text_length > max_word_len else text_length
            for i in range(5, upper_limit + 1):
                offset = 0
                for j in range(text_length - i + 1):
                    words.append(self._text[offset:offset + i])
                    offset += 1
        return words

    # Return list of words split by space symbol
    def split_text(self) -> List[str]:
        words = self._text.split(self._space_symbol)
        return words

    # Returns the text letters ordered by the most common ones
    def letter_stats(self) -> List[Tuple[str, int]]:
        s = list(self.check_symbols())
        s.sort()
        n = 0
        l = []
        for letter in s:
            for c in self.get_text():
                if letter == c:
                    n += 1
            l.append((letter, n))
            n = 0
        l.sort(key=lambda t: t[1], reverse=True)
        return l

    # Replace spaces by a ciphered character
    def cipher_spaces(self) -> None:
        s = set()
        for letter in self._text:
            s.add(letter)
        for code in range(97, 123):
            if chr(code) not in s:
                self._text.replace(' ', chr(code))
                break

    # Method: Trim text
    # Input:
    #     ini: Int
    #     fin: Int
    # Output: String
    def trim(self, **kwargs) -> None:
        ini = 0
        fin = len(self._text)
        if 'ini' in kwargs:
            ini = int(kwargs['ini'])
            if ini < 0 or ini > len(self._text) or fin < ini or fin > len(self._text):
                raise UnboundLocalError
        if 'fin' in kwargs:
            fin = int(kwargs['fin'])
        self._text = self._text[ini:fin]

    def get_text(self):
        return self._text
