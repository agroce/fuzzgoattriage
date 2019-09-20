import glob
import subprocess

for f in glob.glob("out/crashes/id*"):
    bugid = "id" + f.split("id")[1]
    subprocess.call(["rm *.gcda; ./fuzzgoodcov " + f + " ; gcov fuzzgoatNoVulns.c; mv fuzzgoatNoVulns.c.gcov coverages/" + bugid + ".gcov"], shell=True)
