import random
import glob
import subprocess

vectors = {}

ms = sorted(glob.glob("noneqmutants/eqclass.*"))

source = {}
with open("mutantsource.txt") as msource:
    for line in msource:
        if "EQUALS" in line:
            ls = line.split()
            source[ls[0]] = ls[2]

mnum = {}
i = 0
for m in ms:
    mnum[i] = m
    i += 1

with open("matrix.out") as mfile:
    for line in mfile:
        if "id" in line:
            test = line[:-1]
        else:
            vectors[test] = line[:-1]

minv = {}
for t in vectors:
    i = 0
    for m in vectors[t]:
        if i not in minv:
            minv[i] = []
        if m == "1":
            minv[i].append(t)
        i += 1

bugs = {}
with open("whichbugs.txt") as bugfile:
    for line in bugfile:
        if "id" in line:
            test = line[:-1]
            bugs[test] = []
        if "justbug" in line:
            bugs[test].append(line[:-1])

dcache = {}
            
def d(t1, t2):
    if (t1, t2) in dcache:
        return dcache[(t1, t2)]
    if t1 == t2:
        return 0.0
    t1v = vectors[t1]
    t2v = vectors[t2]
    i = 0
    ep = 0.0
    dc = 0
    for i in range(0, len(t1v)):
        if (t1v[i] == "1") or (t2v[i] == "1"):
            ep += 1
            if t1v[i] != t2v[i]:
                dc += 1
    dcache[(t1, t2)] = (dc/ep)
    dcache[(t2, t1)] = (dc/ep)    
    return (dc/ep)

def fpf(N, tests, start, dm):
    ranked = [start]
    while len(ranked) < N:
        maxd = 0.0
        choice = start
        for t in tests:
            mind = 100000.0
            for r in ranked:
                dist = dm(t, r)
                if dist < mind:
                    mind = dist
            if mind > maxd:
                maxd = mind
                choice = t
        ranked.append(choice)
    return ranked

def localize(t, M):
    tv = vectors[t]
    i = 0
    repairing = []
    i = 0
    for m in tv:
        if m == "1":
            others = minv[i]
            dmax = 0.0
            for o in others:
                if d(t, o) > dmax:
                    dmax = d(t, o)
            repairing.append((i, dmax))
        i += 1
    rsort = sorted(repairing, key=lambda x:x[1])
    return rsort[:M]

tests = bugs.keys()

K = 5
if True:
    print "N =", K

    totalBugCount = 0.0
    perfect = 0
    for start in tests:
        ranking = fpf(K, tests, start, d)
        bugsSeen = set([])
        for r in ranking:
            l = localize(r, 3)
            print bugs[r]
            for b in bugs[r]:
                print b
                subprocess.call(["diff fuzzgoatJustBug" + b[-1] + ".c fuzzgoatNoVulns.c"], shell=True)
            for (m, dist) in l:
                print "LOCALIZATION:"
                print "DISTANCE:", dist
                print m
                s = source[mnum[m]].replace("compiled","compilable_mutants") + ".c"
                print s
                subprocess.call(["diff " + s + " fuzzgoat.c"], shell=True)
            print "="*80
            for b in bugs[r]:
                bugsSeen.add(b)
        totalBugCount += len(bugsSeen)
        if len(bugsSeen) == 4:
            perfect += 1

    print "FPF MUTANTS:", perfect, totalBugCount/len(tests)

