import os, sys, getopt, tacticenv
from tactic_client_lib import TacticServerStub
server = TacticServerStub.get()
order_codes = []
print "BEGIN"
if len(sys.argv) > 1:
    print len(sys.argv)
    print "To kill work orders under some order, open this python script and insert the order codes you want the script to handle.\n"
    print "This will kill all incomplete work orders under the order"
else:
    for order_code in order_codes:
        print "ORDER_CODE = %s" % order_code
        work_orders = server.eval("@GET(twog/order['code','%s'].twog/title.twog/proj.twog/work_order.sthpw/task['status','!=','Completed'].lookup_code)" % order_code)
        try:
            for wo in work_orders:
                wo_sk = server.build_search_key('twog/work_order', wo)
                print wo_sk
                #server.delete_sobject(wo_sk)
        except:
            print "%s gave us some errors" % order_code               
            pass
                        
print "END"
































