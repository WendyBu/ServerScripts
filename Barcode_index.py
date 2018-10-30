import pandas as pd
import numpy as np
import os, sys, glob, os.path
import cmd


def get_label(filename):
    """
    :param filename: input_file_name
    :return: all the labels as a list; label lenths
    """
    labels = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines[0::4]:
            line = line.strip('\n')
            label = line.split(" ")[-1]
            label = label.split(':')[-1]
            labels.append(label)
        label_index = list(set(labels))  # find how many kinds of indexes in total in the fastq file
        label_num = len(label_index)
    return label_index, label_num


def generate_newFile(input_fname, label, output_fname):
    with open(input_fname, 'r') as inputF:
        lines = inputF.readlines()
        with open(output_fname, 'a+') as outF:
            for lineNum, line in enumerate(lines):
                if line.endswith(label+"\n"):
                    outF.write(lines[lineNum])
                    outF.write(lines[lineNum+1])
                    outF.write(lines[lineNum + 2])
                    outF.write(lines[lineNum + 3])
        # newfileLineNum = sum(1 for newline in open(output_fname))
        # print newfileLineNum
    pass


def main():
    input_file = sys.argv[1]
    inputbase = os.path.basename(input_file).split(".")[0]
    output_dir = os.path.join(".", inputbase)
    print output_dir
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    label_index, label_num = get_label(input_file)
    for label in label_index:
        print label
        new_fname = os.path.join(inputbase, label+".fq")
        generate_newFile(input_file, label, new_fname)
    pass


if __name__ == "__main__":
    main()
    
    
    
    
# python /archive2/tmhyxb9/ToolBox/Barcode_index.py sample_ribo.fq
## output several files depending on barcode 