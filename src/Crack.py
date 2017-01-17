from src.Alphabet import Alphabet
from src.Patterns import Patterns
from src.Text import Text
from src.Progress import Progress
from src.Dictionary import Dictionary
from multiprocessing import Process
import os


def stats(t: Text, d: Dictionary):
    l = [('a', 'e'), ('a', 'o'), ('a', 's'), ('a', 'n'), ('e', 'o'), ('e', 's'),
         ('e', 'n'), ('o', 's'), ('o', 'n'), ('s', 'n')]
    l_t = t.letter_stats()[:9]
    s_tuples = []
    for t in l:
        for a in l_t:
            for b in l_t:
                if b != a:
                    s_tuples.insert(0, ((a[0], t[0]), (b[0], t[1])))
    a = Alphabet()
    a_copy = a.copy()
    n = 0
    max_alphabet = a
    for t in s_tuples:
        a.match(t[0][0], t[0][1])
        a.match(t[0][0], t[0][1])
        dc = d.copy()
        dc.filter(a)
        temp_alphabet = explore_uniques(dc, a, [], 0)
        n += 1
        if divmod(n, 10)[1] == 0:
            print(pr.stats())
            print(chr(27) + "[2J")
            print('(', n, '/', len(s_tuples), ')')
        # Choose the deepest result from each branch of the tree
        if len(temp_alphabet.get_solved_letters()) > len(max_alphabet.get_solved_letters()):
            max_alphabet = temp_alphabet
        a = a_copy.copy()
    return max_alphabet
    

def explore_uniques(d: Dictionary, a: Alphabet, uniques: list, n: int):
    # If not root node OR uniques remaining, try the solution
    if n > 0:
        # Solve for the first unique and remove it
        first = uniques.pop(0)
        if len(uniques) == 0:
            pr.leaf((first, d.solutions(first)[0]))
        else:
            pr.node((first, d.solutions(first)[0]))
        a.match(first, d.solutions(first)[0])
        # Recheck words dict for filtering matching words
        d.filter(a)
        # Extract the new unique words
        uniques = d.uniques()
    else:
        pr.root()
        if len(uniques) == 0:
            uniques = d.uniques()
    # Explore the next nodes with the new uniques and return the max result
    max_alphabet = a
    n += 1
    for i in range(len(uniques)):
        # Swap the nth word to the first position
        nth_word = uniques.pop(i)
        uniques.insert(0, nth_word)
        temp_alphabet = explore_uniques(d.copy(), a.copy(), uniques.copy(), n)
        if n == 0:
            print(len(uniques))
        # Choose the deepest result from each branch of the tree
        if len(temp_alphabet.get_solved_letters()) > len(max_alphabet.get_solved_letters()):
            max_alphabet = temp_alphabet
    pr.node_up()
    return max_alphabet


def brute_exploration(d: Dictionary):
    # Notice that the .keys method returns a dict_keys object still pointing to the dict
    max_alphabet = Alphabet()
    n = 0
    l = d.__sizeof__()
    for ciphered in d.keys():
        trimmed_words = d.copy()
        # For each possible word
        for possible in d.solutions(ciphered):
            # Leave each possible word as a unique solution
            trimmed_words.remove_key(ciphered)
            trimmed_words.push_entry(ciphered, [possible])
            temp_alphabet = explore_uniques(trimmed_words, max_alphabet.copy(), [ciphered], 0)
            n += 1
            if divmod(n, 10)[1] == 0:
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

p = Patterns('wordPatterns')
pr = Progress()
