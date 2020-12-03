"""Filter trained weight data by id
    The script filters TW data by id. Input directory contains TW data
    The result is saved in output directory. Id list can be found in filter.cfg
    that should be placed in the script directory

    All of *.txt files in output will be overwritten respectevly by their input names
"""

import glob 
import argparse
import os 
import sys

fpattern = '*.txt'
config = 'filter.cfg'

def script_run():
    options = parse_args()
    os.makedirs(options.output, exist_ok=True)

    files = glob.glob(os.path.join(options.input,fpattern))
    ids = get_ids(options.conf)
    for file in files:
        filtredlines = filter_file(file, ids)    
        if not options.onlyfilled or filtredlines:
            filepath = os.path.join(options.output, file.split('/')[-1])
            print(filepath)
            write_file(filepath, filtredlines)


def parse_args(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(
        description=sys.modules[__name__].__doc__)

    parser.add_argument("input", type=str, help="Input data directory")
    parser.add_argument("output", type=str, help="Output data directory")
    parser.add_argument("--conf", type=str, default=config, help="File that contains required ids")
    parser.add_argument("--onlyfilled", help="Removes empty files", action="store_true")

    return parser.parse_args(args)

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
