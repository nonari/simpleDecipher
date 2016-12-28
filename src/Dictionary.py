import copy
import time

# Class for handling possible words in spaced texts


class Dictionary:

    def __init__(self, d: dict):
        self._d = d

    def copy(self):
        s = Dictionary({})
        s._d = copy.deepcopy(self._d)
        return s

    # Method: Leave only fitting possibles and remove non possible keys
    # Input: Alphabet
    def filter(self, alphabet):
        t1 = time.time()
        # Notice that the .keys method returns a dict_keys object still pointing to the dict
        for ciphered in self._d:
            # If word is contained in the solution, remove it
            if alphabet.contains(ciphered):
                self._d.pop(ciphered)
                continue
            # For each possible word
            for possible in list(self._d[ciphered]):
                # If the possible word doesn't fits the current solution
                if not alphabet.fits(ciphered, possible):
                    # Remove the word
                    self._d[ciphered].remove_key(possible)
            # If there are no possible words remaining
            if len(self._d[ciphered]) == 0:
                # Remove it from the dict
                self._d.pop(ciphered)
        t = time.time() - t1
        print(t)

    # Method: Returns the single solution words
    # Output: List
    def uniques(self):
        unique_words = []
        for word in self._d:
            if (len(self._d[word]) == 1) & (len(word) > 4):
                unique_words.append(word)
        unique_words.sort()
        return unique_words

    # Method: Removes a word from the possible words list
    # Input:
    #       key: String (Ciphered word)
    #       word: String (Possible word)
    def remove_key(self, key, word):
        self._d[key].remove_key(word)

    # Method: Removes a word from the dict keys
    # Input: String (Ciphered word)
    def remove_possible(self, key):
        self._d.pop(key)

    # Method: Returns the possible solutions for a ciphered word
    # Input: String (Ciphered word)
    # Output: Non-bonded List
    def get(self, key):
        return list(self._d[key])

    # Method: Returns the internal dict
    # Output: Non-bonded dict
    def get_dict(self):
        return copy.deepcopy(self._d)

    # Method: Adds a new entry to the dict
    # Input:
    #       key: String (Ciphered word)
    #       possibles: List (Possible words)
    def set(self, key, possibles: list):
        self._d[key] = possibles

    # Method: Returns the dictionary keys
    # Output: Non-bonded List
    def keys(self):
        return list(self._d.keys())

    # Method: Returns dictionary size in words
    # Output: Integer
    def __sizeof__(self):
        size = 0
        for c in self._d:
            size += len(self._d[c])
        return size
