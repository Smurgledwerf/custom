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
        # CUSTOM_SCRIPT00057
        def make_timestamp():
            import datetime
            now = datetime.datetime.now()
            return now.strftime("%Y-%m-%d %H:%M:%S")
        #print "IN TITLE COMPLETION"
        update_data = input.get('update_data')
        sk = input.get('search_key')
        sobj = input.get('sobject')
        if 'status' in update_data.keys():
            status = update_data.get('status')
            if status == 'Completed':
                server.update(sk, {'completion_date': make_timestamp()})
                other_titles = server.eval("@SOBJECT(twog/order['code','%s'].twog/title)" % sobj.get('order_code'))
                all_titles_completed = True
                for ot in other_titles:
                    if ot.get('status') not in ['Completed','Complete','completed','complete'] and ot.get('code') != sobj.get('code'):
                        all_titles_completed = False
                if all_titles_completed:
                    server.update(server.build_search_key('twog/order', sobj.get('order_code')), {'needs_completion_review': True})
             
        #print "LEAVING TITLE COMPLETION"
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
