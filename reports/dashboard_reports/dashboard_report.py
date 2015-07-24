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

def get_base_dict(login_dict, day_span):
    hours_potential_worked = float(day_span * 8)
    keys = login_dict.keys()
    base_dict = {}
    inserted = []
    for k in keys:
        if k not in inserted:
            base_dict[k] = {'login': k, 'first_name': login_dict[k]['first_name'], 'last_name': login_dict[k]['last_name'], 'number_of_days': day_span, 'hours_potential_worked': hours_potential_worked}
            inserted.append(k)
    base_dict['Not Set'] = {'login': 'Not Set', 'first_name': 'N/A', 'last_name': 'N/A', 'number_of_days': day_span, 'hours_potential_worked': hours_potential_worked}
    return base_dict 

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

def calc_dates():
    today = datetime.datetime.today()
    today = datetime.datetime(today.year, today.month, today.day)
    today = str(today)
    today_split = today.split('-')
    last_month_year = next_month_year = year = int(today_split[0])
    month = int(today_split[1])
    day = int(today_split[2].split(' ')[0])
    last_month = month - 1
    if last_month < 1:
        last_month = 12
        last_month_year = year - 1
    next_month = month + 1
    if next_month > 12:
        next_month = 1
        next_month_year = year + 1
    yesterday = day - 1
    yesterday_month = month
    yesterday_year = year
    last_month_range = int(calendar.monthrange(last_month_year, last_month)[1])
    this_month_range = int(calendar.monthrange(year, month)[1])
    next_month_range = int(calendar.monthrange(next_month_year, next_month)[1])

    if yesterday < 1:
        yesterday_month = yesterday_month - 1
        yesterday = last_month_range
        if yesterday_month < 0:
            yesterday_year = yesterday_year - 1
            yesterday_month = 12
            yesterday = 31
 
    tomorrow = day + 1
    tomorrow_month = month
    tomorrow_year = year
    if tomorrow > this_month_range:
        tomorrow = 1    
        tomorrow_month = tomorrow_month + 1            
        if tomorrow_month > 12:
            tomorrow_year = tomorrow_year + 1
            tomorrow_month = 1
   
    last_month = make_double_digits(last_month)
    next_month = make_double_digits(next_month)
    yesterday_month = make_double_digits(yesterday_month)
    tomorrow_month = make_double_digits(tomorrow_month)
    day = make_double_digits(day)
    month = make_double_digits(month)
    tomorrow = make_double_digits(tomorrow)
    yesterday = make_double_digits(yesterday)
    last_month_end = '%s-%s-%s 23:59:59' % (last_month_year, last_month, last_month_range)     
    last_month_begin = '%s-%s-01 00:00:00' % (last_month_year, last_month)     
    next_month_end = '%s-%s-%s 23:59:59' % (next_month_year, next_month, next_month_range)     
    next_month_begin = '%s-%s-01 00:00:00' % (next_month_year, next_month)     
    yesterday_begin = '%s-%s-%s 00:00:00' % (yesterday_year, yesterday_month, yesterday) 
    yesterday_end = '%s-%s-%s 23:59:59' % (yesterday_year, yesterday_month, yesterday) 
    today_begin = '%s-%s-%s 00:00:00' % (year, month, day)
    today_end = '%s-%s-%s 23:59:59' % (year, month, day)
    tomorrow_begin = '%s-%s-%s 00:00:00' % (tomorrow_year, tomorrow_month, tomorrow) 
    tomorrow_end = '%s-%s-%s 23:59:59' % (tomorrow_year, tomorrow_month, tomorrow) 
    return {'yesterday': yesterday_begin.split(' ')[0], 'last_month': last_month_end.split(' ')[0], 'next_month': next_month_end.split(' ')[0], 'today': today_end.split(' ')[0], 'tomorrow': tomorrow_end.split(' ')[0]}

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

def make_wh_dict(file_name):
    the_file = open(file_name, 'r')
    fields = []
    count = 0
    boolio = True
    task_based = {}
    code_col = 0
    t_code_col = 0
    login_col = 0
    tkeys = []
    lkeys = []
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
                    elif field == 'task_code':
                        t_code_col = fc
                    elif field == 'login':
                        login_col = fc
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
                task_code = ''
                login = ''
                wh_dict = {}
                for val in data:
                    val = kill_mul_spaces(val)
                    val = val.strip(' ')
                    wh_dict[fields[data_count]] = val
                    if data_count == code_col:
                        this_code = val
                    elif data_count == t_code_col:
                        task_code = val
                    elif data_count == login_col:
                        login = val
                    data_count = data_count + 1 
                if task_code not in [None,'']:
                    if task_code not in tkeys:
                        task_based[task_code] = []
                        tkeys.append(task_code)
                    task_based[task_code].append(wh_dict)
                else:
                    if login not in lkeys:
                        task_based[login] = []
                        lkeys.append(login)
                    task_based[login].append(wh_dict)
            count = count + 1  
    the_file.close()
    return task_based

def get_max_id(file_name):
    the_file = open(file_name)
    count = 0
    max_id = 0
    for line in the_file:
        if count == 2:
            max_str = line
            max_str = max_str.rstrip('\r\n')
            max_str = max_str.strip()
            if max_str not in [None,'']:
                max_id = int(max_str)
            else:
                max_id = 0
        count = count + 1
    return max_id

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

def get_day_span(begin_date, end_date):
    from datetime import datetime
    full_day_secs = 24 * 60 * 60
    if begin_date in [None, '']:
        return 9999999
    if end_date in [None, '']:
        return 9999999
    if ' ' not in begin_date:
        begin_date = '%s 00:00:00' % begin_date
    if ' ' not in end_date:
        end_date = '%s 00:00:00' % end_date
    date_format = "%Y-%m-%d %H:%M:%S"
    a = datetime.strptime(begin_date, date_format)
    b = datetime.strptime(end_date, date_format)
    delta = b - a
    days = delta.days
    day_secs = full_day_secs * days
    begin_time = begin_date.split(' ')
    end_time = end_date.split(' ')
    if len(begin_time) > 1 and len(end_time) > 1:
        begin_time = begin_time[1]
        end_time = end_time[1]
        begin_sections = begin_time.split(':')
        end_sections = end_time.split(':')
        begin_seconds = int(begin_sections[0]) * 60 * 60
        begin_seconds = (int(begin_sections[1]) * 60) + begin_seconds
        begin_seconds = begin_seconds + int(begin_sections[2])
        end_seconds = int(end_sections[0]) * 60 * 60
        end_seconds = (int(end_sections[1]) * 60) + end_seconds
        end_seconds = end_seconds + int(end_sections[2])
    time_diff = int(day_secs + (end_seconds - begin_seconds))
    diff_days = float(float(time_diff)/float(full_day_secs))
    return diff_days

def fill_login_group(base_dict, login_in_group_dict):
    logins = base_dict.keys()
    lig_keys = login_in_group_dict.keys()
    for login in logins:
        base_dict[login]['login_group'] = ''
        for lk in lig_keys:
            if login_in_group_dict[lk].get('login') == login:
                if base_dict[login]['login_group'] == '':
                    base_dict[login]['login_group'] = login_in_group_dict[lk]['login_group']
                else:
                    base_dict[login]['login_group'] = '%s,%s' % (base_dict[login]['login_group'], login_in_group_dict[lk]['login_group'])
    base_dict['Not Set']['login_group'] = 'Not Set'
    return base_dict

def set_default_group_and_rate(base_dict, login_groups):
    logins = base_dict.keys()
    group_keys = login_groups.keys()
    for lg in logins:
        default_group = ''
        default_rate = 20.0
        groups = base_dict[lg]['login_group'].split(',')
        for group in groups:
            if group in group_keys:
                #print "GROUP: %s" % login_groups[group]
                hourly_rate = login_groups[group].get('hourly_rate')
                if hourly_rate in [None,'']:
                    hourly_rate = 0
                else:
                    hourly_rate = float(hourly_rate)
                if hourly_rate > default_rate:
                    default_rate = hourly_rate
                    default_group = group
        base_dict[lg]['default_group'] = default_group
        base_dict[lg]['default_rate'] = default_rate
    return base_dict

        
   
