from typing import List, Set
import random

# Class for handling solution alphabet
# Can only handle an [a-z] ASCII alphabet


class Alphabet:

    def __init__(self):
        self._solved_words = []
        self._number_of_words = 0
        self._number_of_placed_letters = 0
        self._solved_letters = set()
        self._reverse_solved_letters = set()
        self._solving_index = []
        self._ciphering_index = []

        for i in range(0, 26):
            self._solving_index.append('?')
            self._ciphering_index.append('?')

    def __deepcopy__(self):
        clone = Alphabet()
        clone._number_of_words = self._number_of_words
        clone._solving_index = self._solving_index.copy()
        clone._ciphering_index = self._ciphering_index.copy()
        clone._solved_letters = self._solved_letters.copy()
        clone._reverse_solved_letters = self._reverse_solved_letters.copy()
        clone._number_of_placed_letters = self._number_of_placed_letters
        clone._solved_words = self._solved_words.copy()
        return clone

    # Matches ciphered letter with solved
    def match(self, ciphered: str, solved: str) -> None:
        if len(ciphered) != len(solved):
            raise ValueError('Parameters lengths differ')

        if len(ciphered) > 4:
            self._solved_words.append(solved)
            self._number_of_words += 1

        for i in range(len(ciphered)):
            self._number_of_placed_letters += 1
            self._solved_letters.add(ciphered[i])
            self._reverse_solved_letters.add(solved[i])

            c_code = ord(ciphered[i]) - 97
            s_code = ord(solved[i]) - 97
            self._solving_index[c_code] = solved[i]
            self._ciphering_index[s_code] = ciphered[i]

    def match_list(self, ciphered_words: List[str], solved_words: List[str]) -> None:
        for ciphered_word, solved_word in ciphered_words, solved_words:
            self.match(ciphered_word, solved_word)

    # Checks if, for the already solved letters, ciphered word c matches with exp
    def fits(self, ciphered: str, expected: str) -> bool:
        deciphered = self.decipher(ciphered)
        for i in range(len(ciphered)):
            if ciphered[i] in self._solved_letters:
                if deciphered[i] != expected[i]:
                    return False
            else:
                if expected[i] in self._reverse_solved_letters:
                    return False
        return True

    # Check if the current solution contains all of a ciphered word letters
    def contains(self, word: str) -> bool:
        for letter in word:
            if letter not in self._solved_letters:
                return False
        return True

    # Deciphers word with the current index state
    def decipher(self, word: str) -> str:
        deciphered_word = ''
        for letter in word:
            deciphered_word += self._solving_index[ord(letter) - 97]
        return deciphered_word

    # Ciphers word with the current index state
    def cipher(self, word: str) -> str:
        ciphered_word = ''
        for letter in word:
            ciphered_word += self._ciphering_index[ord(letter) - 97]
        return ciphered_word

    def goodness(self) -> float:
        # TODO improve this shit
        if self._solved_letters.__len__() == 0 or self._number_of_words == 0:
            return 0
        else:
            return (self.get_number_of_placed_letters() / self.get_number_of_words()) * self._solved_letters.__len__()

    def merge(self, solution: 'Alphabet') -> None:
        for ciphered in solution.get_solved_letters():
            self.match(ciphered, solution.decipher(ciphered))

    @staticmethod
    def generate_abc_list() -> List[str]:
        abc = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
               'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        return abc.copy()

    @staticmethod
    def generate_random_solution() -> 'Alphabet':
        alphabet = Alphabet()
        ciphering_abc = Alphabet.generate_abc_list()
        solving_abc = Alphabet.generate_abc_list()

        lasting_letters = 25
        for n in range(random.randint(1, 26)):
            ciphered_letter_idx = random.randint(0, lasting_letters)
            solved_letter_idx = random.randint(0, lasting_letters)

            ciphered_letter = ciphering_abc.pop(ciphered_letter_idx)
            solved_letter = solving_abc.pop(solved_letter_idx)

            alphabet.match(ciphered_letter, solved_letter)

            lasting_letters -= 1
        return alphabet

    @staticmethod
    def generate_random_solutions(n) -> List['Alphabet']:
        alphabet_list = []
        for i in range(n):
            alphabet_list.append(Alphabet.generate_random_solution())
        return alphabet_list

    def get_solving_index(self) -> List[str]:
        return self._solving_index

    def get_ciphering_index(self) -> List[str]:
        return self._ciphering_index

    def get_solved_letters(self) -> Set[str]:
        return self._solved_letters

    def get_reverse_solved_letters(self) -> Set[str]:
        return self._reverse_solved_letters

    def get_number_of_words(self) -> int:
        return self._number_of_words

    def get_number_of_placed_letters(self) -> int:
        return self._number_of_placed_letters

    def get_solved_words(self) -> List[str]:
        return self._solved_words

    def __str__(self):
        solving_str = 'Solving index: ' + self.get_solving_index().__str__()
        ciphering_str = 'Ciphering index: ' + self.get_ciphering_index().__str__()
        solved_letters_str = 'Solved letters: ' + self.get_solved_letters().__str__()
        reverse_solved_letters_str = "Reverse solved: " + self.get_reverse_solved_letters().__str__()
        result_str = 'Alphabet: {' + solving_str + '\n' + ciphering_str + '\n' \
                     + solved_letters_str + '\n' + reverse_solved_letters_str
        return result_str
