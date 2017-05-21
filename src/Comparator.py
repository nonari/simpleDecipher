from typing import List, Dict, Tuple
from src.Alphabet import Alphabet

# Class for comparing two lists of solution Alphabets


class Comparator:
    def __init__(self, solutions1: List[Alphabet], solutions2: List[Alphabet]):
        self._solutions1 = solutions1
        self._solutions2 = solutions2
        self._left_list = []
        self._right_index = {}

        # Init index
        for i in range(97, 123):
            for j in range(97, 123):
                ciphered = chr(i)
                solved = chr(j)
                self._right_index[(ciphered, solved)] = []

        # Populate index
        for alphabet in self._solutions1:
            for ciphered in alphabet.get_solved_letters():
                solved = alphabet.decipher(ciphered)
                self._right_index[(ciphered, solved)].append(alphabet)

        # Populate list
        for alphabet in self._solutions2:
            self._left_list.append((alphabet, {}))

        # Compare
        for l_alphabet, matching_index in self.get_solution_pairs():
            for ciphered in l_alphabet.get_solved_letters():
                deciphered = l_alphabet.decipher(ciphered)
                for r_alphabet in self._right_index[(ciphered, deciphered)]:
                    if r_alphabet in matching_index:
                        solution_matches = matching_index[r_alphabet]
                        matching_index[r_alphabet] = solution_matches + 1
                    else:
                        matching_index[r_alphabet] = 1

    # FIXME
    def sort(self, limit: int=5) -> List[Tuple[Alphabet, Alphabet]]:
        ordered_solutions = []
        for solution1, index in self.get_solution_pairs():
            for solution2 in index:
                matches = index[solution2]
                if matches > limit:
                    heuristic_result = solution1.goodness() + solution2.goodness()
                    ordered_solutions.append((solution1, solution2, matches, heuristic_result))
        result = []
        ordered_solutions.sort(key=lambda t: (t[2], t[3]))
        for (solution1, solution2, _, _) in ordered_solutions:
            result.append((solution1, solution2))
        return result

    def best(self) -> Tuple[Alphabet, Alphabet]:
        max_matches = 0
        best_left = Alphabet()
        best_right = Alphabet()
        for solution1, index in self.get_solution_pairs():
            for solution2 in index:

                bigger = index[solution2] >= max_matches
                # TODO should use goodness()
                better_left = solution1.get_solved_letters().__len__() > best_left.get_solved_letters().__len__()
                better_right = solution2.get_solved_letters().__len__() > best_right.get_solved_letters().__len__()

                if bigger and (better_left or better_right):
                    max_matches = index[solution2]
                    best_right = solution2
                    best_left = solution1
        return best_left, best_right

    def get_solution_pairs(self) -> List[Tuple[Alphabet, Dict[Alphabet, int]]]:
        return self._left_list
