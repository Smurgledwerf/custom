"""
This sends notifications to the assigned login group when work orders are created,
or when the assigned group is changed. The custom script in the database simply
calls the main function of this file, that way it can be integrated with GitHub.
"""

__author__ = 'Topher.Hughes'
__date__ = '03/09/2015'

import traceback


def get_notification_setting(login_group, server):
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
    :param event_data: a dict with data like search_key, search_type, sobject, and update_data
    :return: None
    """
    if not event_data:
        event_data = {}

    try:
        # CUSTOM_SCRIPT00107
        work_order = event_data.get('sobject')
        assigned_group = work_order.get('work_group')
        if assigned_group and get_notification_setting(assigned_group, server):
            from formatted_emailer import EmailDirections, email_sender
            order_code = work_order.get('order_code')
            ed = EmailDirections(order_code=order_code)
            internal_data = ed.get_internal_data()
            title = server.query('twog/title', filters=[('code', work_order.get('title_code'))])
            title = title[0] if title else {}

            subject = 'Work Order "{0}" assigned to "{1}"'.format(work_order.get('process'), assigned_group)
            message = work_order.get('instructions')
            internal_data['subject'] = subject
            internal_data['message'] = message
            internal_data['work_order_code'] = work_order.get('code')
            internal_data['work_order_name'] = work_order.get('process')
            internal_data['title_code'] = title.get('code')
            internal_data['title_name'] = title.get('title')

            email_template = '/opt/spt/custom/formatted_emailer/work_order_email_template.html'
            email_file_name = 'work_order_inserted/work_order_{0}.html'.format(work_order.get('code'))
            email_sender.send_email(template=email_template, email_data=internal_data, email_file_name=email_file_name)

    except AttributeError as e:
        traceback.print_exc()
        print str(e) + '\nMost likely the server object does not exist.'
        raise e
    except KeyError as e:
        traceback.print_exc()
        print str(e) + '\nMost likely the event dictionary does not exist.'
        raise e
    except Exception as e:
        traceback.print_exc()
        print str(e)
        raise e


if __name__ == '__main__':
    main()
