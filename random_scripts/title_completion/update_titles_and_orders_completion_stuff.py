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
opts, order_file = getopt.getopt(sys.argv[3], '-m')
print  "order_file = %s" % order_file
pt_tbl = make_data_dict(proj_task_file)
title_tbl = make_data_dict(title_file)
order_tbl = make_data_dict(order_file)
order_codes = []
order_codes = sorted(order_tbl.keys())
title_codes = []
title_codes = sorted(title_tbl.keys())
pt_codes = []
pt_codes = sorted(pt_tbl.keys())
titles_to_complete = {}
order_update_dict = {}
for tc in title_codes:
    print "TITLE CODE = %s" % tc
    title = title_tbl[tc]
    order_code = title.get('order_code')
    print "ORDER_CODE = %s" % order_code
    title_completed = False
    if title.get('status') == 'Completed':
        title_completed = True
    else:
        actually_complete = True
        proj_codes = []
        task_count = 0
        last_completed = '1999-01-01'
        for pt in pt_codes:
            task = pt_tbl[pt]
            if task.get('title_code') == tc:
                task_count = task_count + 1
                if task.get('status') != 'Completed':
                    actually_complete = False
                    print "LOOKUP CODE = %s, STATUS = %s" % (task.get('lookup_code'), task.get('status'))
                else:
                    proj_codes.append(task.get('lookup_code'))
                    if last_completed < task.get('actual_end_date'):
                        last_completed = task.get('actual_end_date')
        if actually_complete and task_count > 0:
            titles_to_complete[tc] = {'proj_codes': proj_codes, 'completion_date': last_completed}
            title_completed = True
        if order_code in order_codes:
            try: 
                order_update_dict[order_code]['titles_total'] = order_update_dict[order_code]['titles_total'] + 1
            except:
                order_update_dict[order_code] = {'titles_completed': 0, 'title_codes_completed': '', 'titles_total': 1}
                pass
                
            if title_completed:
                order_update_dict[order_code]['titles_completed'] = order_update_dict[order_code]['titles_completed'] + 1 
                if order_update_dict[order_code]['title_codes_completed'] == '': 
                    order_update_dict[order_code]['title_codes_completed'] = tc 
                else:
                    order_update_dict[order_code]['title_codes_completed'] = '%s,%s' % (order_update_dict[order_code]['title_codes_completed'], tc) 
                
            
            

out_lines = []
tcom_codes = []
tcom_codes = sorted(titles_to_complete.keys())
for title_code in tcom_codes:
    out_lines.append("update title set status = 'Completed', client_status = 'Completed', completion_date = '%s' where code = '%s';" % (titles_to_complete[title_code].get('completion_date'), title_code))

out_file = open('titles_to_complete.sql', 'w')
out_file.write('%s\n' % titles_to_complete)
for ol in out_lines:
    out_file.write('%s\n' % ol)
out_file.close()

print "ORDER UPDATE DICT = %s" % order_update_dict
out_lines = []
oud_codes = []
oud_codes = sorted(order_update_dict.keys())
for order_code in oud_codes:
    entry = order_update_dict[order_code]
    print "ENTRY for %s = %s" % (order_code, entry) 
    needs_completion_review = False 
    if entry.get('titles_total') == entry.get('titles_completed') and order_tbl[order_code].get('classification') != 'Completed':
        needs_completion_review = True 
        print "NEEDS REVIEW"
    else:
        print "DO NOT REVIEW"
    out_lines.append('''update "order" set titles_completed = '%s', title_codes_completed = '%s', titles_total = '%s' where code = '%s';''' % (entry.get('titles_completed'), entry.get('title_codes_completed'), entry.get('titles_total'), order_code))
    if order_tbl[order_code].get('needs_completion_review') not in ['1',1,'True','T','t',True] and needs_completion_review:
        out_lines.append('''update "order" set needs_completion_review = 'True' where code = '%s';''' % order_code)

out_file = open('order_update.sql', 'w')
out_file.write('%s\n' % order_update_dict)
for ol in out_lines:
    out_file.write('%s\n' % ol)
out_file.close()


































