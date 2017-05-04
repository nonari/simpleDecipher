from typing import List
from src.Alphabet import Alphabet
from src.Text import Text
from src.Progress import Progress
from src.Dictionary import Dictionary
from multiprocessing import Process
import os


def stats(text: Text, dictionary: Dictionary):
    usual_letters = [('a', 'e'), ('a', 'o'), ('a', 's'), ('a', 'n'), ('e', 'o'), ('e', 's'),
                     ('e', 'n'), ('o', 's'), ('o', 'n'), ('s', 'n')]
    text_letters_count = text.letter_stats()[:2]
    combined_letters = []
    for combination in usual_letters:
        for a in list(text_letters_count):
            for b in list(text_letters_count):
                if b != a:
                    combined_letters.insert(0, ((a[0], combination[0]), (b[0], combination[1])))
    print(combined_letters)
    n = 0
    solutions = []
    for combination in combined_letters:
        alphabet = Alphabet()
        alphabet.match(combination[0][0], combination[0][1])
        alphabet.match(combination[1][0], combination[1][1])
        dictionary_copy = dictionary.__deepcopy__()
        dictionary_copy.filter(alphabet)
        solutions += explore_uniques(dictionary, alphabet, [], 0)
        n += 1
        if 0 == divmod(n, 10):
            print(pr.stats())
            print(chr(27) + "[2J")  # Para que servia esta brujeria?
            print('(', n, '/', len(combined_letters), ')')
        # Choose the deepest result from each branch of the tree
        # if temp_alphabet.get_number_of_placed_letters() > max_alphabet.get_number_of_placed_letters():
        #     max_alphabet = temp_alphabet
    return solutions
    

def explore_uniques(dictionary: Dictionary, alphabet: Alphabet, uniques: List[str], n: int = 0) -> List[Alphabet]:
    print('')
    if n > 0:
        print('Uniques for filter: ' + uniques.__str__())
        first = uniques[0]
        solution = dictionary.solutions(first)[0]
        alphabet.match(first, solution)
        print(alphabet.get_number_of_placed_letters())
        print(alphabet.get_number_of_words())
        dictionary.filter(alphabet)
        uniques = dictionary.uniques()

        print('Next uniques: ' + uniques.__str__())
        if len(uniques) == 0:
            pr.leaf((first, solution))
        else:
            pr.node((first, solution))
    else:
        pr.root()
        if len(uniques) == 0:
            uniques = dictionary.uniques()
        print('Uniques: ' + uniques.__str__())

    # Explore the next nodes with the new uniques and return the max result
    max_alphabet = alphabet
    n += 1
    solutions = [max_alphabet]
    for i in range(len(uniques)):
        # Swap the nth word to the first position
        nth_word = uniques.pop(i)
        uniques.insert(0, nth_word)
        solutions += explore_uniques(dictionary.__deepcopy__(), alphabet.__deepcopy__(), uniques.copy(), n)
        # Choose the deepest result from each branch of the tree
        # if temp_alphabet.get_number_of_placed_letters() > max_alphabet.get_number_of_placed_letters():
        #     max_alphabet = temp_alphabet
        print(pr.node_up())

    return solutions


def brute_exploration(d: Dictionary):
    max_alphabet = Alphabet()
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
            temp_alphabet = explore_uniques(trimmed_dictionary, max_alphabet.__deepcopy__(), [ciphered], 0)
            n += 1
            if 0 == divmod(n, 10):
                print(pr.stats())
                print(chr(27) + "[2J")
                print('(', n, '/', l, ')')
            # Choose the deepest result from each branch of the tree
            # if temp_alphabet.get_number_of_words() > max_alphabet.get_number_of_words():
            #     max_alphabet = temp_alphabet
    return max_alphabet


def handle_crack(*args, **kwargs):
    kwargs['function'](args)


def handle_halt(**kwargs):
    fout = os.fdopen(kwargs['fout'], mode='w')
    fin = os.fdopen(kwargs['fin'], mode='r')
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
