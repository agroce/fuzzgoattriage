import subprocess
import shutil
import glob
import os

dnull = open(os.devnull, 'w')

for f in glob.glob("mutants/*.c"):
    r = subprocess.call(["gcc " + f + " main.c -lm"], shell=True, stdout=dnull, stderr=dnull)
    if r == 0:
        shutil.copy(f, "compilable_mutants")
        print f, "COMPILES"
    else:
        print f, "DOES NOT COMPILE"
