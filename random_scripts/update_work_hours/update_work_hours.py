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
    print "File = %s FIELDS = %s" % (file_name, fields)
    return data_dict

opts, work_hour_file = getopt.getopt(sys.argv[1], '-m')
print "work_hour_file = %s" % work_hour_file
opts, task_file = getopt.getopt(sys.argv[2], '-m')
print "task_file = %s" % task_file
opts, work_order_file = getopt.getopt(sys.argv[3], '-m')
print "work_order_file = %s" % work_order_file
opts, proj_file = getopt.getopt(sys.argv[4], '-m')
print "proj_file = %s" % proj_file
opts, title_file = getopt.getopt(sys.argv[5], '-m')
print "title_file = %s" % title_file
opts, order_file = getopt.getopt(sys.argv[6], '-m')
print "order_file = %s" % order_file
opts, client_file = getopt.getopt(sys.argv[7], '-m')
print "client_file = %s" % client_file

work_hours = make_data_dict(work_hour_file)
tasks = make_data_dict(task_file)
work_orders = make_data_dict(work_order_file)
projs = make_data_dict(proj_file)
titles = make_data_dict(title_file)
orders = make_data_dict(order_file)
clients = make_data_dict(client_file)
work_hour_codes = work_hours.keys()
task_codes = tasks.keys()
work_order_codes = work_orders.keys()
proj_codes = projs.keys()
title_codes = titles.keys()
order_codes = orders.keys()
client_codes = clients.keys()
out_lines = []
problem_lines = []
for wh in work_hour_codes:
    #Expected first
    work_hour = work_hours[wh]
    task_code = work_hour.get('task_code')
    if task_code not in [None,''] and task_code in task_codes:
        task = tasks[task_code]
        lookup_code = task.get('lookup_code')
        if lookup_code in work_order_codes:
            work_order = work_orders[lookup_code]
            proj_code = work_order.get('proj_code')
            if proj_code in proj_codes:
                proj = projs[proj_code]
                title_code = proj.get('title_code')
                if title_code in title_codes:
                    title = titles[title_code]
                    order_code = title.get('order_code')
                    if order_code in order_codes:
                        order = orders[order_code]
                        client_code = order.get('client_code')
                        client_name = order.get('client_name')
                        if client_code in client_codes:
                            client = clients[client_code]
                            if client_name != client.get('name'):
                                client_name = client.get('name')
                        out_lines.append('''update work_hour set order_code = '%s', title_code = '%s', scheduler = '%s', client_code = '%s', client_name = '%s', is_billable = 'true' where code = '%s';''' % (order_code, title_code, order.get('login'), client_code, client_name, wh))
    else:
        problem_lines.append('''%s, %s, %s, %s, %s, %s''' % (work_hour.get('code'), work_hour.get('task_code'), work_hour.get('login'), work_hour.get('category'), work_hour.get('straight_time'), work_hour.get('day')))
                                                      
                                
out_file = open('work_hour_fix','w')
for ol in out_lines:
    out_file.write('%s\n' % ol)
out_file.close()
problem_file = open('work_hour_problems', 'w')
for pl in problem_lines:
    problem_file.write('%s\n' % pl)
problem_file.close()
