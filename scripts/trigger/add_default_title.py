"""
This adds the default title to new orders. The title will contain one project with one work order.
Onboarding will be assigned to the work order so that it will show up on their hotlist.
"""

__author__ = 'Topher.Hughes'
__date__ = '15/10/2015'

import traceback


def main(server=None, event_data=None):
    """
    The main function of the custom script.

    :param server: the TacticServerStub object
    :param event_data: a dict with data for the event containing:
    'is_insert': True or False
    'mode': 'insert', 'update', 'retire'
    'prev_data': dict of column: values before the update
    'update_data': dict of column: values that were updated
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
        # CUSTOM_SCRIPT
        
        order = event_data.get('sobject')
        title_name = order.get('name') + ' - Onboarding'
        title_data = {'order_code': order.get('code'), 'title': title_name, 'onboarding_priority': '1',
                      'pipeline_code': 'New_Order_Onboarding', 'client_code': order.get('client_code'),
                      'start_date': order.get('start_date'), 'due_date': order.get('due_date')}

        server.execute_cmd('manual_updaters.commander.CreateTitlesCmd', args={'episodes': [''], 'data': title_data})

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
