"""
giving gene name and tumor type (breast or prostate)
generate a file: eg ADAR_prostate.csv. ADAR expression in prostate cancer sets. 
"""
import pandas as pd
import os, sys
pd.set_option('display.max_columns', 50)



def get_geneID(gene_symbol):
    gene_Table = pd.read_csv("/archive2/tmhyxb9/ref_data/hg19_conversion/ENSG_Symbol_conversion.xls", sep="\t", index_col=1)
    s = gene_Table[gene_Table.Symbol == gene_symbol]
    return s.index.values[0]


def extract_data(gene, tumor):
    if tumor in["breast", "Breast", "BREAST"]:
        df = pd.read_csv("TCGA_BRCA_breat_quantile_fpkm.nor.txt", sep="\t", index_col=0)
    elif tumor in ["prostate", "Prostate", "PROSTATE"]:
        df = pd.read_csv("TCGA_PRAD_prostate_quantile_fpkm.nor.txt", sep="\t", index_col=0)
    else:
        print "Wrong tumor type input!"

    try:
        df_gene = df.loc[[gene],]
        df_geneT = df_gene.T
        df_type = df.iloc[[0], :]
        df_typeT = df_type.T
        combine = df_geneT.join(df_typeT)
    except:
        print "wrong gene input!"
    return combine


def main():
    gene = sys.argv[1]
    tumor = sys.argv[2]
    gene_ID = get_geneID(gene)
    gene_exp = extract_data(gene_ID, tumor)
    filename = "results/" + gene + "_" + tumor + ".csv"
    gene_exp.to_csv(filename, sep="\t")
    pass

if __name__ == "__main__":
    main()


# goto folder: /archive2/tmhyxb9/dataBase/TCGA_quantile/
#python extractData.py KIAA1429 prostate





