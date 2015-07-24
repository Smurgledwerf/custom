import os, sys, math, hashlib, getopt, tacticenv, time
from tactic_client_lib import TacticServerStub
server = TacticServerStub.get(protocol="xmlrpc")
lines_arr = []
print "Example: python insert_with_parameters.py the_list_file twog language 'name,description,type,keywords' tab"
opts, file_name = getopt.getopt(sys.argv[1], '-m')
print "file_name = %s" % file_name
opts, db = getopt.getopt(sys.argv[2], '-m')
print "db = %s" % db
opts, table = getopt.getopt(sys.argv[3], '-m')
print "table = %s" % table
opts, field_order = getopt.getopt(sys.argv[4], '-m')
print "Field Order = %s" % field_order
opts, tabs_or_commas = getopt.getopt(sys.argv[5], '-m')
print "Tabs or commas = %s" % tabs_or_commas
fields_in_order = field_order.split(',')
len_fields_in_order = len(fields_in_order)
delimiter = ','
if tabs_or_commas in [',','comma','commas']:
    delimiter = ','
elif tabs_or_commas in ['	','\t','tab','tabs']:
    delimiter = '\t'
f= open(file_name, 'r')
counter = 0
for line in f:
    if not line.strip():
        continue
    else:
        line = line.rstrip('\r\n')
        vals = line.split(delimiter)
        if len_fields_in_order != len(vals):
            print "Line %s, '''%s''' does not match the entered field lengths" % (counter, line)
        else: 
            package = {}
            c = 0
            for field in fields_in_order:
                package[field] = vals[c]  
                c = c + 1
            server.insert('%s/%s' % (db, table), package)
    counter = counter + 1
f.close()
