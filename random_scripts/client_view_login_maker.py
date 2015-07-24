import os, sys, math, hashlib, getopt, tacticenv, random
from tactic_client_lib import TacticServerStub
def kill_mul_spaces(origstrg):
    newstrg = ''
    for word in origstrg.split():
        newstrg=newstrg+' '+word
    return newstrg

server = TacticServerStub.get(protocol='xmlrpc')
clients = server.eval("@SOBJECT(twog/client['@ORDER_BY','name asc'])")
bad_messages = []
create_messages = []
for client in clients:
    if client.get('portal_login') in [None,'']:
        client_code = client.get('code')
        client_name = client.get('name')
        print "CLIENT NAME = %s" % client_name
        companies = server.eval("@SOBJECT(twog/company['client_code','%s'])" % (client_code))
        company = None
        company_code = ''
        if len(companies) > 0:
            company = companies[0]
            company_code = company.get('code')
        if len(companies) > 1:
            for c in companies:
                bad_messages.append('CLIENT "%s" (%s) is connected to more than 1 Company - Linked to: "%s" (%s)' % (client_name, client_code, c.get('name'), c.get('code')))
            company = companies[0]
            company_code = company.get('code')
        elif len(companies) == 0:
            #Create the Company
            company = server.insert('twog/company', {'name': client_name.upper(), 'country': client.get('country'), 'state': client.get('state'), 'phone': client.get('phone'), 'city': client.get('city'), 'zip': client.get('zip'), 'street_address': client.get('street_address'), 'email': client.get('email'), 'client_code': client_code, 'suite': client.get('suite')}) 
            company_code = company.get('code')
            print "CREATED COMPANY '%s'" % company.get('name').upper()
            create_messages.append('Created Company: "%s" (%s), Connected to Client: "%s" (%s)' % (company.get('name'), company.get('code'), client_name, client_code)) 
        attempted_login = client_name.replace(' ','').lower()
        if len(attempted_login) > 5:
            attempted_login = attempted_login[:5]
        attempted_login = 'gg_%s' % attempted_login
        login_inserted = False
        count = 0
        while not login_inserted:
            random_num = random.randrange(100,1000)
            attempted_login = '%s%s' % (attempted_login, random_num)
            if count > 0:
                attempted_login = '%s%s' % (attemped_login, count)
            anyofem = server.eval("@SOBJECT(sthpw/login['login','%s'])" % attempted_login)
            if len(anyofem) == 0:
                english_pass = '%s%s' % (attempted_login[::-1], random.randint(100,1000)) 
                md5o = hashlib.md5()
                md5o.update(english_pass) 
                md5_pass = md5o.hexdigest()
                print "ATTEMPTED LOGIN = %s" % attempted_login
                print "ENGLISH PASS = %s" % english_pass
                print "MD5 PASS = %s" % md5_pass
                print "CLIENT NAME = %s" % client_name
                safe_client_name = client_name
                if len(client_name) > 27:
                    safe_client_name  = safe_client_name[:27]
                login_obj = server.insert('sthpw/login', {'login': attempted_login, 'code': attempted_login, 'first_name': safe_client_name, 'last_name': 'Portal Account', 'password': md5_pass, 'license_type': 'user', 'email': 'matt.misenhimer@2gdigital.com', 'display_name': 'Portal Account, %s' % client_name, 'location': 'external'})
                #login_obj = server.insert('sthpw/login', {'login': attempted_login, 'code': attempted_login, 'first_name': 'fn', 'last_name': 'Portal Account', 'password': md5_pass, 'license_type': 'user', 'email': 'matt.misenhimer@2gdigital.com', 'display_name': 'Portal Account, %s' % client_name, 'location': 'external'})
                create_messages.append('Created Login: %s, English Pass: %s, MD5 Pass: %s' % (attempted_login, english_pass, md5_pass))
                server.insert('sthpw/login_in_group', {'login_group': 'client', 'login': attempted_login})
                person_obj = server.insert('twog/person', {'login_name': attempted_login, 'first_name': client_name, 'last_name': 'Portal Account', 'email': 'matt.misenhimer@2gdigital.com', 'client_code': client_code, 'company_code': company_code})
                server.update(client.get('__search_key__'), {'portal_login': attempted_login, 'portal_pass': english_pass})
                login_inserted = True
            count = count + 1

print "BAD MESSAGES:"
for bm in bad_messages:
    print bm

print "CREATE MESSAGES:"
for cm in create_messages:
    print cm
            
                    
                
