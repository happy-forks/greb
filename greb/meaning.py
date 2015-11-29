r"""

Greb is a command line tool to find meaning of words.

Usage: greb <WORD> [-leyn] [-h | --help]

Options:
    -l --all        Lists everything
    -e --sen        Lists sentence
    -y --syn        Lists synonyms
    -n --ant        Lists antonyms
    --version       Lists version
    -h --help       Lists help
"""

import requests
import sys
from bs4 import BeautifulSoup
from colorama import Fore
from docopt import docopt

__version__ = '0.0.5'

BASE_URL = 'http://www.merriam-webster.com/dictionary/'

requests.packages.urllib3.disable_warnings()


def print_heading(heading, color):
    '''prints the heading for a section of output'''
    print("")
    print(color + heading + Fore.RESET)
    print("")


def print_error_messages(msg):
    '''prints the error messgaes in red'''
    print(Fore.RED + msg + Fore.RESET)


def display_meaning(tree):
    '''prints the meaning corresponding to a word'''
    meanings = tree.find("div", {"class": "ld_on_collegiate"})
    found_meaning = False
    if meanings:
        found_meaning = True
        print_heading('MEANING', Fore.YELLOW)
        for each in meanings.find_all("p"):
            print(each.get_text())
    else:
        meanings = tree.find_all("span", {"class": "ssens"})
        if meanings:
            found_meaning = True
            print_heading('MEANING', Fore.YELLOW)
            for each in meanings:
                if ':' in each.get_text():
                    each = each.get_text().split(':')[1].replace(u'\xc2', ' ').replace(u'\xa0', ' ')
                    if len(each.strip()) > 0:
                        print(': ' + each.strip().encode('utf8'))
                else:
                    print(each.get_text().encode('utf8').strip())
    if not found_meaning:
        print_error_messages("Unable to find meaning for this word. Are you sure its spelled right?")


def display_sentences(tree, word):
    '''prints the sentences showing the use of a word'''
    sentences = tree.find("div", {"class": "example-sentences"})
    if sentences:
        print_heading('SENTENCE', Fore.GREEN)
        for each in sentences.find_all("li", {"class": "always-visible"}):
            print(each.get_text().replace(word, Fore.CYAN + word + Fore.RESET))
    else:
        print_error_messages("Oops! There are no sentences to display. Why not frame your own?")


def display_synonyms(tree):
    '''prints the synonyms for a given word'''
    synonyms = tree.find("dl")
    if synonyms:
        print_heading('SYNONYM', Fore.BLUE)
        print(', '.join([each.get_text() for each in synonyms.find_all("a")]))
    else:
        print_error_messages("Ohh! There are no synonyms.")


def display_antonyms(tree):
    '''prints the antonyms for a given word'''
    antonyms = tree.find_all("dl")
    if len(antonyms) > 1:
        antonyms = antonyms[1]
        print_heading('ANTONYM', Fore.RED)
        print(', '.join([each.get_text() for each in antonyms.find_all("a")]))
    else:
        print_error_messages("Ohh! There are no antonyms.")


def get_suggestions(tree):
    '''lists the suggestions for a word in case of 404'''
    suggestions = tree.find_all("ol", {"class": "franklin-spelling-help"})
    if suggestions:
        print(Fore.BLUE + 'It seems that you have not entered a valid word. We know' + Fore.RESET +
              Fore.GREEN + ' To err is human.' + Fore.RESET + Fore.BLUE + ' Hence the suggestions.' + Fore.RESET)
        print_heading('SUGGESTION', Fore.YELLOW)
        print(', '.join([each.get_text() for each in suggestions[0].find_all("a")]))


def make_tree(word, print_meaning=False, print_sentence=False, print_synonym=False, print_antonym=False):
    '''reads the web page and make a html tree'''
    req = requests.get(BASE_URL+word)
    tree = BeautifulSoup(req.text, 'html.parser')
    if req.status_code == requests.codes.ok:
        if print_meaning:
            display_meaning(tree)
        if print_sentence:
            display_sentences(tree, word)
        if print_synonym:
            display_synonyms(tree)
        if print_antonym:
            display_antonyms(tree)
    elif req.status_code == 404:
        if 'Dictionary Spelling Help' in req.text:
            get_suggestions(tree)
        else:
            print_error_messages("The word you've entered was not found. Please try your search again.")
    else:
        print_error_messages("Unable to retrieve meaning. Try again later!")
        sys.exit()


def main():
    '''findmeaning is a command line tool to find meanings'''
    arguments = docopt(__doc__, version=__version__)
    if arguments['<WORD>']:
        flag_meaning = True
        if (arguments.get('-l') or arguments.get('--all')):
            flag_sentence, flag_synonym, flag_antonym = [True]*3
        else:
            flag_sentence = (arguments.get('-e') or arguments.get('--sen')) or False
            flag_synonym = (arguments.get('-y') or arguments.get('--syn')) or False
            flag_antonym = (arguments.get('-n') or arguments.get('--ant')) or False
        make_tree(arguments['<WORD>'].lower(), print_meaning=flag_meaning,
                  print_sentence=flag_sentence, print_synonym=flag_synonym,
                  print_antonym=flag_antonym)
    else:
        print(__doc__)

if __name__ == '__main__':
    main()
