from simpledecipher.comparator import Comparator
from simpledecipher.alphabet import Alphabet
from simpledecipher.patterns import Patterns
from simpledecipher.textprocessor import Text
from simpledecipher.dictionary import Dictionary
import simpledecipher.algorithms as algorithms
from simpledecipher.logger import Logger

LOG = Logger.get_logger('test')

class ASD():

    def setUp(self):
        patterns1 = Patterns('spanishPatterns')
        #                 fronteradelosbesosseranmanana
        self.ciphered_text1 = 'deibrwelswkiavwaiaawelbnlblbl'
        self.text1 = Text(self.ciphered_text1)
        possible_words1 = self.text1.extract_words()
        solving_dict1 = patterns1.matching_words_dic(possible_words1)
        self.dictionary1 = Dictionary(solving_dict1)
        # self.alphabet = Alphabet()
        # self.alphabet.match('qwertyuiopasdfghjklzxcvbnm', 'wertyuiopqsdfghjklaxcvbnmz')
        # print(self.alphabet.decipher('deibrwelswkiavwaiaawelbnlblblxylbsiwbklswbrlsyelauwbrlayblenl'))

        patterns2 = Patterns('spanishPatterns')
        #                 cuandoenladentadurasientasunarma
        self.ciphered_text2 = 'xylbsiwbklswbrlsyelauwbrlayblenl'
        self.text2 = Text(self.ciphered_text2)
        possible_words2 = self.text2.extract_words()
        solving_dict2 = patterns2.matching_words_dic(possible_words2)
        self.dictionary2 = Dictionary(solving_dict2)

    def fff(self):
        solutions1 = Alphabet.generate_random_solutions(18000)
        solutions2 = Alphabet.generate_random_solutions(18000)

        result = True
        comparator = Comparator(solutions1, solutions2)

    def test_stats(self):
        self.setUp()
        solutions1 = algorithms.stats(self.text1, self.dictionary1)
        # solved_text = solved_alphabet.decipher('deibrwelswkiavwaiaawelbnlblblxylbsiwbklswbrlsyelauwbrlayblenl')
        LOG.info('@stats-> Soluciones')
        for e in solutions1:
            LOG.info(e.decipher('deibrwelswkiavwaiaawelbnlblbl') + e.goodness().__str__())
        solutions2 = algorithms.stats(self.text2, self.dictionary2)
        # solved_text = solved_alphabet.decipher('deibrwelswkiavwaiaawelbnlblblxylbsiwbklswbrlsyelauwbrlayblenl')
        LOG.info('@stats-> Soluciones')
        for e in solutions2:
            LOG.info(e.decipher('xylbsiwbklswbrlsyelauwbrlayblenl') + e.goodness().__str__())

        comparator = Comparator(solutions2, solutions1)
        best_pair = comparator.best()

        # Optimal separate solutions
        print(best_pair[0].decipher(self.ciphered_text1))
        print(best_pair[1].decipher(self.ciphered_text2))
        for e,i,m in comparator.sort():
            LOG.info(m)
            LOG.info(e.__str__())
            LOG.info(i.__str__())
            LOG.info(i.decipher(self.ciphered_text2))
            LOG.info(e.decipher(self.ciphered_text1))
        # TODO check overlaps

if __name__ == "__main__":
    ASD().test_stats()