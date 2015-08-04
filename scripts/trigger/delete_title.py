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
        # CUSTOM_SCRIPT00086
        from pyasm.common import TacticException
        sob = input.get('data')
        if sob.get('is_external_rejection') in ['true','True',True,'t',1]:
            raise TacticException('Sorry, you cannot delete an externally rejected title. We need that. Please deactivate the title if you want it to disappear from the Operator Views.')
        code = sob.get('code')
        order_code = sob.get('order_code')
        order = server.eval("@SOBJECT(twog/order['code','%s'])" % order_code)
        if order:
            order = order[0]
            order_title_total = int(order.get('titles_total'))
            if order_title_total in [None,'']:
                new_total = 0
            else:
                order_title_total = int(order_title_total)
                new_total = order_title_total - 1
            title_codes_completed = order.get('title_codes_completed')
            titles_completed = order.get('titles_completed')
            if titles_completed in [None,'']:
                titles_completed = 0
            else:
                titles_completed = int(titles_completed)
            if code in title_codes_completed:
                title_codes_completed = title_codes_completed.replace(',%s'  % code,'').replace('%s,'  % code,'').replace('%s'  % code,'')
                if titles_completed > 0:
                    titles_completed = titles_completed - 1
            server.update(order.get('__search_key__'), {'titles_total': new_total, 'titles_completed': titles_completed, 'title_codes_completed': title_codes_completed})
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
