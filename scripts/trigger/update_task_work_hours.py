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
        # CUSTOM_SCRIPT00099
        sobject = input.get('sobject')
        user = sobject.get('login')
        straight_time = sobject.get('straight_time')
        straight_time = float(straight_time)
        task_code = sobject.get('task_code')
        if task_code not in [None,'']:
            task = server.eval("@SOBJECT(sthpw/task['code','%s'])" % task_code)
            if task:
                task = task[0]
                work_hours = task.get('work_hours_str')
                if user in work_hours:
                    whs = work_hours.split('%s:' % user)[1]
                    hours_str = whs.split('|')[0]
                    hours = float(hours_str)
                    new_hours = straight_time + hours
                    work_hours = work_hours.replace('%s:%s' % (user,hours_str), '%s:%s' % (user, new_hours))
                else:
                    if work_hours in [None,'']:
                        work_hours = '%s:%s' % (user, straight_time)
                    else:
                        work_hours = '%s|%s:%s' % (work_hours, user, straight_time)
                total_work_hours = task.get('total_work_hours')
                if total_work_hours in [None,'']:
                    total_work_hours = 0
                total_work_hours = float(total_work_hours)
                total_work_hours = total_work_hours + straight_time
                server.update(task.get('__search_key__'), {'work_hours_str': work_hours, 'total_work_hours': total_work_hours}, triggers=False)
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
