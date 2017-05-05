import copy
import time
from typing import List
from src.Alphabet import Alphabet

# Class for handling possible words in spaced texts


class Dictionary:

    def __init__(self, d: dict):
        self._d = d

    def __deepcopy__(self):
        new_dictionary = Dictionary({})
        new_dictionary._d = copy.deepcopy(self._d)
        return new_dictionary

    # Leave only fitting possibles and remove non possible keys
    def filter(self, alphabet: Alphabet) -> None:
        t1 = time.time()
        for ciphered in list(self._d.keys()):
            if alphabet.contains(ciphered):
                self._d.pop(ciphered)
                continue
            possibles = list(self._d[ciphered])
            for possible in possibles:
                if not alphabet.fits(ciphered, possible):
                    self._d[ciphered].remove(possible)
            if len(self._d[ciphered]) == 0:
                self._d.pop(ciphered)
        t = time.time() - t1
        print('Filtered in ' + t.__str__() + ' ms')

    # Returns the single solution words
    def uniques(self) -> List[str]:
        unique_words = []
        for ciphered in self._d:
            if len(self._d[ciphered]) == 1:
                unique_words.append(ciphered)
        unique_words.sort()
        return unique_words

    def remove_key(self, key: str) -> None:
        self._d.pop(key)

    # Returns the possible solutions for a ciphered word
    def solutions(self, ciphered: str) -> List[str]:
        return list(self._d[ciphered])

    def get_dict(self) -> dict:
        return self._d

    def push_entry(self, key: str, possibles: List[str]) -> None:
        self._d[key] = possibles

    def keys(self) -> List[str]:
        return list(self._d.keys())

    # Returns dictionary size in words
    def __sizeof__(self):
        size = 0
        for c in self._d:
            size += len(self._d[c])
        return size
