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
        # CUSTOM_SCRIPT00059
        # Matthew Tyler Misenhimer
        # Do not send external if location is internal
        # This was made to send info about an order after the order sobject has been edited
        def make_timestamp():
            import datetime
            now = datetime.datetime.now()
            return now.strftime("%Y-%m-%d %H:%M:%S")
        
        def get_time_date_dict(str_time):
            pre_split = str_time.split('.')[0]
            first_split = pre_split.split(' ')
            date = first_split[0]
            time = first_split[1]
            date_split = date.split('-')
            dt = {}
            dt['year'] = int(date_split[0])
            dt['month'] = int(date_split[1])
            dt['day'] = int(date_split[2])
            dt['date'] = date
            dt['time'] = time
            time_split = time.split(':')
            dt['hour'] = int(time_split[0])
            dt['minute'] = int(time_split[1])
            dt['second'] = int(time_split[2])
            dt['big_time'] = float((dt['hour'] * 3600) + (dt['minute'] * 60) + dt['second'])
            return dt
        
        def compare_dt_dicts(dt1, dt2):
            # This is rough. Don't use it for anything else. Should work for this though.
            difference = 0
            newest = -1
            dt1_bignum = float(float((dt1['year'] - 2000) * 365 * 24 * 3600) + float((dt1['month'] - 1) * 31 * 24 * 3600) + float((dt1['day'] - 1) * 24 * 3600) + dt1['big_time'])    
            dt2_bignum = float(float((dt2['year'] - 2000) * 365 * 24 * 3600) + float((dt2['month'] - 1) * 31 * 24 * 3600) + float((dt2['day'] - 1) * 24 * 3600) + dt2['big_time'])    
            difference = dt2_bignum - dt1_bignum
            if difference < 0:
                newest = 0
            else:
                newest = 1
            return [difference, newest]
        
        def fix_date(date):
            #This is needed due to the way Tactic deals with dates (using timezone info), post v4.0
            from pyasm.common import SPTDate
            return_date = ''
            date_obj = SPTDate.convert_to_local(date)
            if date_obj not in [None,'']:
                return_date = date_obj.strftime("%Y-%m-%d  %H:%M")
            return return_date
        
        def fix_note_chars(note):
            if isinstance(note, bool):
                note2 = 'False'
                if note:
                    note2 = 'True'
                note = note2
            else:
                import sys
                from json import dumps as jsondumps
                if note not in [None,'']:
                    if sys.stdout.encoding:
                        note = note.decode(sys.stdout.encoding)
                note = jsondumps(note)
                note = note.replace('||t','&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
                note = note.replace('\\\\t','&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
                note = note.replace('\\\t','&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
                note = note.replace('\\t','&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
                note = note.replace('\t','&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
                note = note.replace('\\"','"')
                note = note.replace('\"','"')
                note = note.replace('||n','<br/>')
                note = note.replace('\\\\n','<br/>')
                note = note.replace('\\\n','<br/>')
                note = note.replace('\\n','<br/>')
                note = note.replace('\n','<br/>')
            return note
        
        
        allow_client_emails = True
        #print "In Order Edited"
        order = input.get('sobject')
        client_code = order.get('client_code')
        update_data = input.get('update_data')
        prev_data = input.get('prev_data')
        sob_timestamp = order.get('timestamp')
        now_time = make_timestamp()
        dt1 = get_time_date_dict(sob_timestamp)
        dt2 = get_time_date_dict(now_time)
        rez = compare_dt_dicts(dt1, dt2)
        go_or_no = True
        good_count = 0
        for key, val in update_data.iteritems():
            #We don't care about changes to the following fields
            if key in ['login','initial_po_upload_list','actual_cost','classification','completion_date','invoiced_date','closed','expected_price','client_email_list','expected_cost','keywords','seen_by','prev_seen_by']:
                go_or_no = False
            else:
                good_count = good_count + 1
        if client_code in [None,'']:
            go_or_no = False
        if good_count > 0:
            go_or_no = True
        if go_or_no:
            if rez[1] == 1:
                if rez[0] > 5:
                    # If more than 5 seconds have passed since the time of this order's creation, then it is ok to send the email notification
                    import os
                    from pyasm.common import Environment
                    from formatted_emailer import EmailDirections
                    external_template_file = '/opt/spt/custom/formatted_emailer/external_email_template.html'
                    internal_template_file = '/opt/spt/custom/formatted_emailer/internal_email_template.html'
                    order_code = order.get('code')
                    ed = EmailDirections(order_code=order_code)
                    int_data = ed.get_internal_data()
                    ext_data = ed.get_external_data()
                    subject = '2G-ORDER-EDIT-"%s" PO#: %s' % (int_data['order_name'], int_data['po_number'])
                    if ext_data['client_email'] == '' and ext_data['location'] == 'external':
                        subject = 'NOT SENT TO CLIENT!? %s' % subject
                    subject_see = subject
                    subject = subject.replace(' ','..')
                    initial_po_upload_list = order.get('initial_po_upload_list')
                    message = '%s has edited an order. Order Name = "%s"  PO Number = "%s".' % (int_data['from_name'].replace('.',' '), int_data['order_name'], int_data['po_number'])
                    message = '%s<br/>Edits Made:' % message
                    
                    added_update = False
                    for key, val in update_data.iteritems():
                        # Report the change of previous value to new value - if it isnt one of these fields
                        if str(prev_data[key]) != str(val) and key not in ['login','initial_po_upload_list','actual_cost','classification','completion_date','invoiced_date','closed','expected_price','client_email_list','expected_cost','keywords','seen_by','prev_seen_by']:
                            message = '%s<br/>%s: "%s"  --- Used to be "%s"' % (message, key, val, prev_data[key])  
                            added_update = True
        
                    message = fix_note_chars(message)
                    if added_update:
                        template = open(internal_template_file, 'r')
                        filled = ''
                        for line in template:
                            line = line.replace('[ORDER_CODE]', int_data['order_code'])
                            line = line.replace('[PO_NUMBER]', int_data['po_number'])
                            line = line.replace('[CLIENT_EMAIL]', int_data['client_email'])
                            line = line.replace('[EMAIL_CC_LIST]', int_data['ccs'])
                            line = line.replace('[SCHEDULER_EMAIL]', int_data['scheduler_email'])
                            line = line.replace('[SUBJECT]', subject_see)
                            line = line.replace('[MESSAGE]', message)
                            line = line.replace('[CLIENT]', int_data['client_name'])
                            line = line.replace('[CLIENT_LOGIN]', int_data['client_login'])
                            line = line.replace('[ORDER_NAME]', int_data['order_name'])
                            line = line.replace('[START_DATE]', fix_date(int_data['start_date']))
                            line = line.replace('[DUE_DATE]', fix_date(int_data['due_date']))
                            line = line.replace('[TITLE_ROW]', '')
                            line = line.replace('[PROJ_ROW]', '')
                            filled = '%s%s' % (filled, line)
                        template.close()
                        filled_in_email = '/var/www/html/formatted_emails/int_order_edited_%s.html' % order_code
                        filler = open(filled_in_email, 'w')
                        filler.write(filled)
                        filler.close()
                        #Send the internal email
                        the_command = "php /opt/spt/custom/formatted_emailer/inserted_order_email.php '''%s''' '''%s''' '''%s''' '''%s''' '''%s''' '''%s'''" % (filled_in_email, int_data['to_email'], int_data['from_email'], int_data['from_name'], subject, int_data['ccs'].replace(';','#Xs*'))
                        os.system(the_command)
                        if ext_data['location'] == 'external' and allow_client_emails:
                            template = open(external_template_file, 'r')
                            filled = ''
                            for line in template:
                                line = line.replace('[ORDER_CODE]', ext_data['order_code'])
                                line = line.replace('[PO_NUMBER]', ext_data['po_number'])
                                line = line.replace('[CLIENT_EMAIL]', ext_data['client_email'])
                                line = line.replace('[EMAIL_CC_LIST]', ext_data['ccs'])
                                line = line.replace('[SCHEDULER_EMAIL]', ext_data['scheduler_email'])
                                line = line.replace('[SUBJECT]', subject_see)
                                line = line.replace('[MESSAGE]', message)
                                line = line.replace('[CLIENT]', ext_data['client_name'])
                                line = line.replace('[CLIENT_LOGIN]', ext_data['client_login'])
                                line = line.replace('[ORDER_NAME]', ext_data['order_name'])
                                line = line.replace('[START_DATE]', fix_date(ext_data['start_date']))
                                line = line.replace('[DUE_DATE]', fix_date(ext_data['due_date']))
                                filled = '%s%s' % (filled, line)
                            template.close()
                            filled_in_email = '/var/www/html/formatted_emails/ext_order_edited_%s.html' % order_code
                            filler = open(filled_in_email, 'w')
                            filler.write(filled)
                            filler.close()
                            #Send the external email
                            the_command = "php /opt/spt/custom/formatted_emailer/inserted_order_email.php '''%s''' '''%s''' '''%s''' '''%s''' '''%s''' '''%s'''" % (filled_in_email, ext_data['to_email'], ext_data['from_email'], ext_data['from_name'], subject, ext_data['ccs'].replace(';','#Xs*'))
                            os.system(the_command)
            else:
                print "THIS MAKES NO SENSE. SOB TIME IS GREATER THAN NOW TIME"
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
