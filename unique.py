import subprocess
import shutil
import glob
import os

dnull = open(os.devnull, 'w')

eqSet =  ["eqclass.1"]

i = 0
for f in glob.glob("compilable_mutants/*.c"):
    i += 1
    print "PROCESSING MUTANT", i, f
    try:
        os.remove("mutation.c")
    except:
        pass
    
    shutil.copy(f, "mutation.c")
    r = subprocess.call(["clang -o newmutant mutation.c main.c -lm"], shell=True, stdout=dnull, stderr=dnull)
    anySame = False
    for c in eqSet:
        r =  subprocess.call(["diff " + c + " newmutant"], shell=True, stdout=dnull, stderr=dnull)
        if r == 0:
            print "SAME AS", c
            anySame = True
            break
    if not anySame:
        newClass = "eqclass." + str(len(eqSet)+1)        
        print "NEW EQUIVALENCE CLASS:", newClass
        shutil.copy("newmutant", newClass)
        eqSet.append(newClass)
        
