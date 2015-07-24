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

def uniq(arr1):
    out = []
    for x in arr1:
        if x not in out:
            out.append(x)
    return out
    
def make_double_digits(number):
    num_str = str(number)
    to_ret = num_str
    the_len = len(num_str)        
    if the_len < 2:
        to_ret = '0%s' % num_str
    return to_ret 

def make_code_digits(number):
    num_str = str(number)
    to_ret = num_str
    the_len = len(num_str)
    if the_len < 5:
        zero_str = ''
        for i in range(0, 5 - the_len):
            zero_str = '%s0' % zero_str
        num_str = '%s%s' % (zero_str, num_str)
    return num_str

_digits = re.compile("\d")
def has_digits(d):
    return bool(_digits.search(d))
def has_letters(c):
    return re.search('[a-zA-Z ]', c)
def make_number(c):
    ret_val = 0.0
    if c not in [None,'']:
        c = '%s' % c
        c = c.replace(',','').replace(' ','') 
        if has_letters(c):
            ret_val = 0.0
        else:
            ret_val = float(c)
    return ret_val

def kill_mul_spaces(origstrg):
    newstrg = ''
    for word in origstrg.split():
        newstrg=newstrg+' '+word
    return newstrg

def make_grouped_filtered_dict(file_name, grouping_col, filter_str):
    the_file = open(file_name, 'r')
    fields = []
    count = 0
    boolio = True
    group_based = {}
    code_col = 0
    t_code_col = 0
    keys = []
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
                    elif field == grouping_col:
                        g_col = fc
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
                grouping_code = ''
                item_dict = {}
                for val in data:
                    val = kill_mul_spaces(val)
                    val = val.strip(' ')
                    item_dict[fields[data_count]] = val
                    if data_count == code_col:
                        this_code = val
                    elif data_count == g_col:
                        grouping_code = val
                    data_count = data_count + 1 
                if grouping_code not in [None,''] and filter_str in grouping_code:
                    if grouping_code not in keys:
                        group_based[grouping_code] = []
                        keys.append(grouping_code)
                    group_based[grouping_code].append(item_dict)
            count = count + 1  
    the_file.close()
    return group_based

def make_grouped_dict(file_name, grouping_col):
    the_file = open(file_name, 'r')
    fields = []
    count = 0
    boolio = True
    group_based = {}
    code_col = 0
    t_code_col = 0
    keys = []
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
                    elif field == grouping_col:
                        g_col = fc
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
                grouping_code = ''
                item_dict = {}
                for val in data:
                    val = kill_mul_spaces(val)
                    val = val.strip(' ')
                    item_dict[fields[data_count]] = val
                    if data_count == code_col:
                        this_code = val
                    elif data_count == g_col:
                        grouping_code = val
                    data_count = data_count + 1 
                if grouping_code not in [None,'']:
                    if grouping_code not in keys:
                        group_based[grouping_code] = []
                        keys.append(grouping_code)
                    group_based[grouping_code].append(item_dict)
            count = count + 1  
    the_file.close()
    return group_based

def make_client_dict(file_name):
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
                        data_dict[val] = ''
                        this_code = val
                    else:
                        data_dict[this_code] = val
                    data_count = data_count + 1 
            count = count + 1  
    the_file.close()
    return data_dict

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

def conform_em():
    user_name = 'stupid'
    path_prefix = '/var/www/html/user_reports_tables/'
    os.system("psql -U postgres twog < /opt/spt/custom/random_scripts/task_conform/order_query > %sorder_list_%s" % (path_prefix, user_name)) 
    os.system("psql -U postgres twog < /opt/spt/custom/random_scripts/task_conform/title_query > %stitle_list_%s" % (path_prefix, user_name)) 
    os.system("psql -U postgres twog < /opt/spt/custom/random_scripts/task_conform/proj_query > %sproj_list_%s" % (path_prefix, user_name)) 
    os.system("psql -U postgres twog < /opt/spt/custom/random_scripts/task_conform/work_order_query > %swork_order_list_%s" % (path_prefix, user_name)) 
    os.system("psql -U postgres twog < /opt/spt/custom/random_scripts/task_conform/client_query > %sclient_list_%s" % (path_prefix, user_name)) 
    os.system("psql -U postgres sthpw < /opt/spt/custom/random_scripts/task_conform/task_query > %stask_list_%s" % (path_prefix, user_name)) 
    orders = make_data_dict('%sorder_list_%s' % (path_prefix, user_name))
    titles = make_grouped_dict('%stitle_list_%s' % (path_prefix, user_name), 'order_code')
    title_lookup = make_data_dict('%stitle_list_%s' % (path_prefix, user_name))
    title_order_codes = titles.keys() 
    projs = make_grouped_dict('%sproj_list_%s' % (path_prefix, user_name), 'title_code')
    proj_title_codes = projs.keys()
    work_orders = make_grouped_dict('%swork_order_list_%s' % (path_prefix, user_name), 'proj_code')
    wos_lookup = make_data_dict('%swork_order_list_%s' % (path_prefix, user_name))
    wo_proj_codes = work_orders.keys()
    tasks = make_grouped_filtered_dict('%stask_list_%s' % (path_prefix, user_name), 'lookup_code', 'WORK_ORDER')
    task_lookup_codes = tasks.keys()
    order_codes = orders.keys()
    client_lookup = make_client_dict('%sclient_list_%s' % (path_prefix, user_name))
    order_codes.sort()
    lines = []
    for order_code in order_codes:
        order = orders[order_code]
        client_name = ''
        client_code = order['client_code']
        if client_code in client_lookup.keys():
            client_name = client_lookup[client_code]
        ts = []
        try:
            ts = titles[order_code]
        except:
            pass
        for title in ts:
            title_code = title['code'] 
            ps = []
            try:
                ps = projs[title_code]
            except:
                pass
            for proj in ps:
                proj_code = proj['code']
                wos = []
                try:
                    wos = work_orders[proj_code]
                except:
                    pass
                for work_order in wos:
                    work_order_code = work_order['code']
                    tsks = []
                    try:
                        tsks = tasks[work_order_code]
                    except:
                        pass
                    t_count = 0
                    for task in tsks:
                        task_code = task['code']
                        if client_name != '':
                            lines.append("update task set order_code = '%s', title_code = '%s', client_code = '%s', client_name = '%s' where code = '%s';" % (order_code, title_code, client_code, client_name, task_code))
                        else:
                            lines.append("update task set order_code = '%s', title_code = '%s' where code = '%s';" % (order_code, title_code, task_code))

    new_file = '/opt/spt/custom/random_scripts/task_conform/conform_these_tasks'
    if os.path.exists(new_file):
        os.system('rm -rf %s' % new_file)
    new_guy = open(new_file, 'w')
    for i in lines:
        new_guy.write('%s\n' % i)
    new_guy.close()

    #throwin_order_report_begin_time = time.time()
    #os.system('psql -U postgres sthpw < /opt/spt/custom/random_scripts/task_conform/conform_these_tasks')
    #throwin_order_report_end_time = time.time()

if True:
    conform_em()
else:
   sys.exit(-1) 

