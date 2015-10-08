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
        # CUSTOM_SCRIPT00063
        # Matthew Tyler Misenhimer
        # This was made to handle new snapshot insertions (uploads) and notify relevant people via email about the new upload
        
        # Do Not send external if location is internal
        def make_right_code_ending(sid):
            ending = str(sid)
            ending_len = len(ending)
            if ending_len < 5:
                zeros = 5 - ending_len
                for num in range (0, zeros):
                    ending = '0%s' % ending
            return ending
        
        def make_note_code_ending(sid):
            ending = str(sid)
            ending_len = len(ending)
            if ending_len < 8:
                zeros = 8 - ending_len
                for num in range (0, zeros):
                    ending = '0%s' % ending
            return ending
        
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
        
        import os
        from pyasm.common import Environment
        allow_client_emails = True
        sobject = input.get('sobject')
        update_data = input.get('update_data')
        parent_type_solid = update_data.get('search_type')
        parent_type = update_data.get('search_type').split('?')[0]
        find_str = parent_type.split('/')[1].upper().split('?')[0]
        is_latest = sobject.get('is_latest')
        process = sobject.get('process')
        id = sobject.get('id')
        search_id = sobject.get('search_id')
        code = sobject.get('code')
        version = sobject.get('version')
        snap_timestamp = sobject.get('timestamp')
        
        sea_t = update_data.get('search_type').split('?')[0]
        upper_st = sea_t.split('/')[1].upper()
        srch_id = update_data.get('search_id')
        full_ending = make_right_code_ending(srch_id)
        parent_code = '%s%s' % (upper_st, full_ending)
        parent_sk = server.build_search_key(sea_t, parent_code)
        
        parent_type = parent_sk.split('?')[0]
        internal_template_file = '/opt/spt/custom/formatted_emailer/internal_email_template.html'
        external_template_file = '/opt/spt/custom/formatted_emailer/external_email_template.html'
        if is_latest and find_str == 'ORDER':
            # If this is the newest file, and it was uploaded to an order...
            order_code = parent_code
            if version not in [-1,'-1']:
                if process == 'PO':
                    # ... notify people about the upload if it was a new PO file
                    parent = server.eval("@SOBJECT(%s['code','%s'])" % (parent_type, parent_code))[0]
                    parent_timestamp = parent.get('timestamp')
                    snap_tdict = get_time_date_dict(snap_timestamp)
                    parent_tdict = get_time_date_dict(parent_timestamp)
                    #If the snapshot was made after the order, then we can search for the files
                    rez = compare_dt_dicts(parent_tdict, snap_tdict)
                    if rez[1] == 1:
                        # If the order has been there for at least 15 milliseconds before the snapshot, then you'll be able to find the file objects
                        if rez[0] > 15:
                            filez = server.eval("@SOBJECT(sthpw/file['search_id','%s']['search_type','%s'])" % (search_id, parent_type_solid))
                            file_name = ''
                            if filez:
                                for fi in filez:
                                    if fi.get('type') == 'main': 
                                        sp = fi.get('source_path').split('/')
                                        lsp = sp[len(sp) - 1].split('\\')
                                        file_name = lsp[len(lsp) - 1]
                            #Then send an email
                            from formatted_emailer import EmailDirections
                            ed = EmailDirections(order_code=order_code)
                            int_data = ed.get_internal_data()
                            subject = '2G-FILE-UPLOAD %s Order: "%s" PO#: %s' % (file_name, int_data['order_name'], int_data['po_number']) 
                            if int_data['client_email'] == '' and int_data['location'] == 'external':
                                subject = 'NOT SENT TO CLIENT!? %s' % subject
                            subject_see = subject
                            subject = subject.replace(' ','..') # Spaces are no good when sending to php as a parameter
                            message = '%s has uploaded a new PO File.' % int_data['from_name'].replace('.',' ')
                            message = '%s<br/>Uploaded PO File: %s' % (message, file_name) 
                            message = fix_note_chars(message)
                            #Fill the internal template file to create a file you can email
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
                                line = line.replace('[ORDER_NAME]', int_data.get('order_hyperlink', int_data['order_name']))
                                line = line.replace('[START_DATE]', fix_date(int_data['start_date']))
                                line = line.replace('[DUE_DATE]', fix_date(int_data['due_date']))
                                line = line.replace('[TITLE_ROW]', '')
                                line = line.replace('[PROJ_ROW]', '')
                                filled = '%s%s' % (filled, line)
                            template.close()
                            filled_in_email = '/var/www/html/formatted_emails/int_snap_inserted_%s.html' % code
                            filler = open(filled_in_email, 'w')
                            filler.write(filled)
                            filler.close()
                            #Send the internal email
                            the_command = "php /opt/spt/custom/formatted_emailer/inserted_order_email.php '''%s''' '''%s''' '''%s''' '''%s''' '''%s''' '''%s'''" % (filled_in_email, int_data['to_email'], int_data['from_email'], int_data['from_name'], subject, int_data['ccs'].replace(';','#Xs*'))
                            os.system(the_command)
                            if int_data['location'] == 'external' and allow_client_emails:
                                ext_data = ed.get_external_data()
                                #Fill the external template file to create a file you can email
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
                                filled_in_email = '/var/www/html/formatted_emails/ext_snap_inserted_%s.html' % code
                                filler = open(filled_in_email, 'w')
                                filler.write(filled)
                                filler.close()
                                #Send the external email
                                os.system("php /opt/spt/custom/formatted_emailer/inserted_order_email.php '''%s''' '''%s''' '''%s''' '''%s''' '''%s''' '''%s'''" % (filled_in_email, ext_data['to_email'], ext_data['from_email'], ext_data['from_name'], subject, ext_data['ccs'].replace(';','#Xs*')))
                    else:
                        print "THIS MAKES NO SENSE. THE SNAPSHOT WAS CREATED BEFORE THE ORDER?"
        elif find_str == 'NOTE':
            #If the upload was made to a note
            #Get the correct 
            #full_ending = make_note_code_ending(srch_id) #This was for Tactic v3.9
            #parent_code = 'NOTE%s' % (full_ending) #This was for Tactic v3.9
            #parent_sk = server.build_search_key('sthpw/note', parent_code) #This was for Tactic v3.9
            #note_obj = server.eval("@SOBJECT(sthpw/note['code','%s'])" % parent_code)[0] #This was for Tactic v3.9
            note_obj = server.eval("@SOBJECT(sthpw/note['id','%s'])" % srch_id)[0]
            parent_sk = note_obj.get('__search_key__')
            parent_code = note_obj.get('code') 
            note = note_obj.get('note')
            #Need to wait until all files have been checked in to Tactic
            if 'HASATTACHEDFILES:' in note:
                prenote = note.split('HASATTACHEDFILES')[0]
                count = int(note.split('HASATTACHEDFILES:')[1].split('MTMCOUNT')[0])
                new_count = count - 1
                if count == 1 or count == 0:
                    #Get all the files that have been checked in so far and send them along with the note in an email
                    #MAKE SURE TO REMOVE THE HASATTACHEDFILES section from the note before sending it, also update it in the db
                    server.update(parent_sk, {'note': prenote}, triggers=False)
                    search_id = note_obj.get('search_id') 
                    login = note_obj.get('login')
                    process = note_obj.get('process')
                    note = prenote
                    #Have to make the note work in html format
                    note = note.replace('\t','&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
                    note = note.replace('\n','<br/>')
                    note = note.replace('  ', '&nbsp;&nbsp;')
                    note = fix_note_chars(note)
                    note_id = note_obj.get('id')
                    timestamp = note_obj.get('timestamp').split('.')[0]
                    #time.sleep(60)
                    addressed_to = note_obj.get('addressed_to')
                    search_type = note_obj.get('search_type').split('?')[0]
                    parent_tall_str = search_type.split('/')[1].upper()
                    groups = Environment.get_group_names()
                    order = None
                    title = None
                    proj = None
                    work_order = None
                    order_code = ''
                    display_ccs = ''
                    subject_see = ''
                    message = ''
                    title_row = ''
                    proj_row = ''
                    if parent_tall_str in ['ORDER','TITLE','PROJ','WORK_ORDER']: # and 'compression' not in groups and 'compression supervisor' not in groups:
                        from formatted_emailer import EmailDirections
                        right_ending = make_right_code_ending(search_id)
                        parent_code = '%s%s' % (parent_tall_str, right_ending)
                        parent = server.eval("@SOBJECT(%s['code','%s'])" % (search_type, parent_code))
                        if parent:
                            parent = parent[0]
                        ident_str = ''
                        going_to_client = False
                        if parent_tall_str == 'WORK_ORDER':
                            proj = server.eval("@SOBJECT(twog/work_order['code','%s'].twog/proj)" % parent_code)[0]
                            title = server.eval("@SOBJECT(twog/work_order['code','%s'].twog/proj.twog/title)" % parent_code)[0] 
                            order = server.eval("@SOBJECT(twog/order['code','%s'])" % title.get('order_code'))[0]
                        elif parent_tall_str == 'PROJ':
                            proj = parent
                            title = server.eval("@SOBJECT(twog/proj['code','%s'].twog/title)" % parent_code)[0] 
                            order = server.eval("@SOBJECT(twog/order['code','%s'])" % title.get('order_code'))[0]
                        elif parent_tall_str == 'TITLE':
                            title = parent
                            order = server.eval("@SOBJECT(twog/order['code','%s'])" % title.get('order_code'))[0]
                        elif parent_tall_str == 'ORDER':
                            order = server.eval("@SOBJECT(twog/order['code','%s'])" % parent_code)[0]
                        if parent_tall_str == 'ORDER' and process == 'client':
                            order = parent 
                            going_to_client = True
                        elif parent_tall_str == 'TITLE' and process == 'client':
                            going_to_client = True
                        display_heirarchy = ''
                    
                        ed = EmailDirections(order_code=order.get('code'))
                        int_data = ed.get_internal_data()
                        ext_data = ed.get_external_data()
                    
                        if title:
                            title_display = title.get('title')
                            if title.get('episode') not in [None,'']:
                                title_display = '%s: %s' % (title_display, title.get('episode'))
                            display_heirarchy = '"%s" in %s' % (title_display, display_heirarchy)
                        ident_str = ''
                        if parent_tall_str in ['ORDER','TITLE']:
                            ident_str = '%s PO#: %s' % (display_heirarchy, ext_data['po_number'])
                        else:
                            ident_str = '%s (%s)' % (parent_code, ext_data['po_number'])
                        subject = '2G-NOTE FOR %s' % (ident_str)
                        if ext_data['to_email'] == '' and ext_data['ext_ccs'] == '' and ext_data['location'] == 'external':
                            subject = 'NOT SENT TO CLIENT!? %s' % subject
                        subject_see = subject
                        subject = subject.replace(' ','..')
                        message = '<br/>%s has added a new note for %s:<br/><br/>Note:<br/>%s<br/>%s' % (ext_data['from_name'], ident_str, note, timestamp)
                        message = fix_note_chars(message)
                        if going_to_client and allow_client_emails:
                            ext_template = open(external_template_file, 'r')
                            filled = ''
                            for line in ext_template:
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
                            snaps_expr = "@SOBJECT(sthpw/snapshot['search_type','sthpw/note']['search_id','%s'])" % note_id
                            snaps = server.eval(snaps_expr)
                            for snap in snaps:
                                if snap.get('is_current') in [True,'T','true','t']:
                                    #files_expr = "@SOBJECT(sthpw/file['snapshot_code','%s'])" % snap.get('code')
                                    files_expr = "@SOBJECT(sthpw/file['search_type','sthpw/note']['search_id','%s'])" % note_obj.get('id')
                                    files = server.eval(files_expr)
                                    for file in files:
                                        if file.get('type') == 'main' and file.get('snapshot_code') == snap.get('code'):
                                            file_path = '%s/%s' % (file.get('checkin_dir'), file.get('file_name'))
                                            filled = '%s\nMATTACHMENT:%s' % (filled, file_path) 
                            ext_template.close()
                            filled_in_email = '/var/www/html/formatted_emails/ext_note_inserted_%s.html' % note_id
                            filler = open(filled_in_email, 'w')
                            filler.write(filled)
                            filler.close()
                            if addressed_to not in [None,'']:
                                adt = addressed_to.split(',')
                                for adta in adt:
                                    if '@2gdigital' not in adta and adta not in ext_data['ext_ccs']:
                                        if ext_data['ext_ccs'] == '':
                                            ext_data['ext_ccs'] = adta
                                        else:
                                            ext_data['ext_ccs'] = '%s;%s' % (ext_data['ext_ccs'], adta)
                            the_command = "php /opt/spt/custom/formatted_emailer/trusty_emailer.php '''%s''' '''%s''' '''%s''' '''%s''' '''%s''' '''%s'''" % (filled_in_email, ext_data['to_email'], ext_data['from_email'], ext_data['from_name'], subject, ext_data['ext_ccs'].replace(';','#Xs*'))
                            if ext_data['to_email'] not in [None,''] and ext_data['ext_ccs'] not in [None,'',';']:
                                os.system(the_command)
                        #Now do internal email
                        if title:
                            full_title = title.get('title')
                            if title.get('episode') not in [None,'']:
                                full_title = '%s: %s' % (full_title, title.get('episode'))
                            title_row = "<div id='pagesubTitle3'>Title: <strong>%s</strong> | Title Code: <strong>%s</strong></div>" % (full_title, title.get('code')) 
                        if proj:
                            proj_row = "<div id='pagesubTitle3'>Project: <strong>%s</strong> | Project Code: <strong>%s</strong></div>" % (proj.get('process'), proj.get('code'))
                        int_template = open(internal_template_file, 'r')
                        filled = ''
                        for line in int_template:
                            line = line.replace('[ORDER_CODE]', int_data['order_code'])
                            line = line.replace('[PO_NUMBER]', int_data['po_number'])
                            line = line.replace('[CLIENT_EMAIL]', int_data['client_email'])
                            line = line.replace('[EMAIL_CC_LIST]', int_data['int_ccs'])
                            line = line.replace('[SCHEDULER_EMAIL]', int_data['scheduler_email'])
                            line = line.replace('[SUBJECT]', subject_see)
                            line = line.replace('[MESSAGE]', message)
                            line = line.replace('[CLIENT]', int_data['client_name'])
                            line = line.replace('[CLIENT_LOGIN]', int_data['client_login'])
                            line = line.replace('[ORDER_NAME]', int_data.get('order_hyperlink', int_data['order_name']))
                            line = line.replace('[START_DATE]', fix_date(int_data['start_date']))
                            line = line.replace('[DUE_DATE]', fix_date(int_data['due_date']))
                            line = line.replace('[TITLE_ROW]', title_row)
                            line = line.replace('[PROJ_ROW]', proj_row)
                            filled = '%s%s' % (filled, line)
                        snaps_expr = "@SOBJECT(sthpw/snapshot['search_type','sthpw/note']['search_id','%s'])" % note_id
                        snaps = server.eval(snaps_expr)
                        for snap in snaps:
                            if snap.get('is_current') in [True,'T','true','t']:
                                #files_expr = "@SOBJECT(sthpw/file['snapshot_code','%s'])" % snap.get('code')
                                files_expr = "@SOBJECT(sthpw/file['search_type','sthpw/note']['search_id','%s'])" % note_obj.get('id')
                                files = server.eval(files_expr)
                                for file in files:
                                    if file.get('type') == 'main' and file.get('snapshot_code') == snap.get('code'):
                                        file_path = '%s/%s' % (file.get('checkin_dir'), file.get('file_name'))
                                        filled = '%s\nMATTACHMENT:%s' % (filled, file_path) 
                        int_template.close()
                        filled_in_email = '/var/www/html/formatted_emails/int_note_inserted_%s.html' % note_id
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
                        login_email = server.eval("@GET(sthpw/login['login','%s'].email)" % login)
                        if login_email:
                            int_data['from_email'] = login_email[0] 
                        the_command = "php /opt/spt/custom/formatted_emailer/trusty_emailer.php '''%s''' '''%s''' '''%s''' '''%s''' '''%s''' '''%s'''" % (filled_in_email, int_data['to_email'], int_data['from_email'], int_data['from_name'], subject, int_data['int_ccs'].replace(';','#Xs*'))
                        if int_data['to_email'] not in [None,''] and int_data['int_ccs'] not in [None,'',';']:
                            os.system(the_command)
                else:
                    #Keep going until all uploads have been accounted for
                    new_note = '%s\nHASATTACHEDFILES:%sMTMCOUNT' % (prenote, new_count) 
                    server.update(parent_sk, {'note': new_note})
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
