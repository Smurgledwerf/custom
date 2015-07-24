import os, sys, math, hashlib, getopt, tacticenv
from tactic_client_lib import TacticServerStub
def kill_mul_spaces(origstrg):
    newstrg = ''
    for word in origstrg.split():
        newstrg=newstrg+' '+word
    return newstrg

def make_qb_data_dict(file_name, find_str):
    the_file = open(file_name, 'r')
    fields = []
    data_dict = {}
    count = 0
    code_col = 0
    lower_find = find_str.lower()
    top_line = ''
    for line in the_file:
        line = line.rstrip('\r\n')
        lower_line = line.lower()
        #data = line.split('\t')
        data = line.split('\t')
        if count == 0:
            top_line = line
            fc = 0
            for field in data:
                field = kill_mul_spaces(field)
                field = field.strip(' ')
                fields.append(field)
                fc = fc + 1
        elif lower_find in lower_line:
            ddkey = 'Record %s' % count
            data_dict[ddkey] = {'whole_line': line}
            data_count = 0
            this_code = ''
            for val in data:
                val = kill_mul_spaces(val)
                val = val.strip(' ')
                data_dict[ddkey][fields[data_count]] = val
                data_count = data_count + 1 
        count = count + 1  
    the_file.close()
    return [data_dict, top_line]

opts, file_name = getopt.getopt(sys.argv[1], '-m')
print "file_name = %s" % file_name
opts, find_text = getopt.getopt(sys.argv[2], '-m')
print "find_text = %s" % find_text
print file_name
rez = make_qb_data_dict(file_name, find_text)
invoices = rez[0]
top_line = rez[1]
file_s = file_name.split('.')
file_first = ''.join(file_s[:len(file_s) - 1])
out_lines = []
for i in invoices.keys():
    invoice = invoices[i]
    out_lines.append(invoice.get('whole_line'))
    
new_insert_file = '/opt/spt/custom/random_scripts/%s_with_%s' % (file_first, find_text.replace(' ','_'))
if os.path.exists(new_insert_file):
    os.system('rm -rf %s' % new_insert_file)

new_guy = open(new_insert_file, 'w')
new_guy.write('%s\n' % top_line)
for line in out_lines:
    new_guy.write('%s\n' % line)
new_guy.close()
    
    
