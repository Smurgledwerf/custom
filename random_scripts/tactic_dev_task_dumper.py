import os, sys, math, hashlib, getopt, tacticenv
from tactic_client_lib import TacticServerStub
server = TacticServerStub.get()
dev_tasks = server.eval("@SOBJECT(tactic_dev/tasks)")
lines = 'Id\tCode\tName\tFunction\tAssigned\tStatus\tDescription\n'
file_name = 'Tactic_Dev_Tasks.tsv'
for dt in dev_tasks:
    assigned = ''
    status = ''
    task = server.eval("@SOBJECT(sthpw/task['project_code','tactic_dev']['search_id','%s'])" % dt.get('id'))
    if task:
        task = task[0]
        status = task.get('status')
        assigned = task.get('assigned')
    new_line = '%s\t%s\t%s\t%s\t%s\t%s\t%s' % (dt.get('id'), dt.get('code'), dt.get('name'), dt.get('function'), assigned, status, dt.get('description')) 
    lines = '%s\n%s' % (lines, new_line)
lines = lines.encode('utf-8') 
f= open(file_name, 'w')
f.write(lines)
f.close()
