from typing import List
from simpledecipher.alphabet import Alphabet
from simpledecipher.textprocessor import Text
from simpledecipher.progress import Progress
from simpledecipher.dictionary import Dictionary
from multiprocessing import Process
from simpledecipher.logger import Logger
from os import fdopen

LOG = Logger.get_logger("algorithms")


def stats(text: Text, dictionary: Dictionary) -> List[Alphabet]:
    usual_letters = [('a', 'e'), ('a', 'o'), ('a', 's'), ('a', 'n'), ('e', 'o'), ('e', 's'),
                     ('e', 'n'), ('o', 's'), ('o', 'n'), ('s', 'n')]
    text_letters_count = text.letter_stats()[:2]
    combined_letters = []
    for combination in usual_letters:
        for a in list(text_letters_count):
            for b in list(text_letters_count):
                if b != a:
                    combined_letters.insert(0, ((a[0], combination[0]), (b[0], combination[1])))
    LOG.debug('@stats-> Combinations chosen:' + combined_letters.__str__())
    n = 0
    solutions = []
    for combination in combined_letters:
        alphabet = Alphabet()
        alphabet.match(combination[0][0], combination[0][1])
        alphabet.match(combination[1][0], combination[1][1])
        LOG.debug('@stats->' + alphabet.__str__())
        dictionary_copy = dictionary.__deepcopy__()
        dictionary_copy.filter(alphabet)
        solutions += explore_uniques(dictionary_copy, alphabet, [], 0)
        solutions.sort(key=lambda t: t.goodness())
        n += 1
        if 0 == divmod(n, 10):
            LOG.debug('@stats->' + pr.stats())
            print(chr(27) + "[2J")  # Para que servia esta brujeria?
            print('(', n, '/', len(combined_letters), ')')
    return solutions
    

def explore_uniques(dictionary: Dictionary, alphabet: Alphabet, uniques: List[str], n: int = 0) -> List[Alphabet]:
    if n > 0:
        LOG.debug('@explore-> Uniques for filter: ' + uniques.__str__())
        first = uniques[0]
        solution = dictionary.solutions(first)[0]
        alphabet.match(first, solution)
        dictionary.filter(alphabet)
        uniques = dictionary.uniques()

        LOG.debug('@explore-> Next uniques: ' + uniques.__str__())
        if len(uniques) == 0:
            LOG.debug('@explore-> ' + pr.leaf((first, solution)))
        else:
            LOG.debug('@explore-> ' + pr.node((first, solution)))
    else:
        LOG.debug('@explore-> ' + pr.root())
        if len(uniques) == 0:
            uniques = dictionary.uniques()
            LOG.debug('@explore-> Uniques: ' + uniques.__str__())

    # Explore the next nodes with the new uniques and return the max result
    max_alphabet = alphabet
    n += 1
    solutions = [max_alphabet]
    for i in range(len(uniques)):
        # Swap the nth word to the first position
        nth_word = uniques.pop(i)
        uniques.insert(0, nth_word)
        solutions += explore_uniques(dictionary.__deepcopy__(), alphabet.__deepcopy__(), uniques.copy(), n)
        LOG.debug('@explore-> ' + pr.node_up().__str__())
    return solutions


def brute_exploration(d: Dictionary) -> List[Alphabet]:
    solutions = []
    n = 0
    l = d.__sizeof__()
    ciphered_possibles = list(d.keys())
    for ciphered in ciphered_possibles:
        if len(d.solutions(ciphered)) > 200:
            continue
        trimmed_dictionary = d.__deepcopy__()
        for possible in d.solutions(ciphered):
            # Leave each possible word as a unique solution
            trimmed_dictionary.remove_key(ciphered)
            trimmed_dictionary.push_entry(ciphered, [possible])
            solutions += explore_uniques(trimmed_dictionary, Alphabet(), [ciphered], 0)
            n += 1
            if 0 == divmod(n, 10):
                print(pr.stats())
                print(chr(27) + "[2J")
                print('(', n, '/', l, ')')
            # Choose the deepest result from each branch of the tree
            # if temp_alphabet.get_number_of_words() > max_alphabet.get_number_of_words():
            #     max_alphabet = temp_alphabet
    return solutions


def handle_crack(*args, **kwargs):
    kwargs['function'](args)


def handle_halt(**kwargs):
    fout = fdopen(kwargs['fout'], mode='w')
    fin = fdopen(kwargs['fin'], mode='r')
    print('Press ENTER to halt cracking process', file=fout, flush=True)
    fin.read(1)
    print('Process halted', file=fout, flush=True)


def handle_subprocess(*args, **kwargs):
    input_process = Process(target=handle_crack, args=args, kwargs=kwargs)
    input_process.start()
    crack_process = Process(target=handle_halt, kwargs=kwargs)
    crack_process.start()

    while 1:
        if input_process.is_alive():
            if not crack_process.is_alive():
                input_process.terminate()
                break
        else:
            crack_process.terminate()
            break

pr = Progress()
