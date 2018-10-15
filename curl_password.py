## for MMC project, curl with password and username to download fastq files

import os , sys, os.path
import pandas as pd

def generate_pbs(cmd, binPath, binName):
    pbsName = os.path.join(binPath, binName)
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
    pbs.write("#PBS -q mediummem\n")
    pbs.write("#PBS -q default\n")
    pbs.write("cd /archive2/tmhyxb9/MMC\n")
    pbs.write(cmd)
    pbs.close()
    os.system('qsub '+ pbsName + ".pbs")
    return

# curl ftp://128.120.88.242/C202SC18081457/README.txt --user P202SC18081455-01_20181014_Qbqeu9:DoGkOL -o ./README.txt

def main(argv1):
    fastq_bin = "/archive2/tmhyxb9/MMC/fastq_bin"
    # Open a file
    with open(argv1) as f:
        ftplist = f.read().splitlines()
        for ftplink in ftplist:
            filename = os.path.split(ftplink)[1]
            cmd = "curl " + ftplink + " --user P202SC18081455-01_20181014_Qbqeu9:DoGkOL -o ./fastq/" + filename
            generate_pbs(cmd, fastq_bin, filename)
    return


if __name__ == "__main__":
    main(sys.argv[1])

# python /archive2/tmhyxb9/ToolBox/curl_password.py /archive2/tmhyxb9/MMC/fastq_ftplinks.txt