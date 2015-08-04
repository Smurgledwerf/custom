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
        # CUSTOM_SCRIPT00075
        from pyasm.common import Environment
        update_data = input.get('update_data')
        prev_data = input.get('prev_data')
        sobject = input.get('sobject')
        login = Environment.get_login()
        user_name = login.get_login()
        name = ''
        if 'TITLE' in sobject.get('code'):
            name = sobject.get('title')
            if sobject.get('episode') not in [None,'']:
                name = '%s: %s' % (name, sobject.get('episode'))
        else:
            title = server.eval("@SOBJECT(twog/title['code','%s'])" % sobject.get('title_code'))[0]
            name = title.get('title')
            if title.get('episode') not in [None,'']:
                name = '%s: %s' % (name, title.get('episode'))
            name = '%s -> %s' % (name, sobject.get('process')) 
        from_priority = prev_data.get('priority')
        if from_priority in [None,'']:
            from_priority = 100
        server.insert('twog/priority_log', {'to_priority': update_data.get('priority'), 'from_priority': from_priority, 'login': user_name, 'lookup_code': sobject.get('code'), 'name': name})
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
