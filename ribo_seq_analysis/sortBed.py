"""
from tophat/sample/accepted_hits.bam
generate the sorted bed.

step1: input preparation: samtools sort bam
module load samtools/1.9
samtools sort filename -o outputfilename

step2: bamtobed
module load bedtool/2.26.0
bedtools bamtobed -i inputfile.bam > output.bed


structure /archive2/tmhyxb9/FBL/fastq/rmUMI/MAPPING_EXON/tophat_exon/tophat/sampleName/accepted_hits.bam
input  /archive2/tmhyxb9/FBL/fastq/rmUMI/MAPPING_EXON/tophat_exon/
output  /archive2/tmhyxb9/FBL/fastq/rmUMI/MAPPING_EXON/tophat_exon/tophat/sampleName/sortedBed/sorted.bed
create  sortedBed folder
binfolder  /archive2/tmhyxb9/FBL/fastq/rmUMI/MAPPING_EXON/tophat_exon/tophat/sampleName/bins/
binName sampleName_bam2bed
"""



import sys, os, glob
sys.path.insert(0, "/archive2/tmhyxb9/ToolBox")
import pandas as pd
import cmd


def generate_cmds(inputDir, outputDir):
    inputBam = os.path.join(inputDir, "accepted_hits.bam")
    cmd0 = "cd " + outputDir
    cmd3 = "module load samtools/1.9"
    cmd4 = "module load bedtool/2.26.0"
    cmd5 = "samtools sort " + inputBam + " -o sorted_hits.bam"   # step1, sort bam
    cmd6 = "bedtools bamtobed -i sorted_hits.bam > sorted_hits.bed"  # step2, convert bam to bed
    cmds = [cmd0, cmd3, cmd4, cmd5, cmd6]
    return cmds


def main():
    projectDir= sys.argv[1] + "tophat"  #/archive2/tmhyxb9/FBL/fastq/rmUMI/MAPPING_EXON/tophat_exon/
    samples = os.listdir(projectDir)
    for sample in samples:
        inputDir = os.path.join(projectDir,sample)
        outputDir = os.path.join(inputDir, "sortedBed")
        if not os.path.exists(outputDir):
            os.mkdir(outputDir)
        cmds = generate_cmds(inputDir=inputDir, outputDir=outputDir)

        binPath=os.path.join(inputDir, "bins")
        if not os.path.exists(binPath):
            os.mkdir(binPath)
        binName=os.path.join(binPath, sample+"_bam2bed")
        # cmd.generate_pbs(cmds, binName, binPath)
        cmd.generate_submit_pbs(cmds, binName, binPath)
    pass


if __name__ == "__main__":
    main()





