import unittest
from src.Alphabet import Alphabet
from src.Patterns import Patterns
from src.Text import Text


class AlphabetTest(unittest.TestCase):

    def setUp(self):
        self.a = Alphabet()

    def test_decipher(self):

        ciphered = 'vwjw'
        ciphered_2 = 'wxwpyva'
        exp_deciphered = 'casa'
        exp_deciphered_2 = 'apatico'
        self.a.match(ciphered, exp_deciphered)
        self.a.match(ciphered_2, exp_deciphered_2)
        deciphered = self.a.decipher(ciphered)
        deciphered_2 = self.a.decipher(ciphered_2)
        self.assertEqual(deciphered, exp_deciphered)
        self.assertEqual(deciphered_2, exp_deciphered_2)

    def test_cipher(self):
        exp_ciphered = 'vwjw'
        exp_ciphered_2 = 'wxwpyva'
        deciphered = 'casa'
        deciphered_2 = 'apatico'
        self.a.match(exp_ciphered, deciphered)
        self.a.match(exp_ciphered_2, deciphered_2)
        ciphered = self.a.cipher(deciphered)
        ciphered_2 = self.a.cipher(deciphered_2)
        self.assertEqual(exp_ciphered, ciphered)
        self.assertEqual(exp_ciphered_2, ciphered_2)

    def test_fits(self):
        word = 'sabanamarga'
        ciphered_word = 'xomolofotyo'
        self.a.match(ciphered_word, word)
        result = self.a.fits('xomologotyo', 'sabanalarga')
        self.assertTrue(result)

    def test_letter_set(self):
        deciphered = 'farfullar'
        ciphered = 'xdfxghhdf'
        exp_set = {'x', 'd', 'f', 'g', 'h'}
        self.a.match(ciphered, deciphered)
        self.assertSetEqual(self.a.get_solved_letters(), exp_set)


class PatternsTest(unittest.TestCase):

    def setUp(self):
        self.p = Patterns('wordPatterns')

    def test_build_pattern(self):
        word = 'aldaba'
        exp_pattern = '0.1.2.0.3.0'
        pattern = self.p.pattern(word)
        self.assertEqual(exp_pattern, pattern)

    def test_matching_words(self):
        word = 'aldaba'
        matching_words = self.p.get_matching_words(word)
        self.assertIn(word, matching_words)

        word_2 = 'macarron'
        matching_words_2 = self.p.get_matching_words(word_2)
        self.assertIn(word_2, matching_words_2)

    def test_matching_words_dic(self):
        words = ['aldaba', 'macarron']
        matching_words = self.p.get_matching_words_dic(words)
        self.assertIn(words[0], matching_words[words[0]])


class TextTest(unittest.TestCase):

    def setUp(self):
        ciphered_text = open('texts/reto_12.txt', encoding='iso-8859-1').read()
        self.t = Text(ciphered_text)

    def test_symbols(self):
        self.t.normalize_text()

    def test_reduce_key(self):
        ciphered_text = open('texts/reto_07.txt', encoding='iso-8859-1').read()
        self.t = Text(ciphered_text)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(AlphabetTest)
    unittest.TextTestRunner(verbosity=2).run(suite)