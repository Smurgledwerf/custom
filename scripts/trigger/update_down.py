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
        # CUSTOM_SCRIPT00044
        def removekey(d, key):
            r = dict(d)
            del r[key]
            return r
        # This will act as a recursive trigger.
        if 'update_data' in input.keys():
            from pyasm.common import SPTDate
        
            update_data = input.get('update_data') 
            ukeys = update_data.keys()
            sobject = input.get('sobject')
            keep_going = True
            if 'tripwire' in ukeys:
                if update_data.get('tripwire') == 'No Send Back':
                    keep_going = False
                    task = server.eval("@SOBJECT(sthpw/task['code','%s'])" % sobject.get('task_code'))
                    if task:
                        task = task[0]
                        server.update(task.get('__search_key__'), {'tripwire': ''}, triggers=False)
                        server.update(input.get('search_key'), {'tripwire': ''}, triggers=False)
            if keep_going:
                prev_data = input.get('prev_data')
                sobject = input.get('sobject')
                search_type = input.get('search_type').split('?')[0]
                search_key = input.get('search_key')
                code = search_key.split('code=')[1]
                st_kids = {'twog/order': ['twog/title', 'order_code'], 'twog/title': ['twog/proj', 'title_code'], 'twog/proj': ['twog/work_order', 'proj_code']}
                kids_data = {}
                task_data = {}
                if 'po_number' in ukeys:
                    kids_data['po_number'] = update_data.get('po_number')
                    task_data['po_number'] = update_data.get('po_number')
                if 'name' in ukeys and search_type == 'twog/order':
                    kids_data['order_name'] = update_data.get('name')
                if 'order_name' in ukeys:
                    kids_data['order_name'] = update_data.get('order_name')
                    task_data['order_name'] = update_data.get('order_name')
                if 'territory' in ukeys:
                    kids_data['territory'] = update_data.get('territory')
                    task_data['territory'] = update_data.get('territory')
                if 'title' in ukeys:
                    kids_data['title'] = update_data.get('title')
                    task_data['title'] = update_data.get('title')
                if 'episode' in ukeys: 
                    kids_data['episode'] = update_data.get('episode')
                    task_data['episode'] = update_data.get('episode')
                if 'platform' in ukeys: 
                    kids_data['platform'] = update_data.get('platform')
                    task_data['platform'] = update_data.get('platform')
                if 'title_id_number' in ukeys: 
                    kids_data['title_id_number'] = update_data.get('title_id_number')
                    task_data['title_id_number'] = update_data.get('title_id_number')
                if 'login' in ukeys: 
                    kids_data['login'] = update_data.get('login')
                    task_data['login'] = update_data.get('login')
                if 'client_code' in ukeys: 
                    cl_c = update_data.get('client_code')
                    if cl_c not in [None,'']:
                        kids_data['client_code'] = cl_c 
                        task_data['client_code'] = cl_c 
                if 'client_name' in ukeys: 
                    cl_n =  update_data.get('client_name')
                    if cl_n not in [None,'']:
                        kids_data['client_name'] = cl_n 
                        task_data['client_name'] = cl_n 
                if 'status' in ukeys and search_type not in ['twog/order','twog/title']:
                    task_data['status'] = update_data.get('status')
                if 'expected_delivery_date' in ukeys and search_type != 'twog/title':
                    kids_data['expected_delivery_date'] = SPTDate.convert_to_local(update_data.get('expected_delivery_date'))
                if 'due_date' in ukeys:
                    kids_data['due_date'] = SPTDate.convert_to_local(update_data.get('due_date'))
                    if search_type in ['twog/proj','twog/work_order']:
                        task_data['bid_end_date'] = kids_data['due_date']
                if 'start_date' in ukeys:
                    kids_data['start_date'] = SPTDate.convert_to_local(update_data.get('start_date'))
                    if search_type in ['twog/proj','twog/work_order']:
                        task_data['bid_start_date'] = kids_data['start_date']
                if kids_data != {} and search_type != 'twog/work_order':
                    kids_expr = "@SOBJECT(%s['%s','%s'])" % (st_kids[search_type][0], st_kids[search_type][1], code)
                    kids = server.eval(kids_expr)
                    for kid in kids:
                        server.update(kid.get('__search_key__'), kids_data) 
                if task_data != {} and search_type in ['twog/proj','twog/work_order']:
                    task_code = sobject.get('task_code')
                    if task_code not in [None,'']:
                        task = server.eval("@SOBJECT(sthpw/task['code','%s'])" % task_code)
                        if task:
                            task = task[0]
                            if 'status' in task_data.keys():
                                task_data['tripwire'] = 'No Send Back'
                            server.update(task.get('__search_key__'), task_data)
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
