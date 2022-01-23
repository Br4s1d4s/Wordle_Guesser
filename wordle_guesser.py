# @ TODO: simulate with an initial word
# @ TODO: help command line flag
# @ TODO: check inputs for char and int types

"""
This program is a Wordle guess optimizer. 
"""

from collections import OrderedDict
import sys

"""
This class captures the current state of knowlege regarding the letters in the
Wordle. Due to the way the word list is pruned, the program only needs the colors
in the letters of the last guess to work. Conversely, you can re-start the program
and use the sum total of your knowledge to skip to which ever step you were on if 
a letter is entered incorrectly, etc.

Eventually this program will contain a Wordle simulator - which will return a 
Feedback class with all the information for the current guess. The Feedback class
is also where a "display" function would go to show the yellow boxes for each guess.
"""
class Feedback:
    def __init__(self, black_letters, yellow_letters, green_letters):
        Feedback.black_letters = black_letters
        Feedback.yellow_letters = yellow_letters
        Feedback.green_letters = green_letters

"""
This function returns a list of the characters in a given word. while short,
it is used multiple times in the prune process.
"""
def split(word):
    return [char for char in word]


"""
This function returns the intersection between two lists. Facilitates testing whether
a word has a black letter or doesn't have a yellow letter, and checking for double
letter rules (one black and one yellow or green letter being the same).
"""
def intersection(list_1, list_2):
    list_3 = [value for value in list_1 if value in list_2]
    return list_3


"""
The prune step removes any word from the reamaining word list using 6 tests, each
of which returns a boolean value: does the word contain any black letters, does the
word not contain any yellow letters, does the word contain yellow letters in their
current position, does the word not contain green letters in their current positions,
does the word contain any double letters from the yellow list and black list, and the
same from the green list and black list.
"""
def prune(word_list, Feedback):
    """
    Shrink the list based on the puzzle's current state, return the pruned list
    """
    new_list = []
    for word in word_list:
        test = split(word)
        black_test = not intersection(test, Feedback.black_letters)
        yellow_test_1 = True
        yellow_test_2 = True
        green_test = True
        if sorted(intersection(test, Feedback.yellow_letters.values())) != sorted(feedback.yellow_letters.values()):
            yellow_test_1 = False
        for position in Feedback.yellow_letters:
            if test[position] == Feedback.yellow_letters[position]:
                yellow_test_2 = False
        for position in Feedback.green_letters:
            if test[position] != Feedback.green_letters[position]:
                green_test = False
        if black_test and yellow_test_1 and yellow_test_2 and green_test:
            new_list.append(word)
        if len(new_list) == 0:
            print("letter criteria not met by members of current list")
            sys.exit()
    return new_list


"""
The guess function uses a naive gradient descent to pick the word with the most
likely letters from the remaining words on the word list. First, the function
calculates the current letter frequency based on the words remaining in the word list.
Then, the function scores each word for each unique letter from that list.

There is a possibility that this approach is not ideal for Wordles with double letters,
but the algorithm will find them.
"""
def guess(word_list, verbose):
    """
    Figure out the best guess word based on letter frequency in the word list
    """
    frequency_list = {}
    for word in word_list:
        letters = split(word)
        for char in letters:
            if char in frequency_list:
                frequency_list[char] += 1
            else:
                frequency_list[char] = 1

    if verbose:
        print("Top 10 letters with # of appearances:")
        sorted_freq = sorted(frequency_list.items(),
                             key=lambda x: x[1], reverse=True)
        for i in range(10):
            try:
                print(sorted_freq[i])
            except:
                break
    score = 0
    for word in word_list:
        letters = list(OrderedDict.fromkeys(split(word)).keys())
        test = 0
        for char in letters:
            test += frequency_list[char]
        if test > score:
            score = test
            guess = word
    return guess


"""
Run is a convenient packagign fo the prune and guess steps.
"""
def run(word_list, Feedback, verbose):
    new_list = prune(word_list, Feedback)
    new_guess = guess(new_list, verbose)
    return new_list, new_guess


def get_input():
    """
    Receive the state of the game from user input after a guess
    """
    new_black_letters = []
    while True:
        try:
            letter = input("input a black letter or type 'done' ")
            if letter == "done":
                break
            elif letter == "quit":
                sys.exit()
            new_black_letters.append(letter)
        except Exception as e:
            print("Error:", e)

    print("black letters are  ", new_black_letters)

    new_yellow_letters = {}
    while True:
        try:
            letter = input("input a yellow letter or type 'done' ")
            if letter == "done":
                break
            elif letter == "quit":
                sys.exit()
            position = int(input("input yellow letter's position "))
            new_yellow_letters[position] = letter
        except Exception as e:
            print("Error:", e)

    print("yellow letters are  ", new_yellow_letters)

    new_green_letters = {}
    while True:
        try:
            letter = input("input a green letter or type 'done' ")
            if letter == "done":
                break
            elif letter == "quit":
                sys.exit()
            position = int(input("input green letter's position "))
            new_green_letters[position] = letter
        except Exception as e:
            print("Error:", e)

    print("green letters are  ", new_green_letters)

    Feedback.black_letters = new_black_letters
    Feedback.yellow_letters = new_yellow_letters
    Feedback.green_letters = new_green_letters

    return Feedback


def simulate(the_answer):
    pass


if __name__ == "__main__":

    verbose = False

    if ((len(sys.argv)) > 1):
        if (sys.argv[1] == "-v"):
            verbose = True
            print("Running in Verbose Mode\n")

    with open('wordle_word_list.txt') as f:
        Strings = f.read()

        word_list = Strings.split()

    iterations = 0
    while len(word_list) > 1:
        if verbose:
            print("Beginning pass #: " + str(iterations + 1))
        Feedback = get_input()

        word_list, new_guess = run(word_list, Feedback, verbose)
        if verbose:
            print("Current wordlist length: " + str(len(word_list)))
        print(new_guess)