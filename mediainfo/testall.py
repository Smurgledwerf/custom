import os, sys, getopt, pprint
from mitest import MITest
mitest = MITest()
opts, dir = getopt.getopt(sys.argv[1], '-m')
pp = pprint.PrettyPrinter(depth=4)
infos = []
for root, dirs, files in os.walk(dir):
    for f in files:
        fullpath = '%s/%s' % (root, f)
        print "FILE = %s" % fullpath
        info = mitest.get_mi(fullpath)
        pp.pprint(info)
        infos.append(info)
groups = {}
for info in infos:
    ikeys = info.keys()
    for ikey in ikeys: 
        if ikey not in groups.keys():
            groups[ikey] = {}
        for k in info[ikey].keys():
            v = info[ikey][k]
            if k not in groups[ikey].keys():
                groups[ikey][k] = []
            if isinstance(v, dict):
                xkeys = v.keys()
                groups[ikey][k] = {}
                for xkey in xkeys:
                    if xkey not in groups[ikey][k].keys():
                        groups[ikey][k][xkey] = []
                    val = info[ikey][k][xkey]
                    if val not in groups[ikey][k][xkey]:
                        groups[ikey][k][xkey].append(val)
            else:
                if v not in groups[ikey][k]:
                    groups[ikey][k].append(v)
print "GROUPED INFO:"
pp.pprint(groups)
