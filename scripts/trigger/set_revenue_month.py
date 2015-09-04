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
        # CUSTOM_SCRIPT00049
        #print "IN SET REVENUE MONTH"
        from pyasm.common import SPTDate
        update_data = input.get('update_data')
        if 'due_date' in update_data.keys():
            if update_data.get('due_date') not in [None,'']:
                sobj = input.get('sobject')
                sk = input.get('search_key')
                if sobj.get('expected_delivery_date') in [None,''] and input.get('is_insert'):
                    server.update(sk, {'expected_revenue_month': SPTDate.convert_to_local(update_data.get('due_date')), 'expected_delivery_date': SPTDate.convert_to_local(update_data.get('due_date'))})
                elif not input.get('is_insert'):
                    do_it = True
                    if 'expected_delivery_date' in update_data.keys():
                        if update_data.get('expected_delivery_date') not in [None,'']:
                            do_it = False 
                    if do_it: 
                        server.update(sk, {'expected_revenue_month': SPTDate.convert_to_local(update_data.get('due_date')), 'expected_delivery_date': SPTDate.convert_to_local(update_data.get('due_date'))})
        #print "LEAVING SET REVENUE MONTH"
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
