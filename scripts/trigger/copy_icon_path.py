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
        # CUSTOM_SCRIPT00087
        # Do Not send external if location is internal
        def make_right_code_ending(sid):
            ending = str(sid)
            ending_len = len(ending)
            if ending_len < 5:
                zeros = 5 - ending_len
                for num in range (0, zeros):
                    ending = '0%s' % ending
            return ending
        import os
        from pyasm.common import Environment
        sobject = input.get('sobject')
        update_data = input.get('update_data')
        parent_type = update_data.get('search_type').split('?')[0]
        find_str = parent_type.split('/')[1].upper().split('?')[0]
        process = sobject.get('process')
        id = sobject.get('id')
        search_id = sobject.get('search_id')
        sea_t = update_data.get('search_type').split('?')[0]
        upper_st = sea_t.split('/')[1].upper()
        srch_id = update_data.get('search_id')
        full_ending = make_right_code_ending(srch_id)
        parent_code = '%s%s' % (upper_st, full_ending)
        parent_sk = server.build_search_key(sea_t, parent_code)
        parent_type = parent_sk.split('?')[0]
        if find_str == 'ORDER' and process == 'icon':
            preview_path = server.get_path_from_snapshot(sobject.get('code'), mode="web")
            server.update(parent_sk, {'icon_path': preview_path})
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
