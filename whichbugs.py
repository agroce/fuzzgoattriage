import subprocess
import glob
import os
import sys

dnull = open(os.devnull, 'w')

ms = glob.glob("justbug*")
ms = map(lambda x: "./" +x, ms)

if True:
    for t in glob.glob("out/crashes/id*"):
        print t
        i = 0
        for m in ms:
            r = subprocess.call(["ulimit -t 1;" + m + " " + t], shell=True, stdout=dnull, stderr=dnull)
            if r != 0:
                print m
            sys.stdout.flush()
        print
            
    
