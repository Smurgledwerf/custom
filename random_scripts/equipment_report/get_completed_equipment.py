import os, sys, math, hashlib, getopt, tacticenv, time
from tactic_client_lib import TacticServerStub
server = TacticServerStub.get()
equipment = server.eval("@SOBJECT(twog/order['classification','Completed'].twog/title.twog/proj.twog/work_order.twog/equipment_used)")
bads = []
for eq in equipment:
    if eq.get('actual_duration') in [None,'']:
        if eq.get('expected_duration') not in [None,'']:
            print "update equipment_used set actual_duration = '%s' where code = '%s';" % (eq.get('expected_duration'), eq.get('code'))
        else:
            bads.append(eq.get('code'))
for bad in bads:
    print bad
