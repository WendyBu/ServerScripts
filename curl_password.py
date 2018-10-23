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

def main():
    ftp_file = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]

    project_root = os.path.dirname(ftp_file)
    fastq_bin = os.path.join(project_root, "fastq_bin")
    fastq_dir = os.path.join(project_root, "fastq")
    if not os.path.exists(fastq_bin):
        os.mkdir(fastq_bin)
    if not os.path.exists(fastq_dir):
        os.mkdir(fastq_dir)

    # Open a file
    with open(ftp_file) as f:
        ftplist = f.read().splitlines()
        for ftplink in ftplist:
            filename = os.path.split(ftplink)[1]
            cmd = "curl " + ftplink + " --user " + username + ":" + password + " -o ./fastq/" + filename
            generate_pbs(cmd, fastq_bin, filename)
    return


if __name__ == "__main__":
    main()

# python /archive2/tmhyxb9/ToolBox/curl_password.py /archive2/tmhyxb9/FBL/fastq_ftplinks.txt P202SC18100591-01_20181022_guCAtO uKuyzk
# Usage: goto the project root.
# python /archive2/tmhyxb9/ToolBox/curl_password.py /archive2/tmhyxb9/FBL/fastq_ftplinks.txt username password