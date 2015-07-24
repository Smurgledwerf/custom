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
    code_index = 0
    for line in the_file:
        line = line.rstrip('\r\n')
        #data = line.split('\t')
        data = line.split('|')
        if boolio:
            if count == 0:
                field_counter = 0
                for field in data:
                    field = kill_mul_spaces(field)
                    field = field.strip(' ')
                    fields.append(field)
                    if field == 'code':
                        code_index = field_counter
                    field_counter = field_counter + 1
                        
            elif count == 1:
                print file_name
            elif data[0][0] == '(':
                print "END OF FILE"
                boolio = False
            else:
                data_count = 0
                this_code = ''
                this_data = {}
                for val in data:
                    val = kill_mul_spaces(val)
                    val = val.strip(' ')
                    if data_count == code_index:
                        this_code = val
                    this_data[fields[data_count]] = val
                    data_count = data_count + 1 
                data_dict[this_code] = this_data
            count = count + 1  
    the_file.close()
    #print "File = %s FIELDS = %s" % (file_name, fields)
    id_dict = {}
    for code, dd in data_dict.iteritems():
        id_dict[dd.get('id')] = dd
    return [data_dict, id_dict]

os.system('psql -U postgres twog < order_query > order_file')
os.system('psql -U postgres twog < person_query > person_file')
os.system('psql -U postgres twog < client_query > client_file')
order_file = 'order_file'
person_file = 'person_file'
client_file = 'client_file'

opts, date_considering = getopt.getopt(sys.argv[1], '-m')
print "date_considering = %s" % date_considering
opts, begin_date = getopt.getopt(sys.argv[2], '-m')
print "begin_date = %s" % begin_date
opts, end_date = getopt.getopt(sys.argv[3], '-m')
print "end_date = %s" % end_date
opts, classifications_to_block = getopt.getopt(sys.argv[4], '-m')
print "classifications_to_block = %s" % classifications_to_block
opts, ignore_fields = getopt.getopt(sys.argv[5], '-m')
print "ignore_fields = %s" % ignore_fields
opts, grouping_type = getopt.getopt(sys.argv[6], '-m')
print "grouping_type = %s" % grouping_type

do_scheduler = False
if grouping_type.lower() in ['scheduling','scheduler','schedulers','login','user_name','creator']:
    do_scheduling = True
    print 'DO SCHEDULING: %s' % do_scheduling
do_classification = False
if grouping_type.lower() in ['class','classification','status']:
    do_classification = True
    print 'DO CLASSIFICATION: %s' % do_classification

blocked_classifications = classifications_to_block.split(',')
blocked_classifications.append('Master')
ignore_fields = ignore_fields.lower()
ignores = ignore_fields.split(',') 
CODE = 0
ID = 1
persons = make_data_dict(person_file)
orders = make_data_dict(order_file)
clients = make_data_dict(client_file)
order_codes = orders[CODE].keys()
person_codes = persons[CODE].keys()
client_codes = clients[CODE].keys()
out_lines = []
grouping = {}
for order_code in order_codes:
    #Expected first
    order = orders[CODE][order_code]
    lookat_date = order.get(date_considering)
    classification = order.get('classification')
    scheduler = order.get('login')
    if lookat_date >= begin_date and lookat_date <= end_date and classification not in blocked_classifications:
        #print "%s: Begin: %s >= %s <= End: %s" % (order_code, begin_date, lookat_date, end_date)
        if do_scheduling:
            if scheduler not in grouping.keys():
                grouping[scheduler] = []
            grouping[scheduler].append(order)
        elif do_classification:
            if classification not in grouping.keys():
                grouping[classification] = []
            grouping[classification].append(order)
grouping_keys = grouping.keys()
grouping_keys.sort()
grouping_totals = {}
for gk in grouping_keys:
    grouping[gk].sort(key=lambda item:item[date_considering], reverse=True) 
    if gk not in grouping_totals:
        grouping_totals[gk] = {'count': 0, 'total_estimated_cost': 0, 'total_estimated_price': 0, 'total_actual_cost': 0, 'total_actual_price': 0}
    for order in grouping[gk]:
        expected_price = order.get('expected_price')
        price = order.get('price')
        expected_cost = order.get('expected_cost')
        actual_cost = order.get('actual_cost')
        if expected_price in [None,'']:
            expected_price = 0
        else:
            expected_price = float(expected_price) 
        if price in [None,'']:
            price = 0
        else:
            price = float(price) 
        if expected_cost in [None,'']:
            expected_cost = 0
        else:
            expected_cost = float(expected_cost) 
        if actual_cost in [None,'']:
            actual_cost = 0
        else:
            actual_cost = float(actual_cost) 
        grouping_totals[gk]['count'] = grouping_totals[gk]['count'] + 1
        grouping_totals[gk]['total_estimated_cost'] = grouping_totals[gk]['total_estimated_cost'] + expected_cost
        grouping_totals[gk]['total_estimated_price'] = grouping_totals[gk]['total_estimated_price'] + expected_price
        grouping_totals[gk]['total_actual_cost'] = grouping_totals[gk]['total_actual_cost'] + actual_cost
        grouping_totals[gk]['total_actual_price'] = grouping_totals[gk]['total_actual_price'] + price

top_line_written = False
for gk in grouping_keys:
    orders = grouping[gk]
    print "GK: %s, Count of Orders = %s" % (gk, len(orders))
    for order in orders:
        if not top_line_written:
            top_line_written = True
            order_keys = order.keys()
            line = ''
            for ok in order_keys:
                if ok not in ignores:
                    if line == '':
                        line = ok
                    else:
                        line = '%s,%s' % (line, ok)
            out_lines.append(line)
        line = ''
        order_keys = order.keys()
        for ok in order_keys:
            if ok not in ignores:
                value = order.get(ok)
                if 'PERSON' in value:
                    if value in person_codes:
                        person = persons[CODE][value]
                        value = '%s %s' % (person.get('first_name'), person.get('last_name'))
                if 'CLIENT' in value:
                    if value in client_codes:
                        value = clients[CODE][value].get('name')
                if line == '':
                    line = '"%s"' % value
                else:
                    line = '%s,"%s"' % (line, value)
        out_lines.append(line)
    out_lines.append('%s, Total Estimated Cost: %s, Total Actual Cost: %s, Total Estimated Price: %s, Total Actual Price: %s' % (gk, grouping_totals[gk]['total_estimated_cost'], grouping_totals[gk]['total_actual_cost'], grouping_totals[gk]['total_estimated_price'], grouping_totals[gk]['total_actual_price']))
    count = grouping_totals[gk]['count']
    average_estimated_cost = 0
    average_estimated_price = 0
    average_actual_cost = 0
    average_actual_price = 0
    if count > 0:
        average_estimated_cost = '%.2f' % float(float(grouping_totals[gk]['total_estimated_cost'])/count)
        average_estimated_price = '%.2f' % float(float(grouping_totals[gk]['total_estimated_price'])/count)
        average_actual_cost = '%.2f' % float(float(grouping_totals[gk]['total_actual_cost'])/count)
        average_actual_price = '%.2f' % float(float(grouping_totals[gk]['total_actual_price'])/count)
    out_lines.append('%s, Average Estimated Cost: %s, Average Actual Cost: %s, Average Estimated Price: %s, Average Actual Price: %s' % (gk, average_estimated_cost, average_actual_cost, average_estimated_price, average_actual_price))
                                
out_file = open('order_report_%s_%s_to_%s.csv' % (date_considering, begin_date, end_date),'w')
for ol in out_lines:
    out_file.write('%s\n' % ol)
out_file.close()
