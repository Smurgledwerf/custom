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
        # CUSTOM_SCRIPT00054
        # Calculate expected wo cost trickle up
        def update_expected_cost(sob, prev_cost, new_cost):
            current_cost = sob.get('expected_cost')
            if current_cost in [None,'']:
                current_cost = float(0)
            else:
                current_cost = float(current_cost)
            new_cost = current_cost - prev_cost + new_cost
            server.update(sob.get('__search_key__'), {'expected_cost': new_cost})
        
        update_data = input.get('update_data')
        sobject = input.get('sobject')
        #print "IN CACLC EXPECTED WO COST TRICKLE UP"
        if 'estimated_work_hours' in update_data.keys() or 'work_group' in update_data.keys():
            estimated_work_hours = sobject.get('estimated_work_hours')
            work_group = sobject.get('work_group')
            prev_cost = 0
            if 'prev_data' in input.keys():
                prev_data = input.get('prev_data')
                prev_est_wh = estimated_work_hours
                prev_work_group = work_group
                if 'estimated_work_hours' in prev_data.keys():
                    prev_est_wh = prev_data.get('estimated_work_hours')
                if 'work_group' in prev_data.keys():
                    prev_work_group = prev_data.get('work_group')
                if prev_est_wh not in [None,'',0,'0']:
                    prev_est_wh = float(prev_est_wh)
                    if prev_work_group not in [None,''] and prev_est_wh not in [None,'',0,'0']:
                        prev_group = server.eval("@SOBJECT(sthpw/login_group['login_group','%s'])" % prev_work_group)
                        if prev_group:
                            prev_group = prev_group[0]
                            prev_group_rate = prev_group.get('hourly_rate')
                            if prev_group_rate not in [None,'']:
                                prev_group_rate = float(prev_group_rate)
                                prev_cost = float(prev_group_rate * prev_est_wh)
        
            if work_group not in [None,''] and estimated_work_hours not in [None,'',0,'0']:
                estimated_work_hours = float(estimated_work_hours)
                group = server.eval("@SOBJECT(sthpw/login_group['login_group','%s'])" % work_group)
                if group:
                    group = group[0]
                    group_rate = group.get('hourly_rate')
                    if group_rate not in [None,'']:
                        group_rate = float(group_rate)
                        new_expected_cost = float(group_rate * estimated_work_hours)
                        #server.update(sobject.get('__search_key__'), {'expected_cost': new_expected_cost})
                        update_expected_cost(sobject, prev_cost, new_expected_cost)
                        proj = server.eval("@SOBJECT(twog/proj['code','%s'])" % sobject.get('proj_code'))
                        if proj:
                            proj = proj[0]
                            update_expected_cost(proj, prev_cost, new_expected_cost)
                            title = server.eval("@SOBJECT(twog/title['code','%s'])" % proj.get('title_code'))
                            if title:
                                title = title[0]
                                update_expected_cost(title, prev_cost, new_expected_cost)
                                order = server.eval("@SOBJECT(twog/order['code','%s'])" % title.get('order_code'))
                                if order:
                                    order = order[0]
                                    update_expected_cost(order, prev_cost, new_expected_cost)
        #print "LEAVING CACLC EXPECTED WO COST TRICKLE UP"
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
