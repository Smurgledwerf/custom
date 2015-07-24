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
opts, order_title_file = getopt.getopt(sys.argv[1], '-m')
print "order_title_file = %s" % order_title_file
title_tbl = make_data_dict(order_title_file)
title_codes = []
title_codes = sorted(title_tbl.keys())
orders = {}
for tc in title_codes:
    title = title_tbl[tc]
    order_code = title.get('order_code')
    status = title.get('status')
    stat_num = 0
    if status == 'Completed' or status == 'Complete':
        print "TITLE = %s, ORDER = %s, STATUS = COMPLETED" % (tc, order_code)
        stat_num = 1
    try:
        order = orders[order_code]
        orders[order_code]['total'] = orders[order_code]['total'] + 1 
        orders[order_code]['completed'] = orders[order_code]['completed'] + stat_num 
    except:
        orders[order_code] = {'completed': stat_num, 'total': 1}
        


out_lines = []
order_codes = sorted(orders.keys())
for oc in order_codes:
    order = orders[oc]
    out_lines.append('''update "order" set titles_completed = %s, titles_total = %s where code = '%s' and titles_total < %s;''' % (order.get('completed'), order.get('total'), oc, order.get('total')))
        
       
out_file = open('order_title_completion.sql', 'w')
for ol in out_lines:
    out_file.write('%s\n' % ol)
out_file.close()

