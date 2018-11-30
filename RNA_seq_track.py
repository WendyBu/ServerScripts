"""
RNA-seq, making track, generate the bigwig file.
"remember to load danpos"
"""

import sys, os, glob, os.path
sys.path.insert(0, "/archive2/tmhyxb9/ToolBox")
import pandas as pd
import cmd


def cmds_bamToBigWig(sampleName, trackDir, bam):
    genomeFile = "/archive2/tmhyxb9/ref_data/hg19/hg19.chrom.sizes.xls"
    cmd0 = "module load danpos"
    cmd1 = "cd " + trackDir
    cmd2 = "mkdir " + sampleName
    cmd3 = "cd " + sampleName
    cmd4 = "/archive2/tmhyxb9/tools/bedtools2/bin/genomeCoverageBed -ibam " + bam + " -split -bg -g " + genomeFile + " >accepted_hits.bg"
    cmd5 = "python /archive2/tmhyxb9/tools/lib/bedGraphLib.py nor2total accepted_hits.bg 50000000"
    cmd6 = "/archive2/tmhyxb9/tools/bin/bedGraphToBigWig accepted_hits.nor.bg " + genomeFile +  " " + sampleName + ".nor.bw"
    cmds = [cmd0, cmd1, cmd2, cmd3, cmd4, cmd5, cmd6]
    return cmds


def tophatBam_BigWig(project_root):
    """
    input: project root. real input is the accepted_hits.bam
    structure: the project root/tophat/sampleName/accepted_bam
    :param project_root:
    :return: bigwig file for making track
    """
    # create track/, track_bin/ , create file  UCSC_trackTxt.txt
    track_dir = os.path.join(project_root, "track")
    if not os.path.exists(track_dir):
        os.mkdir(track_dir)
    track_bin = os.path.join(project_root, "track_bin")
    if not os.path.exists(track_bin):
        os.mkdir(track_bin)

    # find accepted_hits.bam files
    bams = os.path.join(project_root, "tophat/*", "accepted_hits.bam")
    for bam in glob.glob(bams):
        sample_name = bam.split("/")[-2]   # get sample name, one level up from .bam
        cmds = cmds_bamToBigWig(sample_name, track_dir, bam)
        binname = sample_name + "_track"
        # cmd.generate_pbs(cmds=cmds, binName=binname, binPath=track_bin)
        cmd.generate_submit_pbs(cmds=cmds, binName=binname, binPath=track_bin)
    pass


def generate_trackFile(cigiwig_dirName, sampleNames):
    with open('UCSC_trackTxt.txt', 'w+') as f:
        for sampleName in sampleNames:
            trackTxt = "track type=bigWig name=\'" + sampleName + "\' description=\"\" visibility=2  db=\"hg19\" color=0,0,255 maxHeightPixels=60:60:60 windowingFunction=maximum viewLimits=0:80 autoScale=off bigDataUrl=http://cigwiki.houstonmethodist.org/trackhub/yiwen/" + cigiwig_dirName + "/" + sampleName + ".nor.bw"
            f.write("%s\n" % trackTxt)
    pass


def main():
    project_root = sys.argv[1]
    cigwiki_dir = sys.argv[2]
    tophatBam_BigWig(project_root)  #step1: generate bigwig (need to move the bw to cigwiki)
    sampleNames = os.listdir(project_root + "/tophat")  #step2 get sample names
    generate_trackFile(cigiwig_dirName=cigwiki_dir, sampleNames=sampleNames)  #step2 make track files
    pass


if __name__ == "__main__":
    main()


# two arguments:  project_root, one layer before tophat/samplename/bamfile;  second is cigwiki folder
# python /archive2/tmhyxb9/ToolBox/RNA_seq_track.py /archive2/tmhyxb9/FBL/RNA_seq/tophat_pair
# python /archive2/tmhyxb9/ToolBox/RNA_seq_track.py /archive2/tmhyxb9/FBL/fastq/rmUMI FBL_ribo_mergeDup
# python /archive2/tmhyxb9/ToolBox/RNA_seq_track.py /archive2/tmhyxb9/FBL/fastq/rmUMI/MAPPING_EXON/tophat_exon FBL_RIBO_ucsc