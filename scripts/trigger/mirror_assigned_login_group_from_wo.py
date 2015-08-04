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
        # CUSTOM_SCRIPT00024
        #print "IN MIRROR ASSIGNED FROM WO"
        update_data = input.get('update_data')
        work_group = update_data.get('work_group')
        if not work_group:
            work_group = '' 
        sob = input.get('sobject')
        task_code = sob.get('task_code')
        if task_code not in [None,'']:
            task = server.eval("@SOBJECT(sthpw/task['code','%s'])" % task_code)
            if task: 
                task = task[0]
                if task.get('assigned_login_group') != work_group:
                    server.update(task.get('__search_key__'), {'assigned_login_group': work_group})
        #print "LEAVING MIRROR ASSIGNED FROM WO"
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
