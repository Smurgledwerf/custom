"""
This file was generated automatically from a custom script found in Project -> Script Editor.
The custom script was moved to a file so that it could be integrated with GitHub.
"""

__author__ = 'Topher.Hughes'
__date__ = '04/08/2015'

import traceback


def main(server=None, event_data=None):
    """
    The main function of the custom script.

    :param server: the TacticServerStub object
    :param event_data: a dict with data for the event containing:
    'is_insert': True or False
    'mode': 'insert', 'update', 'retire'
    'prev_data': dict of {column: values} before the update
    'update_data': dict of {column: values} that were updated
    'search_type': search type of triggering sobject
    'search_code': code of the sobject
    'search_key': search key of the sobject
    'sobject': the triggering sobject
    'trigger_sobject': the config/trigger sobject itself
    :return: None
    """
    if not event_data:
        event_data = {}

    try:
        # CUSTOM_SCRIPT00108
        # this is a test file
        
        from pprint import pprint
        import sys
        pprint(sys.path)
        print 'hello world'
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
