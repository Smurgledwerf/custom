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
        # CUSTOM_SCRIPT00023
        #print "IN MIRROR ASSIGNED FROM TASK"
        update_data = input.get('update_data')
        assigned_login_group = update_data.get('assigned_login_group')
        if not assigned_login_group:
            assigned_login_group = ''
        sob = input.get('sobject')
        lookup_code = sob.get('lookup_code')
        if lookup_code.find('WORK_ORDER') != -1:
            wo = server.eval("@SOBJECT(twog/work_order['code','%s'])" % lookup_code)
            if wo:
                wo = wo[0]
                if wo.get('work_group') != assigned_login_group:
                    server.update(wo.get('__search_key__'), {'work_group': assigned_login_group})
        if 'tripwire' in update_data.keys():
            if update_data.get('tripwire') == 'No Send Back':
                server.update(input.get('search_key'), {'tripwire': ''}, triggers=False)
        #print "LEAVING MIRROR ASSIGNED FROM TASK"
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
