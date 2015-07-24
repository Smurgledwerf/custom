import os, sys, math, hashlib, getopt, tacticenv, time
from tactic_client_lib import TacticServerStub
server = TacticServerStub.get()
opts, order_code = getopt.getopt(sys.argv[1], '-m')
print "order_code = %s" % order_code
projs = server.eval("@SOBJECT(twog/title['order_code','%s'].twog/proj)" % order_code)
task_codes = []
task_info = {}
for proj in projs:
    ptask_code = proj.get('task_code')
    if ptask_code not in [None,'']:
        task_codes.append(ptask_code)
    wo_task_codes = server.eval("@GET(twog/work_order['proj_code','%s'].WT:sthpw/task.code)" % proj.get('code'))
    for wtc in wo_task_codes:
        if wtc not in [None,'']:
            task_codes.append(wtc)
for tcode in task_codes:
    print tcode

