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
        # CUSTOM_SCRIPT00076
        from pyasm.common import Environment
        update_data = input.get('update_data')
        prev_data = input.get('prev_data')
        sobject = input.get('sobject')
        login = Environment.get_login()
        user_name = login.get_login()
        name = sobject.get('title')
        season = sobject.get('season')
        if season not in [None,'']:
            name = '%s, SEASON: %s' % (name, season)
        episode = sobject.get('episode')
        if episode not in [None,'']:
            name = '%s, EPISODE: %s' % (name, episode)
        code = sobject.get('code')
        prevkeys = prev_data.keys()
        update_str = ''
        for key in prevkeys:
            if update_str == '':
                update_str = '[%s from:%s, to:%s]' % (key, prev_data[key], update_data[key])
            else:
                update_str = '%s[%s from:%s, to:%s]' % (update_str, key, prev_data[key], update_data[key])
        server.insert('twog/source_log', {'name': name, 'updates': update_str, 'login': user_name, 'source_code': code})
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
