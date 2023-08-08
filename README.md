# Most-Used-Words

```
usage: Most Used Words [-h] [-f FILE] [-d DIRECTORY] [-i INPUT] [-o OUTPUT] [-of {json,xml}] [-n NUMBER] [-s START] [-sw {english,french}] [-t THRESHOLD] [-v]

A very basic tool that let's you get the most used word in a text or file.

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Input file to read text from.
  -d DIRECTORY, --directory DIRECTORY
                        Processes every file in this directory independently.
  -i INPUT, --input INPUT
                        Input text.
  -o OUTPUT, --output OUTPUT
                        Specifies the path to an output file or directory if using -d.
  -of {json,xml}, --output-format {json,xml}
                        Specifies the format to use for the output. (default : xml) (does not affect the extension except if -d and -o are used)
  -n NUMBER, --number NUMBER
                        Specifies the number of words to get the count of from the start argument. (default 10, gets the 10 most used words) (if zero, shows count for every word)
  -s START, --start START
                        Specifies the starting number from wich to get the N^th most used words. (default 1, if 10 with n = 10 would show the 10th to 19th most used words)
  -sw {english,french}, --stopwords {english,french}
                        Specifies to remove supplied language specific stopwords (such as 'a' 'the' 'wich' etc.) (defined by languages in config.conf)
  -t THRESHOLD, --threshold THRESHOLD
                        Specifies the minimum number of word occurences at wich words will be added to output (default 1)
  -v, --verbose

Configuration is defined in config.conf, MUW by Ryan Ducret
```
