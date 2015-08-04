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
        # CUSTOM_SCRIPT00060
        # Matthew Tyler Misenhimer
        # This was made to report by email that a new order has been inserted
        # Do not send external if location is internal
        
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
        
        import os
        from pyasm.common import Environment
        from pyasm.common import SPTDate
        from formatted_emailer import EmailDirections
        allow_client_emails = True
        internal_template_file = '/opt/spt/custom/formatted_emailer/internal_email_template.html'
        external_template_file = '/opt/spt/custom/formatted_emailer/external_email_template.html'
        #print "In Order Inserted"
        order = input.get('sobject')
        order_code = order.get('code')
        client = order.get('client_code')
        if client not in [None,'']:
            #Get the valid recipients for this work, both internal and external
            ed = EmailDirections(order_code=order_code)
            int_data = ed.get_internal_data()
            subject = '2G-ORDER-CREATED-"%s" PO#: %s' % (int_data['order_name'], int_data['po_number'])
            subject_see = subject
            subject = subject.replace(' ','..')
            initial_po_upload_list = order.get('initial_po_upload_list')
            message = '%s has uploaded a new PO.' % int_data['from_name'].replace('.',' ')
            #The initial po upload list was created to handle uploads by clients, as the files will not exist for querying until after this trigger has been run.
            #These are the files the client uploaded to the order, inserted into the initial_po_upload_list after being selected by the client
            if initial_po_upload_list not in [None,'']:
                message = '%s<br/>Uploaded PO File: %s' % (message, initial_po_upload_list) 
            message = fix_note_chars(message) 
            #Open the internal template file and create a new file to send as email
            template = open(internal_template_file, 'r')
            filled = ''
            for line in template:
                line = line.replace('[ORDER_CODE]', int_data['order_code'])
                line = line.replace('[PO_NUMBER]', int_data['po_number'])
                line = line.replace('[CLIENT_EMAIL]', int_data['client_email'])
                line = line.replace('[EMAIL_CC_LIST]', int_data['int_ccs'])
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
            filled_in_email = '/var/www/html/formatted_emails/int_order_inserted_%s.html' % order_code
            filler = open(filled_in_email, 'w')
            filler.write(filled)
            filler.close()
            #Send the internal Email
            the_command = "php /opt/spt/custom/formatted_emailer/inserted_order_email.php '''%s''' '''%s''' '''%s''' '''%s''' '''%s''' '''%s'''" % (filled_in_email, int_data['to_email'], int_data['from_email'], int_data['from_name'], subject, int_data['ccs'].replace(';','#Xs*'))
            os.system(the_command)
            ext_data = ed.get_external_data()
            if int_data['location'] == 'external' and allow_client_emails:
                ext_data = ed.get_external_data()
                #Open the external template file and create a new file to send as email
                template = open(external_template_file, 'r')
                filled = ''
                for line in template:
                    line = line.replace('[ORDER_CODE]', ext_data['order_code'])
                    line = line.replace('[PO_NUMBER]', ext_data['po_number'])
                    line = line.replace('[CLIENT_EMAIL]', ext_data['client_email'])
                    line = line.replace('[EMAIL_CC_LIST]', ext_data['ext_ccs'])
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
                filled_in_email = '/var/www/html/formatted_emails/ext_order_inserted_%s.html' % order_code
                filler = open(filled_in_email, 'w')
                filler.write(filled)
                filler.close()
                #Send the External Email
                the_command = "php /opt/spt/custom/formatted_emailer/inserted_order_email.php '''%s''' '''%s''' '''%s''' '''%s''' '''%s''' '''%s'''" % (filled_in_email, ext_data['to_email'], ext_data['from_email'], ext_data['from_name'], subject, ext_data['ccs'].replace(';','#Xs*'))
                os.system(the_command)
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
