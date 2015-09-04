"""
This sends notifications to the assigned login group when work orders are created,
or when the assigned group is changed. The custom script in the database simply
calls the main function of this file, that way it can be integrated with GitHub.
"""

__author__ = 'Topher.Hughes'
__date__ = '03/09/2015'

import traceback


def get_notification_setting(login_group):
    """Get the notification setting for the login group.
    Return True if the group should get the notification.

    :param login_group: the login group name as a string
    :return: boolean if group should get notification or not
    """
    # TODO: use some kind of user/group setting
    if login_group == 'localization':
        return True
    return False


def main(server=None, event_data=None):
    """
    The main function of the custom script.

    :param server: the TacticServerStub object
    :param event_data: a dict with data like like search_key, search_type, sobject, and update_data
    :return: None
    """
    if not event_data:
        event_data = {}

    try:
        # CUSTOM_SCRIPT00107
        work_order = event_data.get('sobject')
        assigned_group = work_order.get('work_group')
        if assigned_group:
            if get_notification_setting(assigned_group):
                pass

    except AttributeError as e:
        traceback.print_exc()
        print str(e) + '\nMost likely the server object does not exist.'
    except KeyError as e:
        traceback.print_exc()
        print str(e) + '\nMost likely the event dictionary does not exist.'
    except Exception as e:
        traceback.print_exc()
        print str(e)


if __name__ == '__main__':
    main()
