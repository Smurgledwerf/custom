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
        # CUSTOM_SCRIPT00071
        sobject = input.get('data')
        eq_u_code = sobject.get('code')
        wo_code = sobject.get('work_order_code')
        if 'WORK_HOUR' not in wo_code:
            wo = server.eval("@SOBJECT(twog/work_order['code','%s'])" % wo_code)
            if wo:
                wo = wo[0]
                info_s = wo.get('eq_info').split('Z,Z')
                new_str = ''
                for info in info_s:
                   if eq_u_code not in info:
                       if new_str == '':
                           new_str = info
                       else:
                           new_str = '%sZ,Z%s' % (new_str, info)
                if new_str not in [None,'']:
                    server.update(wo.get('__search_key__'), {'eq_info': new_str})
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
