from simpledecipher.comparator import Comparator
from simpledecipher.alphabet import Alphabet
from simpledecipher.patterns import Patterns
from simpledecipher.textprocessor import Text
from simpledecipher.dictionary import Dictionary
import simpledecipher.algorithms as algorithms

class ASD():

    def setUp(self):
        patterns = Patterns('spanishPatterns')
        # fronteradelosbesosseranmananacuandoenladentadurasientasunarma
        ciphered_text = 'deibrwelswkiavwaiaawelbnlblblxylbsiwbklswbrlsyelauwbrlayblenl'
        self.text = Text(ciphered_text)
        possible_words = self.text.extract_words()
        solving_dict = patterns.matching_words_dic(possible_words)
        self.dictionary = Dictionary(solving_dict)
        self.alphabet = Alphabet()
        self.alphabet.match('qwertyuiopasdfghjklzxcvbnm', 'wertyuiopqsdfghjklaxcvbnmz')
        print(self.alphabet.decipher('deibrwelswkiavwaiaawelbnlblblxylbsiwbklswbrlsyelauwbrlayblenl'))


    def test_stats(self):
        self.setUp()
        solutions = algorithms.stats(self.text, self.dictionary)
        # solved_text = solved_alphabet.decipher('deibrwelswkiavwaiaawelbnlblblxylbsiwbklswbrlsyelauwbrlayblenl')
        print(solutions)
        for e in solutions:
            print(e.decipher('deibrwelswkiavwaiaawelbnlblblxylbsiwbklswbrlsyelauwbrlayblenl') +
                  " " + e.get_number_of_placed_letters().__str__() + " " + e.get_number_of_words().__str__() + " " +
                  e.get_solved_words().__str__())

if __name__ == "__main__":
    ASD().test_stats()