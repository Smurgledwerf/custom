import os, sys, math, hashlib, getopt, tacticenv, time
from tactic_client_lib import TacticServerStub
server = TacticServerStub.get(protocol="xmlrpc")
def kill_mul_spaces(origstrg):
    newstrg = ''
    for word in origstrg.split():
        newstrg=newstrg+' '+word
    return newstrg

def make_data_dict(file_name, grouping_col):
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
                    if field == grouping_col:
                        code_index = field_counter
                    field_counter = field_counter + 1
                        
            elif count == 1:
                print file_name
                print line
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
    print "File = %s FIELDS = %s" % (file_name, fields)
    return data_dict

def make_base_cost_tbl(elements):
    table = '<table>'
    for element in elements:
        lenpart = ''
        if element.get('length') not in [None,'']:
            lenpart = '<td>Len: %s</td>' % element.get('length')
        table = '%s<tr><td>Unit: %s</td><td>Cost: %s</td>%s</tr>' % (table, element.get('unit'), element.get('cost'), lenpart)
    table = '%s</table>' % table    
    return table

opts, eq_file = getopt.getopt(sys.argv[1], '-m')
print "eq_file = %s" % eq_file
opts, eq_u_file = getopt.getopt(sys.argv[2], '-m')
print "eq_u_file = %s" % eq_u_file
opts, eq_unit_cost_file = getopt.getopt(sys.argv[3], '-m')
print "eq_unit_cost_file = %s" % eq_unit_cost_file

lookup_codes = {}
eqs = make_data_dict(eq_file, 'code')
#print eqs
equs = make_data_dict(eq_u_file, 'code')
eq_unit_costs_pre = make_data_dict(eq_unit_cost_file, 'code')
eq_unit_cost = {}
for eqc in eq_unit_costs_pre.keys():
    guy = eq_unit_costs_pre[eqc]
    if guy.get('equipment_code') in eq_unit_cost.keys():
        eq_unit_cost[guy.get('equipment_code')].append({'unit': guy.get('unit'), 'cost': guy.get('cost'), 'length': guy.get('length')}) 
    else:
        eq_unit_cost[guy.get('equipment_code')] = [{'unit': guy.get('unit'), 'cost': guy.get('cost'), 'length': guy.get('length')}] 
equipment_codes = eqs.keys()
equipment_used_codes = equs.keys()
out_lines = []
problem_lines = []
eq_report = {}
for code in equipment_used_codes:
    s_status = equs[code]['s_status']
    eq_code = equs[code]['equipment_code']
    if s_status not in ['retired','r'] and eq_code not in [None,''] and eq_code in eqs.keys():
        if eq_code not in eq_report.keys():
            report = {'name': eqs[eq_code]['name'], 'count': 0, 'count_has_duration': 0, 'avg_duration': 0.0, 'total_duration': 0.0, 'count_has_length': 0, 'count_by_length': {}, 'total_expected_cost': 0.0, 'avg_expected_cost': 0.0, 'total_actual_cost': 0.0, 'count_actual_filled': 0, 'avg_actual_cost_filled': 0, 'avg_actual_cost': 0, 'count_by_unit': {}, 'total_quantity': 0, 'count_has_quantity': 0} 
            eq_report[eq_code] = report

        eq_report[eq_code]['count'] = eq_report[eq_code]['count'] + 1

        actual_duration = equs[code]['actual_duration']
        if actual_duration not in [None,'',0,'0']:
            eq_report[eq_code]['count_has_duration'] = eq_report[eq_code]['count_has_duration'] + 1
            eq_report[eq_code]['total_duration'] = eq_report[eq_code]['total_duration'] + float(actual_duration)

        length = equs[code]['length']
        if length not in [None,'',0,'0']:
            eq_report[eq_code]['count_has_length'] = eq_report[eq_code]['count_has_length'] + 1
            if length not in eq_report[eq_code]['count_by_length'].keys():
                eq_report[eq_code]['count_by_length'][length] = 1
            else:
                eq_report[eq_code]['count_by_length'][length] = eq_report[eq_code]['count_by_length'][length] + 1

        units = equs[code]['units']
        if units not in eq_report[eq_code]['count_by_unit'].keys():
            eq_report[eq_code]['count_by_unit'][units] = 1
        else:
            eq_report[eq_code]['count_by_unit'][units] = eq_report[eq_code]['count_by_unit'][units] + 1

        expected_cost = equs[code]['expected_cost']
        if expected_cost in [None,'','0',0]:
            expected_cost = 0
        eq_report[eq_code]['total_expected_cost'] = eq_report[eq_code]['total_expected_cost'] + float(expected_cost)

        actual_cost = equs[code]['actual_cost']
        if actual_cost in [None,'','0',0]:
            actual_cost = 0
        else:
            eq_report[eq_code]['count_actual_filled'] = eq_report[eq_code]['count_actual_filled'] + 1
        eq_report[eq_code]['total_actual_cost'] = eq_report[eq_code]['total_actual_cost'] + float(actual_cost)

        quantity = equs[code]['actual_quantity']
        if quantity in [None,'',0,'0']:
            quantity = 0
        else:
            eq_report[eq_code]['count_has_quantity'] = eq_report[eq_code]['count_has_quantity'] + 1
        eq_report[eq_code]['total_quantity'] = eq_report[eq_code]['total_quantity'] + float(quantity)
    else:
        if s_status not in ['retired','r']:
            rr = 5 + 5
            #print "BAD EQ CODE: %s. FROM: %s" % (eq_code, code)

