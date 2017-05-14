from typing import List, Dict, Tuple

# Class for comparing two lists of solution Alphabets
from src.Alphabet import Alphabet


class Comparator:

    def __init__(self, solutions1: List[Alphabet], solutions2: List[Alphabet]):
        self._solutions1 = solutions1
        self._solutions2 = solutions2
        self._left_list = []
        self._right_index = {}
        self.init_index()
        self.populate_index()
        self.populate_left()
        self.compare()

    def init_index(self) -> None:
        for i in range(97, 123):
            for j in range(97, 123):
                ciphered = chr(i)
                solved = chr(j)
                self._right_index[(ciphered, solved)] = []

    def populate_index(self) -> None:
        for alphabet in self._solutions1:
            for ciphered in alphabet.get_solved_letters():
                solved = alphabet.decipher(ciphered)
                self._right_index[(ciphered, solved)].append(alphabet)

    def populate_left(self):
        for alphabet in self._solutions2:
            self._left_list.append((alphabet, {}))

    def compare(self) -> None:
        for (l_alphabet, matching_index) in self._left_list:
            for ciphered in l_alphabet.get_solved_letters():
                deciphered = l_alphabet.decipher(ciphered)
                for r_alphabet in self._right_index[(ciphered, deciphered)]:
                    if r_alphabet in matching_index:
                        solution_matches = matching_index[r_alphabet]
                        matching_index[r_alphabet] = solution_matches + 1
                    else:
                        matching_index[r_alphabet] = 1

    def get_solution_pairs(self) -> List[Tuple[Alphabet, Dict[Alphabet, int]]]:
        return self._left_list
