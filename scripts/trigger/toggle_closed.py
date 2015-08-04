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
        # CUSTOM_SCRIPT00034
        #print "TOGGLE CLOSED INPUT = %s" % input
        sobject = input.get('sobject')
        update_data = input.get('update_data')
        #print "CLOSED UPDATE_DATA = %s" % update_data
        if 'closed' in update_data.keys():
            #print "CLOSED IN IF"
            new_val = update_data.get('closed')
            #print "CLOSED NEW_VAL = %s" % new_val
            stes = ['twog/order','twog/title','twog/proj','twog/work_order']
            fk = ['order_code','title_code','proj_code','work_order_code']
            st = input.get('search_type').split('?')[0]
            #print "CLOSED ST = %s" % st
            idx = int(stes.index(st))
            nidx = idx + 1
            #print "CLOSED NIDX =%s" % nidx
            if st != 'twog/work_order':
                my_kids_expr = "@SOBJECT(%s['%s','%s'])" % (stes[nidx], fk[idx], sobject.get('code'))
                #print "CLOSED MY KIDS EXPR =%s" % my_kids_expr
                my_kids = server.eval(my_kids_expr)
                #print "CLOSED MY_KIDS LEN = %s" % len(my_kids)
                for kid in my_kids:
                    server.update(kid.get('__search_key__'), {'closed': new_val})
        
            if st in ['twog/proj','twog/work_order']:
                task_code = sobject.get('task_code')
                if task_code not in [None,'']:
                    task = server.eval("@SOBJECT(sthpw/task['code','%s'])" % task_code)
                    if task:
                        task = task[0]
                        server.update(task.get('__search_key__'), {'closed': new_val})
        #print "LEAVING TOGGLE CLOSED"
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
