#NEED TO COLLECT ALL WORK HOURS AND REPORT THOSE UNCONNECTED TO WORK ORDERS AND TASKS, CONNECT THEM TO CLIENT AS WELL
__all__ = ["DashboardReportWdg"]
import tacticenv
import os, sys, calendar, dateutil, datetime, time, getopt, pprint, re, math
from pyasm.biz import *
from tactic_client_lib import TacticServerStub


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

def get_base_dict(login_dict):
    keys = login_dict.keys()
    base_dict = {}
    inserted = []
    for k in keys:
        if k not in inserted:
            base_dict[k] = {'login': k, 'first_name': login_dict[k]['first_name'], 'last_name': login_dict[k]['last_name']}
            inserted.append(k)
    base_dict['Not Set'] = {'login': 'Not Set', 'first_name': 'N/A', 'last_name': 'N/A'}
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
    this_month_s = today_end.split('-')
    this_month = ''.join(this_month_s[:2])
    print "This Month = %s" % this_month
    return {'yesterday': yesterday_begin.split(' ')[0], 'last_month': last_month_end.split(' ')[0], 'next_month': next_month_end.split(' ')[0], 'this_month': this_month, 'today': today_end.split(' ')[0], 'tomorrow': tomorrow_end.split(' ')[0]}

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

def fill_wh(whs):
    pp3 = pprint.PrettyPrinter(depth=3)
    wharr = []
    for wh in whs:
        line = wh.get('line')
        line = line.replace('MTMWHMTM ','')
        dict = {'line': line}
        line_s = line.split(':MTM:')
        lensplit = len(line_s) 
        current_key = ''
        for i in range(0,lensplit):
            if i % 2 == 0:
                current_key = line_s[i].lower()
            else:
                dict[current_key] = line_s[i]
        wharr.append(dict)
        #pp3.pprint(dict)
    return wharr

def id_only(the_code):
    the_thing = re.findall("(\d+)", the_code)[0]
    the_int = int(the_thing)
    the_id = str(the_int)
    return the_id

def sum_em_eqs(record, to_sum_dict):
    seqt = time.time()
    record['eq_actual_hours'] = float(record['eq_actual_hours']) + to_sum_dict['actual_duration']
    record['eq_expected_hours'] = float(record['eq_expected_hours']) + to_sum_dict['expected_duration']
    record['eq_actual_cost'] = float(record['eq_actual_cost']) + to_sum_dict['actual_cost']
    record['eq_expected_cost'] = float(record['eq_expected_cost']) + to_sum_dict['expected_cost']
    return record

def sum_em_whs(record, to_sum_dict): 
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
    return record

def fill_report_vars(file_name):
    new_info = {'WH': [], 'EQ': []}
    if os.path.exists(file_name):
        dates_here = calc_dates()
        updates = open(file_name, 'r')
        for line in updates:
            line = line.rstrip('\r\n')
            if 'MTMWHMTM' in line:
                new_info['WH'].append({'line': line})
            elif 'MTMEQMTM' in line:
                new_info['EQ'].append({'line': line})
        updates.close()
        new_info['WH'] = fill_wh(new_info['WH']) 
        order_codes = ''
        for guy in new_info['WH']:
             ocode = guy.get('order')
             if ocode not in order_codes:
                 if order_codes == '':
                     order_codes = ocode
                 else: 
                     order_codes = '%s|%s' % (order_codes, ocode)
        print order_codes
        # - MTM TURN ON WHEN YOU GO LIVE: os.system('rm -rf %s' % file_name)
        path_prefix = '/var/www/html/user_reports_tables/'
        os.system("psql -U postgres sthpw < /opt/spt/custom/reports/dashboard_reports/login_query > %slogin_list_updater" % (path_prefix)) 
        os.system("psql -U postgres sthpw < /opt/spt/custom/reports/dashboard_reports/login_group_query > %slogin_group_list_updater" % (path_prefix)) 
        os.system("psql -U postgres sthpw < /opt/spt/custom/reports/dashboard_reports/login_in_group_query > %slogin_in_group_list_updater" % (path_prefix)) 
    
        logins = make_data_dict('%slogin_list_updater' % (path_prefix))
        login_groups = make_data_dict('%slogin_group_list_updater' % (path_prefix))
        login_group_codes = login_groups.keys()
        login_in_groups = make_data_dict('%slogin_in_group_list_updater' % (path_prefix))
        login_report = get_base_dict(logins)
        login_report = fill_login_group(login_report, login_in_groups)
        login_report = set_default_group_and_rate(login_report, login_groups)
        login_codes = login_report.keys()
        current_time_flat = time.time()        
        current_time = datetime.datetime.fromtimestamp(current_time_flat).strftime('%Y-%m-%d %H:%M:%S')
        current_day = current_time.split(' ')[0]
        current_split = current_day.split('-')
        yesterday = dates_here['yesterday']
        tomorrow = dates_here['tomorrow']
        last_month = dates_here['last_month']
        next_month = dates_here['next_month']
        this_month = dates_here['this_month']
    
    


        # MTM TURN ON ONCE YOU WANT TO ACTUALLY DO THE UPDATE    
#        new_owr_file = '/opt/spt/custom/reports/dashboard_reports/order_report_update'
#        if os.path.exists(new_owr_file):
#            os.system('rm -rf %s' % new_owr_file)
#        new_guy = open(new_owr_file, 'w')
#        for i in owr:
#            new_guy.write('%s\n' % i)
#        new_guy.close()
#          
#        new_iwr_file = '/opt/spt/custom/reports/dashboard_reports/wo_report_update'
#        if os.path.exists(new_iwr_file):
#            os.system('rm -rf %s' % new_iwr_file)
#        new_guy = open(new_iwr_file, 'w')
#        for i in iwr:
#            new_guy.write('%s\n' % i)
#        new_guy.close()
#    
#        new_ewr_file = '/opt/spt/custom/reports/dashboard_reports/error_report_update'
#        if os.path.exists(new_ewr_file):
#            os.system('rm -rf %s' % new_ewr_file)
#        new_guy = open(new_ewr_file, 'w')
#        for i in ewr:
#            new_guy.write('%s\n' % i)
#        new_guy.close()
#        
#        os.system('psql -U postgres twog < /opt/spt/custom/reports/dashboard_reports/order_report_update')
#        os.system('psql -U postgres twog < /opt/spt/custom/reports/dashboard_reports/wo_report_update')
#        os.system('psql -U postgres twog < /opt/spt/custom/reports/dashboard_reports/error_report_update')
        # MTM END

opts, file_name = getopt.getopt(sys.argv[1], '-m')
fill_report_vars(file_name)
# Insert into DB: timestamp, work_orders due today & codes, error & codes, error_types & codes number late & codes, orphaned title, proj, wo, task numbers, no due date tasks, titles, orders counts,  

