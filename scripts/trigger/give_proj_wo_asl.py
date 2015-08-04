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
        # CUSTOM_SCRIPT00083
        #Give the newest work_group assigned to a work order under this proj to the proj task
        sobj = input.get('sobject')
        proj_code = sobj.get('proj_code')
        work_group = sobj.get('work_group')
        if work_group not in [None,''] and proj_code not in [None,'']:
            task_code = server.eval("@GET(twog/proj['code','%s'].task_code)" % proj_code)[0]
            if task_code not in [None,'']:
                if len(task_code) > 0:
                    task_sk = server.build_search_key('sthpw/task', task_code)
                    server.update(task_sk, {'assigned_login_group': work_group}, triggers=False)
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
