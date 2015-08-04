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
        # CUSTOM_SCRIPT00051
        # Matthew Tyler Misenhimer
        # Calculates the expected cost for work orders, based on the estimated work hours and the group they are in.
        update_data = input.get('update_data')
        sobject = input.get('sobject')
        #print "IN CALC EXPECTED WO COST"
        if 'estimated_work_hours' in update_data.keys() or 'work_group' in update_data.keys():
            estimated_work_hours = sobject.get('estimated_work_hours')
            work_group = sobject.get('work_group')
            if work_group not in [None,''] and estimated_work_hours not in [None,'',0,'0']:
                estimated_work_hours = float(estimated_work_hours)
                group = server.eval("@SOBJECT(sthpw/login_group['login_group','%s'])" % work_group)
                if group:
                    group = group[0]
                    group_rate = group.get('hourly_rate')
                    if group_rate not in [None,'']:
                        group_rate = float(group_rate)
                        new_expected_cost = float(group_rate * estimated_work_hours)
                        server.update(sobject.get('__search_key__'), {'expected_cost': new_expected_cost})
        #print "LEAVING CALC EXPECTED WO COST"
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
