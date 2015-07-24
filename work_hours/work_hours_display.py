__all__ = ["WorkHoursDisplayWdg"]
import tacticenv
from pyasm.common import Environment
from pyasm.biz import *
from pyasm.web import Table, DivWdg
from tactic.ui.common import BaseTableElementWdg
from tactic.ui.common import BaseRefreshWdg

class WorkHoursDisplayWdg(BaseTableElementWdg):
    def init(my):
        from client.tactic_client_lib import TacticServerStub
        my.server = TacticServerStub.get()
        my.login = Environment.get_login()
        my.user = my.login.get_login()
        my.task_code = ''
        my.task_codes = ''
        my.code = ''
    
    def toggle_hide(my, code):   # DOESN'T WORK IN TACTIC TABLE ROWS. WON'T EXPAND 
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                             code = '%s';
                             table = document.getElementsByClassName('whd_' + code)[0];
                             alert(table);
                             rows = table.getElementsByClassName('whdg_' + code);
                             alert(rows);
                             //deet = table.getElementsByClassName('deets_' + code)[0];
                             //alert(deet);
                             hid = false;
                             for(var r = 0; r < rows.length; r++){
                                 row = rows[r];
                                 if(row.style.display == 'none'){
                                     row.style.diplay = 'table-row';
                                 }else{
                                     row.style.display = 'none';
                                     hid = true;
                                 }
                             }
                             if(hid){
                                 bvr.src_el.innerHTML = '<u>Details</u>';
                             }else{
                                 bvr.src_el.innerHTML = '<u>Hide</u>';
                             }
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                          //alert(err);
                }
         ''' % (code)}
        return behavior

    def get_display(my):
        sobject = None
        lookup_code = ''
        if 'task_code' in my.kwargs.keys():
            my.task_code = str(my.kwargs.get('task_code'))
            my.code = my.task_code
        elif 'code' in my.kwargs.keys():
            my.code = str(my.kwargs.get('code'))
        else:
            sobject = my.get_current_sobject()
            my.code = sobject.get_code()
            if 'WORK_ORDER' in my.code:
                my.task_code = sobject.get_value('task_code')
            elif 'TASK' in my.code:
                my.task_code = sobject.get_value('code')
                my.code = my.task_code
                lookup_code = sobject.get_value('lookup_code')

        if 'WORK_ORDER' in my.code:
            my.work_order_code = my.code
            my.task_code = my.server.eval("@GET(twog/work_order['code','%s'].task_code)" % my.work_order_code)[0];
        elif 'PROJ' in my.code:
            tcs = my.server.eval("@GET(twog/proj['code','%s'].twog/work_order.WT:sthpw/task.code)" % my.code)
            my.task_codes = '|'.join(tcs)
        elif 'TITLE' in my.code:
            tcs = my.server.eval("@GET(twog/title['code','%s'].twog/proj.twog/work_order.WT:sthpw/task.code)" % my.code)
            my.task_codes = '|'.join(tcs)
        elif 'ORDER' in my.code:
            tcs = my.server.eval("@GET(twog/order['code','%s'].twog/title.twog/proj.twog/work_order.WT:sthpw/task.code)" % my.code)
            my.task_codes = '|'.join(tcs)
        elif 'STATUS_LOG' in my.code:
            my.task_code = sobject.get_value('task_code')
            my.code = my.task_code 
        elif 'TASK' in my.code:
            my.task_code = my.code
            if 'PROJ' in lookup_code:
                tcs = my.server.eval("@GET(twog/proj['code','%s'].twog/work_order.WT:sthpw/task.code)" % lookup_code)
                my.task_codes = '|'.join(tcs)
                my.task_code = ''
                  
        widget = DivWdg()
        table = Table()
        table.add_attr('class','whd_%s' % my.code)
        if my.task_code == -1 or my.task_code == '-1':
            sobject = my.get_current_sobject()
            my.task_code = sobject.get_code()
        elif my.task_code not in [None,'']:
            my.task_codes = my.task_code
        if my.task_codes not in [-1,'-1',None,'']:
                work_hours = None
		work_hours = my.server.eval("@SOBJECT(sthpw/work_hour['task_code','in','%s'])" % my.task_codes) # Instead, make task_code in list of task codes from order, title, proj, whatevs
		group_sums = {}
		user_sums = {}
		group_users = {}
		user_lines = {}
		total = 0
                saved_login_in_groups = {}
		for wh in work_hours:
		   login = wh.get('login')
		   straight_time = wh.get('straight_time')
                   work_description = wh.get('description')
		   if straight_time in [None,'']:
		       straight_time = 0
		   else:
		       straight_time = float(straight_time)
		   if login not in user_lines.keys():
		       user_lines[login] = []
		   login_sobj = my.server.eval("@SOBJECT(sthpw/login['login','%s'])" % login)
                   login_group = None
                   if login_sobj:
                       login_sobj = login_sobj[0]
		       login_group = login_sobj.get('default_group')
                   else:
		       login_sobj = my.server.eval("@SOBJECT(sthpw/login['login','%s'])" % login, show_retired=True)
                       if login_sobj:
                           login_sobj = login_sobj[0] 
		           login_group = login_sobj.get('default_group')
                       
		   if login == 'admin':
		       login_group = 'admin'
		   if login_group in [None,'']:
                       if login in saved_login_in_groups.keys():
                           login_group = saved_login_in_groups[login]
                       else:
		           login_in_groups = my.server.eval("@SOBJECT(sthpw/login_in_group['login','%s']['login_group','not in','client|user|vault'])" % login)
                           for lg in login_in_groups:
                               if login_group in [None,'']:
                                   login_group = lg.get('login_group')
                               if 'supervisor' in lg.get('login_group'):
                                   login_group = lg.get('login_group')
                           saved_login_in_groups[login] = login_group
                   else:
                       if login not in saved_login_in_groups.keys():
                           saved_login_in_groups[login] = login_group
		   if login_group not in group_users.keys():
		       group_users[login_group] = []
		   if login not in group_users[login_group]:
		       group_users[login_group].append(login)
		   if login not in user_sums.keys():
		       user_sums[login] = float(straight_time)
		   else:
		       user_sums[login] = float(user_sums[login]) + float(straight_time)
		   if login_group not in group_sums.keys():
		       group_sums[login_group] = float(straight_time)
		   else:
		       group_sums[login_group] = float(group_sums[login_group]) + float(straight_time)
		   total = total + float(straight_time)   
		   user_lines[login].append('%s %s <u>%s</u>: <b>%s</b> %s' % (wh.get('day').split(' ')[0], login_group, login, straight_time, work_description)) 
		   
		table.add_row()
		total_total = table.add_cell("<b>TOTAL: %s</b>" % total)
		total_total.add_attr('colspan','4')
		total_total.add_attr('align','left')
		total_total.add_attr('nowrap','nowrap')
		total_total.add_style('font-size: 16px;')
                table.add_cell(' ')
                #deets = table.add_cell('<u>Details</u>')
                #deets.add_attr('name','deets_%s' % my.code)
                #deets.add_style('cursor: pointer;')
                #deets.add_behavior(my.toggle_hide(my.code))
		groups = group_users.keys()
		for group in groups:
		    group_table = Table()
		    top_row = group_table.add_row()
                    top_row.add_style('display: table-row;')
		    gtc = group_table.add_cell('<b>Group "%s" Total: %s</b>' % (group, group_sums[group]))
		    gtc.add_attr('colspan','3')
		    gtc.add_attr('align','left')
		    gtc.add_attr('nowrap','nowrap')
		    gtc.add_style('font-size: 13px;')
		    for user in group_users[group]:
			user_table = Table()
			user_table.add_row() 
			lc = user_table.add_cell('<b>User "%s" Total: %s</b>' % (user, user_sums[user]))
			lc.add_attr('colspan','2')
			lc.add_attr('align','left')
			lc.add_attr('nowrap','nowrap')
			lc.add_style('font-size: 11px;')
			for line in user_lines[user]:
			    user_table.add_row()
			    user_table.add_cell('&nbsp;&nbsp;&nbsp;')
			    ll = user_table.add_cell(line)
			    ll.add_attr('align','left')
			    ll.add_attr('nowrap','nowrap')
			group_table.add_row()
			group_table.add_cell('&nbsp;&nbsp;&nbsp;')
			group_table.add_cell(user_table)
		    hider = table.add_row()
                    #hider.add_attr('class','whdg_%s' % my.code)
                    #hider.add_style('display: none;')
		    table.add_cell('&nbsp;&nbsp;&nbsp;')
		    table.add_cell(group_table)
        
        widget.add(table)
        return widget
        
        
