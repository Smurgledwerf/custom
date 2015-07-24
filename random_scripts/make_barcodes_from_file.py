import os, sys, math, hashlib, getopt, tacticenv, time
opts, file_name = getopt.getopt(sys.argv[1], '-m')

bc_arr = []
f= open(file_name, 'r')
for line in f:
    if not line.strip():
        continue
    else:
        line = line.rstrip('\r\n')
        line = line.strip()
        bc_arr.append(line)
f.close()
loops = 0
for i in range(0, len(bc_arr)):
    top_str = ''
    bot_str = ''
    addon = loops * 3 + i
    for i2 in range(addon+0,addon+4):
        if i2 < len(bc_arr):
            istr = bc_arr[i2]
            if top_str == '':
                top_str = "*%s*" % (istr)
            else:
                top_str = "%s,,*%s*" % (top_str, istr)
            if bot_str == '':
                bot_str = "%s" % (istr)
            else:
                bot_str = "%s,,%s" % (bot_str, istr)
            #print "*%s%s*" % (prefix, istr)
            #print "%s%s" % (prefix, istr)
    loops = loops + 1
    print top_str
    print bot_str
