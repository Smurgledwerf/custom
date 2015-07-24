import os, sys, math, hashlib, getopt, tacticenv
from tactic_client_lib import TacticServerStub
def kill_mul_spaces(origstrg):
    newstrg = ''
    for word in origstrg.split():
        newstrg=newstrg+' '+word
    return newstrg
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


server = TacticServerStub.get(protocol="xmlrpc")
lines_arr = []
opts, file_name = getopt.getopt(sys.argv[1], '-m')
print "file_name = %s" % file_name
print file_name
f= open(file_name, 'r')
by_po = {}
by_code = {}
for line in f:
	if not line.strip():
		continue
	else:
		line = line.rstrip('\r\n')
                columns = line.split(',')
                date = columns[1]
                po_numbers = columns[2]
                order_remnants = columns[3]
                name = columns[4]
                po_split = po_numbers.split('/')
                for po in po_split:
                    po_num = po.replace(' ','').replace('.','')
                    if po_num not in [None,'']:
                        if po_num not in by_po.keys():
                            by_po[po_num] = {'count': 1, 'date': date, 'po_numbers': po_numbers, 'order_codes': order_remnants, 'name': name}
                        else:
                            by_po[po_num]['count'] = by_po[po_num]['count'] + 1
                            by_po[po_num]['date'] = '%s |X| %s' % (by_po[po_num]['date'], date)
                            by_po[po_num]['po_numbers'] = '%s |X| %s' % (by_po[po_num]['po_numbers'], po_numbers)
                            by_po[po_num]['name'] = '%s |X| %s' % (by_po[po_num]['order_codes'], order_remnants)

                order_split = order_remnants.split('/')
                for o in order_split:
                    o = po.replace(' ','').replace('.','')
                    if o not in [None,'']: 
                        order_code = make_code_digits(o) 
                        if order_code not in by_code.keys():
                            by_code[order_code] = {'count': 1, 'date': date, 'po_numbers': po_numbers, 'order_codes': order_remnants, 'name': name, 'order_code': order_code}
                        else:
                            by_code[order_code]['count'] = by_code[order_code]['count'] + 1
                            by_code[order_code]['date'] = '%s |X| %s' % (by_code[order_code]['date'], date)
                            by_code[order_code]['po_numbers'] = '%s |X| %s' % (by_code[order_code]['po_numbers'], po_numbers)
                            by_code[order_code]['name'] = '%s |X| %s' % (by_code[order_code]['order_codes'], order_remnants)
                            by_code[order_code]['order_code'] = '%s |X| %s' % (by_code[order_code]['order_code'], order_code)
  

