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
        # CUSTOM_SCRIPT00103
        # Matthew Tyler Misenhimer
        # Sends an email when a External Rejection is inserted or updated
        
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
        
        import os, time
        from pyasm.common import Environment
        internal_template_file = '/opt/spt/custom/formatted_emailer/internal_general_fillin_template.html'
        trigger_sobject = input.get('trigger_sobject')
        event = trigger_sobject.get('event')
        is_insert = False
        if 'insert' in event:
            is_insert = True
        if not is_insert:
            er_dict = input.get('sobject')
            login = er_dict.get('login')
            order_code = er_dict.get('order_code')
            title_code = er_dict.get('title_code')
        
            reported_issue = er_dict.get('reported_issue')
            if reported_issue not in [None,'']:
                reported_issue = reported_issue.replace('\n','<br/>').replace(' ','&nbsp;')
            reported_issue = fix_note_chars(reported_issue)
            
            rcnq = "@SOBJECT(sthpw/note['search_id','%s']['process','Root Cause']['search_type','twog/external_rejection?project=twog'])" % (er_dict.get('id'))
            root_cause_notes = server.eval(rcnq)
            root_cause = ''
            for rc in root_cause_notes:
                root_cause = '%s\n%s -- %s\n<b>Note: %s</b>\n' % (root_cause, rc.get('login'), rc.get('timestamp').split('.')[0], rc.get('note'))
            if root_cause not in [None,'']:
                root_cause = root_cause.replace('\n','<br/>').replace(' ','&nbsp;')
            root_cause = fix_note_chars(root_cause)
        
            corrective_action_notes = server.eval("@SOBJECT(sthpw/note['search_id','%s']['process','Corrective Action']['search_type','twog/external_rejection?project=twog'])" % (er_dict.get('id')))
            corrective_action = ''
            for ca in corrective_action_notes:
                corrective_action = '%s\n%s -- %s\n<b>Note:%s</b>\n' % (corrective_action, ca.get('login'), ca.get('timestamp').split('.')[0], ca.get('note'))
            if corrective_action not in [None,'']:
                corrective_action = corrective_action.replace('\n','<br/>').replace(' ','&nbsp;')
            corrective_action = fix_note_chars(corrective_action)

            title = er_dict.get('title')
            episode = er_dict.get('episode')
            po_number = er_dict.get('po_number')
            assigned = er_dict.get('assigned')
            status = er_dict.get('status')
            root_cause_type = er_dict.get('root_cause_type')
            corrective_action_assigned = er_dict.get('corrective_action_assigned')
            email_list = er_dict.get('email_list')
            addressed_to = email_list
            sources = er_dict.get('sources')
            replacement_order_code = er_dict.get('replacement_order_code')
            replacement_title_code = er_dict.get('replacement_title_code')
            
            reasons = ['video_cropping_reason','video_digihits_reason','video_dropped_frames_reason','video_dropout_reason','video_duplicate_frames_reason','video_interlacing_progressive_reason','video_motion_lag_reason','video_missing_elements_reason','video_corrupt_file_reason','video_bad_aspect_ratio_reason','video_bad_resolution_reason','video_bad_pixel_aspect_ratio_reason','video_bad_specifications_reason','video_bad_head_tail_reason','video_other_reason','audio_bad_mapping_reason','audio_missing_audio_channel_reason','audio_crackle_reason','audio_distortion_reason','audio_dropouts_reason','audio_sync_reason','audio_missing_elements_reason','audio_corrupt_missing_file_reason','audio_bad_specifications_reason','audio_other_reason','metadata_missing_info_reason','metadata_bad_info_reason','metadata_bad_formatting_reason','metadata_other_reason','subtitle_interlacing_reason','subtitle_bad_subtitles_reason','subtitle_sync_issue_reason','subtitle_overlapping_reason','subtitle_other_reason','cc_sync_issue_reason','cc_bad_cc_reason','cc_overlapping_reason','cc_other_reason']
            
            order_obj = server.eval("@SOBJECT(twog/order['code','%s'])" % order_code)
            order_name = ''
            client_name = ''
            scheduler = ''
            if order_obj:
                order_obj = order_obj[0]
                order_name = order_obj.get('name')
                client_name = order_obj.get('client_name')
                scheduler = order_obj.get('login')
            title_obj = server.eval("@SOBJECT(twog/title['code','%s'])" % title_code)
            title_due_date = ''
            title_expected_delivery = ''
            title_full_name = title
            if episode not in [None,'']:
                title_full_name = '%s: %s' % (title, episode)
            if title_obj:
                title_obj = title_obj[0]
                title_due_date = title_obj.get('due_date')
                title_expected_delivery = title_obj.get('expected_delivery_date')
                if client_name in [None,'']:
                    client_name = title_obj.get('client_name')
                if scheduler in [None,'']:
                    scheduler = order_obj.get('login')
                
            update_data = None
            main_message = ''
            head_message = ''
            head_detail = ''
            is_an_update = False
            if 'update_data' in input.keys():
                update_data = input.get('update_data')
                prev_data = input.get('prev_data')
                if prev_data not in [None,{},'']:
                    ukeys = update_data.keys()
                    if len(ukeys) > 0:
                        is_an_update = True
                        head_message = 'Update for External Rejection on %s (%s) [%s PO#: %s]:' % (title_full_name, title_code, order_code, po_number)
                        if 'status' in ukeys and update_data['status'] == 'Closed':
                            head_message += '<br/><br/>THIS EXTERNAL REJECTION IS NOW CLOSED'
                        else:
                            return
                    main_message = '<table style="font-size: 14px;"><tr><td colspan="2"><br/><br/><hr></td><td> </td></tr>'
                    main_message += '<tr><td valign="top"><b><u>Reported Issue:</u></b></td><td valign="top">{0}</td></tr>'.format(reported_issue)
                    main_message += '<tr><td valign="top"><b><u>Root Cause:</u></b></td><td valign="top">{0}</td></tr>'.format(root_cause)
                    main_message += '<tr><td valign="top"><b><u>Corrective Action:</u></b></td><td valign="top">{0}</td></tr>'.format(corrective_action)
                    main_message += '</table>'

            if is_an_update:
                subject_int = 'NEW - URGENT External Rejection Updates for %s (%s) - Status: %s Scheduler: %s PO#: %s' % (title_full_name, title_code, status, scheduler, po_number) 
            else:
                return
            
            head_detail = '<tr><td align="left" style="color: #0C6; font-size: 16px;">Replacement Order Code: <strong>%s</strong></td></tr><tr><td align="left" style="color: #0C6; font-size: 16px;">Replacement Title Code: <strong>%s</strong></td></tr>' % (replacement_order_code, replacement_title_code)
            
            from formatted_emailer import EmailDirections
            
            ed = EmailDirections(order_code=order_code)
            int_data = ed.get_internal_data()
            
            int_template = open(internal_template_file, 'r')
            filled = ''
            for line in int_template:
                line = line.replace('[ORDER_CODE]', order_code)
                line = line.replace('[ORDER_NAME]', order_name)
                line = line.replace('[PO_NUMBER]', po_number)
                line = line.replace('[MAIN_MESSAGE]', main_message)
                line = line.replace('[TOP_MESSAGE]', head_message)
                line = line.replace('[EXTRA_HEAD_DETAIL]', head_detail)
                line = line.replace('[CLIENT_NAME]', client_name)
                line = line.replace('[TITLE_CODE]', title_code)
                line = line.replace('[TITLE_FULL_NAME]', title_full_name)
                line = line.replace('[TITLE_DUE_DATE]', title_due_date)
                line = line.replace('[TITLE_EXPECTED_DELIVERY]', title_expected_delivery)
                filled = '%s%s' % (filled, line)
            int_template.close()
            filled_in_email = '/var/www/html/formatted_emails/int_note_inserted_%s.html' % er_dict.get('code')
            filler = open(filled_in_email, 'w')
            filler.write(filled)
            filler.close()
            if addressed_to not in [None,'']:
                adt = addressed_to.split(',')
                for adta in adt:
                    if '@2gdigital' in adta and adta not in int_data['int_ccs']:
                        if int_data['int_ccs'] == '':
                            int_data['int_ccs'] = adta
                        else:
                            int_data['int_ccs'] = '%s;%s' % (int_data['int_ccs'], adta)
            if int_data['int_ccs'] in [None,'']:
                int_data['int_ccs'] = 'jaime.torres@2gdigital.com;Justin.Kelley@2gdigital.com'
            else:
                int_data['int_ccs'] = '%s;jaime.torres@2gdigital.com;Justin.Kelley@2gdigital.com' % int_data['int_ccs']
            int_data['int_ccs'] = '%s;rejections@2gdigital.com' % (int_data['int_ccs']) 
            login_email = server.eval("@GET(sthpw/login['login','%s'].email)" % login)
            if login_email:
                int_data['from_email'] = login_email[0] 
            #NEW WAY TO SET THE FROM FOR THE EMAIL
            login_obj = Environment.get_login()
            sender_email = login_obj.get_value('email')
            sender_name = '%s %s' % (login_obj.get_value('first_name'), login_obj.get_value('last_name'))
            subject_int = subject_int.replace(' ','..')
            #the_command = "php /opt/spt/custom/formatted_emailer/trusty_emailer.php '''%s''' '''%s''' '''%s''' '''%s''' '''%s''' '''%s'''" % (filled_in_email, int_data['to_email'], int_data['from_email'], int_data['from_name'], subject_int, int_data['int_ccs'].replace(';','#Xs*'))
            the_command = "php /opt/spt/custom/formatted_emailer/trusty_emailer.php '''%s''' '''%s''' '''%s''' '''%s''' '''%s''' '''%s'''" % (filled_in_email, int_data['to_email'], sender_email, sender_name, subject_int, int_data['int_ccs'].replace(';','#Xs*'))
            if int_data['to_email'] not in [None,''] and int_data['int_ccs'] not in [None,'',';']:
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
