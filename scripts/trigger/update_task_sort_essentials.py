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
        # CUSTOM_SCRIPT00046
        #print "UPDATE TASK SORT ESSENTIALS"
        from pyasm.common import SPTDate
        update_data = input.get('update_data')
        sobject = input.get('sobject')
        if 'twog/title' in sobject.get('search_type'):
            server.update(input.get('search_key'), {'tripwire': ''}, triggers=False)
            proj_sk = server.build_search_key('twog/proj', sobject.get('lookup_code'))
            proj_data = {}
            task_data = {}
            if 'bid_end_date' in update_data:
                proj_data['due_date'] = SPTDate.convert_to_local(update_data.get('bid_end_date'))
                task_data['bid_end_date'] = proj_data['due_date']
            if proj_data != {}:
                server.update(proj_sk, proj_data, triggers=False)
                wos = server.eval("@SOBJECT(twog/work_order['proj_code','%s'])" % sobject.get('lookup_code'))
                for wo in wos:
                    server.update(wo.get('__search_key__'), proj_data, triggers=False) 
                    if wo.get('task_code') not in [None,'']:
                        task = server.eval("@SOBJECT(sthpw/task['code','%s'])" % wo.get('task_code'))
                        if len(task) > 0:
                            task = task[0]
                            task_data['tripwire'] = ''
                            server.update(task.get('__search_key__'), task_data, triggers=False)
        elif 'twog/proj' in sobject.get('search_type'):
            wo_sk = server.build_search_key('twog/work_order', sobject.get('lookup_code'))
            wo_data = {}
            if 'bid_end_date' in update_data:
                wo_data['due_date'] = SPTDate.convert_to_local(update_data.get('bid_end_date'))
            if wo_data != {}:
                server.update(wo_sk, wo_data, triggers=False)
        #print "LEAVING UPDATE TASK SORT ESSENTIALS"
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
