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
        # CUSTOM_SCRIPT00039
        code = input.get('search_key').split('code=')[1]
        #print "TRICKLE UP NEW COST. Code = %s" % code
        #print "TUNC INPUT = %s" % input
        sts = {'twog/equipment_used': ['twog/work_order','work_order_code'],'twog/work_order': ['twog/proj','proj_code'],'twog/proj': ['twog/title','title_code'], 'twog/title': ['twog/order','order_code']}
        st = input.get('search_type').split('?')[0]
        sobject = input.get('sobject')
        update_data = input.get('update_data')
        prev_data = input.get('prev_data')
        parent_obj = server.eval("@SOBJECT(%s['code','%s'])" % (sts[st][0], sobject.get(sts[st][1])))
        data = {}
        do_expected = False
        do_actual = False
        if parent_obj:
            parent_obj = parent_obj[0]
            if 'expected_cost' in update_data.keys():
                do_expected = True
                parent_expected_cost = parent_obj.get('expected_cost')
                if parent_expected_cost in [None,'']:
                    parent_expected_cost = 0
                else:
                    parent_expected_cost = float(parent_expected_cost)
                old_expected_cost = prev_data.get('expected_cost')
                new_expected_cost = update_data.get('expected_cost')
                if old_expected_cost in [None,'']:
                    old_expected_cost = 0
                else:
                    old_expected_cost = float(old_expected_cost)
                if new_expected_cost in [None,'']:
                    new_expected_cost = 0
                else:
                    new_expected_cost = float(new_expected_cost)
                #print "NPEC = %s [(PEC = %s) - (OEC = %s) + (NEC = %s)]" % (parent_expected_cost - old_expected_cost + new_expected_cost, parent_expected_cost, old_expected_cost, new_expected_cost) 
                new_parent_expected_cost = parent_expected_cost - old_expected_cost + new_expected_cost
                data['expected_cost'] = new_parent_expected_cost
                
            if 'actual_cost' in update_data.keys():
                #print "PARENT_OBJ %s, ACTUAL COST = %s" % (parent_obj.get('code'), parent_obj.get('actual_cost'))
                do_actual = True
                parent_actual_cost = parent_obj.get('actual_cost')
                if parent_actual_cost in [None,'']:
                    parent_actual_cost = 0
                else:
                    parent_actual_cost = float(parent_actual_cost)
                old_actual_cost = prev_data.get('actual_cost')
                new_actual_cost = update_data.get('actual_cost')
                if old_actual_cost in [None,'']:
                    old_actual_cost = 0
                else:
                    old_actual_cost = float(old_actual_cost)
                if new_actual_cost in [None,'']:
                    new_actual_cost = 0
                else:
                    new_actual_cost = float(new_actual_cost)
                #print "NPAC = %s [(PAC = %s) - (OAC = %s) + (NAC = %s)]" % (parent_actual_cost - old_actual_cost + new_actual_cost, parent_actual_cost, old_actual_cost, new_actual_cost) 
                new_parent_actual_cost = parent_actual_cost - old_actual_cost + new_actual_cost
                data['actual_cost'] = new_parent_actual_cost
            if do_expected or do_actual:
                #print "UPDATING %s with %s" % (parent_obj.get('code'), data)
                server.update(parent_obj.get('__search_key__'), data)
        #print "LEAVING TRICKLE UP NEW COST. Code = %s" % code
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
