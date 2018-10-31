"""
Input: fastq file. In this case, it is fastq already removed 3 nt from N terminal by "fastx_trimmer -f 4"
split original fastq files into a couple of files by barcode, then remove the barcode and after, match the same length with quality line
"""


import pandas as pd
import numpy as np
import os, sys, glob, os.path


def write_in_file(celltype, lineNum, lines, newline, newline_len, outDir):
    outputFName = os.path.join(outDir, celltype + ".fq")
    with open(outputFName, "a+") as outF:
        outF.write(lines[lineNum - 1])
        outF.write(newline+"\n")
        outF.write(lines[lineNum + 1])
        line4 = lines[lineNum + 2]
        line4 = line4[0:newline_len]  #quality line has to be the same length as sequence line
        outF.write(line4+"\n")
    pass


def remove_barcode(barcode, line):
    newline = list(line.partition(barcode))[0] # remove barcode and following
    return newline, len(newline)


def splitFile(filename, barcodes, outDir):
    with open(filename, 'r') as f:
        lines = f.readlines()
        for lineNum, line in enumerate(lines):
            for cell, barcode in barcodes.iteritems():
                if barcode in line:
                    newLine, newLine_length = remove_barcode(barcode, line)
                    write_in_file(cell, lineNum, lines, newLine, newLine_length, outDir)
                    break
    return lineNum+1


def count_lines(filename):
    num_lines = sum(1 for line in open(filename))
    return num_lines


def main():
    input_file = sys.argv[1]
    output_dir = sys.argv[2]

    # barcode information
    ctr = 'ATCGTAGATCGGAAGAGCACACGTCTGAA'
    ctr = ctr[0:10]  # take the first 10nt to match
    EZH1 = 'AGCTAAGATCGGAAGAGCACACGTCTGAA'
    EZH1 = EZH1[0:10]
    EZH2 = 'CGTAAAGATCGGAAGAGCACACGTCTGAA'
    EZH2 = EZH2[0:10]
    FBL = 'GATCAAGATCGGAAGAGCACACGTCTGAA'
    FBL = FBL[0:10]
    barcodes = {'control':ctr, 'EZHsh1':EZH1, 'EZHsh2':EZH2, 'FBL':FBL}
    totalLineNum = splitFile(input_file, barcodes, output_dir) #split file by barcode

    # count matched records
    matched_lines = 0
    matched_records = 0
    for outputFile in glob.glob(output_dir+"/*"):
        fileLength = count_lines(outputFile)
        matched_lines += fileLength
        matched_records += fileLength/4
        print outputFile, fileLength, fileLength/4
    print "total line number in file:", totalLineNum
    print "total records:", totalLineNum/4
    print "total matched lines:", matched_lines
    print "total matched records:", matched_records
    pass


if __name__ == "__main__":
    main()


# usage:
# python find_barcode.py ./trimN4/sample.fq ./trimN4/RmBarcode/sample
