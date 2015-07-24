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
    print "FIELDS = %s" % fields
    return data_dict
opts, work_order_file = getopt.getopt(sys.argv[1], '-m')
print "work_order_file = %s" % work_order_file
opts, task_file = getopt.getopt(sys.argv[2], '-m')
print "task_file = %s" % task_file
opts, group_file = getopt.getopt(sys.argv[3], '-m')
print "group_file = %s" % group_file
opts, login_in_group_file = getopt.getopt(sys.argv[4], '-m')
print "login_in_group_file = %s" % login_in_group_file
opts, work_hour_file = getopt.getopt(sys.argv[5], '-m')
print "work_hour_file = %s" % work_hour_file

lookup_codes = {}
work_orders = make_data_dict(work_order_file)
#print "WORK ORDERS = %s" % work_orders
tasks = make_data_dict(task_file)
#print "TASKS = %s" % tasks
groups = make_data_dict(group_file)
#print "GROUPS = %s" % groups
login_in_groups = make_data_dict(login_in_group_file)
#print "LOGIN IN GROUPS = %s" % login_in_groups
work_hours = make_data_dict(work_hour_file)
#print "WORK HOURS = %s" % work_hours
work_order_codes = work_orders.keys()
task_codes = tasks.keys()
work_hour_codes = work_hours.keys()
out_lines = []
problem_lines = []
for woc in work_order_codes:
    #Expected first
    s_status = work_orders[woc]['s_status']
    if s_status not in ['retired','r']:
        work_group = work_orders[woc]['work_group']
        estimated_work_hours = work_orders[woc]['estimated_work_hours']
        if work_group not in [None,''] and estimated_work_hours not in [None,'',0,'0']:
            estimated_work_hours = float(estimated_work_hours)
            group_rate = groups[work_group]['hourly_rate']
            if group_rate not in [None,'']:
                group_rate = float(group_rate)
                new_expected_cost = float(estimated_work_hours * group_rate)
                out_lines.append("update work_order set expected_cost = '%s' where code = '%s';" % (new_expected_cost, woc))
        else:
            problem_lines.append("Work Order %s is incomplete. Work Group = %s, Est_WH = %s" % (woc, work_group, estimated_work_hours))
        task_code = work_orders[woc]['task_code']
        if task_code not in [None,'']:
            summed_actual_cost = 0
            if task_code in task_codes:
                if tasks[task_code]['s_status'] not in ['retired','r']:
                    for whc in work_hour_codes:
                        if work_hours[whc]['task_code'] == task_code:
                            user = work_hours[whc]['login']
                            straight_time = work_hours[whc]['straight_time']
                            if straight_time not in [None,'',0,'0']:
                                straight_time = float(straight_time)
                                group_chosen = ''
                                group_rate = 0
                                for lg in login_in_groups.keys():
                                    if login_in_groups[lg]['login'] == user:
                                        if group_chosen == '':
                                            group_chosen = login_in_groups[lg]['login_group']
                                            if group_chosen in groups.keys():
                                                group_rate = groups[group_chosen]['hourly_rate']
                                                if group_rate not in [None,'',0,'0.0']:
                                                    group_rate = float(group_rate)
                                                else:
                                                    group_rate = 0
                                        else:
                                            this_group = login_in_groups[lg]['login_group']
                                            if this_group in groups.keys():
                                                this_rate = groups[this_group]['hourly_rate']
                                                if this_rate not in [None,'',0,'0.0']:
                                                    this_rate = float(this_rate)
                                                else:
                                                    this_rate = 0
                                                if this_rate > group_rate:
                                                    group_rate = this_rate
                                                    group_chosen = this_group
                                if group_rate not in [None,'']:
                                    if group_rate == 0:
                                        problem_lines.append("GROUP RATE WAS 0 for %s, user %s, group %s" % (whc, user, group_chosen)) 
                                    else:
                                        summed_actual_cost = summed_actual_cost + float(group_rate * straight_time)
                    if summed_actual_cost not in [None,'']:
                        out_lines.append("update work_order set actual_cost = '%s' where code = '%s';" % (summed_actual_cost, woc))
                                           
                                
out_file = open('work_order_cost_fix','w')
for ol in out_lines:
    out_file.write('%s\n' % ol)
out_file.close()
problem_file = open('work_order_cost_problems', 'w')
for pl in problem_lines:
    problem_file.write('%s\n' % pl)
problem_file.close()
