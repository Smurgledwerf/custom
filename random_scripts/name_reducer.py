import os, sys, math, hashlib, getopt
def kill_mul_spaces(origstrg):
    newstrg = ''
    for word in origstrg.split():
        newstrg=newstrg+' '+word
    return newstrg

lines_arr = []
opts, file_name = getopt.getopt(sys.argv[1], '-m')
print file_name
opts, out_file_name = getopt.getopt(sys.argv[2], '-m')
print out_file_name
f= open(file_name, 'r')
active_directory = ''
count = 0
wo_names = []
wo_tree = {}
for line in f:
	if not line.strip():
		continue
	else:
		line = line.rstrip('\r\n')
                line = line.upper()
                if line not in wo_names:
                    wo_names.append(line)
                    added = False
                    for k in wo_tree.keys():
                        if k in line:
                            wo_tree[k].append(line)
                            added = True
                    if not added:
                        wo_tree[line] = []
f.close()
wo_names.sort()
wo_tree_keys = wo_tree.keys()
wo_tree_keys.sort()
out = open(out_file_name, 'w')
for wtk in wo_tree_keys:
    out.write('%s\n' % wtk)
    els = wo_tree[wtk]
    for el in els:
        out.write('\t%s\n' % el)
out.write('\n\n\n')
out.write("LIST OF ALL\n")
for wo_name in wo_names:
    out.write('%s\n' % wo_name)
out.close()
