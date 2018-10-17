#####wget geo dataset in queue
### create a geodataset folder, goto the same layer, copy the get_geo inside
### run python get_geo geodataset_dir
## automatically create geo_bin and srr folder.

import os , sys, os.path
import pandas as pd

def wget_geo(srr, srr_dir, bin_dir):
    bin_file = os.path.join(bin_dir , str(srr))
    pbs = open(bin_file +".pbs", "w")
    pbs.write("#!/bin/bash\n")
    pbs.write("#PBS -r n\n")
    pbs.write("#PBS -o " + bin_file + ".out\n")
    pbs.write("#PBS -e " + bin_file + ".err\n")
    pbs.write("#PBS -m e\n")
    pbs.write("#PBS -M ybu2@houstonmethodist.org\n")
    pbs.write("#PBS -l walltime=96:00:00\n")
    pbs.write("#PBS -l nodes=1:ppn=8\n")
    pbs.write("#PBS -l pmem=16000mb\n")
    pbs.write("##PBS -q mediummem\n")
    pbs.write("#PBS -q default\n")
    pbs.write("cd "+ srr_dir + "/" + "\n")
    pbs.write("wget https://sra-download.ncbi.nlm.nih.gov/srapub/"+str(srr) + "\n")
    pbs.close()
    os.system('qsub '+ bin_file + ".pbs")
    return


def main(SRR_list_dir):
    srr_list_f = os.path.join(SRR_list_dir, "SRR_Acc_List.txt")
    srr_list = pd.read_table(srr_list_f, sep="\t", header=None)
    bin_dir = os.path.join(os.getcwd(), SRR_list_dir, "geo_bin")
    if not os.path.exists(bin_dir):
        os.mkdir(bin_dir)
    srr_dir = os.path.join(os.getcwd(), SRR_list_dir, "SRR")
    if not os.path.exists(srr_dir):
        os.mkdir(srr_dir)
    srrList = srr_list.iloc[:, 0].tolist()
    for srr in srrList:
        wget_geo(srr, srr_dir, bin_dir)
    return


if __name__ == "__main__":
    main(sys.argv[1])


### module load python/2.7.11
### python get_geo.py ADAR_CLIP/
### python get_geo.py iCLIP/
### python get_geo.py ezh2_chipseq_mus/
### python get_geo.py iclip_seq_mus/
