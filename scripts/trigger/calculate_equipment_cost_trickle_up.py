"""
This file was generated automatically from a custom script found in Project -> Script Editor.
The custom script was moved to a file so that it could be integrated with GitHub.
"""

__author__ = 'Topher.Hughes'
__date__ = '04/08/2015'

import traceback


def main(server=None, input=None):
    """
    The main function of the custom script. The entire script was copied
    and pasted into the body of the try statement in order to add some
    error handling. It's all legacy code, so edit with caution.

    :param server: the TacticServerStub object
    :param input: a dict with data like like search_key, search_type, sobject, and update_data
    :return: None
    """
    if not input:
        input = {}

    try:
        # CUSTOM_SCRIPT00053
        #Calculate Equipment cost trickle up
        def update_expected_cost(sob, prev_cost, new_cost):
            current_cost = sob.get('expected_cost')
            if current_cost in [None,'']:
                current_cost = float(0)
            else:
                current_cost = float(current_cost)
            new_cost = current_cost - prev_cost + new_cost
            server.update(sob.get('__search_key__'), {'expected_cost': new_cost})
        
        def update_actual_cost(sob, prev_cost, new_cost):
            current_cost = sob.get('actual_cost')
            if current_cost in [None,'']:
                current_cost = float(0)
            else:
                current_cost = float(current_cost)
            new_cost = current_cost - prev_cost + new_cost
            server.update(sob.get('__search_key__'), {'actual_cost': new_cost})
        
        update_data = input.get('update_data')
        sobject = input.get('sobject')
        eq_code = sobject.get('equipment_code')
        eq_expr = "@SOBJECT(twog/equipment['code','%s'])" % eq_code
        #print "EQ EXPR = %s" % eq_expr
        eq = server.eval(eq_expr)
        #print "EQ = %s" % eq
        throwin_data = {}
        old_expected_cost = sobject.get('expected_cost')
        old_actual_cost = sobject.get('actual_cost')
        new_actual_duration = sobject.get('actual_duration')
        wo_code = sobject.get('work_order_code')
        if 'WORK_HOUR' not in wo_code:
            wo = server.eval("@SOBJECT(twog/work_order['code','%s'])" % wo_code)[0]
            unit_lookup = {'length': 'LEN', 'gb': 'GB', 'tb': 'TB', 'mb': 'MB', 'hr': 'HR', 'items': 'HR'}
            eq_u_code = sobject.get('code')
            wo_eq_info = wo.get('eq_info')
            if wo_eq_info in [None,'']:
                wo_eq_info = ''
            info_s = wo_eq_info.split('Z,Z')
            found = False
            new_str = ''
            for info in info_s:
                if eq_u_code in info:
                    add_str = '%sX|X%sX|X%sX|X%s' % (eq_u_code, sobject.get('name'), unit_lookup[sobject.get('units')], new_actual_duration)
                    found = True
                else:
                    add_str = info
                if new_str == '':
                    new_str = add_str
                else:
                    new_str = '%sZ,Z%s' % (new_str, add_str)
            if not found:
                if new_str == '': 
                    new_str = '%sX|X%sX|X%sX|X%s' % (eq_u_code, sobject.get('name'), unit_lookup[sobject.get('units')], new_actual_duration)
                else:
                    new_str = '%sZ,Z%sX|X%sX|X%sX|X%s' % (new_str, eq_u_code, sobject.get('name'), unit_lookup[sobject.get('units')], new_actual_duration)
            server.update(wo.get('__search_key__'), {'eq_info': new_str})
                
        if old_expected_cost in [None,'']:
            old_expected_cost = 0
        if old_actual_cost in [None,'']:
            old_actual_cost = 0
        new_expected_cost = 0
        new_actual_cost = 0
        if eq:
            eq = eq[0]
            lengths = eq.get('lengths')
            if lengths not in [None,'']:
                if sobject.get('length') not in [None,'']:
                    sob_len = sobject.get('length')
                    eq_cost_expr = "@SOBJECT(twog/equipment_unit_cost['equipment_code','%s']['length','%s'])" % (eq_code, sob_len)
                    #print "EQ COST EXPR = %s" % eq_cost_expr
                    eq_cost = server.eval(eq_cost_expr)
                    #print "EQ COST = %s" % eq_cost
                    if eq_cost:
                        eq_cost = eq_cost[0]
                        cost = eq_cost.get('cost')
                        if cost in [None,'']:
                            cost = 0
                        cost = float(cost)
                        quant = sobject.get('expected_quantity')
                        if quant in [None,'',0,'0']:
                            throwin_data['expected_quantity'] = 1
                            quant = 1
                        quant = float(quant)
                        set_cost = float(cost * quant)
                        if set_cost > 0:
                            new_expected_cost = throwin_data['expected_cost'] = set_cost
                            new_actual_cost = throwin_data['actual_cost'] = set_cost
            else:
                # Calculate the cost normally here, update
                units = sobject.get('units')
                divisor = 1
                if units in [None,'','items']:
                    units = 'hr'
                    throwin_data['units'] = 'hr'
                if units == 'mb':
                    units == 'gb'
                    divisor = .01
                if ('E_DELIVERY' in sobject.get('name') or 'STORAGE' in sobject.get('name')) and units in ['hr','items']:
                    units = 'gb'
                    sk = server.build_search_key('twog/equipment_used', sobject.get('code'))
                    server.update(sk, {'units': 'gb'})
                actual_quant = expected_quant = sobject.get('expected_quantity')
                expected_dur = sobject.get('expected_duration')
                if expected_dur in [None,'',0,'0']:
                    expected_dur = 1
                    throwin_data['expected_duration'] = 1
                actual_dur = sobject.get('actual_duration')
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
                #print "EQ COST EXPR = %s" % eq_cost_expr
                eq_cost = server.eval(eq_cost_expr)
                #print "EQ COST = %s" % eq_cost
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
                    new_expected_cost = throwin_data['expected_cost'] = expected_cost
                    new_actual_cost = throwin_data['actual_cost'] = actual_cost
        
        if throwin_data != {}:
            server.update(input.get('search_key'), throwin_data, triggers=False)
            wo = server.eval("@SOBJECT(twog/work_order['code','%s'])" % sobject.get('work_order_code'))
            if wo:
                wo = wo[0]
                update_expected_cost(wo, old_expected_cost, new_expected_cost)
                update_actual_cost(wo, old_actual_cost, new_actual_cost) 
                proj = server.eval("@SOBJECT(twog/proj['code','%s'])" % wo.get('proj_code'))
                if proj:
                    proj = proj[0]
                    update_expected_cost(proj, old_expected_cost, new_expected_cost)
                    update_actual_cost(proj, old_actual_cost, new_actual_cost) 
                    title = server.eval("@SOBJECT(twog/title['code','%s'])" % proj.get('title_code'))
                    if title:
                        title = title[0]
                        update_expected_cost(title, old_expected_cost, new_expected_cost)
                        update_actual_cost(title, old_actual_cost, new_actual_cost) 
                        order = server.eval("@SOBJECT(twog/order['code','%s'])" % title.get('order_code'))
                        if order:
                            order = order[0]
                            update_expected_cost(order, old_expected_cost, new_expected_cost)
                            update_actual_cost(order, old_actual_cost, new_actual_cost) 
            elif 'WORK_HOUR' in sobject.get('work_order_code'):  
                wh = server.eval("@SOBJECT(sthpw/work_hour['code','%s'])" % sobject.get('work_order_code'))
                if wh:
                    wh = wh[0]
                    if wh.get('title_code') not in [None,'']:
                        title = server.eval("@SOBJECT(twog/title['code','%s'])" % wh.get('title_code'))
                        if title:
                            title = title[0]
                            update_expected_cost(title, old_expected_cost, new_expected_cost)
                            update_actual_cost(title, old_actual_cost, new_actual_cost) 
                            order = server.eval("@SOBJECT(twog/order['code','%s'])" % title.get('order_code'))
                            if order:
                                order = order[0]
                                update_expected_cost(order, old_expected_cost, new_expected_cost)
                                update_actual_cost(order, old_actual_cost, new_actual_cost)
    except AttributeError as e:
        traceback.print_exc()
        print str(e) + '\nMost likely the server object does not exist.'
    except KeyError as e:
        traceback.print_exc()
        print str(e) + '\nMost likely the input dictionary does not exist.'
    except Exception as e:
        traceback.print_exc()
        print str(e)


if __name__ == '__main__':
    main()
