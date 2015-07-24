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
for client in clients:
    client_code = client.get('code')
    client_name = client.get('name')
    print "CLIENT NAME = %s" % client_name
    companies = server.eval("@SOBJECT(twog/company['client_code','%s'])" % (client_code))
    company = None
    company_code = ''
    if len(companies) > 1:
        for c in companies:
            bad_messages.append('CLIENT "%s" (%s) is connected to more than 1 Company - Linked to: "%s" (%s)' % (client_name, client_code, c.get('name'), c.get('code')))
print "BAD MESSAGES:"
for bm in bad_messages:
    print bm.encode('utf-8')
            
                    
                
