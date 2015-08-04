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
        # CUSTOM_SCRIPT00036
        #print "IN SUBTRACT PRICES"
        data = input.get('data')
        price = float(data.get('price'))
        
        proj = server.eval("@SOBJECT(twog/proj['code','%s'])" % data.get('proj_code'))[0]
        current_proj_price_str = proj.get('price')
        current_proj_price = 0
        if current_proj_price_str not in [None,'']:
            current_proj_price = float(current_proj_price_str)
        new_proj_price = current_proj_price - price
        server.update(proj.get('__search_key__'), {'price': new_proj_price})
        
        title = server.eval("@SOBJECT(twog/title['code','%s'])" % proj.get('title_code'))[0]
        current_title_price_str = title.get('price')
        current_title_price = 0
        if current_title_price_str not in [None,'']:
            current_title_price = float(current_title_price_str) 
        new_title_price = current_title_price - price
        server.update(title.get('__search_key__'), {'price': new_title_price})
        
        order = server.eval("@SOBJECT(twog/order['code','%s'])" % title.get('order_code'))[0]
        current_order_price_str = order.get('price')
        current_order_price = 0
        if current_order_price_str not in [None,'']:
            current_order_price = float(current_order_price_str)
        new_order_price = current_order_price - price
        server.update(order.get('__search_key__'), {'price': new_order_price}) 
        #print "LEAVING SUBTRACT PRICES"
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
