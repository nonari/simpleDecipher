import unittest

from simpledecipher.comparator import Comparator
from simpledecipher.alphabet import Alphabet
from simpledecipher.patterns import Patterns
from simpledecipher.textprocessor import Text
from simpledecipher.dictionary import Dictionary
import simpledecipher.algorithms as algorithms


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
        pattern = self.patterns.pattern_of(word)
        self.assertEqual(exp_pattern, pattern)

    def test_matching_words(self):
        word = 'aldaba'
        matching_words = self.patterns.matching_words(word)
        self.assertIn(word, matching_words)

        word_2 = 'macarron'
        matching_words_2 = self.patterns.matching_words(word_2)
        self.assertIn(word_2, matching_words_2)

    def test_matching_words_dic(self):
        words = ['aldaba', 'macarron']
        matching_words = self.patterns.matching_words_dic(words)
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
        ciphered_text = 'xylbsiwbklswbrls'
        self.text = Text(ciphered_text)

    def test_symbols(self):
        self.text.normalize_text()

    def test_extract(self):
        possible_words = self.text.extract_words()
        expected_possible_words = ['xylbs', 'ylbsi', 'lbsiw', 'bsiwb', 'siwbk', 'iwbkl', 'wbkls', 'swbrl', 'wbrls',
                                   'xylbsi', 'ylbsiw', 'iwbkls', 'wbklsw', 'bklswb', 'swbrls',
                                   'xylbsiwbklswbrl', 'ylbsiwbklswbrls']
        result = True
        for word in expected_possible_words:
            if not possible_words.__contains__(word):
                result = False
                break
        assert result

    def test_extract_with_position(self):
        possible_words_with_pos = self.text.extract_words_with_position()
        assert(possible_words_with_pos['ylbsi'] == (1, 5))
        assert(possible_words_with_pos['ylbsiwbklswbrls'] == (1, 15))

    def test_reduce_key(self):
        pass
        # ciphered_text = open('texts/reto_07.txt', encoding='iso-8859-1').read()
        # self.t = Text(ciphered_text)


class ComparatorTest(unittest.TestCase):

    def test_count_correct(self):
        solution1 = Alphabet()
        solution2 = Alphabet()
        solution3 = Alphabet()
        solution1.match("abcdef", "fedcba")
        solution2.match("abcdef", "fexcba")
        solution3.match("abcdef", "fedcnm")
        exp_matching_dict = {solution2: 5, solution3: 4}
        c = Comparator([solution2, solution3], [solution1])
        for solution1, index in c.get_solution_pairs():
            for solution2 in index:
                assert exp_matching_dict[solution2] == index[solution2]

    def test_match_count(self):
        # Max 18000
        solutions1 = Alphabet.generate_random_solutions(150)
        solutions2 = Alphabet.generate_random_solutions(150)

        result = True
        comparator = Comparator(solutions1, solutions2)
        for solution1, index in comparator.get_solution_pairs():
            for solution2 in index:
                count = 0
                for letter1 in solution1.get_solved_letters():
                    if letter1 in solution2.get_solved_letters():
                        if solution1.decipher(letter1) == solution2.decipher(letter1):
                            count += 1
                if index[solution2] != count:
                    result = False
                    break
            if not result:
                break
        assert result

    def test_overlaps(self):
        text = Text('catastropajoblanco')
        word_positions = text.extract_words_with_position(max_len=15)
        alphabet = Alphabet()
        alphabet.match('catastro', 'catastro')
        alphabet.match('astropajo', 'astropajo')
        alphabet.match('ajoblanco', 'ajoblanco')
        overlaps = Comparator.overlaps(alphabet.get_solved_words(), word_positions)
        assert(overlaps == 8)


class IntegrationTest(unittest.TestCase):

    def test_correct_deciphered_word(self):
        patterns = Patterns('spanishPatterns')
        #                rubicundosunicorniossobrevolaran
        ciphered_text = 'eyvuxybsiaybuxiebuiaaivewciklelb'
        text = Text(ciphered_text)
        possible_words = text.extract_words()
        solving_dict = patterns.matching_words_dic(possible_words)
        dictionary = Dictionary(solving_dict)
        alphabet = Alphabet()
        alphabet.match('ey', 'ru')
        dictionary.filter(alphabet)
        unique_words_found = dictionary.uniques()
        expected_uniques = ['eyvuxybsi', 'ybuxiebuia']
        self.assertIn(expected_uniques[0], unique_words_found)
        self.assertIn(expected_uniques[1], unique_words_found)


class CrackTextWithUniqueWordsTest(unittest.TestCase):

    def setUp(self):
        patterns1 = Patterns('spanishPatterns')
        #                 rubicundosunicorniosvolaranllameantes
        self.raw_text1 = 'eyvuxybsiaybuxiebuiaciklelbkklnwlbrwa'
        text1 = Text(self.raw_text1)
        possible_words1 = text1.extract_words()
        solving_dict1 = patterns1.matching_words_dic(possible_words1)
        self.dictionary1 = Dictionary(solving_dict1)
        self.alphabet1 = Alphabet()

        patterns2 = Patterns('spanishPatterns')
        #                 vueloblancodegaviotarogatorio
        self.raw_text2 = 'cywkivklbxiswzlcuirleizlrieui'
        text2 = Text(self.raw_text2)
        possible_words2 = text2.extract_words()
        solving_dict2 = patterns2.matching_words_dic(possible_words2)
        self.dictionary2 = Dictionary(solving_dict2)
        self.alphabet2 = Alphabet()

    def test_divide_to_win(self):
        solutions = algorithms.explore_uniques(self.dictionary1, self.alphabet1, [])
        solutions2 = algorithms.explore_uniques(self.dictionary2, self.alphabet2, [])

        comparator = Comparator(solutions, solutions2)
        best_pair = comparator.best()

        # Optimal separate solutions
        assert(best_pair[1].decipher(self.raw_text1) == 'rubicundosunicornios?olaranllameantes')
        assert(best_pair[0].decipher(self.raw_text2) == 'vueloslancomegaviotarogatorio')


class CrackTextWithoutUniqueWords(unittest.TestCase):

    def setUp(self):
        patterns1 = Patterns('spanishPatterns')
        #                      fronteradelosbesosseranmanana
        self.ciphered_text1 = 'deibrwelswkiavwaiaawelbnlblbl'
        self.text1 = Text(self.ciphered_text1)
        possible_words1 = self.text1.extract_words()
        solving_dict1 = patterns1.matching_words_dic(possible_words1)
        self.dictionary1 = Dictionary(solving_dict1)
        patterns2 = Patterns('spanishPatterns')
        #                      cuandoenladentadurasientasunarma
        self.ciphered_text2 = 'xylbsiwbklswbrlsyelauwbrlayblenl'
        self.text2 = Text(self.ciphered_text2)
        possible_words2 = self.text2.extract_words()
        solving_dict2 = patterns2.matching_words_dic(possible_words2)
        self.dictionary2 = Dictionary(solving_dict2)

    def test_stats(self):
        solutions1 = algorithms.stats(self.text1, self.dictionary1)
        solutions2 = algorithms.stats(self.text2, self.dictionary2)

        comparator = Comparator(solutions2, solutions1, self.text1.extract_words_with_position(),
                                self.text2.extract_words_with_position())

        result = comparator.sort()
        result.reverse()
        e, i = result[12]
        # TODO formalize verification
        print(i.decipher(self.ciphered_text2))
        print(e.decipher(self.ciphered_text1))


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(AlphabetTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
