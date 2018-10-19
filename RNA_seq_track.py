"""
RNA-seq, making track, generate the bigwig file.
"remember to load danpos"
"""

import os , sys
import pandas as pd
import glob, os.path

def generate_pbs(cmd0, cmd1, cmd2, cmd3, binName, binPath):
    """
    :param cmd: command,
    :param binName:
    :param binPath:
    :return: pbs filename
    """
    binAbsName = os.path.join(binPath, binName)
    pbs = open(binAbsName + ".pbs", "w")
    pbs.write("#!/bin/bash\n")
    pbs.write("#PBS -r n\n")
    pbs.write("#PBS -o " + binAbsName + ".out\n")
    pbs.write("#PBS -e " + binAbsName + ".err\n")
    pbs.write("#PBS -m e\n")
    pbs.write("#PBS -M ybu2@houstonmethodist.org\n")
    pbs.write("#PBS -l walltime=96:00:00\n")
    pbs.write("#PBS -l nodes=1:ppn=8\n")
    pbs.write("#PBS -l pmem=6000mb\n")
    pbs.write("#PBS -q mediummem\n")
    pbs.write("module load danpos \n")
    pbs.write(cmd0 + "\n")
    pbs.write(cmd1 + "\n")
    pbs.write(cmd2 + "\n")
    pbs.write(cmd3 + "\n")
    pbs.close()
    os.system('qsub ' + binAbsName + ".pbs")
    pass


def generate_track_cmd(sampleName, trackDir, bam):
    genomeFile = "/archive2/tmhyxb9/ref_data/hg19/hg19.chrom.sizes.xls"
    cmd0 = "cd " + trackDir
    cmd1 = "/archive2/tmhyxb9/tools/bedtools2/bin/genomeCoverageBed -ibam " + bam + " -split -bg -g " + genomeFile + " >accepted_hits.bg"
    cmd2 = "python /archive2/tmhyxb9/tools/lib/bedGraphLib.py nor2total accepted_hits.bg 50000000"
    cmd3 = "/archive2/tmhyxb9/tools/bin/bedGraphToBigWig accepted_hits.nor.bg " + genomeFile +  " " + sampleName + ".nor.bw"
    return cmd0, cmd1, cmd2, cmd3


def generate_ucsc_trackTxt(sampleName, bwPath_Cig):
    trackTxt = "track type=bigWig name=\'" + sampleName + "\' description=\"\" visibility=2  db=\"hg19\" color=0,0,255 maxHeightPixels=60:60:60 windowingFunction=maximum viewLimits=0:80 autoScale=off bigDataUrl=http://cigwiki.houstonmethodist.org/trackhub/yiwen/"+ bwPath_Cig + sampleName + ".nor.bw"
    return trackTxt


def main(project_root):
    # create track/ and track_bin/
    f = open('UCSC_trackTxt.txt', 'w+')                                                     # step2
    track_dir = os.path.join(project_root, "track")
    if not os.path.exists(track_dir):
        os.mkdir(track_dir)
    track_bin = os.path.join(project_root, "track_bin")
    if not os.path.exists(track_bin):
        os.mkdir(track_bin)
    bams = os.path.join(project_root, "tophat/*", "accepted_hits.bam")
    for bam in glob.glob(bams):
        bam_track_dir = os.path.split(bam)[0].replace("tophat", "track")
        if not os.path.exists(bam_track_dir):
            os.mkdir(bam_track_dir)
        sampleName = bam_track_dir.split("/")[-1]
        # cmd0, cmd1, cmd2, cmd3 = generate_track_cmd(sampleName, bam_track_dir, bam)        ## step1:generate bw
        # generate_pbs(cmd0, cmd1, cmd2, cmd3, binName = sampleName, binPath = track_bin)    ## step1: generate bw
        bwPath = "MMC/"                                                                      # step2
        ucscTrack = generate_ucsc_trackTxt(sampleName, bwPath_Cig=bwPath)                     # step2
        f.write("%s\n" % ucscTrack)                                                            # step2
    f.close()                                                                                  # step2
    pass

if __name__ == "__main__":
    main(sys.argv[1])



# giving the project_dir_name, run all the samples inside tophat of it
# python /archive2/tmhyxb9/ToolBox/RNA_seq_track.py /archive2/tmhyxb9/MMC/
# excute step1
# move the bw file into cigwiki
# excute step2 commands