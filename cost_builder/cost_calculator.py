__all__ = ["CostCalculatorLauncherWdg","CostCalculator"]
import tacticenv
from pyasm.common import Environment
from pyasm.biz import *
from pyasm.web import Table, DivWdg
from pyasm.widget import SelectWdg, IconWdg, TextWdg, CheckboxWdg
from tactic.ui.common import BaseTableElementWdg
from tactic.ui.common import BaseRefreshWdg
from tactic.ui.panel import EditWdg
from tactic.ui.widget.button_new_wdg import ButtonSmallNewWdg, ButtonRowWdg

class CostCalculatorLauncherWdg(BaseTableElementWdg):

    def init(my):
        from client.tactic_client_lib import TacticServerStub
        my.order_code = None
        my.order_name = None
        my.server = TacticServerStub.get()

    def get_launch_behavior(my):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                          var server = TacticServerStub.get();
                          var order_name =  bvr.src_el.get('order_name');
                          var order_code = bvr.src_el.get('order_code');
                          var my_user = bvr.src_el.get('user');
                          var class_name = 'cost_builder.cost_calculator.CostCalculator';
                          kwargs = {
                                           'order_code': order_code,
                                           'user': my_user
                                   };
                          spt.panel.load_popup('Costs for ' + order_name, class_name, kwargs);
                }
                catch(err){
                          spt.app_busy.hide();
                          alert(err);
                }
         '''}
        return behavior

    def get_display(my):
        sobject = None
        if 'order_code' in my.kwargs.keys():
            my.order_code = my.kwargs.get('order_code')
        else:
            sobject = my.get_current_sobject()
            my.order_code = sobject.get_code()
        sobject = my.server.eval("@SOBJECT(twog/order['code','%s'])" % my.order_code)[0]
        my.order_name = sobject.get('name')
        widget = DivWdg()
        table = Table()
        table.add_attr('width', '50px')
        login = Environment.get_login()
        user_name = login.get_login()
        table.add_row()
        cell1 = table.add_cell('<b><u>Calculate Costs</u></b>')
        cell1.add_attr('order_code', my.order_code)
        cell1.add_attr('user', user_name)
        cell1.add_attr('order_name', my.order_name)
        cell1.add_attr('nowrap','nowrap')
        launch_behavior = my.get_launch_behavior()
        cell1.add_style('cursor: pointer;')
        cell1.add_behavior(launch_behavior)
        widget.add(table)

        return widget

class CostCalculator(BaseRefreshWdg):
    def init(my):
        from client.tactic_client_lib import TacticServerStub
        from pyasm.common import Environment
        my.server = TacticServerStub.get()
        my.sk = ''
        my.login = '' 
        my.order_code = ''

    def update_costs(my):   
        my.order_code = str(my.kwargs.get('order_code'))
        my.login = str(my.kwargs.get('user'))
        order = my.server.eval("@SOBJECT(twog/order['code','%s'])" % my.order_code)[0]
        order_dict = {'actual_cost': 0, 'expected_cost': 0, 'titles':{}}
        titles = my.server.eval("@SOBJECT(twog/title['order_code','%s'])" % my.order_code)
        group_dict = my.server.eval("@SOBJECT(sthpw/login_group)")
        groups = {}
        for g in group_dict:
            grp = g.get('login_group')
            groups[grp] = g
        equipment_dict = my.server.eval("@SOBJECT(twog/equipment)")
        equipment_lookup = {}
        for ed in equipment_dict:
            edcode = ed.get('code')
            equipment_lookup[edcode] = ed

        for title in titles:
            title_code = title.get('code')
            order_dict['titles'][title_code] = {'actual_cost': 0, 'expected_cost': 0, 'projs': {}}
            # get unattached work hours and equipment attached, add to actual cost
            twhs = my.server.eval("@SOBJECT(sthpw/work_hour['is_billable','1']['title_code','%s'])" % title_code)
            #print "%s WHS = %s" % (title_code, twhs) 
            for twh in twhs:
                if twh.get('task_code') in [None,'']:
                    #print "TWH = %s" % twh
                    wh_code = twh.get('code')
                    # make cost here
                    cost_to_add = 0
                    user = twh.get('login')
                    straight_time = twh.get('straight_time')
                    if straight_time in [None,'']:
                        straight_time = float(0)
                    else:
                        straight_time = float(straight_time)
                    found = False
                    group_rate = 0
                    group_chosen = ''
                    user_groups = my.server.eval("@SOBJECT(sthpw/login_in_group['login','%s']['login_group','not in','client|user|admin'])" % user)
                    for ug in user_groups:
                        if ug.get('login_group') in groups.keys():
                            group = groups[ug.get('login_group')]
                            this_rate = group.get('hourly_rate')
                            if this_rate not in [None,'']:
                                this_rate = float(this_rate)
                                if this_rate > group_rate:
                                    group_rate = this_rate
                                    group_chosen = ug.get('login_group')
                    cost_to_add = float(group_rate * straight_time)
                    order_dict['titles'][title_code]['actual_cost'] = float(order_dict['titles'][title_code]['actual_cost']) + cost_to_add
                    order_dict['actual_cost'] = float(order_dict['actual_cost']) + cost_to_add
                    wheq = my.server.eval("@SOBJECT(twog/equipment_used['work_order_code','%s'])" % twh.get('code'))
                    for equip in wheq:
                        #print "WHEQUIP = %s" % equip
                        eq_u_code = equip.get('code')
                        #######
                        eq_code = equip.get('equipment_code')
                        eq = None
                        if eq_code in equipment_lookup.keys():
                            eq = equipment_lookup[eq_code]
                        throwin_data = {'actual_cost': 0, 'expected_cost': 0}
                        if eq:
                            lengths = eq.get('lengths')
                            if lengths not in [None,'']:
                                if equip.get('length') not in [None,'']:
                                    sob_len = equip.get('length')
                                    eq_cost_expr = "@SOBJECT(twog/equipment_unit_cost['equipment_code','%s']['length','%s'])" % (eq_code, sob_len)
                                    eq_cost = my.server.eval(eq_cost_expr)
                                    if eq_cost:
                                        eq_cost = eq_cost[0]
                                        cost = eq_cost.get('cost')
                                        if cost in [None,'']:
                                            cost = 0
                                        cost = float(cost)
                                        quant = equip.get('expected_quantity')
                                        if quant in [None,'',0,'0']:
                                            throwin_data['expected_quantity'] = 1
                                            quant = 1
                                        quant = float(quant)
                                        set_cost = float(cost * quant)
                                        if set_cost > 0:
                                            throwin_data['expected_cost'] = set_cost
                                            throwin_data['actual_cost'] = set_cost
                            else:
                                units = equip.get('units')
                                divisor = 1
                                if units in [None,'','items']:
                                    units = 'hr'
                                    throwin_data['units'] = 'hr'
                                if units == 'mb':
                                    units == 'gb'
                                    divisor = .01
                                if ('E_DELIVERY' in equip.get('name') or 'STORAGE' in equip.get('name')) and units in ['hr','items']:
                                    units = 'gb'
                                    my.server.update(equip.get('__search_key__'), {'units': 'gb'})
                                actual_quant = expected_quant = equip.get('expected_quantity')
                                expected_dur = equip.get('expected_duration')
                                if expected_dur in [None,'',0,'0']:
                                    expected_dur = 1
                                    throwin_data['expected_duration'] = 1
                                actual_dur = equip.get('actual_duration')
                                if actual_dur in [None,'',0,'0']:
                                    actual_dur = 0
                                expected_dur = float(expected_dur)
                                actual_dur = float(actual_dur)
                                if expected_quant in [None,'','0',0]:
                                    actual_quant = expected_quant = 1
                                    throwin_data['actual_quantity'] = 1
                                    throwin_data['expected_quantity'] = 1
                                actual_quant = expected_quant = float(expected_quant)
                                eq_cost_expr = "@SOBJECT(twog/equipment_unit_cost['equipment_code','%s']['unit','%s'])" % (eq_code, units)
                                eq_cost = my.server.eval(eq_cost_expr)
                                if eq_cost:
                                    eq_cost = eq_cost[0]
                                    cost = eq_cost.get('cost')
                                    if cost in [None,'']:
                                        cost = 0
                                    cost = float(cost)
                                    actual_cost = 0
                                    expected_cost = 0
                                    if units in ['hr','items']:
                                        expected_cost = float(expected_dur * expected_quant * cost)
                                        actual_cost = float(actual_dur * actual_quant * cost)
                                    else:
                                        expected_cost = float(expected_quant * expected_dur * divisor * cost)
                                        actual_cost = expected_cost
                                    throwin_data['expected_cost'] = expected_cost
                                    throwin_data['actual_cost'] = actual_cost
                        if throwin_data != {}:
                            my.server.update(equip.get('__search_key__'), throwin_data, triggers=False)    
                        #####
                        if throwin_data['actual_cost'] > 0:
                            order_dict['titles'][title_code]['actual_cost'] = float(order_dict['titles'][title_code]['actual_cost']) + float(throwin_data['actual_cost'])
                            order_dict['actual_cost'] = float(order_dict['actual_cost']) + float(throwin_data['actual_cost'])
                        if throwin_data['expected_cost'] > 0:
                            order_dict['titles'][title_code]['expected_cost'] = float(order_dict['titles'][title_code]['expected_cost']) + float(throwin_data['expected_cost'])
                            order_dict['expected_cost'] = float(order_dict['expected_cost']) + float(throwin_data['expected_cost'])
 
             
            projs = my.server.eval("@SOBJECT(twog/proj['title_code','%s'])" % title_code)
            for proj in projs:
                proj_code = proj.get('code')
                order_dict['titles'][title_code]['projs'][proj_code] = {'actual_cost': 0, 'expected_cost': 0, 'wos': {}}
                wos = my.server.eval("@SOBJECT(twog/work_order['proj_code','%s'])" % proj_code)
                for wo in wos:
                    wo_code = wo.get('code')
                    estimated_work_hours = wo.get('estimated_work_hours')
                    work_group = wo.get('work_group')
                    new_expected_cost = 0
                    if work_group not in [None,''] and estimated_work_hours not in [None,'',0,'0']:
                        estimated_work_hours = float(estimated_work_hours)
                        if work_group in groups.keys():
                            group = groups[work_group]
                            group_rate = group.get('hourly_rate')
                            if group_rate not in [None,'']:
                                group_rate = float(group_rate)
                                new_expected_cost = float(group_rate * estimated_work_hours)
                    order_dict['titles'][title_code]['projs'][proj_code]['wos'][wo_code] = {'actual_cost': 0, 'expected_cost': new_expected_cost, 'whs': {}, 'eqs': {}}
                    order_dict['titles'][title_code]['projs'][proj_code]['expected_cost'] = float(order_dict['titles'][title_code]['projs'][proj_code]['expected_cost']) + new_expected_cost
                    order_dict['titles'][title_code]['expected_cost'] = float(order_dict['titles'][title_code]['expected_cost']) + new_expected_cost
                    order_dict['expected_cost'] = float(order_dict['expected_cost']) + new_expected_cost
                    task = my.server.eval("@SOBJECT(sthpw/task['lookup_code','%s'])" % wo_code)
                    if task:
                        task = task[0]
                        task_code = task.get('code')
                        whs = my.server.eval("@SOBJECT(sthpw/work_hour['is_billable','1']['task_code','%s'])" % task_code)
                        for wh in whs:
                            wh_code = wh.get('code')
                            # make cost here
                            cost_to_add = 0
                            user = wh.get('login')
                            straight_time = wh.get('straight_time')
                            if straight_time in [None,'']:
                                straight_time = float(0)
                            else:
                                straight_time = float(straight_time)
                            assigned_login_group = task.get('assigned_login_group')
                            found = False
                            group_rate = 0
                            group_chosen = ''
                            user_groups = my.server.eval("@SOBJECT(sthpw/login_in_group['login','%s']['login_group','not in','client|user|admin'])" % user)
                            for ug in user_groups:
                                if ug.get('login_group') in groups.keys():
                                    group = groups[ug.get('login_group')]
                                    this_rate = group.get('hourly_rate')
                                    if this_rate not in [None,'']:
                                        this_rate = float(this_rate)
                                        if this_rate > group_rate:
                                            group_rate = this_rate
                                            group_chosen = ug.get('login_group')
                            cost_to_add = float(group_rate * straight_time)
                            order_dict['titles'][title_code]['projs'][proj_code]['wos'][wo_code]['whs'][wh_code] = {'actual_cost': cost_to_add}
                            #Force the cost up here
                            order_dict['titles'][title_code]['projs'][proj_code]['wos'][wo_code]['actual_cost'] = float(order_dict['titles'][title_code]['projs'][proj_code]['wos'][wo_code]['actual_cost']) + cost_to_add
                            order_dict['titles'][title_code]['projs'][proj_code]['actual_cost'] = float(order_dict['titles'][title_code]['projs'][proj_code]['actual_cost']) + cost_to_add
                            order_dict['titles'][title_code]['actual_cost'] = float(order_dict['titles'][title_code]['actual_cost']) + cost_to_add
                            order_dict['actual_cost'] = float(order_dict['actual_cost']) + cost_to_add
                        eqs = my.server.eval("@SOBJECT(twog/equipment_used['work_order_code','%s'])" % wo_code)
                        for equip in eqs:
                            eq_u_code = equip.get('code')
                            #######
                            eq_code = equip.get('equipment_code')
                            eq = None
                            if eq_code in equipment_lookup.keys():
                                eq = equipment_lookup[eq_code]
                            throwin_data = {'actual_cost': 0, 'expected_cost': 0}
                            if eq:
                                lengths = eq.get('lengths')
                                if lengths not in [None,'']:
                                    if equip.get('length') not in [None,'']:
                                        sob_len = equip.get('length')
                                        eq_cost_expr = "@SOBJECT(twog/equipment_unit_cost['equipment_code','%s']['length','%s'])" % (eq_code, sob_len)
                                        eq_cost = my.server.eval(eq_cost_expr)
                                        if eq_cost:
                                            eq_cost = eq_cost[0]
                                            cost = eq_cost.get('cost')
                                            if cost in [None,'']:
                                                cost = 0
                                            cost = float(cost)
                                            quant = equip.get('expected_quantity')
                                            if quant in [None,'',0,'0']:
                                                throwin_data['expected_quantity'] = 1
                                                quant = 1
                                            quant = float(quant)
                                            set_cost = float(cost * quant)
                                            if set_cost > 0:
                                                throwin_data['expected_cost'] = set_cost
                                                throwin_data['actual_cost'] = set_cost
                                else:
                                    units = equip.get('units')
                                    divisor = 1
                                    if units in [None,'','items']:
                                        units = 'hr'
                                        throwin_data['units'] = 'hr'
                                    if units == 'mb':
                                        units == 'gb'
                                        divisor = .01
                                    if ('E_DELIVERY' in equip.get('name') or 'STORAGE' in equip.get('name')) and units in ['hr','items']:
                                        units = 'gb'
                                        my.server.update(equip.get('__search_key__'), {'units': 'gb'})
                                    actual_quant = expected_quant = equip.get('expected_quantity')
                                    expected_dur = equip.get('expected_duration')
                                    if expected_dur in [None,'',0,'0']:
                                        expected_dur = 1
                                        throwin_data['expected_duration'] = 1
                                    actual_dur = equip.get('actual_duration')
                                    if actual_dur in [None,'',0,'0']:
                                        actual_dur = 0
                                    expected_dur = float(expected_dur)
                                    actual_dur = float(actual_dur)
                                    if expected_quant in [None,'','0',0]:
                                        actual_quant = expected_quant = 1
                                        throwin_data['actual_quantity'] = 1
                                        throwin_data['expected_quantity'] = 1
                                    actual_quant = expected_quant = float(expected_quant)
                                    eq_cost_expr = "@SOBJECT(twog/equipment_unit_cost['equipment_code','%s']['unit','%s'])" % (eq_code, units)
                                    eq_cost = my.server.eval(eq_cost_expr)
                                    if eq_cost:
                                        eq_cost = eq_cost[0]
                                        cost = eq_cost.get('cost')
                                        if cost in [None,'']:
                                            cost = 0
                                        cost = float(cost)
                                        actual_cost = 0
                                        expected_cost = 0
                                        if units in ['hr','items']:
                                            expected_cost = float(expected_dur * expected_quant * cost)
                                            actual_cost = float(actual_dur * actual_quant * cost)
                                        else:
                                            expected_cost = float(expected_quant * expected_dur * divisor * cost)
                                            actual_cost = expected_cost
                                        throwin_data['expected_cost'] = expected_cost
                                        throwin_data['actual_cost'] = actual_cost
                            if throwin_data != {}:
                                my.server.update(equip.get('__search_key__'), throwin_data, triggers=False)    
                            #####
                            order_dict['titles'][title_code]['projs'][proj_code]['wos'][wo_code]['eqs'][eq_u_code] = {'actual_cost': throwin_data['actual_cost'], 'expected_cost': throwin_data['expected_cost']} 
                            if throwin_data['actual_cost'] > 0:
                                order_dict['titles'][title_code]['projs'][proj_code]['wos'][wo_code]['actual_cost'] = float(order_dict['titles'][title_code]['projs'][proj_code]['wos'][wo_code]['actual_cost']) + float(throwin_data['actual_cost'])
                                order_dict['titles'][title_code]['projs'][proj_code]['actual_cost'] = float(order_dict['titles'][title_code]['projs'][proj_code]['actual_cost']) + float(throwin_data['actual_cost'])
                                order_dict['titles'][title_code]['actual_cost'] = float(order_dict['titles'][title_code]['actual_cost']) + float(throwin_data['actual_cost'])
                                order_dict['actual_cost'] = float(order_dict['actual_cost']) + float(throwin_data['actual_cost'])
                            if throwin_data['expected_cost'] > 0:
                                order_dict['titles'][title_code]['projs'][proj_code]['wos'][wo_code]['expected_cost'] = float(order_dict['titles'][title_code]['projs'][proj_code]['wos'][wo_code]['expected_cost']) + float(throwin_data['expected_cost'])
                                order_dict['titles'][title_code]['projs'][proj_code]['expected_cost'] = float(order_dict['titles'][title_code]['projs'][proj_code]['expected_cost']) + float(throwin_data['expected_cost'])
                                order_dict['titles'][title_code]['expected_cost'] = float(order_dict['titles'][title_code]['expected_cost']) + float(throwin_data['expected_cost'])
                                order_dict['expected_cost'] = float(order_dict['expected_cost']) + float(throwin_data['expected_cost'])
                    #Update the wo costs here
                    wo_actual = float(order_dict['titles'][title_code]['projs'][proj_code]['wos'][wo_code]['actual_cost'])
                    wo_expected = float(order_dict['titles'][title_code]['projs'][proj_code]['wos'][wo_code]['expected_cost'])
                    my.server.update(wo.get('__search_key__'), {'expected_cost': wo_expected, 'actual_cost': wo_actual})
                #Update the proj costs here
                proj_actual = float(order_dict['titles'][title_code]['projs'][proj_code]['actual_cost'])
                proj_expected = float(order_dict['titles'][title_code]['projs'][proj_code]['expected_cost'])
                my.server.update(proj.get('__search_key__'), {'expected_cost': proj_expected, 'actual_cost': proj_actual})
            #Update the title costs here
            title_actual = float(order_dict['titles'][title_code]['actual_cost'])
            title_expected = float(order_dict['titles'][title_code]['expected_cost'])
            my.server.update(title.get('__search_key__'), {'expected_cost': title_expected, 'actual_cost': title_actual})
        #Update the order costs here            
        order_actual = float(order_dict['actual_cost'])
        order_expected = float(order_dict['expected_cost'])
        my.server.update(order.get('__search_key__'), {'expected_cost': order_expected, 'actual_cost': order_actual})
        #print "ORDER DICT = %s" % order_dict
        return [order_actual, order_expected]

    def get_display(my):   
        my.order_code = str(my.kwargs.get('order_code'))
        my.login = str(my.kwargs.get('user'))
        #print "ORDER CODE = %s" % my.order_code
        order = my.server.eval("@SOBJECT(twog/order['code','%s'])" % my.order_code)[0]
        #print "ORDER = %s" % order
        order_dict = {'actual_cost': 0, 'expected_cost': 0, 'titles':{}}
        titles = my.server.eval("@SOBJECT(twog/title['order_code','%s'])" % my.order_code)
        group_dict = my.server.eval("@SOBJECT(sthpw/login_group)")
        groups = {}
        for g in group_dict:
            grp = g.get('login_group')
            groups[grp] = g
        equipment_dict = my.server.eval("@SOBJECT(twog/equipment)")
        equipment_lookup = {}
        for ed in equipment_dict:
            edcode = ed.get('code')
            equipment_lookup[edcode] = ed

        for title in titles:
            title_code = title.get('code')
            order_dict['titles'][title_code] = {'actual_cost': 0, 'expected_cost': 0, 'projs': {}}
            # get unattached work hours and equipment attached, add to actual cost
            twhs = my.server.eval("@SOBJECT(sthpw/work_hour['is_billable','1']['title_code','%s'])" % title_code)
            #print "%s WHS = %s" % (title_code, twhs) 
            for twh in twhs:
                if twh.get('task_code') in [None,'']:
                    #print "TWH = %s" % twh
                    wh_code = twh.get('code')
                    # make cost here
                    cost_to_add = 0
                    user = twh.get('login')
                    straight_time = twh.get('straight_time')
                    if straight_time in [None,'']:
                        straight_time = float(0)
                    else:
                        straight_time = float(straight_time)
                    found = False
                    group_rate = 0
                    group_chosen = ''
                    user_groups = my.server.eval("@SOBJECT(sthpw/login_in_group['login','%s']['login_group','not in','client|user|admin'])" % user)
                    for ug in user_groups:
                        if ug.get('login_group') in groups.keys():
                            group = groups[ug.get('login_group')]
                            this_rate = group.get('hourly_rate')
                            if this_rate not in [None,'']:
                                this_rate = float(this_rate)
                                if this_rate > group_rate:
                                    group_rate = this_rate
                                    group_chosen = ug.get('login_group')
                    cost_to_add = float(group_rate * straight_time)
                    order_dict['titles'][title_code]['actual_cost'] = float(order_dict['titles'][title_code]['actual_cost']) + cost_to_add
                    order_dict['actual_cost'] = float(order_dict['actual_cost']) + cost_to_add
                    wheq = my.server.eval("@SOBJECT(twog/equipment_used['work_order_code','%s'])" % twh.get('code'))
                    for equip in wheq:
                        #print "WHEQUIP = %s" % equip
                        eq_u_code = equip.get('code')
                        #######
                        eq_code = equip.get('equipment_code')
                        eq = None
                        if eq_code in equipment_lookup.keys():
                            eq = equipment_lookup[eq_code]
                        throwin_data = {'actual_cost': 0, 'expected_cost': 0}
                        if eq:
                            lengths = eq.get('lengths')
                            if lengths not in [None,'']:
                                if equip.get('length') not in [None,'']:
                                    sob_len = equip.get('length')
                                    eq_cost_expr = "@SOBJECT(twog/equipment_unit_cost['equipment_code','%s']['length','%s'])" % (eq_code, sob_len)
                                    eq_cost = my.server.eval(eq_cost_expr)
                                    if eq_cost:
                                        eq_cost = eq_cost[0]
                                        cost = eq_cost.get('cost')
                                        if cost in [None,'']:
                                            cost = 0
                                        cost = float(cost)
                                        quant = equip.get('expected_quantity')
                                        if quant in [None,'',0,'0']:
                                            throwin_data['expected_quantity'] = 1
                                            quant = 1
                                        quant = float(quant)
                                        set_cost = float(cost * quant)
                                        if set_cost > 0:
                                            throwin_data['expected_cost'] = set_cost
                                            throwin_data['actual_cost'] = set_cost
                            else:
                                units = equip.get('units')
                                divisor = 1
                                if units in [None,'','items']:
                                    units = 'hr'
                                    throwin_data['units'] = 'hr'
                                if units == 'mb':
                                    units == 'gb'
                                    divisor = .01
                                if ('E_DELIVERY' in equip.get('name') or 'STORAGE' in equip.get('name')) and units in ['hr','items']:
                                    units = 'gb'
                                    my.server.update(equip.get('__search_key__'), {'units': 'gb'})
                                actual_quant = expected_quant = equip.get('expected_quantity')
                                expected_dur = equip.get('expected_duration')
                                if expected_dur in [None,'',0,'0']:
                                    expected_dur = 1
                                    throwin_data['expected_duration'] = 1
                                actual_dur = equip.get('actual_duration')
                                if actual_dur in [None,'',0,'0']:
                                    actual_dur = 0
                                expected_dur = float(expected_dur)
                                actual_dur = float(actual_dur)
                                if expected_quant in [None,'','0',0]:
                                    actual_quant = expected_quant = 1
                                    throwin_data['actual_quantity'] = 1
                                    throwin_data['expected_quantity'] = 1
                                actual_quant = expected_quant = float(expected_quant)
                                eq_cost_expr = "@SOBJECT(twog/equipment_unit_cost['equipment_code','%s']['unit','%s'])" % (eq_code, units)
                                eq_cost = my.server.eval(eq_cost_expr)
                                if eq_cost:
                                    eq_cost = eq_cost[0]
                                    cost = eq_cost.get('cost')
                                    if cost in [None,'']:
                                        cost = 0
                                    cost = float(cost)
                                    actual_cost = 0
                                    expected_cost = 0
                                    if units in ['hr','items']:
                                        expected_cost = float(expected_dur * expected_quant * cost)
                                        actual_cost = float(actual_dur * actual_quant * cost)
                                    else:
                                        expected_cost = float(expected_quant * expected_dur * divisor * cost)
                                        actual_cost = expected_cost
                                    throwin_data['expected_cost'] = expected_cost
                                    throwin_data['actual_cost'] = actual_cost
                        if throwin_data != {}:
                            my.server.update(equip.get('__search_key__'), throwin_data, triggers=False)    
                        #####
                        if throwin_data['actual_cost'] > 0:
                            order_dict['titles'][title_code]['actual_cost'] = float(order_dict['titles'][title_code]['actual_cost']) + float(throwin_data['actual_cost'])
                            order_dict['actual_cost'] = float(order_dict['actual_cost']) + float(throwin_data['actual_cost'])
                        if throwin_data['expected_cost'] > 0:
                            order_dict['titles'][title_code]['expected_cost'] = float(order_dict['titles'][title_code]['expected_cost']) + float(throwin_data['expected_cost'])
                            order_dict['expected_cost'] = float(order_dict['expected_cost']) + float(throwin_data['expected_cost'])
 
             
            projs = my.server.eval("@SOBJECT(twog/proj['title_code','%s'])" % title_code)
            for proj in projs:
                proj_code = proj.get('code')
                order_dict['titles'][title_code]['projs'][proj_code] = {'actual_cost': 0, 'expected_cost': 0, 'wos': {}}
                wos = my.server.eval("@SOBJECT(twog/work_order['proj_code','%s'])" % proj_code)
                for wo in wos:
                    wo_code = wo.get('code')
                    estimated_work_hours = wo.get('estimated_work_hours')
                    work_group = wo.get('work_group')
                    new_expected_cost = 0
                    if work_group not in [None,''] and estimated_work_hours not in [None,'',0,'0']:
                        estimated_work_hours = float(estimated_work_hours)
                        if work_group in groups.keys():
                            group = groups[work_group]
                            group_rate = group.get('hourly_rate')
                            if group_rate not in [None,'']:
                                group_rate = float(group_rate)
                                new_expected_cost = float(group_rate * estimated_work_hours)
                    order_dict['titles'][title_code]['projs'][proj_code]['wos'][wo_code] = {'actual_cost': 0, 'expected_cost': new_expected_cost, 'whs': {}, 'eqs': {}}
                    order_dict['titles'][title_code]['projs'][proj_code]['expected_cost'] = float(order_dict['titles'][title_code]['projs'][proj_code]['expected_cost']) + new_expected_cost
                    order_dict['titles'][title_code]['expected_cost'] = float(order_dict['titles'][title_code]['expected_cost']) + new_expected_cost
                    order_dict['expected_cost'] = float(order_dict['expected_cost']) + new_expected_cost
                    task = my.server.eval("@SOBJECT(sthpw/task['lookup_code','%s'])" % wo_code)
                    if task:
                        task = task[0]
                        task_code = task.get('code')
                        whs = my.server.eval("@SOBJECT(sthpw/work_hour['is_billable','1']['task_code','%s'])" % task_code)
                        for wh in whs:
                            wh_code = wh.get('code')
                            # make cost here
                            cost_to_add = 0
                            user = wh.get('login')
                            straight_time = wh.get('straight_time')
                            if straight_time in [None,'']:
                                straight_time = float(0)
                            else:
                                straight_time = float(straight_time)
                            assigned_login_group = task.get('assigned_login_group')
                            found = False
                            group_rate = 0
                            group_chosen = ''
                            user_groups = my.server.eval("@SOBJECT(sthpw/login_in_group['login','%s']['login_group','not in','client|user|admin'])" % user)
                            for ug in user_groups:
                                if ug.get('login_group') in groups.keys():
                                    group = groups[ug.get('login_group')]
                                    this_rate = group.get('hourly_rate')
                                    if this_rate not in [None,'']:
                                        this_rate = float(this_rate)
                                        if this_rate > group_rate:
                                            group_rate = this_rate
                                            group_chosen = ug.get('login_group')
                            cost_to_add = float(group_rate * straight_time)
                            order_dict['titles'][title_code]['projs'][proj_code]['wos'][wo_code]['whs'][wh_code] = {'actual_cost': cost_to_add}
                            #Force the cost up here
                            order_dict['titles'][title_code]['projs'][proj_code]['wos'][wo_code]['actual_cost'] = float(order_dict['titles'][title_code]['projs'][proj_code]['wos'][wo_code]['actual_cost']) + cost_to_add
                            order_dict['titles'][title_code]['projs'][proj_code]['actual_cost'] = float(order_dict['titles'][title_code]['projs'][proj_code]['actual_cost']) + cost_to_add
                            order_dict['titles'][title_code]['actual_cost'] = float(order_dict['titles'][title_code]['actual_cost']) + cost_to_add
                            order_dict['actual_cost'] = float(order_dict['actual_cost']) + cost_to_add
                        eqs = my.server.eval("@SOBJECT(twog/equipment_used['work_order_code','%s'])" % wo_code)
                        for equip in eqs:
                            eq_u_code = equip.get('code')
                            #######
                            eq_code = equip.get('equipment_code')
                            eq = None
                            if eq_code in equipment_lookup.keys():
                                eq = equipment_lookup[eq_code]
                            throwin_data = {'actual_cost': 0, 'expected_cost': 0}
                            if eq:
                                lengths = eq.get('lengths')
                                if lengths not in [None,'']:
                                    if equip.get('length') not in [None,'']:
                                        sob_len = equip.get('length')
                                        eq_cost_expr = "@SOBJECT(twog/equipment_unit_cost['equipment_code','%s']['length','%s'])" % (eq_code, sob_len)
                                        eq_cost = my.server.eval(eq_cost_expr)
                                        if eq_cost:
                                            eq_cost = eq_cost[0]
                                            cost = eq_cost.get('cost')
                                            if cost in [None,'']:
                                                cost = 0
                                            cost = float(cost)
                                            quant = equip.get('expected_quantity')
                                            if quant in [None,'',0,'0']:
                                                throwin_data['expected_quantity'] = 1
                                                quant = 1
                                            quant = float(quant)
                                            set_cost = float(cost * quant)
                                            if set_cost > 0:
                                                throwin_data['expected_cost'] = set_cost
                                                throwin_data['actual_cost'] = set_cost
                                else:
                                    units = equip.get('units')
                                    divisor = 1
                                    if units in [None,'','items']:
                                        units = 'hr'
                                        throwin_data['units'] = 'hr'
                                    if units == 'mb':
                                        units == 'gb'
                                        divisor = .01
                                    if ('E_DELIVERY' in equip.get('name') or 'STORAGE' in equip.get('name')) and units in ['hr','items']:
                                        units = 'gb'
                                        my.server.update(equip.get('__search_key__'), {'units': 'gb'})
                                    actual_quant = expected_quant = equip.get('expected_quantity')
                                    expected_dur = equip.get('expected_duration')
                                    if expected_dur in [None,'',0,'0']:
                                        expected_dur = 1
                                        throwin_data['expected_duration'] = 1
                                    actual_dur = equip.get('actual_duration')
                                    if actual_dur in [None,'',0,'0']:
                                        actual_dur = 0
                                    expected_dur = float(expected_dur)
                                    actual_dur = float(actual_dur)
                                    if expected_quant in [None,'','0',0]:
                                        actual_quant = expected_quant = 1
                                        throwin_data['actual_quantity'] = 1
                                        throwin_data['expected_quantity'] = 1
                                    actual_quant = expected_quant = float(expected_quant)
                                    eq_cost_expr = "@SOBJECT(twog/equipment_unit_cost['equipment_code','%s']['unit','%s'])" % (eq_code, units)
                                    eq_cost = my.server.eval(eq_cost_expr)
                                    if eq_cost:
                                        eq_cost = eq_cost[0]
                                        cost = eq_cost.get('cost')
                                        if cost in [None,'']:
                                            cost = 0
                                        cost = float(cost)
                                        actual_cost = 0
                                        expected_cost = 0
                                        if units in ['hr','items']:
                                            expected_cost = float(expected_dur * expected_quant * cost)
                                            actual_cost = float(actual_dur * actual_quant * cost)
                                        else:
                                            expected_cost = float(expected_quant * expected_dur * divisor * cost)
                                            actual_cost = expected_cost
                                        throwin_data['expected_cost'] = expected_cost
                                        throwin_data['actual_cost'] = actual_cost
                            if throwin_data != {}:
                                my.server.update(equip.get('__search_key__'), throwin_data, triggers=False)    
                            #####
                            order_dict['titles'][title_code]['projs'][proj_code]['wos'][wo_code]['eqs'][eq_u_code] = {'actual_cost': throwin_data['actual_cost'], 'expected_cost': throwin_data['expected_cost']} 
                            if throwin_data['actual_cost'] > 0:
                                order_dict['titles'][title_code]['projs'][proj_code]['wos'][wo_code]['actual_cost'] = float(order_dict['titles'][title_code]['projs'][proj_code]['wos'][wo_code]['actual_cost']) + float(throwin_data['actual_cost'])
                                order_dict['titles'][title_code]['projs'][proj_code]['actual_cost'] = float(order_dict['titles'][title_code]['projs'][proj_code]['actual_cost']) + float(throwin_data['actual_cost'])
                                order_dict['titles'][title_code]['actual_cost'] = float(order_dict['titles'][title_code]['actual_cost']) + float(throwin_data['actual_cost'])
                                order_dict['actual_cost'] = float(order_dict['actual_cost']) + float(throwin_data['actual_cost'])
                            if throwin_data['expected_cost'] > 0:
                                order_dict['titles'][title_code]['projs'][proj_code]['wos'][wo_code]['expected_cost'] = float(order_dict['titles'][title_code]['projs'][proj_code]['wos'][wo_code]['expected_cost']) + float(throwin_data['expected_cost'])
                                order_dict['titles'][title_code]['projs'][proj_code]['expected_cost'] = float(order_dict['titles'][title_code]['projs'][proj_code]['expected_cost']) + float(throwin_data['expected_cost'])
                                order_dict['titles'][title_code]['expected_cost'] = float(order_dict['titles'][title_code]['expected_cost']) + float(throwin_data['expected_cost'])
                                order_dict['expected_cost'] = float(order_dict['expected_cost']) + float(throwin_data['expected_cost'])
                    #Update the wo costs here
                    wo_actual = float(order_dict['titles'][title_code]['projs'][proj_code]['wos'][wo_code]['actual_cost'])
                    wo_expected = float(order_dict['titles'][title_code]['projs'][proj_code]['wos'][wo_code]['expected_cost'])
                    my.server.update(wo.get('__search_key__'), {'expected_cost': wo_expected, 'actual_cost': wo_actual})
                #Update the proj costs here
                proj_actual = float(order_dict['titles'][title_code]['projs'][proj_code]['actual_cost'])
                proj_expected = float(order_dict['titles'][title_code]['projs'][proj_code]['expected_cost'])
                my.server.update(proj.get('__search_key__'), {'expected_cost': proj_expected, 'actual_cost': proj_actual})
            #Update the title costs here
            title_actual = float(order_dict['titles'][title_code]['actual_cost'])
            title_expected = float(order_dict['titles'][title_code]['expected_cost'])
            my.server.update(title.get('__search_key__'), {'expected_cost': title_expected, 'actual_cost': title_actual})
        #Update the order costs here            
        order_actual = float(order_dict['actual_cost'])
        order_expected = float(order_dict['expected_cost'])
        my.server.update(order.get('__search_key__'), {'expected_cost': order_expected, 'actual_cost': order_actual})
        #print "ORDER DICT = %s" % order_dict
        table = Table()
        table.add_row()
        table.add_cell('Expected: $%s Actual: $%s' % (order_expected, order_actual))
        return table
