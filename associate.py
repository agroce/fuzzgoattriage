import subprocess
import shutil
import glob
import os
import sys

dnull = open(os.devnull, 'w')

map = {}

i = 0
for f in []: #glob.glob("compilable_mutants/*.c"):
    i += 1
    print i,
    sys.stdout.flush()
    mn = f.split("/")[1].replace(".c","")
    try:
        os.remove("mutation.c")
    except:
        pass
    shutil.copy(f, "mutation.c")
    subprocess.call(["clang -o compiled/" + mn + " mutation.c main.c -lm"], shell=True, stdout=dnull, stderr=dnull)

ms = sorted(glob.glob("noneqmutants/eqclass.*"))
interesting = set([])

with open("matrix.out") as mfile:
    for line in mfile:
        if "id" not in line:
            i = 0
            for c in line:
                if c == "1":
                    interesting.add(ms[i])
                i += 1

print len(interesting)

for f in interesting:
    for c in glob.glob("compiled/*"):
        r =  subprocess.call(["diff " + c + " " + f], shell=True, stdout=dnull, stderr=dnull)
        if r == 0:
            print f, "EQUALS", c
            break
        
