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
opts, code_or_id = getopt.getopt(sys.argv[3], '-m')
print "code_or_id = %s" % code_or_id
opts, current_table_file = getopt.getopt(sys.argv[4], '-m')
print "current_table_file = %s" % current_table_file
opts, client_file = getopt.getopt(sys.argv[5], '-m')
print "client_file = %s" % client_file
lookup_codes = {'CLIENT00046': 'CLIENT00042', 'CLIENT00003': 'CLIENT00042', 'CLIENT00005': 'CLIENT00042', 'CLIENT00008': 'CLIENT00047', 'CLIENT00009': 'CLIENT00042', 'CLIENT00010': 'CLIENT00042', 'CLIENT00011': 'CLIENT00042', 'CLIENT00012': 'CLIENT00042', 'CLIENT00013': 'CLIENT00042', 'CLIENT00014': 'CLIENT00042', 'CLIENT00015': 'CLIENT00042', 'CLIENT00016': 'CLIENT00042', 'CLIENT00017': 'CLIENT00042', 'CLIENT00020': 'CLIENT00019', 'CLIENT00021': 'CLIENT00007', 'CLIENT00023': 'CLIENT00047', 'CLIENT00024': 'CLIENT00047', 'CLIENT00025': 'CLIENT00047', 'CLIENT00062': 'CLIENT00042'}
current_tbl = make_data_dict(current_table_file)
print "GOT CURRENT TABLE"
client_tbl = make_data_dict(client_file)
print "GOT CLIENT TABLE"
current_codes = []
current_codes = current_tbl.keys()
out_lines = []
problem_lines = []
count = 0
for cc in current_codes:
   #print "Count = %s, Len = %s Code = %s" % (count, current_len, cc) 
   #print "Count = %s, Code = %s" % (count, cc) 
   # If client_code is in this table, look at it and resolve it, if needed
   if 'client_code' in current_tbl.keys():
       resolved_client = current_client = current_tbl[cc]['client_code']
       if current_client in lookup_codes.keys():
           resolved_client = lookup_codes[current_client]
           out_lines.append("update %s set client_code = '%s' where %s = '%s';" % (table, resolved_client, code_or_id, cc))
           if 'client_name' in current_tbl.keys():
               new_name = client_tbl[resolved_code]['name']
               out_lines.append("update %s set client_name = '%s' where %s = '%s';" % (table, new_name, code_or_id, cc))
       elif current_client not in client_tbl.keys():
           problem_lines.append("%s's Client Code: %s, doesn't exist in the client table")
   # If login things are in the table, make them lowercase
   for field in current_tbl[cc].keys():
       if field not in ['client_code','client_name'] and not (table == 'client' and field == 'name'):
           # If field isn't a client related thing, just make lowercase.
           # Make sure you don't do an update if there has been no change made
           current_field_data = current_tbl[cc][field]
           new_field_data = current_field_data.lower()
           if current_field_data != new_field_data:
               out_lines.append("update %s set %s = '%s' where %s = '%s';" % (table, field, new_field_data, code_or_id, cc))
   count = count + 1
       
out_file = open('%s_%s_fix.sql' % (db, table), 'w')
for ol in out_lines:
    out_file.write('%s\n' % ol)
out_file.close()
problem_file = open('ClientCodeProblems', 'w')
for pl in problem_lines:
    problem_file.write('%s\n' % pl)
problem_file.close()
