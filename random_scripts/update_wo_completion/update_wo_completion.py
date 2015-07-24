#NEED TO COLLECT ALL WORK HOURS AND REPORT THOSE UNCONNECTED TO WORK ORDERS AND TASKS, CONNECT THEM TO CLIENT AS WELL
import tacticenv
import os, sys, calendar, dateutil, datetime, time, getopt, pprint, re, math
from pyasm.biz import *


def init():
    nothing = 'true'
    yesterday_begin = ''
    last_month_end = ''
    last_month_begin = ''
    next_month_end = ''
    next_month_begin = ''
    yesterday_begin = ''
    yesterday_end = ''
    today_begin = ''
    today_end = ''
    tomorrow_begin = ''
    tomorrow_end = ''
    begin_date = ''
    end_date = ''

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

def fill_wo_completion():
    path_prefix = '/var/www/html/user_reports_tables/'
    os.system("psql -U postgres sthpw < /opt/spt/custom/random_scripts/update_wo_completion/task_query > %swo_count_task_list_general" % (path_prefix)) 
    tasks = make_data_dict('%swo_count_task_list_general' % (path_prefix))
    orders = {}
    titles = {}
    for t in tasks.keys():
        task = tasks[t]
        order_code = task.get('order_code')
        title_code = task.get('title_code')
        if order_code not in [None,'']:
            try:
                orders[order_code][0] = orders[order_code][0] + 1
            except:
                orders[order_code] = [1,0] 
        if title_code not in [None,'']:
            try:
                titles[title_code][0] = titles[title_code][0] + 1
            except:
                titles[title_code] = [1,0]
        status = task.get('status')
        if status == 'Completed':
            if order_code not in [None,'']:
                try:
                    orders[order_code][1] = orders[order_code][1] + 1
                except:
                    orders[order_code] = [0,1] 
            if title_code not in [None,'']:
                try:
                    titles[title_code][1] = titles[title_code][1] + 1
                except:
                    titles[title_code] = [0,1]
            
        

    new_update_order_file = '%supdate_order_wo_completion_var.sql' % path_prefix
    if os.path.exists(new_update_order_file):
        os.system('rm -rf %s' % new_update_order_file)
    new_guy = open(new_update_order_file, 'w')
    for i in orders.keys():
        new_guy.write('''update "order" set wo_count = %s, wo_completed = %s where code = '%s';\n''' % (orders[i][0], orders[i][1], i))
    new_guy.close()

    new_update_title_file = '%supdate_title_wo_completion_var.sql' % path_prefix
    if os.path.exists(new_update_title_file):
        os.system('rm -rf %s' % new_update_title_file)
    new_guy = open(new_update_title_file, 'w')
    for i in titles.keys():
        new_guy.write('''update title set wo_count = %s, wo_completed = %s where code = '%s';\n''' % (titles[i][0], titles[i][1], i))
    new_guy.close()
    
    #Throw the values in there
    #OFF BECAUSE YOU SHOULD PROBABLY CHECK FIRST os.system('psql -U postgres twog < %s' % new_update_order_file)
    os.system('psql -U postgres twog < %s' % new_update_order_file)
    #OFF BECAUSE YOU SHOULD PROBABLY CHECK FIRST os.system('psql -U postgres twog < %s' % new_update_title_file)
    os.system('psql -U postgres twog < %s' % new_update_title_file)
    
fill_wo_completion()

