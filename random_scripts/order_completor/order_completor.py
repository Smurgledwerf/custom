import os, sys, math, hashlib, getopt, tacticenv, time
from tactic_client_lib import TacticServerStub
server = TacticServerStub.get(protocol="xmlrpc")
orders = server.eval("@GET(twog/order['classification','not in','Completed|On Hold|Cancelled|Master'].code)")
for order in orders:
    print "ORDER = %s" % order
    all_done = True
    title_statuses = server.eval("@GET(twog/title['order_code','%s'].status)" % order)
    for ts in title_statuses:
        if ts != 'Completed':
            all_done = False
    if all_done and len(title_statuses) > 0:
        order_sk = server.build_search_key('twog/order', order)
        os.system('''echo 'update "order" set classification = "Completed" where code = "%s"' >> orders_to_complete''' % order)  
    
 
