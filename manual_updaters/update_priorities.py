#NEED TO COLLECT ALL WORK HOURS AND REPORT THOSE UNCONNECTED TO WORK ORDERS AND TASKS, CONNECT THEM TO CLIENT AS WELL
import tacticenv
import os, sys, calendar, dateutil, datetime, time, getopt, pprint, re, math
from pyasm.biz import *


def init():
    nothing = 'true'

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
   
def do_updates():
    path_prefix = '/var/www/html/user_reports_tables/'
    os.system("psql -U postgres twog < /opt/spt/custom/manual_updaters/queries/title_priority_query > %stitle_priority_list_general" % (path_prefix)) 
    os.system("psql -U postgres sthpw < /opt/spt/custom/manual_updaters/queries/task_query > %stask_list_general" % (path_prefix)) 
    titles = make_data_dict('%stitle_priority_list_general' % (path_prefix))
    title_codes = titles.keys() 
    tasks = make_data_dict('%stask_list_general' % (path_prefix))
    task_codes = tasks.keys() 
    titles_to_do = []
    for task_code in task_codes:
        task = tasks[task_code]
        if task.get('active') in ['True','true','1','t'] and task.get('assigned_login_group') == 'qc':
            ttitle = task.get('title_code')
            if ttitle not in titles_to_do and ttitle not in [None,'']: 
                titles_to_do.append(ttitle)
    titles_to_do2 = {}
    taken_prios = {} 
    last_prio = 1
    
    print "TITLES TO DO = %s" % titles_to_do
    for title_code in titles_to_do:
        try:
            title = titles[title_code]
            priority = title.get('priority')
            if priority not in [None,'']:
                priority = float(priority)
                if priority not in [5000,300,200,150,100,90,80]:
                    if priority > 1:
                        print "HERE"
                        if title_code not in titles_to_do2.keys():
                            titles_to_do2[title_code] = -1
                        titles_to_do2[title_code] = priority  
                        int_prio = int(priority)
                        int_prio_str = str(int_prio)
                        if int_prio_str not in taken_prios.keys():
                            taken_prios[int_prio_str] = last_prio
                            last_prio = last_prio + 1
        except:
            pass
    print "TAKEN PRIOS = %s" % taken_prios
    print "TITLES TO DO2 = %s" % titles_to_do2
    lines = []
    for title_code in titles_to_do2:
        old_priority = titles_to_do2[title_code]
        tmp = str(int(old_priority))
        int_prio = taken_prios[tmp]
        new_priority = float(int_prio) + float((float(old_priority) - int(old_priority))) 
        #new_priority = float(old_priority/4) 
        print "%s %s to %s" % (title_code, old_priority, new_priority)
        lines.append("update title set priority = %s where code = '%s';" % (new_priority, title_code))
    new_prio_file = '/var/www/html/user_reports_tables/title_priority_update'
    if os.path.exists(new_prio_file):
        os.system('rm -rf %s' % new_prio_file)
    new_guy = open(new_prio_file, 'w')
    for i in lines:
        new_guy.write('%s\n' % i)
    new_guy.close()

    os.system('psql -U postgres twog < %s' % new_prio_file)
    print 'DONE'
                
                
            

        

do_updates()
# Insert into DB: timestamp, work_orders due today & codes, error & codes, error_types & codes number late & codes, orphaned title, proj, wo, task numbers, no due date tasks, titles, orders counts,  

