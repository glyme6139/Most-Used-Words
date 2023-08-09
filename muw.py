######################
##                  ##
##  Most Used Words ##
##                  ##
######################


# Imports
from helpers import *

# Config Parsing
config = parse_config()

# Arguments Parsing
args = parse_args()

# Variables
total_word_count = None
unique_word_count = None


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



def text_to_words(text: str):
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


def word_list_to_word_dict(word_list):
    output_dict = {}
    for w in word_list:
        output_dict[w[1]] = w[0]
    return output_dict


def save_results(filename, word_list):
    file_data = None
    if args.output_format == "json":
        output_dict = word_list_to_word_dict(word_list)
        file_data = json.dumps(output_dict, indent=4)

    if args.output_format == "xml":
        output_xml = "<data>\n"
        for w in word_list:
            output_xml += "    <word>\n"
            output_xml += "        <text>"+w[1]+"</text>\n"
            output_xml += "        <number>"+str(w[0])+"</number>\n"
            output_xml += "    </word>\n"
        output_xml += "</data>\n"
        file_data = output_xml

    # writing data if any
    if file_data:
        with open(filename, "w") as outfile:
            outfile.write(file_data)
        return f"Successfuly saved data to {filename} with {args.output_format} format."
    else:
        raise RuntimeError(
            f"Cannot save data to {filename} with {args.output_format} format, the format isn't supported.")


def filter_stopwords(word_list):
    filtered_word_list = []
    for w in word_list:
        if w[1] not in stopwords[args.stopwords]:
            filtered_word_list.append(w)
    return filtered_word_list

def filter_stopwordsv2(word_list):
    filtered_word_list = []
    for w in word_list:
        if w not in stopwords[args.stopwords]:
            filtered_word_list.append(w)
    return filtered_word_list


def filter_threshold(word_list):
    filtered_word_list = []
    for w in word_list:
        if w[0] >= args.threshold:
            filtered_word_list.append(w)
    return filtered_word_list


def process_inputv2(input_text):
    global total_word_count
    global unique_word_count
    
    debug_print("Input Text", input_text)

    word_list = text_to_words(input_text)

    debug_print("Text To Words", word_list)
    total_word_count = len(word_list)


    if args.stopwords:
        word_list = filter_stopwordsv2(word_list)

        debug_print("Stopwords Filtered Word List", word_list)


    word_count_dict = count_words(word_list)

    debug_print("Word Count", word_count_dict)

    unique_word_list = word_dict_to_word_list(word_count_dict)

    debug_print("Word Dict To Word List", unique_word_list)
    unique_word_count = len(unique_word_list)

    if args.threshold > 1:
        unique_word_list = filter_threshold(unique_word_list)

        debug_print("Threshold Filtered Word List", unique_word_list)

    return unique_word_list

def process_inputv3(input_text):
    global total_word_count
    global unique_word_count
    
    debug_print("Input Text", input_text)

    word_list = text_to_words(input_text)

    debug_print("Text To Words", word_list)
    total_word_count = len(word_list)

    word_count_dict = count_words(word_list)

    debug_print("Word Count", word_count_dict)

    unique_word_list = word_dict_to_word_list(word_count_dict)

    debug_print("Word Dict To Word List", unique_word_list)
    unique_word_count = len(unique_word_list)

    if args.stopwords:
        unique_word_list = filter_stopwords(unique_word_list)

        debug_print("Stopwords Filtered Word List", unique_word_list)

    if args.threshold > 1:
        unique_word_list = filter_threshold(unique_word_list)

        debug_print("Threshold Filtered Word List", unique_word_list)

    return unique_word_list

def process_input(input_text):
    global total_word_count
    global unique_word_count
    
    debug_print("Input Text", input_text)

    word_list = text_to_words(input_text)

    debug_print("Text To Words", word_list)
    total_word_count = len(word_list)

    word_count_dict = count_words(word_list)

    debug_print("Word Count", word_count_dict)

    unique_word_list = word_dict_to_word_list(word_count_dict)

    debug_print("Word Dict To Word List", unique_word_list)
    unique_word_count = len(unique_word_list)

    if args.stopwords:
        unique_word_list = filter_stopwords(unique_word_list)

        debug_print("Stopwords Filtered Word List", unique_word_list)

    if args.threshold > 1:
        unique_word_list = filter_threshold(unique_word_list)

        debug_print("Threshold Filtered Word List", unique_word_list)

    return unique_word_list

def main(input_text,output_filename=None, version=1) :
    unique_word_list = []
    if version==1 :
        unique_word_list = process_input(input_text)
    elif version==2:
        pass

    # Last checks to ensure we don't access non existing memory

    if args.start > len(unique_word_list):
        # raise ValueError(
        #     f"Argument start supplied ({args.start}) is bigger than the unique words count in the text ({len(unique_word_list)}).")
        print(f"Argument start supplied ({args.start}) is bigger than the unique words count in the text ({len(unique_word_list)}).")
        return

    if len(unique_word_list) < 1:
        return

    # Text padding
    print("\n")

    result_list = unique_word_list

    if args.number == 0:
        for i in range(args.start-1, len(unique_word_list)):
            print(
                f'The {i+1}{get_number_suffix(i+1)} most used word in the text is : "{unique_word_list[i][1]}" with {unique_word_list[i][0]} occurences.')

    else:
        result_list = unique_word_list[args.start -
                                       1:min(args.start+args.number, len(unique_word_list)+1)-1]
        for i in range(len(result_list)):
            print(
                f'The {i+args.start}{get_number_suffix(i+args.start)} most used word in the text is : "{result_list[i][1]}" with {result_list[i][0]} occurences.')

    print(
        "\n"+f"({total_word_count} words in text, {unique_word_count} unique.)", end="\n\n")

    if args.output:

        print(f"Saving results to {args.output}", end="\n\n")
 
        print(save_results(args.output if not output_filename else output_filename, result_list))

    return



if __name__ == "__main__":
    if args.input :
        main(str.lower(args.input))

    elif args.file :
        main(str.lower(read_file(args.file)))

    elif args.directory :
        for f in next(os.walk(args.directory))[2] :
            output_file = None
            if args.output :
                output_file = os.path.abspath(args.output+os.path.sep+"muw_out_"+f.rsplit(".",1)[0]+f".{args.output_format}")
            print(f"Parsing file {f}",end="\n\n")
            main(str.lower(read_file(   os.path.abspath(args.directory+os.path.sep+f))),
                                        output_filename=output_file) # passing output filename too, parsing f to remove extension of original file and appending new extension
