
import sys, os, glob
sys.path.insert(0, "/archive2/tmhyxb9/ToolBox")
import pandas as pd
import cmd


def write_stat_file(projectDir, outputFile):
    if os.path.exists(outputFile):
        os.remove(outputFile)
    with open(outputFile, "a") as StatF:
        inputFiles = os.path.join(projectDir, "*", "bins", "*.out")
        for inputFile in glob.glob(inputFiles):
            print inputFile
            with open(inputFile, "r") as inputF:
                for line in inputF:
                    print line
                    StatF.write(line)
    pass


def calculate(outputFile, sample):
    df = pd.read_csv(outputFile, sep=" ", header=None, index_col=1)
    subDF = df[df.index.str.contains(sample)]
    subDF['label'] = subDF.index.str.extract('.+_(.+).bed')
    cds = subDF.ix[subDF["label"] == "CDS", 0].values
    exons = subDF.ix[subDF["label"] == "exon", 0].values
    introns = subDF.ix[subDF["label"] == "intron", 0].values
    UTR5 = subDF.ix[subDF["label"] == "5UTR", 0].values
    UTR3 = subDF.ix[subDF["label"] == "3UTR", 0].values
    whole = subDF.ix[subDF["label"] == "whole", 0].values

    all = float(UTR5 + UTR3 + cds + introns)
    UTR5 = float(UTR5/all)
    UTR3 = float(UTR3/all)
    CDS = float(cds/all)
    intron = float(introns / all)
    # for information
    exon = float(exons/all)
    diff = whole - all

    print sample
    print "5UTR Percentage  ",UTR5
    print "3UTR Percentage  ",UTR3
    print "CDS Percentage   ", CDS
    print "intron percentage    ", intron

    # print "whole value  ", whole
    # print "exon percentage  ", exon
    # print "exon value   ", exons
    # print "intron value ", introns
    # print "exon+intron  ", all
    # print "whole - (intron+exon)    ", diff
    pass


def main():
    projectDir = sys.argv[1]+ "tophat"  # /archive2/tmhyxb9/FBL/fastq/rmUMI/MAPPING_EXON/tophat_exon/
    outputFile = os.path.join(projectDir, "..", "Distribution_Stats.txt")
    samples = os.listdir(projectDir)
    write_stat_file(projectDir, outputFile)
    for sample in samples:
        calculate(outputFile, sample)
    pass


if __name__ == "__main__":
    main()