orders = server.eval("@SOBJECT(twog/order['classification','not in','Master|Cancelled|master|cancelled'])")
unfinished_code = {}
unfinished_po = {}
in_production = {}
for order in orders:
    order_code = order.get('code')
    po_number = order.get('po_number')
    title_statuses = server.eval("@GET(twog/title['order_code','%s'].status)" % order_code)
    title_total = len(title_statuses)
    title_incomplete = 0
    title_str = 'TITLES COMPLETE'
    for ts in title_statuses:
        if ts not in ['Complete','complete','Completed','completed']:
            title_incomplete = title_incomplete + 1
    if title_incomplete > 0:
        title_str = 'NOT FINISHED'

    if order_code in by_code.keys():
        by_code[order_code]['found'] = 'True'
    else:
        if order.get('classification') in ['completed','Completed']:
            if order_code not in unfinished_code.keys():
                closed = order.get('closed')
                closed_str = 'False'
                if closed:
                    closed_str = 'True'
                needs_completion = order.get('needs_completion_review')
                needs_completion_str = 'False'
                if needs_completion:
                    needs_completion_str = 'True'
                unfinished_code[order_code] = {'timestamp': order.get('timestamp'), 'code': order_code, 'po_number': order.get('po_number'), 'classification': order.get('classification'), 'closed': closed_str, 'needs_completion': needs_completion_str, 'titles_str': title_str, 'ratio': '%s/%s' % ((title_total - title_incomplete), title_total), 'price': order.get('price'), 'actual_cost': order.get('actual_cost'), 'title_total': title_total} 
                unfinished_po[order_code] = {'timestamp': order.get('timestamp'), 'code': order_code, 'po_number': order.get('po_number'), 'classification': order.get('classification'), 'closed': closed_str, 'needs_completion': needs_completion_str, 'titles_str': title_str, 'ratio': '%s/%s' % ((title_total - title_incomplete), title_total), 'price': order.get('price'), 'actual_cost': order.get('actual_cost'), 'title_total': title_total} 
          
    if po_number in by_po.keys():
        by_po[po_number]['found'] = 'True'
    else:
        if order.get('classification') in ['completed','Completed']:
            if order_code not in unfinished_code.keys():
                closed = order.get('closed')
                closed_str = 'False'
                if closed:
                    closed_str = 'True'
                needs_completion = order.get('needs_completion_review')
                needs_completion_str = 'False'
                if needs_completion:
                    needs_completion_str = 'True'
                unfinished_code[order_code] = {'timestamp': order.get('timestamp'), 'code': order_code, 'po_number': order.get('po_number'), 'classification': order.get('classification'), 'closed': closed_str, 'needs_completion': needs_completion_str, 'titles_str': title_str, 'ratio': '%s/%s' % ((title_total - title_incomplete), title_total), 'price': order.get('price'), 'actual_cost': order.get('actual_cost'), 'title_total': title_total} 
                unfinished_po[order_code] = {'timestamp': order.get('timestamp'), 'code': order_code, 'po_number': order.get('po_number'), 'classification': order.get('classification'), 'closed': closed_str, 'needs_completion': needs_completion_str, 'titles_str': title_str, 'ratio': '%s/%s' % ((title_total - title_incomplete), title_total), 'price': order.get('price'), 'actual_cost': order.get('actual_cost'), 'title_total': title_total} 
                
    if order.get('classification') in ['in_production','In Production']:
        if order_code not in in_production.keys():
            in_production[order_code] =  {'timestamp': order.get('timestamp'), 'code': order_code, 'po_number': order.get('po_number'), 'classification': order.get('classification'), 'closed': closed_str, 'needs_completion': needs_completion_str, 'titles_str': title_str, 'ratio': '%s/%s' % ((title_total - title_incomplete), title_total), 'price': order.get('price'), 'actual_cost': order.get('actual_cost'), 'title_total': title_total} 


print "\nNEXTNEXT NOT BILLED IN QUICKBOOKS, BUT COMPLETED, BY PO\n"
unfin_po_keys = unfinished_po.keys()
unfin_po_keys.sort()
for upk in unfin_po_keys:
    if unfinished_po[upk]['title_total'] > 0:
        if unfinished_po[upk]['closed'] == 'False':
            print unfinished_po[upk] 
for upk in unfin_po_keys:
    if unfinished_po[upk]['title_total'] > 0:
        if unfinished_po[upk]['closed'] == 'True':
            print unfinished_po[upk] 

print "\nNEXTNEXT NOT BILLED IN QUICKBOOKS, BUT COMPLETED, BY CODE\n"
unfin_code_keys = unfinished_code.keys()
unfin_code_keys.sort()
for uck in unfin_code_keys:
    if unfinished_code[uck]['title_total'] > 0:
        if unfinished_code[uck]['closed'] == 'False':
            print unfinished_code[uck]
for uck in unfin_code_keys:
    if unfinished_code[uck]['title_total'] > 0:
        if unfinished_code[uck]['closed'] == 'True':
            print unfinished_code[uck]

print "\nNEXTNEXT IN_PRODUCTION, YET TITLES COMPLETE\n"
ip_keys = in_production.keys()
ip_keys.sort()
for ik in ip_keys:
    if in_production[ik]['title_total'] > 0:
        if in_production[ik]['classification'] not in ['completed','Completed'] and in_production[ik]['titles_str'] == 'TITLES COMPLETE' and in_production[ik]['closed'] == 'False':
            print in_production[ik]
for ik in ip_keys:
    if in_production[ik]['title_total'] > 0:
        if in_production[ik]['classification'] not in ['completed','Completed'] and in_production[ik]['titles_str'] == 'TITLES COMPLETE' and in_production[ik]['closed'] == 'True':
            print in_production[ik]

print "\nNEXTNEXT BILLED, BUT NOT FOUND TO BE BILLED in TACTIC, BY PO\n"
po_num_keys = by_po.keys()
po_num_keys.sort()
for pn in po_num_keys:
    if 'found' not in by_po[pn].keys():
        print by_po[pn]

print "\nNEXTNEXT BILLED, BUT NOT FOUND TO BE BILLED in TACTIC, BY CODE\n"
code_keys = by_code.keys()
code_keys.sort()
for ck in code_keys:
    if 'found' not in by_code[ck].keys():
        print by_code[ck]


                 
                
