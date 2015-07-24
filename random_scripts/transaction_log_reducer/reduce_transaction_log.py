import os, sys, calendar, dateutil, datetime, time, getopt, pprint, re, math

opts, lowest_str = getopt.getopt(sys.argv[1], '-m')
opts, highest_str = getopt.getopt(sys.argv[2], '-m')
opts, chunk_str = getopt.getopt(sys.argv[3], '-m')
highest = int(highest_str)
lowest = int(lowest_str)
chunk = int(chunk_str)
max = highest
if highest == 0:
    os.system("psql -U postgres sthpw < max_query > max_result") 
    time.sleep(10)
    the_file = open('max_result', 'r')
    count = 0
    for line in the_file:
        line = line.rstrip('\r\n')
        if count == 2:
            fstr = line.strip(' ')
            max = int(fstr) 
        count = count + 1
    the_file.close()
print 'MAX = %s' % max

if lowest == 0:
    lowest = 100
last_chunk = lowest

for i in range(lowest, max):
    if i % chunk == 0: 
        if os.path.exists('killer'):
            os.system('rm -rf killer')
        killer_file = open('killer','w')
        print "DOING %s - %s" % (last_chunk, i)
        print 'delete from transaction_log where id < %s and id > %s;' % (i, lowest)
        killer_file.write('delete from transaction_log where id < %s and id > %s;' % (i, lowest)) 
        killer_file.close()
        time.sleep(1)
        os.system('psql -U postgres sthpw < killer')
        last_chunk = i

        
    
