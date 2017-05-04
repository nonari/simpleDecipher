from typing import List, Set

# Class for handling solution alphabet
# Can only handle an [a-z] ASCII alphabet


class Alphabet:

    # Constructor
    # Initializes index lists
    def __init__(self):
        self._solved_words = []
        self._number_of_words = 0
        self._number_of_placed_letters = 0
        self._solved_letters = set()
        self._reverse_solved_letters = set()
        self._solving_index = []
        self._ciphering_index = []
        # Initializes each array with 25 numbers each representing an ASCII letter (a-z)
        for i in range(0, 26):
            self._solving_index.append('?')
            self._ciphering_index.append('?')

    # Method: Returns a self copy
    # Output: Alphabet
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

    # Method: Match c with s
    def match(self, ciphered: str, solved: str) -> None:
        if len(ciphered) != len(solved):
            raise ValueError('Parameters lengths differ')
        self._solved_words.append(solved)
        self._number_of_words += 1

        for i in range(len(ciphered)):
            self._number_of_placed_letters += 1
            self._solved_letters.add(ciphered[i])
            self._reverse_solved_letters.add(solved[i])
            # Convert chars to ASCII code
            c_code = ord(ciphered[i]) - 97
            s_code = ord(solved[i]) - 97
            self._solving_index[c_code] = solved[i]
            self._ciphering_index[s_code] = ciphered[i]

    def match_list(self, ciphered_words: List[str], solved_words: List[str]) -> None:
        for ciphered_word, solved_word in ciphered_words, solved_words:
            self.match(ciphered_word, solved_word)

    # Method: Checks if, for the already solved letters, ciphered word c matches with exp
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

    # Method: Check if the current solution contains all of a ciphered word letters
    def contains(self, word: str) -> bool:
        for c in word:
            if c not in self._solved_letters:
                return False
        return True

    # Method: Deciphers word with the current index state
    def decipher(self, word: str) -> str:
        deciphered_word = ''
        # Matches each char from the input String with a char at the solving_index
        for i in word:
            deciphered_word += self._solving_index[ord(i) - 97]
        return deciphered_word

    # Method: Ciphers word with the current index state
    def cipher(self, word: str) -> str:
        ciphered_word = ''
        # Matches each char from the input String with a char at the ciphering_index
        for i in word:
            ciphered_word += self._ciphering_index[ord(i) - 97]
        return ciphered_word

    # Method: Returns solving index
    def get_solving_index(self) -> List[str]:
        return self._solving_index

    # Method: Returns ciphering index
    def get_ciphering_index(self) -> List[str]:
        return self._ciphering_index

    # Method: Returns already solved chars
    def get_solved_letters(self) -> Set[str]:
        return self._solved_letters

    # Method: Returns already solved chars
    def get_reverse_solved_letters(self) -> Set[str]:
        return self._reverse_solved_letters

    # Method: Returns the number of matched words
    def get_number_of_words(self) -> int:
        return self._number_of_words

    def get_number_of_placed_letters(self) -> int:
        return self._number_of_placed_letters

    def get_solved_words(self) -> List[str]:
        return self._solved_words

    def __str__(self):
        solving_str = 'Solving index: ' + self.get_solving_index().__str__()
        ciphering_str = 'Ciphering index: ' + self.get_ciphering_index().__str__()
        solved_letters_str = '         Solved letters: ' + self.get_solved_letters().__str__()
        reverse_solved_letters_str = "         Reverse solved: " + self.get_reverse_solved_letters().__str__()
        result_str = 'Alphabet {' + solving_str + '\n        ' + ciphering_str + '\n' \
                     + solved_letters_str + '\n' + reverse_solved_letters_str
        return result_str
