import subprocess
import glob
import os
import sys

with open("covmatrix.out", 'w') as matrix:
    for tcov in glob.glob("coverages/*.gcov"):
        t = "out/crashes/" + tcov.split(".gcov")[0].split("/")[1]
        matrix.write(t+"\n")
        print t
        i = 0
        for line in open(tcov):
            lcov = line.split(":")[0]
            if "-" in lcov:
                continue
            if "#" in lcov:
                matrix.write("0")
            else:
                matrix.write("1")
        matrix.write("\n")
        print
            
    
