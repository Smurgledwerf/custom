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
        # CUSTOM_SCRIPT00093
        def make_timestamp():
            #Makes a Timestamp for postgres
            import datetime
            now = datetime.datetime.now()
            return now.strftime("%Y-%m-%d %H:%M:%S")
        
        
        if 'update_data' in input.keys():
            update_data = input.get('update_data') 
            if 'indie_bigboard' in update_data.keys():
                indie_bigboard = update_data.get('indie_bigboard')
                if indie_bigboard in [None,False,'false','f','F',0]:
                    from pyasm.common import Environment
                    login = Environment.get_login().get_login() 
                    server.update(input.get('search_key'), {'removal_login': login, 'removal_timestamp': make_timestamp()})
        
                    #HERE NEED TO DETERMINE WHICH DEPT THIS WAS FOR AND SEE IF ANY OTHER WOs
                    #IN THE SAME DEPT ARE STILL INDIE. IF NOT, THEN TAKE THE DEPT NAME OUT OF 
                    #active_dept_priorities ON THE TITLE
                    sobject = input.get('sobject')
                    task_code = sobject.get('task_code')
                    task = server.eval("@SOBJECT(sthpw/task['code','%s'])" % task_code)[0]
                    alg = task.get('assigned_login_group')
                    lookup_code = sobject.get('lookup_code')
                    title_code = sobject.get('title_code')
                    others = server.eval("@SOBJECT(sthpw/task['title_code','%s']['indie_bigboard','True']['assigned_login_group','%s']['code','not in','%s'])" % (title_code, alg, task_code))
                    if len(others) == 0:
                        title = server.eval("@SOBJECT(twog/title['code','%s'])" % title_code)[0]
                        adps = title.get('active_dept_priorities')
                        if alg in adps:
                            new_adps = adps.replace(',%s' % alg, '').replace('%s,' % alg, '').replace(alg, '')
                            tdata = {'active_dept_priorities': new_adps}
                            prio_name = '%s_priority' % alg.replace(' supervisor','').replace(' ','_')
                            tdata[prio_name] = title.get('priority')
                            server.update(title.get('__search_key__'), tdata)
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
