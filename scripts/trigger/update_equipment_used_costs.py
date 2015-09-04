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
        # CUSTOM_SCRIPT00037
        def float_cost(my_str):
            out_cost = 0
            if my_str not in [None,'']:
                out_cost = float(my_str)
            return out_cost
        #print "IN UPDATE EQUIPMENT USED COSTS"
        #For updates/inserts of expected/actual_cost, expected/actual_duration, units on equipment_used
        #print 'INPUT = %s' % input
        if 'update_data' in input.keys():
            #print "UPDATE DATA in input keys"
            update_data = input.get('update_data') 
            do_expected = False
            do_actual = False
            if 'expected_quantity' in update_data.keys():
                do_expected = True
            if 'expected_duration' in update_data.keys():
                do_expected = True
            if 'units' in update_data.keys():
                do_expected = True
                do_actual = True
            if 'actual_duration' in update_data.keys():
                do_actual = True
            if 'actual_quantity' in update_data.keys():
                do_actual = True
            #print "DO EXPECTED = %s" % do_expected
            #print "DO ACTUAL = %s" % do_actual
            expected_cost = 0
            item_expected_cost = 0
            old_expected_cost = 0
            actual_cost = 0
            item_actual_cost = 0
            old_actual_cost = 0
            if do_actual or do_expected:
                new_data = input.get('update_data')
                old_data = input.get('prev_data')
                sobject = input.get('sobject')
                eq_code = sobject.get('equipment_code')
                if eq_code in [None,'']:
                    eq_name = sobject.get('name')
                    poss_eqs = server.eval("@SOBJECT(twog/equipment['name','%s'])" % eq_name)
                    if poss_eqs:
                        eq_code = poss_eqs[0].get('code')
                expected_cost = sobject.get('expected_cost')
                expected_cost = float_cost(expected_cost)
                actual_cost = sobject.get('actual_cost')
                actual_cost = float_cost(actual_cost)
                unit_lookup = {'items': 'disc|tape|mile|miles|hr', 'gb': 'gb', 'mb': 'gb', 'tb': 'gb'}
                old_units = new_units = sobject.get('units')
                if old_units in [None, '']:
                    old_units = 'items'
                if new_units in [None, '']:
                    new_units = 'items'
                if 'units' in new_data.keys():
                    new_units = new_data.get('units')
                    if new_units in [None,'']:
                        new_units = 'items'
                if 'units' in old_data.keys():
                    old_units = old_data.get('units')
                    if old_units in [None,'']:
                        old_units = new_units
                old_unit_cost_expr = "@SOBJECT(twog/equipment_unit_cost['equipment_code','%s']['unit','in','%s'])" % (eq_code, unit_lookup[old_units])
                old_unit_cost = server.eval(old_unit_cost_expr)
                if old_unit_cost == []:
                    old_unit_cost_expr = "@SOBJECT(twog/equipment_unit_cost['equipment_code','%s']['unit','hr'])" % (eq_code)
                    old_unit_cost = server.eval(old_unit_cost_expr)
                    
                new_unit_cost_expr = "@SOBJECT(twog/equipment_unit_cost['equipment_code','%s']['unit','in','%s'])" % (eq_code, unit_lookup[new_units])
                new_unit_cost = server.eval(new_unit_cost_expr)
                if new_unit_cost == []:
                    new_unit_cost_expr = "@SOBJECT(twog/equipment_unit_cost['equipment_code','%s']['unit','hr'])" % (eq_code)
                    new_unit_cost = server.eval(new_unit_cost_expr)
                if old_unit_cost in [None,'',[]]:
                    old_unit_type = 'items'
                    old_unit_cost = 0
                else:
                    old_unit_type = old_unit_cost[0].get('unit')
                    old_unit_cost = old_unit_cost[0].get('cost')
                if new_unit_cost in [None,'',[]]:
                    new_unit_type = 'items'
                    new_unit_cost = 0
                else:
                    new_unit_type = new_unit_cost[0].get('unit')
                    new_unit_cost = new_unit_cost[0].get('cost')
                new_expected_cost = -1
                new_actual_cost = -1
                if do_expected:
                    old_quantity = new_quantity = sobject.get('expected_quantity')
                    old_duration = new_duration = sobject.get('expected_duration')
        
                    old_expected_cost = 0
                    if 'expected_quantity' in new_data.keys():
                        new_quantity = new_data.get('expected_quantity')
                        old_quantity = old_data.get('expected_quantity')
                    if 'expected_duration' in new_data.keys():
                        new_duration = new_data.get('expected_duration')
                        old_duration = old_data.get('expected_duration')
                    if old_duration in [None,'']:
                        old_duration = 1
                    if new_duration in [None,'']:
                        new_duration = 1
                    if old_quantity in [None,'']:
                        old_quantity = 1
                    if new_quantity in [None,'']:
                        new_quantity = 1
                    if old_units == 'mb':
                        old_quantity = float(float(old_quantity)/1000) 
                    if new_units == 'mb':
                        new_quantity = float(float(new_quantity)/1000) 
                    if old_units == 'tb':
                        old_quantity = float(float(old_quantity) * 1000) 
                    if new_units == 'tb':
                        new_quantity = float(float(new_quantity) * 1000) 
                    item_expected_cost = 0
                    if old_units == 'items':
                        old_expected_cost = float(old_unit_cost) * float(old_quantity)
                    if old_units in ['mb','gb','tb'] or old_unit_type == 'hr':
                        old_expected_cost = float(old_unit_cost) * float(old_quantity) * float(old_duration)
                    if new_units == 'items':
                        item_expected_cost = float(new_unit_cost) * float(new_quantity)
                        #print "1 ITEM EXPECTED COST = %s" % item_expected_cost
                    if new_units in ['mb','gb','tb'] or new_unit_type == 'hr':
                        item_expected_cost = float(new_unit_cost) * float(new_quantity) * float(new_duration)
                        #print "2 ITEM EXPECTED COST = %s" % item_expected_cost
                    if item_expected_cost == 1:
                        item_expected_cost = 0
                        #print "3 ITEM EXPECTED COST = %s" % item_expected_cost
                    new_expected_cost = expected_cost - old_expected_cost + item_expected_cost
                    #print "NEW EXPECTED COST = %s" % new_expected_cost
                    if expected_cost == 0:
                        new_expected_cost = item_expected_cost
                if do_actual and ('actual_duration' in update_data.keys() or 'actual_quantity' in update_data.keys()):
                    old_quantity = new_quantity = sobject.get('actual_quantity')
                    old_duration = new_duration = sobject.get('actual_duration')
                    old_actual_cost = 0
                    if 'actual_quantity' in new_data.keys():
                        new_quantity = new_data.get('actual_quantity')
                        old_quantity = old_data.get('actual_quantity')
                    if 'actual_duration' in new_data.keys():
                        new_duration = new_data.get('actual_duration')
                        old_duration = old_data.get('actual_duration')
                    if old_duration in [None,'']:
                        old_duration = 1
                    if new_duration in [None,'']:
                        new_duration = 1
                    if old_quantity in [None,'']:
                        old_quantity = 1
                    if new_quantity in [None,'']:
                        new_quantity = 1
                    if old_units == 'mb':
                        old_quantity = float(float(old_quantity)/1000) 
                    if new_units == 'mb':
                        new_quantity = float(float(new_quantity)/1000) 
                    if old_units == 'tb':
                        old_quantity = float(float(old_quantity) * 1000) 
                    if new_units == 'tb':
                        new_quantity = float(float(new_quantity) * 1000) 
                    item_actual_cost = 0
                    if old_units == 'items':
                        old_actual_cost = float(old_unit_cost) * float(old_quantity)
                    if old_units in ['mb','gb','tb'] or old_unit_type == 'hr':
                        old_actual_cost = float(old_unit_cost) * float(old_quantity) * float(old_duration)
                    if new_units == 'items':
                        item_actual_cost = float(new_unit_cost) * float(new_quantity)
                    if new_units in ['mb','gb','tb'] or new_unit_type == 'hr':
                        item_actual_cost = float(new_unit_cost) * float(new_quantity) * float(new_duration)
                    if item_actual_cost == 1:
                        item_actual_cost = 0
                    new_actual_cost = actual_cost - old_actual_cost + item_actual_cost
                    if actual_cost == 0:
                        new_actual_cost = item_actual_cost
                send_data = {}
                if new_actual_cost not in [None,'','-1']:
                    send_data['actual_cost'] = new_actual_cost
                if new_expected_cost not in [None,'','-1']:
                    send_data['expected_cost'] = new_expected_cost
                server.update(sobject.get('__search_key__'), send_data)
                #print "ITEM EXPECTED COST = %s" % item_expected_cost
                #print "OLD_EXPECTED_COST = %s" % old_expected_cost
                #print "EXPECTED_COST = %s" % expected_cost
                if do_expected:
                    #print "EXPECTED PUSH UP"
                    work_order = server.eval("@SOBJECT(twog/work_order['code','%s'])" % sobject.get('work_order_code'))[0]
                    wo_expected_cost = work_order.get('expected_cost')
                    wo_expected_cost = float_cost(wo_expected_cost)
                    new_wo_expected_cost = float(wo_expected_cost) - float(old_expected_cost) + float(item_expected_cost)
                    #print "UPDATE WO %s, expected_cost = %s" % (work_order.get('code'), new_wo_expected_cost)
                    server.update(work_order.get('__search_key__'), {'expected_cost': new_wo_expected_cost})
        
                    proj = server.eval("@SOBJECT(twog/proj['code','%s'])" % work_order.get('proj_code'))[0]
                    proj_expected_cost = proj.get('expected_cost')
                    proj_expected_cost = float_cost(wo_expected_cost)
                    new_proj_expected_cost = float(proj_expected_cost) - float(old_expected_cost) + float(item_expected_cost)
                    #print "UPDATE PROJ %s, expected_cost = %s" % (proj.get('code'), new_proj_expected_cost)
                    server.update(proj.get('__search_key__'), {'expected_cost': new_proj_expected_cost})
                    
                    title = server.eval("@SOBJECT(twog/title['code','%s'])" % proj.get('title_code'))[0]
                    title_expected_cost = title.get('expected_cost')
                    title_expected_cost = float_cost(wo_expected_cost)
                    new_title_expected_cost = float(title_expected_cost) - float(old_expected_cost) + float(item_expected_cost)
                    #print "UPDATE TITLE %s, expected_cost = %s" % (title.get('code'), new_title_expected_cost)
                    server.update(title.get('__search_key__'), {'expected_cost': new_title_expected_cost})
                     
                    order = server.eval("@SOBJECT(twog/order['code','%s'])" % title.get('order_code'))[0]
                    order_expected_cost = order.get('expected_cost')
                    order_expected_cost = float_cost(wo_expected_cost)
                    new_order_expected_cost = float(order_expected_cost) - float(old_expected_cost) + float(item_expected_cost)
                    #print "UPDATE ORDER %s, expected_cost = %s" % (order.get('code'), new_order_expected_cost)
                    server.update(order.get('__search_key__'), {'expected_cost': new_order_expected_cost})
        
                if do_actual and ('actual_duration' in update_data.keys() or 'actual_quantity' in update_data.keys()):
                    #print "ACTUAL PUSH UP"
                    work_order = server.eval("@SOBJECT(twog/work_order['code','%s'])" % sobject.get('work_order_code'))[0]
                    wo_actual_cost = work_order.get('actual_cost')
                    wo_actual_cost = float_cost(wo_actual_cost)
                    new_wo_actual_cost = float(wo_actual_cost) - float(old_actual_cost) + float(item_actual_cost)
                    #print "UPDATE WO %s, actual_cost = %s" % (work_order.get('code'), new_wo_actual_cost)
                    server.update(work_order.get('__search_key__'), {'actual_cost': new_wo_actual_cost})
        
                    proj = server.eval("@SOBJECT(twog/proj['code','%s'])" % work_order.get('proj_code'))[0]
                    proj_actual_cost = proj.get('actual_cost')
                    proj_actual_cost = float_cost(wo_actual_cost)
                    new_proj_actual_cost = float(proj_actual_cost) - float(old_actual_cost) + float(item_actual_cost)
                    #print "UPDATE PROJ %s, actual_cost = %s" % (proj.get('code'), new_proj_actual_cost)
                    server.update(proj.get('__search_key__'), {'actual_cost': new_proj_actual_cost})
                    
                    title = server.eval("@SOBJECT(twog/title['code','%s'])" % proj.get('title_code'))[0]
                    title_actual_cost = title.get('actual_cost')
                    title_actual_cost = float_cost(wo_actual_cost)
                    new_title_actual_cost = float(title_actual_cost) - float(old_actual_cost) + float(item_actual_cost)
                    #print "UPDATE TITLE %s, actual_cost = %s" % (title.get('code'), new_title_actual_cost)
                    server.update(title.get('__search_key__'), {'actual_cost': new_title_actual_cost})
                     
                    order = server.eval("@SOBJECT(twog/order['code','%s'])" % title.get('order_code'))[0]
                    order_actual_cost = order.get('actual_cost')
                    order_actual_cost = float_cost(wo_actual_cost)
                    new_order_actual_cost = float(order_actual_cost) - float(old_actual_cost) + float(item_actual_cost)
                    #print "UPDATE ORDER %s, actual_cost = %s" % (order.get('code'), new_order_actual_cost)
                    server.update(order.get('__search_key__'), {'actual_cost': new_order_actual_cost})
        #print "LEAVING UPDATE EQUIPMENT USED COSTS"
    except AttributeError as e:
        traceback.print_exc()
        print str(e) + '\nMost likely the server object does not exist.'
        raise e
    except KeyError as e:
        traceback.print_exc()
        print str(e) + '\nMost likely the input dictionary does not exist.'
        raise e
    except Exception as e:
        traceback.print_exc()
        print str(e)
        raise e


if __name__ == '__main__':
    main()
