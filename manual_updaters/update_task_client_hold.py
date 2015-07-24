import tacticenv
import os, sys, calendar, dateutil, datetime, time, getopt, pprint, re, math
from pyasm.biz import *


def init():
    nothing = 'true'

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
   
def do_updates(client_code, new_task_str):
    #Need to get the passins here: client_code & new_task_str
    path_prefix = '/var/www/html/user_reports_tables/'
    the_file = '%sclient_billing_task_query' % path_prefix
    lines = ["update task set client_hold = '%s' where client_code = '%s';" % (new_task_str, client_code)]
    if os.path.exists(the_file):
        os.system('rm -rf %s' % the_file)
    new_guy = open(the_file, 'w')
    for i in lines:
        new_guy.write('%s\n' % i)
    new_guy.close()
    
    os.system("psql -U postgres sthpw < %s > %stask_list_cbill" % (the_file, path_prefix)) 

opts, client_code = getopt.getopt(sys.argv[1], '-m')
opts, new_task_str = getopt.getopt(sys.argv[2], '-m')
do_updates(client_code, new_task_str)
