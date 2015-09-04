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
        # CUSTOM_SCRIPT00097
        #
        # Created By Matthew Tyler Misenhimer
        #
        # This trigger is run on update of a task's status
        # It records the date that the task was originally set to 'Ready'
        def make_timestamp():
            from pyasm.common import SPTDate
            #Makes a Timestamp for postgres
            import datetime
            now = SPTDate.convert_to_local(datetime.datetime.now())
            return now
        
        if 'update_data' in input.keys():
            update_data = input.get('update_data') 
            if 'status' in update_data.keys():
                status = update_data.get('status')
                if status == 'Ready':
                    sobject = input.get('sobject')
                    set_to_ready_date = sobject.get('set_to_ready_date')
                    if set_to_ready_date in [None,'']:
                        server.update(input.get('search_key'), {'set_to_ready_date': make_timestamp()}, triggers=False)
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
