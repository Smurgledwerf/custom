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
        # CUSTOM_SCRIPT00080
        #print "IN REMOVE FROM COMPLETION RATIO"
        data = input.get('data')
        title_code = data.get('title_code')
        order_code = data.get('order_code')
        title = server.eval("@SOBJECT(twog/title['code','%s'])" % title_code)
        order = server.eval("@SOBJECT(twog/order['code','%s'])" % order_code)
        task_expr = "@SOBJECT(sthpw/task['lookup_code','%s'])" % data.get('code')
        task = server.eval(task_expr)
        decrement = 0
        if task:
            task = task[0]
            if task.get('status') == 'Completed': 
                decrement = 1
        classification = 'Bid'
        if order:
            classification = order[0].get('classification')
        if title and classification not in ['master','bid','Master','Bid']:
            title = title[0]
            wo_count = title.get('wo_count')
            wo_count = wo_count - 1
            data1 = {'wo_count': wo_count}
            if decrement == 1:
                wo_completed = title.get('wo_completed')
                wo_completed = wo_completed - decrement
                data1['wo_completed'] = wo_completed
            server.update(title.get('__search_key__'), data1)
        if order and classification not in ['master','bid','Master','Bid']:
            order = order[0]
            wo_count = order.get('wo_count')
            wo_count = wo_count - 1
            data2 = {'wo_count': wo_count}
            if decrement == 1:
                wo_completed = order.get('wo_completed')
                wo_completed = wo_completed - decrement
                data2['wo_completed'] = wo_completed
            server.update(order.get('__search_key__'), data2)
        #print "LEAVING REMOVE FROM COMPLETION RATIO"
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
