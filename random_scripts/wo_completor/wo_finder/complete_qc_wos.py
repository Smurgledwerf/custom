import os, sys, math, hashlib, getopt, tacticenv, time
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
    code_index = 0
    for line in the_file:
        line = line.rstrip('\r\n')
        #data = line.split('\t')
        data = line.split('|')
        if boolio:
            if count == 0:
                field_counter = 0
                for field in data:
                    field = kill_mul_spaces(field)
                    field = field.strip(' ')
                    fields.append(field)
                    if field == 'code':
                        code_index = field_counter
                    field_counter = field_counter + 1
                        
            elif count == 1:
                print file_name
                print line
            elif data[0][0] == '(':
                print "END OF FILE"
                boolio = False
            else:
                data_count = 0
                this_code = ''
                this_data = {}
                for val in data:
                    val = kill_mul_spaces(val)
                    val = val.strip(' ')
                    if data_count == code_index:
                        this_code = val
                    this_data[fields[data_count]] = val
                    data_count = data_count + 1 
                data_dict[this_code] = this_data
            count = count + 1  
    the_file.close()
    #print "File = %s FIELDS = %s" % (file_name, fields)
    id_dict = {}
    for code, dd in data_dict.iteritems():
        id_dict[dd.get('id')] = dd
    return [data_dict, id_dict]

server = TacticServerStub.get(protocol="xmlrpc")
opts, task_file = getopt.getopt(sys.argv[1], '-m')
print "task_file = %s" % task_file

CODE = 0
ID = 1
tasks = make_data_dict(task_file)
task_codes = tasks[CODE].keys()
count = 0
for task_code in task_codes:
    count = count + 1
    print count
    info = tasks[CODE][task_code]
    print info
    sk = server.build_search_key('sthpw/task', task_code)
    process = info.get('process')
    task_id = info.get('id')
    scheduler = info.get('scheduler')
    client_code = info.get('client_code')
    client_name = info.get('client_name')
    order_code = info.get('order_code')
    title_code = info.get('title_code')
    #print info
    server.insert('sthpw/work_hour', {'task_code': task_code, 'project_code': 'twog', 'description': 'Added with wo_completor.py', 'login': 'luis.barajas', 'process': process, 'straight_time': .5, 'search_id': task_id, 'search_type': 'sthpw/task', 'is_billable': True, 'scheduler': scheduler, 'client_code': client_code, 'client_name': client_name, 'order_code': order_code, 'title_code': title_code}) 
    server.update(sk, {'status': 'Completed'}, triggers=False)
