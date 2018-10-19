import os , sys
import pandas as pd
import glob, os.path

def generate_pbs(cmds, binName, binPath):
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
    for cmd in cmds:
        pbs.write(cmd + "\n")
    pbs.close()
    os.system('qsub ' + binAbsName + ".pbs")
    pass


def trim_adaptor(inputFile):
    out = os.path.split(inputFile)[0]
    outputFile = out + "_trim.fastq"
    cmd0 = "module load fastx-toolkit"
    cmd1 = "fastx_trimmer -f 7 -i " + inputFile +" -o " + outputFile
    cmds = [cmd0, cmd1]
    return cmds
# fastx_trimmer -f 7 -i SRR5720009.fastq -o SRR5720009_trim.fastq  # using absolute path


def main(dirs):
    for dir in dirs:
        cwdir = os.getcwd()
        full_input_dir = os.path.join(cwdir, dir)
        # print full_input_dir
        for file in glob.glob(full_input_dir+"/*.fastq"):
            cmds = trim_adaptor(file)
            binPath = os.path.join(cwdir, os.pardir, "fastq_bin")
            binName = "trim_" + os.path.basename(file).split(".")[0]
            generate_pbs(cmds, binName, binPath)
    pass


if __name__ == "__main__":
    main(sys.argv[1:])

# under tophat, assuming tophat_bin exists. save bin to tophat_bin
# python /archive2/tmhyxb9/RNAediting/ADAR_CLIP/trim_fastq.py SRR5720006 SRR5720007 SRR5720008
