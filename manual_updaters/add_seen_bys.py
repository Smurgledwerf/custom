#NEED TO COLLECT ALL WORK HOURS AND REPORT THOSE UNCONNECTED TO WORK ORDERS AND TASKS, CONNECT THEM TO CLIENT AS WELL
import tacticenv
import os, sys, calendar, dateutil, datetime, time, getopt, pprint, re, math
from pyasm.biz import *


opts, login = getopt.getopt(sys.argv[1], '-m')
opts, codes_to_update = getopt.getopt(sys.argv[2], '-m')
opts, timestamp = getopt.getopt(sys.argv[3], '-m')
note_codes = codes_to_update.split(',')
make_ems = ''
seen_block = '[%s,%s]' % (login,timestamp)
for code in note_codes:
    if make_ems == '':
        make_ems = "update note set seen_by = 'SEEN:' where code = '%s' and (seen_by is NULL or seen_by = '');" % (code)
        make_ems = "%s\nupdate note set seen_by = seen_by || '%s' where code = '%s';" % (make_ems, seen_block, code)
    else:
        make_ems = "%s\nupdate note set seen_by = 'SEEN:' where code = '%s' and (seen_by is NULL or seen_by = '');" % (make_ems, code)
        make_ems = "%s\nupdate note set seen_by = seen_by || '%s' where code = '%s';" % (make_ems, seen_block, code)
note_updater_path = '/var/www/html/note_updating/%s_note_update.sql' % login
if os.path.exists(note_updater_path):
    os.system('rm -rf %s' % note_updater_path)
f = open(note_updater_path, 'w')
f.write(str(make_ems))
f.close()
os.system("psql -U postgres sthpw < '''%s'''" % note_updater_path) 
