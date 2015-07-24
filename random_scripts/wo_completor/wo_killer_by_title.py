import os, sys, getopt, tacticenv
from tactic_client_lib import TacticServerStub
server = TacticServerStub.get()
title_codes = ['TITLE21772']
seen_titles = []

print "BEGIN"
if len(sys.argv) > 1:
    print len(sys.argv)
    print "To kill work orders under some order, open this python script and insert the order codes you want the script to handle.\n"
    print "This will kill all incomplete work orders under the order"
else:
    for title_code in title_codes:
        if title_code not in seen_titles:
            print "TITLE_CODE = %s" % title_code
            expr = "@GET(twog/title['code','%s'].twog/proj.twog/work_order.WT:sthpw/task['status','!=','Completed'].lookup_code)" % title_code
            work_orders = server.eval(expr)
            seen_titles.append(title_code)
            try:
                for wo in work_orders:
                    wo_sk = server.build_search_key('twog/work_order', wo)
                    print wo_sk
                    server.delete_sobject(wo_sk)
            except:
                print "%s gave us some errors" % title_code               
                pass
        
                        
print "END"
































