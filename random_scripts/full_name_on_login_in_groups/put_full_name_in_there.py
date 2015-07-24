import os, sys, math, hashlib, getopt, tacticenv, time
def kill_mul_spaces(origstrg):
    newstrg = ''
    for word in origstrg.split():
        newstrg=newstrg+' '+word
    return newstrg

def make_data_dict(file_name, key_field):
    the_file = open(file_name, 'r')
    fields = []
    data_dict = {}
    count = 0
    boolio = True
    for line in the_file:
        line = line.rstrip('\r\n')
        #data = line.split('\t')
        data = line.split('|')
        line_dict = {}
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
                    if fields[data_count] == key_field:
                        this_code = val
                    line_dict[fields[data_count]] = val
                    data_count = data_count + 1 
                data_dict[this_code] = line_dict
            count = count + 1  
    the_file.close()
    print "File = %s FIELDS = %s" % (file_name, fields)
    return data_dict

opts, login_file = getopt.getopt(sys.argv[1], '-m')
print  "login_file = %s" % login_file
opts, login_in_group_file = getopt.getopt(sys.argv[2], '-m')
print  "login_in_group_file = %s" % login_in_group_file
login_tbl = make_data_dict(login_file, 'login')
lig_tbl = make_data_dict(login_in_group_file, 'id')
lig_codes = []
lig_codes = sorted(lig_tbl.keys())
login_codes = []
login_codes = sorted(login_tbl.keys())
lig_updates = []
for li in lig_codes:
    lig = lig_tbl[li]
    lig_id = lig.get('id')
    lg = lig.get('login_in_group')
    login = lig.get('login')
    if login in login_codes:
        login_dict = login_tbl[login] 
        
        full_name_s = login.split('.')    
        fn = full_name_s[0]
        fn = '%s%s' % (fn[0], fn[1:])
    
        ln = ''
        if len(full_name_s) > 1:
            ln = full_name_s[1]
      
        if login_dict.get('first_name') not in [None,'']:
            fn = login_dict.get('first_name')
    
        if login_dict.get('last_name') not in [None,'']:
            ln = login_dict.get('last_name')
        full_name = '%s %s' % (fn ,ln)
        lig_updates.append('''update login_in_group set login_full_name = '%s' where id = %s;''' % (full_name, lig_id))
    
            
out_file = open('login_in_group_update.sql', 'w')
for ol in lig_updates:
    out_file.write('%s\n' % ol)
out_file.close()


































