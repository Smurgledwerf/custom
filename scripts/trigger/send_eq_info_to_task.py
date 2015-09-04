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
        # CUSTOM_SCRIPT00098
        #
        # Created By Matthew Tyler Misenhimer
        #
        # This trigger is run on update of a work order's eq_info
        # It passes the eq_info from the wo to the connected task
        if 'update_data' in input.keys():
            update_data = input.get('update_data') 
            if 'eq_info' in update_data.keys():
                eq_info = update_data.get('eq_info')
                sobject = input.get('sobject')
                task_code = sobject.get('task_code')
                if task_code not in [None,'']:
                    task_sk = server.build_search_key('sthpw/task', task_code)
                    server.update(task_sk, {'eq_info': eq_info}, triggers=False)
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
