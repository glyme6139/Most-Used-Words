
import argparse
import configparser
import json
import os

default_number = 10
default_start = 1
default_format = "json"
default_threshold = 1
stopwords = {}
verbose = False


def debug_print(title, message):
    if verbose:
        print("\n\n"+f"{'-'*8} {title} {'-'*8}"+"\n\n")
        print(message)


def parse_config():
    global default_number
    global default_start
    global default_format
    global default_threshold
    global stopwords
    config = configparser.ConfigParser()
    config.read('config.conf')
    if "muw_settings" in config.sections():
        default_number = config["muw_settings"].getint(
            "default_number", default_number)
        default_start = config["muw_settings"].getint(
            "default_start", default_start)
        default_format = config["muw_settings"].get(
            "default_format", default_format)
        default_threshold = config["muw_settings"].getint(
            "default_threshold", default_threshold)
    else:
        config["muw_settings"] = {
            "default_number": 10,
            "default_start": 0,
            "default_format": "json",
            "default_threshold": 1
        }
        f = open("config.conf", "w")
        config.write(f)
        f.close()
    if "muw_stopwords" in config.sections():
        for i in config["muw_stopwords"]:
            stopwords[i] = str.lower(config["muw_stopwords"].get(i)).replace(
                "[", "").replace("]", "").replace(" ", "").replace('"', "").split(",")
    return config

# Variables


def parse_args():
    # Argument Parsing
    parser = argparse.ArgumentParser(
        prog='Most Used Words',
        description='A very basic tool that let\'s you get the most used word in a text or file.',
        epilog='Configuration is defined in config.conf,    MUW by Ryan Ducret')

    parser.add_argument('-f', '--file', help="Input file to read text from.",
                        type=str)

    parser.add_argument('-d', '--directory', help="Processes every file in this directory independently.",
                        type=str)

    parser.add_argument('-i', '--input', help="Input text.",
                        type=str)

    parser.add_argument('-o', '--output', help="Specifies the path to an output file or directory if using -d.",
                        type=str)

    parser.add_argument('-of', '--output-format', help=f"Specifies the format to use for the output. (default : {default_format}) (does not affect the extension except if -d and -o are used)",
                        type=str, default=default_format, choices=["json", "xml"])

    parser.add_argument('-n', '--number', help=f"Specifies the number of words to get the count of from the start argument. (default {default_number}, gets the {default_number} most used words) (if zero, shows count for every word)",
                        type=int, default=default_number)

    parser.add_argument('-s', '--start', help=f"Specifies the starting number from wich to get the N^th most used words. (default {default_start}, if 10 with n = 10 would show the 10th to 19th most used words)",
                        type=int, default=default_start)

    parser.add_argument('-sw', '--stopwords', help="Specifies to remove supplied language specific stopwords (such as 'a' 'the' 'wich' etc.) (defined by languages in config.conf)",
                        type=str, choices=list(stopwords.keys()))

    parser.add_argument('-t', '--threshold', help=f"Specifies the minimum number of word occurences at wich words will be added to output (default {default_threshold})",
                        type=int, default=default_threshold)

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

    if args.threshold < 1:
        raise ValueError(
            f"Threshold supplied ({args.threshold}) is invalid, number must be at least 1.")

    if not args.file and not args.input and not args.directory:
        raise SyntaxError(
            f"You must supply an input either a file (-f <filenae>), a text (-i <text>), or a directory (-d <directory>).")
    if args.file and args.input and args.directory:
        raise SyntaxError(
            f"You must supply at most one input.")
    
    if args.directory :
        if not os.path.exists(args.directory) :
            raise RuntimeError(f"Directory {args.directory} not found.")
        
        if len(next(os.walk(args.directory))[2]) < 1 :
            raise RuntimeError(f"Directory {args.directory} has no files.")
        
        if args.directory and args.output:
            if os.path.exists(args.output) and os.path.isdir(args.output):
                pass
            elif os.access(os.path.dirname(args.output), os.W_OK):
                os.mkdir(args.output)
            else:
                raise RuntimeError(f"Could not find output directory {args.output} and could not create it.")
            

    global verbose
    verbose = args.verbose

    return args


def read_file(filename: str):
    f = open(filename, 'r')
    file_data = ''.join(f.readlines())  # Concatinating lines to a big text
    f.close()
    return file_data


def remove_all_non_alpha(input_text: str):
    return ''.join([i for i in input_text if (i.isalpha() or i == " ")])
