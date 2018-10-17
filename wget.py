"""
wget tools
wget using through server.
go to the folder, eg CCLE/CNV,
two input options: one is single file link: eg  https://data.broadinstitute.org/ccle_legacy_data/dna_copy_number/CCLE_copynumber_2013-12-03.seg.txt
second is txt file with every file link in one row:  CCLE/CNV/downloadlinks.txt
every file wget will generate one pbs.
structure: cwd/Downloads/bins
"""

import os , sys, os.path
import pandas as pd

def wget_file(address, binPath, basename, downloadPath):
    pbsName = os.path.join(binPath, basename)
    pbs = open(pbsName + ".pbs", "w")
    pbs.write("#!/bin/bash\n")
    pbs.write("#PBS -r n\n")
    pbs.write("#PBS -o " + pbsName + ".out\n")
    pbs.write("#PBS -e " + pbsName + ".err\n")
    pbs.write("#PBS -m e\n")
    pbs.write("#PBS -M ybu2@houstonmethodist.org\n")
    pbs.write("#PBS -l walltime=96:00:00\n")
    pbs.write("#PBS -l nodes=1:ppn=8\n")
    pbs.write("#PBS -l pmem=16000mb\n")
    pbs.write("##PBS -q mediummem\n")
    pbs.write("#PBS -q default\n")
    pbs.write("cd " + downloadPath + "\n")
    pbs.write("wget "+ address + "\n")
    pbs.close()
    os.system('qsub '+ pbsName + ".pbs")
    return


def main(argv1):
    if not os.path.exists("Downloads"):
        os.mkdir("Downloads")
    binPath = os.path.join(os.getcwd(), "Downloads", "bins")
    if not os.path.exists(binPath):
        os.mkdir(binPath)
    downloadPath = os.path.join(os.getcwd(), "Downloads")

    if os.path.islink(argv1):
        basename = os.path.basename(argv1)
        wget_file(argv1, binPath, basename, downloadPath)
    elif os.path.isfile(argv1):
        lines = [line.rstrip('\n') for line in open(argv1)]
        for link in lines:
            basename = os.path.basename(link)
            wget_file(link, binPath, basename, downloadPath)
    return


if __name__ == "__main__":
    main(sys.argv[1])


# python /archive2/tmhyxb9/ToolBox/wget.py https://data.broadinstitute.org/ccle_legacy_data/dna_copy_number/CCLE_copynumber_2013-12-03.seg.txt
# /archive2/tmhyxb9/CCLE/CNV $ python /archive2/tmhyxb9/ToolBox/wget.py downloadlinks.txt


