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
        # CUSTOM_SCRIPT00082
        def make_timestamp():
            #Makes a Timestamp for postgres
            import datetime
            now = datetime.datetime.now()
            return now.strftime("%Y-%m-%d %H:%M:%S")
        
        from pyasm.common import Environment
        login = Environment.get_login()
        user_name = login.get_login()
        update_data = input.get('update_data')
        sobject = input.get('sobject')
        client_billing = update_data.get('billing_status')
        client_code = sobject.get('code')
        new_task_str = ''
        if client_billing == 'On Hold - Do Not Book':
            new_task_str = 'nobook'
        if client_billing == 'On Hold - Do Not Ship':
            new_task_str = 'noship'
        server.execute_cmd('manual_updaters.commander.ClientBillingTaskVisibilityCmd', {'client_code': client_code, 'new_task_str': new_task_str})
        client_sk = server.build_search_key('twog/client', client_code)
        timestamp = make_timestamp()
        note = "%s has been set to '%s' by %s on %s" % (sobject.get('name'), client_billing, user_name, timestamp)
        note_ccs = 'stephen.buchsbaum@2gdigital.com;accounting@2gdigital.com'
        server.execute_cmd('operator_view.MakeNoteWdg', {'obj_sk': client_sk, 'header': client_billing + ' ' + timestamp, 'note': note, 'note_ccs': note_ccs})
    except AttributeError as e:
        traceback.print_exc()
        print str(e) + '\nMost likely the server object does not exist.'
        raise e
    except KeyError as e:
        traceback.print_exc()
        print str(e) + '\nMost likely the input dictionary does not exist.'
        raise e
    except Exception as e:
        traceback.print_exc()
        print str(e)
        raise e


if __name__ == '__main__':
    main()
