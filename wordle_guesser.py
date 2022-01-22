# @ TODO: verbose mode CLI option: displays the status of the search, current
#         letter frequencies, etc.
# @ TODO: clean and sanitize input()throw an error instead of crashing if
#         entire wordlist is pruned.
# @ TODO: simulate with an initial word

from collections import OrderedDict
import sys


class feedback:
    def __init__(self, black_letters, yellow_letters, green_letters):
        feedback.black_letters = black_letters
        feedback.yellow_letters = yellow_letters
        feedback.green_letters = green_letters


def split(word):
    return [char for char in word]


def intersection(list_1, list_2):
    list_3 = [value for value in list_1 if value in list_2]
    return list_3


def prune(word_list, feedback):
    new_list = []
    for word in word_list:
        test = split(word)
        black_test = not intersection(test, feedback.black_letters)
        yellow_test_1 = True
        yellow_test_2 = True
        green_test = True
        if sorted(intersection(test, feedback.yellow_letters.values())) != sorted(feedback.yellow_letters.values()):
            yellow_test_1 = False
        for position in feedback.yellow_letters:
            if test[position] == feedback.yellow_letters[position]:
                yellow_test_2 = False
        for position in feedback.green_letters:
            if test[position] != feedback.green_letters[position]:
                green_test = False
        if black_test and yellow_test_1 and yellow_test_2 and green_test:
            new_list.append(word)
    return new_list


def guess(word_list, verbose):
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
            print(sorted_freq[i])
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


def run(word_list, feedback, verbose):
    new_list = prune(word_list, feedback)
    new_guess = guess(new_list, verbose)
    return new_list, new_guess


def get_input():
    new_black_letters = []
    while True:
        try:
            letter = input("input a black letter or type 'done' ")
            if letter == "done":
                break
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
            position = int(input("input green letter's position "))
            new_green_letters[position] = letter
        except Exception as e:
            print("Error:", e)

    print("green letters are  ", new_green_letters)

    feedback.black_letters = new_black_letters
    feedback.yellow_letters = new_yellow_letters
    feedback.green_letters = new_green_letters

    return feedback


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
        feedback = get_input()

        word_list, new_guess = run(word_list, feedback, verbose)
        if verbose:
            print("Current wordlist length: " + str(len(word_list)))
        print(new_guess)
