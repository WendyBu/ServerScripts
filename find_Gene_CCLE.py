import pandas as pd
import numpy as np
import os.path
import glob, sys
import getopt

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

    df_tumor = [col for col in df_gene.columns if tumor in col]
    df_gene_tumor = df_gene.loc[:,df_tumor]
    return df_gene_tumor


def extract_Data_from_all(geneID):
    df_full = pd.read_csv("/archive2/tmhyxb9/dataBase/CCLE/qauntile_RPKM/quantiled_RPKM_2.csv", sep="\t", index_col=0)
    df_gene = df_full.loc[[geneID],]
    return df_gene


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "g:t:", ["gene=", "tumor="])
    except getopt.GetoptError as err:
        print str(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    for o, a in opts:
        if o in ["-g", "--gene"]:
            gene = a
        elif o in ("-t", "--tumor"):
            tumor = a.upper()
        else:
            assert False, "unhandled option"

    geneID = get_geneID(gene)

    if not (tumor is None):
        df_data = extract_Data(geneID, tumor)
        filename = "/archive2/tmhyxb9/dataBase/CCLE/qauntile_RPKM/results/" + gene + "_" + tumor + "_CCLE.csv"
    else:
        df_data = extract_Data_from_all(geneID)
        filename = "/archive2/tmhyxb9/dataBase/CCLE/qauntile_RPKM/results/" + gene +  "_CCLE.csv"

    df_data.to_csv(filename, sep="\t")
    pass


if __name__ == "__main__":
    main()

