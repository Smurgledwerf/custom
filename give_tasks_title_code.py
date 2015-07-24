import os, sys, calendar, dateutil, datetime, time, getopt, pprint, re, math

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

def start():
    sthpw_lines = []
    twog_lines = []
    path_prefix = '/var/www/html/user_reports_tables/'
    os.system("psql -U postgres twog < /opt/spt/custom/reports/dashboard_reports/order_query > %sorder_list_%s" % (path_prefix, 'r')) 
    os.system("psql -U postgres twog < /opt/spt/custom/reports/dashboard_reports/title_query > %stitle_list_%s" % (path_prefix, 'r')) 
    os.system("psql -U postgres twog < /opt/spt/custom/reports/dashboard_reports/proj_query > %sproj_list_%s" % (path_prefix, 'r')) 
    os.system("psql -U postgres twog < /opt/spt/custom/reports/dashboard_reports/work_order_query > %swork_order_list_%s" % (path_prefix, 'r')) 
    os.system("psql -U postgres sthpw < /opt/spt/custom/reports/dashboard_reports/task_query > %stask_list_%s" % (path_prefix, 'r')) 
    orders = make_data_dict('%sorder_list_%s' % (path_prefix, 'r'))
    order_codes = orders.keys()
    titles = make_grouped_dict('%stitle_list_%s' % (path_prefix, 'r'), 'order_code')
    title_lookup = make_data_dict('%stitle_list_%s' % (path_prefix, 'r'))
    title_order_codes = titles.keys() 
    projs = make_grouped_dict('%sproj_list_%s' % (path_prefix, 'r'), 'title_code')
    proj_title_codes = projs.keys()
    work_orders = make_grouped_dict('%swork_order_list_%s' % (path_prefix, 'r'), 'proj_code')
    wos_lookup = make_data_dict('%swork_order_list_%s' % (path_prefix, 'r'))
    wo_proj_codes = work_orders.keys()
    tasks = make_grouped_filtered_dict('%stask_list_%s' % (path_prefix, 'r'), 'lookup_code', 'O')
    task_lookup_codes = tasks.keys()
    for order_code in order_codes:
        ts = []
        try:
            ts = titles[order_code]  
        except:
            pass
        for title in ts:
            ps = []
            title_code = title['code']
            try:
                ps = projs[title_code] 
            except:
                pass
            for proj in ps:
                wos = []
                proj_code = proj['code']
                # Give proj order code here
                twog_lines.append("update proj set order_code = '%s' where code = '%s';" % (order_code, proj_code))
                tsks1 = []
                try:
                    tsks1 = tasks[proj_code]
                except:
                    pass
                t_count = 0
                for task in tsks1:
                    # Create the update lines here
                    # Give title code and order code
                    sthpw_lines.append("update task set order_code = '%s', title_code = '%s' where code = '%s';" % (order_code, title_code, task.get('code')))
                try:
                    wos = work_orders[proj_code]
                except:
                    pass
                for work_order in wos:
                    work_order_code = work_order['code']
                    tsks2 = []
                    # Give WO Title code, proj code, order code
                    twog_lines.append("update work_order set order_code = '%s', title_code = '%s' where code = '%s';" % (order_code, title_code, work_order_code))
                    try:
                        tsks2 = tasks[work_order_code]
                    except:
                        pass
                    t_count = 0
                    for task in tsks2:
                        # Create the update lines here
                        # give task the order code title code proj code
                        sthpw_lines.append("update task set order_code = '%s', title_code = '%s' where code = '%s';" % (order_code, title_code, task.get('code')))
                    
    sthpw_file = '/opt/spt/custom/sthpw_update'
    if os.path.exists(sthpw_file):
        os.system('rm -rf %s' % sthpw_file)
    new_guy = open(sthpw_file, 'w')
    for i in sthpw_lines:
        new_guy.write('%s\n' % i)
    new_guy.close()

    twog_file = '/opt/spt/custom/twog_update'
    if os.path.exists(twog_file):
        os.system('rm -rf %s' % twog_file)
    new_guy = open(twog_file, 'w')
    for i in twog_lines:
        new_guy.write('%s\n' % i)
    new_guy.close()

start()














