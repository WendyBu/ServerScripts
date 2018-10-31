"""python find_Gene_CCLE.py -g KIAA1429 -t prostate
given gene name and/or tumor name,
find the gene expression, or in specific tumor cell lines.
"""


import pandas as pd
import numpy as np
import os.path
import glob, sys
import getopt, re

pd.set_option('display.max_columns', 50)


def get_geneID(gene_symbol):
    gene_Table = pd.read_csv("/archive2/tmhyxb9/ref_data/hg19_conversion/ENSG_Symbol_conversion.xls", sep="\t",
                             index_col=1)
    try:
        s = gene_Table[gene_Table.Symbol == gene_symbol]
        return s.index.values[0]
    except:
        print "Invalid input gene!"


def extract_Data(geneIDs, tumor):
    df_full = pd.read_csv("/archive2/tmhyxb9/dataBase/CCLE/qauntile_RPKM/quantiled_RPKM_2.csv", sep="\t", index_col=0)
    df_gene = df_full.loc[geneIDs,]
    if tumor:
        df_tumor = [col for col in df_gene.columns if tumor in col]
        df_gene = df_gene.loc[:,df_tumor]
    df_T = df_gene.T
    return df_T


def add_label(df):
    df.reset_index(inplace=True)
    print df.head()
    df["Cell Line"] = df["index"].str.split("_", expand=True)[0]
    df["Tissue"] = df["index"].str.extract(r'_(.*?)\(')
    df.set_index("index", inplace=True)
    return df


def add_histType(df, hist):
    annotFile = "/archive2/tmhyxb9/dataBase/CCLE/CCLE_sample_info_file_2012-10-18.txt"
    annot = pd.read_csv(annotFile, sep="\t", index_col=0)
    annot = annot.loc[:, ['Histology','Hist Subtype1']]
    df.reset_index(inplace=True)
    df["CCLE_name"] = df.iloc[:,0].str.split(" ", expand=True).iloc[:,0]
    df.set_index("CCLE_name", inplace=True)
    df_hist = df.join(annot,  how="left")
    if hist:
        df_hist = df_hist[df_hist.loc[:,"Hist Subtype1"].str.contains(hist, na=False)]
    return df_hist


def main():
    tumor = None
    hist = None
    genes = []
    # Read file and arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:], "g:t:o:h:", ["gene=", "tumor=", "output=", "histSubtype"])
    except getopt.GetoptError as err:
        print str(err)  # will print something like "option -a not recognized"wge
        sys.exit(2)
    for o, a in opts:
        if o in ["-g", "--gene"]:
            gene = a.upper()
            genes.append(gene)
        elif o in ("-t", "--tumor"):
            tumor = a.upper()
        elif o in ("-o", "--output"):
            outputFile = a
        elif o in ("-h", "--histSubtype"):
            hist = a
        else:
            assert False, "unhandled option"

    # Retrive gene ID (from symbol to ensemble ID)
    geneID_gene = {}
    geneIDs = []
    for gene in genes:
        geneID = get_geneID(gene)
        geneIDs.append(geneID)
        geneID_gene[geneID] = gene
    # # Extract data
    df_data = extract_Data(geneIDs, tumor)
    # add label
    df_data = add_label(df_data)
    df_data.rename(columns=geneID_gene, inplace=True)
    # add histtype

    df_data = add_histType(df_data, hist)
    df_data.to_csv(outputFile, sep="\t")
    pass


if __name__ == "__main__":
    main()



# python find_Gene_CCLE.py -g LILRB1 -g LILRB2 -g LILRB3 -g LILRB4 -g LILRB5 -h lymph -o ../results/LILRBs_ccle_annot_lym.xls
# usage: -g  genename; -h histology; -o outputfile -t tumorname
# python find_Gene_CCLE.py -g EZH2 -g FBL -t prostate -o ../results/EZH_FLB_PCs.xls
# python find_Gene_CCLE.py -g EZH2 -g FBL  -o ../results/EZH_FLB_ccle.xls

