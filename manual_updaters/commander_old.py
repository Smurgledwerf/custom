__all__ = ["ShrinkPrioritiesCmd","ClientBillingTaskVisibilityCmd","DBDirectCmd"]
import os
from pyasm.command import Command, CommandException

class ShrinkPrioritiesCmd(Command): 
    def execute(my):
        os.system('python /opt/spt/custom/manual_updaters/update_priorities.py > /tmp/prio_adj')

class ClientBillingTaskVisibilityCmd(Command): 
    def init(my):
        my.client_code = ''
        my.new_task_str = ''
    def execute(my):
        my.client_code = my.kwargs.get('client_code')
        my.new_task_str = my.kwargs.get('new_task_str')
        os.system('''python /opt/spt/custom/manual_updaters/update_task_client_hold.py '%s' '%s' > /tmp/task_adj''' % (my.client_code, my.new_task_str))

class DBDirectCmd(Command):
    def init(my):
        my.cmnd = ''
        my.which_db = ''

    def make_timestamp(my):
        #Makes a Timestamp for postgres
        #NEED TO GET RID OF THIS AND USE A PASSIN FROM KWARGS INSTEAD
        import datetime
        now = datetime.datetime.now()
        return now.strftime("%Y_%m_%d_%H_%M_%S")

    def execute(my):
        my.cmnd = my.kwargs.get('cmnd')
        my.which_db = my.kwargs.get('which_db')
        print "MY COMMAND = %s" % my.cmnd
        print "WHICH DB = %s" % my.which_db
        if my.cmnd not in [None,''] and my.which_db not in [None,'']:
            #NEED TO GET RID OF THIS AND USE A PASSIN FROM KWARGS INSTEAD
            #This is for avoiding collisions
            timestamp = my.make_timestamp()
            path_prefix = '/var/www/html/user_reports_tables/'
            the_file = '%sdb_direct_cmd_%s' % (path_prefix, timestamp)
            rez_file = '%sdb_direct_cmd_result_%s' % (path_prefix, timestamp)
            if os.path.exists(the_file):
                os.system('rm -rf %s' % the_file)
            new_guy = open(the_file, 'w')
            new_guy.write('%s\n' % my.cmnd)
            new_guy.close()
            print "GOT TO THE ACTION PART"
            os.system('''psql -U postgres %s < %s > %s''' % (my.which_db, the_file, rez_file))
        
         

