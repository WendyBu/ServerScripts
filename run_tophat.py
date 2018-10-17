### batch run tophat#
# create date 10-11-2018
# give the srr name and folder location, run tophat
# result stored in project_root/tophat/SRRXXX

import os , sys
import pandas as pd
import glob, os.path

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
    pbs.write("#PBS -l pmem=6000mb\n")
    pbs.write("#PBS -q mediummem\n")
    pbs.write(cmd + "\n")
    pbs.close()
    os.system('qsub ' + binAbsName + ".pbs")
    pass


def run_tophat(full_input_path, project_root, srrName):
    output_dir = os.path.join(project_root, "tophat", srrName)
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    input_files = os.listdir(full_input_path)
    if len(input_files) == 2:
        file1 = os.path.join(full_input_path, input_files[0])
        file2 = os.path.join(full_input_path, input_files[1])
        cmd = "tophat --mate-std-dev 200 -p 8 -r 203 -o " + output_dir + " /archive2/tmhyxb9/ref_data/hg19/bowtie2/hg19 " + file1 + " " + file2 + "\n"
    elif len(input_files) == 1:
        file = os.path.join(full_input_path, input_files[0])
        cmd = "tophat --mate-std-dev 200 -p 8 -r 203 -o " + output_dir + " /archive2/tmhyxb9/ref_data/hg19/bowtie2/hg19 " + file  + "\n"
    else:
        "FASTQ files are not correct!"
    return cmd


def main():
    for arg in sys.argv[1:]:
        cwdir = os.getcwd()
        full_input_path = os.path.join(cwdir, arg)
        fastq_dir = os.path.abspath(os.path.join(full_input_path, os.pardir))
        project_root = os.path.abspath(os.path.join(fastq_dir, os.pardir))
        command = run_tophat(full_input_path, project_root, arg) # use absolute path for each file
        binpath = os.path.join(project_root, "tophat_bin")
        if not os.path.exists(binpath):
            os.mkdir(binpath)
        generate_pbs(command, arg, binpath)
    pass


if __name__ == "__main__":
    main()




# python /archive2/tmhyxb9/ToolBox/run_tophat.py SRR5720006 SRR5720007 SRR5720008 SRR5720009
# python /archive2/tmhyxb9/ToolBox/run_tophat.py HT37_MMC  HT42_MMC  HT_37C  HT_42C  SNU37MMC  SNU42MMC  SNU_37C  SNU_42C
# project_root/fastq/SRRXXX/SRRXXX.fastq
# need to make a directory project_root/tophat/