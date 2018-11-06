###  data not from geo. allready data saved as fastq.gz
###  step1: unzip first
###  step2: run tophat
###  step3: run bowtie

import os, sys, os.path
import pandas as pd
import glob

def generate_pbs(cmd, binName, binPath):
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
    pbs.write("#PBS -l pmem=10000mb\n")
    pbs.write("#PBS -q mediummem\n")
    pbs.write("module load python/2.7.11\n")
    pbs.write(cmd + "\n")
    pbs.close()
    os.system('qsub ' + binAbsName + ".pbs")
    pass


def bowtie_cmd(file, outputDir):
    cmd1 = "bowtie -m 1 -p 8 --chunkmbs 512 --best /archive2/tmhyxb9/ref_data/hg19/bowtie/hg19 "
    cmd2 = file + " "
    cmd3 = outputDir + "/"
    cmd4 = os.path.basename(file).split(".")[0] + ".bowtie"
    cmd = cmd1 + cmd2 + cmd3 + cmd4
    return cmd

#bowtie -m 1 -p 8 --chunkmbs 512 --best /home/tmhdxz9/scratch/reference/ref_data/hg19/bowtie/hg19 SRR6321859.fastq GSM2864676_mm9_brain_h3k27me3.bowtie

def main():
    fastq_dir = sys.argv[1]
    if not os.path.exists("bowtie"):
        os.mkdir("bowtie")
    outputdir = os.path.join(os.getcwd(), "bowtie")
    for file in glob.glob(fastq_dir + "/*/*.fastq"):
        command = bowtie_cmd(file, outputdir)
        binPath = os.path.join(os.getcwd(), "bowtie_bin")
        if not os.path.exists(binPath):
            os.mkdir(binPath)
        binName = os.path.basename(file).split(".")[0] + "_bowtie"
        generate_pbs(command, binName, binPath)
    return


if __name__ == "__main__":
    main()


# cd project root
# root/fastq/sampleID/sample.fastq  ----structure.
# python /archive2/tmhyxb9/ToolBox/chip_seq/bowtie.py  /archive2/tmhyxb9/Palb/Palb_pol2/fastq(input)