# Most-Used-Words

usage: Most Used Words [-h] [-f FILE] [-i INPUT] [-o OUTPUT] [-of {json,xml}] [-n NUMBER] [-s START] [-v]

A very basic tool that let's you get the most used word in a text or file.

optional arguments:

  -h, --help            show this help message and exit
  
  -f FILE, --file FILE  Input file to read text from.
  
  -i INPUT, --input INPUT
                        Input text.
                        
  -o OUTPUT, --output OUTPUT
                        Specifies the path to an output file.
                        
  -of {json,xml}, --output-format {json,xml}
                        Specifies the format to use for the output. (default : json) (does not affect the extension)
                        
  -n NUMBER, --number NUMBER
                        Specifies the number of words to get the count of from the start argument. (default 10, gets the 10 most used words) (if zero, shows count for every word)
                        
  -s START, --start START
                        Specifies the starting number from wich to get the N^th most used words. (default 1, if 10 with n = 10 would show the 10th to 19th most used words)
                        
  -v, --verbose

Configuration is defined in config.conf, MUW by Ryan Ducret
