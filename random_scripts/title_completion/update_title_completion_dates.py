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
    for line in the_file:
        line = line.rstrip('\r\n')
        #data = line.split('\t')
        data = line.split('|')
        if boolio:
            if count == 0:
                for field in data:
                    field = kill_mul_spaces(field)
                    field = field.strip(' ')
                    fields.append(field)
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
                    if data_count == 0:
                        data_dict[val] = {fields[data_count]: val}
                        this_code = val
                    else:
                        data_dict[this_code][fields[data_count]] = val
                    data_count = data_count + 1 
            count = count + 1  
    the_file.close()
    print "File = %s FIELDS = %s" % (file_name, fields)
    return data_dict
opts, title_file = getopt.getopt(sys.argv[1], '-m')
print "title_file = %s" % title_file
opts, proj_file = getopt.getopt(sys.argv[2], '-m')
print "proj_file = %s" % proj_file
opts, work_order_file = getopt.getopt(sys.argv[3], '-m')
print "work_order_file = %s" % work_order_file
opts, task_file = getopt.getopt(sys.argv[4], '-m')
print "task_file = %s" % task_file
opts, status_log_file = getopt.getopt(sys.argv[5], '-m')
print "status_log_file = %s" % status_log_file
title_tbl = make_data_dict(title_file)
print "GOT TITLE TABLE"
proj_tbl = make_data_dict(proj_file)
print "GOT PROJ TABLE"
work_order_tbl = make_data_dict(work_order_file)
print "GOT WORK ORDER TABLE"
task_tbl = make_data_dict(task_file)
print "GOT TASK TABLE"
status_log_tbl = make_data_dict(status_log_file)
print "GOT STATUS LOG TABLE"
title_codes = []
title_codes = sorted(title_tbl.keys())
proj_codes = []
proj_codes = sorted(proj_tbl.keys())
work_order_codes = []
work_order_codes = sorted(work_order_tbl.keys())
task_codes = []
task_codes = sorted(task_tbl.keys())
status_log_codes = []
status_log_codes = sorted(status_log_tbl.keys())
out_lines = []
problem_lines = []
count = 0
title_kids = {}
for tc in title_codes:
    title_kids[tc] = []
    if title_tbl[tc].get('status') == 'Completed' and title_tbl[tc].get('completion_date') in ['',None]:
        for pc in proj_codes:
            if proj_tbl[pc].get('title_code') == tc:
                title_kids[tc].append(pc)
                for wc in work_order_codes:
                    if work_order_tbl[wc].get('proj_code') == pc:
                        title_kids[tc].append(wc)
title_tasks = {}
for tc in title_codes:
    title_tasks[tc] = []
    for lookup_code in title_kids[tc]:
        for kc in task_codes:
            if task_tbl[kc].get('lookup_code') == lookup_code:
                task_id = task_tbl[kc].get('id')
                for sc in status_log_codes:
                    if status_log_tbl[sc].get('search_id') == task_id and status_log_tbl[sc]['to_status'] not in ['Pending','Assignment']:
                        title_tasks[tc].append([kc,status_log_tbl[sc].get('timestamp'),status_log_tbl[sc].get('to_status')])

for tc in title_codes:
    best_time = '0000-00-00 00:00:00.00'
    orig = best_time
    print '%s::::::: %s' % (title_tasks[tc], len(title_tasks[tc]))
    if title_tasks[tc] == []:
        os.system('echo "No information for %s" >> NoInfo' % tc)
        print "CAUGHT"
    for tt in title_tasks[tc]:
        if tt[1] > best_time:
            best_time = tt[1]
    if best_time != orig:
        out_lines.append("update title set completion_date = '%s' where code = '%s';" % (best_time, tc))
        
       
out_file = open('title_completion_fix.sql', 'w')
out_file.write('%s\n' % title_tasks)
for ol in out_lines:
    out_file.write('%s\n' % ol)
out_file.close()
problem_file = open('TitleCompletionProblems', 'w')
for pl in problem_lines:
    problem_file.write('%s\n' % pl)
problem_file.close()

