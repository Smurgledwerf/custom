import os, sys, math, hashlib, getopt
def kill_mul_spaces(origstrg):
    newstrg = ''
    for word in origstrg.split():
        newstrg=newstrg+' '+word
    return newstrg
opts, file_name = getopt.getopt(sys.argv[1], '-m')
f= open(file_name, 'r')
current_table = ''
tables = {}
for line in f:
	if not line.strip():
		continue
	else:
		line = line.rstrip('\r\n')
                if line.find("CREATE TABLE") != -1:
                    table = line.split("CREATE TABLE ")[1].split(' ')[0]
                    table = table.replace('"','')
                    current_table = 'twog/%s' % table
                    if current_table not in tables.keys():
                        tables[current_table] = []
                else:
                    if line.find(');') == -1:
                        kill_mul = kill_mul_spaces(line)
                        kill_mul = kill_mul[1:]
                        column = kill_mul.split(' ')[0]
                        column = column.replace('"','')
                        tables[current_table].append(column)
f.close()
print "<rules>"
tabls_list = tables.keys()
tabls_list.sort()
for table in tabls_list:
    tables[table].sort()
    for el in tables[table]:
        print "    <rule group='element' search_type='%s' key='%s' access='edit'/>" % (table, el) 
print "</rules>"
