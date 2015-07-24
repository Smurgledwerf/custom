import os, sys, math, hashlib, getopt, tacticenv, time
from tactic_client_lib import TacticServerStub
def kill_mul_spaces(origstrg):
    newstrg = ''
    for word in origstrg.split():
        newstrg=newstrg+' '+word
    return newstrg

server = TacticServerStub.get(protocol="xmlrpc")
opts, file_name = getopt.getopt(sys.argv[1], '-m')
print "file_name = %s" % file_name
opts, last_passed_in = getopt.getopt(sys.argv[2], '-m')
print "last_passed_in = %s" % last_passed_in
print file_name
f= open(file_name, 'r')
count = 0
line_count = 0
fields = [] 
print "GOING IN"
found_first = False
for line in f:
	line = line.rstrip('\r\n')
        data = line.split(',')
        source_id = 0
        if line_count > 0:
            source_id = int(data[0])
	source_code = data[1]
	caid = data[2]
	obc1 = data[3]
	obc2 = data[4]
	obc3 = data[5]
	part = data[6]
	strat2g_part = data[7]
        if not found_first and source_id > int(last_passed_in):
            found_first = True
        if found_first:
            if count % 150 == 0:
                if count != 0:
                    server.finish()
                    print "SLEEPING"
                    time.sleep(5)
                server.start('IMPORTING SOURCES AND THINGS %s' % count)
            print "COUNT = %s" % count
        if found_first and source_id > int(last_passed_in) and line_count > 0:
            if caid not in [None,'']:
	        server.insert('twog/outside_barcode', {'source_code': source_code, 'barcode': caid})
            if obc1 not in [None,'']:
	        server.insert('twog/outside_barcode', {'source_code': source_code, 'barcode': obc1})
            if obc2 not in [None,'']:
	        server.insert('twog/outside_barcode', {'source_code': source_code, 'barcode': obc2})
            if obc3 not in [None,'']:
	        server.insert('twog/outside_barcode', {'source_code': source_code, 'barcode': obc3})
            if part in [None,'']:
	        if strat2g_part not in [None,'']:
	            server.update(server.build_search_key('twog/source', source_code), {'part': strat2g_part})
            count = count + 1
            print "SOURCE_ID = %s" % source_id
        line_count = line_count + 1
f.close()
server.finish()
