import pandas as pd
import os, sys


def diff(file1, file2):
    df1 = pd.read_csv(file1, sep = " ", header=None, index_col=2)
    df2 = pd.read_csv(file2, sep=" ", header = None, index_col=2)
    df = df1.join(df2, how='outer', lsuffix="old", rsuffix="new")
    df["old"] = df["0old"]
    df["new"] = df["0new"]
    df_same = df[df.old == df.new]
    df_diff = df[~(df.old == df.new)]
    if df_same.shape[0] == df1.shape[0]:
        print "All the md5 check are correct!"
    else:
        print "something wrong!"
    if df_diff.shape[0] != 0:
        print "something different"
    else:
        print "Nothing different was found!"
    pass


def main():
    oldmd5 = sys.argv[1]
    newmd5 = sys.argv[2]
    diff(oldmd5, newmd5)
    return


if __name__ == "__main__":
    main()


# cd /archive2/tmhyxb9/RNAediting/20181112ADAR_Seq/Downloads
# python /archive2/tmhyxb9/ToolBox/md5check.py Reads/md5.txt Reads/newmd5.txt