table2 = '<table style="border-width: 1px;">'
table = '<table border="1"><tr><td>Name</td><td>Eq Code</td><td>Count</td><td>Base Costs</td><td>Have Actual Duration</td><td>Avg Duration</td><td>Have Length</td><td>Count By Length</td><td>Count By Unit</td><td>Avg Expected Cost</td><td>Avg Actual Cost (Filled)</td><td>Avg Actual Cost Total</td><td>Total Quantity</td></tr>'
for code in equipment_codes:
    if code in eq_report.keys():
        data = eq_report[code]
        base_cost_tbl = 'No Information'
        if code in eq_unit_cost.keys():
            base_cost_tbl = make_base_cost_tbl(eq_unit_cost[code])
        name = data['name']
        count = data['count']
        count_has_duration = data['count_has_duration']
        total_duration = data['total_duration']
        count_has_length = data['count_has_length']
        total_expected_cost = data['total_expected_cost']
        total_actual_cost = data['total_actual_cost']
        count_actual_filled = data['count_actual_filled']
        total_quantity = data['total_quantity']
        count_has_quantity = data['count_has_quantity']
        
        len_tbl = '<table border="1">'
        by_length = data['count_by_length']
        for key, val in by_length.iteritems():
            len_tbl = '%s<tr><td>%s: %s</td></tr>' % (len_tbl, key, val)
        len_tbl = '%s</table>' % len_tbl
    
        unit_tbl = '<table border="1">'
        by_unit = data['count_by_unit']
        for key, val in by_unit.iteritems():
            unit_tbl = '%s<tr><td>%s: %s</td></tr>' % (unit_tbl, key, val)
        unit_tbl = '%s</table>' % unit_tbl
        
        avg_duration = 'N/A'
        if count_has_duration != 0:
            avg_duration = float(float(total_duration)/float(count_has_duration))
        avg_expected_cost = 'N/A'
        avg_actual_cost = 'N/A'
        if count > 0:
            avg_expected_cost = float(float(total_expected_cost)/float(count))   
            avg_actual_cost = float(float(total_actual_cost)/float(count))   
        avg_actual_cost_filled = 'N/A'
        if count_actual_filled != 0:
            avg_actual_cost_filled = float(float(total_actual_cost)/float(count_actual_filled))
    
        table = '%s<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (table, name, code, count, base_cost_tbl, count_has_duration, avg_duration, count_has_length, len_tbl, unit_tbl, avg_expected_cost, avg_actual_cost_filled, avg_actual_cost, total_quantity) 
    else:
        table2 = '%s<tr><td>%s</td><td>%s</td></tr>' % (table2, eqs[code]['name'], code)
table = '%s</table>' % table
table2 = '%s</table>' % table2
out_file = open('/var/www/html/source_labels/eq_report.html','w')
out_file.write(table)
out_file.close()
problem_file = open('/var/www/html/source_labels/eq_report_problems.html', 'w')
problem_file.write(table2)
problem_file.close()
