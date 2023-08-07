######################
##                  ##
##  Most Used Words ##
##                  ##
######################

# Imports
import argparse


# Argument Parsing
parser = argparse.ArgumentParser(
    prog='Most Used Words',
    description='A very basic tool that let\'s you get the N^th most used word in a text or file.',
    epilog='MUW by Ryan Ducret')

parser.add_argument(
    'Input', type=str, help="Specifies the text to count from, if the -f (--file) flag is supplied, will treat input as a filename.")

parser.add_argument(
    'N', type=int, help="Specifies that you want the N^th most used word. If zero, will return the count of all words.")

parser.add_argument('-f', '--file', help="If passed, will consider the input as a filename.",
                    action='store_true')

parser.add_argument('-v', '--verbose',
                    action='store_true')

args = parser.parse_args()


# Argument Checks
if args.N < 0:
    raise ValueError(
        f"Argument N supplied ({args.N}) is invalid, N must be at least zero.")


# Variables
bVerbose = args.verbose


# Functions
def CountWords(lWords: list):
    dictWords = {}
    for w in lWords:
        if w in dictWords:
            dictWords[w] += 1
        else:
            dictWords[w] = 1
    return dictWords


def WordDictToList(dictWords: dict):
    lWords = []
    for i in dictWords:
        lWords.append((dictWords[i], i))
    # Sorting tuples by first and second item.
    sorted_list = sorted(lWords, key=lambda x: (x[0], x[1]), reverse=True)
    return sorted_list


def ReadFile(sFilename: str):
    f = open(sFilename, 'r')
    sFileData = ''.join(f.readlines())  # Concatinating lines to a big text
    f.close()
    return sFileData


def RemoveAllNonAlphanumeric(sInput: str):
    return ''.join([i for i in sInput if (i.isalpha() or i == " ")])


def ParseText(sText: str):
    # Filters the text to remove all characters that are not letters or spaces and splits the text in words, converts tabs in spaces for splitting
    lUnprocessedWordList = RemoveAllNonAlphanumeric(
        sText.strip().strip("\n").replace("\t", " ")).split(" ")

    # Removing empty entries in list due to multiple spaces in a row
    lProcessedWordList = []
    for w in lUnprocessedWordList:
        if w != "":
            lProcessedWordList.append(w)
    return lProcessedWordList


def GetNumberSuffix(iNumber: int):
    sNumberSuffix = "th"
    if str(args.N)[-1] == "1":
        sNumberSuffix = "st"
    if str(args.N)[-1] == "2":
        sNumberSuffix = "nd"
    if str(args.N)[-1] == "3":
        sNumberSuffix = "rd"
    return sNumberSuffix


# Main
def main():

    sInputText = ""
    if args.file:
        sInputText = ReadFile("Internet.txt")
    else:
        sInputText = args.Input

    if bVerbose:
        print("\n\n-------- Input Text --------\n\n")
        print(sInputText)

    lWords = ParseText(sInputText)

    if bVerbose:
        print("\n\n-------- Parsed Text --------\n\n")
        print(lWords)

    dictWordCount = CountWords(lWords)

    if bVerbose:
        print("\n\n-------- Word Count --------\n\n")
        print(dictWordCount)

    lWordCount = WordDictToList(dictWordCount)

    if bVerbose:
        print("\n\n-------- Word Dict To Word List --------\n\n")
        print(lWordCount)

    if args.N-1 > len(lWordCount):
        raise ValueError(
            f"Argument N supplied ({args.N}) is bigger than the unique words count in the text ({len(lWordCount)}).")

    if len(lWordCount) < 1:
        exit()

    # Text padding
    print("\n")

    if args.N == 0:
        for i in range(len(lWordCount)):
            print(
                f'The {i+1}{GetNumberSuffix(i)} most used word in the text is : "{lWordCount[i][1]}" with {lWordCount[i][0]} occurences.')

    else:
        print(
            f'The {args.N}{GetNumberSuffix(args.N)} most used word in the text is : "{lWordCount[args.N-1][1]}" with {lWordCount[args.N-1][0]} occurences. ({len(lWords)} words in text)')

    # Text padding
    print("\n")

    return


if __name__ == "__main__":
    main()
