import copy
import time
from typing import List
from src.Alphabet import Alphabet

# Class for handling possible words in spaced texts


class Dictionary:

    def __init__(self, d: dict):
        self._d = d

    def copy(self):
        new_dictionary = Dictionary({})
        new_dictionary._d = copy.deepcopy(self._d)
        return new_dictionary

    # Method: Leave only fitting possibles and remove non possible keys
    # Input: Alphabet
    def filter(self, alphabet: Alphabet) -> None:
        t1 = time.time()
        # Notice that the .keys method returns a dict_keys object still pointing to the dict
        for ciphered in list(self._d.keys()):
            # If word is contained in the solution, remove it
            if alphabet.contains(ciphered):
                self._d.pop(ciphered)
                continue
            # For each possible word
            possibles = list(self._d[ciphered])
            for possible in possibles:
                # If the possible word doesn't fits the current solution
                if not alphabet.fits(ciphered, possible):
                    # Remove the word
                    self._d[ciphered].remove(possible)
            # If there are no possible words remaining
            if len(self._d[ciphered]) == 0:
                # Remove it from the dict
                self._d.pop(ciphered)
        t = time.time() - t1
        # print('Filtered in ' + t.__str__() + ' ms')

    # Method: Returns the single solution words
    def uniques(self) -> List[str]:
        unique_words = []
        for ciphered in self._d:
            if len(self._d[ciphered]) == 1:
                unique_words.append(ciphered)
        unique_words.sort()
        return unique_words

    # Method: Removes a word from the dict keys
    def remove_key(self, key: str):
        self._d.pop(key)

    # Method: Returns the possible solutions for a ciphered word
    def solutions(self, key: str):
        return list(self._d[key])

    # Method: Returns the internal dict
    def get_dict(self):
        return self._d

    # Method: Adds a new entry to the dict
    def push_entry(self, key: str, possibles: List[str]):
        self._d[key] = possibles

    # Method: Returns the dictionary keys
    def keys(self) -> List[str]:
        return list(self._d.keys())

    # Method: Returns dictionary size in words
    def __sizeof__(self):
        size = 0
        for c in self._d:
            size += len(self._d[c])
        return size
