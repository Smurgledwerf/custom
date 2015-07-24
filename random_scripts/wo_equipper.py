import os, sys, math, hashlib, getopt, tacticenv
from tactic_client_lib import TacticServerStub
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
    boolio = True
    code_col = 0
    for line in the_file:
        line = line.rstrip('\r\n')
        #data = line.split('\t')
        data = line.split(' | ')
        if boolio:
            if count == 0:
                fc = 0
                for field in data:
                    field = kill_mul_spaces(field)
                    field = field.strip(' ')
                    fields.append(field)
                    if field == 'code':
                        code_col = fc
                    fc = fc + 1
            elif count == 1:
                print file_name
                print line
            elif data[0][0] == '(':
                print "END OF FILE"
                boolio = False
            else:
                data_count = 0
                this_code = ''
                for val in data:
                    val = kill_mul_spaces(val)
                    val = val.strip(' ')
                    if data_count == code_col:
                        data_dict[val] = {fields[data_count]: val}
                        this_code = val
                    else:
                        data_dict[this_code][fields[data_count]] = val
                    data_count = data_count + 1 
            count = count + 1  
    the_file.close()
    return data_dict

server = TacticServerStub.get(protocol="xmlrpc")
file_name =  "/opt/spt/custom/random_scripts/wo_eq_result" 
os.system("psql -U postgres twog < /opt/spt/custom/random_scripts/wo_eq_query > %s" % file_name) 
eqs = make_data_dict(file_name)
wo_insert = {}
unit_lookup = {'length': 'LEN', 'gb': 'GB', 'tb': 'TB', 'mb': 'MB', 'hr': 'HR', 'items': 'HR'}
for eq_code in eqs.keys():
    eq = eqs[eq_code]
    unit = eq['units']
    name = eq['name']
    if unit not in [None,'']:
        unit = unit_lookup[unit]
    else:
        unit = 'UNK'
    actual_duration = eq['actual_duration']
    if actual_duration in [None,'']:
        actual_duration = 0
    wo_code = eq['work_order_code']
    try:
        current = wo_insert[wo_code]
    except:
        wo_insert[wo_code] = '%sX|X%sX|X%sX|X%s' % (eq_code, name, unit, actual_duration) 
        pass 
    else:
        wo_insert[wo_code] = '%sZ,Z%sX|X%sX|X%sX|X%s' % (wo_insert[wo_code], eq_code, name, unit, actual_duration) 
new_insert_file = '/opt/spt/custom/random_scripts/wo_eq_insert'
if os.path.exists(new_insert_file):
    os.system('rm -rf %s' % new_insert_file)
new_guy = open(new_insert_file, 'w')
for wo in wo_insert.keys():
    new_guy.write("update work_order set eq_info = '%s' where code = '%s';\n" % (wo_insert[wo], wo))
new_guy.close()
    
    
