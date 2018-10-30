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


def extract_Data(geneID, tumor):
    df_full = pd.read_csv("/archive2/tmhyxb9/dataBase/CCLE/qauntile_RPKM/quantiled_RPKM_2.csv", sep="\t", index_col=0)
    df_gene = df_full.loc[[geneID],]
    if tumor:
        df_tumor = [col for col in df_gene.columns if tumor in col]
        df_gene = df_gene.loc[:,df_tumor]
    df_T = df_gene.T
    df_T.sort_values(by=geneID, axis=0, ascending=False, inplace=True)
    return df_T


def add_label(df):
    df.reset_index(inplace=True)
    print df.head()
    df["Cell Line"] = df["index"].str.split("_", expand=True)[0]
    df["Tissue"] = df["index"].str.extract(r'_(.*?)\(')
    df.set_index("index", inplace=True)
    return df



def main():
    tumor = None
    # Read file and arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:], "g:t:", ["gene=", "tumor="])
    except getopt.GetoptError as err:
        print str(err)  # will print something like "option -a not recognized"
        sys.exit(2)
    for o, a in opts:
        if o in ["-g", "--gene"]:
            gene = a.upper()
        elif o in ("-t", "--tumor"):
            tumor = a.upper()
        else:
            assert False, "unhandled option"
    # Retrive gene ID (from symbol to ensemble ID)
    geneID = get_geneID(gene)
    # Extract data
    df_data = extract_Data(geneID, tumor)
    # add label
    df_data = add_label(df_data)
    df_data.rename(columns={geneID: gene}, inplace=True)
    # save file as .xls
    if tumor:
        filename = "/archive2/tmhyxb9/dataBase/CCLE/qauntile_RPKM/results/" + gene + "_" + tumor + "_CCLE.xls"
    else:
        filename = "/archive2/tmhyxb9/dataBase/CCLE/qauntile_RPKM/results/" + gene + "_CCLE.xls"
    df_data.to_csv(filename, sep="\t")
    pass


if __name__ == "__main__":
    main()


# python find_Gene_CCLE.py -g KIAA1429 -t liver
# python find_Gene_CCLE.py -g LILRB1
# LILRB1, 2, 3, 4, 5
