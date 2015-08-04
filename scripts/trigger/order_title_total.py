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
        # CUSTOM_SCRIPT00085
        sk = input.get('search_key')
        sob = input.get('sobject')
        order_code = sob.get('order_code')
        order = server.eval("@SOBJECT(twog/order['code','%s'])" % order_code)
        print "OTT ORDER = %s" % order
        if order:
            order = order[0]
            order_title_total = order.get('titles_total')
            print "OTT TT = %s" % order_title_total
            if order_title_total in [None,'']:
                order_title_total = 0
            else:
                order_title_total = int(order_title_total)
            new_total = order_title_total + 1
            print "OTT NEW TOTAL = %s" % new_total
            server.update(order.get('__search_key__'), {'titles_total': new_total}, triggers=False)
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
