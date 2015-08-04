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
        # CUSTOM_SCRIPT00055
        #Calculate work hour wo cost trickle up
        def update_actual_cost(sob, new_cost):
            current_cost = sob.get('actual_cost')
            if current_cost in [None,'']:
                current_cost = float(0)
            else:
                current_cost = float(current_cost)
            new_cost = float(current_cost + new_cost)
            server.update(sob.get('__search_key__'), {'actual_cost': new_cost})
        
        def make_timestamp():
            import datetime
            now = datetime.datetime.now()
            return now.strftime("%Y-%m-%d %H:%M:%S")
        #print "IN CALC WH WO COST TRICKLE UP"
        wo = None
        proj = None
        title = None
        order = None
        update_data = input.get('update_data')
        sobject = input.get('sobject')
        user = update_data.get('login')
        straight_time = update_data.get('straight_time')
        straight_time = float(straight_time)
        user_groups = server.eval("@SOBJECT(sthpw/login_in_group['login','%s']['login_group','not in','client|user|admin'])" % user)
        group_rate = 0
        group_chosen = ''
        for ug in user_groups:
            group = server.eval("@SOBJECT(sthpw/login_group['login_group','%s'])" % ug.get('login_group'))[0]
            this_rate = group.get('hourly_rate')
            if this_rate not in [None,'']:
                this_rate = float(this_rate)
                if this_rate > group_rate:
                    group_rate = this_rate
                    group_chosen = ug.get('login_group')
        cost_to_add = float(group_rate * straight_time)
        
        if sobject.get('is_billable') in [True,'True','true','t',1,'1']:
            task = server.eval("@SOBJECT(sthpw/task['code','%s'])" % update_data.get('task_code'))
            if task:
                task = task[0]
                wo = server.eval("@SOBJECT(twog/work_order['code','%s'])" % task.get('lookup_code'))
                if wo:
                    wo = wo[0]
                    update_actual_cost(wo, cost_to_add)
                    proj = server.eval("@SOBJECT(twog/proj['code','%s'])" % wo.get('proj_code'))
                    if proj:
                        proj = proj[0]
                        update_actual_cost(proj, cost_to_add)
                        title = server.eval("@SOBJECT(twog/title['code','%s'])" % proj.get('title_code'))
                        if title:
                            title = title[0]
                            update_actual_cost(title, cost_to_add)
                            order = server.eval("@SOBJECT(twog/order['code','%s'])" % title.get('order_code'))
                            if order:
                                order = order[0]
                                update_actual_cost(order, cost_to_add)
            elif sobject.get('task_code') in [None,''] and sobject.get('title_code') not in [None,'']:
                title = server.eval("@SOBJECT(twog/title['code','%s'])" % sobject.get('title_code'))
                if title:
                    title = title[0]
                    update_actual_cost(title, cost_to_add)
                    order = server.eval("@SOBJECT(twog/order['code','%s'])" % title.get('order_code'))
                    if order:
                        order = order[0]
                        update_actual_cost(order, cost_to_add)
        #if title and wo:
        #    import os
        #    wo_code = wo.get('code')
        #    order_code = order.get('code')
        #    title_code = title.get('code')
        #    platform = title.get('platform')
        #    client_code = order.get('client_code')
        #    billed = sobject.get('is_billable')
        #    classification = order.get('classification')
        #    login_name = user
        #    group = group_chosen
        #    task_due_date = task.get('bid_end_date')
        #    order_due_date = order.get('due_date')
        #    task_completion_date = make_timestamp()
        #    order_completion_date = order.get('completion_date')
        #    echo_str = 'MTMWHMTM WO:MTM:%s:MTM:TITLE:MTM:%s:MTM:ORDER:MTM:%s:MTM:PLATFORM:MTM:%s:MTM:CLIENT_CODE:MTM:%s:MTM:BILLED:MTM:%s:MTM:CLASSIFICATION:MTM:%s:MTM:LOGIN_NAME:MTM:%s:MTM:GROUP:MTM:%s:MTM:TASK_DUE_DATE:MTM:%s:MTM:ORDER_DUE_DATE:MTM:%s:MTM:TASK_COMPLETION_DATE:MTM:%s:MTM:ORDER_COMPLETION_DATE:MTM:%s:MTMSTRAIGHT_TIME:MTM:%s:MTM:COST_TO_ADD:MTM:%s' % (wo_code, title_code, order_code, platform, client_code, billed, classification, login_name, group, task_due_date, order_due_date, task_completion_date, order_completion_date, straight_time, cost_to_add) 
        #    os.system("""echo '%s' >> /var/www/html/report_updater/report_update_queue""" % echo_str) 
        #print "LEAVING CALC WH WO COST TRICKLE UP"
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
