import copy
import time

# Class for handling possible words in spaced texts


class Dictionary:

    def __init__(self, d: dict, index):
        self._d = d
        self._idx = index
        self._used = False
        self._index = {}
        # Index keys are tuples of (c,s) letters, being that the association
        # between a ciphered letter c and a solved letter d
        # Each entry of the index has a tuple of (c_word, p_word), being c_word the ciphered word and p_word
        # the possible word that matches the relation between the letters at the corresponding index key
        if index:
            for l1 in range(97, 123):
                for l2 in range(97, 123):
                    self._index[(chr(l1), chr(l2))] = []
            for ciphered in d:
                for possible in d[ciphered]:
                    for pos in range(len(ciphered)):
                        c_letter = ciphered[pos]
                        p_letter = possible[pos]
                        # bisect.insort_left(self._index[(c_letter, p_letter)], (ciphered, possible))
                        self._index[(c_letter, p_letter)].insert(0, (ciphered, possible))
            for t in self._index:
                self._index[t] = list(set(self._index[t]))
                self._index[t].sort()

    def copy(self):
        s = Dictionary({}, False)
        if not self._used:
            s._index = self._index
            s._d = self._d
        else:
            s._d = copy.deepcopy(self._d)
            s._used = True
        return s

    def filter(self, a):
        if not self._used:
            self.filter_v2(a)
            self._used = True
        else:
            self.filter_v1(a)

    def filter_v2(self, alphabet):
        t1 = time.time()
        self._d = {}
        # For each solved letter in alphabet
        l = []
        for letter in alphabet.get_solved_letters():
            # For each words tuple in index that matches the solution
            for words_tuple in self._index[(letter, alphabet.decipher(letter))]:
                l.insert(0, words_tuple)
        l = list(set(l))
        for words_tuple in l:
            if alphabet.fits(words_tuple[0], words_tuple[1]):
                if not alphabet.contains(words_tuple[0]):
                    # Add the word to the new dictionary
                    if words_tuple[0] not in self._d:
                        self._d[words_tuple[0]] = []
                    self._d[words_tuple[0]].insert(0, words_tuple[1])
        for ciphered in self._d.keys():
            self._d[ciphered].sort()
        t = time.time() - t1
        print(t)

    # Method: Leave only fitting possibles and remove non possible keys
    # Input: Alphabet
    def filter_v1(self, alphabet):
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
                    self._d[ciphered].remove(possible)
            # If there are no possible words remaining
            if len(self._d[ciphered]) == 0:
                # Remove it from the dict
                self._d.pop(ciphered)
        t = time.time() - t1
        if not self._used:
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
    def remove(self, key, word):
        self._used = True
        self._d[key].remove(word)

    # Method: Removes a word from the dict keys
    # Input: String (Ciphered word)
    def pop(self, key):
        self._used = True
        self._d.pop(key)

    # Method: Returns the possible solutions for a ciphered word
    # Input: String (Ciphered word)
    # Output: Non-bonded List
    def get(self, key):
        return list(self._d[key])

    # Method: Adds a new entry to the dict
    # Input:
    #       key: String (Ciphered word)
    #       possibles: List (Possible words)
    def set(self, key, possibles: list):
        self._used = True
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
