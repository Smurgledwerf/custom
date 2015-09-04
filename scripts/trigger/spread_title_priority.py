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
        # CUSTOM_SCRIPT00094
        if 'update_data' in input.keys():
            update_data = input.get('update_data') 
            if 'priority' in update_data.keys():
                prev_data = input.get('prev_data')
                old_priority = prev_data.get('priority')
                title = input.get('sobject')
                active_dept_priorities = title.get('active_dept_priorities')
                priority = update_data.get('priority')
                sk = input.get('search_key')
                depts = ['audio','compression','edeliveries','edit','machine room','media vault','qc','vault']
                do_data = {}
                do_the_do = False
                for dept in depts:
                    if dept not in active_dept_priorities:
                        prio_name = '%s_priority' % dept.replace(' ','_')
                        #ONLY CHANGE THE DEPT PRIORITY IF IT'S VALUE IS THE SAME AS THE OLD (JUST CHANGED) TITLE MAIN PRIORITY
                        if title.get(prio_name) == old_priority:
                            do_data[prio_name] = priority
                            do_the_do = True
                if do_the_do:
                    server.update(sk, do_data)
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
