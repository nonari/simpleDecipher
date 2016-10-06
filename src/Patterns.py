import importlib

# Class for handling word patterns


class Patterns:

    # Constructor
    # Input: String (Patterns dictionary name in /lib)
    def __init__(self, dic_name):
        # Compose dictionary path
        dic_dir = 'lib.' + dic_name
        # Imports the patterns set
        self._patterns = importlib.import_module(dic_dir).allPatterns

    # Method: Returns a list of matching words for a given word
    # Input: String (Word)
    # Output: List of strings
    def get_matching_words(self, word):
        # Obtain the word pattern
        pattern = self.pattern(word)
        # Search at the pattern dictionary for the pattern
        if pattern in self._patterns:
            # Return list of matching words if found
            return self._patterns[pattern].copy()
        else:
            return []

    # Method: Returns a list of matching words for each given word
    # Input: List of strings (Words)
    # Output: Dic of strings
    def get_matching_words_dic(self, words):
        matching_words_dic = {}
        for word in words:
            matching_list = self.get_matching_words(word)
            if len(matching_list) > 0:
                matching_words_dic[word] = matching_list
        return matching_words_dic

    # Static Method: Builds word pattern
    # Input: String (Word)
    # Output: String (Pattern)
    @staticmethod
    def pattern(word):
        next_num = 0
        letter_set = {}
        word_pattern = []
        for letter in word:
            if letter not in letter_set:
                letter_set[letter] = str(next_num)
                next_num += 1
            word_pattern.append(letter_set[letter])
        return '.'.join(word_pattern)
