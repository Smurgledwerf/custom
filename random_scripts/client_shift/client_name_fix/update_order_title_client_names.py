import os, sys, math, hashlib, getopt, tacticenv, time
def kill_mul_spaces(origstrg):
    newstrg = ''
    for word in origstrg.split():
        newstrg=newstrg+' '+word
    return newstrg

def make_data_dict(file_name):
    the_file = open(file_name, 'r')
    fields = []
    data_dict = {}
    count = 0
    for line in the_file:
        line = line.rstrip('\r\n')
        data = line.split('\t')
        if count == 0:
            for field in data:
                field = kill_mul_spaces(field)
                field = field.strip(' ')
                fields.append(field)
        else:
            data_count = 0
            this_code = ''
            for val in data:
                val = kill_mul_spaces(val)
                val = val.strip(' ')
                if data_count == 0:
                    data_dict[val] = {}
                    this_code = val
                else:
                    data_dict[this_code][fields[data_count]] = val
                data_count = data_count + 1 
        count = count + 1  
    the_file.close()
    print "File = %s FIELDS = %s" % (file_name, fields)
    return data_dict
opts, db = getopt.getopt(sys.argv[1], '-m')
print "db = %s" % db
opts, table = getopt.getopt(sys.argv[2], '-m')
print "table = %s" % table
opts, current_table_file = getopt.getopt(sys.argv[3], '-m')
print "current_table_file = %s" % current_table_file
opts, client_file = getopt.getopt(sys.argv[4], '-m')
print "client_file = %s" % client_file
current_tbl = make_data_dict(current_table_file)
print "GOT CURRENT TABLE: %s/%s" % (db, table) 
client_tbl = make_data_dict(client_file)
print "GOT CLIENT TABLE"
current_codes = []
current_codes = current_tbl.keys()
lookup_codes = client_tbl.keys() 
out_lines = []
problem_lines = []
count = 0
for cc in current_codes:
   if current_tbl[cc]['client_code'] in lookup_codes:
       new_name = client_tbl[current_tbl[cc]['client_code']]['name']
       if table == 'order':
           out_lines.append('''update "%s" set client_name = '%s' where code = '%s';''' % (table, new_name, cc))
       else:
           out_lines.append('''update %s set client_name = '%s' where code = '%s';''' % (table, new_name, cc))
   else:
       problem_lines.append('Not found in lookup codes: %s' % current_tbl[cc]['client_code'])
   count = count + 1
       
out_file = open('%s_%s_NAMEFIX.sql' % (db, table), 'w')
for ol in out_lines:
    out_file.write('%s\n' % ol)
out_file.close()
problem_file = open('ClientCodeProblems', 'w')
for pl in problem_lines:
    problem_file.write('%s\n' % pl)
problem_file.close()
