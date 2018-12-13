"""
input: sorted bed
output: map to gtf_bed file
get the distribution of the reads, in CDS, intron, 3utr, 5utr, whole, exons

Usage:
input given:  /archive2/tmhyxb9/FBL/fastq/rmUMI/MAPPING_EXON/tophat_exon/
structure: /archive2/tmhyxb9/FBL/fastq/rmUMI/MAPPING_EXON/tophat_exon/tophat/ctr/sortedBed/sorted_hits.bed
"""


import sys, os, glob
sys.path.insert(0, "/archive2/tmhyxb9/ToolBox")
import pandas as pd
import cmd


def map_gtf_bed(inputDir, gtf, sampleName):
    gtf_file = "/archive2/tmhyxb9/ref_data/hg19/hg19_genomicFeatureTable/hg19_UCSC_geneTable/hg19_ucsc_" + gtf
    outputFname = sampleName + "_" + gtf + ".bed"
    cmd0 = "module load bedops/2.4.35"
    cmd1 = "cd " + inputDir
    cmd2 = "bedops --element-of 1 sorted_hits.bed " + gtf_file + " > " + outputFname
    cmd3 = "wc -l " + outputFname
    cmd7 = "wc -l " + outputFname + " >> stats.txt"
    cmds = [cmd0, cmd1, cmd2, cmd3, cmd4, cmd5, cmd6, cmd7]
    return cmds


def main():
    projectDir = sys.argv[1] + "tophat"  # /archive2/tmhyxb9/FBL/fastq/rmUMI/MAPPING_EXON/tophat_exon/
    samples = os.listdir(projectDir)
    gtfBeds = ["CDS", "5UTR", "3UTR", "exon", "intron", "whole"]
    for sample in samples:
        inputDir = os.path.join(projectDir,sample,"sortedBed")
        for gtf in gtfBeds:
            cmds = map_gtf_bed(inputDir, gtf, sample)
            binPath = os.path.join(projectDir,sample,"bins")
            binName = sample + "_" + gtf
            # cmd.generate_pbs(cmds, binName, binPath)
            cmd.generate_submit_pbs(cmds, binName, binPath)
    pass


if __name__ == "__main__":
    main()





