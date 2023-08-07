######################
##                  ##
##  Most Used Words ##
##                  ##
######################

# Imports
import argparse
import configparser

# Config Parsing
default_number = 10
config = configparser.ConfigParser()
config.read('config.conf')
if "muw.settings" in config.sections() :
    default_number = config["muw.settings"].getint("DefaultNumber", 10)
else :
    config["muw.settings"] = {"DefaultNumber" : 10}
    f = open("config.conf","w")
    config.write(f)
    f.close()



# Argument Parsing
parser = argparse.ArgumentParser(
    prog='Most Used Words',
    description='A very basic tool that let\'s you get the most used word in a text or file.',
    epilog='Configuration is defined in config.conf,    MUW by Ryan Ducret')



parser.add_argument('-f', '--file', help="Input file to read text from.",
                    type=str)

parser.add_argument('-i', '--input', help="Input text.",
                    type=str)

parser.add_argument('-n', '--number', help=f"Specifies the number of words to get the count of from the start argument. (default {default_number}, gets the {default_number} most used words) (if zero, shows count for every word)",
                    type=int, default=default_number)

parser.add_argument('-s', '--start', help=f"Specifies the starting number from wich to get the N^th most used words. (default 1, if 10 with n = 10 would show the 10th to 19th most used words)",
                    type=int, default=1)

parser.add_argument('-v', '--verbose',
                    action='store_true')

args = parser.parse_args()


# Argument Checks
if args.start < 1:
    raise ValueError(
        f"Argument start supplied ({args.start}) is invalid, start must be at least 1.")

if args.number < 0:
    raise ValueError(
        f"Number supplied ({args.number}) is invalid, number must be at least 0.")

if not args.file and not args.input :
    raise SyntaxError(
        f"You must supply an input either a file (-f <filenae>) or a text (-i <text>).")

if args.file and args.input :
    raise SyntaxError(
        f"You must supply at most one input.")



# Variables
bVerbose = args.verbose


# Functions
def count_words(word_list: list):
    word_dict = {}
    for w in word_list:
        if w in word_dict:
            word_dict[w] += 1
        else:
            word_dict[w] = 1
    return word_dict


def word_dict_to_list(word_dict: dict):
    word_list = []
    for i in word_dict:
        word_list.append((word_dict[i], i))
    # Sorting tuples by first and second item.
    sorted_list = sorted(word_list, key=lambda x: (x[0], x[1]), reverse=True)
    return sorted_list


def read_file(filename: str):
    f = open(filename, 'r')
    file_data = ''.join(f.readlines())  # Concatinating lines to a big text
    f.close()
    return file_data


def remove_all_non_alpha(input_text: str):
    return ''.join([i for i in input_text if (i.isalpha() or i == " ")])


def parse_text(text: str):
    # Filters the text to remove all characters that are not letters or spaces and splits the text in words, converts tabs in spaces for splitting
    unprocessed_word_list = remove_all_non_alpha(
        text.strip().strip("\n").replace("\t", " ")).split(" ")

    # Removing empty entries in list due to multiple spaces in a row
    processed_word_list = []
    for w in unprocessed_word_list:
        if w != "":
            processed_word_list.append(w)
    return processed_word_list


def get_number_suffix(number: int):
    number_suffix = "th"
    if str(number)[-1] == "1":
        number_suffix = "st"
    if str(number)[-1] == "2":
        number_suffix = "nd"
    if str(number)[-1] == "3":
        number_suffix = "rd"
    return number_suffix


if __name__ == "__main__":
    
    input_text = ""
    if args.file:
        input_text = read_file(args.file)
    if args.input :
        input_text = args.input

    if bVerbose:
        print("\n\n-------- Input Text --------\n\n")
        print(input_text)

    word_list = parse_text(input_text)

    if bVerbose:
        print("\n\n-------- Parsed Text --------\n\n")
        print(word_list)

    word_count_dict = count_words(word_list)

    if bVerbose:
        print("\n\n-------- Word Count --------\n\n")
        print(word_count_dict)

    word_count = word_dict_to_list(word_count_dict)

    if bVerbose:
        print("\n\n-------- Word Dict To Word List --------\n\n")
        print(word_count)

    if args.start > len(word_count):
        raise ValueError(
            f"Argument start supplied ({args.start}) is bigger than the unique words count in the text ({len(word_count)}).")

    if len(word_count) < 1:
        exit()

    # Text padding
    print("\n")

    if args.number == 0:
        for i in range(args.start-1, len(word_count)):
            print(
                f'The {i+1}{get_number_suffix(i+1)} most used word in the text is : "{word_count[i][1]}" with {word_count[i][0]} occurences.')

    else:
        for i in range(args.start,min(args.start+args.number,len(word_count)+1)):
            print(
                f'The {i}{get_number_suffix(i)} most used word in the text is : "{word_count[i-1][1]}" with {word_count[i-1][0]} occurences.')
            
    
    
    # Text padding
    print("\n")


    print(f"({len(word_list)} words in text)")

    # Text padding
    print("\n")

    exit()
