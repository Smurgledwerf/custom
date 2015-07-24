import os, sys, getopt
opts, pattern = getopt.getopt(sys.argv[1], '-m')
opts, cutoff = getopt.getopt(sys.argv[2], '-m')
opts, file_name = getopt.getopt(sys.argv[3], '-m')
uniqlist = []
if cutoff in ['spc','SPC','SPACE','space',' ']:
    cutoff = ' '
elif cutoff in ['tab','TAB','\t']:
    cutoff = '\t'
f = open(file_name, 'r')
for line in f:
    line = line.strip()
    if pattern in line:
        portion = line.split(pattern)[1].split(cutoff)[0]
        polecat = '%s%s' % (pattern, portion)
        if polecat not in uniqlist:
            uniqlist.append(polecat)
print uniqlist
for entry in uniqlist:
    print entry
