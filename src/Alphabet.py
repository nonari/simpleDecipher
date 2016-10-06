

# Class for handling solution alphabet
# Can only handle an [a-z] ASCII alphabet


class Alphabet:

    # Constructor
    # Initializes index lists
    def __init__(self):
        # Number of words matched
        self._number_of_words = 0
        # Set of solved letters (ciphered)
        self._solved_letters = set()
        # Set of reverse solved letters (deciphered)
        self._reverse_solved_letters = set()
        # This index matches: Ciphered -> Solved
        self._solving_index = []
        # Solved -> Ciphered
        self._ciphering_index = []
        # Initializes each array with 25 numbers each representing an ASCII letter (a-z)
        for i in range(0, 26):
            self._solving_index.append(i)
            self._ciphering_index.append(i)

    # Method: Returns a self copy
    # Output: Alphabet
    def copy(self):
        a_clone = Alphabet()
        a_clone._number_of_words = self._number_of_words
        a_clone._solving_index = self._solving_index.copy()
        a_clone._ciphering_index = self._ciphering_index.copy()
        a_clone._solved_letters = self._solved_letters.copy()
        return a_clone

    # Method: Match c with s
    # Input:
    #     c: String (Ciphered)
    #     s: String (Solved for c)
    def match(self, c, s):
        # Check if parameters lengths match
        if len(c) != len(s):
            raise ValueError('Parameters lengths differ')
        # Update matched words counter
        self._number_of_words += 1
        # For each char in the parameters update the indexes
        for i in range(len(c)):
            self._solved_letters.add(c[i])
            self._reverse_solved_letters.add(s[i])
            # Convert chars to ASCII code
            c_code = ord(c[i]) - 97
            s_code = ord(s[i]) - 97
            # Save previous solved letter for c (c -> s')
            temp = self._solving_index[c_code]
            # Update solved letter for c (c -> s)
            self._solving_index[c_code] = s_code
            # Save previous ciphered letter for s (s -> c')
            temp2 = self._ciphering_index[s_code]
            # Update solved letter for c' (c' -> s')
            self._solving_index[temp2] = temp
            # Update solved letter for s' (s' -> c')
            self._ciphering_index[temp] = temp2
            # Update ciphered letter for s (s -> c)
            self._ciphering_index[s_code] = c_code

    def match_list(self, l):
        for words_tuple in l:
            self.match(words_tuple[0], words_tuple[1])

    # Method: Checks if, for the already solved letters, ciphered word c matches with exp
    # Input:
    #     c: String (Ciphered)
    #     exp: String (Expected for c)
    def fits(self, c, exp):
        result = True
        deciphered = self.decipher(c)
        for i in range(len(c)):
            if c[i] in self._solved_letters:
                if deciphered[i] != exp[i]:
                    result = False
                    break
            else:
                if exp[i] in self._reverse_solved_letters:
                    result = False
                    break
        return result

    # Method: Check if the current solution contains all of a ciphered word letters
    # Input: String (Ciphered word)
    # Output: Boolean
    def contains(self, word):
        result = True
        for c in word:
            if c not in self._solved_letters:
                result = False
                break
        return result

    # Method: Deciphers word with the current index state
    # Input: String
    # Output: String
    def decipher(self, w):
        deciphered_word = ''
        # Matches each char from the input String with a char at the solving_index
        for i in w:
            deciphered_word += chr(self._solving_index[ord(i) - 97] + 97)
        return deciphered_word

    # Method: Ciphers word with the current index state
    # Input: String
    # Output: String
    def cipher(self, w):
        ciphered_word = ''
        # Matches each char from the input String with a char at the ciphering_index
        for i in w:
            ciphered_word += chr(self._ciphering_index[ord(i) - 97] + 97)
        return ciphered_word

    # Method: Returns solving index
    # Output: List of Chars
    def get_solving_index(self):
        solving_chars_idx = []
        # Converts the internal representation into Chars
        for i in range(0, 26):
            solving_chars_idx.append(chr(self._solving_index[i] + 97))
        return solving_chars_idx

    # Method: Returns ciphering index
    # Output: List of Chars
    def get_ciphering_index(self):
        ciphering_chars_idx = []
        # Converts the internal representation into Chars
        for i in range(0, 26):
            ciphering_chars_idx.append(chr(self._ciphering_index[i] + 97))
        return ciphering_chars_idx

    # Method: Returns already solved chars
    # Output: Set of Chars
    def get_solved_letters(self):
        return self._solved_letters

    # Method: Returns the number of matched words
    # Output: Integer
    def get_number_of_words(self):
        return self._number_of_words

    # Method: Checks if this alphabet is a superset of a given one
    # Input: Alphabet
    # Output: Boolean
    def is_superset(self, a):
        result = True
        for i in a._solved_letters:
            if (a.decipher(i) != self.decipher(i)) and (i in self._solved_letters):
                result = False
                break
        return result

    # Method: Prints the indexes
    # Output: String
    def __str__(self):
        solving_str = 'Solving index: ' + self.get_solving_index().__str__()
        ciphering_str = 'Ciphering index: ' + self.get_ciphering_index().__str__()
        result_str = solving_str + '\n' + ciphering_str
        return result_str