def fill_report_vars(user_name, max_diff, efficiency_cost_prev_days):
    begin_time = time.time()
    pp3 = pprint.PrettyPrinter(depth=3)
    pp4 = pprint.PrettyPrinter(depth=4)
    pp6 = pprint.PrettyPrinter(depth=6)
    pp9 = pprint.PrettyPrinter(depth=9)
    max_diff = int(max_diff)
    efficiency_cost_prev_days = int(efficiency_cost_prev_days)
    dates_here = calc_dates()
    dump_fill_begin_time = time.time()
    #print "D BEGIN TIME = %s" % dump_fill_begin_time
    path_prefix = '/var/www/html/user_reports_tables/'
    os.system("psql -U postgres twog < /opt/spt/custom/reports/dashboard_reports/order_query > %sorder_list_%s" % (path_prefix, user_name)) 
    os.system("psql -U postgres twog < /opt/spt/custom/reports/dashboard_reports/title_query > %stitle_list_%s" % (path_prefix, user_name)) 
    os.system("psql -U postgres twog < /opt/spt/custom/reports/dashboard_reports/proj_query > %sproj_list_%s" % (path_prefix, user_name)) 
    os.system("psql -U postgres twog < /opt/spt/custom/reports/dashboard_reports/work_order_query > %swork_order_list_%s" % (path_prefix, user_name)) 
    os.system("psql -U postgres twog < /opt/spt/custom/reports/dashboard_reports/equipment_used_query > %sequipment_used_list_%s" % (path_prefix, user_name)) 
    #os.system("psql -U postgres twog < /opt/spt/custom/reports/dashboard_reports/status_log_query > %sstatus_log_list_%s" % (path_prefix, user_name)) 
    os.system("psql -U postgres twog < /opt/spt/custom/reports/dashboard_reports/production_error_query > %sproduction_error_list_%s" % (path_prefix, user_name)) 
    os.system("psql -U postgres twog < /opt/spt/custom/reports/dashboard_reports/client_query > %sclient_list_%s" % (path_prefix, user_name)) 
    os.system("psql -U postgres sthpw < /opt/spt/custom/reports/dashboard_reports/task_query > %stask_list_%s" % (path_prefix, user_name)) 
    os.system("psql -U postgres sthpw < /opt/spt/custom/reports/dashboard_reports/login_query > %slogin_list_%s" % (path_prefix, user_name)) 
    os.system("psql -U postgres sthpw < /opt/spt/custom/reports/dashboard_reports/login_group_query > %slogin_group_list_%s" % (path_prefix, user_name)) 
    os.system("psql -U postgres sthpw < /opt/spt/custom/reports/dashboard_reports/login_in_group_query > %slogin_in_group_list_%s" % (path_prefix, user_name)) 
    os.system("psql -U postgres twog < /opt/spt/custom/reports/dashboard_reports/delete_reports")
    os.system("psql -U postgres twog < /opt/spt/custom/reports/dashboard_reports/reset_report_ids") 
    os.system("psql -U postgres twog < /opt/spt/custom/reports/dashboard_reports/max_order_id_query > %smax_order_id_%s" % (path_prefix, user_name)) 
    os.system("psql -U postgres twog < /opt/spt/custom/reports/dashboard_reports/max_wo_id_query > %smax_wo_id_%s" % (path_prefix, user_name)) 
    os.system("psql -U postgres twog < /opt/spt/custom/reports/dashboard_reports/max_err_id_query > %smax_err_id_%s" % (path_prefix, user_name)) 
    os.system("psql -U postgres twog < /opt/spt/custom/reports/dashboard_reports/max_report_day_id_query > %smax_report_day_id_%s" % (path_prefix, user_name)) 
    print "DONE DUMPING: %s" % (time.time() - dump_fill_begin_time)
    work_hours = None
    task_work_hour_codes = []
    wh_by_client = None
    wh_by_platform = None
    wh_by_login = None
    wh_by_day = None
    wh_by_group = None
    if efficiency_cost_prev_days > 0:
        os.system("psql -U postgres sthpw < /opt/spt/custom/reports/dashboard_reports/work_hour_query > %swork_hour_list_%s" % (path_prefix, user_name)) 
        wh_time = time.time()
        work_hours = make_wh_dict('%swork_hour_list_%s' % (path_prefix, user_name))
        #print "WH TIME = %s" % (time.time() - wh_time)
        task_work_hour_codes = work_hours.keys()
        wh_by_client = {}
        wh_by_platform = {}
        wh_by_login = {}
        wh_by_day = {}
        wh_by_group = {}

    #print "WORK HOURS"
    #pp4.pprint(work_hours)    
    max_order_id = get_max_id('%smax_order_id_%s' % (path_prefix, user_name))
    print "MAX_ID= %s" % max_order_id
    new_id = max_order_id 
    print "NEW ID = %s" % new_id
    max_wo_id = get_max_id('%smax_wo_id_%s' % (path_prefix, user_name))
    print "MAX_ID= %s" % max_wo_id
    new_wor_id = max_wo_id 
    max_err_id = get_max_id('%smax_err_id_%s' % (path_prefix, user_name))
    print "MAX_ID= %s" % max_err_id
    new_err_id = max_err_id 
    max_report_day_id = get_max_id('%smax_report_day_id_%s' % (path_prefix, user_name))
    print "MAX_ID= %s" % max_report_day_id
    new_report_day_id = max_report_day_id 
    order_time = time.time()
    print "ORDERS"
    orders = make_data_dict('%sorder_list_%s' % (path_prefix, user_name))
    #print "ORDER TIME = %s" % (time.time() - order_time)
    title_time = time.time()
    print "TITLES"
    titles = make_grouped_dict('%stitle_list_%s' % (path_prefix, user_name), 'order_code')
    title_lookup = make_data_dict('%stitle_list_%s' % (path_prefix, user_name))
    title_order_codes = titles.keys() 
    #print "TITLE TIME = %s" % (time.time() - title_time)
    proj_time = time.time()
    print "PROJS"
    projs = make_grouped_dict('%sproj_list_%s' % (path_prefix, user_name), 'title_code')
    proj_title_codes = projs.keys()
    #print "PROJ TIME = %s" % (time.time() - proj_time)
    wo_time = time.time()
    print "WORK ORDERS"
    work_orders = make_grouped_dict('%swork_order_list_%s' % (path_prefix, user_name), 'proj_code')
    wos_lookup = make_data_dict('%swork_order_list_%s' % (path_prefix, user_name))
    wo_proj_codes = work_orders.keys()
    #print "WORK ORDER TIME = %s" % (time.time() - wo_time)
    eq_time = time.time()
    print "EQUIPMENT"
    equipment = make_grouped_dict('%sequipment_used_list_%s' % (path_prefix, user_name), 'work_order_code')
    eq_wo_codes = equipment.keys()
    #print "EQ TIME = %s" % (time.time() - eq_time)
    pe_time = time.time()
    print "PRODUCTION ERRORS"
    production_errors = make_data_dict('%sproduction_error_list_%s' % (path_prefix, user_name))
    #print "PRODUCTION ERROR TIME = %s" % (time.time() - pe_time)
    pec_time = time.time()
    production_error_codes = production_errors.keys()
    #print "PRODUCTION ERROR CODE TIME = %s" % (time.time() - pec_time)
    #status_logs = make_data_dict('%sstatus_log_list_%s' % (path_prefix, user_name))
    task_time = time.time()
    print "TASKS"
    tasks = make_grouped_filtered_dict('%stask_list_%s' % (path_prefix, user_name), 'lookup_code', 'WORK_ORDER')
    task_lookup_codes = tasks.keys()
    #print "TASK TIME = %s" % (time.time() - task_time)
    #print "DONE DICTING %s" % (time.time() - dump_fill_begin_time)
    order_codes = orders.keys()
    login_time = time.time()
    logins = make_data_dict('%slogin_list_%s' % (path_prefix, user_name))
    #print "LOGIN TIME = %s" % (time.time() - login_time)
    lg_time = time.time()
    login_groups = make_data_dict('%slogin_group_list_%s' % (path_prefix, user_name))
    #print "LOGIN GROUP TIME = %s" % (time.time() - lg_time)
    login_group_codes = login_groups.keys()
    lig_time = time.time()
    login_in_groups = make_data_dict('%slogin_in_group_list_%s' % (path_prefix, user_name))
    #print "LOGIN IN GROUPS TIME = %s" % (time.time() - lig_time)
    dump_fill_end_time = time.time()
    client_lookup = make_client_dict('%sclient_list_%s' % (path_prefix, user_name))
    #print "DUMP FILL TIME = %s" % (dump_fill_end_time - dump_fill_begin_time)
    #work_hours = make_data_dict('%swork_hour_list_%s' % (path_prefix, user_name))
    record_begin_time = time.time()
    lr1_time = time.time()
    login_report = get_base_dict(logins, max_diff)
    #print "LOGIN REPORT 1 TIME = %s" % (time.time() - lr1_time)
    lr2_time = time.time()
    login_report = fill_login_group(login_report, login_in_groups)
    print "LOGIN REPORT = %s" % login_report
    #print "LOGIN REPORT 2 TIME = %s" % (time.time() - lr2_time)
    lr3_time = time.time()
    login_report = set_default_group_and_rate(login_report, login_groups)
    print "LOGIN REPORT 2 = %s" % login_report
    #print "LOGIN REPORT 3 TIME = %s" % (time.time() - lr3_time)
    login_codes = login_report.keys()
    current_time_flat = time.time()        
    current_time = datetime.datetime.fromtimestamp(current_time_flat).strftime('%Y-%m-%d %H:%M:%S')
    print "CURRENT TIME = %s" % current_time
    os.system('echo "current_time = %s" > /opt/spt/custom/reports/dashboard_reports/current_time' % current_time)
    current_day = current_time.split(' ')[0]
    current_split = current_day.split('-')
    yesterday = dates_here['yesterday']
    tomorrow = dates_here['tomorrow']
    last_month = dates_here['last_month']
    next_month = dates_here['next_month']
    this_month = '%s-%s' % (current_split[0], current_split[1])
    current_month = this_month
    #print "THIS MONTH = %s" % this_month
    order_clients = {}
    order_platforms = {}
    order_days = {'expected_cost': 0.0, 'expected_price': 0.0, 'actual_cost': 0.0, 'price': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'wh_billable_cost': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'estimated_work_hours': 0.0, 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_expected_cost': 0.0, 'eq_actual_cost': 0.0, 'due_dates': {}, 'completion_dates': {}, 'billed_dates': {}, 'order_codes': '', 'client_code': '0', 'by_billed': {}, 'by_classification': {}, 'month_completion_dates': {}, 'month_due_dates': {}, 'month_billed_dates': {}} 
    orders_no_due = []
    orders_late = []
    orders_due = []
    future_orders = {}
    titles_late = []
    titles_due = []
    titles_no_due = []
    title_completed_yesterday = []
    future_titles = {}
    tasks_late = []
    tasks_due = []
    future_tasks = {}
    task_day = {'completion_dates': {}, 'due_dates': {}, 'clients': {}, 'platforms': {}, 'by_status': {}, 'month_completion_dates': {}, 'month_due_dates': {}}
    tasks_no_due = []
    orders_been_priced = []
    order_top_fields = {'expected_cost': 'expected_cost', 'expected_price': 'expected_price', 'actual_cost': 'actual_cost', 'price': 'price'} 
    print "END OF TOP"

    def id_only(the_code):
        the_thing = re.findall("(\d+)", the_code)[0]
        the_int = int(the_thing)
        the_id = str(the_int)
        return the_id

    sum_em_eqs_time = 0
    def sum_em_eqs(record, to_sum_dict, sum_em_eqs_time):
        seqt = time.time()
        record['eq_actual_hours'] = float(record['eq_actual_hours']) + to_sum_dict['actual_duration']
        record['eq_expected_hours'] = float(record['eq_expected_hours']) + to_sum_dict['expected_duration']
        record['eq_actual_cost'] = float(record['eq_actual_cost']) + to_sum_dict['actual_cost']
        record['eq_expected_cost'] = float(record['eq_expected_cost']) + to_sum_dict['expected_cost']
        sum_em_eqs_time = sum_em_eqs_time + (time.time() - seqt)
        return [record, sum_em_eqs_time]

    sum_em_whs_time = 0
    def sum_em_whs(record, to_sum_dict, sum_em_whs_time): 
        sewt = time.time()
        record['wh_total_hours'] = float(record['wh_total_hours']) + to_sum_dict['total_hours']
        record['wh_billable_hours'] = float(record['wh_billable_hours']) + to_sum_dict['billable_hours']
        record['wh_actual_cost'] = float(record['wh_actual_cost']) + to_sum_dict['actual_cost']
        record['wh_estimated_cost'] = float(record['wh_estimated_cost']) + to_sum_dict['estimated_cost']
        record['wh_billable_cost'] = float(record['wh_billable_cost']) + to_sum_dict['billable_cost']
        record['estimated_work_hours'] = float(record['estimated_work_hours']) + to_sum_dict['estimated_work_hours']
        if 'all' in record.keys():
            id_only_code = id_only(to_sum_dict['code'])
            if record['all'] in [None,'',[]]:
                record['all'].append(id_only_code)
            elif id_only_code not in record['all']:
                record['all'].append(id_only_code) # '%s,%s' % (record['all'], id_only_code)
        sum_em_whs_time = sum_em_whs_time + (time.time() - sewt)
        return [record, sum_em_whs_time]

    sum_em_time = 0
    def sum_em(record, to_sum_dict, fields, sum_em_time): 
        semt = time.time()
        for field in fields.keys():
            val = to_sum_dict[fields[field]].replace(' ','').replace(',','')
            if val in [None,''] or has_letters(val):
                val = 0.0
            else:
                val = float(val.replace(',','').replace('.00.00','.00').replace('.00.','.00').replace('$','').replace('..','.'))
            record[field] = float(record[field]) + val 
        sum_em_time = sum_em_time + (time.time() - semt)
        if 'order_codes' in record.keys():
            id_only_code = id_only(to_sum_dict['code'])
            if record['order_codes'] in [None,'']:
                record['order_codes'] = id_only_code
            elif id_only_code not in record['order_codes']:
                record['order_codes'] = '%s,%s' % (record['order_codes'], id_only_code)
        return [record, sum_em_time]

    main_body_time = time.time()
    order_codes.sort()
    for order_code in order_codes:
        late = False
        future = False
        order = orders[order_code]
        classification = order['classification']
        platform = order['platform']
        if platform in [None,'']:
            platform = 'No Platform'
        billed_bool = order['closed']
        billed = ''
        if billed_bool in [False,None,'','f',0,'0','false']:
            billed = 'Not Billed'
        elif billed_bool in [True,1,'t','true','1']:
            billed = 'Billed'
        if classification not in [None,'','master','cancelled','Master','Cancelled','Test']:
            client_code = order['client_code']
            order_completion_day = order['completion_date'].split(' ')[0]
            o_completion_diff = int(get_day_span(current_day, order_completion_day))
            if order_completion_day in [None,'']:
                order_completion_day = '1999-01-01'
            ocms = order_completion_day.split('-')
            order_completion_month = '%s-%s' % (ocms[0], ocms[1])

            order_billed_day = order['billed_date'].split(' ')[0]
            o_billed_diff = int(get_day_span(current_day, order_billed_day))
            if order_billed_day in [None,'']:
                order_billed_day = '1999-01-01'
            ocms = order_billed_day.split('-')
            order_billed_month = '%s-%s' % (ocms[0], ocms[1])

            order_due_day = order['due_date'].split(' ')[0] 
            o_due_diff = int(get_day_span(current_day, order_due_day))
            if order_due_day in [None,'']:
                order_due_day = '1999-01-01'
                orders_no_due.append(order_code)     
            odms = order_due_day.split('-')
            order_due_month = '%s-%s' % (odms[0], odms[1])
            if classification not in ['completed','Completed'] and o_due_diff < 0:
                orders_late.append(order_code)
                late = True
            elif classification not in ['completed','Completed'] and o_due_diff == 0:
                orders_due.append(order_code)
            elif classification not in  ['completed','Completed'] and o_due_diff > 0:
                future = True
                if order_due_day not in future_orders.keys():
                    future_orders[order_due_day] = []
                future_orders[order_due_day].append(order_code)
            if future and 'future' not in order_days.keys():
                order_days['future'] = {'expected_cost': 0.0, 'expected_price': 0.0, 'actual_cost': 0.0, 'price': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'wh_billable_cost': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'estimated_work_hours': 0.0, 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_expected_cost': 0.0, 'eq_actual_cost': 0.0, 'order_codes': '', 'client_code': '0'}  
            if late and 'late' not in order_days.keys():
                order_days['late'] = {'expected_cost': 0.0, 'expected_price': 0.0, 'actual_cost': 0.0, 'price': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'wh_billable_cost': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'estimated_work_hours': 0.0, 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_expected_cost': 0.0, 'eq_actual_cost': 0.0, 'order_codes': '', 'client_code': '0'}  
            if order_due_day not in order_days['due_dates'].keys():
                order_days['due_dates'][order_due_day] = {'expected_cost': 0.0, 'expected_price': 0.0, 'actual_cost': 0.0, 'price': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'wh_billable_cost': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'estimated_work_hours': 0.0, 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_expected_cost': 0.0, 'eq_actual_cost': 0.0, 'order_codes': '', 'by_classification': {}, 'by_billed': {}, 'client_code': '0'}  
            if order_due_month not in order_days['month_due_dates'].keys():
                order_days['month_due_dates'][order_due_month] = {'expected_cost': 0.0, 'expected_price': 0.0, 'actual_cost': 0.0, 'price': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'wh_billable_cost': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'estimated_work_hours': 0.0, 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_expected_cost': 0.0, 'eq_actual_cost': 0.0, 'order_codes': '', 'by_classification': {}, 'by_billed': {}, 'client_code': '0'}  
            if billed not in order_days['by_billed'].keys():
                order_days['by_billed'][billed] = {'expected_cost': 0.0, 'expected_price': 0.0, 'actual_cost': 0.0, 'price': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'wh_billable_cost': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'estimated_work_hours': 0.0, 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_expected_cost': 0.0, 'eq_actual_cost': 0.0, 'order_codes': '', 'client_code': '0'}  
            if classification not in order_days['by_classification'].keys():
                order_days['by_classification'][classification] = {'expected_cost': 0.0, 'expected_price': 0.0, 'actual_cost': 0.0, 'price': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'wh_billable_cost': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'estimated_work_hours': 0.0, 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_expected_cost': 0.0, 'eq_actual_cost': 0.0, 'order_codes': '', 'client_code': '0'}  
            if billed not in order_days['due_dates'][order_due_day]['by_billed'].keys():
                order_days['due_dates'][order_due_day]['by_billed'][billed] = {'expected_cost': 0.0, 'expected_price': 0.0, 'actual_cost': 0.0, 'price': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'wh_billable_cost': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'estimated_work_hours': 0.0, 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_expected_cost': 0.0, 'eq_actual_cost': 0.0, 'order_codes': '', 'client_code': '0'}  
            if billed not in order_days['month_due_dates'][order_due_month]['by_billed'].keys():
                order_days['month_due_dates'][order_due_month]['by_billed'][billed] = {'expected_cost': 0.0, 'expected_price': 0.0, 'actual_cost': 0.0, 'price': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'wh_billable_cost': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'estimated_work_hours': 0.0, 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_expected_cost': 0.0, 'eq_actual_cost': 0.0, 'order_codes': '', 'client_code': '0'}  
            if classification not in order_days['due_dates'][order_due_day]['by_classification'].keys():
                order_days['due_dates'][order_due_day]['by_classification'][classification] = {'expected_cost': 0.0, 'expected_price': 0.0, 'actual_cost': 0.0, 'price': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'wh_billable_cost': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'estimated_work_hours': 0.0, 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_expected_cost': 0.0, 'eq_actual_cost': 0.0, 'order_codes': '', 'client_code': '0'}  
            if classification not in order_days['month_due_dates'][order_due_month]['by_classification'].keys():
                order_days['month_due_dates'][order_due_month]['by_classification'][classification] = {'expected_cost': 0.0, 'expected_price': 0.0, 'actual_cost': 0.0, 'price': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'wh_billable_cost': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'estimated_work_hours': 0.0, 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_expected_cost': 0.0, 'eq_actual_cost': 0.0, 'order_codes': '', 'client_code': '0'}  
            if order_completion_day not in order_days['completion_dates'].keys():
                order_days['completion_dates'][order_completion_day] = {'expected_cost': 0.0, 'expected_price': 0.0, 'actual_cost': 0.0, 'price': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'wh_billable_cost': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'estimated_work_hours': 0.0, 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_expected_cost': 0.0, 'eq_actual_cost': 0.0, 'order_codes': '', 'by_billed': {}, 'client_code': '0'}  
            if billed not in order_days['completion_dates'][order_completion_day]['by_billed'].keys():
                order_days['completion_dates'][order_completion_day]['by_billed'][billed] = {'expected_cost': 0.0, 'expected_price': 0.0, 'actual_cost': 0.0, 'price': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'wh_billable_cost': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'estimated_work_hours': 0.0, 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_expected_cost': 0.0, 'eq_actual_cost': 0.0, 'order_codes': '', 'client_code': '0'}  
            if order_completion_month not in order_days['month_completion_dates'].keys():
                order_days['month_completion_dates'][order_completion_month] = {'expected_cost': 0.0, 'expected_price': 0.0, 'actual_cost': 0.0, 'price': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'wh_billable_cost': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'estimated_work_hours': 0.0, 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_expected_cost': 0.0, 'eq_actual_cost': 0.0, 'order_codes': '', 'by_billed': {}, 'client_code': '0'}  
            if billed not in order_days['month_completion_dates'][order_completion_month]['by_billed'].keys():
                order_days['month_completion_dates'][order_completion_month]['by_billed'][billed] = {'expected_cost': 0.0, 'expected_price': 0.0, 'actual_cost': 0.0, 'price': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'wh_billable_cost': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'estimated_work_hours': 0.0, 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_expected_cost': 0.0, 'eq_actual_cost': 0.0, 'order_codes': '', 'client_code': '0'}  
            if order_billed_day not in order_days['billed_dates'].keys():
                order_days['billed_dates'][order_billed_day] = {'expected_cost': 0.0, 'expected_price': 0.0, 'actual_cost': 0.0, 'price': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'wh_billable_cost': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'estimated_work_hours': 0.0, 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_expected_cost': 0.0, 'eq_actual_cost': 0.0, 'order_codes': '', 'by_billed': {}, 'client_code': '0'}  
            if billed not in order_days['billed_dates'][order_billed_day]['by_billed'].keys():
                order_days['billed_dates'][order_billed_day]['by_billed'][billed] = {'expected_cost': 0.0, 'expected_price': 0.0, 'actual_cost': 0.0, 'price': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'wh_billable_cost': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'estimated_work_hours': 0.0, 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_expected_cost': 0.0, 'eq_actual_cost': 0.0, 'order_codes': '', 'client_code': '0'}  
            if order_billed_month not in order_days['month_billed_dates'].keys():
                order_days['month_billed_dates'][order_billed_month] = {'expected_cost': 0.0, 'expected_price': 0.0, 'actual_cost': 0.0, 'price': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'wh_billable_cost': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'estimated_work_hours': 0.0, 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_expected_cost': 0.0, 'eq_actual_cost': 0.0, 'order_codes': '', 'by_billed': {}, 'client_code': '0'}  
            if billed not in order_days['month_billed_dates'][order_billed_month]['by_billed'].keys():
                order_days['month_billed_dates'][order_billed_month]['by_billed'][billed] = {'expected_cost': 0.0, 'expected_price': 0.0, 'actual_cost': 0.0, 'price': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'wh_billable_cost': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'estimated_work_hours': 0.0, 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_expected_cost': 0.0, 'eq_actual_cost': 0.0, 'order_codes': '', 'client_code': '0'}  
            if client_code not in order_clients.keys():
                order_clients[client_code] = {'expected_cost': 0.0, 'expected_price': 0.0, 'actual_cost': 0.0, 'price': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'wh_billable_cost': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'estimated_work_hours': 0.0, 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_expected_cost': 0.0, 'eq_actual_cost': 0.0, 'due_dates': {}, 'completion_dates': {}, 'order_codes': '', 'by_billed': {}, 'month_due_dates': {}, 'month_completion_dates': {}, 'billed_dates': {}, 'month_billed_dates': {}} 
            if billed not in order_clients[client_code]['by_billed'].keys():
                order_clients[client_code]['by_billed'][billed] = {'expected_cost': 0.0, 'expected_price': 0.0, 'actual_cost': 0.0, 'price': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'wh_billable_cost': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'estimated_work_hours': 0.0, 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_expected_cost': 0.0, 'eq_actual_cost': 0.0, 'due_dates': {}, 'completion_dates': {}, 'order_codes': '', 'billed_dates': {}, 'month_billed_dates': {}} 
            if order_completion_day not in order_clients[client_code]['completion_dates'].keys():
                order_clients[client_code]['completion_dates'][order_completion_day] = {'expected_cost': 0.0, 'expected_price': 0.0, 'actual_cost': 0.0, 'price': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'wh_billable_cost': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'estimated_work_hours': 0.0, 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_expected_cost': 0.0, 'eq_actual_cost': 0.0, 'order_codes': '', 'by_billed': {}}  
            if billed not in order_clients[client_code]['completion_dates'][order_completion_day]['by_billed'].keys():
                order_clients[client_code]['completion_dates'][order_completion_day]['by_billed'][billed] = {'expected_cost': 0.0, 'expected_price': 0.0, 'actual_cost': 0.0, 'price': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'wh_billable_cost': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'estimated_work_hours': 0.0, 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_expected_cost': 0.0, 'eq_actual_cost': 0.0, 'order_codes': ''}  
            if order_completion_month not in order_clients[client_code]['month_completion_dates'].keys():
                order_clients[client_code]['month_completion_dates'][order_completion_month] = {'expected_cost': 0.0, 'expected_price': 0.0, 'actual_cost': 0.0, 'price': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'wh_billable_cost': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'estimated_work_hours': 0.0, 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_expected_cost': 0.0, 'eq_actual_cost': 0.0, 'order_codes': '', 'by_billed': {}}  
            if billed not in order_clients[client_code]['month_completion_dates'][order_completion_month]['by_billed'].keys():
                order_clients[client_code]['month_completion_dates'][order_completion_month]['by_billed'][billed] = {'expected_cost': 0.0, 'expected_price': 0.0, 'actual_cost': 0.0, 'price': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'wh_billable_cost': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'estimated_work_hours': 0.0, 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_expected_cost': 0.0, 'eq_actual_cost': 0.0, 'order_codes': ''}  
            if order_billed_day not in order_clients[client_code]['billed_dates'].keys():
                order_clients[client_code]['billed_dates'][order_billed_day] = {'expected_cost': 0.0, 'expected_price': 0.0, 'actual_cost': 0.0, 'price': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'wh_billable_cost': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'estimated_work_hours': 0.0, 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_expected_cost': 0.0, 'eq_actual_cost': 0.0, 'order_codes': '', 'by_billed': {}}  
            if billed not in order_clients[client_code]['billed_dates'][order_billed_day]['by_billed'].keys():
                order_clients[client_code]['billed_dates'][order_billed_day]['by_billed'][billed] = {'expected_cost': 0.0, 'expected_price': 0.0, 'actual_cost': 0.0, 'price': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'wh_billable_cost': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'estimated_work_hours': 0.0, 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_expected_cost': 0.0, 'eq_actual_cost': 0.0, 'order_codes': ''}  
            if order_billed_month not in order_clients[client_code]['month_billed_dates'].keys():
                order_clients[client_code]['month_billed_dates'][order_billed_month] = {'expected_cost': 0.0, 'expected_price': 0.0, 'actual_cost': 0.0, 'price': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'wh_billable_cost': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'estimated_work_hours': 0.0, 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_expected_cost': 0.0, 'eq_actual_cost': 0.0, 'order_codes': '', 'by_billed': {}}  
            if billed not in order_clients[client_code]['month_billed_dates'][order_billed_month]['by_billed'].keys():
                order_clients[client_code]['month_billed_dates'][order_billed_month]['by_billed'][billed] = {'expected_cost': 0.0, 'expected_price': 0.0, 'actual_cost': 0.0, 'price': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'wh_billable_cost': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'estimated_work_hours': 0.0, 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_expected_cost': 0.0, 'eq_actual_cost': 0.0, 'order_codes': ''}  
            if order_due_day not in order_clients[client_code]['due_dates'].keys():
                order_clients[client_code]['due_dates'][order_due_day] = {'expected_cost': 0.0, 'expected_price': 0.0, 'actual_cost': 0.0, 'price': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'wh_billable_cost': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'estimated_work_hours': 0.0, 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_expected_cost': 0.0, 'eq_actual_cost': 0.0, 'order_codes': '', 'by_classification': {}, 'by_billed': {}}  
            if order_due_month not in order_clients[client_code]['month_due_dates'].keys():
                order_clients[client_code]['month_due_dates'][order_due_month] = {'expected_cost': 0.0, 'expected_price': 0.0, 'actual_cost': 0.0, 'price': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'wh_billable_cost': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'estimated_work_hours': 0.0, 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_expected_cost': 0.0, 'eq_actual_cost': 0.0, 'order_codes': '', 'by_classification': {}, 'by_billed': {}}  
            if classification not in order_clients[client_code]['due_dates'][order_due_day]['by_classification'].keys():
                order_clients[client_code]['due_dates'][order_due_day]['by_classification'][classification] =  {'expected_cost': 0.0, 'expected_price': 0.0, 'actual_cost': 0.0, 'price': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'wh_billable_cost': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'estimated_work_hours': 0.0, 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_expected_cost': 0.0, 'eq_actual_cost': 0.0, 'order_codes': ''}  
            if billed not in order_clients[client_code]['due_dates'][order_due_day]['by_billed'].keys():
                order_clients[client_code]['due_dates'][order_due_day]['by_billed'][billed] =  {'expected_cost': 0.0, 'expected_price': 0.0, 'actual_cost': 0.0, 'price': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'wh_billable_cost': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'estimated_work_hours': 0.0, 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_expected_cost': 0.0, 'eq_actual_cost': 0.0, 'order_codes': ''}  
            if classification not in order_clients[client_code]['month_due_dates'][order_due_month]['by_classification'].keys():
                order_clients[client_code]['month_due_dates'][order_due_month]['by_classification'][classification] =  {'expected_cost': 0.0, 'expected_price': 0.0, 'actual_cost': 0.0, 'price': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'wh_billable_cost': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'estimated_work_hours': 0.0, 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_expected_cost': 0.0, 'eq_actual_cost': 0.0, 'order_codes': ''}  
            if billed not in order_clients[client_code]['month_due_dates'][order_due_month]['by_billed'].keys():
                order_clients[client_code]['month_due_dates'][order_due_month]['by_billed'][billed] =  {'expected_cost': 0.0, 'expected_price': 0.0, 'actual_cost': 0.0, 'price': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'wh_billable_cost': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'estimated_work_hours': 0.0, 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_expected_cost': 0.0, 'eq_actual_cost': 0.0, 'order_codes': ''}  
            if platform not in order_platforms.keys():
                order_platforms[platform] = {'expected_cost': 0.0, 'expected_price': 0.0, 'actual_cost': 0.0, 'price': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'wh_billable_cost': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'estimated_work_hours': 0.0, 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_expected_cost': 0.0, 'eq_actual_cost': 0.0, 'due_dates': {}, 'completion_dates': {}, 'order_codes': '', 'by_billed': {}, 'month_due_dates': {}, 'month_completion_dates': {}, 'billed_dates': {}, 'month_billed_dates': {}} 
            if billed not in order_platforms[platform]['by_billed'].keys():
                order_platforms[platform]['by_billed'][billed] = {'expected_cost': 0.0, 'expected_price': 0.0, 'actual_cost': 0.0, 'price': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'wh_billable_cost': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'estimated_work_hours': 0.0, 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_expected_cost': 0.0, 'eq_actual_cost': 0.0, 'due_dates': {}, 'completion_dates': {}, 'order_codes': '', 'billed_dates': {}, 'month_billed_dates': {}} 
            if order_completion_day not in order_platforms[platform]['completion_dates'].keys():
                order_platforms[platform]['completion_dates'][order_completion_day] = {'expected_cost': 0.0, 'expected_price': 0.0, 'actual_cost': 0.0, 'price': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'wh_billable_cost': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'estimated_work_hours': 0.0, 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_expected_cost': 0.0, 'eq_actual_cost': 0.0, 'order_codes': ''}  
            if order_billed_day not in order_platforms[platform]['billed_dates'].keys():
                order_platforms[platform]['billed_dates'][order_billed_day] = {'expected_cost': 0.0, 'expected_price': 0.0, 'actual_cost': 0.0, 'price': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'wh_billable_cost': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'estimated_work_hours': 0.0, 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_expected_cost': 0.0, 'eq_actual_cost': 0.0, 'order_codes': ''}  
            if order_due_day not in order_platforms[platform]['due_dates'].keys():
                order_platforms[platform]['due_dates'][order_due_day] = {'expected_cost': 0.0, 'expected_price': 0.0, 'actual_cost': 0.0, 'price': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'wh_billable_cost': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'estimated_work_hours': 0.0, 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_expected_cost': 0.0, 'eq_actual_cost': 0.0, 'order_codes': '', 'by_classification': {}, 'by_billed': {}}  
            if classification not in order_platforms[platform]['due_dates'][order_due_day]['by_classification'].keys():
                order_platforms[platform]['due_dates'][order_due_day]['by_classification'][classification] =  {'expected_cost': 0.0, 'expected_price': 0.0, 'actual_cost': 0.0, 'price': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'wh_billable_cost': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'estimated_work_hours': 0.0, 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_expected_cost': 0.0, 'eq_actual_cost': 0.0, 'order_codes': ''}  
            if billed not in order_platforms[platform]['due_dates'][order_due_day]['by_billed'].keys():
                order_platforms[platform]['due_dates'][order_due_day]['by_billed'][billed] =  {'expected_cost': 0.0, 'expected_price': 0.0, 'actual_cost': 0.0, 'price': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'wh_billable_cost': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'estimated_work_hours': 0.0, 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_expected_cost': 0.0, 'eq_actual_cost': 0.0, 'order_codes': ''}  
            if order_completion_month not in order_platforms[platform]['month_completion_dates'].keys():
                order_platforms[platform]['month_completion_dates'][order_completion_month] = {'expected_cost': 0.0, 'expected_price': 0.0, 'actual_cost': 0.0, 'price': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'wh_billable_cost': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'estimated_work_hours': 0.0, 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_expected_cost': 0.0, 'eq_actual_cost': 0.0, 'order_codes': ''}  
            if order_billed_month not in order_platforms[platform]['month_billed_dates'].keys():
                order_platforms[platform]['month_billed_dates'][order_billed_month] = {'expected_cost': 0.0, 'expected_price': 0.0, 'actual_cost': 0.0, 'price': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'wh_billable_cost': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'estimated_work_hours': 0.0, 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_expected_cost': 0.0, 'eq_actual_cost': 0.0, 'order_codes': ''}  
            if order_due_month not in order_platforms[platform]['month_due_dates'].keys():
                order_platforms[platform]['month_due_dates'][order_due_month] = {'expected_cost': 0.0, 'expected_price': 0.0, 'actual_cost': 0.0, 'price': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'wh_billable_cost': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'estimated_work_hours': 0.0, 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_expected_cost': 0.0, 'eq_actual_cost': 0.0, 'order_codes': '', 'by_classification': {}, 'by_billed': {}}  
            if classification not in order_platforms[platform]['month_due_dates'][order_due_month]['by_classification'].keys():
                order_platforms[platform]['month_due_dates'][order_due_month]['by_classification'][classification] =  {'expected_cost': 0.0, 'expected_price': 0.0, 'actual_cost': 0.0, 'price': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'wh_billable_cost': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'estimated_work_hours': 0.0, 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_expected_cost': 0.0, 'eq_actual_cost': 0.0, 'order_codes': ''}  
            if billed not in order_platforms[platform]['month_due_dates'][order_due_month]['by_billed'].keys():
                order_platforms[platform]['month_due_dates'][order_due_month]['by_billed'][billed] =  {'expected_cost': 0.0, 'expected_price': 0.0, 'actual_cost': 0.0, 'price': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'wh_billable_cost': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'estimated_work_hours': 0.0, 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_expected_cost': 0.0, 'eq_actual_cost': 0.0, 'order_codes': ''}  
                
            order_days, sum_em_time = sum_em(order_days, order, order_top_fields, sum_em_time)
            if future:
                order_days['future'], sum_em_time = sum_em(order_days['future'], order, order_top_fields, sum_em_time)
            if late:
                order_days['late'], sum_em_time = sum_em(order_days['late'], order, order_top_fields, sum_em_time)
            order_days['due_dates'][order_due_day], sum_em_time = sum_em(order_days['due_dates'][order_due_day], order, order_top_fields, sum_em_time)
            order_days['month_due_dates'][order_due_month], sum_em_time = sum_em(order_days['month_due_dates'][order_due_month], order, order_top_fields, sum_em_time)
            order_days['completion_dates'][order_completion_day], sum_em_time = sum_em(order_days['completion_dates'][order_completion_day], order, order_top_fields, sum_em_time)
            order_days['completion_dates'][order_completion_day]['by_billed'][billed], sum_em_time = sum_em(order_days['completion_dates'][order_completion_day]['by_billed'][billed], order, order_top_fields, sum_em_time)
            order_days['month_completion_dates'][order_completion_month], sum_em_time = sum_em(order_days['month_completion_dates'][order_completion_month], order, order_top_fields, sum_em_time)
            order_days['month_completion_dates'][order_completion_month]['by_billed'][billed], sum_em_time = sum_em(order_days['month_completion_dates'][order_completion_month]['by_billed'][billed], order, order_top_fields, sum_em_time)
            order_days['billed_dates'][order_billed_day], sum_em_time = sum_em(order_days['billed_dates'][order_billed_day], order, order_top_fields, sum_em_time)
            order_days['billed_dates'][order_billed_day]['by_billed'][billed], sum_em_time = sum_em(order_days['billed_dates'][order_billed_day]['by_billed'][billed], order, order_top_fields, sum_em_time)
            order_days['month_billed_dates'][order_billed_month], sum_em_time = sum_em(order_days['month_billed_dates'][order_billed_month], order, order_top_fields, sum_em_time)
            order_days['month_billed_dates'][order_billed_month]['by_billed'][billed], sum_em_time = sum_em(order_days['month_billed_dates'][order_billed_month]['by_billed'][billed], order, order_top_fields, sum_em_time)
            order_days['by_classification'][classification], sum_em_time = sum_em(order_days['by_classification'][classification], order, order_top_fields, sum_em_time)
            order_days['by_billed'][billed], sum_em_time = sum_em(order_days['by_billed'][billed], order, order_top_fields, sum_em_time)
            order_days['due_dates'][order_due_day]['by_billed'][billed], sum_em_time = sum_em(order_days['due_dates'][order_due_day]['by_billed'][billed], order, order_top_fields, sum_em_time)
            order_days['due_dates'][order_due_day]['by_classification'][classification], sum_em_time = sum_em(order_days['due_dates'][order_due_day]['by_classification'][classification], order, order_top_fields, sum_em_time)
            order_days['month_due_dates'][order_due_month]['by_billed'][billed], sum_em_time = sum_em(order_days['month_due_dates'][order_due_month]['by_billed'][billed], order, order_top_fields, sum_em_time)
            order_days['month_due_dates'][order_due_month]['by_classification'][classification], sum_em_time = sum_em(order_days['month_due_dates'][order_due_month]['by_classification'][classification], order, order_top_fields, sum_em_time)
            order_clients[client_code], sum_em_time = sum_em(order_clients[client_code], order, order_top_fields, sum_em_time)
            order_clients[client_code]['by_billed'][billed], sum_em_time = sum_em(order_clients[client_code]['by_billed'][billed], order, order_top_fields, sum_em_time)
            order_clients[client_code]['completion_dates'][order_completion_day], sum_em_time = sum_em(order_clients[client_code]['completion_dates'][order_completion_day], order, order_top_fields, sum_em_time)
            order_clients[client_code]['completion_dates'][order_completion_day]['by_billed'][billed], sum_em_time = sum_em(order_clients[client_code]['completion_dates'][order_completion_day]['by_billed'][billed], order, order_top_fields, sum_em_time)
            order_clients[client_code]['month_completion_dates'][order_completion_month], sum_em_time = sum_em(order_clients[client_code]['month_completion_dates'][order_completion_month], order, order_top_fields, sum_em_time)
            order_clients[client_code]['month_completion_dates'][order_completion_month]['by_billed'][billed], sum_em_time = sum_em(order_clients[client_code]['month_completion_dates'][order_completion_month]['by_billed'][billed], order, order_top_fields, sum_em_time)
            order_clients[client_code]['billed_dates'][order_billed_day], sum_em_time = sum_em(order_clients[client_code]['billed_dates'][order_billed_day], order, order_top_fields, sum_em_time)
            order_clients[client_code]['billed_dates'][order_billed_day]['by_billed'][billed], sum_em_time = sum_em(order_clients[client_code]['billed_dates'][order_billed_day]['by_billed'][billed], order, order_top_fields, sum_em_time)
            order_clients[client_code]['month_billed_dates'][order_billed_month], sum_em_time = sum_em(order_clients[client_code]['month_billed_dates'][order_billed_month], order, order_top_fields, sum_em_time)
            order_clients[client_code]['month_billed_dates'][order_billed_month]['by_billed'][billed], sum_em_time = sum_em(order_clients[client_code]['month_billed_dates'][order_billed_month]['by_billed'][billed], order, order_top_fields, sum_em_time)
            order_clients[client_code]['due_dates'][order_due_day], sum_em_time = sum_em(order_clients[client_code]['due_dates'][order_due_day], order, order_top_fields, sum_em_time)
            order_clients[client_code]['due_dates'][order_due_day]['by_classification'][classification], sum_em_time = sum_em(order_clients[client_code]['due_dates'][order_due_day]['by_classification'][classification], order, order_top_fields, sum_em_time)
            order_clients[client_code]['due_dates'][order_due_day]['by_billed'][billed], sum_em_time = sum_em(order_clients[client_code]['due_dates'][order_due_day]['by_billed'][billed], order, order_top_fields, sum_em_time)
            order_clients[client_code]['month_due_dates'][order_due_month], sum_em_time = sum_em(order_clients[client_code]['month_due_dates'][order_due_month], order, order_top_fields, sum_em_time)
            order_clients[client_code]['month_due_dates'][order_due_month]['by_classification'][classification], sum_em_time = sum_em(order_clients[client_code]['month_due_dates'][order_due_month]['by_classification'][classification], order, order_top_fields, sum_em_time)
            order_clients[client_code]['month_due_dates'][order_due_month]['by_billed'][billed], sum_em_time = sum_em(order_clients[client_code]['month_due_dates'][order_due_month]['by_billed'][billed], order, order_top_fields, sum_em_time)
            order_platforms[platform], sum_em_time = sum_em(order_platforms[platform], order, order_top_fields, sum_em_time)
            order_platforms[platform]['by_billed'][billed], sum_em_time = sum_em(order_platforms[platform]['by_billed'][billed], order, order_top_fields, sum_em_time)
            order_platforms[platform]['completion_dates'][order_completion_day], sum_em_time = sum_em(order_platforms[platform]['completion_dates'][order_completion_day], order, order_top_fields, sum_em_time)
            order_platforms[platform]['month_completion_dates'][order_completion_month], sum_em_time = sum_em(order_platforms[platform]['month_completion_dates'][order_completion_month], order, order_top_fields, sum_em_time)
            order_platforms[platform]['billed_dates'][order_billed_day], sum_em_time = sum_em(order_platforms[platform]['billed_dates'][order_billed_day], order, order_top_fields, sum_em_time)
            order_platforms[platform]['month_billed_dates'][order_billed_month], sum_em_time = sum_em(order_platforms[platform]['month_billed_dates'][order_billed_month], order, order_top_fields, sum_em_time)
            order_platforms[platform]['due_dates'][order_due_day], sum_em_time = sum_em(order_platforms[platform]['due_dates'][order_due_day], order, order_top_fields, sum_em_time)
            order_platforms[platform]['due_dates'][order_due_day]['by_classification'][classification], sum_em_time = sum_em(order_platforms[platform]['due_dates'][order_due_day]['by_classification'][classification], order, order_top_fields, sum_em_time)
            order_platforms[platform]['due_dates'][order_due_day]['by_billed'][billed], sum_em_time = sum_em(order_platforms[platform]['due_dates'][order_due_day]['by_billed'][billed], order, order_top_fields, sum_em_time)
            order_platforms[platform]['month_due_dates'][order_due_month], sum_em_time = sum_em(order_platforms[platform]['month_due_dates'][order_due_month], order, order_top_fields, sum_em_time)
            order_platforms[platform]['month_due_dates'][order_due_month]['by_classification'][classification], sum_em_time = sum_em(order_platforms[platform]['month_due_dates'][order_due_month]['by_classification'][classification], order, order_top_fields, sum_em_time)
            order_platforms[platform]['month_due_dates'][order_due_month]['by_billed'][billed], sum_em_time = sum_em(order_platforms[platform]['month_due_dates'][order_due_month]['by_billed'][billed], order, order_top_fields, sum_em_time)
            ts = []
            try:
                ts = titles[order_code]
            except:
                pass
            for title in ts:
                title_code = title['code'] 
                title_due_day = title['due_date'].split(' ')[0]
                title_due_diff = int(get_day_span(current_day, title_due_day)) 
                title_status = title['status']
                title_completion_day = title['completion_date'].split(' ')[0] 
                title_late = False
                if yesterday == title_completion_day:
                    title_completed_yesterday.append('%s:%s' % (order_code, title_code))
                    
                if title_due_day in [None,'']:
                    titles_no_due.append('%s:%s' % (order_code, title_code))
                if title_due_diff < 0 and (title_status not in ['Completed','Invoiced'] and title_completion_day in [None,'']):
                    titles_late.append('%s:%s' % (order_code, title_code))
                    title_late = True
                elif title_due_diff == 0 and (title_status not in ['Completed','Invoiced'] and title_completion_day in [None,'']):
                    titles_due.append('%s:%s' % (order_code, title_code))
                elif title_due_diff > 0 and (title_status not in ['Completed','Invoiced'] and title_completion_day in [None,'']):
                    if title_due_day not in future_titles.keys():
                        future_titles[title_due_day] = []
                    future_titles[title_due_day].append('%s:%s' % (order_code, title_code))
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
                        wo_id = id_only(work_order_code)
                        estimated_work_hours = make_number(work_order['estimated_work_hours'])
                        eqs = []
                        #Eq Stuff

                        try:
                           eqs = equipment[work_order_code]
                        except:
                            pass
                        eq_sum_dict = {'actual_duration': 0.0, 'expected_duration': 0.0, 'actual_cost': 0.0, 'expected_cost': 0.0}
                        for eq in eqs:
                            eq_code = eq['code']
                            actual_duration = make_number(eq['actual_duration'])
                            expected_duration = make_number(eq['expected_duration'])
                            actual_cost = make_number(eq['actual_cost'])
                            expected_cost = make_number(eq['expected_cost'])
                            eq_send_dict = {'actual_duration': actual_duration, 'expected_duration': expected_duration, 'actual_cost': actual_cost, 'expected_cost': expected_cost}
                            order_days, sum_em_eqs_time = sum_em_eqs(order_days, eq_send_dict,sum_em_eqs_time)
                            if future:
                                order_days['future'], sum_em_eqs_time = sum_em_eqs(order_days['future'], eq_send_dict,sum_em_eqs_time)
                            if late:
                                order_days['late'], sum_em_eqs_time = sum_em_eqs(order_days['late'], eq_send_dict,sum_em_eqs_time)
                            order_days['due_dates'][order_due_day], sum_em_eqs_time = sum_em_eqs(order_days['due_dates'][order_due_day], eq_send_dict,sum_em_eqs_time)
                            order_days['completion_dates'][order_completion_day], sum_em_eqs_time = sum_em_eqs(order_days['completion_dates'][order_completion_day], eq_send_dict,sum_em_eqs_time)
                            order_days['completion_dates'][order_completion_day]['by_billed'][billed], sum_em_eqs_time = sum_em_eqs(order_days['completion_dates'][order_completion_day]['by_billed'][billed], eq_send_dict,sum_em_eqs_time)
                            order_days['billed_dates'][order_billed_day], sum_em_eqs_time = sum_em_eqs(order_days['billed_dates'][order_billed_day], eq_send_dict,sum_em_eqs_time)
                            order_days['billed_dates'][order_billed_day]['by_billed'][billed], sum_em_eqs_time = sum_em_eqs(order_days['billed_dates'][order_billed_day]['by_billed'][billed], eq_send_dict,sum_em_eqs_time)
                            order_days['month_due_dates'][order_due_month], sum_em_eqs_time = sum_em_eqs(order_days['month_due_dates'][order_due_month], eq_send_dict,sum_em_eqs_time)
                            order_days['month_completion_dates'][order_completion_month], sum_em_eqs_time = sum_em_eqs(order_days['month_completion_dates'][order_completion_month], eq_send_dict,sum_em_eqs_time)
                            order_days['month_completion_dates'][order_completion_month]['by_billed'][billed], sum_em_eqs_time = sum_em_eqs(order_days['month_completion_dates'][order_completion_month]['by_billed'][billed], eq_send_dict,sum_em_eqs_time)
                            order_days['month_billed_dates'][order_billed_month], sum_em_eqs_time = sum_em_eqs(order_days['month_billed_dates'][order_billed_month], eq_send_dict,sum_em_eqs_time)
                            order_days['month_billed_dates'][order_billed_month]['by_billed'][billed], sum_em_eqs_time = sum_em_eqs(order_days['month_billed_dates'][order_billed_month]['by_billed'][billed], eq_send_dict,sum_em_eqs_time)
                            order_days['by_classification'][classification], sum_em_eqs_time = sum_em_eqs(order_days['by_classification'][classification], eq_send_dict,sum_em_eqs_time)
                            order_days['by_billed'][billed], sum_em_eqs_time = sum_em_eqs(order_days['by_billed'][billed], eq_send_dict,sum_em_eqs_time)
                            order_days['due_dates'][order_due_day]['by_billed'][billed], sum_em_eqs_time = sum_em_eqs(order_days['due_dates'][order_due_day]['by_billed'][billed], eq_send_dict,sum_em_eqs_time)
                            order_days['due_dates'][order_due_day]['by_classification'][classification], sum_em_eqs_time = sum_em_eqs(order_days['due_dates'][order_due_day]['by_classification'][classification], eq_send_dict,sum_em_eqs_time)
                            order_days['month_due_dates'][order_due_month]['by_billed'][billed], sum_em_eqs_time = sum_em_eqs(order_days['month_due_dates'][order_due_month]['by_billed'][billed], eq_send_dict,sum_em_eqs_time)
                            order_days['month_due_dates'][order_due_month]['by_classification'][classification], sum_em_eqs_time = sum_em_eqs(order_days['month_due_dates'][order_due_month]['by_classification'][classification], eq_send_dict,sum_em_eqs_time)
                            order_clients[client_code], sum_em_eqs_time = sum_em_eqs(order_clients[client_code], eq_send_dict, sum_em_eqs_time)
                            order_clients[client_code]['by_billed'][billed], sum_em_eqs_time = sum_em_eqs(order_clients[client_code]['by_billed'][billed], eq_send_dict, sum_em_eqs_time)
                            order_clients[client_code]['completion_dates'][order_completion_day], sum_em_eqs_time = sum_em_eqs(order_clients[client_code]['completion_dates'][order_completion_day], eq_send_dict, sum_em_eqs_time)
                            order_clients[client_code]['completion_dates'][order_completion_day]['by_billed'][billed], sum_em_eqs_time = sum_em_eqs(order_clients[client_code]['completion_dates'][order_completion_day]['by_billed'][billed], eq_send_dict, sum_em_eqs_time)
                            order_clients[client_code]['billed_dates'][order_billed_day], sum_em_eqs_time = sum_em_eqs(order_clients[client_code]['billed_dates'][order_billed_day], eq_send_dict, sum_em_eqs_time)
                            order_clients[client_code]['billed_dates'][order_billed_day]['by_billed'][billed], sum_em_eqs_time = sum_em_eqs(order_clients[client_code]['billed_dates'][order_billed_day]['by_billed'][billed], eq_send_dict, sum_em_eqs_time)
                            order_clients[client_code]['due_dates'][order_due_day], sum_em_eqs_time = sum_em_eqs(order_clients[client_code]['due_dates'][order_due_day], eq_send_dict, sum_em_eqs_time)
                            order_clients[client_code]['due_dates'][order_due_day]['by_classification'][classification], sum_em_eqs_time = sum_em_eqs(order_clients[client_code]['due_dates'][order_due_day]['by_classification'][classification], eq_send_dict, sum_em_eqs_time)
                            order_clients[client_code]['due_dates'][order_due_day]['by_billed'][billed], sum_em_eqs_time = sum_em_eqs(order_clients[client_code]['due_dates'][order_due_day]['by_billed'][billed], eq_send_dict, sum_em_eqs_time)
                            order_clients[client_code]['month_completion_dates'][order_completion_month], sum_em_eqs_time = sum_em_eqs(order_clients[client_code]['month_completion_dates'][order_completion_month], eq_send_dict, sum_em_eqs_time)
                            order_clients[client_code]['month_completion_dates'][order_completion_month]['by_billed'][billed], sum_em_eqs_time = sum_em_eqs(order_clients[client_code]['month_completion_dates'][order_completion_month]['by_billed'][billed], eq_send_dict, sum_em_eqs_time)
                            order_clients[client_code]['month_billed_dates'][order_billed_month], sum_em_eqs_time = sum_em_eqs(order_clients[client_code]['month_billed_dates'][order_billed_month], eq_send_dict, sum_em_eqs_time)
                            order_clients[client_code]['month_billed_dates'][order_billed_month]['by_billed'][billed], sum_em_eqs_time = sum_em_eqs(order_clients[client_code]['month_billed_dates'][order_billed_month]['by_billed'][billed], eq_send_dict, sum_em_eqs_time)
                            order_clients[client_code]['month_due_dates'][order_due_month], sum_em_eqs_time = sum_em_eqs(order_clients[client_code]['month_due_dates'][order_due_month], eq_send_dict, sum_em_eqs_time)
                            order_clients[client_code]['month_due_dates'][order_due_month]['by_classification'][classification], sum_em_eqs_time = sum_em_eqs(order_clients[client_code]['month_due_dates'][order_due_month]['by_classification'][classification], eq_send_dict, sum_em_eqs_time)
                            order_clients[client_code]['month_due_dates'][order_due_month]['by_billed'][billed], sum_em_eqs_time = sum_em_eqs(order_clients[client_code]['month_due_dates'][order_due_month]['by_billed'][billed], eq_send_dict, sum_em_eqs_time)
                            order_platforms[platform], sum_em_eqs_time = sum_em_eqs(order_platforms[platform], eq_send_dict, sum_em_eqs_time)
                            order_platforms[platform]['by_billed'][billed], sum_em_eqs_time = sum_em_eqs(order_platforms[platform]['by_billed'][billed], eq_send_dict, sum_em_eqs_time)
                            order_platforms[platform]['completion_dates'][order_completion_day], sum_em_eqs_time = sum_em_eqs(order_platforms[platform]['completion_dates'][order_completion_day], eq_send_dict, sum_em_eqs_time)
                            order_platforms[platform]['month_completion_dates'][order_completion_month], sum_em_eqs_time = sum_em_eqs(order_platforms[platform]['month_completion_dates'][order_completion_month], eq_send_dict, sum_em_eqs_time)
                            order_platforms[platform]['billed_dates'][order_billed_day], sum_em_eqs_time = sum_em_eqs(order_platforms[platform]['billed_dates'][order_billed_day], eq_send_dict, sum_em_eqs_time)
                            order_platforms[platform]['month_billed_dates'][order_billed_month], sum_em_eqs_time = sum_em_eqs(order_platforms[platform]['month_billed_dates'][order_billed_month], eq_send_dict, sum_em_eqs_time)
                            order_platforms[platform]['due_dates'][order_due_day], sum_em_eqs_time = sum_em_eqs(order_platforms[platform]['due_dates'][order_due_day], eq_send_dict, sum_em_eqs_time)
                            order_platforms[platform]['due_dates'][order_due_day]['by_classification'][classification], sum_em_eqs_time = sum_em_eqs(order_platforms[platform]['due_dates'][order_due_day]['by_classification'][classification], eq_send_dict, sum_em_eqs_time)
                            order_platforms[platform]['due_dates'][order_due_day]['by_billed'][billed], sum_em_eqs_time = sum_em_eqs(order_platforms[platform]['due_dates'][order_due_day]['by_billed'][billed], eq_send_dict, sum_em_eqs_time)
                            order_platforms[platform]['month_due_dates'][order_due_month], sum_em_eqs_time = sum_em_eqs(order_platforms[platform]['month_due_dates'][order_due_month], eq_send_dict, sum_em_eqs_time)
                            order_platforms[platform]['month_due_dates'][order_due_month]['by_classification'][classification], sum_em_eqs_time = sum_em_eqs(order_platforms[platform]['month_due_dates'][order_due_month]['by_classification'][classification], eq_send_dict, sum_em_eqs_time)
                            order_platforms[platform]['month_due_dates'][order_due_month]['by_billed'][billed], sum_em_eqs_time = sum_em_eqs(order_platforms[platform]['month_due_dates'][order_due_month]['by_billed'][billed], eq_send_dict, sum_em_eqs_time)
                            eq_sum_dict['actual_duration'] = eq_sum_dict['actual_duration'] + actual_duration
                            eq_sum_dict['expected_duration'] = eq_sum_dict['expected_duration'] + expected_duration
                            eq_sum_dict['actual_cost'] = eq_sum_dict['actual_cost'] + actual_cost
                            eq_sum_dict['expected_cost'] = eq_sum_dict['expected_cost'] + expected_cost
                        #Task Stuff
                        tsks = []
                        try:
                            tsks = tasks[work_order_code]
                        except:
                            pass
                        t_count = 0
                        for task in tsks:
                            task_code = task['code']
                            task_assigned = task['assigned']
                            assigned_login_group = task['assigned_login_group']
                            if assigned_login_group in [None,'']:
                                if task_assigned in login_codes:
                                    assigned_login_group = login_report[task_assigned]['default_group']
                            task_status = task['status']
                            task_platform = task['platform']
                            if task_platform in [None,'']:
                                task_platform = platform
                            task_due_day = task['bid_end_date'].split(' ')[0]
                            task_completion_day = task['actual_end_date']
                            task_completion_day = task_completion_day.split(' ')[0]
                            task_completion_diff = int(get_day_span(current_day, task_completion_day)) 
                            if task_completion_day in [None,'']:
                                task_completion_day = '1999-01-01'
                            tcds = task_completion_day.split('-')
                            task_completion_month = '%s-%s' % (tcds[0], tcds[1])
                            task_due_diff = int(get_day_span(current_day, task_due_day))  
                            if task_due_day in [None,'']:
                                task_due_day = title_due_day
                            if task_due_day in [None,'']:
                                tasks_no_due.append(wo_id)
                                task_due_day = '1999-01-01'
                            tdms = task_due_day.split('-')
                            task_due_month = '%s-%s' % (tdms[0], tdms[1])
                            if task_status != 'Completed':
                                if task_due_diff <= 0: 
                                    tasks_late.append(wo_id)
                                else:
                                    if task_due_day not in future_tasks.keys():
                                        future_tasks[task_due_day] = []
                                    future_tasks[task_due_day].append(wo_id)
    
                            if task_status not in task_day['by_status'].keys():
                                task_day['by_status'][task_status] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0}
                            task_day['by_status'][task_status]['all'].append(wo_id)
    
                            if task_due_day not in task_day['due_dates'].keys():
                                task_day['due_dates'][task_due_day] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0, 'clients': {}, 'platforms': {}, 'by_status': {}, 'groups': {}}
                            task_day['due_dates'][task_due_day]['all'].append(wo_id)

                            if task_due_month not in task_day['month_due_dates'].keys():
                                task_day['month_due_dates'][task_due_month] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0, 'clients': {}, 'platforms': {}, 'by_status': {}, 'groups': {}}
                            task_day['month_due_dates'][task_due_month]['all'].append(wo_id)
    
                            if task_platform not in task_day['due_dates'][task_due_day]['platforms'].keys():
                                task_day['due_dates'][task_due_day]['platforms'][task_platform] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0}
                            task_day['due_dates'][task_due_day]['platforms'][task_platform]['all'].append(wo_id)

                            if task_platform not in task_day['month_due_dates'][task_due_month]['platforms'].keys():
                                task_day['month_due_dates'][task_due_month]['platforms'][task_platform] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0}
                            task_day['month_due_dates'][task_due_month]['platforms'][task_platform]['all'].append(wo_id)
    
                            if client_code not in task_day['due_dates'][task_due_day]['clients'].keys():
                                task_day['due_dates'][task_due_day]['clients'][client_code] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0, 'groups': {}, 'platforms': {}}
                            task_day['due_dates'][task_due_day]['clients'][client_code]['all'].append(wo_id)

                            if client_code not in task_day['month_due_dates'][task_due_month]['clients'].keys():
                                task_day['month_due_dates'][task_due_month]['clients'][client_code] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0, 'groups': {}, 'platforms': {}}
                            task_day['month_due_dates'][task_due_month]['clients'][client_code]['all'].append(wo_id)
    
                            if assigned_login_group not in task_day['due_dates'][task_due_day]['clients'][client_code]['groups'].keys():
                                task_day['due_dates'][task_due_day]['clients'][client_code]['groups'][assigned_login_group] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0}
                            task_day['due_dates'][task_due_day]['clients'][client_code]['groups'][assigned_login_group]['all'].append(wo_id)

                            if assigned_login_group not in task_day['month_due_dates'][task_due_month]['clients'][client_code]['groups'].keys():
                                task_day['month_due_dates'][task_due_month]['clients'][client_code]['groups'][assigned_login_group] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0}
                            task_day['month_due_dates'][task_due_month]['clients'][client_code]['groups'][assigned_login_group]['all'].append(wo_id)
    
                            if task_platform not in task_day['due_dates'][task_due_day]['clients'][client_code]['platforms'].keys():
                                task_day['due_dates'][task_due_day]['clients'][client_code]['platforms'][task_platform] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0}
                            task_day['due_dates'][task_due_day]['clients'][client_code]['platforms'][task_platform]['all'].append(wo_id)

                            if task_platform not in task_day['month_due_dates'][task_due_month]['clients'][client_code]['platforms'].keys():
                                task_day['month_due_dates'][task_due_month]['clients'][client_code]['platforms'][task_platform] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0}
                            task_day['month_due_dates'][task_due_month]['clients'][client_code]['platforms'][task_platform]['all'].append(wo_id)
    
                            if task_status not in task_day['due_dates'][task_due_day]['by_status'].keys():
                                task_day['due_dates'][task_due_day]['by_status'][task_status] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0}
                            task_day['due_dates'][task_due_day]['by_status'][task_status]['all'].append(wo_id)

                            if task_status not in task_day['month_due_dates'][task_due_month]['by_status'].keys():
                                task_day['month_due_dates'][task_due_month]['by_status'][task_status] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0}
                            task_day['month_due_dates'][task_due_month]['by_status'][task_status]['all'].append(wo_id)
    
                            if assigned_login_group not in task_day['due_dates'][task_due_day]['groups'].keys():
                                task_day['due_dates'][task_due_day]['groups'][assigned_login_group] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0, 'by_status': {}}
                            task_day['due_dates'][task_due_day]['groups'][assigned_login_group]['all'].append(wo_id)

                            if assigned_login_group not in task_day['month_due_dates'][task_due_month]['groups'].keys():
                                task_day['month_due_dates'][task_due_month]['groups'][assigned_login_group] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0, 'by_status': {}}
                            task_day['month_due_dates'][task_due_month]['groups'][assigned_login_group]['all'].append(wo_id)
    
                            if task_status not in task_day['due_dates'][task_due_day]['groups'][assigned_login_group]['by_status'].keys():
                                task_day['due_dates'][task_due_day]['groups'][assigned_login_group]['by_status'][task_status] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0}
                            task_day['due_dates'][task_due_day]['groups'][assigned_login_group]['by_status'][task_status]['all'].append(wo_id)

                            if task_status not in task_day['month_due_dates'][task_due_month]['groups'][assigned_login_group]['by_status'].keys():
                                task_day['month_due_dates'][task_due_month]['groups'][assigned_login_group]['by_status'][task_status] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0}
                            task_day['month_due_dates'][task_due_month]['groups'][assigned_login_group]['by_status'][task_status]['all'].append(wo_id)
     
                            if client_code not in task_day['clients'].keys():
                                task_day['clients'][client_code] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0, 'completion_dates': {}, 'due_dates': {}, 'month_due_dates': {}, 'month_completion_dates': {}}
                            task_day['clients'][client_code]['all'].append(wo_id)
    
                            if task_due_day not in task_day['clients'][client_code]['due_dates'].keys():
                                task_day['clients'][client_code]['due_dates'][task_due_day] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0, 'by_status': {}, 'groups': {}}
                            task_day['clients'][client_code]['due_dates'][task_due_day]['all'].append(wo_id)

                            if task_due_month not in task_day['clients'][client_code]['month_due_dates'].keys():
                                task_day['clients'][client_code]['month_due_dates'][task_due_month] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0, 'by_status': {}, 'groups': {}}
                            task_day['clients'][client_code]['month_due_dates'][task_due_month]['all'].append(wo_id)

                            if task_completion_day not in task_day['clients'][client_code]['completion_dates'].keys():
                                task_day['clients'][client_code]['completion_dates'][task_completion_day] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0, 'by_status': {}, 'groups': {}}
                            task_day['clients'][client_code]['completion_dates'][task_completion_day]['all'].append(wo_id)

                            if task_completion_month not in task_day['clients'][client_code]['month_completion_dates'].keys():
                                task_day['clients'][client_code]['month_completion_dates'][task_completion_month] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0, 'by_status': {}, 'groups': {}}
                            task_day['clients'][client_code]['month_completion_dates'][task_completion_month]['all'].append(wo_id)

                            if task_status not in task_day['clients'][client_code]['due_dates'][task_due_day]['by_status'].keys(): 
                                task_day['clients'][client_code]['due_dates'][task_due_day]['by_status'][task_status] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0}
                            task_day['clients'][client_code]['due_dates'][task_due_day]['by_status'][task_status]['all'].append(wo_id)
    
                            if assigned_login_group not in task_day['clients'][client_code]['due_dates'][task_due_day]['groups'].keys():
                                task_day['clients'][client_code]['due_dates'][task_due_day]['groups'][assigned_login_group] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0, 'by_status': {}}
                            task_day['clients'][client_code]['due_dates'][task_due_day]['groups'][assigned_login_group]['all'].append(wo_id)
    
                            if task_status not in task_day['clients'][client_code]['due_dates'][task_due_day]['groups'][assigned_login_group]['by_status'].keys():
                                task_day['clients'][client_code]['due_dates'][task_due_day]['groups'][assigned_login_group]['by_status'][task_status] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0}
                            task_day['clients'][client_code]['due_dates'][task_due_day]['groups'][assigned_login_group]['by_status'][task_status]['all'].append(wo_id)

                            if task_status not in task_day['clients'][client_code]['completion_dates'][task_completion_day]['by_status'].keys(): 
                                task_day['clients'][client_code]['completion_dates'][task_completion_day]['by_status'][task_status] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0}
                            task_day['clients'][client_code]['completion_dates'][task_completion_day]['by_status'][task_status]['all'].append(wo_id)
    
                            if assigned_login_group not in task_day['clients'][client_code]['completion_dates'][task_completion_day]['groups'].keys():
                                task_day['clients'][client_code]['completion_dates'][task_completion_day]['groups'][assigned_login_group] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0, 'by_status': {}}
                            task_day['clients'][client_code]['completion_dates'][task_completion_day]['groups'][assigned_login_group]['all'].append(wo_id)
    
                            if task_status not in task_day['clients'][client_code]['completion_dates'][task_completion_day]['groups'][assigned_login_group]['by_status'].keys():
                                task_day['clients'][client_code]['completion_dates'][task_completion_day]['groups'][assigned_login_group]['by_status'][task_status] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0}
                            task_day['clients'][client_code]['completion_dates'][task_completion_day]['groups'][assigned_login_group]['by_status'][task_status]['all'].append(wo_id)
    



                            if task_status not in task_day['clients'][client_code]['month_due_dates'][task_due_month]['by_status'].keys(): 
                                task_day['clients'][client_code]['month_due_dates'][task_due_month]['by_status'][task_status] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0}
                            task_day['clients'][client_code]['month_due_dates'][task_due_month]['by_status'][task_status]['all'].append(wo_id)
    
                            if assigned_login_group not in task_day['clients'][client_code]['month_due_dates'][task_due_month]['groups'].keys():
                                task_day['clients'][client_code]['month_due_dates'][task_due_month]['groups'][assigned_login_group] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0, 'by_status': {}}
                            task_day['clients'][client_code]['month_due_dates'][task_due_month]['groups'][assigned_login_group]['all'].append(wo_id)
    
                            if task_status not in task_day['clients'][client_code]['month_due_dates'][task_due_month]['groups'][assigned_login_group]['by_status'].keys():
                                task_day['clients'][client_code]['month_due_dates'][task_due_month]['groups'][assigned_login_group]['by_status'][task_status] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0}
                            task_day['clients'][client_code]['month_due_dates'][task_due_month]['groups'][assigned_login_group]['by_status'][task_status]['all'].append(wo_id)

                            if task_status not in task_day['clients'][client_code]['month_completion_dates'][task_completion_month]['by_status'].keys(): 
                                task_day['clients'][client_code]['month_completion_dates'][task_completion_month]['by_status'][task_status] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0}
                            task_day['clients'][client_code]['month_completion_dates'][task_completion_month]['by_status'][task_status]['all'].append(wo_id)
    
                            if assigned_login_group not in task_day['clients'][client_code]['month_completion_dates'][task_completion_month]['groups'].keys():
                                task_day['clients'][client_code]['month_completion_dates'][task_completion_month]['groups'][assigned_login_group] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0, 'by_status': {}}
                            task_day['clients'][client_code]['month_completion_dates'][task_completion_month]['groups'][assigned_login_group]['all'].append(wo_id)
    
                            if task_status not in task_day['clients'][client_code]['month_completion_dates'][task_completion_month]['groups'][assigned_login_group]['by_status'].keys():
                                task_day['clients'][client_code]['month_completion_dates'][task_completion_month]['groups'][assigned_login_group]['by_status'][task_status] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0}
                            task_day['clients'][client_code]['month_completion_dates'][task_completion_month]['groups'][assigned_login_group]['by_status'][task_status]['all'].append(wo_id)

                            if task_platform not in task_day['platforms'].keys():
                                task_day['platforms'][task_platform] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0, 'due_dates': {}, 'month_due_dates': {}}
                            task_day['platforms'][task_platform]['all'].append(wo_id)
    
                            if task_due_day not in task_day['platforms'][task_platform]['due_dates'].keys():
                                task_day['platforms'][task_platform]['due_dates'][task_due_day] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0, 'by_status': {}, 'groups': {}}
                            task_day['platforms'][task_platform]['due_dates'][task_due_day]['all'].append(wo_id)
    
                            if task_status not in task_day['platforms'][task_platform]['due_dates'][task_due_day]['by_status'].keys(): 
                                task_day['platforms'][task_platform]['due_dates'][task_due_day]['by_status'][task_status] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0}
                            task_day['platforms'][task_platform]['due_dates'][task_due_day]['by_status'][task_status]['all'].append(wo_id)
    
                            if assigned_login_group not in task_day['platforms'][task_platform]['due_dates'][task_due_day]['groups'].keys():
                                task_day['platforms'][task_platform]['due_dates'][task_due_day]['groups'][assigned_login_group] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0, 'by_status': {}}
                            task_day['platforms'][task_platform]['due_dates'][task_due_day]['groups'][assigned_login_group]['all'].append(wo_id)
    
                            if task_status not in task_day['platforms'][task_platform]['due_dates'][task_due_day]['groups'][assigned_login_group]['by_status'].keys():
                                task_day['platforms'][task_platform]['due_dates'][task_due_day]['groups'][assigned_login_group]['by_status'][task_status] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0}
                            task_day['platforms'][task_platform]['due_dates'][task_due_day]['groups'][assigned_login_group]['by_status'][task_status]['all'].append(wo_id)

                            if task_due_month not in task_day['platforms'][task_platform]['month_due_dates'].keys():
                                task_day['platforms'][task_platform]['month_due_dates'][task_due_month] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0, 'by_status': {}, 'groups': {}}
                            task_day['platforms'][task_platform]['month_due_dates'][task_due_month]['all'].append(wo_id)
    
                            if task_status not in task_day['platforms'][task_platform]['month_due_dates'][task_due_month]['by_status'].keys(): 
                                task_day['platforms'][task_platform]['month_due_dates'][task_due_month]['by_status'][task_status] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0}
                            task_day['platforms'][task_platform]['month_due_dates'][task_due_month]['by_status'][task_status]['all'].append(wo_id)
    
                            if assigned_login_group not in task_day['platforms'][task_platform]['month_due_dates'][task_due_month]['groups'].keys():
                                task_day['platforms'][task_platform]['month_due_dates'][task_due_month]['groups'][assigned_login_group] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0, 'by_status': {}}
                            task_day['platforms'][task_platform]['month_due_dates'][task_due_month]['groups'][assigned_login_group]['all'].append(wo_id)
    
                            if task_status not in task_day['platforms'][task_platform]['month_due_dates'][task_due_month]['groups'][assigned_login_group]['by_status'].keys():
                                task_day['platforms'][task_platform]['month_due_dates'][task_due_month]['groups'][assigned_login_group]['by_status'][task_status] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0}
                            task_day['platforms'][task_platform]['month_due_dates'][task_due_month]['groups'][assigned_login_group]['by_status'][task_status]['all'].append(wo_id)
                            
                            task_day['by_status'][task_status], sum_em_eqs_time = sum_em_eqs(task_day['by_status'][task_status], eq_sum_dict, sum_em_eqs_time)
                            task_day['due_dates'][task_due_day], sum_em_eqs_time = sum_em_eqs(task_day['due_dates'][task_due_day], eq_sum_dict, sum_em_eqs_time)
                            task_day['due_dates'][task_due_day]['platforms'][task_platform], sum_em_eqs_time = sum_em_eqs(task_day['due_dates'][task_due_day]['platforms'][task_platform], eq_sum_dict, sum_em_eqs_time)
                            task_day['due_dates'][task_due_day]['clients'][client_code], sum_em_eqs_time = sum_em_eqs(task_day['due_dates'][task_due_day]['clients'][client_code], eq_sum_dict, sum_em_eqs_time)
                            task_day['due_dates'][task_due_day]['clients'][client_code]['groups'][assigned_login_group], sum_em_eqs_time = sum_em_eqs(task_day['due_dates'][task_due_day]['clients'][client_code]['groups'][assigned_login_group], eq_sum_dict, sum_em_eqs_time)
                            task_day['due_dates'][task_due_day]['clients'][client_code]['platforms'][task_platform], sum_em_eqs_time = sum_em_eqs(task_day['due_dates'][task_due_day]['clients'][client_code]['platforms'][task_platform], eq_sum_dict, sum_em_eqs_time)
                            task_day['due_dates'][task_due_day]['by_status'][task_status], sum_em_eqs_time = sum_em_eqs(task_day['due_dates'][task_due_day]['by_status'][task_status], eq_sum_dict, sum_em_eqs_time)
                            task_day['due_dates'][task_due_day]['groups'][assigned_login_group], sum_em_eqs_time = sum_em_eqs(task_day['due_dates'][task_due_day]['groups'][assigned_login_group], eq_sum_dict, sum_em_eqs_time)
                            task_day['due_dates'][task_due_day]['groups'][assigned_login_group]['by_status'][task_status], sum_em_eqs_time = sum_em_eqs(task_day['due_dates'][task_due_day]['groups'][assigned_login_group]['by_status'][task_status], eq_sum_dict, sum_em_eqs_time)
                            task_day['month_due_dates'][task_due_month], sum_em_eqs_time = sum_em_eqs(task_day['month_due_dates'][task_due_month], eq_sum_dict, sum_em_eqs_time)
                            task_day['month_due_dates'][task_due_month]['platforms'][task_platform], sum_em_eqs_time = sum_em_eqs(task_day['month_due_dates'][task_due_month]['platforms'][task_platform], eq_sum_dict, sum_em_eqs_time)
                            task_day['month_due_dates'][task_due_month]['clients'][client_code], sum_em_eqs_time = sum_em_eqs(task_day['month_due_dates'][task_due_month]['clients'][client_code], eq_sum_dict, sum_em_eqs_time)
                            task_day['month_due_dates'][task_due_month]['clients'][client_code]['groups'][assigned_login_group], sum_em_eqs_time = sum_em_eqs(task_day['month_due_dates'][task_due_month]['clients'][client_code]['groups'][assigned_login_group], eq_sum_dict, sum_em_eqs_time)
                            task_day['month_due_dates'][task_due_month]['clients'][client_code]['platforms'][task_platform], sum_em_eqs_time = sum_em_eqs(task_day['month_due_dates'][task_due_month]['clients'][client_code]['platforms'][task_platform], eq_sum_dict, sum_em_eqs_time)
                            task_day['month_due_dates'][task_due_month]['by_status'][task_status], sum_em_eqs_time = sum_em_eqs(task_day['month_due_dates'][task_due_month]['by_status'][task_status], eq_sum_dict, sum_em_eqs_time)
                            task_day['month_due_dates'][task_due_month]['groups'][assigned_login_group], sum_em_eqs_time = sum_em_eqs(task_day['month_due_dates'][task_due_month]['groups'][assigned_login_group], eq_sum_dict, sum_em_eqs_time)
                            task_day['month_due_dates'][task_due_month]['groups'][assigned_login_group]['by_status'][task_status], sum_em_eqs_time = sum_em_eqs(task_day['month_due_dates'][task_due_month]['groups'][assigned_login_group]['by_status'][task_status], eq_sum_dict, sum_em_eqs_time)
                            task_day['clients'][client_code], sum_em_eqs_time = sum_em_eqs(task_day['clients'][client_code], eq_sum_dict, sum_em_eqs_time)
                            task_day['clients'][client_code]['due_dates'][task_due_day], sum_em_eqs_time = sum_em_eqs(task_day['clients'][client_code]['due_dates'][task_due_day], eq_sum_dict, sum_em_eqs_time)
                            task_day['clients'][client_code]['due_dates'][task_due_day]['by_status'][task_status], sum_em_eqs_time = sum_em_eqs(task_day['clients'][client_code]['due_dates'][task_due_day]['by_status'][task_status], eq_sum_dict, sum_em_eqs_time)
                            task_day['clients'][client_code]['due_dates'][task_due_day]['groups'][assigned_login_group], sum_em_eqs_time = sum_em_eqs(task_day['clients'][client_code]['due_dates'][task_due_day]['groups'][assigned_login_group], eq_sum_dict, sum_em_eqs_time)
                            task_day['clients'][client_code]['due_dates'][task_due_day]['groups'][assigned_login_group]['by_status'][task_status], sum_em_eqs_time = sum_em_eqs(task_day['clients'][client_code]['due_dates'][task_due_day]['groups'][assigned_login_group]['by_status'][task_status], eq_sum_dict, sum_em_eqs_time)
                            task_day['clients'][client_code]['month_due_dates'][task_due_month], sum_em_eqs_time = sum_em_eqs(task_day['clients'][client_code]['month_due_dates'][task_due_month], eq_sum_dict, sum_em_eqs_time)
                            task_day['clients'][client_code]['month_due_dates'][task_due_month]['by_status'][task_status], sum_em_eqs_time = sum_em_eqs(task_day['clients'][client_code]['month_due_dates'][task_due_month]['by_status'][task_status], eq_sum_dict, sum_em_eqs_time)
                            task_day['clients'][client_code]['month_due_dates'][task_due_month]['groups'][assigned_login_group], sum_em_eqs_time = sum_em_eqs(task_day['clients'][client_code]['month_due_dates'][task_due_month]['groups'][assigned_login_group], eq_sum_dict, sum_em_eqs_time)
                            task_day['clients'][client_code]['month_due_dates'][task_due_month]['groups'][assigned_login_group]['by_status'][task_status], sum_em_eqs_time = sum_em_eqs(task_day['clients'][client_code]['month_due_dates'][task_due_month]['groups'][assigned_login_group]['by_status'][task_status], eq_sum_dict, sum_em_eqs_time)
                            task_day['platforms'][task_platform], sum_em_eqs_time = sum_em_eqs(task_day['platforms'][task_platform], eq_sum_dict, sum_em_eqs_time)
                            task_day['platforms'][task_platform]['due_dates'][task_due_day], sum_em_eqs_time = sum_em_eqs(task_day['platforms'][task_platform]['due_dates'][task_due_day], eq_sum_dict, sum_em_eqs_time)
                            task_day['platforms'][task_platform]['due_dates'][task_due_day]['by_status'][task_status], sum_em_eqs_time = sum_em_eqs(task_day['platforms'][task_platform]['due_dates'][task_due_day]['by_status'][task_status], eq_sum_dict, sum_em_eqs_time)
                            task_day['platforms'][task_platform]['due_dates'][task_due_day]['groups'][assigned_login_group], sum_em_eqs_time = sum_em_eqs(task_day['platforms'][task_platform]['due_dates'][task_due_day]['groups'][assigned_login_group], eq_sum_dict, sum_em_eqs_time)
                            task_day['platforms'][task_platform]['due_dates'][task_due_day]['groups'][assigned_login_group]['by_status'][task_status], sum_em_eqs_time = sum_em_eqs(task_day['platforms'][task_platform]['due_dates'][task_due_day]['groups'][assigned_login_group]['by_status'][task_status], eq_sum_dict, sum_em_eqs_time)
                            task_day['platforms'][task_platform]['month_due_dates'][task_due_month], sum_em_eqs_time = sum_em_eqs(task_day['platforms'][task_platform]['month_due_dates'][task_due_month], eq_sum_dict, sum_em_eqs_time)
                            task_day['platforms'][task_platform]['month_due_dates'][task_due_month]['by_status'][task_status], sum_em_eqs_time = sum_em_eqs(task_day['platforms'][task_platform]['month_due_dates'][task_due_month]['by_status'][task_status], eq_sum_dict, sum_em_eqs_time)
                            task_day['platforms'][task_platform]['month_due_dates'][task_due_month]['groups'][assigned_login_group], sum_em_eqs_time = sum_em_eqs(task_day['platforms'][task_platform]['month_due_dates'][task_due_month]['groups'][assigned_login_group], eq_sum_dict, sum_em_eqs_time)
                            task_day['platforms'][task_platform]['month_due_dates'][task_due_month]['groups'][assigned_login_group]['by_status'][task_status], sum_em_eqs_time = sum_em_eqs(task_day['platforms'][task_platform]['month_due_dates'][task_due_month]['groups'][assigned_login_group]['by_status'][task_status], eq_sum_dict, sum_em_eqs_time)
                                
                             
                            
                            if task_status == 'Completed':
                                my_login_group = 'Not Set'
                                if task_assigned in ['','NOTHING']:
                                    task_assigned = 'Not Set'
                                else:
                                    #MIGHT NEED TO WATCH FOR PEOPLE WHO NO LONGER BELONG TO A GROUP...
                                    my_login_group = login_report[task_assigned]['default_group']
                                if task_completion_day not in task_day['completion_dates'].keys():
                                    task_day['completion_dates'][task_completion_day] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0, 'logins': {}, 'groups': {}, 'clients': {}, 'platforms': {}}
                                task_day['completion_dates'][task_completion_day]['all'].append(wo_id)

                                if task_completion_month not in task_day['month_completion_dates'].keys():
                                    task_day['month_completion_dates'][task_completion_month] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0, 'logins': {}, 'platforms': {}, 'groups': {}, 'clients': {}}
#                                else:
#                                    if 'platforms' not in task_day['month_completion_dates'][task_completion_month].keys():
#                                        task_day['month_completion_dates'][task_completion_month]['platforms'] = {}
                                task_day['month_completion_dates'][task_completion_month]['all'].append(wo_id)

                                if task_platform not in task_day['month_completion_dates'][task_completion_month]['platforms'].keys():
                                    task_day['month_completion_dates'][task_completion_month]['platforms'][task_platform] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0, 'groups': {}, 'logins': {}}
                                task_day['month_completion_dates'][task_completion_month]['platforms'][task_platform]['all'].append(wo_id)
    
                                if task_assigned not in task_day['completion_dates'][task_completion_day]['logins'].keys():
                                    task_day['completion_dates'][task_completion_day]['logins'][task_assigned] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0}
                                task_day['completion_dates'][task_completion_day]['logins'][task_assigned]['all'].append(wo_id)

                                if task_assigned not in task_day['month_completion_dates'][task_completion_month]['logins'].keys():
                                    task_day['month_completion_dates'][task_completion_month]['logins'][task_assigned] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0}
                                task_day['month_completion_dates'][task_completion_month]['logins'][task_assigned]['all'].append(wo_id)
    
                                if my_login_group not in task_day['completion_dates'][task_completion_day]['groups'].keys():
                                    task_day['completion_dates'][task_completion_day]['groups'][my_login_group] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0, 'logins': {}}
                                task_day['completion_dates'][task_completion_day]['groups'][my_login_group]['all'].append(wo_id)

                                if my_login_group not in task_day['month_completion_dates'][task_completion_month]['groups'].keys():
                                    task_day['month_completion_dates'][task_completion_month]['groups'][my_login_group] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0, 'logins': {}}
                                task_day['month_completion_dates'][task_completion_month]['groups'][my_login_group]['all'].append(wo_id)
                                #print "TD GROUP = %s, LOGIN = %s" % (my_login_group, task_assigned) 
                                if task_assigned not in task_day['completion_dates'][task_completion_day]['groups'][my_login_group]['logins'].keys():
                                    task_day['completion_dates'][task_completion_day]['groups'][my_login_group]['logins'][task_assigned] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0}
                                task_day['completion_dates'][task_completion_day]['groups'][my_login_group]['logins'][task_assigned]['all'].append(wo_id)

                                if task_assigned not in task_day['month_completion_dates'][task_completion_month]['groups'][my_login_group]['logins'].keys():
                                    task_day['month_completion_dates'][task_completion_month]['groups'][my_login_group]['logins'][task_assigned] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0}
                                task_day['month_completion_dates'][task_completion_month]['groups'][my_login_group]['logins'][task_assigned]['all'].append(wo_id)
    
                                if client_code not in task_day['completion_dates'][task_completion_day]['clients'].keys():
                                    task_day['completion_dates'][task_completion_day]['clients'][client_code] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0, 'groups': {}, 'logins': {}}
                                task_day['completion_dates'][task_completion_day]['clients'][client_code]['all'].append(wo_id)

                                if client_code not in task_day['month_completion_dates'][task_completion_month]['clients'].keys():
                                    task_day['month_completion_dates'][task_completion_month]['clients'][client_code] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0, 'groups': {}, 'logins': {}}
                                task_day['month_completion_dates'][task_completion_month]['clients'][client_code]['all'].append(wo_id)
                                if task_platform not in task_day['completion_dates'][task_completion_day]['platforms'].keys():
                                    task_day['completion_dates'][task_completion_day]['platforms'][task_platform] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0, 'logins': {}, 'groups': {}}

                                
                                task_day['completion_dates'][task_completion_day], sum_em_eqs_time = sum_em_eqs(task_day['completion_dates'][task_completion_day], eq_sum_dict, sum_em_whs_time)
                                #task_day['completion_dates'][task_completion_day]['logins'][task_assigned], sum_em_eqs_time = sum_em_eqs(task_day['completion_dates'][task_completion_day]['logins'][task_assigned], eq_sum_dict, sum_em_whs_time)
                                task_day['completion_dates'][task_completion_day]['groups'][my_login_group], sum_em_eqs_time = sum_em_eqs(task_day['completion_dates'][task_completion_day]['groups'][my_login_group], eq_sum_dict, sum_em_whs_time)
                                #print "T COUNT = %s, GROUP = %s, LOGIN = %s" % (t_count, my_login_group, task_assigned)
                                #task_day['completion_dates'][task_completion_day]['groups'][my_login_group]['logins'][task_assigned], sum_em_eqs_time = sum_em_eqs(task_day['completion_dates'][task_completion_day]['groups'][my_login_group]['logins'][task_assigned], eq_sum_dict, sum_em_whs_time)
                                task_day['completion_dates'][task_completion_day]['clients'][client_code], sum_em_eqs_time = sum_em_eqs(task_day['completion_dates'][task_completion_day]['clients'][client_code], eq_sum_dict, sum_em_whs_time)
                                task_day['completion_dates'][task_completion_day]['platforms'][task_platform], sum_em_eqs_time = sum_em_eqs(task_day['completion_dates'][task_completion_day]['platforms'][task_platform], eq_sum_dict, sum_em_whs_time)
                                task_day['month_completion_dates'][task_completion_month], sum_em_eqs_time = sum_em_eqs(task_day['month_completion_dates'][task_completion_month], eq_sum_dict, sum_em_whs_time)
                                #task_day['month_completion_dates'][task_completion_month]['logins'][task_assigned], sum_em_eqs_time = sum_em_eqs(task_day['month_completion_dates'][task_completion_month]['logins'][task_assigned], eq_sum_dict, sum_em_whs_time)
                                #task_day['month_completion_dates'][task_completion_month]['groups'][my_login_group], sum_em_eqs_time = sum_em_eqs(task_day['month_completion_dates'][task_completion_month]['groups'][my_login_group], eq_sum_dict, sum_em_whs_time)
                                #task_day['month_completion_dates'][task_completion_month]['groups'][my_login_group]['logins'][task_assigned], sum_em_eqs_time = sum_em_eqs(task_day['month_completion_dates'][task_completion_month]['groups'][my_login_group]['logins'][task_assigned], eq_sum_dict, sum_em_whs_time)
                                task_day['month_completion_dates'][task_completion_month]['clients'][client_code], sum_em_eqs_time = sum_em_eqs(task_day['month_completion_dates'][task_completion_month]['clients'][client_code], eq_sum_dict, sum_em_whs_time)
                                task_day['month_completion_dates'][task_completion_month]['platforms'][task_platform], sum_em_eqs_time = sum_em_eqs(task_day['month_completion_dates'][task_completion_month]['platforms'][task_platform], eq_sum_dict, sum_em_whs_time)
                            t_count = t_count + 1 
                            whs = []
                            try:
                                whs = work_hours[task_code]
                            except:
                                pass
                            nlogins = {}
                            ngroups = {}
                            send_dict = {'total_hours': 0.0, 'estimated_work_hours': 0.0, 'billable_hours': 0.0, 'actual_cost': 0.0, 'estimated_cost': 0.0, 'billable_cost': 0.0, 'code': work_order_code}
                            login = task_assigned 
                            hour_day = ''
                            hour_month = ''
                            for wh in whs:
                                wh_code = wh['code']
                                is_billable = wh['is_billable']
                                straight_time = make_number(wh['straight_time'])
                                hour_day = wh['day'].split(' ')[0]
                                if hour_day in [None,'']:
                                    hour_day = '1999-01-01'
                                hcds = hour_day.split('-')
                                hour_month = '%s-%s' % (hcds[0], hcds[1])
                                login = wh['login']
                                default_rate = 0.0
                                if login in login_codes:
                                    default_rate = make_number(login_report[login]['default_rate'])
                                lgroup = login_report[login]['default_group']
                                total_hours = straight_time 
                                billable_hours = 0.0
                                if is_billable not in [None,'','f',False]:
                                    billable_hours = total_hours
                                actual_cost = total_hours * default_rate
                                estimated_cost = estimated_work_hours * default_rate
                                billable_cost = billable_hours * default_rate        
                                if send_dict['estimated_work_hours'] in [0,0.0]:
                                    send_dict['estimated_work_hours'] = estimated_work_hours
                                if send_dict['estimated_cost'] in [0,0.0]:
                                    send_dict['estimated_cost'] = estimated_cost
                                send_dict['total_hours'] = send_dict['total_hours'] + total_hours
                                send_dict['billable_hours'] = send_dict['billable_hours'] + billable_hours
                                send_dict['actual_cost'] = send_dict['actual_cost'] + actual_cost
                                send_dict['billable_cost'] = send_dict['billable_cost'] + billable_cost
                                if login not in nlogins.keys():
                                    nlogins[login] = {'total_hours': 0.0, 'estimated_work_hours': estimated_work_hours, 'billable_hours': 0.0, 'actual_cost': 0.0, 'estimated_cost': estimated_cost, 'billable_cost': 0.0, 'code': work_order_code}
                                if lgroup not in ngroups.keys():
                                    ngroups[lgroup] = {'total_hours': 0.0, 'estimated_work_hours': estimated_work_hours, 'billable_hours': 0.0, 'actual_cost': 0.0, 'estimated_cost': estimated_cost, 'billable_cost': 0.0, 'code': work_order_code}
                                nlogins[login]['total_hours'] = nlogins[login]['total_hours'] + total_hours
                                nlogins[login]['billable_hours'] = nlogins[login]['billable_hours'] + billable_hours
                                nlogins[login]['actual_cost'] = nlogins[login]['actual_cost'] + actual_cost
                                nlogins[login]['billable_cost'] = nlogins[login]['billable_cost'] + billable_cost
                                ngroups[lgroup]['total_hours'] = ngroups[lgroup]['total_hours'] + total_hours
                                ngroups[lgroup]['billable_hours'] = ngroups[lgroup]['billable_hours'] + billable_hours
                                ngroups[lgroup]['actual_cost'] = ngroups[lgroup]['actual_cost'] + actual_cost
                                ngroups[lgroup]['billable_cost'] = ngroups[lgroup]['billable_cost'] + billable_cost
                                #NOW DO PEOPLE AND GROUPS, then make the following sums consider the login and group
                            order_days, sum_em_whs_time = sum_em_whs(order_days, send_dict, sum_em_whs_time)
                            if future:
                                order_days['future'], sum_em_whs_time = sum_em_whs(order_days['future'], send_dict, sum_em_whs_time)
                            if late:
                                order_days['late'], sum_em_whs_time = sum_em_whs(order_days['late'], send_dict, sum_em_whs_time)
                            order_days['due_dates'][order_due_day], sum_em_whs_time = sum_em_whs(order_days['due_dates'][order_due_day], send_dict, sum_em_whs_time)
                            order_days['due_dates'][order_due_day], sum_em_whs_time = sum_em_whs(order_days['due_dates'][order_due_day], send_dict, sum_em_whs_time)
                            order_days['month_due_dates'][order_due_month], sum_em_whs_time = sum_em_whs(order_days['month_due_dates'][order_due_month], send_dict, sum_em_whs_time)
                            order_days['month_due_dates'][order_due_month], sum_em_whs_time = sum_em_whs(order_days['month_due_dates'][order_due_month], send_dict, sum_em_whs_time)
                            order_days['completion_dates'][order_completion_day], sum_em_whs_time = sum_em_whs(order_days['completion_dates'][order_completion_day], send_dict, sum_em_whs_time)
                            order_days['completion_dates'][order_completion_day]['by_billed'][billed], sum_em_whs_time = sum_em_whs(order_days['completion_dates'][order_completion_day]['by_billed'][billed], send_dict, sum_em_whs_time)
                            order_days['month_completion_dates'][order_completion_month], sum_em_whs_time = sum_em_whs(order_days['month_completion_dates'][order_completion_month], send_dict, sum_em_whs_time)
                            order_days['month_completion_dates'][order_completion_month]['by_billed'][billed], sum_em_whs_time = sum_em_whs(order_days['month_completion_dates'][order_completion_month]['by_billed'][billed], send_dict, sum_em_whs_time)
                            order_days['billed_dates'][order_billed_day], sum_em_whs_time = sum_em_whs(order_days['billed_dates'][order_billed_day], send_dict, sum_em_whs_time)
                            order_days['billed_dates'][order_billed_day]['by_billed'][billed], sum_em_whs_time = sum_em_whs(order_days['billed_dates'][order_billed_day]['by_billed'][billed], send_dict, sum_em_whs_time)
                            order_days['month_billed_dates'][order_billed_month], sum_em_whs_time = sum_em_whs(order_days['month_billed_dates'][order_billed_month], send_dict, sum_em_whs_time)
                            order_days['month_billed_dates'][order_billed_month]['by_billed'][billed], sum_em_whs_time = sum_em_whs(order_days['month_billed_dates'][order_billed_month]['by_billed'][billed], send_dict, sum_em_whs_time)
                            order_days['by_classification'][classification], sum_em_whs_time = sum_em_whs(order_days['by_classification'][classification], send_dict, sum_em_whs_time)
                            order_days['by_billed'][billed], sum_em_whs_time = sum_em_whs(order_days['by_billed'][billed], send_dict, sum_em_whs_time)
                            order_days['due_dates'][order_due_day]['by_billed'][billed], sum_em_whs_time = sum_em_whs(order_days['due_dates'][order_due_day]['by_billed'][billed], send_dict, sum_em_whs_time)
                            order_days['due_dates'][order_due_day]['by_classification'][classification], sum_em_whs_time = sum_em_whs(order_days['due_dates'][order_due_day]['by_classification'][classification], send_dict, sum_em_whs_time)
                            order_clients[client_code], sum_em_whs_time = sum_em_whs(order_clients[client_code], send_dict, sum_em_whs_time) 
                            order_clients[client_code]['by_billed'][billed], sum_em_whs_time = sum_em_whs(order_clients[client_code]['by_billed'][billed], send_dict, sum_em_whs_time) 
                            order_clients[client_code]['completion_dates'][order_completion_day], sum_em_whs_time = sum_em_whs(order_clients[client_code]['completion_dates'][order_completion_day],send_dict, sum_em_whs_time) 
                            order_clients[client_code]['completion_dates'][order_completion_day]['by_billed'][billed], sum_em_whs_time = sum_em_whs(order_clients[client_code]['completion_dates'][order_completion_day]['by_billed'][billed],send_dict, sum_em_whs_time) 
                            order_clients[client_code]['month_completion_dates'][order_completion_month], sum_em_whs_time = sum_em_whs(order_clients[client_code]['month_completion_dates'][order_completion_month],send_dict, sum_em_whs_time) 
                            order_clients[client_code]['month_completion_dates'][order_completion_month]['by_billed'][billed], sum_em_whs_time = sum_em_whs(order_clients[client_code]['month_completion_dates'][order_completion_month]['by_billed'][billed],send_dict, sum_em_whs_time) 
                            order_clients[client_code]['billed_dates'][order_billed_day], sum_em_whs_time = sum_em_whs(order_clients[client_code]['billed_dates'][order_billed_day],send_dict, sum_em_whs_time) 
                            order_clients[client_code]['billed_dates'][order_billed_day]['by_billed'][billed], sum_em_whs_time = sum_em_whs(order_clients[client_code]['billed_dates'][order_billed_day]['by_billed'][billed],send_dict, sum_em_whs_time) 
                            order_clients[client_code]['month_billed_dates'][order_billed_month], sum_em_whs_time = sum_em_whs(order_clients[client_code]['month_billed_dates'][order_billed_month],send_dict, sum_em_whs_time) 
                            order_clients[client_code]['month_billed_dates'][order_billed_month]['by_billed'][billed], sum_em_whs_time = sum_em_whs(order_clients[client_code]['month_billed_dates'][order_billed_month]['by_billed'][billed],send_dict, sum_em_whs_time) 
                            order_clients[client_code]['due_dates'][order_due_day], sum_em_whs_time = sum_em_whs(order_clients[client_code]['due_dates'][order_due_day], send_dict, sum_em_whs_time) 
                            order_clients[client_code]['due_dates'][order_due_day]['by_classification'][classification], sum_em_whs_time = sum_em_whs(order_clients[client_code]['due_dates'][order_due_day]['by_classification'][classification],send_dict, sum_em_whs_time) 
                            order_clients[client_code]['due_dates'][order_due_day]['by_billed'][billed], sum_em_whs_time = sum_em_whs(order_clients[client_code]['due_dates'][order_due_day]['by_billed'][billed],send_dict, sum_em_whs_time) 
                            order_clients[client_code]['month_due_dates'][order_due_month], sum_em_whs_time = sum_em_whs(order_clients[client_code]['month_due_dates'][order_due_month], send_dict, sum_em_whs_time) 
                            order_clients[client_code]['month_due_dates'][order_due_month]['by_classification'][classification], sum_em_whs_time = sum_em_whs(order_clients[client_code]['month_due_dates'][order_due_month]['by_classification'][classification],send_dict, sum_em_whs_time) 
                            order_clients[client_code]['month_due_dates'][order_due_month]['by_billed'][billed], sum_em_whs_time = sum_em_whs(order_clients[client_code]['month_due_dates'][order_due_month]['by_billed'][billed],send_dict, sum_em_whs_time) 
                            #CONTINUE WRITING MONTHS HERE
                            order_platforms[platform], sum_em_whs_time = sum_em_whs(order_platforms[platform],send_dict, sum_em_whs_time) 
                            order_platforms[platform]['by_billed'][billed], sum_em_whs_time = sum_em_whs(order_platforms[platform]['by_billed'][billed],send_dict, sum_em_whs_time) 
                            order_platforms[platform]['completion_dates'][order_completion_day], sum_em_whs_time = sum_em_whs(order_platforms[platform]['completion_dates'][order_completion_day],send_dict, sum_em_whs_time) 
                            order_platforms[platform]['month_completion_dates'][order_completion_month], sum_em_whs_time = sum_em_whs(order_platforms[platform]['month_completion_dates'][order_completion_month],send_dict, sum_em_whs_time) 
                            order_platforms[platform]['billed_dates'][order_billed_day], sum_em_whs_time = sum_em_whs(order_platforms[platform]['billed_dates'][order_billed_day],send_dict, sum_em_whs_time) 
                            order_platforms[platform]['month_billed_dates'][order_billed_month], sum_em_whs_time = sum_em_whs(order_platforms[platform]['month_billed_dates'][order_billed_month],send_dict, sum_em_whs_time) 
                            order_platforms[platform]['due_dates'][order_due_day], sum_em_whs_time = sum_em_whs(order_platforms[platform]['due_dates'][order_due_day],send_dict, sum_em_whs_time) 
                            order_platforms[platform]['due_dates'][order_due_day]['by_classification'][classification], sum_em_whs_time = sum_em_whs(order_platforms[platform]['due_dates'][order_due_day]['by_classification'][classification],send_dict, sum_em_whs_time) 
                            order_platforms[platform]['due_dates'][order_due_day]['by_billed'][billed], sum_em_whs_time = sum_em_whs(order_platforms[platform]['due_dates'][order_due_day]['by_billed'][billed],send_dict, sum_em_whs_time) 
                            order_platforms[platform]['month_due_dates'][order_due_month], sum_em_whs_time = sum_em_whs(order_platforms[platform]['month_due_dates'][order_due_month],send_dict, sum_em_whs_time) 
                            order_platforms[platform]['month_due_dates'][order_due_month]['by_classification'][classification], sum_em_whs_time = sum_em_whs(order_platforms[platform]['month_due_dates'][order_due_month]['by_classification'][classification],send_dict, sum_em_whs_time) 
                            order_platforms[platform]['month_due_dates'][order_due_month]['by_billed'][billed], sum_em_whs_time = sum_em_whs(order_platforms[platform]['month_due_dates'][order_due_month]['by_billed'][billed],send_dict, sum_em_whs_time) 
                            task_day['by_status'][task_status], sum_em_whs_time = sum_em_whs(task_day['by_status'][task_status], send_dict, sum_em_whs_time)
                            task_day['due_dates'][task_due_day], sum_em_whs_time = sum_em_whs(task_day['due_dates'][task_due_day], send_dict, sum_em_whs_time)
                            task_day['due_dates'][task_due_day]['platforms'][task_platform], sum_em_whs_time = sum_em_whs(task_day['due_dates'][task_due_day]['platforms'][task_platform], send_dict, sum_em_whs_time)
                            task_day['due_dates'][task_due_day]['clients'][client_code], sum_em_whs_time = sum_em_whs(task_day['due_dates'][task_due_day]['clients'][client_code], send_dict, sum_em_whs_time)
                            task_day['due_dates'][task_due_day]['clients'][client_code]['groups'][assigned_login_group], sum_em_whs_time = sum_em_whs(task_day['due_dates'][task_due_day]['clients'][client_code]['groups'][assigned_login_group], send_dict, sum_em_whs_time)
                            task_day['due_dates'][task_due_day]['clients'][client_code]['platforms'][task_platform], sum_em_whs_time = sum_em_whs(task_day['due_dates'][task_due_day]['clients'][client_code]['platforms'][task_platform], send_dict, sum_em_whs_time)
                            task_day['due_dates'][task_due_day]['by_status'][task_status], sum_em_whs_time = sum_em_whs(task_day['due_dates'][task_due_day]['by_status'][task_status], send_dict, sum_em_whs_time)
                            task_day['due_dates'][task_due_day]['groups'][assigned_login_group], sum_em_whs_time = sum_em_whs(task_day['due_dates'][task_due_day]['groups'][assigned_login_group], send_dict, sum_em_whs_time)
                            task_day['due_dates'][task_due_day]['groups'][assigned_login_group]['by_status'][task_status], sum_em_whs_time = sum_em_whs(task_day['due_dates'][task_due_day]['groups'][assigned_login_group]['by_status'][task_status], send_dict, sum_em_whs_time)
                            task_day['month_due_dates'][task_due_month], sum_em_whs_time = sum_em_whs(task_day['month_due_dates'][task_due_month], send_dict, sum_em_whs_time)
                            task_day['month_due_dates'][task_due_month]['platforms'][task_platform], sum_em_whs_time = sum_em_whs(task_day['month_due_dates'][task_due_month]['platforms'][task_platform], send_dict, sum_em_whs_time)
                            task_day['month_due_dates'][task_due_month]['clients'][client_code], sum_em_whs_time = sum_em_whs(task_day['month_due_dates'][task_due_month]['clients'][client_code], send_dict, sum_em_whs_time)
                            task_day['month_due_dates'][task_due_month]['clients'][client_code]['groups'][assigned_login_group], sum_em_whs_time = sum_em_whs(task_day['month_due_dates'][task_due_month]['clients'][client_code]['groups'][assigned_login_group], send_dict, sum_em_whs_time)
                            task_day['month_due_dates'][task_due_month]['clients'][client_code]['platforms'][task_platform], sum_em_whs_time = sum_em_whs(task_day['month_due_dates'][task_due_month]['clients'][client_code]['platforms'][task_platform], send_dict, sum_em_whs_time)
                            task_day['month_due_dates'][task_due_month]['by_status'][task_status], sum_em_whs_time = sum_em_whs(task_day['month_due_dates'][task_due_month]['by_status'][task_status], send_dict, sum_em_whs_time)
                            task_day['month_due_dates'][task_due_month]['groups'][assigned_login_group], sum_em_whs_time = sum_em_whs(task_day['month_due_dates'][task_due_month]['groups'][assigned_login_group], send_dict, sum_em_whs_time)
                            task_day['month_due_dates'][task_due_month]['groups'][assigned_login_group]['by_status'][task_status], sum_em_whs_time = sum_em_whs(task_day['month_due_dates'][task_due_month]['groups'][assigned_login_group]['by_status'][task_status], send_dict, sum_em_whs_time)
                            task_day['clients'][client_code], sum_em_whs_time = sum_em_whs(task_day['clients'][client_code], send_dict, sum_em_whs_time)
                            task_day['clients'][client_code]['due_dates'][task_due_day], sum_em_whs_time = sum_em_whs(task_day['clients'][client_code]['due_dates'][task_due_day], send_dict, sum_em_whs_time)
                            task_day['clients'][client_code]['due_dates'][task_due_day]['by_status'][task_status], sum_em_whs_time = sum_em_whs(task_day['clients'][client_code]['due_dates'][task_due_day]['by_status'][task_status], send_dict, sum_em_whs_time)
                            task_day['clients'][client_code]['due_dates'][task_due_day]['groups'][assigned_login_group], sum_em_whs_time = sum_em_whs(task_day['clients'][client_code]['due_dates'][task_due_day]['groups'][assigned_login_group], send_dict, sum_em_whs_time)
                            task_day['clients'][client_code]['due_dates'][task_due_day]['groups'][assigned_login_group]['by_status'][task_status], sum_em_whs_time = sum_em_whs(task_day['clients'][client_code]['due_dates'][task_due_day]['groups'][assigned_login_group]['by_status'][task_status], send_dict, sum_em_whs_time)
                            task_day['clients'][client_code]['month_due_dates'][task_due_month], sum_em_whs_time = sum_em_whs(task_day['clients'][client_code]['month_due_dates'][task_due_month], send_dict, sum_em_whs_time)
                            task_day['clients'][client_code]['month_due_dates'][task_due_month]['by_status'][task_status], sum_em_whs_time = sum_em_whs(task_day['clients'][client_code]['month_due_dates'][task_due_month]['by_status'][task_status], send_dict, sum_em_whs_time)
                            task_day['clients'][client_code]['month_due_dates'][task_due_month]['groups'][assigned_login_group], sum_em_whs_time = sum_em_whs(task_day['clients'][client_code]['month_due_dates'][task_due_month]['groups'][assigned_login_group], send_dict, sum_em_whs_time)
                            task_day['clients'][client_code]['month_due_dates'][task_due_month]['groups'][assigned_login_group]['by_status'][task_status], sum_em_whs_time = sum_em_whs(task_day['clients'][client_code]['month_due_dates'][task_due_month]['groups'][assigned_login_group]['by_status'][task_status], send_dict, sum_em_whs_time)
                            task_day['platforms'][task_platform], sum_em_whs_time = sum_em_whs(task_day['platforms'][task_platform], send_dict, sum_em_whs_time)
                            task_day['platforms'][task_platform]['due_dates'][task_due_day], sum_em_whs_time = sum_em_whs(task_day['platforms'][task_platform]['due_dates'][task_due_day], send_dict, sum_em_whs_time)
                            task_day['platforms'][task_platform]['due_dates'][task_due_day]['by_status'][task_status], sum_em_whs_time = sum_em_whs(task_day['platforms'][task_platform]['due_dates'][task_due_day]['by_status'][task_status], send_dict, sum_em_whs_time)
                            task_day['platforms'][task_platform]['due_dates'][task_due_day]['groups'][assigned_login_group], sum_em_whs_time = sum_em_whs(task_day['platforms'][task_platform]['due_dates'][task_due_day]['groups'][assigned_login_group], send_dict, sum_em_whs_time)
                            task_day['platforms'][task_platform]['due_dates'][task_due_day]['groups'][assigned_login_group]['by_status'][task_status], sum_em_whs_time = sum_em_whs(task_day['platforms'][task_platform]['due_dates'][task_due_day]['groups'][assigned_login_group]['by_status'][task_status], send_dict, sum_em_whs_time)
                            task_day['platforms'][task_platform]['month_due_dates'][task_due_month], sum_em_whs_time = sum_em_whs(task_day['platforms'][task_platform]['month_due_dates'][task_due_month], send_dict, sum_em_whs_time)
                            task_day['platforms'][task_platform]['month_due_dates'][task_due_month]['by_status'][task_status], sum_em_whs_time = sum_em_whs(task_day['platforms'][task_platform]['month_due_dates'][task_due_month]['by_status'][task_status], send_dict, sum_em_whs_time)
                            task_day['platforms'][task_platform]['month_due_dates'][task_due_month]['groups'][assigned_login_group], sum_em_whs_time = sum_em_whs(task_day['platforms'][task_platform]['month_due_dates'][task_due_month]['groups'][assigned_login_group], send_dict, sum_em_whs_time)
                            task_day['platforms'][task_platform]['month_due_dates'][task_due_month]['groups'][assigned_login_group]['by_status'][task_status], sum_em_whs_time = sum_em_whs(task_day['platforms'][task_platform]['month_due_dates'][task_due_month]['groups'][assigned_login_group]['by_status'][task_status], send_dict, sum_em_whs_time)
                            if task_status == 'Completed':
                                my_login_group = 'Not Set'
                                if login not in ['','Nothing']:
                                    my_login_group = login_report[login]['default_group']
                                else:
                                    login = 'Not Set'
                                if hour_day not in task_day['completion_dates'].keys():
                                    task_day['completion_dates'][hour_day] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0, 'logins': {}, 'groups': {}, 'clients': {}, 'platforms': {}}
                                    task_day['completion_dates'][hour_day], sum_em_eqs_time = sum_em_eqs(task_day['completion_dates'][hour_day], eq_sum_dict, sum_em_whs_time)
                                task_day['completion_dates'][hour_day]['all'].append(wo_id)

                                if hour_month not in task_day['month_completion_dates'].keys():
                                    task_day['month_completion_dates'][hour_month] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0, 'logins': {}, 'groups': {}, 'clients': {}, 'platforms': {}}
                                    task_day['month_completion_dates'][hour_month], sum_em_eqs_time = sum_em_eqs(task_day['month_completion_dates'][hour_month], eq_sum_dict, sum_em_whs_time)
                                task_day['month_completion_dates'][hour_month]['all'].append(wo_id)

                                if task_platform not in task_day['completion_dates'][hour_day]['platforms'].keys():
                                    task_day['completion_dates'][hour_day]['platforms'][task_platform] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0, 'logins': {}, 'groups': {}, 'clients': {}, 'platforms': {}}
                                    task_day['completion_dates'][hour_day]['platforms'][task_platform], sum_em_eqs_time = sum_em_eqs(task_day['completion_dates'][hour_day]['platforms'][task_platform], eq_sum_dict, sum_em_whs_time)
                                task_day['completion_dates'][hour_day]['platforms'][task_platform]['all'].append(wo_id)

                                if task_platform not in task_day['month_completion_dates'][hour_month]['platforms'].keys():
                                    task_day['month_completion_dates'][hour_month]['platforms'][task_platform] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0, 'logins': {}, 'groups': {}, 'clients': {}}
                                    task_day['month_completion_dates'][hour_month]['platforms'][task_platform], sum_em_eqs_time = sum_em_eqs(task_day['month_completion_dates'][hour_month]['platforms'][task_platform], eq_sum_dict, sum_em_whs_time)
                                task_day['month_completion_dates'][hour_month]['platforms'][task_platform]['all'].append(wo_id)

                                if client_code not in task_day['completion_dates'][hour_day]['clients'].keys():
                                    task_day['completion_dates'][hour_day]['clients'][client_code] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0, 'logins': {}, 'groups': {}}
                                    task_day['completion_dates'][hour_day]['clients'][client_code], sum_em_eqs_time = sum_em_eqs(task_day['completion_dates'][hour_day]['clients'][client_code], eq_sum_dict, sum_em_whs_time)
                                task_day['completion_dates'][hour_day]['clients'][client_code]['all'].append(wo_id)

                                if client_code not in task_day['month_completion_dates'][hour_month]['clients'].keys():
                                    task_day['month_completion_dates'][hour_month]['clients'][client_code] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0, 'logins': {}, 'groups': {}}
                                    task_day['month_completion_dates'][hour_month]['clients'][client_code], sum_em_eqs_time = sum_em_eqs(task_day['month_completion_dates'][hour_month]['clients'][client_code], eq_sum_dict, sum_em_whs_time)
                                task_day['month_completion_dates'][hour_month]['clients'][client_code]['all'].append(wo_id)
                                for ngroup in ngroups.keys():
                                    if ngroup not in task_day['completion_dates'][hour_day]['platforms'][task_platform]['groups'].keys():
                                        task_day['completion_dates'][hour_day]['platforms'][task_platform]['groups'][ngroup] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0}
                                        task_day['completion_dates'][hour_day]['platforms'][task_platform]['groups'][ngroup], sum_em_eqs_time = sum_em_eqs(task_day['completion_dates'][hour_day]['platforms'][task_platform]['groups'][ngroup], eq_sum_dict, sum_em_whs_time)
                                    task_day['completion_dates'][hour_day]['platforms'][task_platform]['groups'][ngroup]['all'].append(wo_id)

                                    if ngroup not in task_day['month_completion_dates'][hour_month]['platforms'][task_platform]['groups'].keys():
                                        task_day['month_completion_dates'][hour_month]['platforms'][task_platform]['groups'][ngroup] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0}
                                        task_day['month_completion_dates'][hour_month]['platforms'][task_platform]['groups'][ngroup], sum_em_eqs_time = sum_em_eqs(task_day['month_completion_dates'][hour_month]['platforms'][task_platform]['groups'][ngroup], eq_sum_dict, sum_em_whs_time)
                                    task_day['month_completion_dates'][hour_month]['platforms'][task_platform]['groups'][ngroup]['all'].append(wo_id)

    
                                    if ngroup not in task_day['completion_dates'][hour_day]['groups'].keys():
                                        task_day['completion_dates'][hour_day]['groups'][ngroup] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0, 'logins': {}}
                                        task_day['completion_dates'][hour_day]['groups'][ngroup], sum_em_eqs_time = sum_em_eqs(task_day['completion_dates'][hour_day]['groups'][ngroup], eq_sum_dict, sum_em_whs_time)
                                    task_day['completion_dates'][hour_day]['groups'][ngroup]['all'].append(wo_id)

                                    if ngroup not in task_day['month_completion_dates'][hour_month]['groups'].keys():
                                        task_day['month_completion_dates'][hour_month]['groups'][ngroup] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0, 'logins': {}}
                                        task_day['month_completion_dates'][hour_month]['groups'][ngroup], sum_em_eqs_time = sum_em_eqs(task_day['month_completion_dates'][hour_month]['groups'][ngroup], eq_sum_dict, sum_em_whs_time)
                                    task_day['month_completion_dates'][hour_month]['groups'][ngroup]['all'].append(wo_id)
    
                                    if ngroup not in task_day['completion_dates'][hour_day]['clients'][client_code]['groups'].keys():
                                        task_day['completion_dates'][hour_day]['clients'][client_code]['groups'][ngroup] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0, 'logins': {}}
                                        task_day['completion_dates'][hour_day]['clients'][client_code]['groups'][ngroup], sum_em_eqs_time = sum_em_eqs(task_day['completion_dates'][hour_day]['clients'][client_code]['groups'][ngroup], eq_sum_dict, sum_em_whs_time)
                                    task_day['completion_dates'][hour_day]['clients'][client_code]['groups'][ngroup]['all'].append(wo_id)

                                    if ngroup not in task_day['month_completion_dates'][hour_month]['clients'][client_code]['groups'].keys():
                                        task_day['month_completion_dates'][hour_month]['clients'][client_code]['groups'][ngroup] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0, 'logins': {}}
                                        task_day['month_completion_dates'][hour_month]['clients'][client_code]['groups'][ngroup], sum_em_eqs_time = sum_em_eqs(task_day['month_completion_dates'][hour_month]['clients'][client_code]['groups'][ngroup], eq_sum_dict, sum_em_whs_time)
                                    task_day['month_completion_dates'][hour_month]['clients'][client_code]['groups'][ngroup]['all'].append(wo_id)

                                    for nlogin in nlogins.keys():
                                        if ngroup == login_report[nlogin]['default_group']:
                                            if nlogin not in task_day['completion_dates'][hour_day]['groups'][ngroup]['logins'].keys():
                                                task_day['completion_dates'][hour_day]['groups'][ngroup]['logins'][nlogin] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0}
                                                task_day['completion_dates'][hour_day]['groups'][ngroup]['logins'][nlogin], sum_em_eqs_time = sum_em_eqs(task_day['completion_dates'][hour_day]['groups'][ngroup]['logins'][nlogin], eq_sum_dict, sum_em_whs_time)
                                            task_day['completion_dates'][hour_day]['groups'][ngroup]['logins'][nlogin]['all'].append(wo_id)
                                            if nlogin not in task_day['month_completion_dates'][hour_month]['groups'][ngroup]['logins'].keys():
                                                task_day['month_completion_dates'][hour_month]['groups'][ngroup]['logins'][nlogin] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0}
                                                task_day['month_completion_dates'][hour_month]['groups'][ngroup]['logins'][nlogin], sum_em_eqs_time = sum_em_eqs(task_day['month_completion_dates'][hour_month]['groups'][ngroup]['logins'][nlogin], eq_sum_dict, sum_em_whs_time)
                                            task_day['month_completion_dates'][hour_month]['groups'][ngroup]['logins'][nlogin]['all'].append(wo_id)
                                            if nlogin not in task_day['completion_dates'][hour_day]['clients'][client_code]['groups'][ngroup]['logins'].keys():
                                                task_day['completion_dates'][hour_day]['clients'][client_code]['groups'][ngroup]['logins'][nlogin] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0}
                                                task_day['completion_dates'][hour_day]['clients'][client_code]['groups'][ngroup]['logins'][nlogin], sum_em_eqs_time = sum_em_eqs(task_day['completion_dates'][hour_day]['groups'][ngroup]['logins'][nlogin], eq_sum_dict, sum_em_whs_time)
                                            task_day['completion_dates'][hour_day]['clients'][client_code]['groups'][ngroup]['logins'][nlogin]['all'].append(wo_id)
                                            if nlogin not in task_day['month_completion_dates'][hour_month]['clients'][client_code]['groups'][ngroup]['logins'].keys():
                                                task_day['month_completion_dates'][hour_month]['clients'][client_code]['groups'][ngroup]['logins'][nlogin] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0}
                                                task_day['month_completion_dates'][hour_month]['clients'][client_code]['groups'][ngroup]['logins'][nlogin], sum_em_eqs_time = sum_em_eqs(task_day['month_completion_dates'][hour_month]['clients'][client_code]['groups'][ngroup]['logins'][nlogin], eq_sum_dict, sum_em_whs_time)
                                            task_day['month_completion_dates'][hour_month]['clients'][client_code]['groups'][ngroup]['logins'][nlogin]['all'].append(wo_id)
                                for nlogin in nlogins.keys():
                                    if nlogin not in task_day['completion_dates'][hour_day]['logins'].keys():
                                        task_day['completion_dates'][hour_day]['logins'][nlogin] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0}
                                        task_day['completion_dates'][hour_day]['logins'][nlogin], sum_em_eqs_time = sum_em_eqs(task_day['completion_dates'][hour_day]['logins'][nlogin], eq_sum_dict, sum_em_whs_time)
                                    task_day['completion_dates'][hour_day]['logins'][nlogin]['all'].append(wo_id)
                                    if nlogin not in task_day['completion_dates'][hour_day]['platforms'][task_platform]['logins'].keys():
                                        task_day['completion_dates'][hour_day]['platforms'][task_platform]['logins'][nlogin] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0}
                                        task_day['completion_dates'][hour_day]['platforms'][task_platform]['logins'][nlogin], sum_em_eqs_time = sum_em_eqs(task_day['completion_dates'][hour_day]['platforms'][task_platform]['logins'][nlogin], eq_sum_dict, sum_em_whs_time)
                                    task_day['completion_dates'][hour_day]['platforms'][task_platform]['logins'][nlogin]['all'].append(wo_id)
                                    if nlogin not in task_day['month_completion_dates'][hour_month]['platforms'][task_platform]['logins'].keys():
                                        task_day['month_completion_dates'][hour_month]['platforms'][task_platform]['logins'][nlogin] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0}
                                        task_day['month_completion_dates'][hour_month]['platforms'][task_platform]['logins'][nlogin], sum_em_eqs_time = sum_em_eqs(task_day['month_completion_dates'][hour_month]['platforms'][task_platform]['logins'][nlogin], eq_sum_dict, sum_em_whs_time)
                                    task_day['month_completion_dates'][hour_month]['platforms'][task_platform]['logins'][nlogin]['all'].append(wo_id)
                                    if nlogin not in task_day['month_completion_dates'][hour_month]['logins'].keys():
                                        task_day['month_completion_dates'][hour_month]['logins'][nlogin] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0}
                                        task_day['month_completion_dates'][hour_month]['logins'][nlogin], sum_em_eqs_time = sum_em_eqs(task_day['month_completion_dates'][hour_month]['logins'][nlogin], eq_sum_dict, sum_em_whs_time)
                                    task_day['month_completion_dates'][hour_month]['logins'][nlogin]['all'].append(wo_id)
                                    if nlogin not in task_day['completion_dates'][hour_day]['clients'][client_code]['logins'].keys():
                                        task_day['completion_dates'][hour_day]['clients'][client_code]['logins'][nlogin] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0}
                                        task_day['completion_dates'][hour_day]['clients'][client_code]['logins'][nlogin], sum_em_eqs_time = sum_em_eqs(task_day['completion_dates'][hour_day]['clients'][client_code]['logins'][nlogin], eq_sum_dict, sum_em_whs_time)
                                    task_day['completion_dates'][hour_day]['clients'][client_code]['logins'][nlogin]['all'].append(wo_id)
                                    if nlogin not in task_day['month_completion_dates'][hour_month]['clients'][client_code]['logins'].keys():
                                        task_day['month_completion_dates'][hour_month]['clients'][client_code]['logins'][nlogin] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0}
                                        task_day['month_completion_dates'][hour_month]['clients'][client_code]['logins'][nlogin], sum_em_eqs_time = sum_em_eqs(task_day['month_completion_dates'][hour_month]['clients'][client_code]['logins'][nlogin], eq_sum_dict, sum_em_whs_time)
                                    task_day['month_completion_dates'][hour_month]['clients'][client_code]['logins'][nlogin]['all'].append(wo_id)

                                task_day['completion_dates'][hour_day], sum_em_whs_time = sum_em_whs(task_day['completion_dates'][hour_day], send_dict, sum_em_whs_time)
                                task_day['completion_dates'][hour_day]['clients'][client_code], sum_em_whs_time = sum_em_whs(task_day['completion_dates'][hour_day]['clients'][client_code], send_dict, sum_em_whs_time)
                                task_day['completion_dates'][hour_day]['platforms'][task_platform], sum_em_whs_time = sum_em_whs(task_day['completion_dates'][hour_day]['platforms'][task_platform], send_dict, sum_em_whs_time)
                                task_day['month_completion_dates'][hour_month], sum_em_whs_time = sum_em_whs(task_day['month_completion_dates'][hour_month], send_dict, sum_em_whs_time)
                                task_day['month_completion_dates'][hour_month]['clients'][client_code], sum_em_whs_time = sum_em_whs(task_day['month_completion_dates'][hour_month]['clients'][client_code], send_dict, sum_em_whs_time)
                                task_day['month_completion_dates'][hour_month]['platforms'][task_platform], sum_em_whs_time = sum_em_whs(task_day['month_completion_dates'][hour_month]['platforms'][task_platform], send_dict, sum_em_whs_time)
                                for ngroup in ngroups.keys():
                                    task_day['completion_dates'][hour_day]['clients'][client_code]['groups'][ngroup], sum_em_whs_time = sum_em_whs(task_day['completion_dates'][hour_day]['clients'][client_code]['groups'][ngroup], ngroups[ngroup], sum_em_whs_time)
                                    task_day['completion_dates'][hour_day]['groups'][ngroup], sum_em_whs_time = sum_em_whs(task_day['completion_dates'][hour_day]['groups'][ngroup], ngroups[ngroup], sum_em_whs_time)
                                    task_day['completion_dates'][hour_day]['platforms'][task_platform]['groups'][ngroup], sum_em_whs_time = sum_em_whs(task_day['completion_dates'][hour_day]['platforms'][task_platform]['groups'][ngroup], ngroups[ngroup], sum_em_whs_time)
                                    task_day['completion_dates'][hour_day]['groups'][ngroup], sum_em_whs_time = sum_em_whs(task_day['completion_dates'][hour_day]['groups'][ngroup], ngroups[ngroup], sum_em_whs_time)
                                    task_day['month_completion_dates'][hour_month]['clients'][client_code]['groups'][ngroup], sum_em_whs_time = sum_em_whs(task_day['month_completion_dates'][hour_month]['clients'][client_code]['groups'][ngroup], ngroups[ngroup], sum_em_whs_time)
                                    task_day['month_completion_dates'][hour_month]['platforms'][task_platform]['groups'][ngroup], sum_em_whs_time = sum_em_whs(task_day['month_completion_dates'][hour_month]['platforms'][task_platform]['groups'][ngroup], ngroups[ngroup], sum_em_whs_time)
                                    for nlogin in nlogins.keys():
                                        if ngroup == login_report[nlogin]['default_group']:
                                            task_day['completion_dates'][hour_day]['groups'][ngroup]['logins'][nlogin], sum_em_whs_time = sum_em_whs(task_day['completion_dates'][hour_day]['groups'][ngroup]['logins'][nlogin], nlogins[nlogin], sum_em_whs_time)
                                            task_day['completion_dates'][hour_day]['clients'][client_code]['groups'][ngroup]['logins'][nlogin], sum_em_whs_time = sum_em_whs(task_day['completion_dates'][hour_day]['clients'][client_code]['groups'][ngroup]['logins'][nlogin], nlogins[nlogin], sum_em_whs_time)
                                            task_day['month_completion_dates'][hour_month]['groups'][ngroup]['logins'][nlogin], sum_em_whs_time = sum_em_whs(task_day['month_completion_dates'][hour_month]['groups'][ngroup]['logins'][nlogin], nlogins[nlogin], sum_em_whs_time)
                                            task_day['month_completion_dates'][hour_month]['clients'][client_code]['groups'][ngroup]['logins'][nlogin], sum_em_whs_time = sum_em_whs(task_day['month_completion_dates'][hour_month]['clients'][client_code]['groups'][ngroup]['logins'][nlogin], nlogins[nlogin], sum_em_whs_time)
                                for nlogin in nlogins.keys():
                                    task_day['completion_dates'][hour_day]['logins'][nlogin], sum_em_whs_time = sum_em_whs(task_day['completion_dates'][hour_day]['logins'][nlogin], nlogins[nlogin], sum_em_whs_time)
                                    task_day['completion_dates'][hour_day]['clients'][client_code]['logins'][nlogin], sum_em_whs_time = sum_em_whs(task_day['completion_dates'][hour_day]['clients'][client_code]['logins'][nlogin], nlogins[nlogin], sum_em_whs_time)
                                    task_day['completion_dates'][hour_day]['platforms'][task_platform]['logins'][nlogin], sum_em_whs_time = sum_em_whs(task_day['completion_dates'][hour_day]['platforms'][task_platform]['logins'][nlogin], nlogins[nlogin], sum_em_whs_time)
                                    task_day['month_completion_dates'][hour_month]['logins'][nlogin], sum_em_whs_time = sum_em_whs(task_day['month_completion_dates'][hour_month]['logins'][nlogin], nlogins[nlogin], sum_em_whs_time)
                                    task_day['month_completion_dates'][hour_month]['clients'][client_code]['logins'][nlogin], sum_em_whs_time = sum_em_whs(task_day['month_completion_dates'][hour_month]['clients'][client_code]['logins'][nlogin], nlogins[nlogin], sum_em_whs_time)
                                    task_day['month_completion_dates'][hour_month]['platforms'][task_platform]['logins'][nlogin], sum_em_whs_time = sum_em_whs(task_day['month_completion_dates'][hour_month]['platforms'][task_platform]['logins'][nlogin], nlogins[nlogin], sum_em_whs_time)
    print "SUM_EM_TIME = %s" % sum_em_time                    
    print "SUM_EM_EQS_TIME = %s" % sum_em_eqs_time                    
    print "SUM_EM_WHS_TIME = %s" % sum_em_whs_time                    
    print "MAIN BODY TIME = %s" % (time.time() - main_body_time)
