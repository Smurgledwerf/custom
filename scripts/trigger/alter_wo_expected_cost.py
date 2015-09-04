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
        # CUSTOM_SCRIPT00038
        # Matthew Tyler Misenhimer
        # updates the expected cost and delivers the increase to all sobjects above it (order, title, proj..)
        def float_cost(my_str):
            out_cost = 0
            if my_str not in [None,'']:
                out_cost = float(my_str)
            return out_cost
        #For updates/inserts of work_orders, to adjust the expected cost
        if 'update_data' in input.keys():
            update_data = input.get('update_data') 
            do_wg = False
            do_ewh = False
            if 'work_group' in update_data.keys():
                do_wg = True
            if 'estimated_work_hours' in update_data.keys():
                do_ewh = True
            if do_wg or do_ewh:
                sobject = input.get('sobject')
                proj = server.eval("@SOBJECT(twog/proj['code','%s'])" % sobject.get('proj_code'))[0]
                title = server.eval("@SOBJECT(twog/title['code','%s'])" % proj.get('title_code'))[0]
                order = server.eval("@SOBJECT(twog/order['code','%s'])" % title.get('order_code'))[0]
                if order.get('classification') not in ['master','Master']:
                    old_expected_cost = sobject.get('expected_cost')
                    if old_expected_cost in [None,'']:
                        old_expected_cost = 0
                    else:
                        old_expected_cost = float(old_expected_cost)
                    prev_data = input.get('prev_data')
                    old_wg = new_wg = sobject.get('work_group')
                    old_ewh = new_ewh = sobject.get('estimated_work_hours')
                    new_hourly_rate = old_hourly_rate = 0
                    new_ewh = old_ewh = 0
                    if do_wg:
                        new_wg = update_data.get('work_group')
                        if new_wg not in [None,'']:
                            new_hourly_rate = server.eval("@GET(sthpw/login_group['login_group','%s'].hourly_rate)" % new_wg)[0]
                        old_wg = prev_data.get('work_group')
                        if old_wg not in [None,'']:
                            old_hourly_rate = server.eval("@GET(sthpw/login_group['login_group','%s'].hourly_rate)" % old_wg)[0]
                    else:
                        new_wg = old_wg = sobject.get('work_group')
                        new_hourly_rate = old_hourly_rate = server.eval("@GET(sthpw/login_group['login_group','%s'].hourly_rate)" % old_wg)[0]
                    if do_ewh:
                        new_ewh = update_data.get('estimated_work_hours')
                        new_ewh = float_cost(new_ewh)
                        old_ewh = prev_data.get('estimated_work_hours')
                        old_ewh = float_cost(old_ewh)
                    new_hourly_rate = float_cost(new_hourly_rate)
                    old_hourly_rate = float_cost(old_hourly_rate)
                    old_piece_cost = old_hourly_rate * old_ewh
                    new_piece_cost = new_hourly_rate * new_ewh
                    new_expected_cost =  old_expected_cost - old_piece_cost + new_piece_cost
                    server.update(input.get('search_key'), {'expected_cost': new_expected_cost})
                    
                    proj_expected_cost = proj.get('expected_cost')
                    proj_expected_cost = float_cost(proj_expected_cost)
                    new_proj_expected_cost = proj_expected_cost - old_piece_cost + new_piece_cost
                    new_proj_expected_cost = float_cost(new_proj_expected_cost)
                    server.update(proj.get('__search_key__'), {'expected_cost': new_proj_expected_cost})
            
                    title_expected_cost = title.get('expected_cost')
                    title_expected_cost = float_cost(title_expected_cost)
                    new_title_expected_cost = title_expected_cost - old_piece_cost + new_piece_cost
                    new_title_expected_cost = float_cost(new_title_expected_cost)
                    server.update(title.get('__search_key__'), {'expected_cost': new_title_expected_cost})
            
                    order_expected_cost = order.get('expected_cost')
                    order_expected_cost = float_cost(order_expected_cost)
                    new_order_expected_cost = order_expected_cost - old_piece_cost + new_piece_cost
                    new_order_expected_cost = float_cost(new_order_expected_cost)
                    server.update(order.get('__search_key__'), {'expected_cost': new_order_expected_cost})
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
