import subprocess
import glob
import os
import sys

dnull = open(os.devnull, 'w')

ms = sorted(glob.glob("noneqmutants/eqclass.*"))

with open("matrix.out", 'w') as matrix:
    for t in glob.glob("out/crashes/id*"):
        matrix.write(t+"\n")
        print t
        i = 0
        for m in ms:
            i += 1
            r = subprocess.call(["ulimit -t 1;" + m + " " + t], shell=True, stdout=dnull, stderr=dnull)
            if r == 0:
                matrix.write("1")
                print i,
            else:
                matrix.write("0")
            matrix.flush()
            sys.stdout.flush()
        matrix.write("\n")
        print
            
    
