import unittest

from builtins import print

from src.Alphabet import Alphabet
from src.Patterns import Patterns
from src.Text import Text
from src.Dictionary import Dictionary
# import cProfile


class AlphabetTest(unittest.TestCase):

    def setUp(self):
        self.alphabet = Alphabet()

    def test_match(self):
        alphabet = self.alphabet
        alphabet.match("t", "a")
        alphabet.match("t", "b")
        alphabet.match("b", "a")
        alphabet.match("a", "j")
        alphabet.match("r", "q")
        alphabet.match("r", "y")
        exp_solving_idx = ['j', 'a', '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', '?', '?',
                            'y', '?', 'b', '?', '?', '?', '?', '?', '?']
        exp_ciphering_idx = ['b', 't', '?', '?', '?', '?', '?', '?', '?', 'a', '?', '?', '?', '?', '?', '?', 'r',
                             '?', '?', '?', '?', '?', '?', '?', 'r', '?']
        self.assertListEqual(exp_solving_idx, alphabet.get_solving_index())
        self.assertListEqual(exp_ciphering_idx, alphabet.get_ciphering_index())

    def test_contains(self):
        self.alphabet.match("bdbxihbkkwlb", "abacogalleta")
        self.assertTrue(self.alphabet.contains("xihikki"))

    def test_new(self):
        self.alphabet.match("t", "a")
        print(self.alphabet.get_solving_index())

    # def cont(self):
    #     for i in range(10000000):
    #         self.a.contains("xihikki")

    # def test_speed(self):
    #     c = 'abnxhdyemricousd'
    #     s = 'ajduethrncmxlapq'
    #     b = 'yemricoqhdsl'
    #     self.a.match(c, s)
    #     pr = cProfile.Profile()
    #     pr.enable()
    #     pr.runcall(self.cont)
    #     pr.disable()
    #     pr.print_stats()

    def test_decipher(self):
        ciphered = 'vwjw'
        ciphered_2 = 'wxwpyva'
        exp_deciphered = 'casa'
        exp_deciphered_2 = 'apatico'
        self.alphabet.match(ciphered, exp_deciphered)
        self.alphabet.match(ciphered_2, exp_deciphered_2)
        deciphered = self.alphabet.decipher(ciphered)
        deciphered_2 = self.alphabet.decipher(ciphered_2)
        self.assertEqual(deciphered, exp_deciphered)
        self.assertEqual(deciphered_2, exp_deciphered_2)

    def test_cipher(self):
        exp_ciphered = 'vwjw'
        exp_ciphered_2 = 'wxwpyva'
        deciphered = 'casa'
        deciphered_2 = 'apatico'
        self.alphabet.match(exp_ciphered, deciphered)
        self.alphabet.match(exp_ciphered_2, deciphered_2)
        ciphered = self.alphabet.cipher(deciphered)
        ciphered_2 = self.alphabet.cipher(deciphered_2)
        self.assertEqual(exp_ciphered, ciphered)
        self.assertEqual(exp_ciphered_2, ciphered_2)

    def test_fits(self):
        word = 'sabanamarga'
        ciphered_word = 'xomolofotyo'
        self.alphabet.match(ciphered_word, word)
        result = self.alphabet.fits('xomologotyo', 'sabanalarga')
        self.assertTrue(result)

    def test_letter_set(self):
        deciphered = 'farfullar'
        ciphered = 'xdfxghhdf'
        exp_set = {'x', 'd', 'f', 'g', 'h'}
        self.alphabet.match(ciphered, deciphered)
        self.assertSetEqual(self.alphabet.get_solved_letters(), exp_set)


class PatternsTest(unittest.TestCase):

    def setUp(self):
        self.patterns = Patterns('spanishPatterns')

    def test_build_pattern(self):
        word = 'aldaba'
        exp_pattern = '0.1.2.0.3.0'
        pattern = self.patterns.pattern(word)
        self.assertEqual(exp_pattern, pattern)

    def test_matching_words(self):
        word = 'aldaba'
        matching_words = self.patterns.get_matching_words(word)
        self.assertIn(word, matching_words)

        word_2 = 'macarron'
        matching_words_2 = self.patterns.get_matching_words(word_2)
        self.assertIn(word_2, matching_words_2)

    def test_matching_words_dic(self):
        words = ['aldaba', 'macarron']
        matching_words = self.patterns.get_matching_words_dic(words)
        self.assertIn(words[0], matching_words[words[0]])
        self.assertIn(words[1], matching_words[words[1]])


class DictionaryTest(unittest.TestCase):

    def setUp(self):
        self.patterns = Patterns('spanishPatterns')
        self.dictionary = Dictionary({})

    def test_uniques(self):
        self.dictionary.push_entry('xsfs', ["dogo"])
        self.dictionary.push_entry('kilde', ["movil", "capon", "caton"])
        self.dictionary.push_entry('sabana', ["cabana", "calana"])
        uniques = self.dictionary.uniques()
        self.assertListEqual(uniques, ["xsfs"])

    def test_filter(self):
        alphabet = Alphabet()
        alphabet.match('sz', 'oy')
        exp_dict = {'xsfs': ['dogo'],
                    'lebene': ['cabana']
                    }
        self.dictionary.push_entry('xsfs', ['dogo'])
        self.dictionary.push_entry('zszs', ['yoyo', 'mama'])
        self.dictionary.push_entry('kilde', ['movil', 'capon', 'caton', 'jabon'])
        self.dictionary.push_entry('lebene', ['cabana', 'colono'])
        self.dictionary.filter(alphabet)
        self.assertDictEqual(exp_dict, self.dictionary.get_dict())


class TextTest(unittest.TestCase):

    def setUp(self):
        ciphered_text = 'eyvuxybsia'
        self.t = Text(ciphered_text)

    def test_symbols(self):
        self.t.normalize_text()

    def test_reduce_key(self):
        pass
        # ciphered_text = open('texts/reto_07.txt', encoding='iso-8859-1').read()
        # self.t = Text(ciphered_text)

class IntegrationTest(unittest.TestCase):

    def test_correctDecipheredWord(self):
        patterns = Patterns('spanishPatterns')
        ciphered_text = 'eyvuxybsiaybuxiebuia' #rubicundosunicornios
        text = Text(ciphered_text)
        possible_words = text.extract_words()
        print(possible_words)
        dict = patterns.get_matching_words_dic(possible_words)
        print(dict)
        dictionary = Dictionary(dict)
        alphabet = Alphabet()
        alphabet.match('ey', 'ru')
        dictionary.filter(alphabet)
        print(dictionary.uniques())


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(AlphabetTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
