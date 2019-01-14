
import pandas as pd
import os, os.path, sys

sys.path.insert(0, "/archive2/tmhyxb9/ToolBox")
import cmd


samples = ["Control", "FBL", "EZH2sh1", "EZH2sh2"]
for sample in samples:
    geneGTF = "/archive2/tmhyxb9/ref_data/hg19/hg19.ucscgenes.knowngene.gtf"
    outputFile = "/archive2/tmhyxb9/FBL/RNA_seq/tophat_pair/HTseq_RNAseq/HTseq_RNAseq_results" + sample + "_RNAC_raw_count.txt"

    cmd0 = "cd /archive2/tmhyxb9/FBL/RNA_seq/tophat_pair/tophat/" + sample

    cmd1 = "module load samtools/1.9"
    cmd2 = "samtools sort accepted_hits.bam > accepted_hits.sorted.bam"
    cmd3 = "samtools index accepted_hits.sorted.bam"

    cmd4 = "module load python/2.7.11"

    cmd5 = "htseq-count -f bam accepted_hits.sorted.bam -s no -m intersection-nonempty " + geneGTF  + " > " + outputFile

    cmds = [cmd0, cmd1, cmd2, cmd3, cmd4, cmd5]
    binPath = "/archive2/tmhyxb9/FBL/RNA_seq/tophat_pair/HTseq_RNAseq/bin"
    cmd.generate_submit_pbs(cmds = cmds , binName = sample, binPath = binPath)