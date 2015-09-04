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
        # CUSTOM_SCRIPT00033
        #print "IN KICKOFF FROM PROJ READY"
        COMPLETE = 'Completed'
        READY = 'Ready'
        sobj = input.get('sobject')
        this_process = sobj.get('process')
        this_lookup = sobj.get('lookup_code')
        if this_lookup.find('PROJ') != -1: 
            sk = input.get('search_key')
            if sobj.get('status') == READY: 
                proj = server.eval("@SOBJECT(twog/proj['code','%s'])" % this_lookup)[0]
                wos = server.eval("@SOBJECT(twog/work_order['proj_code','%s'])" % proj.get('code'))
                title = server.eval("@SOBJECT(twog/title['code','%s'])" % proj.get('title_code'))[0]
                if title.get('status_triggers') != 'No':
                    for wo in wos: 
                        this_process = wo.get('process')
                        info = server.get_pipeline_processes_info(proj.get('__search_key__'), related_process=this_process)
                        input_processes = info.get('input_processes')
                        if len(input_processes) < 1:
                            task = server.eval("@SOBJECT(sthpw/task['code','%s'])" % wo.get('task_code'))[0] 
                            if task.get('status') not in ['In Progress','In_Progress','On Hold','On_Hold','Client Response','Review','Approved','Ready','DR In_Progress','DR In Progress','Amberfin01_In_Progress','Amberfin01 In Progress', 'Amberfin02_In_Progress','Amberfin02 In Progress','BATON In_Progress','BATON In Progress','Export In_Progress','Export In Progress','Need Buddy Check','Buddy Check In_Progress','Buddy Check In Progress','Rejected','Completed','Waiting','Need Assistance','Failed QC','Rejected','Fix Needed','In Review']:
                                server.update(task.get('__search_key__'), {'status': READY})
        #print "LEAVING KICKOFF 2"
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
