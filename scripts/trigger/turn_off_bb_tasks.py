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
        # CUSTOM_SCRIPT00081
        from pyasm.common import TacticException, Environment
        login = Environment.get_login()
        user_name = login.get_login()
        update_data = input.get('update_data') 
        sobject = input.get('sobject')
        title_code = sobject.get('code')
        if 'bigboard' in update_data.keys():
            bigboard = update_data.get('bigboard')
            if bigboard not in [True,'True','true','t','T',1,'1']:
                server.insert('twog/bigboard_record', {'title_code': title_code, 'bigboard_value': 'False', 'login': user_name})
                #cmnd = "update task set bigboard = False where title_code = '%s'" % title_code
                #server.execute_cmd('manual_updaters.commander.DBDirectCmd', {'cmnd': cmnd, 'which_db': 'sthpw'})
                task_expr = "@SOBJECT(sthpw/task['title_code','%s']['bigboard','in','True|true|t|1'])" % title_code
                tasks = server.eval(task_expr)
                for task in tasks:
                    if task.get('bigboard'):
                        server.update(task.get('__search_key__'), {'bigboard': False});       
            else:
                server.insert('twog/bigboard_record', {'title_code': title_code, 'bigboard_value': 'True', 'login': user_name})
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
