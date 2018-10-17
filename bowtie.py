###  data not from geo. allready data saved as fastq.gz
###  step1: unzip first
###  step2: run tophat

import os, sys, os.path
import pandas as pd
import glob

def bowtie(filename):
    base = os.path.basename(filename).split(".")[0]
    dir = os.path.dirname(filename)
    binpath = os.path.join("chipbin","bowtie_"+ base)
    pbs = open(binpath +".pbs", "w")
    pbs.write("#!/bin/bash\n")
    pbs.write("#PBS -r n\n")
    pbs.write("#PBS -o " + binpath + ".out\n")
    pbs.write("#PBS -e " + binpath + ".err\n")
    pbs.write("#PBS -m e\n")
    pbs.write("#PBS -M ybu2@houstonmethodist.org\n")
    pbs.write("#PBS -l walltime=96:00:00\n")
    pbs.write("#PBS -l nodes=1:ppn=8\n")
    pbs.write("#PBS -l pmem=6000mb\n")
    pbs.write("#PBS -q mediummem\n")
    pbs.write("cd "+ dir + "\n")
    pbs.write("bowtie -m 1 -p 8 --chunkmbs 512 --best /archive2/tmhyxb9/ref_data/hg19/bowtie/hg19 " + base + ".fastq " + "/archive2/tmhyxb9/AY/chip_bowtie/" + base + ".bowtie"  + "\n")
    pbs.close()
    os.chdir("/archive2/tmhyxb9/AY/")
    os.system('qsub '+ binpath + '.pbs')
    return



#bowtie -m 1 -p 8 --chunkmbs 512 --best /home/tmhdxz9/scratch/reference/ref_data/hg19/bowtie/hg19 SRR6321859.fastq GSM2864676_mm9_brain_h3k27me3.bowtie

def main():
    for file in glob.glob("/archive2/tmhyxb9/AY/CHIP/*/*"):
        bowtie(file)
    return


if __name__ == "__main__":
    main()

