
import os , sys
import pandas as pd
import glob
import os.path
pd.set_option("display.max_column", 100)

def fastq_dump(file, srr, p, bin_dir, fastq_dir):
    bin_file = os.path.join(bin_dir, "fastq_"+ srr)
    pbs = open(bin_file + ".pbs", "w")
    pbs.write("#!/bin/bash\n")
    pbs.write("#PBS -r n\n")
    pbs.write("#PBS -o " + bin_file + ".out\n")
    pbs.write("#PBS -e " + bin_file + ".err\n")
    pbs.write("#PBS -m e\n")
    pbs.write("#PBS -M ybu2@houstonmethodist.org\n")
    pbs.write("#PBS -l walltime=96:00:00\n")
    pbs.write("#PBS -l nodes=1:ppn=8\n")
    pbs.write("#PBS -l pmem=6000mb\n")
    pbs.write("#PBS -q mediummem\n")
    pbs.write("#PBS -q default\n")
    pbs.write("cd " + fastq_dir + "/" + "\n")
    pbs.write("mkdir " + srr + "\n")
    if p == "SINGLE":
        pbs.write("/archive2/tmhyxb9/tools/sratoolkit.2.9.0-centos_linux64/bin/fastq-dump -O " + fastq_dir + "/" + srr  + "/ -B " + file +  "/ \n")
    elif p == "PAIRED":
        pbs.write("/archive2/tmhyxb9/tools/sratoolkit.2.9.0-centos_linux64/bin/fastq-dump -O " + fastq_dir + "/" + srr  + "/ -B --split-3 " + file + "/ \n")
    pbs.close()
    os.system('qsub '+bin_file+ ".pbs")
    return


def main(dir):
    srr_dir = os.path.join(os.getcwd(), dir, "SRR")
    index_file = os.path.join(dir, "SraRunTable.txt")
    file_info = pd.read_csv(index_file, sep="\t", index_col="Run")
    bin_dir = os.path.join(os.getcwd(), dir, "fastq_bin")
    if not os.path.exists(bin_dir):
        os.mkdir(bin_dir)
    fastq_dir = os.path.join(os.getcwd(), dir, "fastq")
    if not os.path.exists(fastq_dir):
        os.mkdir(fastq_dir)
    for file in glob.glob(srr_dir + "/*"):
        srr = os.path.basename(file)
        p = file_info.loc[srr, "LibraryLayout"]
        fastq_dump(file, srr, p, bin_dir, fastq_dir)
    return


if __name__ == "__main__":
    main(sys.argv[1])



## python fastq_dump.py ADAR_CLIP/
## python fastq_dump.py iCLIP_ezh2_hct116/
