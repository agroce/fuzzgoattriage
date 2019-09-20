import random

vectors = {}

with open("covmatrix.out") as mfile:
    for line in mfile:
        if "id" in line:
            test = line[:-1]
        else:
            vectors[test] = line[:-1]

bugs = {}
with open("whichbugs.txt") as bugfile:
    for line in bugfile:
        if "id" in line:
            test = line[:-1]
            bugs[test] = []
        if "justbug" in line:
            bugs[test].append(line[:-1])

def d(t1, t2):
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
    return (dc/ep)

def fpf(N, tests, start, dm):
    ranked = [start]
    while len(ranked) < N:
        maxd = 0.0
        choice = None
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

tests = bugs.keys()

for K in range(2,39):
    print "N =", K

    totalBugCount = 0.0
    perfect = 0
    for start in tests:
        ranking = fpf(K, tests, start, d)
        bugsSeen = set([])
        for r in ranking:
            for b in bugs[r]:
                bugsSeen.add(b)
        totalBugCount += len(bugsSeen)
        if len(bugsSeen) == 4:
            perfect += 1

    print "FPF MUTANTS:", perfect, totalBugCount/len(tests)

    totalBugCount = 0.0
    perfect = 0
    for start in tests:
        tshuffle = list(tests)
        random.shuffle(tshuffle)
        ranking = tshuffle[:K]
        bugsSeen = set([])
        for r in ranking:
            for b in bugs[r]:
                bugsSeen.add(b)
        totalBugCount += len(bugsSeen)
        if len(bugsSeen) == 4:
            perfect += 1

    print "RANDOM:", perfect, totalBugCount/len(tests)
