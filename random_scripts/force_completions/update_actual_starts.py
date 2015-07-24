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
    return data_dict

opts, wo_task_file = getopt.getopt(sys.argv[1], '-m')
print  "wo_task_file = %s" % wo_task_file
opts, title_file = getopt.getopt(sys.argv[2], '-m')
print  "title_file = %s" % title_file
opts, order_file = getopt.getopt(sys.argv[3], '-m')
print  "order_file = %s" % order_file
wt_tbl = make_data_dict(wo_task_file)
title_tbl = make_data_dict(title_file)
order_tbl = make_data_dict(order_file)
order_codes = []
order_codes = sorted(order_tbl.keys())
title_codes = []
title_codes = sorted(title_tbl.keys())
wot_codes = []
wot_codes = sorted(wt_tbl.keys())
order_updates = {}
title_updates = {}
for wotc in wot_codes:
    wot = wt_tbl[wotc]
    task_sd = wot.get('actual_start_date')

    order_code = wot.get('order_code')
    if order_code not in [None,'']:
        try:
            oups = order_updates[order_code]
        except:
            order_updates[order_code] = {'actual_start_date': '', 'code': order_code}
            try:
                order_obj = order_tbl[order_code]
                if order_obj.get('actual_start_date') not in [None,'']:
                    order_updates[order_code]['actual_start_date'] = order_obj.get('actual_start_date')
            except:
                pass
            pass


    title_code = wot.get('title_code')
    if title_code not in [None,'']:
        try:
            tups = title_updates[title_code]
        except:
            title_updates[title_code] = {'actual_start_date': '', 'code': title_code}
            try:
                title_obj = title_tbl[title_code]
                if title_obj.get('actual_start_date') not in [None,'']:
                    title_updates[title_code]['actual_start_date'] = title_obj.get('actual_start_date')
            except:
                pass
            pass


    try:
        title = title_tbl[title_code]
        title_actual = title_updates[title_code]['actual_start_date']
        if title_actual not in [None,'']:
            if task_sd < title_actual:
                print "%s IS EARLIER THAN %s" % (task_sd, title_actual)
                title_updates[title_code]['actual_start_date'] = task_sd
        else:
            title_updates[title_code]['actual_start_date'] = task_sd
    except:
        pass

    try:
        order = order_tbl[order_code]
        order_actual = order_updates[order_code]['actual_start_date']
        if order_actual not in [None,'']:
            if task_sd < order_actual:
                print "%s IS EARLIER THAN %s" % (task_sd, order_actual)
                order_updates[order_code]['actual_start_date'] = task_sd
        else:
            order_updates[order_code]['actual_start_date'] = task_sd
    except:
        pass

title_upd_arr = []
for title_code in title_updates.keys():
    entry = title_updates[title_code]
    asd = entry['actual_start_date']
    if asd not in [None,'']:
        update_str = '''update title set actual_start_date = '%s' where code = '%s';''' % (asd, title_code)
        print update_str
        title_upd_arr.append(update_str)

order_upd_arr = []
for order_code in order_updates.keys():
    entry = order_updates[order_code]
    asd = entry['actual_start_date']
    if asd not in [None,'']:
        update_str = '''update "order" set actual_start_date = '%s' where code = '%s';''' % (asd, order_code)
        print update_str
        order_upd_arr.append(update_str)
    
            
out_file = open('title_asd_update.sql', 'w')
for ol in title_upd_arr:
    out_file.write('%s\n' % ol)
out_file.close()

out_file = open('order_asd_update.sql', 'w')
for ol in order_upd_arr:
    out_file.write('%s\n' % ol)
out_file.close()
