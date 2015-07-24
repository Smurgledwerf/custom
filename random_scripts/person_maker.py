import os, sys, math, hashlib, getopt, tacticenv
from tactic_client_lib import TacticServerStub
def kill_mul_spaces(origstrg):
    newstrg = ''
    for word in origstrg.split():
        newstrg=newstrg+' '+word
    return newstrg

server = TacticServerStub.get(protocol='xmlrpc')
lines_arr = []
opts, file_name = getopt.getopt(sys.argv[1], '-m')
print file_name
f= open(file_name, 'r')
active_directory = ''
count = 0
fields = [] 
dpp = {}
people = []
for line in f:
	if not line.strip():
		continue
	else:
		line = line.rstrip('\r\n')
                if count == 0:
                    fields = line.split('\t')
                    print fields
                    count = count + 1
                else:
                    data = line.split('\t')
                    first = data[fields.index('first_name')].strip().replace('&','and')
                    last = data[fields.index('last_name')].strip()
                    print "FIRST, LAST = %s, %s" % (first, last)
                    expr2 = "@SOBJECT(twog/person['first_name','%s']['last_name','%s'])" % (first,last) 
                    rez2 = server.eval(expr2)
                    if first not in ['',None] and last not in ['',None]:
                        first_last = '%s %s' % (first, last)
                  
                        print "FIRST_LAST = %s" % first_last
                        if first_last not in dpp.keys():
                            dpp[first_last] = {}
                            people.append(first_last)
                        ind = 0
                        for d in data:
                            if fields[ind] not in dpp[first_last].keys():
                                dpp[first_last][fields[ind]] = d.strip()
                            ind = ind + 1
                        count = count + 1
f.close()
server.start('IMPORTING PEOPLE AND THINGS')
companies = []
comp_code_lookup = {}
for dude in people:
    company  = kill_mul_spaces(dpp[dude]['company_name'].upper().strip())
    if company not in companies and company not in ['',None]:
        print "COMPANY = %s" % company
        companies.append(company)
        address = dpp[dude]['company_address'].upper()
        city = dpp[dude]['company_city'].upper()
        state = dpp[dude]['company_state'].upper()
        zip = dpp[dude]['company_zip']
        expr = "@SOBJECT(twog/company['name','%s'])" % company
        rez = server.eval(expr)
        if len(rez) > 0:
            rez=rez[0] 
        #else:
        #    rez = server.insert('twog/company', {'name': company, 'street_address': address, 'state': state, 'zip': zip, 'city': city})
        comp_code_lookup[company] = rez.get('code')
print "CCL = %s" % comp_code_lookup
for dude in people:
    print "DUDE = %s" % dude
    person_data = {'cell_phone': '', 'main_phone': '', 'work_phone': '', 'home_phone': '', 'fax': '', 'pager': ''}
    for field in fields:
        if '_type' not in field:
            chunk = dpp[dude][field]
            if 'phone' in field:
                pnum = field.split('hone')[1]
                phone_number = chunk
                phone_type = dpp[dude]['phone%s_type' % pnum].upper()
                if phone_type.find('MAIN') != -1 or phone_type.find('DIRECT') != -1:
                    person_data['main_phone'] = phone_number
                elif phone_type.find('CELL') != -1 or phone_type.find('MOBILE') != -1:
                    person_data['cell_phone'] = phone_number
                elif phone_type.find('FAX'):
                    person_data['fax'] = phone_number
                elif phone_type.find('PAGER') != -1:
                    person_data['pager'] = phone_number
                elif phone_type.find('HOME') != -1:
                    person_data['home_phone'] = phone_number
                elif phone_type.find('WORK') != -1:
                    person_data['work_phone'] = phone_number
                else:
                    print "NOTHING TO DO WITH PHONE TYPE OF %s" % phone_type
            else:
                if field.find('company') != -1:
                    if field.find('address') != -1:
                        person_data['street_address'] = chunk.upper()
                    elif field.find('zip') != -1:
                        person_data['zip'] = chunk
                    elif field == 'company_name': 
                        if chunk != '':
                            person_data['company_code'] = comp_code_lookup[kill_mul_spaces(chunk.upper().strip())]
                    elif field.find('suite') != -1:
                        person_data['suite'] = chunk
                    elif field.find('state') != -1:
                        person_data['state'] = chunk.upper()
                    elif field.find('city') != -1:
                        person_data['city'] = chunk.upper()
                else:
                    if field.find('first') != -1 or field.find('last') != -1:
                        chunk=chunk.capitalize()
                    person_data[field] = chunk
    print "PERSON DATA = %s" % person_data
    pers_expr = "@SOBJECT(twog/person['first_name','%s']['last_name','%s'])" % (person_data['first_name'],person_data['last_name'])
    #pers = server.eval(pers_expr)
    #update_sk = ''
    #if len(pers) > 0:
    #    update_sk = pers[0].get('__search_key__')    
    #    server.update(update_sk, person_data)
    #else:
    #    server.insert('twog/person', person_data)
                    
                
server.finish()
