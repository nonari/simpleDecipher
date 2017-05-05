import importlib
from typing import Dict, List

# Class for handling word patterns


class Patterns:

    def __init__(self, dict_name: str):
        dict_dir = 'lib.' + dict_name
        self._patterns = importlib.import_module(dict_dir).allPatterns

    # Returns a list of matching words for a given word
    def matching_words(self, word: str) -> List[str]:
        pattern = self.pattern_of(word)
        if pattern in self._patterns:
            return list(self._patterns[pattern])
        else:
            return []

    # Returns a dict of matching words for each given word
    def matching_words_dic(self, words: List[str]) -> Dict[str, str]:
        matching_words_dic = {}
        for word in words:
            matching_list = self.matching_words(word)
            if len(matching_list) > 0:
                matching_words_dic[word] = matching_list
        return matching_words_dic

    @staticmethod
    def pattern_of(word: str) -> str:
        next_num = 0
        letter_set = {}
        word_pattern = []
        for letter in word:
            if letter not in letter_set:
                letter_set[letter] = str(next_num)
                next_num += 1
            word_pattern.append(letter_set[letter])
        return '.'.join(word_pattern)
