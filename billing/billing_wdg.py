__all__ = ["BillingLauncherWdg","BillingWdg"]
import tacticenv, re
from pyasm.common import Environment
from pyasm.biz import *
from pyasm.web import Table, DivWdg
from pyasm.widget import SelectWdg, IconWdg, TextWdg, CheckboxWdg
from tactic.ui.common import BaseTableElementWdg
from tactic.ui.common import BaseRefreshWdg
from tactic.ui.widget import DiscussionWdg

class BillingLauncherWdg(BaseTableElementWdg):

    def init(my):
        nothing = 'true'
        my.server = None
        my.login = Environment.get_login()
        my.groups_arr = Environment.get_group_names()
        my.groups_str = ''
        for guy in my.groups_arr:
            if my.groups_str == '':
                my.groups_str = guy
            else:
                my.groups_str = '%s,%s' % (my.groups_str, guy)
        my.user_name = my.login.get_login()

    def get_stub(my):
        from tactic_client_lib import TacticServerStub
        my.server = TacticServerStub.get()
    
    def get_launch_behavior(my, order_name):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                          var order_name = '%s';
                          var my_sk = bvr.src_el.get('sk');
                          var my_code = my_sk.split('code=')[1];
                          var my_user = bvr.src_el.get('user');
                          var my_groups = bvr.src_el.get('groups');
                          var class_name = 'billing.billing_wdg.BillingWdg';
                          kwargs = {
                                           'sk': my_sk,
                                           'user': my_user,
                                           'groups': my_groups,
                                           'code': my_code,
                                           'order_name': order_name
                                   };
                          spt.panel.load_popup('Billing View for ' + order_name, class_name, kwargs);
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         ''' % order_name}
        return behavior

    def get_display(my):
        expression_lookup = {'twog/order': "@SOBJECT(twog/order['code','REPLACE_ME'])", 'twog/title': "@SOBJECT(twog/title['code','REPLACE_ME'].twog/order)", 'twog/proj': "@SOBJECT(twog/proj['code','REPLACE_ME'].twog/title.twog/order)", 'twog/work_order': "@SOBJECT(twog/work_order['code','REPLACE_ME'].twog/proj.twog/title.twog/order)", 'twog/equipment_used': "@SOBJECT(twog/equipment_used['code','REPLACE_ME'].twog/work_order.twog/proj.twog/title.twog/order)"}
        search_type = 'twog/order'
        code = ''
        order_name = ''
        sob_sk = ''
        if 'search_type' in my.kwargs.keys():
            my.get_stub()
            search_type = str(my.kwargs.get('search_type'))
            code = str(my.kwargs.get('code'))
            sobject = my.server.eval(expression_lookup[search_type].replace('REPLACE_ME',code))
            if sobject:
                sobject = sobject[0]
                code = sobject.get('code')
                sob_sk = sobject.get('__search_key__')
                order_name = sobject.get('name')
        else: 
            sobject = my.get_current_sobject()
            code = sobject.get_code()
            not_order = False
            if 'WORK_ORDER' in code:
                my.get_stub()
                sobject = my.server.eval(expression_lookup['twog/work_order'].replace('REPLACE_ME',code))
                not_order = True
            elif 'EQUIPMENT_USED' in code:
                my.get_stub()
                sobject = my.server.eval(expression_lookup['twog/equipment_used'].replace('REPLACE_ME',code))
                not_order = True
            elif 'PROJ' in code:
                my.get_stub()
                sobject = my.server.eval(expression_lookup['twog/proj'].replace('REPLACE_ME',code))
                not_order = True
            elif 'TITLE' in code: 
                my.get_stub()
                sobject = my.server.eval(expression_lookup['twog/title'].replace('REPLACE_ME',code))
                not_order = True
            elif 'PRODUCTION_ERROR' in code:
                my.get_stub()
                wo_code = sobject.get_value('work_order_code')
                sobject = my.server.eval(expression_lookup['twog/work_order'].replace('REPLACE_ME',wo_code)) 
                not_order = True
            else:
                order_name = sobject.get_value('name')
                sob_sk = sobject.get_search_key()
            if not_order:
                if sobject:
                    sobject = sobject[0]
                    code = sobject.get('code')
                    sob_sk = sobject.get('__search_key__')
                    order_name = sobject.get('name')
        widget = DivWdg()
        table = Table()
        table.add_attr('width', '50px')
        table.add_row()
        cell1 =  table.add_cell('<img border="0" style="vertical-align: middle" title="" src="/context/icons/custom/dollar.png">')
        cell1.add_attr('sk', sob_sk)
        cell1.add_attr('user', my.user_name)
        launch_behavior = my.get_launch_behavior(order_name)
        cell1.add_style('cursor: pointer;')
        cell1.add_behavior(launch_behavior)
        widget.add(table)

        return widget

class BillingWdg(BaseRefreshWdg):
    def init(my):
        from client.tactic_client_lib import TacticServerStub
        from pyasm.common import Environment
        my.server = TacticServerStub.get()
        my.sk = ''
        my.user = ''
        my.groups = ''
        my.login_group_rates = {}

    def fix_date(my, date):
        #This is needed due to the way Tactic deals with dates (using timezone info), post v4.0
        from pyasm.common import SPTDate
        return_date = ''
        date_obj = SPTDate.convert_to_local(date)
        if date_obj not in [None,'']:
            return_date = date_obj.strftime("%Y-%m-%d  %H:%M")
        return return_date
   
    def get_fk_code_multi_look_dict(my, dikshunarry, which_code):
        new_dict = {}
        for dude in dikshunarry:
            what_code = dude.get(which_code)
            if what_code not in new_dict.keys():
                new_dict[what_code] = []
            new_dict[what_code].append(dude)
        return new_dict

    def get_code_look_dict(my, dikshunarry, which_code):
        new_dict = {}
        for dude in dikshunarry:
            what_code = dude.get(which_code)
            if what_code not in new_dict.keys():
                new_dict[what_code] = dude
        return new_dict

    def get_info(my, code):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                          var code = '%s';
                          var class_name = 'work_hours.work_hours_display.WorkHoursDisplayWdg';
                          kwargs = {
                                           'code': code
                                   };
                          spt.panel.load_popup('Work Hours Info for ' + code, class_name, kwargs);
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         ''' % code}
        return behavior

    def has_letters(my, c):
        return re.search('[a-zA-Z ]', c)
    
    def make_number(my, c):
        ret_val = 0.0
        if c not in [None,'']:
            c = '%s' % c
            c = c.replace(',','').replace(' ','') 
            if my.has_letters(c):
                ret_val = 0.0
            else:
                ret_val = float(c)
        return ret_val

    def make_number_disp(my, c):
        thing = my.make_number(c)
        ret_str = '0.0'
        if thing > 0:
            ret_str = '%.2f' % thing
        return ret_str
  
    def make_hours_tbl(my, dict, code):
        table = Table()
        table.add_attr('cellspacing','3')
        table.add_attr('cellpadding','3')
        eq_tbl = Table()
        eq_tbl.add_attr('cellspacing','3')
        eq_tbl.add_attr('cellpadding','3')
        eq_tbl.add_attr('border','1')
        eq_tbl.add_style('background-color: #e4e4e4;')
        eq = dict['eq']
        t_act_hours = 0
        t_act_size = 0
        t_act_els = 0
        t_act_cost = 0
        t_est_hours = 0
        t_est_size = 0
        t_est_els = 0
        t_est_cost = 0
        for name in eq.keys():
            piece = eq[name]
            r1 = eq_tbl.add_row()
            eq_tbl.add_cell('<b>Name:</b>')
            c1 = eq_tbl.add_cell('<b>%s</b>' % name)
            c1.add_attr('colspan','4')
            eq_tbl.add_row()
            eq_tbl.add_cell('')
            eq_tbl.add_cell('Hours')
            eq_tbl.add_cell('Size')
            eq_tbl.add_cell('Elements')
            eq_tbl.add_cell('Cost')
            r2 = eq_tbl.add_row()
            r2.add_style('background-color: #dd8c98;')
            eq_tbl.add_cell('Actual: ')
            eq_tbl.add_cell(my.make_number_disp(piece['actual']['hrs']))
            eq_tbl.add_cell('%s GB' % my.make_number_disp(piece['actual']['size']))
            eq_tbl.add_cell(my.make_number_disp(piece['actual']['tapes']))
            eq_tbl.add_cell('$%s' % my.make_number_disp(piece['actual']['cost']))
            r3 = eq_tbl.add_row()
            r3.add_style('background-color: #c2c2e8;')
            eq_tbl.add_cell('Estimated: ')
            eq_tbl.add_cell(my.make_number_disp(piece['estimated']['hrs']))
            eq_tbl.add_cell('%s GB' % my.make_number_disp(piece['estimated']['size']))
            eq_tbl.add_cell(my.make_number_disp(piece['estimated']['tapes']))
            eq_tbl.add_cell('$%s' % my.make_number_disp(piece['estimated']['cost']))
            t_act_hours = t_act_hours + piece['actual']['hrs']
            t_act_size = t_act_size + piece['actual']['size']
            t_act_els = t_act_els + piece['actual']['tapes']
            t_act_cost = t_act_cost + piece['actual']['cost']
            t_est_hours = t_est_hours + piece['estimated']['hrs']
            t_est_size = t_est_size + piece['estimated']['size']
            t_est_els = t_est_els + piece['estimated']['tapes']
            t_est_cost = t_est_cost + piece['estimated']['cost']
        gtbl = Table()
        gtbl.add_attr('cellspacing','3')
        gtbl.add_attr('cellpadding','3')
        gtbl.add_attr('border','1')
        gtbl.add_style('background-color: #e4e4e4;')
        gtbl.add_row()
        gtbl.add_cell('<b>Group</b>')
        ccc1 = gtbl.add_cell('Actual Hrs')
        ccc1.add_style('background-color: #dd8c98;')
        ccc2 = gtbl.add_cell('Actual Cost')
        ccc2.add_style('background-color: #dd8c98;')
        ccc3 = gtbl.add_cell('Estimated Hrs')
        ccc3.add_style('background-color: #c2c2e8;')
        ccc4 = gtbl.add_cell('Estimated Cost')
        ccc4.add_style('background-color: #c2c2e8;')
        groups = dict['groups']
        tg_act_hours = 0
        tg_act_cost = 0
        tg_est_hours = 0
        tg_est_cost = 0
        for group in groups.keys():
            gel = groups[group]
            gtbl.add_row()
            gtbl.add_cell('<b>%s</b>' % group)
            cc1 = gtbl.add_cell('%s' % my.make_number_disp(gel['actual']))
            cc1.add_style('background-color: #dd8c98;')
            cc2 = gtbl.add_cell('$%s' % my.make_number_disp(gel['actual_cost']))
            cc2.add_style('background-color: #dd8c98;')
            cc3 = gtbl.add_cell('%s' % my.make_number_disp(gel['estimated']))
            cc3.add_style('background-color: #c2c2e8;')
            cc4 = gtbl.add_cell('$%s' % my.make_number_disp(gel['estimated_cost']))
            cc4.add_style('background-color: #c2c2e8;')
            tg_act_hours = tg_act_hours + my.make_number(gel['actual'])
            tg_act_cost = tg_act_cost + my.make_number(gel['actual_cost'])
            tg_est_hours = tg_est_hours + my.make_number(gel['estimated'])
            tg_est_cost = tg_est_cost + my.make_number(gel['estimated_cost'])
            
            
        utbl = Table()
        utbl.add_attr('cellspacing','3')
        utbl.add_attr('cellpadding','3')
        utbl.add_attr('border','1')
        utbl.add_style('background-color: #e4e4e4;')
        utbl.add_row()
        utbl.add_cell('<b>Employee</b>')
        utbl.add_cell('Hrs')
        users = dict['users']
        total_hours = 0
        for user in users.keys():
            hrs = users[user]
            if hrs in [None,'']:
                hrs = 0
            utbl.add_row()
            utbl.add_cell('<b>%s</b>' % user)
            utbl.add_cell('%.3f' % my.make_number(hrs))
            total_hours = total_hours + my.make_number(hrs)
            


        t_eqtbl = Table()
        t_eqtbl.add_attr('border','1')
        t_eqtbl.add_style('background-color: #e4e4e4;')
        t_eqtbl.add_row()
        t_eqtbl.add_cell('<b>Total</b>')
        t_eqtbl.add_cell('Hours')
        t_eqtbl.add_cell('Size')
        t_eqtbl.add_cell('Elements')
        t_eqtbl.add_cell('Cost')
        t_eqtbl.add_row()
        a1 = t_eqtbl.add_cell('<b>Actual</b>')
        a1.add_style('background-color: #dd8c98;')
        a2 = t_eqtbl.add_cell('%s' % my.make_number_disp(t_act_hours))
        a2.add_style('background-color: #dd8c98;')
        a3 = t_eqtbl.add_cell('%s GB' % my.make_number_disp(t_act_size))
        a3.add_style('background-color: #dd8c98;')
        a4 = t_eqtbl.add_cell('%s' % my.make_number_disp(t_act_els))
        a4.add_style('background-color: #dd8c98;')
        a5 = t_eqtbl.add_cell('$%.2f' % t_act_cost)
        a5.add_style('background-color: #dd8c98;')
        t_eqtbl.add_row()
        e1 = t_eqtbl.add_cell('<b>Estimated</b>')
        e1.add_style('background-color: #c2c2e8;')
        e2 = t_eqtbl.add_cell('%s' % my.make_number_disp(t_est_hours))
        e2.add_style('background-color: #c2c2e8;')
        e3 = t_eqtbl.add_cell('%s GB' % my.make_number_disp(t_est_size))
        e3.add_style('background-color: #c2c2e8;')
        e4 = t_eqtbl.add_cell('%s' % my.make_number_disp(t_est_els))
        e4.add_style('background-color: #c2c2e8;')
        e5 = t_eqtbl.add_cell('$%.2f' % t_est_cost)
        e5.add_style('background-color: #c2c2e8;')

        tg = Table()
        tg.add_attr('border','1')
        tg.add_style('background-color: #e4e4e4;')
        tg.add_row()
        tg.add_cell('<b>Total</b>')
        tg1 = tg.add_cell('Actual Hrs')
        tg1.add_style('background-color: #dd8c98;')
        tg2 = tg.add_cell('Actual Cost')
        tg2.add_style('background-color: #dd8c98;')
        tg3 = tg.add_cell('Estimated Hrs')
        tg3.add_style('background-color: #c2c2e8;')
        tg4 = tg.add_cell('Estimated Cost')
        tg4.add_style('background-color: #c2c2e8;')
        tg.add_row()
        tg0 = tg.add_cell('<b>All Groups:</b>')
        tg5 = tg.add_cell(my.make_number_disp(tg_act_hours))
        tg5.add_style('background-color: #dd8c98;')
        tg6 = tg.add_cell('$%s' % my.make_number_disp(tg_act_cost))
        tg6.add_style('background-color: #dd8c98;')
        tg7 = tg.add_cell(my.make_number_disp(tg_est_hours))
        tg7.add_style('background-color: #c2c2e8;')
        tg8 = tg.add_cell('$%s' % my.make_number_disp(tg_est_cost))
        tg8.add_style('background-color: #c2c2e8;')
        
        table.add_row()
        t1 = table.add_cell(eq_tbl)
        t1.add_attr('valign','top')
        t2 = table.add_cell(gtbl)
        t2.add_attr('valign','top')
        t3 = table.add_cell(utbl)
        t3.add_attr('valign','top')
        t4 = table.add_cell('<img border="0" style="vertical-align: middle" title="Inspect" name="Inspect" src="/context/icons/silk/information.png">')
        t4.add_attr('valign','top')
        t4.add_style('cursor: pointer;')
        wh_info_bvr = my.get_info(code)
        t4.add_behavior(wh_info_bvr)
        table.add_row()
        t5 = table.add_cell(t_eqtbl)
        t5.add_attr('valign','top')
        t6 = table.add_cell(tg)
        t6.add_attr('valign','top')
        t7 = table.add_cell('<b>Total Employee Hours:</b> %.3f' % my.make_number(total_hours))
        t7.add_attr('valign','top')
  
        return table
    
    def get_hide_unhide(my, code):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                          var code = '%s';
                          var row = document.getElementById('billing_' + code);
                          if(row.style.display == 'none'){
                              row.style.display = 'table-row';
                          }else{
                              row.style.display = 'none';
                          }
                          
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                          //alert(err);
                }
        ''' % code}
        return behavior

    def get_display(my):   
        from uploader import CustomHTML5UploadButtonWdg
        from order_builder import OrderBuilderLauncherWdg
        my.sk = str(my.kwargs.get('sk'))
        my.groups = str(my.kwargs.get('groups'))
        my.user = str(my.kwargs.get('user'))
        my.code = my.sk.split('code=')[1]
        my.order_code = my.code
        wo_to_title_dict = {}
        order_hours = {'groups': {}, 'users': {}, 'eq': {}} 
        title_hours = {}
        sob_expr = "@SOBJECT(twog/order['code','%s'])" % my.code
        order = my.server.eval(sob_expr)[0]
        titles = my.server.eval("@SOBJECT(twog/title['order_code','%s'])" % my.code)
        work_orders = my.server.eval("@SOBJECT(twog/work_order['order_code','%s'])" % my.code)
        tasks = my.server.eval("@SOBJECT(sthpw/task['order_code','%s']['search_type','twog/proj?project=twog'])" % my.code)
        task_lookup = my.get_code_look_dict(tasks, 'code')
        equipment = my.server.eval("@SOBJECT(twog/work_order['order_code','%s'].twog/equipment_used)" % my.code)
        login_groups_rez = my.server.eval("@SOBJECT(sthpw/login_group)")
        for login_group in login_groups_rez:
            if login_group.get('login_group') not in my.login_group_rates.keys():
                hourly_rate = login_group.get('hourly_rate')
                if hourly_rate in [None,'']:
                    hourly_rate = 0
                else:
                    hourly_rate = float(hourly_rate)
                my.login_group_rates[login_group.get('login_group')] = hourly_rate
        wo_eq = my.get_fk_code_multi_look_dict(equipment, 'work_order_code')
        for work_order in work_orders:
            wo_code = work_order.get('code')
            title_code = work_order.get('title_code')
            if wo_code not in wo_to_title_dict.keys():
                wo_to_title_dict[wo_code] = title_code
            if title_code not in title_hours.keys():
                title_hours[title_code] = {'groups': {}, 'users': {}, 'eq': {}}
            task = task_lookup[work_order.get('task_code')]
            whs = my.server.eval("@SOBJECT(sthpw/work_hour['task_code','%s'])" % task.get('code'))
            #assined login group comes from the task
            assigned_login_group = task.get('assigned_login_group')
            if assigned_login_group not in order_hours['groups'].keys():
                order_hours['groups'][assigned_login_group] = {'actual': 0, 'actual_cost': 0, 'estimated': 0, 'estimated_cost': 0}
            if assigned_login_group not in title_hours[title_code]['groups'].keys():
                title_hours[title_code]['groups'][assigned_login_group] = {'actual': 0, 'actual_cost': 0, 'estimated': 0, 'estimated_cost': 0}
            estimated_work_hours = work_order.get('estimated_work_hours')
            if estimated_work_hours not in [None,'','N/A']:
                estimated_work_hours = float(estimated_work_hours)
            else:
                estimated_work_hours = 0
            title_hours[title_code]['groups'][assigned_login_group]['estimated'] = title_hours[title_code]['groups'][assigned_login_group]['estimated'] + estimated_work_hours 
            title_hours[title_code]['groups'][assigned_login_group]['estimated_cost'] = title_hours[title_code]['groups'][assigned_login_group]['estimated'] * my.login_group_rates[assigned_login_group] 
            order_hours['groups'][assigned_login_group]['estimated'] = order_hours['groups'][assigned_login_group]['estimated'] + estimated_work_hours 
            order_hours['groups'][assigned_login_group]['estimated_cost'] = order_hours['groups'][assigned_login_group]['estimated'] * my.login_group_rates[assigned_login_group] 
            for wh in whs:
                user = wh.get('login')
                straight_time = wh.get('straight_time')
                order_hours['groups'][assigned_login_group]['actual'] = order_hours['groups'][assigned_login_group]['actual'] + straight_time
                order_hours['groups'][assigned_login_group]['actual_cost'] = order_hours['groups'][assigned_login_group]['actual'] * my.login_group_rates[assigned_login_group] 
                title_hours[title_code]['groups'][assigned_login_group]['actual'] = title_hours[title_code]['groups'][assigned_login_group]['actual'] + straight_time
                title_hours[title_code]['groups'][assigned_login_group]['actual_cost'] = title_hours[title_code]['groups'][assigned_login_group]['actual'] * my.login_group_rates[assigned_login_group] 
                if user not in order_hours['users'].keys():
                    order_hours['users'][user] = 0
                order_hours['users'][user] = order_hours['users'][user] + straight_time
                if user not in title_hours[title_code]['users'].keys():
                    title_hours[title_code]['users'][user] = 0
                title_hours[title_code]['users'][user] = title_hours[title_code]['users'][user] + straight_time
            eqs = []
            try:
                eqs = wo_eq[wo_code]
            except:
                pass
            for eq in eqs:
                name = eq.get('name')
                units = eq.get('units')
                actual_duration = eq.get('actual_duration') 
                actual_cost = eq.get('actual_cost') 
                actual_quantity = eq.get('actual_quantity')
                expected_duration = eq.get('expected_duration')
                expected_cost = eq.get('expected_cost')
                expected_quantity = eq.get('expected_quantity')
                if name not in title_hours[title_code]['eq'].keys():
                    title_hours[title_code]['eq'][name] =  {'actual': {'hrs': 0, 'size': 0, 'tapes': 0, 'cost': 0}, 'details': [], 'estimated': {'hrs': 0, 'size': 0, 'tapes': 0, 'cost': 0}}
                if name not in order_hours['eq'].keys():
                    order_hours['eq'][name] = {'actual': {'hrs': 0, 'size': 0, 'tapes': 0, 'cost': 0}, 'details': [], 'estimated': {'hrs': 0, 'size': 0, 'tapes': 0, 'cost': 0}}
                if units in ['mb','gb','tb']:
                    new_gb = actual_duration
                    if new_gb in [None,'']:
                        new_gb = 0
                    if units == 'mb':
                        new_gb = new_gb/1000
                    if units == 'tb':
                        new_gb = new_gb * 1000
                    ex_gb = expected_duration
                    if ex_gb in [None,'']:
                        ex_gb = 0
                    if units == 'mb':
                        ex_gb = ex_gb/1000
                    if units == 'tb':
                        ex_gb = ex_gb * 1000
                    units = 'gb'
                    if actual_cost in [None,'']:
                        actual_cost = 0
                    if expected_cost in [None,'']:
                        expected_cost = 0
                    title_hours[title_code]['eq'][name]['actual']['size'] = new_gb + title_hours[title_code]['eq'][name]['actual']['size']
                    title_hours[title_code]['eq'][name]['actual']['cost'] = actual_cost + title_hours[title_code]['eq'][name]['actual']['cost']
                    order_hours['eq'][name]['actual']['size'] = new_gb + order_hours['eq'][name]['actual']['size']
                    order_hours['eq'][name]['actual']['cost'] = actual_cost + order_hours['eq'][name]['actual']['cost']
                    title_hours[title_code]['eq'][name]['estimated']['size'] = ex_gb + title_hours[title_code]['eq'][name]['estimated']['size']
                    title_hours[title_code]['eq'][name]['estimated']['cost'] = expected_cost + title_hours[title_code]['eq'][name]['estimated']['cost']
                    order_hours['eq'][name]['estimated']['size'] = ex_gb + order_hours['eq'][name]['estimated']['size']
                    order_hours['eq'][name]['estimated']['cost'] = expected_cost + order_hours['eq'][name]['estimated']['cost']
                elif units == 'length':
                    if expected_cost in [None,'']:
                        expected_cost = 0
                    if expected_quantity in [None,'',0]:
                        expected_quantity = 1
                    if actual_quantity in [None,'',0]:
                        actual_quantity = 1
                    if actual_cost in [None,'']:
                        actual_cost = expected_cost 
                    title_hours[title_code]['eq'][name]['actual']['tapes'] = title_hours[title_code]['eq'][name]['actual']['tapes'] + actual_quantity
                    title_hours[title_code]['eq'][name]['actual']['cost'] = actual_cost + title_hours[title_code]['eq'][name]['actual']['cost']
                    order_hours['eq'][name]['actual']['tapes'] = order_hours['eq'][name]['actual']['tapes'] + actual_quantity
                    order_hours['eq'][name]['actual']['cost'] = actual_cost + order_hours['eq'][name]['actual']['cost']
                    title_hours[title_code]['eq'][name]['estimated']['tapes'] = title_hours[title_code]['eq'][name]['estimated']['tapes'] + expected_quantity
                    title_hours[title_code]['eq'][name]['estimated']['cost'] = expected_cost + title_hours[title_code]['eq'][name]['estimated']['cost']
                    order_hours['eq'][name]['estimated']['tapes'] = order_hours['eq'][name]['estimated']['tapes'] + expected_quantity
                    order_hours['eq'][name]['estimated']['cost'] = expected_cost + order_hours['eq'][name]['estimated']['cost']
                elif units in ['items','hr']:
                    if actual_cost in [None,'']:
                        actual_cost = 0
                    if expected_cost in [None,'']:
                        expected_cost = 0
                    if expected_quantity in [None,'',0]:
                        expected_quantity = 0
                    if expected_duration in [None,'',0]:
                        expected_duration = 0
                    if actual_duration in [None,'',0]:
                        actual_duration = 0
                    expected_adder = 0
                    actual_adder = 0
                    if actual_quantity in [None,'',0] and units == 'items':
                        actual_quantity = expected_quantity
                    else:
                        actual_quantity = 0
                    if units == 'items':
                        expected_adder = expected_quantity
                        actual_adder = actual_quantity
                    else:
                        expected_adder = expected_duration
                        actual_adder = actual_duration
                       
                    title_hours[title_code]['eq'][name]['actual']['hrs'] = title_hours[title_code]['eq'][name]['actual']['hrs'] + actual_adder
                    title_hours[title_code]['eq'][name]['actual']['cost'] = actual_cost + title_hours[title_code]['eq'][name]['actual']['cost']
                    order_hours['eq'][name]['actual']['hrs'] = order_hours['eq'][name]['actual']['hrs'] + actual_adder
                    order_hours['eq'][name]['actual']['cost'] = actual_cost + order_hours['eq'][name]['actual']['cost']
                    title_hours[title_code]['eq'][name]['estimated']['hrs'] = title_hours[title_code]['eq'][name]['estimated']['hrs'] + expected_adder
                    title_hours[title_code]['eq'][name]['estimated']['cost'] = expected_cost + title_hours[title_code]['eq'][name]['estimated']['cost']
                    order_hours['eq'][name]['estimated']['hrs'] = order_hours['eq'][name]['estimated']['hrs'] + expected_adder
                    order_hours['eq'][name]['estimated']['cost'] = expected_cost + order_hours['eq'][name]['estimated']['cost']
                eq['units'] = units
                eq['actual_duration'] = actual_duration 
                eq['actual_quantity'] = actual_quantity 
                eq['actual_cost'] = actual_cost
                eq['expected_duration'] = expected_duration 
                eq['expected_quantity'] = expected_quantity 
                eq['expected_cost'] = expected_cost
                title_hours[title_code]['eq'][name]['details'].append(eq)
                order_hours['eq'][name]['details'].append(eq)
        widget = DivWdg()
        table = Table()
        otbl = Table()
        otbl.add_attr('cellspacing','3')
        otbl.add_attr('cellpadding','3')
        #otbl.add_attr('bgcolor','#d9edf7')
        otbl.add_style('background-color: #d9edf7;')
        otbl.add_style('border-bottom-right-radius', '10px')
        otbl.add_style('border-bottom-left-radius', '10px')
        otbl.add_style('border-top-right-radius', '10px')
        otbl.add_style('border-top-left-radius', '10px')
        hide_unhide_bvr = my.get_hide_unhide(order.get('code'))
        otbl.add_behavior(hide_unhide_bvr)
        botbl = Table()
        botbl.add_attr('cellspacing','3')
        botbl.add_attr('cellpadding','3')
        botbl.add_row()
        bo1 = botbl.add_cell("<b>Name:</b> %s " % order.get('name'))
        bo1.add_attr('nowrap','nowrap')
        bo2 = botbl.add_cell('<b>Scheduler:</b> %s ' % order.get('login'))
        bo2.add_attr('nowrap','nowrap')
        botbl.add_cell('<b>Sales Rep:</b> %s ' % order.get('sales_rep'))
        bo2.add_attr('nowrap','nowrap')
        botbl.add_row()
        bo3 = botbl.add_cell('<b>Code:</b> %s ' % my.code)
        bo3.add_attr('nowrap','nowrap')
        bo4 = botbl.add_cell('<b>PO#:</b> %s ' % order.get('po_number'))
        bo4.add_attr('nowrap','nowrap')
        bo5 = botbl.add_cell('<b>Classification:</b> %s ' % order.get('classification'))
        bo5.add_attr('nowrap','nowrap')
        botbl.add_row()
        uploader = CustomHTML5UploadButtonWdg(sk=order.get('__search_key__'))
        liltbl = Table()
        liltbl.add_row()
        liltbl.add_cell(uploader)
        ob_button = OrderBuilderLauncherWdg(code=my.code)
        liltbl.add_cell(ob_button)
        bo6 = botbl.add_cell(liltbl)
        bo7 = botbl.add_cell('<b>Client:</b> %s ' % order.get('client_name'))
        bo7.add_attr('nowrap','nowrap')
        
        client_rep = order.get('client_rep')
        cr = my.server.eval("@SOBJECT(twog/person['code','%s'])" % client_rep)
        if cr:
            cr = cr[0]
            client_rep = '%s %s' % (cr.get('first_name'), cr.get('last_name'))
        bo8 = botbl.add_cell('<b>Client Rep:</b> %s ' % client_rep)
        bo8.add_attr('nowrap','nowrap')
        dtbl = Table()
        dtbl.add_attr('cellspacing','3')
        dtbl.add_attr('cellpadding','3')
        dtbl.add_row()
        d1 = dtbl.add_cell('<b>Start Date:</b> %s ' % my.fix_date(order.get('start_date')))
        d1.add_attr('nowrap','nowrap')
        dtbl.add_row()
        d2 = dtbl.add_cell('<b>Due Date:</b> %s ' % my.fix_date(order.get('due_date')))
        d2.add_attr('nowrap','nowrap')
        dtbl.add_row()
        d3 = dtbl.add_cell('<b>Completion Date:</b> %s ' % my.fix_date(order.get('completion_date')))
        d3.add_attr('nowrap','nowrap')
        dtbl.add_row()
        d4 = dtbl.add_cell('<b>Billed Date:</b> %s ' % my.fix_date(order.get('billed_date')))
        d4.add_attr('nowrap','nowrap')
        dtbl.add_row()
        d5 = dtbl.add_cell('<b>Invoiced Date:</b> %s ' % my.fix_date(order.get('invoiced_date')))
        d5.add_attr('nowrap','nowrap')
        ctbl = Table()
        ctbl.add_attr('cellspacing','3')
        ctbl.add_attr('cellpadding','3')
        ctbl.add_row()
        c1 = ctbl.add_cell('<b>Completion Ratio:</b> %s/%s ' % (order.get('wo_completed'), order.get('wo_count')))
        c1.add_attr('nowrap','nowrap')
        ctbl.add_row()
        o_expected_cost = my.make_number(order.get('expected_cost'))
        o_actual_cost = my.make_number(order.get('actual_cost'))
        o_expected_price = my.make_number(order.get('expected_price'))
        o_actual_price = my.make_number(order.get('price'))
        c2 = ctbl.add_cell('<b>Expected Cost:</b> $%.2f ' % o_expected_cost)
        c2.add_attr('nowrap','nowrap')
        ctbl.add_row()
        c3 = ctbl.add_cell('<b>Actual Cost:</b> $%.2f ' % o_actual_cost)
        c3.add_attr('nowrap','nowrap')
        ctbl.add_row()
        c4 = ctbl.add_cell('<b>Expected Price:</b> $%.2f ' % o_expected_price)
        c4.add_attr('nowrap','nowrap')
        ctbl.add_row()
        c5 = ctbl.add_cell('<b>Actual Price:</b> $%.2f ' % o_actual_price)
        c5.add_attr('nowrap','nowrap')
        otbl.add_row()
        o1 = otbl.add_cell(botbl)
        o1.add_attr('valign','top')
        o2 = otbl.add_cell(dtbl)
        o2.add_attr('valign','top')
        o3 = otbl.add_cell(ctbl)
        o3.add_attr('valign','top')
        discuss = DiscussionWdg(search_key=my.sk,append_process='Client Services,Redelivery/Rejection Request,Redelivery/Rejection Completed',chronological=True)
        o4 = otbl.add_cell(discuss)
        o4.add_attr('valign','top')
        
        hide_row1 = otbl.add_row()
        hide_row1.add_attr('id','billing_%s' % order.get('code'))
        hide_row1.add_style('display: none;')
        order_hours_tbl = my.make_hours_tbl(order_hours, order.get('code'))
        tspan = otbl.add_cell(order_hours_tbl)
        tspan.add_attr('colspan','3')
        table.add_row()
        table.add_cell(otbl)
        #colors = ['#04f002','#0e9422']
        colors = ['#d9edcf','#e9edcf']
        i = 0
        for title in titles:
            title_full_name = title.get('title')
            title_code = title.get('code')
            ttbl = Table()
            ttbl.add_attr('cellspacing','3')
            ttbl.add_attr('cellpadding','3')
            ttbl.add_style('border-bottom-right-radius', '10px')
            ttbl.add_style('border-bottom-left-radius', '10px')
            ttbl.add_style('border-top-right-radius', '10px')
            ttbl.add_style('border-top-left-radius', '10px')
            ttbl.add_style('padding-left: 40px;')
            hide_unhide_bvr = my.get_hide_unhide(title_code)
            ttbl.add_behavior(hide_unhide_bvr)
            cval = i % 2
            #ttbl.add_attr('bgcolor',colors[cval])
            ttbl.add_style('background-color: %s;' % colors[cval])
            if title.get('episode') not in [None,'']:
                title_full_name = '%s: %s' % (title_full_name, title.get('episode'))
            totbl = Table()
            totbl.add_attr('cellspacing','3')
            totbl.add_attr('cellpadding','3')
            totbl.add_row()
            t1 = totbl.add_cell("<b>Title:</b> %s" % title_full_name)
            t1.add_attr('nowrap','nowrap')
            t2 = totbl.add_cell("<b>Status:</b> %s" % title.get('status'))
            t2.add_attr('nowrap','nowrap')
            t3 = totbl.add_cell("<b>Platform:</b> %s" % title.get('platform'))
            t3.add_attr('nowrap','nowrap')
            t4 = totbl.add_cell("<b>Pipeline:</b> %s" % title.get('pipeline_code'))
            t4.add_attr('nowrap','nowrap')
            totbl.add_row()
            t5 = totbl.add_cell("<b>Code:</b> %s" % title.get('code'))
            t5.add_attr('nowrap','nowrap')
            t6 = totbl.add_cell("<b>Language:</b> %s" % title.get('language'))
            t6.add_attr('nowrap','nowrap')
            t7 = totbl.add_cell("<b>Territory:</b> %s" % title.get('territory'))
            t7.add_attr('nowrap','nowrap')
            t8 = totbl.add_cell("<b>Title ID#:</b> %s" % title.get('title_id_number'))
            t8.add_attr('nowrap','nowrap')
            totbl.add_row()
            tuploader = CustomHTML5UploadButtonWdg(sk=title.get('__search_key__'))
            totbl.add_cell(tuploader)
            t9 = totbl.add_cell("<b>TRT:</b> %s" % title.get('total_program_runtime'))
            t9.add_attr('nowrap','nowrap')
            t10 = totbl.add_cell("<b>TRT w/ Textless:</b> %s" % title.get('total_runtime_w_textless'))
            t10.add_attr('nowrap','nowrap')
            t11 = totbl.add_cell("<b>Pulled Blacks:</b> %s" % title.get('pulled_blacks'))
            t11.add_attr('nowrap','nowrap')
            totbl.add_row()
            t12 = totbl.add_cell(' ')
            t13 = totbl.add_cell('<b>File Size:</b> %s' % title.get('file_size'))
            dttbl = Table()
            dttbl.add_attr('cellspacing','3')
            dttbl.add_attr('cellpadding','3')
            dttbl.add_row()
            d1 = dttbl.add_cell('<b>Start Date:</b> %s ' % my.fix_date(title.get('start_date')))
            d1.add_attr('nowrap','nowrap')
            dttbl.add_row()
            d2 = dttbl.add_cell('<b>Due Date:</b> %s ' % my.fix_date(title.get('due_date')))
            d2.add_attr('nowrap','nowrap')
            dttbl.add_row()
            d3 = dttbl.add_cell('<b>Completion Date:</b> %s ' % my.fix_date(title.get('completion_date')))
            d3.add_attr('nowrap','nowrap')
            cttbl = Table()
            cttbl.add_attr('cellspacing','3')
            cttbl.add_attr('cellpadding','3')
            cttbl.add_row()
            c1 = cttbl.add_cell('<b>Completion Ratio:</b> %s/%s ' % (title.get('wo_completed'), title.get('wo_count')))
            c1.add_attr('nowrap','nowrap')
            cttbl.add_row()
            t_expected_cost = my.make_number(title.get('expected_cost'))
            t_actual_cost = my.make_number(title.get('actual_cost'))
            t_expected_price = my.make_number(title.get('expected_price'))
            t_actual_price = my.make_number(title.get('price'))
            c2 = cttbl.add_cell('<b>Expected Cost:</b> $%.2f ' % t_expected_cost)
            c2.add_attr('nowrap','nowrap')
            cttbl.add_row()
            c3 = cttbl.add_cell('<b>Actual Cost:</b> $%.2f ' % t_actual_cost)
            c3.add_attr('nowrap','nowrap')
            cttbl.add_row()
            c4 = cttbl.add_cell('<b>Expected Price:</b> $%.2f ' % t_expected_price)
            c4.add_attr('nowrap','nowrap')
            cttbl.add_row()
            c5 = cttbl.add_cell('<b>Actual Price:</b> $%.2f ' % t_actual_price)
            c5.add_attr('nowrap','nowrap')
            ttbl.add_row()
            tt1 = ttbl.add_cell(totbl)
            tt1.add_attr('valign','top')
            tt2 = ttbl.add_cell(dttbl)
            tt2.add_attr('valign','top')
            tt3 = ttbl.add_cell(cttbl)
            tt3.add_attr('valign','top')
            discuss = DiscussionWdg(search_key=title.get('__search_key__'),append_process='Client Services,Redelivery/Rejection Request,Redelivery/Rejection Completed',chronological=True)
            tt4 = ttbl.add_cell(discuss)
            tt4.add_attr('valign','top')
            hide_row2 = ttbl.add_row()
            hide_row2.add_attr('id','billing_%s' % title_code)
            hide_row2.add_style('display: none;')
            t_hours_tbl = my.make_hours_tbl(title_hours[title_code], title_code)
            tspan = ttbl.add_cell(t_hours_tbl)
            tspan.add_attr('colspan','3')
            table.add_row()
            cellio = table.add_cell(ttbl)
            cellio.add_style('padding-left: 40px;')
            i = i + 1
            
        widget.add(table)
        return widget
