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
        # CUSTOM_SCRIPT00069
        sobject = input.get('sobject')
        update_data = input.get('update_data')
        lookup_code = sobject.get('lookup_code')
        status = update_data.get('status')
        if 'PROJ' in lookup_code and status == 'Ready':
            proj = server.eval("@SOBJECT(twog/proj['code','%s'])" % lookup_code)[0]
            title = server.eval("@SOBJECT(twog/title['code','%s'])" % proj.get('title_code'))[0]
            if proj.get('priority') not in [None,''] and title.get('priority_triggers') != 'No':
                title_sk = title.get('__search_key__')
                server.update(title_sk, {'priority': proj.get('priority')}, triggers=False)
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
