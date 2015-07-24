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
file_name =  "/opt/spt/custom/random_scripts/hand_proj_wo_asl/wos" 
os.system("psql -U postgres twog < /opt/spt/custom/random_scripts/hand_proj_wo_asl/wo_query > %s" % file_name) 
wos = make_data_dict(file_name)
projs = {}
for wo_code in wos.keys():
    wo = wos[wo_code]
    if wo.get('proj_code') not in [None,'']:
        try:
            projs[wo.get('proj_code')].append(wo.get('work_group'))
        except:
            projs[wo.get('proj_code')] = [wo.get('work_group')] 
tlines = []
for p in projs.keys():
    proj_asls = projs[p]
    pk = {}
    for asl in proj_asls:
        if asl not in pk.keys():
            pk[asl] = 1
        else:
            pk[asl] = pk[asl] + 1
    greatest_num = -1
    greatest_asl = ''
    for k in pk.keys():
        if pk[k] >= greatest_num:
            greatest_num = pk[k]
            greatest_asl = k
    tlines.append('''update task set assigned_login_group = '%s' where lookup_code = '%s';\n''' % (greatest_asl, p)) 
new_insert_file = '/opt/spt/custom/random_scripts/hand_proj_wo_asl/proj_update'
if os.path.exists(new_insert_file):
    os.system('rm -rf %s' % new_insert_file)
new_guy = open(new_insert_file, 'w')
for line in tlines:
    new_guy.write(line)
new_guy.close()
    
    
