import os, sys, math, hashlib, getopt, tacticenv
from tactic_client_lib import TacticServerStub
server = TacticServerStub.get(protocol="xmlrpc")
orders = server.eval("@SOBJECT(twog/order['classification','Completed'])")
for order in orders:
    wo_task_statuses = server.eval("@GET(twog/title['order_code','%s'].twog/proj.twog/work_order.WT:sthpw/task.status)" % order.get('code'))
    task_total = len(wo_task_statuses)
    incomplete = 0
    for wot in wo_task_statuses:
        if wot != 'Completed':
            incomplete = incomplete + 1
    bien_str = 'BAD'
    if incomplete == 0:
        bien_str = 'GOOD'
    closed_str = 'False'
    if order.get('closed'):
        closed_str = 'True'
    if incomplete > 0:
        print "%s   ORDER CODE = %s, Classification = %s, Closed = %s, Ratio=(%s/%s)" % (bien_str, order.get('code'), order.get('classification'), closed_str, (task_total - incomplete), task_total)
        

