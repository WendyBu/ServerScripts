"""
parse folders, each folder represent one group of samples

"""


import os , sys, getopt
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


def run_cuffdiff(outputDir, labels, input_files, replicates=1):
    cmdLabel = ",".join(labels)
    cmdInput = " ".join(input_files)
    cmd = "cuffdiff -p 9 --output-dir " + outputDir + " --labels "+ cmdLabel + " /archive2/tmhyxb9/ref_data/hg19/hg19.refGene.exon.anno.gtf "+ cmdInput
    # print cmd
    return cmd



def main():
    """
    input folders
    output folder
    :return:
    """
    inputFiles = []
    labels = []
    try:
        opts, args = getopt.getopt(sys.argv[1:], "o:i:", ["output=", "input="])
    except getopt.GetoptError as err:
        print str(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    for o, a in opts:
        if o in ["-o", "--output"]:
            cwdir = os.getcwd()
            project_root = os.path.join(cwdir, os.pardir)
            outputDir = os.path.join(project_root, a)
            binName = a
            # print "outputDir", outputDir
        elif o in ("-i", "--input"):
            labels.append(a)
        else:
            assert False, "unhandled option"
    # print "labels", labels
    for label in labels:
        inputFile = os.path.join(cwdir, label,  "accepted_hits.bam")
        inputFiles.append(inputFile)
    # print "inputFiles", inputFiles
    command = run_cuffdiff(outputDir, labels, inputFiles, 1) # use absolute path for each input file

    if not os.path.exists(outputDir):
        os.mkdir(outputDir)
    binpath = os.path.join(project_root, "cuffdiff_bin")
    if not os.path.exists(binpath):
        os.mkdir(binpath)
    generate_pbs(command, binName, binpath)
    pass


if __name__ == "__main__":
    main()



# cuffdiff -p 9 --output-dir cuffdiffout_directory --labels foldernames,  /archive/tmhkxc48/ref_data/hg19/hg19.refGene.exon.anno.gtf control1/accepted_hits.bam,control2/accepted_hits.bam treat1/accepted_hits.bam,treat2/accepted_hits.bam
# under tophat directory, giving the output folder name and the input folder name
# python /archive2/tmhyxb9/ToolBox/cuffdiff.py -o cuffdiff_HT -i HT37_MMC -i HT42_MMC -i HT_37C -i HT_42C
# python /archive2/tmhyxb9/ToolBox/cuffdiff.py -o cuffdiff_SNU -i SNU37MMC -i SNU42MMC -i SNU_37C -i SNU_42C
