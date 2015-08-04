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
        # CUSTOM_SCRIPT00070
        print "IN GIVE TITLE PROJ PRIORITY 2"
        sobject = input.get('sobject')
        update_data = input.get('update_data')
        priority = update_data.get('priority')
        task_code = sobject.get('task_code')
        task = server.eval("@SOBJECT(sthpw/task['code','%s'])" % task_code)
        if task:
            task = task[0]
            status = task.get('status') 
            title = server.eval("@SOBJECT(twog/title['code','%s'])" % sobject.get('title_code'))[0]
            if title.get('priority_triggers') != 'No':
                if status in ['Ready','In_Progress','In Progress','DR In_Progress','DR In Progress', 'Amberfin01_In_Progress','Amberfin01 In Progress','Amberfin02_In_Progress','Amberfin02 In Progress','BATON In_Progress','BATON In Progress','Export In_Progress','Export In Progress','Need Buddy Check','Buddy Check In_Progress','Buddy Check In Progress','In Review']:
                    server.update(title.get('__search_key__'), {'priority': priority}, triggers=False)
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
