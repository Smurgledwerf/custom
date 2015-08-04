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
        # CUSTOM_SCRIPT00100
        #Easy way to get the name of something you only have a code for
        def get_name(code, stype):
            name = 'N/A'
            sob_name = server.eval("@GET(%s['code','%s'].name)" % (stype,code))
            if sob_name:
                name = sob_name[0]
            return name
        
        def kill_nulls(poss_str):
            ret_str = 'N/A'
            if poss_str not in [None,'']:
                ret_str = str(poss_str) 
            return ret_str
        
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
        
        from pyasm.common import Environment
        from pyasm.common import SPTDate
        #print "IN SEND MOVEMENT PENDING EMAIL"
        login = Environment.get_login()
        user_name = login.get_login()
        sobject = input.get('sobject')
        spe = sobject.get('send_pending_email')
        if spe in [True,'True','true','t','T','1',1]:    
            name = sobject.get('name')
            code = sobject.get('code')
            waybill = sobject.get('waybill')
            outside_movement_contact = sobject.get('outside_movement_contact')
            expected_date = sobject.get('expected_date')
            if expected_date in [None,'']:
                expected_date = 'N/A'
            else:
                expected_date_obj = SPTDate.convert_to_local(expected_date)
                expected_date = expected_date_obj.strftime("%Y-%m-%d  %H:%M:%S")
            shipper_name = get_name(sobject.get('shipper_code'), 'twog/shipper')
            sending_company_name = get_name(sobject.get('sending_company_code'), 'twog/company')
            receiving_company_name = get_name(sobject.get('receiving_company_code'), 'twog/company')
            description = sobject.get('description')
            #Need these replacements to convert to html formatting
            description = description.replace('\t','        ')
            description = description.replace('\n','<br/>')
            description = description.replace('  ', '  ')
            description = fix_note_chars(description)
            
            delim = '#Xs*'
            all_ccs = 'fernando.vazquez@2gdigital.com%s2GVault@2gdigital.com%sScheduling@2gdigital.com%smatt.misenhimer@2gdigital.com' % (delim, delim, delim)
            
            #This is the person that originally created the movement, want to add them to the email recipients
            creator_name = sobject.get('login')
            creator = server.eval("@SOBJECT(sthpw/login['login','%s']['location','internal'])" % creator_name)
            if creator:
                creator = creator[0]
                all_ccs = '%s%s%s' % (all_ccs, delim, creator.get('email'))
            
            #This is the person that just saved "send_pending_email" = True, want to add them to the email recipients
            requestor = server.eval("@SOBJECT(sthpw/login['login','%s']['location','internal'])" % user_name)
            requestor_full_name = 'N/A'
            if requestor:
                requestor = requestor[0]
                requestor_full_name = '%s %s' % (requestor.get('first_name'), requestor.get('last_name'))
                all_ccs = '%s%s%s' % (all_ccs, delim, requestor.get('email'))
            
            #Create the list of sources with their locations
            client_names = {}
            sources = server.eval("@SOBJECT(twog/asset_to_movement['movement_code','%s'].twog/source)" % code)
            table = '<table>'
            for source in sources:
                client_code = source.get('client_code')
                client_name = 'N/A'
                try:
                    client_name = client_names[client_code]
                except:
                    client_name = get_name(client_code, 'twog/client')
                    client_names[client_code] = client_name
                    pass
                title = kill_nulls(source.get('title'))
                episode = kill_nulls(source.get('episode'))
                season = kill_nulls(source.get('season'))
                version = kill_nulls(source.get('version'))
                barcode = kill_nulls(source.get('barcode'))
                source_type = kill_nulls(source.get('source_type'))
                in_house = kill_nulls(source.get('in_house'))
                generation = kill_nulls(source.get('generation'))
                location = 'N/A'
                last_location = server.eval("@SOBJECT(twog/location_tracker['source_barcode','%s']['@ORDER_BY','timestamp desc'])" % barcode)
                if last_location:
                    last_location = last_location[len(last_location) - 1]
                    location = last_location.get('location_name')
                table = '%s<tr><td nowrap="nowrap"><b>Barcode:</b> %s</td><td nowrap="nowrap"><b>Title:</b> %s <b>Episode:</b> %s <b>Season:</b> %s <b>Version:</b> %s</td><td><b>Type:</b> %s <b>Generation:</b> %s</td><td><b>Client:</b> %s</td><td><b>In House:</b> %s</td></tr><tr><td><b>Location:</b> %s</td></tr><tr><td>|</td></tr>' % (table, barcode, title, episode, season, version, source_type, generation, client_name, in_house, location) 
            table = '%s</table>' % table
                
                
            header_row = "<div id='pagesubTitle3'>Movement Pending: <strong>%s (%s)</strong></div>" % (name, code) 
            
            template_path = '/opt/spt/custom/formatted_emailer/pending_movement.html'
            filled_in_path = '/var/www/html/formatted_emails/pending_movement_%s.html' % code
            template = open(template_path, 'r')
            filled = ''
            for line in template:
                line = line.replace('[MOVEMENT_CODE]', code)
                line = line.replace('[MOVEMENT_NAME]', name)
                line = line.replace('[CREATOR_NAME]', creator_name)
                line = line.replace('[TITLE_ROW]', header_row)
                line = line.replace('[REQUESTOR_NAME]', user_name)
                line = line.replace('[OUTSIDE_MOVEMENT_CONTACT]', outside_movement_contact)
                line = line.replace('[EXPECTED_DATE]', expected_date)
                line = line.replace('[DESCRIPTION]', description)
                line = line.replace('[SHIPPER_NAME]', shipper_name)
                line = line.replace('[SENDING_COMPANY]', sending_company_name)
                line = line.replace('[RECEIVING_COMPANY]', receiving_company_name)
                line = line.replace('[SOURCES_TABLE]', table)
                filled = '%s%s' % (filled, line)
            template.close()
            filler = open(filled_in_path, 'w')
            filler.write(filled)
            filler.close()
            server.insert('twog/bundled_message', {'filled_in_path': filled_in_path, 'message': 'Pending Movement (%s)' % code, 'from_email': 'Scheduling@2gdigital.com', 'to_email': 'Vault@2gdigital.com', 'from_name': requestor_full_name, 'subject': 'Pending Movement: %s (%s) Issued by %s' % (name, code, requestor_full_name), 'all_ccs': all_ccs, 'object_code': code})
        #print "LEAVING SEND PENDING MOVEMENT EMAIL"
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
