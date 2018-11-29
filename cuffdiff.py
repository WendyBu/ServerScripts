"""
parse folders, each folder represent one group of samples

"""


import os , sys, getopt
import pandas as pd
import glob, os.path
sys.path.insert(0, "/archive2/tmhyxb9/ToolBox")
import cmd


def run_cuffdiff(outputDir, labels, input_files, ref):
    cmd = "cuffdiff -p 9 --output-dir " + outputDir + " --labels "+ labels + " " + ref + " " + input_files
    cmds = [cmd]
    return cmds


def main():
    """
    input folders
    output folder
    :return:
    """
    inputs = []
    try:
        opts, args = getopt.getopt(sys.argv[1:], "o:i:l:r:", ["output=", "input=", "label=", "ref="])
    except getopt.GetoptError as err:
        print str(err)  # will print something like "option -a not recognized"
        sys.exit(2)

    for o, a in opts:
        if o in ["-o", "--output"]:
            cwdir = os.getcwd()
            project_root = os.path.join(cwdir, os.pardir)
            outputDir = os.path.join(project_root, a)
            binName = a
            # print "outputDir", outputDir
        elif o in ("-i", "--input"):
            inputs.append(a)
        elif o in ("-l", "--label"):
            labels = a
        elif o in ("-r", "--ref"):
            gene_reference = a
        else:
            assert False, "unhandled option"

    # generate input commands
    inputCommands = ""
    for input in inputs:    # for each item after -i
        input_sub = input.split(",")
        inputFiles = ""
        for input_single_dir in input_sub:
            inputFile = os.path.join(cwdir, input_single_dir,  "accepted_hits.bam")
            inputFiles += inputFile + ","
        inputFiles = inputFiles[0:-1]
        inputCommands += inputFiles + " "

    # choose reference, either ucsc or refseq
    if gene_reference == "ucsc":
        reference = "/archive2/tmhyxb9/ref_data/hg19/hg19.ucscgenes.knowngene.exon.anno.gtf"
    elif gene_reference == "refseq":
        reference = "/archive2/tmhyxb9/ref_data/hg19/hg19.refGene.exon.anno.gtf"
    else:
        print "gene reference cannot be recognized!"


    cmds = run_cuffdiff(outputDir, labels, inputCommands, reference) # use absolute path for each input file

    # make output dir and bin dir
    if not os.path.exists(outputDir):
        os.mkdir(outputDir)
    binpath = os.path.join(project_root, "cuffdiff_bin")
    if not os.path.exists(binpath):
        os.mkdir(binpath)

    cmd.generate_pbs(cmds=cmds, binName=binName, binPath=binpath)  # change to generate_submit_pbs to submit jobs
    pass


if __name__ == "__main__":
    main()



# cuffdiff -p 9 --output-dir cuffdiffout_directory --labels foldernames,  /archive/tmhkxc48/ref_data/hg19/hg19.refGene.exon.anno.gtf control1/accepted_hits.bam,control2/accepted_hits.bam treat1/accepted_hits.bam,treat2/accepted_hits.bam
# under tophat directory, giving the output folder name and the input folder name
# the cffdiff output fold will be built under project root, same level as tophat.
# python /archive2/tmhyxb9/ToolBox/cuffdiff.py -o cuffdiff_HT -i HT37_MMC -i HT42_MMC -i HT_37C -i HT_42C
# python /archive2/tmhyxb9/ToolBox/cuffdiff.py -o cuffdiff_SNU -i SNU37MMC -i SNU42MMC -i SNU_37C -i SNU_42C
# python /archive2/tmhyxb9/ToolBox/cuffdiff.py -o cuffdiff_EZH2 -l control,EZH2_sh1,EZH2_sh2  -i B1,B2 -i B5,B6 -i B7,B8
# python /archive2/tmhyxb9/ToolBox/cuffdiff.py -o cuffdiff_FBL -l control,FBL  -i B1,B2 -i B3,B4
# python /archive2/tmhyxb9/ToolBox/cuffdiff.py -o cuffdiff_EZH2 -l control,EZH2_sh1,EZH2_sh2  -i A1,A2 -i A3,A4 -i A5,A6
# python /archive2/tmhyxb9/ToolBox/cuffdiff.py -o cuffdiff_ADAR1 -l control,ADAR_sh1,ADAR_sh2  -i A1,A2 -i A7,A8 -i A9,A10
# python /archive2/tmhyxb9/ToolBox/cuffdiff.py -o cuffdiff_ADAR2 -l control,ADAR2  -i A1,A2 -i A11,A12
# python /archive2/tmhyxb9/ToolBox/cuffdiff.py -o cuffdiff_FBL -l control,FBL  -i Control -i FBL
# python /archive2/tmhyxb9/ToolBox/cuffdiff.py -o cuffdiff_EZH2 -l control,EZH2sh1,EZH2sh2  -i Control -i EZH2sh1 -i EZH2sh2 -r ucsc

