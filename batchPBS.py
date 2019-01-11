import pandas as pd
import os

def batch_hold(startid=692643, endid=692867):
    for i in range(startid, endid):
        jobid = str(i)
        os.system('qhold ' + jobid)
        print "job hold.", i


def batch_restart(startid=692643, endid=692867):
    for i in range(startid, endid):
        jobid = str(i)
        os.system('qrls ' + jobid)
        print "restart the holded job.", i



def main():
    # batch_hold()
    batch_restart()




if __name__ == "__main__":
    main()
