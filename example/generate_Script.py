"""
input:
bin folder
bin Name
Script
command
"""


import sys, os, glob
sys.path.insert(0, "/archive2/tmhyxb9/ToolBox")
import pandas as pd
import cmd


def generate_cmds(inputFile, outputDir):
    cmd1 = "cd /archive2/tmhyxb9/ToolBox/special"
    cmd2 = "python removeUMI.py " + inputFile + " " + outputDir
    cmds = [cmd1, cmd2]
    return cmds


def main():
    inputfiles = ["/archive2/tmhyxb9/FBL/fastq/Ctr2_sh/control2.fq",
                  "/archive2/tmhyxb9/FBL/fastq/FBL_sh/FBL.fq",
                  "/archive2/tmhyxb9/FBL/fastq/FBL2_sh/FBL2.fq",
                  "/archive2/tmhyxb9/FBL/fastq/EZH2_sh1/EZHsh1_1.fq",
                  "/archive2/tmhyxb9/FBL/fastq/EZH22_sh1/EZHsh1_2.fq",
                  "/archive2/tmhyxb9/FBL/fastq/EZH2_sh2/EZHsh2_1.fq",
                  "/archive2/tmhyxb9/FBL/fastq/EZH22_sh2/EZHsh2_2.fq"]


    for file in inputfiles:
        outputDir = "/archive2/tmhyxb9/FBL/fastq/rmUMI/fastq/"
        binname = "rmUMI_" + os.path.basename(file).split(".")[0]
        cmds = generate_cmds(file, outputDir)
        binpath = "/archive2/tmhyxb9/FBL/fastq/rmUMI/bin"
        cmd.generate_submit_pbs(cmds=cmds, binName=binname, binPath=binpath)
    pass


if __name__ == "__main__":
    main()



