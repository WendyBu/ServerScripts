import pandas as pd
import numpy as np
import os, sys, glob, os.path
import math
from matplotlib import pyplot as plt


def get_output_filename(inputfile, outputDir):
    basename = os.path.basename(inputfile)
    output_filename = "rmUMI_" + basename
    output_full_filename = os.path.join(outputDir, output_filename)
    return output_full_filename


def getLineNum(inputFile):
    with open(inputFile, 'r') as f:
        num_lines = sum(1 for line in f)
        num_fastq = num_lines/4
        print "total number of lines:", num_lines
        print "total number of fastq records:", num_fastq
    return num_lines, num_fastq


def SaveStats(data, outputFileName):    # save every fastq length as a file
    dataX = np.array(data)
    outputFile = os.path.splitext(outputFileName)[0] + ".txt"
    np.savetxt(outputFile, dataX, delimiter="\n", fmt="%d")
    pass


def writeTheUniqueFile(fastqRecordNum, lines, outputFileName):
    fastqReadLen = []
    lineNumbers = [(record*4+1) for record in fastqRecordNum]
    if os.path.exists(outputFileName):
        os.remove(outputFileName)
    for line in lineNumbers:
        with open(outputFileName, "a+") as outF:
            outF.write(lines[line-1])   # FASTQ id line
            fastq = lines[line]
            fastq = fastq[0:-6]  # trim the last 5 nts
            fastqReadLen.append(len(fastq))
            outF.write(fastq +"\n")      # fastq line
            outF.write(lines[line + 1])  # fastq strand line
            line4 = lines[line + 2]
            line4 = line4[0:-6]
            outF.write(line4 + "\n")       # fastq quality line has to be the same length as sequence line
    SaveStats(fastqReadLen, outputFileName)
    pass


def Find_unique_fastq_index(inputFile, outputFile):
    lineNum, fastqNum = getLineNum(inputFile)
    with open(inputFile, 'r') as f:
        lines = f.readlines()
        fastqLines = [lines[i*4+1] for i in range(fastqNum)]
        # fastqLines = [line[0:-6] for line in fastqLines]   # if without the umi label, how many unique reads existed
        fastqLines = np.array(fastqLines)
        unique_fastq, unique_recordNum = np.unique(fastqLines, return_index=True)
        print "unique fastq reads ratio:", unique_fastq.size / float(fastqNum)
        print "Number of unique fastq reads:", unique_recordNum.size
        uniqueFastqRecordNum = unique_recordNum.tolist()
        writeTheUniqueFile(uniqueFastqRecordNum, lines, outputFile)
    pass


def main():
    # input and output filenames
    input_file = sys.argv[1]
    output_dir = sys.argv[2]
    output_filename = get_output_filename(input_file, output_dir)
    Find_unique_fastq_index(input_file, output_filename)    # unique fastq Records number
    pass


if __name__ == "__main__":
    main()



# input file : /archive2/tmhyxb9/FBL/fastq/Ctr_sh/control.fq
# python removeUMI.py /archive2/tmhyxb9/FBL/fastq/Ctr_sh/sample48.fq /archive2/tmhyxb9/FBL/fastq/rmUMI/fastq/
