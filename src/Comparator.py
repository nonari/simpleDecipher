from typing import List

# Class for comparing two lists of solution Alphabets
import Alphabet


class Comparator:


    def __init__(self, solutions1: List[Alphabet], solutions2: List[Alphabet]):
        self._matching_index = {}
        self._solutions1 = solutions1
        self._solutions2 = solutions2
        self._left_list = []
        self.__initIndex()
        self.__populateIndex()
        self.__populateLeft()

    def __initIndex(self):
        for i in range(27):
            for j in range(27):
                ciphered = chr(i)
                solved = chr(j)
                self._matching_index[(ciphered, solved)] = []

    def __populateIndex(self):
        for alphabet in self._solutions2:
            for ciphered in alphabet.get_solved_letters():
                solved = alphabet.decipher(ciphered)
                self._matching_index[(ciphered, solved)].append(alphabet)

    def __populateLeft(self):
        for alphabet in self._solutions2:
            self._left_list.append((alphabet,[]))

    def compare(self):
        for alphabet in self._solutions1:
            for ciphered in alphabet.get_solved_letters():
                deciphered = alphabet.decipher(ciphered)
