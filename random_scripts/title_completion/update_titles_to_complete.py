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
opts, proj_task_file = getopt.getopt(sys.argv[1], '-m')
print  "proj_task_file = %s" % proj_task_file
opts, title_file = getopt.getopt(sys.argv[2], '-m')
print  "title_file = %s" % title_file
pt_tbl = make_data_dict(proj_task_file)
title_tbl = make_data_dict(title_file)
title_codes = []
title_codes = sorted(title_tbl.keys())
pt_codes = []
pt_codes = sorted(pt_tbl.keys())
titles_to_complete = {}
for tc in title_codes:
    print "TITLE CODE = %s" % tc
    title = title_tbl[tc]
    actually_complete = True
    proj_codes = []
    task_count = 0
    for pt in pt_codes:
        task = pt_tbl[pt]
        if task.get('title_code') == tc:
            task_count = task_count + 1
            if task.get('status') != 'Completed':
                actually_complete = False
                print "LOOKUP CODE = %s, STATUS = %s" % (task.get('lookup_code'), task.get('status'))
            else:
                proj_codes.append(task.get('lookup_code'))
    if actually_complete and task_count > 0:
        titles_to_complete[tc] = proj_codes

out_lines = []
tcom_codes = []
tcom_codes = sorted(titles_to_complete.keys())
for title_code in tcom_codes:
    out_lines.append("update title set status = 'Completed', client_status = 'Completed' where code = '%s';" % (title_code))

out_file = open('titles_to_complete.sql', 'w')
out_file.write('%s\n' % titles_to_complete)
for ol in out_lines:
    out_file.write('%s\n' % ol)
out_file.close()
