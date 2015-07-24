import os, sys, math, hashlib, getopt, tacticenv
def make_chars(char, num_chars, max_len):
    count = 0
    out_str = ''
    while count < (max_len - num_chars):
        out_str = '%s%s' % (out_str, char)
        count = count + 1
    return out_str
def make_zeroed(number):
    num_str = '%s' % number
    len_num = len(num_str)
    out_str = '%s%s' % (make_chars('0', len_num, 7), number) 
    return out_str

opts, file_name = getopt.getopt(sys.argv[1], '-m')
opts, name_begin = getopt.getopt(sys.argv[2], '-m')
opts, count = getopt.getopt(sys.argv[3], '-m')
print file_name
print name_begin
print count
f = open(file_name, 'r')
line_num = 0
this_batch = []
batch_num = 1
row_count = 1
for line in f:
    #print line_num
    if '</row>' in line:
        row_count = row_count + 1
        this_batch.append(line)
        #print "ROW_COUNT + 1 = %s" % (row_count + 1)
        #print "COUNT = %s" % int(count)
        #print "(ROW_COUNT + 1) MOD int(count) = %s" % ((row_count + 1) % int(count))
        if (row_count + 1) % int(count) == 0:
            new_name = '%s_%s' % (name_begin, make_zeroed(batch_num))
            print new_name
            noo = open(new_name, 'w')
            for ln in this_batch:
                noo.write(ln)
            noo.close()
            this_batch = []
            batch_num = batch_num + 1
    else:
        this_batch.append(line)
    line_num = line_num + 1
f.close()

    

