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
        # CUSTOM_SCRIPT00078
        from pyasm.common import Environment
        from pyasm.biz import Note
        from pyasm.search import Search
        import common_tools.utils as ctu
        login = Environment.get_login()
        user_name = login.get_login()
        delim = '#Xs*'
        all_ccs = 'fernando.vazquez@2gdigital.com%sScheduling@2gdigital.com' % delim
        #This is for production_error operator_description update
        sobject = input.get('sobject')
        operator_description = sobject.get('operator_description')
        title_code = sobject.get('title_code')
        wo_code = sobject.get('work_order_code')
        title_id_pre = title_code.split('TITLE')[1]
        found_non_zero = False
        title_id = ''
        note = ''
        for ch in title_id_pre:
            if ch != '0':
                found_non_zero = True
            if ch == '0' and found_non_zero or (ch != '0'):
                title_id = '%s%s' % (title_id, ch)
        wo_code = sobject.get('work_order_code')
        expr = "@SOBJECT(sthpw/note['search_id','%s']['search_type','~','twog/title']['process','QC Rejected']['@ORDER_BY','timestamp desc'])" % (title_id)
        last_note = server.eval(expr)
        if last_note:
            last_note = last_note[0]
            # Now just need to update it with the operator description, wo code and title
            note = last_note.get('note')
            note = '%s\n%s' % (note, operator_description)
            server.update(last_note.get('__search_key__'), {'note': note}, triggers=False)
            wo_obj2 = Search.get_by_search_key(server.build_search_key('twog/work_order',wo_code))   #This is the type of object required for Note creation
            note2 = Note.create(wo_obj2, note, context='QC Rejected', process='QC Rejected')
        
        
        wo = server.eval("@SOBJECT(twog/work_order['code','%s'])" % wo_code)[0]
        proj = server.eval("@SOBJECT(twog/proj['code','%s'])" % wo.get('proj_code'))[0]
        title = server.eval("@SOBJECT(twog/title['code','%s'])" % proj.get('title_code'))[0]
        order = server.eval("@SOBJECT(twog/order['code','%s'])" % title.get('order_code'))[0]
        scheduler_name = order.get('login')
        scheduler = server.eval("@SOBJECT(sthpw/login['login','%s']['location','internal'])" % scheduler_name)
        if scheduler:
            scheduler = scheduler[0]
            all_ccs = '%s%s%s' % (all_ccs, delim, scheduler.get('email'))
            
        group = ''
        process = ''
        client_name = ''
        po_number = order.get('po_number')
        order_name = order.get('name')
        title_name = title.get('title')
        episode = title.get('episode')
        if wo:
            group = wo.get('work_group')
            process = wo.get('process')
            client_name = wo.get('client_name')
        error_type = sobject.get('error_type')
        rejection_cause = sobject.get('rejection_cause')
        time_spent = sobject.get('time_spent')
        client_description = sobject.get('client_description')
        client_description = client_description.replace('\t','        ')
        client_description = client_description.replace('\n','<br/>')
        client_description = client_description.replace('  ', '  ')
        operator_description = operator_description.replace('\t','        ')
        operator_description = operator_description.replace('\n','<br/>')
        operator_description = operator_description.replace('  ', '  ')
        action_taken = sobject.get('action_taken')

        order_builder_url = ctu.get_order_builder_url(order.get('code'), server)
        href = '<a href="{0}">{1}</a>'
        order_hyperlink = href.format(order_builder_url, order_name)

        title_row = ''
        proj_row = ''
        if title:
            full_title = title.get('title')
            if title.get('episode') not in [None,'']:
                full_title = '%s: %s' % (full_title, title.get('episode'))
            title_row = "<tr><td align='left' style='color: #06C; font-size: 16px;'>Title: <strong>%s</strong> | Title Code: <strong>%s</strong></td></tr>" % (full_title, title.get('code')) 
        if proj:
            proj_row = "<tr><td align='left' style='color: #06C; font-size: 16px;'>Project: <strong>%s</strong> | Project Code: <strong>%s</strong></td></tr>" % (proj.get('process'), proj.get('code'))
        template_path = '/opt/spt/custom/formatted_emailer/error_msg.html'
        filled_in_path = '/var/www/html/formatted_emails/error_msg_%s.html' % wo_code
        template = open(template_path, 'r')
        filled = ''
        for line in template:
            line = line.replace('[WORK_ORDER_CODE]', wo_code)
            line = line.replace('[TITLE_CODE]', title.get('code'))
            line = line.replace('[PROJ_CODE]', proj.get('code'))
            line = line.replace('[TITLE_ROW]', title_row)
            line = line.replace('[PROJ_ROW]', proj_row)
            line = line.replace('[ORDER_CODE]', order.get('code'))
            line = line.replace('[LOGIN]', user_name)
            line = line.replace('[GROUP]', group)
            line = line.replace('[PROCESS]', process)
            line = line.replace('[CLIENT_NAME]', client_name)
            line = line.replace('[PO_NUMBER]', po_number)
            line = line.replace('[ORDER_NAME]', order_hyperlink)
            line = line.replace('[TITLE]', title_name)
            line = line.replace('[EPISODE]', episode)
            line = line.replace('[ERROR_TYPE]', error_type)
            line = line.replace('[REJECTION_CAUSE]', rejection_cause)
            line = line.replace('[TIME_SPENT]', time_spent)
            line = line.replace('[CLIENT_DESCRIPTION]', client_description)
            line = line.replace('[OPERATOR_DESCRIPTION]', operator_description)
            line = line.replace('[ACTION_TAKEN]', action_taken)
            filled = '%s%s' % (filled, line)
        template.close()
        filler = open(filled_in_path, 'w')
        filler.write(filled)
        filler.close()
        server.insert('twog/bundled_message', {'filled_in_path': filled_in_path, 'message': 'New Error', 'from_email': 'TechAlert@2gdigital.com', 'to_email': 'james.coffey@2gdigital.com', 'from_name': 'Tech Alert', 'subject': 'Error: %s, %s, %s: %s' % (wo_code, po_number, title_name, episode), 'all_ccs': all_ccs, 'object_code': wo_code})
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
