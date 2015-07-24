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
    #print "File = %s FIELDS = %s" % (file_name, fields)
    id_dict = {}
    for code, dd in data_dict.iteritems():
        id_dict[dd.get('id')] = dd
    return [data_dict, id_dict]

opts, task_file = getopt.getopt(sys.argv[1], '-m')
print "task_file = %s" % task_file
opts, work_order_file = getopt.getopt(sys.argv[2], '-m')
print "work_order_file = %s" % work_order_file
opts, proj_file = getopt.getopt(sys.argv[3], '-m')
print "proj_file = %s" % proj_file
opts, title_file = getopt.getopt(sys.argv[4], '-m')
print "title_file = %s" % title_file
opts, order_file = getopt.getopt(sys.argv[5], '-m')
print "order_file = %s" % order_file
opts, dept = getopt.getopt(sys.argv[6], '-m')
print "dept = %s" % dept
opts, classification = getopt.getopt(sys.argv[7], '-m')
print "classification = %s" % classification

CODE = 0
ID = 1
tasks = make_data_dict(task_file)
work_orders = make_data_dict(work_order_file)
projs = make_data_dict(proj_file)
titles = make_data_dict(title_file)
orders = make_data_dict(order_file)
task_codes = tasks[CODE].keys()
work_order_codes = work_orders[CODE].keys()
proj_codes = projs[CODE].keys()
title_codes = titles[CODE].keys()
order_codes = orders[CODE].keys()
out_lines = []
processes = []
for task_code in task_codes:
    #Expected first
    task = tasks[CODE][task_code]
    curr_status = task.get('status')
    login_group = task.get('assigned_login_group')
    lookup_code = task.get('lookup_code')
    if curr_status != 'Completed' and login_group == dept and 'WORK_ORDER' in lookup_code:
        wo_code = lookup_code
        if wo_code in work_order_codes:
            wo = work_orders[0][wo_code]
            p_code = wo.get('proj_code')
            if p_code in proj_codes:
                proj = projs[CODE][p_code]
		t_code = proj.get('title_code')
		if t_code in title_codes:
		    title = titles[CODE][t_code]
		    o_code = title.get('order_code')
                    if o_code in order_codes:
                        order = orders[CODE][o_code]
                        if order.get('classification') == classification:
                            if task.get('process') not in processes:
                                processes.append(task.get('process'))
		            out_lines.append('''%s | %s | %s | %s | %s | %s | %s | %s''' % (task_code, task.get('process'), task.get('id'), order.get('login'), t_code, o_code, order.get('client_code'), order.get('client_name')))
processes.sort()
for p in processes:
    out_lines.append(p)
#out_lines.append(','.join(processes))                  
out_file = open('%s_task_not_completed_order_class_is_%s.csv' % (dept, classification),'w')
for ol in out_lines:
    out_file.write('%s\n' % ol)
out_file.close()
