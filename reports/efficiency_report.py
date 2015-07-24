__all__ = ["EfficiencyReportWdg"]
import tacticenv
import os, calendar, dateutil, datetime, time
from pyasm.common import Environment
from pyasm.biz import *
from pyasm.web import Table, DivWdg
from pyasm.widget import SelectWdg, IconWdg, TextWdg
from tactic.ui.common import BaseTableElementWdg
from tactic.ui.common import BaseRefreshWdg

class EfficiencyReportWdg(BaseTableElementWdg):

    def init(my):
        nothing = 'true'
        my.yesterday_begin = ''
        my.last_month_end = ''
        my.last_month_begin = ''
        my.next_month_end = ''
        my.next_month_begin = ''
        my.yesterday_begin = ''
        my.yesterday_end = ''
        my.today_begin = ''
        my.today_end = ''
        my.tomorrow_begin = ''
        my.tomorrow_end = ''
        my.begin_date = ''
        my.end_date = ''
        
    def make_double_digits(my, number):
        num_str = str(number)
        to_ret = num_str
        the_len = len(num_str)        
        if the_len < 2:
            to_ret = '0%s' % num_str
        return to_ret 

    def calc_dates(my):
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
       
        last_month = my.make_double_digits(last_month)
        next_month = my.make_double_digits(next_month)
        yesterday_month = my.make_double_digits(yesterday_month)
        tomorrow_month = my.make_double_digits(tomorrow_month)
        day = my.make_double_digits(day)
        month = my.make_double_digits(month)
        tomorrow = my.make_double_digits(tomorrow)
        yesterday = my.make_double_digits(yesterday)
        my.last_month_end = '%s-%s-%s 23:59:59' % (last_month_year, last_month, last_month_range)     
        my.last_month_begin = '%s-%s-01 00:00:00' % (last_month_year, last_month)     
        my.next_month_end = '%s-%s-%s 23:59:59' % (next_month_year, next_month, next_month_range)     
        my.next_month_begin = '%s-%s-01 00:00:00' % (next_month_year, next_month)     
        my.yesterday_begin = '%s-%s-%s 00:00:00' % (yesterday_year, yesterday_month, yesterday) 
        my.yesterday_end = '%s-%s-%s 23:59:59' % (yesterday_year, yesterday_month, yesterday) 
        my.today_begin = '%s-%s-%s 00:00:00' % (year, month, day)
        my.today_end = '%s-%s-%s 23:59:59' % (year, month, day)
        my.tomorrow_begin = '%s-%s-%s 00:00:00' % (tomorrow_year, tomorrow_month, tomorrow) 
        my.tomorrow_end = '%s-%s-%s 23:59:59' % (tomorrow_year, tomorrow_month, tomorrow) 

    def kill_mul_spaces(my, origstrg):
        newstrg = ''
        for word in origstrg.split():
            newstrg=newstrg+' '+word
        return newstrg
    
    def make_data_dict(my, file_name):
        the_file = open(file_name, 'r')
        fields = []
        data_dict = {}
        count = 0
        boolio = True
        for line in the_file:
            line = line.rstrip('\r\n')
            #data = line.split('\t')
            data = line.split(' | ')
            if boolio:
                if count == 0:
                    for field in data:
                        field = my.kill_mul_spaces(field)
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
                        val = my.kill_mul_spaces(val)
                        val = val.strip(' ')
                        if data_count == 0:
                            data_dict[val] = {fields[data_count]: val}
                            this_code = val
                        else:
                            data_dict[this_code][fields[data_count]] = val
                        data_count = data_count + 1 
                count = count + 1  
        the_file.close()
        return data_dict

    def get_day_span(my):
        from datetime import datetime
        full_day_secs = 24 * 60 * 60
        date_format = "%Y-%m-%d %H:%M:%S"
        a = datetime.strptime(my.begin_date, date_format)
        b = datetime.strptime(my.end_date, date_format)
        delta = b - a
        days = delta.days
        day_secs = full_day_secs * days
        begin_time = my.begin_date.split(' ')
        end_time = my.end_date.split(' ')
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

    def get_base_dict(my, login_dict, day_span):
        hours_potential_worked = float(day_span * 8)
        keys = login_dict.keys()
        base_dict = {}
        inserted = []
        for k in keys:
            if k not in inserted:
                base_dict[k] = {'login': k, 'first_name': login_dict[k]['first_name'], 'last_name': login_dict[k]['last_name'], 'number_of_days': day_span, 'hours_potential_worked': hours_potential_worked}
                inserted.append(k)
        return base_dict 

    def fill_login_group(my, base_dict, login_in_group_dict):
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
        return base_dict
    
    def get_number_of_work_orders_completed(my, base_dict, status_log):
        logins = base_dict.keys()
        sum_dict = {}
        for lg in logins:
            sum_dict[lg] = {'total': 0, 'closed_task_codes': ''}
        sl_codes = status_log.keys()
        for sl in sl_codes:
            record = status_log[sl]
            if record.get('status') == 'Completed':
                timestamp = record.get('timestamp')
                if timestamp >= my.begin_date and timestamp <= my.end_date:
                    sl_login = record.get('login')
                    if sl_login in logins:
                        if record.get('task_code') not in sum_dict[sl_login]['closed_task_codes'].split(',') and 'WORK_ORDER' in record.get('lookup_code'):
                            sum_dict[sl_login]['total'] = int(int(sum_dict[sl_login]['total']) + 1)
                            if sum_dict[sl_login]['closed_task_codes'] == '':
                                sum_dict[sl_login]['closed_task_codes'] = record.get('task_code')
                            else:
                                sum_dict[sl_login]['closed_task_codes'] = '%s,%s' % (sum_dict[sl_login]['closed_task_codes'], record.get('task_code'))
        sc = sum_dict.keys()
        for s in sc:
            base_dict[s]['number_of_workorders_completed'] = sum_dict[s]['total']
        #print "SUM DICT = %s" % sum_dict
        return [base_dict, sum_dict]

    def set_default_group_and_rate(my, base_dict, login_groups):
        logins = base_dict.keys()
        group_keys = login_groups.keys()
        for lg in logins:
            default_group = ''
            default_rate = 0.0
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
       
        
    def get_hours_and_cost_info(my, base_dict, work_orders, tasks, work_hours):
        # COMPLETED ONLY FOR COST STUFF
        logins = base_dict.keys()
        sum_dict = {}
        for lg in logins:
            sum_dict[lg] = {'hours_bid': 0, 'hours_actual': 0, 'cost_bid': 0, 'cost_actual': 0}
        wh_keys = work_hours.keys()
        wo_keys = work_orders.keys()
        task_keys = tasks.keys()
        #print task_keys
        login_tasks = {}
        for wh in wh_keys:
            wh_login = work_hours[wh].get('login')
            if work_hours[wh].get('day') <= my.end_date and work_hours[wh].get('day') >= my.begin_date:
                wh_login = work_hours[wh].get('login')
                login_rate = float(base_dict[wh_login].get('default_rate'))
                straight = work_hours[wh]['straight_time']
                if straight in [None,'']:
                    straight = float(0)
                else:
                    straight = float(straight)
                sum_dict[wh_login]['hours_actual'] = float(float(sum_dict[wh_login]['hours_actual']) + straight)
                task_code = work_hours[wh].get('task_code')
                if task_code in task_keys:
                    if tasks[task_code].get('status') == 'Completed':
                        sum_dict[wh_login]['cost_actual'] = float(float(sum_dict[wh_login].get('cost_actual')) + float(float(straight) * float(login_rate)))
                #print "TASK CODE = %s" % task_code
                if wh_login not in login_tasks.keys():
                    login_tasks[wh_login] = []
                if task_code not in login_tasks[wh_login]:
                    login_tasks[wh_login].append(task_code)
                    if task_code in task_keys:
                        work_order_code = tasks[task_code].get('lookup_code')
                        #print "IN WO CODE = %s" % work_order_code
                        if 'WORK_ORDER' in work_order_code:
                            if work_order_code in wo_keys:
                                estimated_wh = work_orders[work_order_code].get('estimated_work_hours')
                                if estimated_wh in [None,'']:
                                    estimated_wh = 0
                                else:
                                    estimated_wh = float(estimated_wh)
                                #print "EST = %s" % estimated_wh
                                sum_dict[wh_login]['hours_bid'] = float(float(sum_dict[wh_login]['hours_bid']) + estimated_wh)
                                #cost stuff
                                if tasks[task_code].get('status') == 'Completed':
                                    sum_dict[wh_login]['cost_bid'] = float(float(sum_dict[wh_login].get('cost_bid')) + float(float(estimated_wh) * float(login_rate)))
                                     
                                 
        #print sum_dict 
        for lg in logins:
            hp = base_dict[lg].get('hours_potential_worked')
            base_dict[lg]['hours_actual'] = sum_dict[lg]['hours_actual']
            base_dict[lg]['hours_bid'] = sum_dict[lg]['hours_bid']
            ha = sum_dict[lg]['hours_actual']
            hb = sum_dict[lg]['hours_bid']
            if ha in [None,'']:
                ha = 0
            if hp in [None,'']:
                hp = 0
            ha = float(ha)
            hp = float(hp)
            if hp > 0:
                pct = '%s%s' % (str(float(float(ha)/float(hp)) * 100),'%')
            else:
                pct = 'N/A'
            base_dict[lg]['performance_percentage'] = pct
            base_dict[lg]['cost_actual'] = sum_dict[lg]['cost_actual']
            base_dict[lg]['cost_bid'] = sum_dict[lg]['cost_bid']
            ca = sum_dict[lg]['cost_actual']
            cb = sum_dict[lg]['cost_bid']
            if ca in [None,'']:
                ca = 0
            if cb in [None,'']:
                cb = 0
            ca = float(ca)
            cb = float(cb)
            margin = 'N/A'
            if cb > 0:
                margin = float(float(float(cb) - float(ca))/cb)
            base_dict[lg]['cost_margin'] = margin 
        return base_dict # NEEDS TO CHANGE
                
    def make_number(my, string):
        ret_num = 0
        string = string.replace('%','')
        if string in [None,'','N/A','None',]:
            ret_num = 0
        else:
            ret_num = float(string)
        return ret_num

    def fix_date(my, date):
        #This is needed due to the way Tactic deals with dates (using timezone info), post v4.0
        from pyasm.common import SPTDate
        return_date = ''
        date_obj = SPTDate.convert_to_local(date)
        if date_obj not in [None,'']:
            return_date = date_obj.strftime("%Y-%m-%d  %H:%M")
        return return_date
    
    def get_display(my):
        login_report_columns = ['login','first_name','last_name','default_group','number_of_days','hours_potential_worked','number_of_workorders_completed','hours_bid','hours_actual','performance_percentage','cost_bid','cost_actual','cost_margin']
        login = Environment.get_login()
        user_name = login.get_login()
        my.calc_dates()
        my.begin_date = my.last_month_begin
        my.end_date = my.yesterday_end
        if 'end_date' in my.kwargs.keys():
            my.end_date = str(my.kwargs.get('end_date'))
        if 'begin_date' in my.kwargs.keys():
            my.begin_date = str(my.kwargs.get('begin_date'))
        day_span = my.get_day_span()
        print "DAY SPAN = %s" % day_span
        begin_time = int(round(time.time() * 1000))
        print "BEGIN TIME = %s" % begin_time
        path_prefix = '/var/www/html/user_reports_tables/'
        os.system("psql -U postgres twog < /opt/spt/custom/reports/order_query > %sorder_list_%s" % (path_prefix, user_name)) 
        os.system("psql -U postgres twog < /opt/spt/custom/reports/title_query > %stitle_list_%s" % (path_prefix, user_name)) 
        os.system("psql -U postgres twog < /opt/spt/custom/reports/proj_query > %sproj_list_%s" % (path_prefix, user_name)) 
        os.system("psql -U postgres twog < /opt/spt/custom/reports/work_order_query > %swork_order_list_%s" % (path_prefix, user_name)) 
        os.system("psql -U postgres twog < /opt/spt/custom/reports/status_log_query > %sstatus_log_list_%s" % (path_prefix, user_name)) 
        os.system("psql -U postgres sthpw < /opt/spt/custom/reports/task_query > %stask_list_%s" % (path_prefix, user_name)) 
        os.system("psql -U postgres sthpw < /opt/spt/custom/reports/login_query > %slogin_list_%s" % (path_prefix, user_name)) 
        os.system("psql -U postgres sthpw < /opt/spt/custom/reports/login_group_query > %slogin_group_list_%s" % (path_prefix, user_name)) 
        os.system("psql -U postgres sthpw < /opt/spt/custom/reports/login_in_group_query > %slogin_in_group_list_%s" % (path_prefix, user_name)) 
        os.system("psql -U postgres sthpw < /opt/spt/custom/reports/work_hour_query > %swork_hour_list_%s" % (path_prefix, user_name)) 
        dump_time = int(round(time.time() * 1000))
        print "DUMP TIME = %s" % dump_time 
        print "DIFFERENCE = %s" % (dump_time - begin_time)
        orders = my.make_data_dict('%sorder_list_%s' % (path_prefix, user_name))
        titles = my.make_data_dict('%stitle_list_%s' % (path_prefix, user_name))
        projs = my.make_data_dict('%sproj_list_%s' % (path_prefix, user_name))
        work_orders = my.make_data_dict('%swork_order_list_%s' % (path_prefix, user_name))
        status_logs = my.make_data_dict('%sstatus_log_list_%s' % (path_prefix, user_name))
        tasks = my.make_data_dict('%stask_list_%s' % (path_prefix, user_name))
        logins = my.make_data_dict('%slogin_list_%s' % (path_prefix, user_name))
        login_groups = my.make_data_dict('%slogin_group_list_%s' % (path_prefix, user_name))
        login_in_groups = my.make_data_dict('%slogin_in_group_list_%s' % (path_prefix, user_name))
        work_hours = my.make_data_dict('%swork_hour_list_%s' % (path_prefix, user_name))
        data_dict_time = int(round(time.time() * 1000))
        print "DATA DICT TIME = %s" % data_dict_time 
        print "SECTION DIFFERENCE = %s" % (data_dict_time - dump_time)
        print "DIFFERENCE = %s" % (data_dict_time - begin_time)
        login_report = my.get_base_dict(logins, day_span)
        base_dict_time = int(round(time.time() * 1000))
        print "BASE DICT TIME = %s" % base_dict_time 
        print "SECTION DIFFERENCE = %s" % (base_dict_time - data_dict_time)
        print "DIFFERENCE = %s" % (base_dict_time - begin_time)
        login_report = my.fill_login_group(login_report, login_in_groups)
        fill_lg_time = int(round(time.time() * 1000))
        print "FILL LG TIME = %s" % fill_lg_time 
        print "SECTION DIFFERENCE = %s" % (fill_lg_time - base_dict_time)
        print "DIFFERENCE = %s" % (fill_lg_time - begin_time)
        login_report = my.set_default_group_and_rate(login_report, login_groups)
        dgr_time = int(round(time.time() * 1000))
        print "DGR TIME = %s" % dgr_time 
        print "SECTION DIFFERENCE = %s" % (dgr_time - fill_lg_time)
        print "DIFFERENCE = %s" % (dgr_time - begin_time)
        login_report, completed_sum_dict = my.get_number_of_work_orders_completed(login_report, status_logs)
        num_wo_time = int(round(time.time() * 1000))
        print "NUM WO TIME = %s" % num_wo_time 
        print "SECTION DIFFERENCE = %s" % (num_wo_time - dgr_time)
        print "DIFFERENCE = %s" % (num_wo_time - begin_time)
        login_report = my.get_hours_and_cost_info(login_report, work_orders, tasks, work_hours)
        hc_time = int(round(time.time() * 1000))
        print "HC TIME = %s" % hc_time 
        print "SECTION DIFFERENCE = %s" % (hc_time - num_wo_time)
        print "DIFFERENCE = %s" % (hc_time - begin_time)
        #print "LOGIN REPORT = %s" % login_report
        
        widget = DivWdg()
        table_top = Table()
        table_top.add_row()
        t1 = table_top.add_cell('<font size=5><b>Efficiency By Login Report</b></font>')
        t2 = table_top.add_cell('<font size=4><b>&nbsp;[For period %s to %s]</b></font>' % (my.fix_date(my.begin_date), my.fix_date(my.end_date)))
        t1.add_attr('nowrap','nowrap')
        t2.add_attr('nowrap','nowrap')
        table = Table()
        table.add_attr('border', '1')
        table.add_row()
        for col in login_report_columns:
            table.add_cell('<b>%s</b>' % col)
        table.add_row()
        lrk = login_report.keys()
        lrk = sorted(lrk)
        group_bin = {}
        group_totals = {}
        all_totals = {'count': 0, 'number_of_days': 0, 'hours_potential_worked': 0, 'number_of_workorders_completed': 0, 'hours_bid': 0, 'hours_actual': 0, 'performance_percentage': 0.0, 'perf_mas': 0.0, 'cost_bid': 0.0, 'cost_actual': 0.0, 'cost_margin': 0.0, 'cm_mas': 0.0}
        all_count = 0
        for lr in lrk:
            lr_dg = login_report[lr].get('default_group')
            num_wos = my.make_number(str(login_report[lr].get('number_of_workorders_completed')))
            hr_bid = my.make_number(str(login_report[lr].get('hours_bid')))
            hr_act = my.make_number(str(login_report[lr].get('hours_actual')))
            perf_pct = my.make_number(str(login_report[lr].get('performance_percentage')))
            cost_bid = my.make_number(str(login_report[lr].get('cost_bid')))
            cost_actual = my.make_number(str(login_report[lr].get('cost_actual')))
            cost_margin = my.make_number(str(login_report[lr].get('cost_margin')))
            if lr_dg not in group_bin.keys():
                group_bin[lr_dg] = []
                group_totals[lr_dg] = {'count': 0, 'number_of_days': login_report[lr].get('number_of_days'), 'hours_potential_worked': login_report[lr].get('hours_potential_worked'), 'number_of_workorders_completed': 0, 'hours_bid': 0, 'hours_actual': 0, 'performance_percentage': 0.0, 'perf_mas': 0.0, 'cost_bid': 0.0, 'cost_actual': 0.0, 'cost_margin': 0.0, 'cm_mas': 0.0}
            group_bin[lr_dg].append(login_report[lr])
            group_totals[lr_dg]['count'] = int(group_totals[lr_dg].get('count')) + 1
            group_totals[lr_dg]['number_of_workorders_completed'] = int(group_totals[lr_dg]['number_of_workorders_completed']) + num_wos
            group_totals[lr_dg]['hours_bid'] = float(group_totals[lr_dg]['hours_bid']) + hr_bid
            group_totals[lr_dg]['hours_actual'] = float(group_totals[lr_dg]['hours_actual']) + hr_act
            if perf_pct > 0:
                group_totals[lr_dg]['performance_percentage'] = float(group_totals[lr_dg]['performance_percentage']) + perf_pct
                group_totals[lr_dg]['perf_mas'] = int(group_totals[lr_dg].get('perf_mas')) + 1
                all_totals['performance_percentage'] = float(all_totals['performance_percentage']) + perf_pct
                all_totals['perf_mas'] = int(all_totals.get('perf_mas')) + 1
            else:
                print "PERF_PCT < 0: %s" % perf_pct
            group_totals[lr_dg]['cost_bid'] = float(group_totals[lr_dg]['cost_bid']) + cost_bid
            group_totals[lr_dg]['cost_actual'] = float(group_totals[lr_dg]['cost_actual']) + cost_actual
            if cost_margin not in [0,'N/A']:
                group_totals[lr_dg]['cost_margin'] = float(group_totals[lr_dg]['cost_margin']) + cost_margin
                group_totals[lr_dg]['cm_mas'] = int(group_totals[lr_dg]['cm_mas']) + 1
                all_totals['cost_margin'] = float(all_totals['cost_margin']) + cost_margin
                all_totals['cm_mas'] = int(all_totals['cm_mas']) + 1
            else:
                print "COST MARGIN < 0: %s" % cost_margin
            nod = login_report[lr].get('number_of_days')
            hpw = login_report[lr].get('hours_potential_worked')
            all_totals['count'] = int(all_totals['count']) + 1
            all_totals['number_of_days'] = nod
            all_totals['hours_potential_worked'] = hpw
            all_totals['number_of_workorders_completed'] = int(all_totals['number_of_workorders_completed']) + num_wos
            all_totals['hours_bid'] = float(all_totals['hours_bid']) + hr_bid
            all_totals['hours_actual'] = float(all_totals['hours_actual']) + hr_act
            all_totals['cost_bid'] = float(all_totals['cost_bid']) + cost_bid
            all_totals['cost_actual'] = float(all_totals['cost_actual']) + cost_actual
        print "GROUP TOTALS1 = %s" % group_totals
        print "ALL TOTALS1 = %s" % all_totals
        atpm = int(all_totals.get('perf_mas'))
        if atpm > 0:
            all_totals['performance_percentage'] = float(float(all_totals['performance_percentage'])/atpm)
        else:
            all_totals['performance_percentage'] = 'N/A'
        atcm = float(all_totals['cm_mas'])
        if atcm > 0:
            all_totals['cost_margin'] = float(float(all_totals['cost_margin'])/atcm)
        else:
            all_totals['cost_margin'] = 'N/A'
        lg_keys = sorted(group_totals.keys())
        for lg in lg_keys:
            gtpm = int(group_totals[lg].get('perf_mas'))
            if gtpm > 0:
                group_totals[lg]['performance_percentage'] = float(float(group_totals[lg]['performance_percentage'])/gtpm)
            else:
                group_totals[lg]['performance_percentage'] = 'N/A'
            gtcm = float(group_totals[lg]['cm_mas'])
            if gtcm > 0:
                group_totals[lg]['cost_margin'] = float(float(group_totals[lg]['cost_margin'])/gtcm)
            else:
                group_totals[lg]['cost_margin'] = 'N/A'

        print "GROUP TOTALS2 = %s" % group_totals
        print "ALL TOTALS2 = %s" % all_totals
        for lg in lg_keys:
            table.add_row()
            table.add_cell('<b>%s</b>' % lg.upper())
            table.add_row()
            group_row = None
            for lr in lrk:
                if login_report[lr].get('default_group') == lg:
                    for col in login_report_columns:
                        table.add_cell(login_report[lr][col])
                    group_row = table.add_row()
            group_row.add_style('background-color: #2eaf10;')
            group_row.add_style('font-weight: bold;')
            table.add_cell('')
            table.add_cell(lg.upper())
            table.add_cell('GROUP TOTALS=>')
            table.add_cell('Count: %s' % (group_totals[lg]['count']))
            table.add_cell(str(group_totals[lg]['number_of_days']))
            table.add_cell(str(group_totals[lg]['hours_potential_worked']))
            table.add_cell(str(group_totals[lg]['number_of_workorders_completed']))
            table.add_cell(str(group_totals[lg]['hours_bid']))
            table.add_cell(str(group_totals[lg]['hours_actual']))
            table.add_cell('%s%s' % (str(group_totals[lg]['performance_percentage']), '%'))
            table.add_cell(str(group_totals[lg]['cost_bid']))
            table.add_cell(str(group_totals[lg]['cost_actual']))
            table.add_cell(str(group_totals[lg]['cost_margin']))
        all_row = table.add_row()
        all_row.add_style('background-color: #3eaf10;')
        all_row.add_style('font-weight: bold;')
        table.add_cell('<b>SUMMARY</b>')
        table.add_cell('')
        table.add_cell('TOTALS->')
        table.add_cell('Count: %s' % (all_totals['count']))
        table.add_cell(all_totals['number_of_days'])
        table.add_cell(all_totals['hours_potential_worked'])
        table.add_cell(all_totals['number_of_workorders_completed'])
        table.add_cell(all_totals['hours_bid'])
        table.add_cell(all_totals['hours_actual'])
        table.add_cell('%s%s' % (all_totals['performance_percentage'], '%'))
        table.add_cell(all_totals['cost_bid'])
        table.add_cell(all_totals['cost_actual'])
        table.add_cell(all_totals['cost_margin'])
        
                     
            
        table_whole = Table()
        table_whole.add_row()
        table_whole.add_cell(table_top)
        table_whole.add_row()
        table_whole.add_cell(table)
        widget.add(table_whole)
        draw_time = int(round(time.time() * 1000))
        print "DRAW TIME = %s" % draw_time 
        print "SECTION DIFFERENCE = %s" % (draw_time - hc_time)
        print "END DIFFERENCE = %s" % (draw_time - begin_time)
        return widget

