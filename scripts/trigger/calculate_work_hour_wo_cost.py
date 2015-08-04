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
        # CUSTOM_SCRIPT00052
        update_data = input.get('update_data')
        sobject = input.get('sobject')
        task = server.eval("@SOBJECT(sthpw/task['code','%s'])" % update_data.get('task_code'))
        user = update_data.get('login')
        straight_time = update_data.get('straight_time')
        straight_time = float(straight_time)
        #print "IN CALC WH WO COST"
        if task:
            task = task[0]
            assigned_login_group = task.get('assigned_login_group')
            user_groups = server.eval("@SOBJECT(sthpw/login_in_group['login','%s']['login_group','not in','client|user|admin'])" % user)
            found = False
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
            wo = server.eval("@SOBJECT(twog/work_order['code','%s'])" % task.get('lookup_code'))
            if wo:
                wo = wo[0]
                current_actual = wo.get('actual_cost')
                if current_actual in [None,'']:
                    current_actual = 0
                else:
                    current_actual = float(current_actual)
                new_actual = float(current_actual + cost_to_add)
                if new_actual not in [None,'']:
                    server.update(wo.get('__search_key__'), {'actual_cost': new_actual})
        #print "LEAVING CALC WH WO COST"
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
