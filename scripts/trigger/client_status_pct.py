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
        # CUSTOM_SCRIPT00066
        client_stat_lookup = {
        'Waiting on client materials': 0,
        'Materials received': 20,
        'In Production': 40,
        'In production': 40,
        'In_Production': 40,
        'In_production': 40,
        'QC rejected': 75,
        'QC passed': 75,
        'QC Rejected': 75,
        'QC Passed': 75,
        'Fixes': 60,
        'Out for client approval': 50,
        'Delivered': 100,
        'Invoiced': 100,
        'Complete': 100,
        'Completed': 100
        }
        sob = input.get('sobject')
        numeric = 0
        if sob.get('client_status') not in [None,'']:
            numeric = client_stat_lookup[sob.get('client_status')]
        server.update(input.get('search_key'), {'numeric_client_status': numeric})
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
