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
import shutil

txtpattern = '*.txt'
jpgpattern = '*.jpg'
config = 'filter.cfg'
labelfile = '_darknet.labels'

def script_run():
    options = parse_args()
    os.makedirs(options.output, exist_ok=True)

    files = glob.glob(os.path.join(options.input, txtpattern))
    ids = get_ids(options.conf)
    idold_to_idcur = write_labelfile(os.path.join(options.input, labelfile), 
        os.path.join(options.output, labelfile), ids)
    for file in files:
        lines = filter_file(file, ids)    
        lines = rewrite_ids(lines, idold_to_idcur)
        if not options.onlyfilled or lines:
            filepath = os.path.join(options.output, os.path.split(file)[1])
            print(f'writing: {filepath}')
            write_file(filepath, lines)

    screenshots = glob.glob(os.path.join(options.input, jpgpattern))
    for screenshot in screenshots:
        print(f'copy: {screenshot}')
        try:
            shutil.copyfile(screenshot, 
                os.path.join(options.output, os.path.split(screenshot)[1]))
        except shutil.SameFileError:
            print(f'didnt copy. The same file {screenshot}')


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

def write_labelfile(input, output, ids):
    # create dict label's id to name from source label file
    idtoname_old = {}
    nametoid_old = {}
    with open(input, "r") as labels:
        n = 0
        for label in labels:
            label = label.rstrip('\n')
            idtoname_old[n] = label
            nametoid_old[label] = n
            n += 1
    
    # create name to id from config file
    idtoname_cur = {} 
    n = 0
    for id in ids:
        idtoname_cur[n] = idtoname_old[int(id)]
        n += 1

    # create a map: id from source file to id made from conf file
    idold_to_idcur = {}
    for i in range(len(ids)):
        idold_to_idcur[nametoid_old[idtoname_cur[i]]] = i
    
    # write new label to file
    with open(output, "w") as out:
        out.write("\n".join(idtoname_cur[i] for i in range(len(ids))))

    return idold_to_idcur

def rewrite_ids(lines, idold_to_idcur):
    for i in range(len(lines)):
        words = lines[i].split(' ')
        words[0] = f"{idold_to_idcur[int(words[0])]} "
        lines[i] = "".join(words)
    return lines

if __name__ == "__main__":
    script_run()
