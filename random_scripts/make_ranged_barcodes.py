import os, sys, math, hashlib, getopt, tacticenv, time
opts, prefix = getopt.getopt(sys.argv[1], '-m')
opts, range_begin = getopt.getopt(sys.argv[2], '-m')
opts, range_end = getopt.getopt(sys.argv[3], '-m')
opts, num_nums = getopt.getopt(sys.argv[4], '-m')
range_begin = int(range_begin)
range_end = int(range_end) + 1
num_nums = int(num_nums)

loops = 0
for i in range(range_begin, range_end):
    top_str = ''
    bot_str = ''
    addon = loops * 3 + i
    for i2 in range(addon+0,addon+4):
        if i2 < range_end:
            istr = "%s" % i2
            istr_len = len(istr)
            idif = num_nums - istr_len
            for p in range(0,idif):
                istr = '0%s' % istr
            if top_str == '':
                top_str = "*%s%s*" % (prefix, istr)
            else:
                top_str = "%s,,*%s%s*" % (top_str, prefix, istr)
            if bot_str == '':
                bot_str = "%s%s" % (prefix, istr)
            else:
                bot_str = "%s,,%s%s" % (bot_str, prefix, istr)
            #print "*%s%s*" % (prefix, istr)
            #print "%s%s" % (prefix, istr)
    loops = loops + 1
    print top_str
    print bot_str
