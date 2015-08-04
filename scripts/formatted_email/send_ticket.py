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
        # CUSTOM_SCRIPT00089
        #Matthew Tyler Misenhimer
        #This sends tickets created in Tactic out as emails
        
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
        delim = '#Xs*'
        login = Environment.get_login()
        user_name = login.get_login()
        sobject = input.get('sobject')
        wo_code = sobject.get('work_order_code')
        #This is who it will be going to, at a minimum
        all_ccs = 'fernando.vazquez@2gdigital.com%smatt.misenhimer@2gdigital.com' % (delim)
        # Get the info related to this ticket (if the user provided this info)
        wo = server.eval("@SOBJECT(twog/work_order['code','%s'])" % wo_code)
        if len(wo) > 0:
            wo = wo[0]
            order_code = wo.get('order_code')
            order = server.eval("@SOBJECT(twog/order['code','%s'])" % order_code)[0]
            scheduler_name = order.get('login')
            scheduler = server.eval("@SOBJECT(sthpw/login['login','%s']['location','internal'])" % scheduler_name)
            if scheduler:
                scheduler = scheduler[0]
                all_ccs = '%s%s%s' % (all_ccs, delim, scheduler.get('email'))
            
        #Need to reformat the description and troubleshooting_attempted so they will look right in the html email
        description = sobject.get('description')
        description = description.replace('\t','        ')
        description = description.replace('\n','<br/>')
        description = description.replace('  ', '  ')
        description = fix_note_chars(description)
        
        troubleshooting_attempted = sobject.get('troubleshooting_attempted')
        troubleshooting_attempted = troubleshooting_attempted.replace('\t','        ')
        troubleshooting_attempted = troubleshooting_attempted.replace('\n','<br/>')
        troubleshooting_attempted = troubleshooting_attempted.replace('  ', '  ')
        troubleshooting_attempted = fix_note_chars(troubleshooting_attempted)
        
        template_path = '/opt/spt/custom/formatted_emailer/ticket_msg.html'
        filled_in_path = '/var/www/html/formatted_emails/ticket_msg_%s.html' % sobject.get('code')
        #Fill in the ticket template email
        template = open(template_path, 'r')
        filled = ''
        for line in template:
            for k in sobject.keys():
                if k not in ['description','troubleshooting_attempted','html','id','s_status','name','code']:
                    line = line.replace('[%s]' % k.upper(), sobject[k])
            line = line.replace('[DESCRIPTION]', description)
            line = line.replace('[TROUBLESHOOTING_ATTEMPTED]', troubleshooting_attempted)
            filled = '%s%s' % (filled, line)
        
        template.close()
        filler = open(filled_in_path, 'w')
        filler.write(filled)
        filler.close()
        #Create a bundled message so it will go out as an email
        server.insert('twog/bundled_message', {'filled_in_path': filled_in_path, 'message': 'New Ticket', 'from_email': 'TechAlert@2gdigital.com', 'to_email': 'matt.misenhimer@2gdigital.com', 'from_name': '%s New Ticket' % user_name, 'subject': 'New Ticket from %s' % user_name, 'all_ccs': all_ccs, 'object_code': sobject.get('code')})
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