#MTM UNATTACHED WHS HERE -- I DON'T THINK THIS IS FINISHED
    for login in logins.keys():
        try:
            other_whs = work_hours[login]
            for whd in other_whs:
                category = whd.get('category')
                client_code = whd.get('client_code')
                hour_day = whd.get('day').split(' ')[0]
                odms = hour_day.split('-')
                hour_month = '%s-%s' % (odms[0], odms[1])
                is_billable = whd.get('is_billable')
                login = whd.get('login')
                my_login_group = 'Not Set'
                if login not in ['','Nothing']:
                    my_login_group = login_report[login]['default_group']
                else:
                    login = 'Not Set'
                order_code = whd.get('order_code')
                scheduler = whd.get('scheduler')
                straight_time = float(whd.get('straight_time'))
                title_code = whd.get('title_code') 
                default_rate = 0.0
                if login in login_codes:
                    default_rate = make_number(login_report[login]['default_rate'])
                total_hours = straight_time 
                billable_hours = 0.0
                if is_billable not in [None,'','f',False]:
                    billable_hours = total_hours
                actual_cost = total_hours * default_rate
                billable_cost = billable_hours * default_rate        
                send_dict = {'total_hours': total_hours, 'estimated_work_hours': 0, 'billable_hours': billable_hours, 'actual_cost': actual_cost, 'estimated_cost': 0, 'billable_cost': billable_cost, 'code': ''}
                if client_code not in [None,'']:
                    if hour_day not in task_day['completion_dates'].keys(): 
                        task_day['completion_dates'][hour_day] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0, 'logins': {}, 'groups': {}, 'clients': {}, 'platforms': {}}
                    task_day['completion_dates'][hour_day], sum_em_whs_time = sum_em_whs(task_day['completion_dates'][hour_day], send_dict, sum_em_whs_time)
                    if client_code not in task_day['completion_dates'][hour_day]['clients'].keys():
                        task_day['completion_dates'][hour_day]['clients'][client_code] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0, 'logins': {}, 'groups': {}}
                    task_day['completion_dates'][hour_day]['clients'][client_code], sum_em_whs_time = sum_em_whs(task_day['completion_dates'][hour_day]['clients'][client_code], send_dict, sum_em_whs_time)
                    if my_login_group not in task_day['completion_dates'][hour_day]['groups'].keys():
                        task_day['completion_dates'][hour_day]['groups'][my_login_group] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0, 'logins': {}}
                        
                    if hour_month not in task_day['month_completion_dates'].keys():
                        task_day['month_completion_dates'][hour_month] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0, 'logins': {}, 'groups': {}, 'clients': {}, 'platforms': {}}
                    task_day['month_completion_dates'][hour_month], sum_em_whs_time = sum_em_whs(task_day['month_completion_dates'][hour_month], send_dict, sum_em_whs_time)
                    if client_code not in task_day['month_completion_dates'][hour_month]['clients'].keys():
                        task_day['month_completion_dates'][hour_month]['clients'][client_code] = {'all': [], 'eq_actual_hours': 0.0, 'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0, 'logins': {}, 'groups': {}}
                    task_day['month_completion_dates'][hour_month]['clients'][client_code], sum_em_whs_time = sum_em_whs(task_day['month_completion_dates'][hour_month]['clients'][client_code], send_dict, sum_em_whs_time)
                    
                      
        except:
            pass
                
    errors_today = []
    error_type_counts = {}
    error_day = {'dates': {}, 'months': {}}
    #print 'WOS_LOOKUP KEYS = %s' % wos_lookup.keys()
    for production_error_code in production_error_codes: 
        pe = production_errors[production_error_code]
        timestamp = pe['timestamp']      
        error_type = pe['error_type']
        login = pe['operator_login']
        group = 'Not Set'
        if login not in ['','Nothing']:
            group = login_report[login]['default_group']
        else:
            login = 'Not Set'
        scheduler = pe['scheduler_login']
        wo_code = pe['work_order_code']
        wo = None
        #print 'WO CODE = %s' % wo_code
        if wo_code in wos_lookup.keys():
            wo = wos_lookup[wo_code]
            estimated_work_hours = make_number(wo['estimated_work_hours'])
            task_code = wo['task_code']
            title_code = pe['title_code']
            title = title_lookup[title_code]
    #MTM NEED TO MAKE BELOW PORTION LIVE AGAIN
            platform = title['platform']
            client_code = title['client_code']
            error_type = pe['error_type']
            eqs = []
            #Eq Stuff
            try:
               eqs = equipment[wo_code]
            except:
                pass
            eq_sum_dict = {'actual_duration': 0.0, 'expected_duration': 0.0, 'actual_cost': 0.0, 'expected_cost': 0.0}
            for eq in eqs:
                eq_code = eq['code']
                actual_duration = make_number(eq['actual_duration'])
                expected_duration = make_number(eq['expected_duration'])
                actual_cost = make_number(eq['actual_cost'])
                expected_cost = make_number(eq['expected_cost'])
                eq_sum_dict['actual_duration'] = eq_sum_dict['actual_duration'] + actual_duration
                eq_sum_dict['expected_duration'] = eq_sum_dict['expected_duration'] + expected_duration
                eq_sum_dict['actual_cost'] = eq_sum_dict['actual_cost'] + actual_cost
                eq_sum_dict['expected_cost'] = eq_sum_dict['expected_cost'] + expected_cost
    
            whs = []
            wh_sum_dict =  {'total_hours': 0.0, 'estimated_work_hours': 0.0, 'billable_hours': 0.0, 'actual_cost': 0.0, 'estimated_cost': 0.0, 'billable_cost': 0.0, 'code': wo_code}
            try:
                whs = work_hours[task_code]
            except:
                pass
            pelogins = {}
            pegroups = {}
            for wh in whs:
                wh_code = wh['code']
                is_billable = wh['is_billable']
                straight_time = make_number(wh['straight_time'])
                wlogin = wh['login']
                wgroup = login_report[wlogin]['default_group'] 
                default_rate = 0.0
                if wlogin in login_codes:
                    default_rate = make_number(login_report[wlogin]['default_rate'])
                total_hours = straight_time 
                billable_hours = 0.0
                if is_billable not in [None,'','f',False]:
                    billable_hours = total_hours
                actual_cost = total_hours * default_rate
                estimated_cost = estimated_work_hours * default_rate
                billable_cost = billable_hours * default_rate        
                if wh_sum_dict['estimated_work_hours'] in [0,0.0]:
                    wh_sum_dict['estimated_work_hours'] = wh_sum_dict['estimated_work_hours'] + estimated_work_hours
                if wh_sum_dict['estimated_cost'] in [0,0.0]:
                    wh_sum_dict['estimated_cost'] = wh_sum_dict['estimated_cost'] + estimated_cost
                wh_sum_dict['total_hours'] = wh_sum_dict['total_hours'] + straight_time
                wh_sum_dict['billable_hours'] = wh_sum_dict['billable_hours'] + billable_hours
                wh_sum_dict['actual_cost'] = wh_sum_dict['actual_cost'] + actual_cost
                wh_sum_dict['billable_cost'] = wh_sum_dict['billable_cost'] + billable_cost
                if wlogin not in pelogins.keys():
                    pelogins[wlogin] = {'total_hours': 0.0, 'estimated_work_hours': estimated_work_hours, 'billable_hours': 0.0, 'actual_cost': 0.0, 'estimated_cost': estimated_cost, 'billable_cost': 0.0, 'code': wo_code} 
                if wgroup not in pegroups.keys():
                    pegroups[wgroup] = {'total_hours': 0.0, 'estimated_work_hours': estimated_work_hours, 'billable_hours': 0.0, 'actual_cost': 0.0, 'estimated_cost': estimated_cost, 'billable_cost': 0.0, 'code': wo_code} 
                pelogins[wlogin]['total_hours'] = pelogins[wlogin]['total_hours'] + total_hours
                pelogins[wlogin]['billable_hours'] = pelogins[wlogin]['billable_hours'] + billable_hours
                pelogins[wlogin]['actual_cost'] = pelogins[wlogin]['actual_cost'] + actual_cost
                pelogins[wlogin]['billable_cost'] = pelogins[wlogin]['billable_cost'] + billable_cost
                pegroups[wgroup]['total_hours'] = pegroups[wgroup]['total_hours'] + total_hours
                pegroups[wgroup]['billable_hours'] = pegroups[wgroup]['billable_hours'] + billable_hours
                pegroups[wgroup]['actual_cost'] = pegroups[wgroup]['actual_cost'] + actual_cost
                pegroups[wgroup]['billable_cost'] = pegroups[wgroup]['billable_cost'] + billable_cost
                #Need to be able to split these hours into login and group as well
    #MTM NEED TO MAKE ABOVE PORTION LIVE AGAIN
            ## MTM YOU STOPPED HERE 9/16/2013
            # Need to add hours for work and equipment and add to the dictionaries below.
            # Work hour and eq data might be doubled, so you'll have to fix that
            ts_day = timestamp.split(' ')[0]
            ts_month_s = ts_day.split('-')
            ts_month = '%s-%s' % (ts_month_s[0], ts_month_s[1])
            if ts_day == current_day:
                errors_today.append(production_error_code)
                if error_type not in error_type_counts.keys():
                    error_type_counts[error_type] = []
                error_type_counts[error_type].append(production_error_code)
    #MTM NEED TO MAKE THIS PORTION LIVE AGAIN
            if ts_day not in error_day['dates'].keys():
                error_day['dates'][ts_day] = {'all': [], 'time_spent': 0.0, 'eq_actual_hours': 0.0,  'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0, 'logins': {}, 'groups': {}, 'clients': {}, 'platforms': {}, 'schedulers': {}, 'error_type': {}}
            for pelogin in pelogins.keys():
                if pelogin not in error_day['dates'][ts_day]['logins'].keys():
                    error_day['dates'][ts_day]['logins'][pelogin] = {'all': [], 'time_spent': 0.0, 'eq_actual_hours': 0.0,  'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0}
            for pegroup in pegroups.keys():
                if pegroup not in error_day['dates'][ts_day]['groups'].keys():
                    error_day['dates'][ts_day]['groups'][pegroup] = {'all': [], 'time_spent': 0.0, 'eq_actual_hours': 0.0,  'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0}
            if error_type not in error_day['dates'][ts_day]['error_type'].keys():
                error_day['dates'][ts_day]['error_type'][error_type] = {'all': [], 'time_spent': 0.0, 'eq_actual_hours': 0.0,  'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0}
            if client_code not in error_day['dates'][ts_day]['clients'].keys():
                error_day['dates'][ts_day]['clients'][client_code] = {'all': [], 'time_spent': 0.0, 'eq_actual_hours': 0.0,  'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0}
            if platform not in error_day['dates'][ts_day]['platforms'].keys():
                error_day['dates'][ts_day]['platforms'][platform] = {'all': [], 'time_spent': 0.0, 'eq_actual_hours': 0.0,  'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0}
            if ts_month not in error_day['months'].keys():
                error_day['months'][ts_month] = {'all': [], 'time_spent': 0.0, 'eq_actual_hours': 0.0,  'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0, 'logins': {}, 'groups': {}, 'clients': {}, 'platforms': {}, 'schedulers': {}, 'error_type': {}}
            for pelogin in pelogins.keys():
                if pelogin not in error_day['months'][ts_month]['logins'].keys():
                    error_day['months'][ts_month]['logins'][pelogin] = {'all': [], 'time_spent': 0.0, 'eq_actual_hours': 0.0,  'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0}
            for pegroup in pegroups.keys():
                if pegroup not in error_day['months'][ts_month]['groups'].keys():
                    error_day['months'][ts_month]['groups'][pegroup] = {'all': [], 'time_spent': 0.0, 'eq_actual_hours': 0.0,  'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0}
            if error_type not in error_day['months'][ts_month]['error_type'].keys():
                error_day['months'][ts_month]['error_type'][error_type] = {'all': [], 'time_spent': 0.0, 'eq_actual_hours': 0.0,  'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0}
            if client_code not in error_day['months'][ts_month]['clients'].keys():
                error_day['months'][ts_month]['clients'][client_code] = {'all': [], 'time_spent': 0.0, 'eq_actual_hours': 0.0,  'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0}
            if platform not in error_day['months'][ts_month]['platforms'].keys():
                error_day['months'][ts_month]['platforms'][platform] = {'all': [], 'time_spent': 0.0, 'eq_actual_hours': 0.0,  'eq_expected_hours': 0.0, 'eq_actual_cost': 0.0, 'eq_expected_cost': 0.0, 'wh_total_hours': 0.0, 'wh_billable_hours': 0.0, 'estimated_work_hours': 0.0, 'wh_actual_cost': 0.0, 'wh_estimated_cost': 0.0, 'wh_billable_cost': 0.0}
    #MTM NEED TO MAKE ABOVE PORTION LIVE AGAIN
            error_day['dates'][ts_day], sum_em_whs_time = sum_em_whs(error_day['dates'][ts_day], wh_sum_dict, sum_em_whs_time)
            error_day['dates'][ts_day], sum_em_eqs_time = sum_em_eqs(error_day['dates'][ts_day], eq_sum_dict, sum_em_whs_time)
            error_day['dates'][ts_day]['error_type'][error_type], sum_em_whs_time = sum_em_whs(error_day['dates'][ts_day]['error_type'][error_type], wh_sum_dict, sum_em_whs_time)
            error_day['dates'][ts_day]['error_type'][error_type], sum_em_eqs_time = sum_em_eqs(error_day['dates'][ts_day]['error_type'][error_type], eq_sum_dict, sum_em_whs_time)
            error_day['dates'][ts_day]['clients'][client_code], sum_em_whs_time = sum_em_whs(error_day['dates'][ts_day]['clients'][client_code], wh_sum_dict, sum_em_whs_time)
            error_day['dates'][ts_day]['clients'][client_code], sum_em_eqs_time = sum_em_eqs(error_day['dates'][ts_day]['clients'][client_code], eq_sum_dict, sum_em_whs_time)
            error_day['dates'][ts_day]['platforms'][platform], sum_em_whs_time = sum_em_whs(error_day['dates'][ts_day]['platforms'][platform], wh_sum_dict, sum_em_whs_time)
            error_day['dates'][ts_day]['platforms'][platform], sum_em_eqs_time = sum_em_eqs(error_day['dates'][ts_day]['platforms'][platform], eq_sum_dict, sum_em_whs_time)
            error_day['months'][ts_month], sum_em_whs_time = sum_em_whs(error_day['months'][ts_month], wh_sum_dict, sum_em_whs_time)
            error_day['months'][ts_month], sum_em_eqs_time = sum_em_eqs(error_day['months'][ts_month], eq_sum_dict, sum_em_whs_time)
            error_day['months'][ts_month]['error_type'][error_type], sum_em_whs_time = sum_em_whs(error_day['months'][ts_month]['error_type'][error_type], wh_sum_dict, sum_em_whs_time)
            error_day['months'][ts_month]['error_type'][error_type], sum_em_eqs_time = sum_em_eqs(error_day['months'][ts_month]['error_type'][error_type], eq_sum_dict, sum_em_whs_time)
            error_day['months'][ts_month]['clients'][client_code], sum_em_whs_time = sum_em_whs(error_day['months'][ts_month]['clients'][client_code], wh_sum_dict, sum_em_whs_time)
            error_day['months'][ts_month]['clients'][client_code], sum_em_eqs_time = sum_em_eqs(error_day['months'][ts_month]['clients'][client_code], eq_sum_dict, sum_em_whs_time)
            error_day['months'][ts_month]['platforms'][platform], sum_em_whs_time = sum_em_whs(error_day['months'][ts_month]['platforms'][platform], wh_sum_dict, sum_em_whs_time)
            error_day['months'][ts_month]['platforms'][platform], sum_em_eqs_time = sum_em_eqs(error_day['months'][ts_month]['platforms'][platform], eq_sum_dict, sum_em_whs_time)
            for pelogin in pelogins.keys():
                error_day['dates'][ts_day]['logins'][pelogin], sum_em_whs_time = sum_em_whs(error_day['dates'][ts_day]['logins'][pelogin], pelogins[pelogin], sum_em_whs_time)
                error_day['dates'][ts_day]['logins'][pelogin], sum_em_eqs_time = sum_em_eqs(error_day['dates'][ts_day]['logins'][pelogin], eq_sum_dict, sum_em_whs_time)
                error_day['months'][ts_month]['logins'][pelogin], sum_em_whs_time = sum_em_whs(error_day['months'][ts_month]['logins'][pelogin], pelogins[pelogin], sum_em_whs_time)
                error_day['months'][ts_month]['logins'][pelogin], sum_em_eqs_time = sum_em_eqs(error_day['months'][ts_month]['logins'][pelogin], eq_sum_dict, sum_em_whs_time)
            for pegroup in pegroups.keys():
                error_day['dates'][ts_day]['groups'][pegroup], sum_em_whs_time = sum_em_whs(error_day['dates'][ts_day]['groups'][pegroup], pegroups[pegroup], sum_em_whs_time)
                error_day['dates'][ts_day]['groups'][pegroup], sum_em_eqs_time = sum_em_eqs(error_day['dates'][ts_day]['groups'][pegroup], eq_sum_dict, sum_em_whs_time)
                error_day['months'][ts_month]['groups'][pegroup], sum_em_whs_time = sum_em_whs(error_day['months'][ts_month]['groups'][pegroup], pegroups[pegroup], sum_em_whs_time)
                error_day['months'][ts_month]['groups'][pegroup], sum_em_eqs_time = sum_em_eqs(error_day['months'][ts_month]['groups'][pegroup], eq_sum_dict, sum_em_whs_time)


#NEED TO PRINT OUT THE ERROR DAY LINES AND SLAM THEM INTO THE DB


    orders_completed_yesterday = '' 
    orders_completed_yesterday_len = 0
    if yesterday in order_days['completion_dates'].keys():
        orders_completed_yesterday = order_days['completion_dates'][yesterday]['order_codes']
        orders_completed_yesterday_len = len(orders_completed_yesterday.split(','))
    orders_due_tomorrow = ''
    orders_due_tomorrow_len = 0
    if tomorrow in order_days['due_dates'].keys():
        orders_due_tomorrow = order_days['due_dates'][tomorrow]['order_codes']
        orders_due_tomorrow_len = len(orders_due_tomorrow.split(','))

    #print "DUE DATE CLASSIFICATIONS"
    orders_due_today = ''
    orders_due_today_len = 0
    order_due_classifications = {}
    if current_day in order_days['due_dates'].keys():    
        orders_due_today = order_days['due_dates'][current_day]['order_codes']
        orders_due_today_len = len(orders_due_today.split(','))
        cls_dict = order_days['due_dates'][current_day]['by_classification']
        for clss in cls_dict.keys():
            if clss not in order_due_classifications.keys():
                order_due_classifications[clss] = {'count': len(cls_dict[clss]['order_codes'].split(',')), 'order_codes': cls_dict[clss]['order_codes']} 

    order_past_due = ''
    order_past_due_len = 0
    if 'late' in order_days.keys():
        order_past_due = order_days['late']['order_codes']
        order_past_due_len = len(order_past_due.split(',')) 

    orders_future = ''
    orders_future_len = 0
    if 'future' in order_days.keys():
        orders_future = order_days['future']['order_codes']
        orders_future_len = len(orders_future.split(','))

    orders_no_due_date = ','.join(orders_no_due)
    orders_no_due_date_len = len(orders_no_due)
    
    #print "DOING MONTH COMPLETION DATES"
    last_month_completion = {}
    last_month_completion_len = 0
    this_month_completion = {}
    this_month_completion_len = 0
    next_month_completion = {}
    next_month_completion_len = 0
    if 'month_completion_dates' in order_days.keys():
        if last_month in order_days['month_completion_dates'].keys():
            last_month_completion = order_days['month_completion_dates'][last_month]
            last_month_completion_len = len(last_month_completion['order_codes'].split(','))
        if this_month in order_days['month_completion_dates'].keys():
            this_month_completion = order_days['month_completion_dates'][this_month]
            this_month_completion_len = len(this_month_completion['order_codes'].split(','))
        if next_month in order_days['month_completion_dates'].keys():
            next_month_completion = order_days['month_completion_dates'][next_month]
            next_month_completion_len = len(next_month_completion['order_codes'].split(','))

    #print "DOING MONTH DUE DATES"
    last_month_due = {}
    last_month_due_len = 0
    this_month_due = {}
    this_month_due_len = 0
    next_month_due = {}
    next_month_due_len = 0
    if 'month_due_dates' in order_days.keys():
        if last_month in order_days['month_due_dates'].keys():
            last_month_due = order_days['month_due_dates'][last_month]
            last_month_due_len = len(last_month_due['order_codes'].split(','))
        if this_month in order_days['month_due_dates'].keys():
            this_month_due = order_days['month_due_dates'][this_month]
            this_month_due_len = len(this_month_due['order_codes'].split(','))
        if next_month in order_days['month_due_dates'].keys():
            next_month_due = order_days['month_due_dates'][next_month]
            next_month_due_len = len(next_month_due['order_codes'].split(','))
     
    #print "DOING TITLES"
    titles_due_today = ','.join(titles_due) 
    titles_due_today_len = len(titles_due)
    titles_no_due_date = ','.join(titles_no_due)
    titles_no_due_date_len = len(titles_no_due)
    title_past_due_len = len(titles_late)
    title_past_due = ','.join(titles_late)
    titles_due_in_future_len = 0
    titles_due_in_future = ''
    titles_due_tomorrow = ''
    titles_due_tomorrow_len = 0
    titles_completed_yesterday = ','.join(title_completed_yesterday)
    titles_completed_yesterday_len = len(title_completed_yesterday)
    for ft in future_titles.keys():
        if titles_due_in_future == '':
            titles_due_in_future = ','.join(future_titles[ft])
        else:
            titles_due_in_future = '%s,%s' % (titles_due_in_future, ','.join(future_titles[ft]))
        if ft == tomorrow:
            if titles_due_tomorrow == '':
                titles_due_tomorrow = ','.join(future_titles[ft])
            else:
                titles_due_tomorrow = '%s,%s' % (titles_due_tomorrow, ','.join(future_titles[ft]))
    titles_due_in_future_len = len(titles_due_in_future.split(','))
    titles_due_tomorrow_len = len(titles_due_tomorrow.split(','))
    
    #print "DOING WO DUE DATES"
    wo_due_today = '' 
    wo_due_today_len = 0
    if current_day in task_day['due_dates'].keys():
        wo_due_today = ','.join(task_day['due_dates'][current_day]['all'])
        wo_due_today_len = len(wo_due_today.split(','))

    wo_due_tomorrow = '' 
    wo_due_tomorrow_len = 0
    if tomorrow in task_day['due_dates'].keys():
        wo_due_tomorrow = ','.join(task_day['due_dates'][tomorrow]['all'])
        wo_due_tomorrow_len = len(wo_due_tomorrow.split(','))

    wo_completed_yesterday = '' 
    wo_completed_yesterday_len = 0
    if yesterday in task_day['completion_dates'].keys():
        wo_completed_yesterday = ','.join(task_day['completion_dates'][yesterday]['all'])
        wo_completed_yesterday_len = len(wo_completed_yesterday.split(','))
    
    wo_due_in_future = ''
    wo_due_in_future_len = 0
    for ft in future_tasks.keys(): 
        if wo_due_in_future == '':
            wo_due_in_future = ','.join(future_tasks[ft])
        else:
            wo_due_in_future = '%s,%s' % (wo_due_in_future, ','.join(future_tasks[ft]))
    wo_due_in_future_len = len(wo_due_in_future.split(','))

    wo_past_due_len = len(tasks_late)
    wo_past_due = ','.join(tasks_late)
        
    wo_no_due_date = ','.join(tasks_no_due)
    wo_no_due_date_len = len(tasks_no_due)
    
    #print "DOING TASK MONTH COMPLETION"
    tlast_month_completion = {}
    tlast_month_completion_len = 0
    tthis_month_completion = {}
    tthis_month_completion_len = 0
    tnext_month_completion = {}
    tnext_month_completion_len = 0
    if 'month_completion_dates' in task_day.keys():
        if last_month in task_day['month_completion_dates'].keys():
            tlast_month_completion = task_day['month_completion_dates'][last_month]
            if 'all' in tlast_month_completion.keys() and tlast_month_completion['all'] not in [None,'']:
                tlast_month_completion_len = len(tlast_month_completion['all'])
        if this_month in task_day['month_completion_dates'].keys():
            tthis_month_completion = task_day['month_completion_dates'][this_month]
            if 'all' in tthis_month_completion.keys() and tthis_month_completion['all'] not in [None,'']:
                tthis_month_completion_len = len(tthis_month_completion['all'])
        if next_month in task_day['month_completion_dates'].keys():
            tnext_month_completion = task_day['month_completion_dates'][next_month]
            if 'all' in tnext_month_completion.keys() and tnext_month_completion['all'] not in [None,'']:
                tnext_month_completion_len = len(tnext_month_completion['all'])

    #print "DOING TASK MONTH DUE"
    tlast_month_due = {}
    tlast_month_due_len = 0
    tthis_month_due = {}
    tthis_month_due_len = 0
    tnext_month_due = {}
    tnext_month_due_len = 0
    if 'month_due_dates' in task_day.keys():
        if last_month in task_day['month_due_dates'].keys():
            tlast_month_due = task_day['month_due_dates'][last_month]
            if 'all' in tlast_month_due.keys() and tlast_month_due['all'] not in [None,'']:
                tlast_month_due_len = len(tlast_month_due['all'])
        if this_month in task_day['month_due_dates'].keys():
            tthis_month_due = task_day['month_due_dates'][this_month]
            if 'all' in tthis_month_due.keys() and tthis_month_due['all'] not in [None,'']:
                tthis_month_due_len = len(tthis_month_due['all'])
        if next_month in task_day['month_due_dates'].keys():
            tnext_month_due = task_day['month_due_dates'][next_month]
            if 'all' in tnext_month_due.keys() and tnext_month_due['all'] not in [None,'']:
                tnext_month_due_len = len(tnext_month_due['all'])

    record_end_time = time.time()
    #print "RECORD_TIME = %s" % (record_end_time - record_begin_time)
    insert_order_begin_time = time.time()
    
    def insert_error_info(record, search_dict, new_err_id, client_lookup):
        eq_actual_hours = record['eq_actual_hours']
        eq_expected_hours = record['eq_expected_hours']
        eq_actual_cost = record['eq_actual_cost']
        eq_expected_cost = record['eq_expected_cost']
        wh_total_hours = record['wh_total_hours']
        wh_billable_hours = record['wh_billable_hours']
        wh_estimated_hours = record['estimated_work_hours']
        wh_actual_cost = record['wh_actual_cost']
        wh_estimated_cost = record['wh_estimated_cost']
        wh_billable_cost = record['wh_billable_cost']
        time_spent = record['time_spent']
        all = uniq(record['all'])
        
        wo_codes = ''
        if not isinstance(all, str) and all not in [None,'']:
            wo_codes = ','.join(record['all'])
        elif all in [None,'']:
            wo_codes = ''
        else:
            wo_codes = all
        client_name = ''
        if 'client_code' in search_dict.keys():
            client_code = search_dict['client_code']
            try:
                client_name = client_lookup[client_code]
            except:
                pass
        count = len(wo_codes.split(','))
        if 'date' not in search_dict.keys():
            search_dict['date'] = '2000-01-01'
        if 'client_code' not in search_dict.keys():
            search_dict['client_code'] = '-1'
        if 'platform' not in search_dict.keys():
            search_dict['platform'] = '-1'
        else:
            search_dict['platform'] = search_dict['platform'].replace('[','(').replace(']',')')
        if 'login_name' not in search_dict.keys():
            search_dict['login_name'] = '-1'
        if 'group' not in search_dict.keys():
            search_dict['group'] = '-1'
        if 'month' not in search_dict.keys():
            search_dict['month'] = '-1'
        if search_dict['date'] in [None,'']:
            search_dict['date'] = '1999-01-01' 
        insertion_dict =  {'date': '2000-01-01', 'client_code': '-1', 'platform': '-1', 'login_name': '-1', 'group': '-1', 'eq_actual_hours': eq_actual_hours, 'eq_expected_hours': eq_expected_hours, 'eq_actual_cost': eq_actual_cost, 'eq_expected_cost': eq_expected_cost, 'wh_total_hours': wh_total_hours, 'wh_billable_hours': wh_billable_hours, 'wh_estimated_hours': wh_estimated_hours, 'wh_actual_cost': wh_actual_cost, 'wh_estimated_cost': wh_estimated_cost, 'wh_billable_cost': wh_billable_cost, 'wo_codes': wo_codes, 'count': count, 'day': current_day, 'month': current_month, 'error_type': '-1', 'time_spent': time_spent, 'scheduler': '-1'}
        for k in search_dict.keys():
            insertion_dict[k] = search_dict[k]
        new_err_id = new_err_id + 1
        new_code = 'ERROR_REPORT%s' % make_code_digits(new_err_id)
        total_cost = insertion_dict['wh_actual_cost'] + insertion_dict['eq_actual_cost']
        billable_cost = insertion_dict['wh_billable_cost'] + insertion_dict['eq_actual_cost']
        estimated_cost = insertion_dict['wh_estimated_cost'] + insertion_dict['eq_expected_cost']
        insert_str = "insert into error_report values ('%s', '%s', %s,'%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',%s,%s,%s,%s);" % (new_code,'',new_err_id,wo_codes,insertion_dict['time_spent'],insertion_dict['eq_actual_hours'],insertion_dict['eq_expected_hours'],insertion_dict['eq_actual_cost'],insertion_dict['eq_expected_cost'],insertion_dict['wh_total_hours'],insertion_dict['wh_billable_hours'],insertion_dict['wh_estimated_hours'],insertion_dict['wh_actual_cost'],insertion_dict['wh_estimated_cost'],insertion_dict['wh_billable_cost'],insertion_dict['login_name'], insertion_dict['group'], insertion_dict['client_code'], client_name, insertion_dict['platform'], insertion_dict['scheduler'], insertion_dict['error_type'], insertion_dict['date'], insertion_dict['month'], current_day, current_month, insertion_dict['count'], total_cost, billable_cost, estimated_cost)
        return [new_err_id, insert_str]
       

    def insert_report_day_info(info_dict, new_rd_id):
        new_rd_id = new_rd_id + 1
        print "RD INFO DICT = %s" % info_dict
        new_code = 'REPORT_DAY%s' % make_code_digits(new_rd_id)
        insert_str = "insert into report_day values ('%s', '%s', '%s', %s,%s,'%s',%s,'%s',%s,'%s',%s,'%s',%s,'%s',%s,'%s',%s,%s,'%s',%s,'%s',%s,'%s',%s,'%s',%s,'%s',%s,'%s',%s,'%s',%s,'%s','%s','%s','%s',%s,'%s',%s,'%s',%s);" % (new_code,info_dict['timestamp'],'',new_rd_id,info_dict['order_completed_yesterday_count'], info_dict['order_completed_yesterday'], info_dict['order_due_today_count'], info_dict['order_due_today'], info_dict['order_due_in_future_count'], info_dict['order_due_in_future'], info_dict['order_no_due_date_count'], info_dict['order_no_due_date'], info_dict['title_due_today_count'], info_dict['title_due_today'], info_dict['title_due_in_future_count'], info_dict['title_due_in_future'], info_dict['title_no_due_date_count'], info_dict['title_completed_yesterday_count'], info_dict['title_completed_yesterday'], info_dict['wo_completed_yesterday_count'], info_dict['wo_completed_yesterday'], info_dict['wo_due_today_count'], info_dict['wo_due_today'], info_dict['wo_due_in_future_count'], info_dict['wo_due_in_future'], info_dict['wo_no_due_date_count'], info_dict['wo_no_due_date'], info_dict['order_due_tomorrow_count'], info_dict['order_due_tomorrow'], info_dict['title_due_tomorrow_count'], info_dict['title_due_tomorrow'], info_dict['wo_due_tomorrow_count'], info_dict['wo_due_tomorrow'], info_dict['day'], info_dict['title_no_due_date'], info_dict['order_past_due'], info_dict['order_past_due_count'], info_dict['title_past_due'], info_dict['title_past_due_count'], info_dict['wo_past_due'], info_dict['wo_past_due_count'])
        return [new_rd_id, insert_str]

    def insert_wo_info(record, search_dict, new_wor_id, client_lookup):
        eq_actual_hours = record['eq_actual_hours']
        eq_expected_hours = record['eq_expected_hours']
        eq_actual_cost = record['eq_actual_cost']
        eq_expected_cost = record['eq_expected_cost']
        wh_total_hours = record['wh_total_hours']
        wh_billable_hours = record['wh_billable_hours']
        wh_estimated_hours = record['estimated_work_hours']
        wh_actual_cost = record['wh_actual_cost']
        wh_estimated_cost = record['wh_estimated_cost']
        wh_billable_cost = record['wh_billable_cost']
        all = uniq(record['all'])
        wo_codes = ''
        if not isinstance(all, str) and all not in [None,'']:
            wo_codes = ','.join(record['all'])
        elif all in [None,'']:
            wo_codes = ''
        else:
            wo_codes = all
        client_name = ''
        if 'client_code' in search_dict.keys():
            client_code = search_dict['client_code']
            try:
                client_name = client_lookup[client_code]
            except:
                pass
        count = len(wo_codes.split(','))
        if 'status' not in search_dict.keys():
            search_dict['status'] = '-1'
        if 'due_date' not in search_dict.keys():
            search_dict['due_date'] = '2000-01-01' 
        if 'completion_date' not in search_dict.keys():
            search_dict['completion_date'] = '2000-01-01'
        if 'client_code' not in search_dict.keys():
            search_dict['client_code'] = '-1'
        if 'platform' not in search_dict.keys():
            search_dict['platform'] = '-1'
        else:
            search_dict['platform'] = search_dict['platform'].replace('[','(').replace(']',')')
        if 'login_name' not in search_dict.keys():
            search_dict['login_name'] = '-1'
        if 'group' not in search_dict.keys():
            search_dict['group'] = '-1'
        if 'month_completion_date' not in search_dict.keys():
            search_dict['month_completion_date'] = '-1'
        if 'month_due_date' not in search_dict.keys():
            search_dict['month_due_date'] = '-1'
        if search_dict['completion_date'] in [None,'']:
            search_dict['completion_date'] = '1999-01-01' # considering completion dates, but none set for these records
        if search_dict['due_date'] in [None,'']:
            search_dict['due_date'] = '1999-01-01'    # considering due dates, but none set for these records
        insertion_dict =  {'completion_date': '2000-01-01', 'due_date': '2000-01-01', 'client_code': '-1', 'platform': '-1', 'login_name': '-1', 'group': '-1', 'eq_actual_hours': eq_actual_hours, 'eq_expected_hours': eq_expected_hours, 'eq_actual_cost': eq_actual_cost, 'eq_expected_cost': eq_expected_cost, 'wh_total_hours': wh_total_hours, 'wh_billable_hours': wh_billable_hours, 'wh_estimated_hours': wh_estimated_hours, 'wh_actual_cost': wh_actual_cost, 'wh_estimated_cost': wh_estimated_cost, 'wh_billable_cost': wh_billable_cost, 'wo_codes': wo_codes, 'count': count, 'day': current_day, 'month': current_month, 'month_completion_date': '-1', 'month_due_date': '-1'}
        for k in search_dict.keys():
            insertion_dict[k] = search_dict[k]
        new_wor_id = new_wor_id + 1
        new_code = 'WO_REPORT%s' % make_code_digits(new_wor_id)
        total_cost = insertion_dict['wh_actual_cost'] + insertion_dict['eq_actual_cost']
        billable_cost = insertion_dict['wh_billable_cost'] + insertion_dict['eq_actual_cost']
        estimated_cost = insertion_dict['wh_estimated_cost'] + insertion_dict['eq_expected_cost']
        #HERE
        #print "IUT GROUP = %s, LOGIN = %s" % (insertion_dict['group'], insertion_dict['login_name'])
        insert_str = "insert into wo_report values ('%s', '%s', %s,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,'%s',%s,'%s',%s,%s,%s,%s);" % (new_code,'',new_wor_id,current_day,current_month,insertion_dict['client_code'],client_name,insertion_dict['due_date'],insertion_dict['completion_date'],insertion_dict['month_due_date'],insertion_dict['month_completion_date'],insertion_dict['login_name'],insertion_dict['group'],insertion_dict['status'],insertion_dict['eq_actual_hours'],insertion_dict['eq_expected_hours'],insertion_dict['eq_actual_cost'],insertion_dict['eq_expected_cost'],insertion_dict['wh_total_hours'],insertion_dict['wh_billable_hours'],insertion_dict['wh_estimated_hours'],insertion_dict['wh_estimated_cost'],insertion_dict['wh_billable_cost'],insertion_dict['wo_codes'],insertion_dict['count'],insertion_dict['platform'],insertion_dict['wh_actual_cost'], total_cost, billable_cost, estimated_cost)
        return [new_wor_id, insert_str]

    def insert_order_info(record, search_dict, new_id, client_lookup):
        eq_actual_hours = record['eq_actual_hours']
        eq_expected_hours = record['eq_expected_hours']
        eq_actual_cost = record['eq_actual_cost']
        eq_expected_cost = record['eq_expected_cost']
        wh_total_hours = record['wh_total_hours']
        wh_billable_hours = record['wh_billable_hours']
        wh_estimated_hours = record['estimated_work_hours']
        wh_actual_cost = record['wh_actual_cost']
        wh_estimated_cost = record['wh_estimated_cost']
        wh_billable_cost = record['wh_billable_cost']
        order_codes1 = record['order_codes']
        order_codes = uniq(order_codes1.split(','))
        count = len(order_codes)
        t_expected_cost = record['expected_cost']
        t_actual_cost = record['actual_cost']
        price = record['price']
        expected_price = record['expected_price']
        client_name = ''
        if 'client_code' in search_dict.keys():
            client_code = search_dict['client_code']
            try:
                client_name = client_lookup[client_code]
            except:
                pass
        if 'due_date' not in search_dict.keys():
            search_dict['due_date'] = '2000-01-01' 
        if 'completion_date' not in search_dict.keys():
            search_dict['completion_date'] = '2000-01-01'
        if 'billed_date' not in search_dict.keys():
            search_dict['billed_date'] = '2000-01-01'
        if 'billed' not in search_dict.keys():
            search_dict['billed'] = '-1'
        if 'classification' not in search_dict.keys():
            search_dict['classification'] = '-1'
        if 'client_code' not in search_dict.keys():
            search_dict['client_code'] = '-1'
        if 'platform' not in search_dict.keys():
            search_dict['platform'] = '-1'
        else:
            search_dict['platform'] = search_dict['platform'].replace('[','(').replace(']',')')
        if 'month_completion_date' not in search_dict.keys():
            search_dict['month_completion_date'] = '-1'
        if 'month_billed_date' not in search_dict.keys():
            search_dict['month_billed_date'] = '-1'
        if 'month_due_date' not in search_dict.keys():
            search_dict['month_due_date'] = '-1'
        insertion_dict =  {'completion_date': '2000-01-01', 'billed_date': '2000-01-01', 'due_date': '2000-01-01','billed': '-1', 'classification': '-1', 'client_code': '-1', 'platform': '-1', 'eq_actual_hours': eq_actual_hours, 'eq_expected_hours': eq_expected_hours, 'eq_actual_cost': eq_actual_cost, 'eq_expected_cost': eq_expected_cost, 'wh_total_hours': wh_total_hours, 'wh_billable_hours': wh_billable_hours, 'wh_estimated_hours': wh_estimated_hours, 'wh_actual_cost': wh_actual_cost, 'wh_estimated_cost': wh_estimated_cost, 'wh_billable_cost': wh_billable_cost, 'order_codes': ','.join(order_codes), 'count': count, 't_expected_cost': t_expected_cost, 't_actual_cost': t_actual_cost, 'price': price, 'expected_price': expected_price, 'day': current_day, 'month': current_month, 'month_completion_date': '-1', 'month_billed_date': '-1', 'month_due_date': '-1'}
        for k in search_dict.keys():
            insertion_dict[k] = search_dict[k]
        new_id = new_id + 1
        new_code = 'ORDER_REPORT%s' % make_code_digits(new_id)
        total_cost = insertion_dict['wh_actual_cost'] + insertion_dict['eq_actual_cost']
        billable_cost = insertion_dict['wh_billable_cost'] + insertion_dict['eq_actual_cost']
        estimated_cost = insertion_dict['wh_estimated_cost'] + insertion_dict['eq_expected_cost']
       
        insert_str = "insert into order_report values ('%s', %s,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'%s',%s,%s,%s,%s,%s,'%s',%s,%s,%s,'%s','%s');" % ('',new_id,current_day,current_month,insertion_dict['client_code'],client_name,insertion_dict['due_date'],insertion_dict['completion_date'],insertion_dict['month_due_date'],insertion_dict['month_completion_date'],insertion_dict['classification'],insertion_dict['billed'],insertion_dict['platform'],insertion_dict['eq_actual_hours'],insertion_dict['eq_expected_hours'],insertion_dict['eq_actual_cost'],insertion_dict['eq_expected_cost'],insertion_dict['wh_total_hours'],insertion_dict['wh_billable_hours'],insertion_dict['wh_estimated_hours'],insertion_dict['wh_actual_cost'],insertion_dict['wh_billable_cost'],insertion_dict['wh_estimated_cost'],insertion_dict['order_codes'],insertion_dict['count'],insertion_dict['t_expected_cost'],insertion_dict['t_actual_cost'],insertion_dict['price'],insertion_dict['expected_price'], new_code, total_cost, billable_cost, estimated_cost, insertion_dict['billed_date'], insertion_dict['month_billed_date'])
        #try using the open and append to file function instead of os.system -- might speed things up
        #Do this by writing these lines to an array, then chucking them into order_report_insert
        #os.system('echo "%s" >> /opt/spt/custom/reports/dashboard_reports/order_report_insert' % (insert_str))
        #os.system('psql -U postgres twog < "%s;"' % insert_str)
        return [new_id, insert_str]


    rd_dict =   {'day': current_day, 'timestamp': current_time, 'order_completed_yesterday': orders_completed_yesterday,'order_completed_yesterday_count': orders_completed_yesterday_len,'order_due_in_future': orders_future,'order_due_in_future_count': orders_future_len,'order_due_today': orders_due_today,'order_due_today_count': orders_due_today_len,'order_due_tomorrow': orders_due_tomorrow,'order_due_tomorrow_count': orders_due_tomorrow_len,'order_no_due_date': orders_no_due_date,'order_no_due_date_count': orders_no_due_date_len,'title_completed_yesterday': titles_completed_yesterday,'title_completed_yesterday_count': titles_completed_yesterday_len,'title_due_in_future': titles_due_in_future,'title_due_in_future_count': titles_due_in_future_len,'title_due_today': titles_due_today,'title_due_today_count': titles_due_today_len,'title_due_tomorrow': titles_due_tomorrow,'title_due_tomorrow_count': titles_due_tomorrow_len,'title_no_due_date': titles_no_due_date,'title_no_due_date_count': titles_no_due_date_len,'wo_completed_yesterday': wo_completed_yesterday,'wo_completed_yesterday_count': wo_completed_yesterday_len,'wo_due_in_future': wo_due_in_future,'wo_due_in_future_count': wo_due_in_future_len,'wo_due_today': wo_due_today,'wo_due_today_count': wo_due_today_len,'wo_due_tomorrow': wo_due_tomorrow,'wo_due_tomorrow_count': wo_due_tomorrow_len,'wo_no_due_date': wo_no_due_date,'wo_no_due_date_count': wo_no_due_date_len, 'order_past_due': order_past_due, 'order_past_due_count': order_past_due_len, 'title_past_due': title_past_due, 'title_past_due_count': title_past_due_len, 'wo_past_due': wo_past_due, 'wo_past_due_count': wo_past_due_len}
    new_report_day_id, insert_str = insert_report_day_info(rd_dict, new_report_day_id) 
    report_day_string = insert_str
    
    ior = []
    new_id, insert_str =insert_order_info(order_days, {}, new_id, client_lookup)
    ior.append(insert_str)
    #print "OD COMPLETION MONTH"
    for completion_month in order_days['month_completion_dates'].keys():
        record = order_days['month_completion_dates'][completion_month]
        new_id, insert_str =insert_order_info(record, {'month_completion_date': completion_month}, new_id, client_lookup)
        ior.append(insert_str)
        for billed in record['by_billed'].keys():
            brecord = record['by_billed'][billed]
            new_id, insert_str =insert_order_info(brecord, {'month_completion_date': completion_month, 'billed': billed}, new_id, client_lookup)
            ior.append(insert_str)
    #print "OD COMPLETION DATE"
    for completion_day in order_days['completion_dates'].keys():
        record = order_days['completion_dates'][completion_day]
        new_id, insert_str =insert_order_info(record, {'completion_date': completion_day}, new_id, client_lookup)
        ior.append(insert_str)
        for billed in record['by_billed'].keys():
            brecord = record['by_billed'][billed]
            new_id, insert_str =insert_order_info(brecord, {'completion_date': completion_day, 'billed': billed}, new_id, client_lookup)
            ior.append(insert_str)
    #print "OD BILLED MONTH"
    for billed_month in order_days['month_billed_dates'].keys():
        record = order_days['month_billed_dates'][billed_month]
        new_id, insert_str =insert_order_info(record, {'month_billed_date': billed_month}, new_id, client_lookup)
        ior.append(insert_str)
        for billed in record['by_billed'].keys():
            brecord = record['by_billed'][billed]
            new_id, insert_str =insert_order_info(brecord, {'month_billed_date': billed_month, 'billed': billed}, new_id, client_lookup)
            ior.append(insert_str)
    #print "OD BILLED DATE"
    for billed_day in order_days['billed_dates'].keys():
        record = order_days['billed_dates'][billed_day]
        new_id, insert_str =insert_order_info(record, {'billed_date': billed_day}, new_id, client_lookup)
        ior.append(insert_str)
        for billed in record['by_billed'].keys():
            brecord = record['by_billed'][billed]
            new_id, insert_str =insert_order_info(brecord, {'billed_date': billed_day, 'billed': billed}, new_id, client_lookup)
            ior.append(insert_str)
    #print "OD DUE MONTH"
    for due_month in order_days['month_due_dates'].keys():
        record = order_days['month_due_dates'][due_month]
        new_id, insert_str =insert_order_info(record, {'month_due_date': due_month}, new_id, client_lookup)
        ior.append(insert_str)
        for billed in record['by_billed'].keys():
            brecord = record['by_billed'][billed]
            new_id, insert_str =insert_order_info(brecord, {'month_due_date': due_month, 'billed': billed}, new_id, client_lookup)
            ior.append(insert_str)
        for classification in record['by_classification'].keys():
            crecord = record['by_classification'][classification]
            new_id, insert_str =insert_order_info(crecord, {'month_due_date': due_month, 'classification': classification}, new_id, client_lookup)
            ior.append(insert_str)
    #print "OD DUE DATE"
    for due_day in order_days['due_dates'].keys():     
        record = order_days['due_dates'][due_day]
        new_id, insert_str =insert_order_info(record, {'due_date': due_day}, new_id, client_lookup)
        ior.append(insert_str)
        for billed in record['by_billed'].keys():
            brecord = record['by_billed'][billed]
            new_id, insert_str =insert_order_info(brecord, {'due_date': due_day, 'billed': billed}, new_id, client_lookup)
            ior.append(insert_str)
        for classification in record['by_classification'].keys():
            crecord = record['by_classification'][classification]
            new_id, insert_str =insert_order_info(crecord, {'due_date': due_day, 'classification': classification}, new_id, client_lookup)
            ior.append(insert_str)

    #print "OD CLASSIFICATION"
    for classification in order_days['by_classification'].keys():
        record = order_days['by_classification'][classification]
        new_id, insert_str =insert_order_info(record, {'classification': classification}, new_id, client_lookup)
        ior.append(insert_str)

    #print "OD BILLED"
    for billed in order_days['by_billed'].keys():
        record = order_days['by_billed'][billed]
        new_id, insert_str =insert_order_info(record, {'billed': billed}, new_id, client_lookup)
        ior.append(insert_str)

    #print "OC CLIENT CODE"
    for client_code in order_clients.keys():
        record = order_clients[client_code]
        new_id, insert_str =insert_order_info(record, {'client_code': client_code}, new_id, client_lookup)
        ior.append(insert_str)
        #print "OC CLIENT CODE BILLED"
        for billed in record['by_billed'].keys():
            brecord = record['by_billed'][billed]
            new_id, insert_str =insert_order_info(brecord, {'client_code': client_code, 'billed': billed}, new_id, client_lookup)
            ior.append(insert_str)
        #print "OC CLIENT CODE COMPLETION MONTH"
        for completion_month in record['month_completion_dates'].keys():
            cmrecord = record['month_completion_dates'][completion_month]
            new_id, insert_str =insert_order_info(cmrecord, {'month_completion_date': completion_month, 'client_code': client_code}, new_id, client_lookup)
            ior.append(insert_str)
            for billed in cmrecord['by_billed'].keys():
                bcmrecord = cmrecord['by_billed'][billed]
                new_id, insert_str =insert_order_info(bcmrecord, {'month_completion_date': completion_month, 'billed': billed, 'client_code': client_code}, new_id, client_lookup)
                ior.append(insert_str)
        #print "OC CLIENT CODE COMPLETION DAY"
        for completion_day in record['completion_dates'].keys():
            crecord = record['completion_dates'][completion_day]
            new_id, insert_str =insert_order_info(crecord, {'client_code': client_code, 'completion_date': completion_day}, new_id, client_lookup)
            ior.append(insert_str)
            for billed in crecord['by_billed'].keys():
                bcrecord = crecord['by_billed'][billed]
                new_id, insert_str =insert_order_info(bcrecord, {'completion_date': completion_day, 'billed': billed, 'client_code': client_code}, new_id, client_lookup)
                ior.append(insert_str)
        #print "OC CLIENT CODE BILLED MONTH"
        for billed_month in record['month_billed_dates'].keys():
            cmrecord = record['month_billed_dates'][billed_month]
            new_id, insert_str =insert_order_info(cmrecord, {'month_billed_date': billed_month, 'client_code': client_code}, new_id, client_lookup)
            ior.append(insert_str)
            for billed in cmrecord['by_billed'].keys():
                bcmrecord = cmrecord['by_billed'][billed]
                new_id, insert_str =insert_order_info(bcmrecord, {'month_billed_date': billed_month, 'billed': billed, 'client_code': client_code}, new_id, client_lookup)
                ior.append(insert_str)
        #print "OC CLIENT CODE BILLED DAY"
        for billed_day in record['billed_dates'].keys():
            crecord = record['billed_dates'][billed_day]
            new_id, insert_str =insert_order_info(crecord, {'client_code': client_code, 'billed_date': billed_day}, new_id, client_lookup)
            ior.append(insert_str)
            for billed in crecord['by_billed'].keys():
                bcrecord = crecord['by_billed'][billed]
                new_id, insert_str =insert_order_info(bcrecord, {'billed_date': billed_day, 'billed': billed, 'client_code': client_code}, new_id, client_lookup)
                ior.append(insert_str)
        #print "OC CLIENT DUE MONTH"
        for due_month in record['month_due_dates'].keys():
            dmrecord = record['month_due_dates'][due_month]
            new_id, insert_str =insert_order_info(dmrecord, {'month_due_date': due_month, 'client_code': client_code}, new_id, client_lookup)
            ior.append(insert_str)
            for billed in dmrecord['by_billed'].keys():
                bdmrecord = dmrecord['by_billed'][billed]
                new_id, insert_str =insert_order_info(bdmrecord, {'month_due_date': due_month, 'billed': billed}, new_id, client_lookup)
                ior.append(insert_str)
            for classification in dmrecord['by_classification'].keys():
                cdrecord = dmrecord['by_classification'][classification]
                new_id, insert_str =insert_order_info(cdrecord, {'client_code': client_code, 'month_due_date': due_month, 'classification': classification}, new_id, client_lookup)
                ior.append(insert_str)
        #print "OC CLIENT CODE DUE DAY"
        for due_day in record['due_dates'].keys():
            drecord = record['due_dates'][due_day]
            new_id, insert_str =insert_order_info(drecord, {'client_code': client_code, 'due_date': due_day}, new_id, client_lookup)
            ior.append(insert_str)
            #print "OC CLIENT CODE DUE DAY CLASSIFICATION"
            for classification in drecord['by_classification'].keys():
                cdrecord = drecord['by_classification'][classification]
                new_id, insert_str =insert_order_info(cdrecord, {'client_code': client_code, 'due_date': due_day, 'classification': classification}, new_id, client_lookup)
                ior.append(insert_str)
            #print "OC CLIENT CODE DUE DAY BILLED"
            for billed in drecord['by_billed'].keys():
                bdrecord = drecord['by_billed'][billed]
                new_id, insert_str =insert_order_info(bdrecord, {'client_code': client_code, 'due_date': due_day, 'billed': billed}, new_id, client_lookup)
                ior.append(insert_str)
    #print "OP PLATFORM"
    for platform in order_platforms.keys():
        record = order_platforms[platform]
        new_id, insert_str =insert_order_info(record, {'platform': platform}, new_id, client_lookup)
        ior.append(insert_str)
        #print "OP PLATFORM BILLED"
        for billed in record['by_billed'].keys():
            brecord = record['by_billed'][billed]
            new_id, insert_str =insert_order_info(brecord, {'platform': platform, 'billed': billed}, new_id, client_lookup)
            ior.append(insert_str)
        #print "OP PLATFORM COMPLETION DATES"
        for completion_day in record['completion_dates'].keys():
            crecord = record['completion_dates'][completion_day]
            new_id, insert_str =insert_order_info(crecord, {'platform': platform, 'completion_date': completion_day}, new_id, client_lookup)
            ior.append(insert_str)
        #print "OP PLATFORM BILLED DATES"
        for billed_day in record['billed_dates'].keys():
            crecord = record['billed_dates'][billed_day]
            new_id, insert_str =insert_order_info(crecord, {'platform': platform, 'billed_date': billed_day}, new_id, client_lookup)
            ior.append(insert_str)
        #print "OP PLATFORM DUE DATES"
        for due_day in record['due_dates'].keys():
            drecord = record['due_dates'][due_day]
            new_id, insert_str =insert_order_info(drecord, {'platform': platform, 'due_date': due_day}, new_id, client_lookup)
            ior.append(insert_str)
        #print "OP PLATFORM COMPLETION MONTHS"
        for completion_month in record['month_completion_dates'].keys():
            crecord = record['month_completion_dates'][completion_month]
            new_id, insert_str =insert_order_info(crecord, {'platform': platform, 'month_completion_date': completion_month}, new_id, client_lookup)
            ior.append(insert_str)
        #print "OP PLATFORM BILLED MONTHS"
        for billed_month in record['month_billed_dates'].keys():
            crecord = record['month_billed_dates'][billed_month]
            new_id, insert_str =insert_order_info(crecord, {'platform': platform, 'month_billed_date': billed_month}, new_id, client_lookup)
            ior.append(insert_str)
        #print "OP PLATFORM DUE MONTHS"
        for due_month in record['month_due_dates'].keys():
            drecord = record['month_due_dates'][due_month]
            new_id, insert_str =insert_order_info(drecord, {'platform': platform, 'month_due_date': due_month}, new_id, client_lookup)
            ior.append(insert_str)

    new_ior_file = '/opt/spt/custom/reports/dashboard_reports/order_report_insert'
    if os.path.exists(new_ior_file):
        os.system('rm -rf %s' % new_ior_file)
    new_guy = open(new_ior_file, 'w')
    for i in ior:
        new_guy.write('%s\n' % i)
    new_guy.close()
    print "MADE ORDER REPORT INSERT"

    order_days = None
    order_clients = None
    order_platforms = None

    insert_order_end_time = time.time()
    print "INSERT ORDER TIME = %s" % (insert_order_end_time - insert_order_begin_time)
    insert_wo_begin_time = time.time()
    #tasks
    iwr = []
    plat = []
    #print "TASK COMPLETION MONTH"
    #print "BEGIN CM IN TD"
    for completion_month in task_day['month_completion_dates'].keys():
        record = task_day['month_completion_dates'][completion_month]
        #print "MTMPOINT MCD"
        new_wor_id, insert_str = insert_wo_info(record, {'month_completion_date': completion_month}, new_wor_id, client_lookup)
        iwr.append(insert_str)
        #print "BEGIN CM IN TD LOGIN"
        for login in record['logins'].keys():
            lrecord = record['logins'][login]
            #print "MTMPOINT MCD LOGINS"
            new_wor_id, insert_str = insert_wo_info(lrecord, {'month_completion_date': completion_month, 'login_name': login}, new_wor_id, client_lookup)
            iwr.append(insert_str)
        #print "BEGIN CM IN TD GROUP"
        for group in record['groups'].keys():
            grecord = record['groups'][group]
            #print "MTMPOINT MCD GROUPS"
            new_wor_id, insert_str = insert_wo_info(grecord, {'month_completion_date': completion_month, 'group': group}, new_wor_id, client_lookup)
            iwr.append(insert_str)
            #print "BEGIN CM IN TD GROUP LOGIN"
            for login in grecord['logins'].keys():
                lgrecord = grecord['logins'][login]
                #print "MTMPOINT MCD GROUPS LOGINS"
                new_wor_id, insert_str = insert_wo_info(lgrecord, {'month_completion_date': completion_month, 'login_name': login, 'group': group}, new_wor_id, client_lookup)
                iwr.append(insert_str)
        #print "BEGIN CM IN TD CLIENT"
        for client_code in record['clients'].keys():
            crecord = record['clients'][client_code]
            #print "MTMPOINT MCD CLIENT"
            new_wor_id, insert_str = insert_wo_info(crecord, {'month_completion_date': completion_month, 'client_code': client_code}, new_wor_id, client_lookup)
            iwr.append(insert_str)
            for group in crecord['groups'].keys():
                cgrecord = crecord['groups'][group]
                #print "MTMPOINT MCD CLIENT GROUPS"
                new_wor_id, insert_str = insert_wo_info(cgrecord, {'month_completion_date': completion_month, 'client_code': client_code, 'group': group}, new_wor_id, client_lookup)
                iwr.append(insert_str)
                for login in cgrecord['logins'].keys():
                    clgrecord = cgrecord['logins'][login]
                    #print "MTMPOINT MCD CLIENT GROUPS LOGINS"
                    new_wor_id, insert_str = insert_wo_info(clgrecord, {'month_completion_date': completion_month, 'client_code': client_code, 'group': group, 'login_name': login}, new_wor_id, client_lookup)
                    iwr.append(insert_str)
            for login in crecord['logins'].keys():
                clrecord = crecord['logins'][login]
                #print "MTMPOINT MCD CLIENT LOGINS"
                new_wor_id, insert_str = insert_wo_info(clrecord, {'month_completion_date': completion_month, 'client_code': client_code, 'login_name': login}, new_wor_id, client_lookup)
                iwr.append(insert_str)
        ##print "BEGIN CM IN TD PLATFORM"
        if 'platforms' in record.keys():
            for platform in record['platforms'].keys():
                precord = record['platforms'][platform]
                #print "MTMPOINT MCD CLIENT PLATFORMS"
                new_wor_id, insert_str = insert_wo_info(precord, {'month_completion_date': completion_month, 'platform': platform}, new_wor_id, client_lookup)
                iwr.append(insert_str)
                for login in precord['logins'].keys():
                    lprecord = precord['logins'][login]
                    #print "MTMPOINT MCD CLIENT PLATFORMS LOGINS"
                    new_wor_id, insert_str = insert_wo_info(lprecord, {'month_completion_date': completion_month, 'platform': platform, 'login_name': login}, new_wor_id, client_lookup)
                    iwr.append(insert_str)
                for group in precord['groups'].keys():
                    gprecord = precord['groups'][group]
                    #print "MTMPOINT MCD CLIENT PLATFORMS GROUPS"
                    new_wor_id, insert_str = insert_wo_info(gprecord, {'month_completion_date': completion_month, 'platform': platform, 'group': group}, new_wor_id, client_lookup)
                    iwr.append(insert_str)
            
    #print "TASK COMPLETION DATES"
    #print "BEGIN CD IN TD"
    for completion_day in task_day['completion_dates'].keys():
        record = task_day['completion_dates'][completion_day]
        #print "MTMPOINT CD"
        new_wor_id, insert_str = insert_wo_info(record, {'completion_date': completion_day}, new_wor_id, client_lookup)
        iwr.append(insert_str)
        #print "BEGIN CD IN TD LOGIN"
        for login in record['logins'].keys():
            lrecord = record['logins'][login]
            #print "MTMPOINT CD LOGINS"
            new_wor_id, insert_str = insert_wo_info(lrecord, {'completion_date': completion_day, 'login_name': login}, new_wor_id, client_lookup)
            iwr.append(insert_str)
        #print "BEGIN CD IN TD GROUP"
        for group in record['groups'].keys():
            grecord = record['groups'][group]
            #print "MTMPOINT CD GROUPS"
            new_wor_id, insert_str = insert_wo_info(grecord, {'completion_date': completion_day, 'group': group}, new_wor_id, client_lookup)
            iwr.append(insert_str)
            #print "BEGIN CD IN TD GROUP LOGIN"
            for login in grecord['logins'].keys():
                lgrecord = grecord['logins'][login]
                #print "MTMPOINT CD GROUPS LOGINS"
                new_wor_id, insert_str = insert_wo_info(lgrecord, {'completion_date': completion_day, 'login_name': login, 'group': group}, new_wor_id, client_lookup)
                iwr.append(insert_str)
        #print "BEGIN CD IN TD CLIENT"
        for client_code in record['clients'].keys():
            crecord = record['clients'][client_code]
            #print "MTMPOINT CD CLIENT"
            new_wor_id, insert_str = insert_wo_info(crecord, {'completion_date': completion_day, 'client_code': client_code}, new_wor_id, client_lookup)
            iwr.append(insert_str)
            for group in crecord['groups'].keys():
                cgrecord = crecord['groups'][group]
                #print "MTMPOINT CD CLIENT GROUPS"
                new_wor_id, insert_str = insert_wo_info(cgrecord, {'completion_date': completion_day, 'client_code': client_code, 'group': group}, new_wor_id, client_lookup)
                iwr.append(insert_str)
                for login in cgrecord['logins'].keys():
                    clgrecord = cgrecord['logins'][login]
                    #print "MTMPOINT CD CLIENT GROUPS LOGINS"
                    new_wor_id, insert_str = insert_wo_info(clgrecord, {'completion_date': completion_day, 'client_code': client_code, 'group': group, 'login_name': login}, new_wor_id, client_lookup)
                    iwr.append(insert_str)
            for login in crecord['logins'].keys():
                clrecord = crecord['logins'][login]
                #print "MTMPOINT CD CLIENT LOGINS"
                new_wor_id, insert_str = insert_wo_info(clrecord, {'completion_date': completion_day, 'client_code': client_code, 'login_name': login}, new_wor_id, client_lookup)
                iwr.append(insert_str)
        #print "BEGIN CD IN TD PLATFORM"
        if 'platforms' in record.keys():
            for platform in record['platforms'].keys():
                precord = record['platforms'][platform]
                # THE PROBLEM is that the default platform entry is 0, and there exists also a platform of 0
                #print "MTMPOINT CD PLATFORMS"
                new_wor_id, insert_str = insert_wo_info(precord, {'completion_date': completion_day, 'platform': platform}, new_wor_id, client_lookup)
                iwr.append(insert_str)
                for login in precord['logins'].keys():
                    lprecord = precord['logins'][login]
                    #print "MTMPOINT CD PLATFORMS LOGINS"
                    new_wor_id, insert_str = insert_wo_info(lprecord, {'completion_date': completion_day, 'platform': platform, 'login_name': login}, new_wor_id, client_lookup)
                    iwr.append(insert_str)
                for group in precord['groups'].keys():
                    gprecord = precord['groups'][group]
                    #print "MTMPOINT CD PLATFORMS GROUPS"
                    new_wor_id, insert_str = insert_wo_info(gprecord, {'completion_date': completion_day, 'platform': platform, 'group': group}, new_wor_id, client_lookup)
                    iwr.append(insert_str)

    #print "TASK DUE MONTH"
    for due_month in task_day['month_due_dates'].keys():
        record = task_day['month_due_dates'][due_month]
        #print "MTMPOINT MDD"
        new_wor_id, insert_str = insert_wo_info(record, {'month_due_date': due_month}, new_wor_id, client_lookup)
        iwr.append(insert_str)
        for status in record['by_status'].keys():
            srecord = record['by_status'][status]
            #print "MTMPOINT MDD STATUS"
            new_wor_id, insert_str = insert_wo_info(srecord, {'month_due_date': due_month, 'status': status}, new_wor_id, client_lookup)
            iwr.append(insert_str)
        for platform in record['platforms'].keys():
            precord = record['platforms'][platform]
            #print "MTMPOINT MDD PLATFORMS"
            new_wor_id, insert_str = insert_wo_info(precord, {'month_due_date': due_month, 'platform': platform}, new_wor_id, client_lookup)
            iwr.append(insert_str)
        for client_code in record['clients'].keys():
            crecord = record['clients'][client_code]
            #print "MTMPOINT MDD CLIENT"
            new_wor_id, insert_str = insert_wo_info(crecord, {'month_due_date': due_month, 'client_code': client_code}, new_wor_id, client_lookup)
            iwr.append(insert_str)
            for group in crecord['groups'].keys():
                grecord = crecord['groups'][group]
                #print "MTMPOINT MDD CLIENT GROUPS"
                new_wor_id, insert_str = insert_wo_info(grecord, {'month_due_date': due_month, 'client_code': client_code, 'group': group}, new_wor_id, client_lookup)
                iwr.append(insert_str)
            for platform in crecord['platforms'].keys():
                precord = crecord['platforms'][platform]
                #print "MTMPOINT MDD CLIENT PLATFORMS"
                new_wor_id, insert_str = insert_wo_info(precord, {'month_due_date': due_month, 'client_code': client_code, 'platform': platform}, new_wor_id, client_lookup)
                iwr.append(insert_str)
        for group in record['groups'].keys():
            grecord = record['groups'][group]
            #print "MTMPOINT MDD GROUPS"
            new_wor_id, insert_str = insert_wo_info(grecord, {'month_due_date': due_month, 'group': group}, new_wor_id, client_lookup)
            iwr.append(insert_str)
            for status in grecord['by_status'].keys():
                srecord = grecord['by_status'][status]
                #print "MTMPOINT MDD GROUPS STATUS"
                new_wor_id, insert_str = insert_wo_info(srecord, {'month_due_date': due_month, 'group': group, 'status': status}, new_wor_id, client_lookup)
                iwr.append(insert_str)

    #print "TASK DUE DATES"
    for due_day in task_day['due_dates'].keys():     
        record = task_day['due_dates'][due_day]
        ##print "MTMPOINT DD"
        new_wor_id, insert_str = insert_wo_info(record, {'due_date': due_day}, new_wor_id, client_lookup)
        iwr.append(insert_str)
        for status in record['by_status'].keys():
            srecord = record['by_status'][status]
            #print "MTMPOINT DD STATUS"
            new_wor_id, insert_str = insert_wo_info(srecord, {'due_date': due_day, 'status': status}, new_wor_id, client_lookup)
            iwr.append(insert_str)
        for platform in record['platforms'].keys():
            precord = record['platforms'][platform]
            #print "MTMPOINT DD PLATFORM"
            new_wor_id, insert_str = insert_wo_info(precord, {'due_date': due_day, 'platform': platform}, new_wor_id, client_lookup)
            iwr.append(insert_str)
        for client_code in record['clients'].keys():
            crecord = record['clients'][client_code]
            #print "MTMPOINT DD CLIENT"
            new_wor_id, insert_str = insert_wo_info(crecord, {'due_date': due_day, 'client_code': client_code}, new_wor_id, client_lookup)
            iwr.append(insert_str)
            for group in crecord['groups'].keys():
                grecord = crecord['groups'][group]
                #print "MTMPOINT DD CLIENT GROUPS"
                new_wor_id, insert_str = insert_wo_info(grecord, {'due_date': due_day, 'client_code': client_code, 'group': group}, new_wor_id, client_lookup)
                iwr.append(insert_str)
            for platform in crecord['platforms'].keys():
                precord = crecord['platforms'][platform]
                #print "MTMPOINT DD CLIENT PLATFORMS"
                new_wor_id, insert_str = insert_wo_info(precord, {'due_date': due_day, 'client_code': client_code, 'platform': platform}, new_wor_id, client_lookup)
                iwr.append(insert_str)
        for group in record['groups'].keys():
            grecord = record['groups'][group]
            #print "MTMPOINT DD GROUPS"
            new_wor_id, insert_str = insert_wo_info(grecord, {'due_date': due_day, 'group': group}, new_wor_id, client_lookup)
            iwr.append(insert_str)
            for status in grecord['by_status'].keys():
                srecord = grecord['by_status'][status]
                #print "MTMPOINT DD GROUPS STATUS"
                new_wor_id, insert_str = insert_wo_info(srecord, {'due_date': due_day, 'group': group, 'status': status}, new_wor_id, client_lookup)
                iwr.append(insert_str)

    for client_code in task_day['clients'].keys():
        crecord = task_day['clients'][client_code]
        #print "MTMPOINT CC"
        new_wor_id, insert_str = insert_wo_info(crecord, {'client_code': client_code}, new_wor_id, client_lookup)
        iwr.append(insert_str)
        for due_day in crecord['due_dates'].keys():
            drecord = crecord['due_dates'][due_day]
            for status in drecord['by_status'].keys():
                dsrecord = drecord['by_status'][status]
                #print "MTMPOINT CC DD STATUS"
                new_wor_id, insert_str = insert_wo_info(dsrecord, {'client_code': client_code, 'due_date': due_day, 'status': status}, new_wor_id, client_lookup)
                iwr.append(insert_str)
            for group in drecord['groups'].keys():
                dgrecord = drecord['groups'][group]
                for status in dgrecord['by_status'].keys():
                    dgsrecord = dgrecord['by_status'][status]
                    #print "MTMPOINT CC DD STATUS GROUP"
                    new_wor_id, insert_str = insert_wo_info(dgsrecord, {'client_code': client_code, 'due_date': due_day, 'group': group, 'status': status}, new_wor_id, client_lookup)
                    iwr.append(insert_str)

    for platform in task_day['platforms'].keys():
        precord = task_day['platforms'][platform]
        #print "MTMPOINT PL"
        new_wor_id, insert_str = insert_wo_info(precord, {'platform': platform}, new_wor_id, client_lookup)
        iwr.append(insert_str)
        for due_day in precord['due_dates'].keys():
            drecord = precord['due_dates'][due_day]
            for status in drecord['by_status'].keys():
                dsrecord = drecord['by_status'][status]
                #print "MTMPOINT PL DD STATUS"
                new_wor_id, insert_str = insert_wo_info(dsrecord, {'platform': platform, 'due_date': due_day, 'status': status}, new_wor_id, client_lookup)
                iwr.append(insert_str)
            for group in drecord['groups'].keys():
                dgrecord = drecord['groups'][group]
                #print "MTMPOINT PL DD GROUPS"
                new_wor_id, insert_str = insert_wo_info(dgrecord, {'platform': platform, 'due_date': due_day, 'group': group}, new_wor_id, client_lookup)
                iwr.append(insert_str)
                for status in dgrecord['by_status'].keys():
                    dgsrecord = dgrecord['by_status'][status]
                    #print "MTMPOINT PL DD GROUPS STATUS"
                    new_wor_id, insert_str = insert_wo_info(dgsrecord, {'platform': platform, 'due_date': due_day, 'group': group, 'status': status}, new_wor_id, client_lookup)
                    iwr.append(insert_str)
        for due_month in precord['month_due_dates'].keys():
            drecord = precord['month_due_dates'][due_month]
            for status in drecord['by_status'].keys():
                dsrecord = drecord['by_status'][status]
                #print "MTMPOINT PL DM STATUS"
                new_wor_id, insert_str = insert_wo_info(dsrecord, {'platform': platform, 'month_due_date': due_month, 'status': status}, new_wor_id, client_lookup)
                iwr.append(insert_str)
            for group in drecord['groups'].keys():
                dgrecord = drecord['groups'][group]
                #print "MTMPOINT PL DM GROUPS"
                new_wor_id, insert_str = insert_wo_info(dgrecord, {'platform': platform, 'month_due_date': due_month, 'group': group}, new_wor_id, client_lookup)
                iwr.append(insert_str)
                for status in dgrecord['by_status'].keys():
                    dgsrecord = dgrecord['by_status'][status]
                    #print "MTMPOINT PL DM GROUPS STATUS"
                    new_wor_id, insert_str = insert_wo_info(dgsrecord, {'platform': platform, 'month_due_date': due_month, 'group': group, 'status': status}, new_wor_id, client_lookup)
                    iwr.append(insert_str)

    ewr = []
    for date in error_day['dates'].keys():
        drecord = error_day['dates'][date]
        new_err_id, insert_str = insert_error_info(drecord, {'date': date}, new_err_id, client_lookup)
        ewr.append(insert_str)
        for user in drecord['logins'].keys():
            udrecord = drecord['logins'][user]
            new_err_id, insert_str = insert_error_info(udrecord, {'date': date, 'login_name': user}, new_err_id, client_lookup)
            ewr.append(insert_str)
        for group in drecord['groups'].keys():
            gdrecord = drecord['groups'][group]
            new_err_id, insert_str = insert_error_info(gdrecord, {'date': date, 'group': group}, new_err_id, client_lookup)
            ewr.append(insert_str)
        for error_type in drecord['error_type'].keys():
            edrecord = drecord['error_type'][error_type]
            new_err_id, insert_str = insert_error_info(edrecord, {'date': date, 'error_type': error_type}, new_err_id, client_lookup)
            ewr.append(insert_str)
        for client in drecord['clients'].keys():
            cdrecord = drecord['clients'][client]
            new_err_id, insert_str = insert_error_info(cdrecord, {'date': date, 'client_code': client}, new_err_id, client_lookup)
            ewr.append(insert_str)
        for platform in drecord['platforms'].keys():
            pdrecord = drecord['platforms'][platform]
            new_err_id, insert_str = insert_error_info(pdrecord, {'date': date, 'platform': platform}, new_err_id, client_lookup)
            ewr.append(insert_str)
    for month in error_day['months'].keys():
        drecord = error_day['months'][month]
        new_err_id, insert_str = insert_error_info(drecord, {'month': month}, new_err_id, client_lookup)
        ewr.append(insert_str)
        for user in drecord['logins'].keys():
            udrecord = drecord['logins'][user]
            new_err_id, insert_str = insert_error_info(udrecord, {'month': month, 'login_name': user}, new_err_id, client_lookup)
            ewr.append(insert_str)
        for group in drecord['groups'].keys():
            gdrecord = drecord['groups'][group]
            new_err_id, insert_str = insert_error_info(gdrecord, {'month': month, 'group': group}, new_err_id, client_lookup)
            ewr.append(insert_str)
        for error_type in drecord['error_type'].keys():
            edrecord = drecord['error_type'][error_type]
            new_err_id, insert_str = insert_error_info(edrecord, {'month': month, 'error_type': error_type}, new_err_id, client_lookup)
            ewr.append(insert_str)
        for client in drecord['clients'].keys():
            cdrecord = drecord['clients'][client]
            new_err_id, insert_str = insert_error_info(cdrecord, {'month': month, 'client_code': client}, new_err_id, client_lookup)
            ewr.append(insert_str)
        for platform in drecord['platforms'].keys():
            pdrecord = drecord['platforms'][platform]
            new_err_id, insert_str = insert_error_info(pdrecord, {'month': month, 'platform': platform}, new_err_id, client_lookup)
            ewr.append(insert_str)
        
    new_rd_file = '/opt/spt/custom/reports/dashboard_reports/report_day_insert'
    if os.path.exists(new_rd_file):
        os.system('rm -rf %s' % new_rd_file)
    new_guy = open(new_rd_file, 'w')
    new_guy.write(report_day_string)
    new_guy.close()
    print "MADE REPORT DAY INSERT"
      
    new_iwr_file = '/opt/spt/custom/reports/dashboard_reports/wo_report_insert'
    if os.path.exists(new_iwr_file):
        os.system('rm -rf %s' % new_iwr_file)
    new_guy = open(new_iwr_file, 'w')
    for i in iwr:
        new_guy.write('%s\n' % i)
    new_guy.close()

    new_ewr_file = '/opt/spt/custom/reports/dashboard_reports/error_report_insert'
    if os.path.exists(new_ewr_file):
        os.system('rm -rf %s' % new_ewr_file)
    new_guy = open(new_ewr_file, 'w')
    for i in ewr:
        new_guy.write('%s\n' % i)
    new_guy.close()
    
    task_day = None

    insert_wo_end_time = time.time()
    print "INSERT WO TIME = %s" % (insert_wo_end_time - insert_wo_begin_time)

    throwin_rd_begin_time = time.time()
    os.system('psql -U postgres twog < /opt/spt/custom/reports/dashboard_reports/report_day_insert')
    throwin_rd_end_time = time.time()
    print "THROWIN REPORT DAY TIME = %s" % (throwin_rd_end_time - throwin_rd_begin_time)

    throwin_order_report_begin_time = time.time()
    os.system('psql -U postgres twog < /opt/spt/custom/reports/dashboard_reports/order_report_insert')
    throwin_order_report_end_time = time.time()
    print "THROWIN ORDER TIME = %s" % (throwin_order_report_end_time - throwin_order_report_begin_time)



    throwin_wo_report_begin_time = time.time()
    os.system('psql -U postgres twog < /opt/spt/custom/reports/dashboard_reports/wo_report_insert')
    throwin_wo_report_end_time = time.time()
    print "THROWIN WO TIME = %s" % (throwin_wo_report_end_time - throwin_wo_report_begin_time)

    
    os.system('psql -U postgres twog < /opt/spt/custom/reports/dashboard_reports/error_report_insert')

    

    

    draw_begin_time = time.time()
    #NEED TO COLLECT GROUP DATA AND DATA PER INDIVIDUAL AS WELL, AND SEND THAT ALONG AS WELL. 

#    print "ORDERS DUE"
#    print orders_due
#    print "ORDERS LATE"
#    print orders_late
#    print "ORDERS NO DUE DATE"
#    print orders_no_due
#    print "FUTURE ORDERS"
#    pp4.pprint(future_orders)
#    print "TITLES DUE"
#    print titles_due
#    print "TITLES LATE"
#    print titles_late
#    print "TITLES NO DUE DATE"
#    print titles_no_due
#    print "FUTURE TITLES"
#    pp4.pprint(future_titles)
#    print "TASKS DUE"
#    print tasks_due
#    print "TASKS LATE"
#    print tasks_late
#    print "TASKS NO DUE DATE"
#    print tasks_no_due
#    print "FUTURE TASKS"
#    pp4.pprint(future_tasks)
#    print "WH_BY_PLATFORM"
#    pp4.pprint(wh_by_platform)    
#    print "WH_BY_GROUP"
#    pp4.pprint(wh_by_group)    
#    print "WH_BY_DAY"
#    pp4.pprint(wh_by_day)    
#    print "WH_BY_LOGIN"
#    pp4.pprint(wh_by_login)    
#    print "LOGIN REPORT"
#    pp4.pprint(login_report)    
#
#    print "TASK ERRORS TODAY (%s) = %s" % (len(errors_today), errors_today) 
#
#    print 'TASKS_DUE_TODAY_STATUSES = %s' % tasks_due_today_statuses
#    print "TASKS FUTURE::"
#    fw_keys = tasks_future.keys()
#    fw_keys.sort()
#    for fw in fw_keys:
#        print "%s : %s" % (fw, tasks_future[fw])
#    print 'TASKS NO_DUE_DATE (%s) = %s' % (len(tasks_no_due), tasks_no_due)
#    print 'LATE TASKS (%s) = %s' % (len(late_tasks), late_tasks)
#
#    print 'TITLES_DUE_TODAY_STATUSES = %s' % titles_due_today_statuses
#    print "TITLES FUTURE::"
#    tf_keys = titles_future.keys()
#    tf_keys.sort()
#    for tf in tf_keys:
#        print "%s: %s" % (tf, titles_future[tf])
#    print "TITLES NO_DUE_DATE (%s) = %s" % (len(titles_no_due), titles_no_due)
#    print "LATE TITLES (%s) = %s" % (len(late_titles), late_titles)
#
#    print 'ORDERS_DUE_TODAY_STATUSES = %s' % orders_due_today_statuses
#    print "ORDERS FUTURE::"
#    tf_keys = orders_future.keys()
#    tf_keys.sort()
#    for tf in tf_keys:
#        print "%s: %s" % (tf, orders_future[tf])
#    print "ORDERS NO_DUE_DATE (%s) = %s" % (len(orders_no_due), orders_no_due)
#    print "LATE ORDERS (%s) = %s" % (len(late_orders), late_orders)
#
#    print 'ORPHANED TASKS (%s) = %s' % (len(orphaned_tasks), orphaned_tasks) 
#    print 'ORPHANED WORK_ORDERS (%s) = %s' % (len(orphaned_work_orders), orphaned_work_orders) 
#    print 'ORPHANED PROJS (%s) = %s' % (len(orphaned_projs), orphaned_projs) 
#    print 'ORPHANED TITLES (%s) = %s' % (len(orphaned_titles), orphaned_titles) 
#    print "EQUIPMENT = %s" % equipment
    draw_end_time = time.time()

    print "DUMP FILL TIME = %s" % (dump_fill_end_time - dump_fill_begin_time)
    print "RECORD_TIME = %s" % (record_end_time - record_begin_time)
    print "INSERT ORDER TIME = %s" % (insert_order_end_time - insert_order_begin_time)
    print "INSERT WO TIME = %s" % (insert_wo_end_time - insert_wo_begin_time)
    print "THROWIN ORDER TIME = %s" % (throwin_order_report_end_time - throwin_order_report_begin_time)
    print "THROWIN WO TIME = %s" % (throwin_wo_report_end_time - throwin_wo_report_begin_time)
    print "DRAW TIME = %s" % (draw_end_time - draw_begin_time)
    print "FULL TIME = %s" % (draw_end_time - begin_time)

opts, user_name = getopt.getopt(sys.argv[1], '-m')
opts, max_diff = getopt.getopt(sys.argv[2], '-m')
opts, efficiency_cost_prev_days = getopt.getopt(sys.argv[3], '-m')
running_logger = '/var/www/html/running_reports'
fyle = open(running_logger, 'r')
go_bool = True
for line in fyle:
    if 'RUNNING REPORTS' in line:
        go_bool = False
fyle.close()
if go_bool:
    os.system('''echo "RUNNING REPORTS" > %s''' % running_logger)
    fill_report_vars(user_name, max_diff, efficiency_cost_prev_days)
    print "DONE WITH FILL REPORT VARS"
    os.system('''echo "REPORTS NOT RUNNING" > %s''' % running_logger)
else:
   sys.exit(-1) 
# Insert into DB: timestamp, work_orders due today & codes, error & codes, error_types & codes number late & codes, orphaned title, proj, wo, task numbers, no due date tasks, titles, orders counts,  

