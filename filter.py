"""Filter trained weight data by id
    The script filters TW data by id. Input directory contains TW data
    The result is saved in output directory. Id list can be found in config directory. 

    In order to use the script with default args you should do the following:
    - place data directory named TW in the same directory where the script is
    - create filter.cfg file and fill it with ids separated by space

    The result will be placed in ./filtered directory 
"""

import glob 
import argparse
import os 
import sys

rootdir = 'TW'
filtdir = 'filtered'
fpattern = '*.txt'
config = 'filter.cfg'

def script_run():
    options = parse_args()
    prepare_dirs(os.path.join(filtdir, options.input), fpattern)  

    files = glob.glob(os.path.join(options.input,fpattern))
    ids = get_ids(options.conf)
    for file in files:
        filtredlines = filter_file(file, ids)    
        if options.allfiles or filtredlines:
            filepath = os.path.join(filtdir, file)
            write_file(filepath, filtredlines)


def parse_args(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(
        description=sys.modules[__name__].__doc__)

    parser.add_argument("--input", type=str, default=rootdir, help="Input data directory")
    parser.add_argument("--output", type=str, default=filtdir, help="Output data directory")
    parser.add_argument("--conf", type=str, default=config, help="File that contains required ids")
    parser.add_argument("--allfiles", help="Add empty files", action="store_true")

    return parser.parse_args(args)

def prepare_dirs(path, pattern):
    os.makedirs(path, exist_ok=True)
    files = glob.glob(os.path.join(path, pattern))
    for file in files:
        os.remove(file)

def filter_file(file, ids):
    lines = []
    with open(file) as finput:
        for line in finput:
            id = line.split(' ')[0]
            if id in ids:
                lines.append(line)
    return lines     

def write_file(file, lines):
    with open(file, "w") as foutput:
        foutput.write("".join(lines))

def get_ids(file):
    res = []
    with open(file, "r") as finput:
        res = finput.readline().split(" ")
    return res

if __name__ == "__main__":
    script_run()
