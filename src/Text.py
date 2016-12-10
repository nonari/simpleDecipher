import unicodedata

# Class for handling ciphered text processing


class Text:

    # Constructor
    # Input: String (Ciphered text)
    def __init__(self, text):
        self._text = text
        # Defaults the space symbol to ' '
        self._space_symbol = ''

    # Method: Sets the space symbol equivalence
    # Input: Char
    def set_space(self, symbol):
        self._space_symbol = symbol

    # Static method: Converts ASCII bytes to string
    @staticmethod
    def _ascii_bytes_to_str(ascii_text):
        string = ''
        for i in ascii_text:
            string += chr(i)
        return string

    @staticmethod
    # Static method: Remove grouped spaces
    def _remove_grouped_spaces(text):
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

    # Method: Convert non [a-z] symbols
    def normalize_text(self):
        # Normalize non ASCII characters, returns bytes
        self._text = unicodedata.normalize('NFKD', self._text).encode('ascii', 'ignore')
        # Lower case text
        # self._text = self._text.lower()
        # Convert bytes from the normalizer to string
        self._text = self._ascii_bytes_to_str(self._text)
        # Erase grouped spaces
        self._text = self._remove_grouped_spaces(self._text)

    # Method: Convert non [a-z] symbols in key
    def normalize_key(self):
        keys = set()
        # Add all symbols to keys set
        for char in self._text:
            if char != ' ':
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

    # Method: Remove . , :
    def remove_stops(self):
        self._text = self._text.replace(',', ' ')
        self._text = self._text.replace('.', ' ')
        self._text = self._text.replace(':', ' ')
        self._text = self._text.replace(';', ' ')
        # Erase grouped spaces
        self._text = self._remove_grouped_spaces(self._text)

    # Method: Check there are no more than 26 symbols
    # Output: Set
    def check_symbols(self):
        symbols = set()
        for char in self._text:
            symbols.add(char)
        return symbols

    # Method: Reduces key length to one
    # Output: String: If key is found: reduced text
    #                 If key not found: void string
    def reduce_key(self):
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
                    break
            # If there are less than 27 symbols, key is found
            if key.__len__() < 27:
                break
        # If loops finish with a bad key, return void string
        if key_len > 27:
            return ''
        # If key is found, reduce text
        else:
            pos = 0
            # Replace each occurrence of the keys with a single symbol
            for i in range(int(len(self._text) / key_len)):
                reduced_text += key[self._text[pos:pos + key_len]]
                pos += key_len
            self._text = reduced_text
            return reduced_text

    # Method: Replace each occurrence of the space symbol by an actual space
    def space_text(self):
        text = ''
        for char in self._text:
            if char == self._space_symbol:
                text += ' '
        self._text = text

    # Method: Extract possible words
    # Output: List of Strings
    def extract_words(self):
        if self._space_symbol == ' ':
            words = []
            for word in self._text.split(' '):
                if len(word) > 5:
                    words.append(word)
        else:
            words = []
            for i in range(5, 15):
                offset = 0
                for j in range(int(len(self._text) / i)):
                    words.append(self._text[offset:offset + i])
                    offset += i
        return words

    # Method: Return list of words split by space symbol
    # Output: List of strings
    def split_text(self):
        words = self._text.split(self._space_symbol)
        return words

    # Method: Returns the text letters ordered by the most common ones
    # Output: List of chars
    def letter_stats(self):
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

    # Method: Replace spaces by a ciphered character
    def cipher_spaces(self):
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
    def trim(self, **kwargs):
        ini = 0
        fin = len(self._text)
        if 'ini' in kwargs:
            ini = int(kwargs['ini'])
            if ini < 0 or ini > len(self._text) or fin < ini or fin > len(self._text):
                raise UnboundLocalError
        if 'fin' in kwargs:
            fin = int(kwargs['fin'])
        self._text = self._text[ini:fin]

    # Method: Return text
    # Output: String
    def get_text(self):
        return self._text