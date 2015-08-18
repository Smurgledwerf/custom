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
        # CUSTOM_SCRIPT00074
        # Matthew Tyler Misenhimer
        # This is run when a new file is uploaded to an object or a note (notes handled differently)
        
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
            # This is to see the difference in seconds between two special date&time dicts. 
            # Result in first position in return array will be 1 if the first passed in variable is older, 0 if it is newer than the second passed in
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
            import sys
            from json import dumps as jsondumps
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
        parent_type_solid = sobject.get('search_type')
        parent_type = sobject.get('search_type').split('?')[0]
        find_str = parent_type.split('/')[1].upper().split('?')[0]
        file_name = sobject.get('file_name') #.replace(' ','_')
        #This only handles files that were attached to notes or orders
        
        
        
        
        
        
        
        if '_web.' not in file_name and '_icon.' not in file_name and 'icon' not in sobject.get('checkin_dir'):
            #see if the file was attached to a note, if not, see if it was connected to an order 
            note_expr = "@SOBJECT(sthpw/snapshot['search_id','%s']['search_type','sthpw/note']['@ORDER_BY','timestamp asc'])" % sobject.get('search_id')
            snapshots = server.eval(note_expr)
            if len(snapshots) == 0:
                order_expr = "@SOBJECT(sthpw/snapshot['search_id','%s']['search_type','twog/order?project=twog'])" % sobject.get('search_id')
                snapshots = server.eval(order_expr)
            if len(snapshots) > 0:
                #Get the most recent snapshot that the file could have been attached to
                snapshot = snapshots[len(snapshots) - 1]    
                is_latest = snapshot.get('is_latest')
                description = snapshot.get('description')
                process = snapshot.get('process')
                id = snapshot.get('id')
                search_id = snapshot.get('search_id')
                code = snapshot.get('code')
                snap_timestamp = snapshot.get('timestamp')
                sea_t = sobject.get('search_type').split('?')[0]
                upper_st = sea_t.split('/')[1].upper()
                srch_id = sobject.get('search_id')
                full_ending = make_right_code_ending(srch_id)
                parent_code = '%s%s' % (upper_st, full_ending)
                parent_sk = server.build_search_key(sea_t, parent_code)
                parent_type = parent_sk.split('?')[0]
                version = int(snapshot.get('version'))
                #There's a template for the internal emails, and one for those that go out to our clients
                internal_template_file = '/opt/spt/custom/formatted_emailer/internal_email_template.html'
                external_template_file = '/opt/spt/custom/formatted_emailer/external_email_template.html'
                if is_latest and find_str == 'ORDER':
                    #Handle the case in which it was attached to an order
                    order_code = parent_code
                    if version not in [-1,'-1']:
                        #The only process we care about sending alerts out for is the "PO"
                        if process == 'PO':
                            parent = server.eval("@SOBJECT(%s['code','%s'])" % (parent_type, parent_code))[0]
                            sched = parent.get('login')
                            sched_email = server.eval("@GET(sthpw/login['login','%s'].email)" % sched)
                            if sched_email:
                                sched_email = sched_email[0]
                            else:
                                sched_email = 'imakestringnothinghappn'
                            parent_timestamp = parent.get('timestamp')
                            snap_tdict = get_time_date_dict(snap_timestamp)
                            parent_tdict = get_time_date_dict(parent_timestamp)
                            rez = compare_dt_dicts(parent_tdict, snap_tdict)
                            #If the result is 1, the parent is older than the snapshot
                            #If the snapshot is older than the order, the result will be 0, which means there is a problem
                            if rez[1] == 1:
                                #If the difference in seconds between the object creation is greater than 15 seconds, there will probably be no problems with the following queries (Had to put it in, because it was creating errors occasionally)
                                if rez[0] > 15:
                                    #Get all the files associated with the file upload (there could be others attached to the same snapshot)
                                    #Then send an email, using the internal template
                                    from formatted_emailer import EmailDirections
                                    ed = EmailDirections(order_code=order_code)
                                    int_data = ed.get_internal_data()
                                    subject = '2G-PO-FILE-UPLOAD %s Order: "%s" PO#: %s' % (file_name, int_data['order_name'], int_data['po_number']) 
                                    if int_data['client_email'] == '' and int_data['location'] == 'external':
                                        subject = 'NOT SENT TO CLIENT!? %s' % subject
                                    subject_see = subject
                                    subject = subject.replace(' ','..')
                                    message = '%s has uploaded a new PO File.' % int_data['from_name'].replace('.',' ')
                                    message = '%s<br/>Uploaded PO File: %s' % (message, file_name)
                                    if parent_type == 'twog/order':
                                        sales_repper = parent.get('sales_rep')
                                        sales_rep_email = server.eval("@GET(sthpw/login['login','%s']['location','internal'].email)" % sales_repper)
                                        if sales_rep_email not in [None,'',[]]:
                                            sales_rep_email = sales_rep_email[0]
                                            if int_data['ccs'] not in [None,'']:
                                                int_data['ccs'] = '%s;%s' % (int_data['ccs'], sales_rep_email)
                                            else:
                                                int_data['ccs'] = '%s' % sales_rep_email
                                    int_data['ccs'] = int_data['ccs'].replace(';%s' % sched_email, '').replace('%s;' % sched_email, '')
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
                                    transaction_ticket = server.get_transaction_ticket()
                                    upload_dir = Environment.get_upload_dir(transaction_ticket)
                                    filled = '%s\nMATTACHMENT:%s/%s' % (filled, upload_dir, file_name)
                                    template.close()
                                    filled_in_email = '/var/www/html/formatted_emails/int_snap_inserted_%s.html' % code
                                    filler = open(filled_in_email, 'w')
                                    filler.write(filled)
                                    filler.close()
                                    the_command = "php /opt/spt/custom/formatted_emailer/trusty_emailer.php '''%s''' '''%s''' '''%s''' '''%s''' '''%s''' '''%s'''" % (filled_in_email, int_data['to_email'], int_data['from_email'], int_data['from_name'], subject, int_data['ccs'].replace(';','#Xs*'))
                                    os.system(the_command)
                                    #If the location of the user is external, and we allow this client to receive emails, then send them an email as well
                                    if int_data['location'] == 'external' and allow_client_emails:
                                        ext_data = ed.get_external_data()
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
                                        filled = '%s\nMATTACHMENT:%s/%s' % (filled, upload_dir, file_name)
                                        template.close()
                                        filled_in_email = '/var/www/html/formatted_emails/ext_snap_inserted_%s.html' % code
                                        filler = open(filled_in_email, 'w')
                                        filler.write(filled)
                                        filler.close()
                                        os.system("php /opt/spt/custom/formatted_emailer/trusty_emailer.php '''%s''' '''%s''' '''%s''' '''%s''' '''%s''' '''%s'''" % (filled_in_email, ext_data['to_email'], ext_data['from_email'], ext_data['from_name'], subject, ext_data['ccs'].replace(';','#Xs*')))
                            else:
                                print "THIS MAKES NO SENSE. THE SNAPSHOT WAS CREATED BEFORE THE ORDER?"
                elif find_str == 'NOTE':
                    #So it was attached to a note
                    #Need to make a code with the search id, as there's different ways the order and note deal with their snapshots
                    full_ending = make_note_code_ending(srch_id)
                    parent_code = 'NOTE%s' % (full_ending)
                    parent_sk = server.build_search_key('sthpw/note', parent_code)
                    #Get the note sobject
                    #note_obj = server.eval("@SOBJECT(sthpw/note['code','%s'])" % parent_code)[0]
                    note_obj = server.eval("@SOBJECT(sthpw/note['id','%s'])" % srch_id)[0]
                    note = note_obj.get('note')
                    #Need to wait until all files have been checked in to Tactic
                    if process == 'note_attachment':
                        timestamp = note_obj.get('timestamp').split('.')[0]
                        search_id = note_obj.get('search_id') 
                        login = note_obj.get('login')
                        process = note_obj.get('process')
                        note_id = note_obj.get('id')
                        addressed_to = note_obj.get('addressed_to')
                        override_compression = True
                        #if addressed_to not in [None,'']:
                        #    override_compression = True
                        search_type = note_obj.get('search_type').split('?')[0]
                        parent_tall_str = search_type.split('/')[1].upper()
                        groups = Environment.get_group_names()
                        note = note_obj.get('note')
                        note = note.replace('\t','&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
                        note = note.replace('\n','<br/>')
                        note = note.replace('  ', '&nbsp;&nbsp;')
                        note = fix_note_chars(note)
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
                        #If the note was attached to an order, title, proj or work_order, and compression didn't write the note, then send it. If compression intended to send it, then go ahead and send. 
                        if parent_tall_str in ['ORDER','TITLE','PROJ','WORK_ORDER']: # and (('compression' not in groups and 'compression supervisor' not in groups) or override_compression):
                            from formatted_emailer import EmailDirections
                            #create the note parent's code from search_id
                            right_ending = make_right_code_ending(search_id)
                            parent_code = '%s%s' % (parent_tall_str, right_ending)
                            parent = server.eval("@SOBJECT(%s['code','%s'])" % (search_type, parent_code))
                            if parent:
                                parent = parent[0]
                            ident_str = ''
                            going_to_client = False
                            #Get info from the related elements, going up the chain
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
                            #If the note was attached to an order or a title, go ahead and send it to the client (as long as we allow emailing to that client), otherwise it will remain internal 
                            if parent_tall_str == 'ORDER' and process == 'client':
                                order = parent 
                                going_to_client = True
                            elif parent_tall_str == 'TITLE' and process == 'client':
                                going_to_client = True
                            display_heirarchy = ''
                        
                            #Get the different message elements and mail_to lists for internal and external emails
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
                            subject = '2G-NOTE ATTACHMENT FOR %s (%s)' % (ident_str, file_name)
                            #If it's not going to the client because we don't have their email, at least tell the people internally that it didn't go out to the client
                            if ext_data['to_email'] == '' and ext_data['ext_ccs'] == '' and ext_data['location'] == 'external':
                                subject = 'NOT SENT TO CLIENT!? %s' % subject
                            subject_see = subject
                            subject = subject.replace(' ','..')
                            message = '<br/>%s has added a new note for %s:<br/><br/>Note:<br/>%s<br/>%s' % (ext_data['from_name'], ident_str, note, timestamp)
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
                                #If there were files attached (which there should be), show what they are in the email 
                                transaction_ticket = server.get_transaction_ticket()
                                upload_dir = Environment.get_upload_dir(transaction_ticket)
                                filled = '%s\nMATTACHMENT:%s/%s' % (filled, upload_dir, file_name)
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
                                line = line.replace('[ORDER_NAME]', int_data['order_name'])
                                line = line.replace('[START_DATE]', fix_date(int_data['start_date']))
                                line = line.replace('[DUE_DATE]', fix_date(int_data['due_date']))
                                line = line.replace('[TITLE_ROW]', title_row)
                                line = line.replace('[PROJ_ROW]', proj_row)
                                filled = '%s%s' % (filled, line)
                            #If there were files attached (which there should be), show what they are in the email 
                            transaction_ticket = server.get_transaction_ticket()
                            upload_dir = Environment.get_upload_dir(transaction_ticket)
                            filled = '%s\nMATTACHMENT:%s/%s' % (filled, upload_dir, file_name)
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
                                #Do it. Send the email
                                os.system(the_command)
        elif '_icon' in file_name:
            snapshot_code = sobject.get('snapshot_code')
            extension = 'jpg' #I don't know why I can't get the actual info on this file right now. Kinda tarded. We just have to assume that it will end up being a jpg
            fsplit = file_name.split('.')
            sexpr = "@SOBJECT(sthpw/snapshot['code','%s'])" % snapshot_code
            snapshot = server.eval(sexpr)[0]
            version = int(snapshot.get('version'))
            if version > 9:
                version = 'v0%s' % version
            elif version > 99:
                version = 'v%s' % version
            else:
                version = 'v00%s' % version
            parent_type = snapshot.get('search_type').split('?')[0]
            find_str = parent_type.split('/')[1].upper().split('?')[0]
            process = snapshot.get('process')
            if process == 'icon':
                id = snapshot.get('id')
                search_id = snapshot.get('search_id')
                sea_t = snapshot.get('search_type').split('?')[0]
                upper_st = sea_t.split('/')[1].upper()
                srch_id = snapshot.get('search_id')
                full_ending = make_right_code_ending(srch_id)
                parent_code = '%s%s' % (upper_st, full_ending)
                parent_sk = server.build_search_key(sea_t, parent_code)
                parent_type = parent_sk.split('?')[0]
                #This is to set the icon for orders
                if find_str == 'ORDER':
                    preview_path = server.get_path_from_snapshot(snapshot.get('code'), mode="web")
                    preview_path_i = preview_path.split('/')
                    fn2 = preview_path_i[len(preview_path_i) - 1]
                    fn3_s = fn2.split('.')
                    fn3 = '%s_icon_%s.%s' % (fn3_s[0], version, extension)
                    preview_path = preview_path.replace(fn2, fn3)
                    server.update(parent_sk, {'icon_path': preview_path})
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
