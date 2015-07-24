import os, sys, math, hashlib, getopt, tacticenv, time
from tactic_client_lib import TacticServerStub
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
    #print "File = %s FIELDS = %s" % (file_name, fields)
    id_dict = {}
    for code, dd in data_dict.iteritems():
        id_dict[dd.get('id')] = dd
    return [data_dict, id_dict]

server = TacticServerStub.get(protocol="xmlrpc")
opts, order_file = getopt.getopt(sys.argv[1], '-m')
opts, last_order_id = getopt.getopt(sys.argv[2], '-m')
print "order_file = %s, last_order_id = %s" % (order_file, last_order_id)

CODE = 0
ID = 1
orders = make_data_dict(order_file)
order_codes = orders[CODE].keys()
order_codes.sort()
count = 0
for order_code in order_codes:
    count = count + 1
    print count
    info = orders[CODE][order_code]
    order_id = info.get('id')
    classification = info.get('classification')
    if int(last_order_id) <= int(order_id) and classification not in ['Master','master']:
        server.insert('twog/simplify_pipe', {'order_code': order_code, 'do_all': 'yes'})  
    print "ORDER_ID = %s" % order_id
print "THATS THE END"
