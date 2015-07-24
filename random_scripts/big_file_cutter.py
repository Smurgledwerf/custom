import os, sys, math, hashlib, getopt, tacticenv
opts, file_name = getopt.getopt(sys.argv[1], '-m')
opts, name_begin = getopt.getopt(sys.argv[2], '-m')
opts, count = getopt.getopt(sys.argv[3], '-m')
print file_name
print name_begin
print count
f = open(file_name, 'r')
line_num = 0
top_line = ''
this_batch = []
batch_num = 1
for line in f:
    print line_num
    if line_num == 0:
        top_line = line
    else:
        if line_num % int(count) == 0:
            noo = open('%s_%s' % (name_begin, batch_num), 'w')
            noo.write(top_line)
            for ln in this_batch:
                noo.write(ln)
            noo.close()
            this_batch = []
            batch_num = batch_num + 1
        else:
            this_batch.append(line)
    line_num = line_num + 1
f.close()

    
