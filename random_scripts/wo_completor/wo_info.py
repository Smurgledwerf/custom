import os, sys, math, hashlib, getopt, tacticenv, time
from tactic_client_lib import TacticServerStub
server = TacticServerStub.get()

expr = "@SOBJECT(sthpw/task['assigned_login_group','%s']['status','%s'])" % ('qc','Completed')
tasks = server.eval(expr)
process_info = {}
processes = []
for task in tasks:
    if 'WORK_ORDER' in task.get('lookup_code'):
        process = task.get('process')
        assigned = task.get('assigned')
        wo_code = task.get('lookup_code')
        order = server.eval("@SOBJECT(twog/work_order['code','%s'].twog/proj.twog/title.twog/order)" % wo_code)
        classification = ''
        if order:
            order = order[0]
            classification = order.get('classification')
        if classification == 'Completed':
            if process not in process_info.keys():
                process_info[process] = {'count': 0, 'user_assigned_count': {}, 'hours': 0.0, 'with_hours': 0, 'no_hours': 0}
                processes.append(process)
            process_info[process]['count'] = process_info[process]['count'] + 1
            if assigned not in process_info[process]['user_assigned_count'].keys():
                process_info[process]['user_assigned_count'][assigned] = 0
            process_info[process]['user_assigned_count'][assigned] = process_info[process]['user_assigned_count'][assigned] + 1
            work_hours = server.eval("@SOBJECT(sthpw/work_hour['task_code','%s'])" % task.get('code'))
            booled = False
            for wh in work_hours:
                process_info[process]['hours'] = float(process_info[process]['hours']) + float(wh.get('straight_time'))
                booled = True
            if booled:
                process_info[process]['with_hours'] = process_info[process]['with_hours'] + 1
            else:
                process_info[process]['no_hours'] = process_info[process]['no_hours'] + 1

print "WO NAME,Total Hours,Avg Hours,Count,With Hours,No Hours,User Counts"
processes.sort()
for p in processes:
    total_hours = process_info[p]['hours']
    count = process_info[p]['count']
    with_hours = process_info[p]['with_hours']
    no_hours = process_info[p]['no_hours']
    avg_hours = 0
    if with_hours > 0:
        avg_hours = float(float(total_hours)/float(with_hours))
    user_count = process_info[p]['user_assigned_count']
    uc_keys = user_count.keys()
    uc_keys.sort()
    user_str = ''
    for uc in uc_keys:
        if user_str == '':
            user_str = '[ %s: %s ]' % (uc, user_count[uc]) 
        else:
            user_str = '%s[ %s: %s ]' % (user_str, uc, user_count[uc]) 
    #print "%s ::> Total Hours: %s, Avg Hours: %s, Count: %s, With Hours: %s, No Hours: %s, User Counts: %s" % (p, total_hours, avg_hours, count, with_hours, no_hours, user_str)
    print "%s,%s,%s,%s,%s,%s,%s" % (p, total_hours, avg_hours, count, with_hours, no_hours, user_str)
    

































