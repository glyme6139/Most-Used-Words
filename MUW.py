######################
##                  ##
##  Most Used Words ##
##                  ##
######################

# Imports
import argparse
import configparser
import json
import xml.etree.cElementTree as ET

# Config Parsing
default_number = 10
stopwords = {}
config = configparser.ConfigParser()
config.read('config.conf')
if "muw.settings" in config.sections() :
    default_number = config["muw.settings"].getint("DefaultNumber", 10)
if "muw.stopwords" in config.sections() :
    for i in config["muw.stopwords"] :
        stopwords[i] = str.lower(config["muw.stopwords"].get(i)).replace("[","").replace("]","").replace(" ","").replace('"',"").split(",")
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

parser.add_argument('-o', '--output', help="Specifies the path to an output file.",
                    type=str)

parser.add_argument('-of', '--output-format', help="Specifies the format to use for the output. (default : json) (does not affect the extension)",
                    type=str, default="json",choices=["json", "xml"])

parser.add_argument('-n', '--number', help=f"Specifies the number of words to get the count of from the start argument. (default {default_number}, gets the {default_number} most used words) (if zero, shows count for every word)",
                    type=int, default=default_number)

parser.add_argument('-s', '--start', help=f"Specifies the starting number from wich to get the N^th most used words. (default 1, if 10 with n = 10 would show the 10th to 19th most used words)",
                    type=int, default=1)

parser.add_argument('-sw', '--stopwords', help="If specified will remove stopwords (such as 'a' 'the' 'wich' etc.) (defined by languages in config.conf)",
                    type=str, choices=list(stopwords.keys()))

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


def word_dict_to_word_list(word_dict: dict):
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

def word_list_to_word_dict(word_list) :
    output_dict = {}
    for w in word_list :
        output_dict[w[1]] = w[0]
    return output_dict

def save_results(filename, word_list) :
    file_data = None
    if args.output_format == "json" :
        output_dict = word_list_to_word_dict(word_list)
        file_data = json.dumps(output_dict, indent=4)
        
    if args.output_format == "xml" :
        output_xml = ET.Element("data")
        # populating xml tree
        for w in word_list :
            element = ET.SubElement(output_xml,"word")
            ET.SubElement(element,"text").text = w[1]
            ET.SubElement(element,"number").text = str(w[0])
        # formating xml and dumping to string
        ET.indent(output_xml)
        file_data = ET.tostring(output_xml).decode("UTF-8")

    # writing data if any
    if file_data :
        with open(filename, "w") as outfile:
            outfile.write(file_data)
        return f"Successfuly saved data to {filename} with {args.output_format} format."
    else :
        raise RuntimeError(f"Cannot save data to {filename} with {args.output_format} format, the format isn't supported.")

def filter_stopwords(word_list) :
    filtered_word_list = []
    for w in word_list :
        if w[1] not in stopwords[args.stopwords] :
            filtered_word_list.append(w)
    return filtered_word_list





if __name__ == "__main__":
    
    input_text = ""
    if args.file:
        input_text = str.lower(read_file(args.file))
    if args.input :
        input_text = str.lower(args.input)

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

    word_count = word_dict_to_word_list(word_count_dict)

    if bVerbose:
        print("\n\n-------- Word Dict To Word List --------\n\n")
        print(word_count)

    if args.stopwords :
        word_count = filter_stopwords(word_count)

        if bVerbose:
            print("\n\n-------- Filtered Word List --------\n\n")
            print(word_count)

    if args.start > len(word_count):
        raise ValueError(
            f"Argument start supplied ({args.start}) is bigger than the unique words count in the text ({len(word_count)}).")

    if len(word_count) < 1:
        exit()

    # Text padding
    print("\n")

    result_list = word_count

    if args.number == 0:
        for i in range(args.start-1, len(word_count)):
            print(
                f'The {i+1}{get_number_suffix(i+1)} most used word in the text is : "{word_count[i][1]}" with {word_count[i][0]} occurences.')

    else:
        result_list = word_count[args.start-1:min(args.start+args.number,len(word_count)+1)-1]
        for i in range(len(result_list)):
            print(
                f'The {i+args.start}{get_number_suffix(i+args.start)} most used word in the text is : "{result_list[i][1]}" with {result_list[i][0]} occurences.')
            
    
    
    # Text padding
    print("\n")


    print(f"({len(word_list)} words in text)")

    # Text padding
    print("\n")


    if args.output :

        print(f"Saving results to {args.output}")

        # Text padding
        print("\n")

        print(save_results(args.output, result_list))


    exit()
