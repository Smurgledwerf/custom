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
        # CUSTOM_SCRIPT00105
        def make_timestamp():
            from pyasm.common import SPTDate
            #Makes a Timestamp for postgres
            import datetime
            now = SPTDate.convert_to_local(datetime.datetime.now())
            now = datetime.datetime.now()
            return now
        
        from pyasm.common import Environment
        if 'update_data' in input.keys():
            from pyasm.common import SPTDate
            login = Environment.get_login()
            user_name = login.get_login()
            update_data = input.get('update_data') 
            ukeys = update_data.keys()
            sobject = input.get('sobject')
            history = sobject.get('history_log')
            line = '[???[x^LOGIN: %s^x][x^TIMESTAMP: %s^x]' % (user_name, make_timestamp())
            for u in ukeys:
                line = '%s[^x%s: %sx^]' % (line, u.upper(), update_data.get(u))
            line = '%s???]' % line
            history = '%s%s' % (history, line)
            server.update(input.get('search_key'), {'history_log': history}, triggers=False)
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
