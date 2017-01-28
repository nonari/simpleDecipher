from src.Alphabet import Alphabet
from src.Patterns import Patterns
from src.Text import Text
from src.Progress import Progress
from src.Dictionary import Dictionary
from multiprocessing import Process
import os


def stats(text: Text, dictionary: Dictionary):
    usual_tuples = [('a', 'e'), ('a', 'o'), ('a', 's'), ('a', 'n'), ('e', 'o'), ('e', 's'),
         ('e', 'n'), ('o', 's'), ('o', 'n'), ('s', 'n')]
    text_letters_count = text.letter_stats()[:2]
    combined_tuples = []
    for tuple in usual_tuples:
        for a in text_letters_count:
            for b in text_letters_count:
                if b != a:
                    combined_tuples.insert(0, ((a[0], tuple[0]), (b[0], tuple[1])))
    print(combined_tuples)
    alphabet = Alphabet()
    n = 0
    max_alphabet = alphabet
    for tuple in combined_tuples:
        alphabet.match(tuple[0][0], tuple[0][1])
        alphabet.match(tuple[1][0], tuple[1][1])
        dictionary_copy = dictionary.copy()
        dictionary_copy.filter(alphabet)
        temp_alphabet = explore_uniques(dictionary_copy, alphabet, [], 0)
        alphabet = Alphabet()
        n += 1
        if divmod(n, 10) == 0:
            print(pr.stats())
            print(chr(27) + "[2J") #Para que servia esta brujeria?
            print('(', n, '/', len(combined_tuples), ')')
        # Choose the deepest result from each branch of the tree
        if temp_alphabet.get_number_of_placed_letters() > max_alphabet.get_number_of_placed_letters():
            max_alphabet = temp_alphabet
    return max_alphabet
    

def explore_uniques(d: Dictionary, a: Alphabet, uniques: list, n: int = 0) -> Alphabet:
    # If not root node OR uniques remaining, try the solution
    print('')
    if n > 0:
        print('Uniques for filter: ' + uniques.__str__())
        first = uniques[0]
        solution = d.solutions(first)[0]
        a.match(first, solution)
        print(a.get_number_of_placed_letters())
        print(a.get_number_of_words())
        d.filter(a)
        uniques = d.uniques()

        print('Next uniques: ' + uniques.__str__())
        if len(uniques) == 0:
            pr.leaf((first, solution))
        else:
            pr.node((first, solution))
    else:
        pr.root()
        if len(uniques) == 0:
            uniques = d.uniques()
        print('Uniques: ' + uniques.__str__())

    # Explore the next nodes with the new uniques and return the max result
    max_alphabet = a
    n += 1
    for i in range(len(uniques)):
        # Swap the nth word to the first position
        nth_word = uniques.pop(i)
        uniques.insert(0, nth_word)
        temp_alphabet = explore_uniques(d.copy(), a.copy(), uniques.copy(), n)
        # Choose the deepest result from each branch of the tree
        if temp_alphabet.get_number_of_placed_letters() > max_alphabet.get_number_of_placed_letters():
            max_alphabet = temp_alphabet
        print(pr.node_up())

    return max_alphabet


def brute_exploration(d: Dictionary):
    # Notice that the .keys method returns a dict_keys object still pointing to the dict
    max_alphabet = Alphabet()
    n = 0
    l = d.__sizeof__()
    ciphered_possibles = list(d.keys())
    for ciphered in ciphered_possibles:
        if len(d.solutions(ciphered)) > 200:
            continue
        trimmed_dictionary = d.copy()
        # For each possible word
        for possible in d.solutions(ciphered):
            # Leave each possible word as a unique solution
            trimmed_dictionary.remove_key(ciphered)
            trimmed_dictionary.push_entry(ciphered, [possible])
            temp_alphabet = explore_uniques(trimmed_dictionary, max_alphabet.copy(), [ciphered], 0)
            n += 1
            if divmod(n, 10) == 0:
                print(pr.stats())
                print(chr(27) + "[2J")
                print('(', n, '/', l, ')')
            # Choose the deepest result from each branch of the tree
            if temp_alphabet.get_number_of_words() > max_alphabet.get_number_of_words():
                max_alphabet = temp_alphabet
    return max_alphabet


def handle_crack(*args, **kwargs):
    kwargs['function'](args)


def handle_halt(**kwargs):
    fout = os.fdopen(kwargs['fout'], mode='w')
    fin = os.fdopen(kwargs['fin'], mode='r')
    # Ask for pressing ENTER to quit current crack process
    print('Press ENTER to halt cracking process', file=fout, flush=True)
    fin.read(1)
    print('Process halted', file=fout, flush=True)


def handle_subprocess(*args, **kwargs):
    p1 = Process(target=handle_crack, args=args, kwargs=kwargs)
    p1.start()
    p2 = Process(target=handle_halt, kwargs=kwargs)
    p2.start()

    while 1:
        if p1.is_alive():
            if not p2.is_alive():
                p1.terminate()
                break
        else:
            p2.terminate()
            break

pr = Progress()
