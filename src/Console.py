from src.Crack import handle_crack
from src.Crack import brute_exploration
from src.Crack import stats
from src.Crack import explore_uniques
from src.Alphabet import Alphabet
from src.Patterns import Patterns
from src.Text import Text
from src.Progress import Progress
from src.Dictionary import Dictionary
import os
import sys


p = Patterns('wordPatterns')
t_committed = None
t = None
d = None

ciphered_text = open('/home/alex/PycharmProjects/simpleDecipher/test/texts/reto_11_split.txt',
                     encoding='iso-8859-1').read()


def create_dict():
    di = None
    while 1:
        if d is None:
            response = input('Create dict?: y/n ')
        else:
            response = input('Overwrite existing dict?: y/n ')

        if response == 'y':
            w = t.extract_words()
            di = Dictionary(p.get_matching_words_dic(w))
            print('Dict created')
            break
        else:
            if response != 'n':
                print('Type only y/n ')
            else:
                print('Dict not created')
                break
    return di


print('Type help for commands')
s = ' '
while 1:
    try:
        s = input()
    except EOFError:
        print('Bye')
        break

    if s == '':
        continue

    args = s.split(' ')

    if args[0] == 'quit':
        print('Bye')
        break

    if args[0] == 'help':
        print('Commands:')
        print('    load')
        print('    text')
        print('    crack')
        print('    help')
        print('For more help type the command followed by -h')
        continue

    if args[0] == 'load':
        if len(args) == 1:
            text = input('Input> ')
            t = text
            t_committed = t
            continue
        if args[1] == '-h':
            print('load [FILE]')
            print('Loads the ciphered text, without FILE reads from the stdio')
            print('Options:')
            print('    -h           Show this menu')
            continue
        # Check if the file exists
        if os.path.isfile(args[1]):
            text = open(args[1], encoding='iso-8859-1').read()
            if t is None:
                t = Text(text)
                t_committed = t
                print('Text loaded')
            else:
                while 1:
                    res = input('Overwrite text?: y/n ')
                    if res == 'y':
                        t = Text(text)
                        print('Text saved')
                        break
                    else:
                        if res != 'n':
                            print('Type only y/n ')
                        else:
                            print('Text not saved')
                            break
        else:
            print('File not found')
        continue

    if args[0] == 'text':
        if len(args) == 1:
            print(t.get_text())
            continue
        else:
            if args[1] == '-h':
                print('Operation over the text, without arguments, shows it')
                print('Options: (Non stackable, except -v )')
                print('    -h               Show this menu')
                print('    -n               Normalize text')
                print('    -c               Check key')
                print('    -K               Reduce key')
                print('    -k               Normalize key')
                print('    -r               Remove stops')
                print('    -s               Letter stats')
                print('    -t [ini] [end]   Trim')
                print('    -C               Commit')
                print('    -R               Rollback')
                print('    -v               Show changes')
                continue
            if args[1][:2] == '-n':
                t.normalize_text()
                if len(args[1]) == 3 and args[1][2] == 'v':
                    print(t.get_text())
                continue
            if args[1][:2] == '-c':
                print(t.check_symbols())
                continue
            if args[1][:2] == '-K':
                t.reduce_key()
                if len(args[1]) == 3 and args[1][2] == 'v':
                    print(t.get_text())
                continue
            if args[1][:2] == '-k':
                t.normalize_key()
                if len(args[1]) == 3 and args[1][2] == 'v':
                    print(t.get_text())
                continue
            if args[1][:2] == '-r':
                t.remove_stops()
                if len(args[1]) == 3 and args[1][2] == 'v':
                    print(t.get_text())
                continue
            if args[1][:2] == '-s':
                print(t.letter_stats())
                continue
            if args[1][:2] == '-l':
                print(len(t.get_text()))
                continue
            if args[1] == '-t':
                if len(args) == 4:
                    try:
                        t.trim(ini=int(args[2]), fin=int(args[3]))
                    except UnboundLocalError:
                        print('Parameters out of bounds')
                continue
            if args[1][:2] == '-C':
                t_committed = Text(t.get_text())
                print('Modifications are saved')
                continue
            if args[1][:2] == '-R':
                t = t_committed
                print('Text restored')
                continue
            # Otherwise
            print('Wrong arguments')
            continue

    if args[0] == 'crack':
        if d or t_committed is None:
            print('Dict or text uninitialized')
            continue
        if len(args) == 1:
            handle_crack(d, Alphabet(), None, 0, function=explore_uniques,
                         fout=sys.stdout.fileno(), fin=sys.stdin.fileno())
            continue
        else:
            if args[1] == '-h':
                print('Crack the text with the current dict, without options, performs a normal crack')
                print('Options:')
                print('    -n        Performs a normal cracking, same as with no arguments')
                print('    -b        Performs a brute force cracking')
                print('    -s        Cracks it based on letter statistics')
                print('    -h        Show this menu')
            if len(args) == 1:
                handle_crack(d, Alphabet(), None, 0, function=explore_uniques,
                             fout=sys.stdout.fileno(), fin=sys.stdin.fileno())
            if args[1] == '-b':
                handle_crack(d, function=brute_exploration,
                             fout=sys.stdout.fileno(), fin=sys.stdin.fileno())
            if args[1] == '-s':
                handle_crack(t_committed, d, function=stats,
                             fout=sys.stdout.fileno(), fin=sys.stdin.fileno())
            continue

    if args[0] == 'dict':
        if d is None:
            if t is not None:
                d = create_dict()
                continue
            else:
                print('There is no text to create the dictionary')
                break
        if len(args) == 1:
            continue
        else:
            if args[1] == '-h':
                print('Operation over the dict, without arguments, shows it')
                print('Options:')
                print('    -l [max]         Limit the length of the solutions')
                print('    -f               Find the proposed solutions for a key')
                print('    -r               Remove a key')
                print('    -s               Size')
                print('    -c               Create or overwrite dict')
            if args[1] == '-l':
                if len(args) == 3:
                    l = int(args[2])
                    for i in d.get_dict():
                        if len(d.get_dict()[i]) > l:
                            d.remove_possible(i)

                else:
                    print('Maximum length missing')
            if args[1] == '-f':
                if len(args) == 3:
                    if args[2] in d.get_dict():
                        print(d.get_dict()[args[2]])
                    else:
                        print('Key not found')
                else:
                    print('Key word missing')
            if args[1] == '-r':
                if len(args) == 3:
                    l = int(args[2])
                    if args[2] in d.get_dict():
                        d.remove_possible(args[2])
                    else:
                        print('Key not found')
                else:
                    print('Key word missing')
            if args[1] == '-s':
                n = 0
                for k in d.get_dict():
                    n += len(d.get_dict()[k])
            if args[1] == '-c':
                d = create_dict()

    print('Syntax Error: Type help for commands usage')
