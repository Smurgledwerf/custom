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
        # CUSTOM_SCRIPT00042
        def float_cost(my_str):
            out_cost = 0
            if my_str not in [None,'']:
                out_cost = float(my_str)
            return out_cost
        #print "IN HOURS UPDATED"
        code = input.get('search_key').split('code=')[1]
        sobject = input.get('sobject')
        update_data = input.get('update_data')
        prev_data = input.get('prev_data')
        old_straight_time = prev_data.get('straight_time')
        new_straight_time = update_data.get('straight_time')
        login = sobject.get('login')
        login_in_groups = server.eval("@SOBJECT(sthpw/login_in_group['login','%s'])" % login)
        task_code = sobject.get('task_code')
        task = server.eval("@SOBJECT(sthpw/task['code','%s'])" % task_code)[0]
        lookup_code = task.get('lookup_code')
        if 'WORK_ORDER' in lookup_code:
            work_order = server.eval("@SOBJECT(twog/work_order['code','%s'])" % lookup_code)[0]
            wo_current_cost = work_order.get('actual_cost')
            wo_current_cost = float_cost(wo_current_cost)
        
            work_group = work_order.get('work_group')
            actual_group = ''
            if work_group in [None,'']:
                actual_group = login_in_groups[0].get('login_group')
            else:
                for lg in login_in_groups:
                    if lg.get('login_group') == work_group:
                        actual_group = lg.get('login_group')
            if actual_group in [None,'']:
                actual_group = login_in_groups[0].get('login_group')
        
            rate = server.eval("@GET(sthpw/login_group['login_group','%s'].hourly_rate)" % actual_group)[0] 
            old_wh_cost = float_cost(rate) * float_cost(old_straight_time)
            new_wh_cost = float_cost(rate) * float_cost(new_straight_time)
            work_order_new_cost = wo_current_cost - old_wh_cost + new_wh_cost
            server.update(work_order.get('__search_key__'), {'actual_cost': work_order_new_cost})
        
            proj = server.eval("@SOBJECT(twog/proj['code','%s'])" % work_order.get('proj_code'))[0]
            proj_actual_cost = proj.get('actual_cost')
            proj_actual_cost = float_cost(proj_actual_cost)
            proj_new_cost = proj_actual_cost - old_wh_cost + new_wh_cost
            server.update(proj.get('__search_key__'), {'actual_cost': proj_new_cost})
        
            title = server.eval("@SOBJECT(twog/title['code','%s'])" % proj.get('title_code'))[0]
            title_actual_cost = title.get('actual_cost')
            title_actual_cost = float_cost(title_actual_cost)
            title_new_cost = title_actual_cost - old_wh_cost + new_wh_cost
            server.update(title.get('__search_key__'), {'actual_cost': title_new_cost})
        
            order = server.eval("@SOBJECT(twog/order['code','%s'])" % title.get('order_code'))[0]
            order_actual_cost = order.get('actual_cost')
            order_actual_cost = float_cost(order_actual_cost)
            order_new_cost = order_actual_cost - old_wh_cost + new_wh_cost
            server.update(order.get('__search_key__'), {'actual_cost': order_new_cost})
        #print "LEAVING HOURS UPDATED"
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
