__all__ = ["ClientCSVExportWdg"]
import tacticenv
import os, datetime
from pyasm.biz import *
from pyasm.web import Table, DivWdg
from pyasm.widget import SelectWdg
from tactic.ui.common import BaseTableElementWdg
from tactic.ui.common import BaseRefreshWdg
from tactic.ui.panel import EditWdg

class ClientCSVExportWdg(BaseRefreshWdg):

    def init(my):
        from client.tactic_client_lib import TacticServerStub
        from pyasm.common import Environment
        my.server = TacticServerStub.get()
        my.login = Environment.get_login()
        my.user_name = my.login.get_login()
    
    def nbsp_me(my, el_stringo):
        ret_str = ''
        if el_stringo in [None,'']:
            ret_str = '&nbsp;'
        else:
            ret_str = el_stringo.replace(' ','&nbsp;')
        return ret_str

    def fix_date(my, date):
        #This is needed due to the way Tactic deals with dates (using timezone info), post v4.0
        from pyasm.common import SPTDate
        return_date = ''
        date_obj = SPTDate.convert_to_local(date)
        if date_obj not in [None,'']:
            return_date = date_obj.strftime("%Y-%m-%d  %H:%M")
        return return_date

    def make_right_code_ending(my, sid):
        ending = str(sid)
        ending_len = len(ending)
        if ending_len < 5:
            zeros = 5 - ending_len
        for num in range (0, zeros):
            ending = '0%s' % ending
        return ending

    def get_display(my):   
        order_codes = []
        if 'order_codes' in my.kwargs.keys():
            req_codes = my.kwargs.get('order_codes')
            order_codes = req_codes.split(',')
        elif 'search_keys' in my.kwargs.keys():
            search_keys = my.kwargs.get('search_keys')
            for k in search_keys:
                the_id = k.split('id=')[1]
                order_code = 'ORDER%s' % (my.make_right_code_ending(the_id))
                order_codes.append(order_code)
        straight_export = False
        if 'export_type' in my.kwargs.keys():
            export_type = my.kwargs.get('export_type')
            if export_type == 'straight_export':
                straight_export = True
        rows = []
        count = 1
        client_name = ''
        highest_note_count = 0
        for order_code in order_codes:
            order = my.server.eval("@SOBJECT(twog/order['code','%s'])" % order_code)[0]
            order_due_date = my.fix_date(order.get('due_date'))
            if order_due_date not in [None,'']:
                order_dd = order_due_date.split(' ')[0].split('-')
                order_dd_year = order_dd[0]
                order_dd_month = order_dd[1]
                order_dd_day = order_dd[2]
                order_due_date = '%s/%s/%s' % (order_dd_month, order_dd_day, order_dd_year)
            else:
                order_due_date = 'Not Set'
            if not straight_export:
                client_login = my.nbsp_me(order.get('client_login'))
                client_name = my.nbsp_me(order.get('client_name'))
                scheduler = my.nbsp_me(order.get('login'))
                po_number = my.nbsp_me(order.get('po_number'))
                order_name = my.nbsp_me(order.get('name'))
                order_row = '<tr>'
                order_row = '''%s<td id='%s_client_name'>%s</td><td id='%s_studio'>%s</td><td id='%s_scheduler'>%s</td><td id='%s_po_number'>%s</td><td id='%s_order'>%s</td><td id='%s_title'>%s</td><td id='%s_client_ref_num'>%s</td><td id='%s_territory'>%s</td><td id='%s_platform'>%s</td><td id='%s_due_date'>%s</td><td id='%s_client_status'>%s</td>''' % (order_row, count, client_login, count, client_name, count, scheduler, count, po_number, count, order_name, count, '&nbsp;', count, '&nbsp;', count, '&nbsp;', count, '&nbsp;', count, order_due_date, count, '&nbsp;')
            else:
                client_login = order.get('client_login')
                client_name = order.get('client_name')
                scheduler = order.get('login')
                po_number = order.get('po_number')
                order_name = order.get('name')
                order_row = '''"%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s"''' % (client_login, client_name, scheduler, po_number, order_name, ' ', ' ', ' ', ' ', order_due_date, ' ')
            notes = my.server.eval("@SOBJECT(sthpw/note['search_type','twog/order?project=twog']['search_id','%s']['process','client']['@ORDER_BY','timestamp desc'])" % order.get('id')) 
            note_count = 1
            for note in notes:
                if not straight_export:
                    order_row = '''%s<td id='%s_%s_note'>[%s] %s:<br/>%s</td>''' % (order_row, count, note_count + 1, note.get('timestamp').split('.')[0], note.get('login'), note.get('note').encode('utf-8'))
                else:
                    order_row = '''%s,"[%s] %s: %s"''' % (order_row, note.get('timestamp').split('.')[0], note.get('login'), note.get('note').encode('utf-8'))
                if note_count > highest_note_count:
                    highest_note_count = note_count
                note_count = note_count + 1
            rows.append(order_row)
            count = count + 1
            titles = my.server.eval("@SOBJECT(twog/title['order_code','%s'])" % order_code)
            for title in titles:
                title_title = title.get('title')
                title_episode = title.get('episode')
                if title_episode not in [None,'']:
                    title_title = '%s: %s' % (title_title, title_episode)
                if not straight_export:
                    title_title = my.nbsp_me(title_title)
                    title_client_ref_num = my.nbsp_me(title.get('title_id_number'))
                    title_territory = title.get('territory')
                    if title_territory == '--Select--':
                        title_territory = '&nbsp;'
                    else:
                        title_territory = my.nbsp_me(title_territory)
                    title_platform = title.get('platform')
                    if title_platform == '--Select--':
                        title_platform = '&nbsp;'
                    else:
                        title_platform = my.nbsp_me(title_platform)
                    title_client_status = my.nbsp_me(title.get('client_status'))
                else:
                    title_client_ref_num = title.get('title_id_number')
                    title_territory = title.get('territory')
                    if title_territory == '--Select--':
                        title_territory = ' '
                    else:
                        title_territory = title_territory
                    title_platform = title.get('platform')
                    if title_platform == '--Select--':
                        title_platform = ' '
                    else:
                        title_platform = title_platform
                    title_client_status = title.get('client_status')

                title_due_date = my.fix_date(title.get('due_date'))
                if title_due_date not in [None,'']:
                    title_dd = title_due_date.split(' ')[0].split('-')
                    title_dd_year = title_dd[0]
                    title_dd_month = title_dd[1]
                    title_dd_day = title_dd[2]
                    title_due_date = '%s/%s/%s' % (title_dd_month, title_dd_day, title_dd_year)
                else:
                    title_due_date = 'Not Set'
                if not straight_export:
                    title_row = '<tr>'
                    title_row = '''%s<td id='%s_client_name'>%s</td><td id='%s_studio'>%s</td><td id='%s_scheduler'>%s</td><td id='%s_po_number'>%s</td><td id='%s_order'>%s</td><td id='%s_title'>%s</td><td id='%s_client_ref_num'>%s</td><td id='%s_territory'>%s</td><td id='%s_platform'>%s</td><td id='%s_due_date'>%s</td><td id='%s_client_status'>%s</td>''' % (title_row, count, client_login, count, client_name, count, scheduler, count, po_number, count, order_name, count, title_title, count, title_client_ref_num, count, title_territory, count, title_platform, count, title_due_date, count, title_client_status)
                else:
                    title_row = '''"%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s"''' % (client_login, client_name, scheduler, po_number, order_name, title_title, title_client_ref_num, title_territory, title_platform, title_due_date, title_client_status)
                note_count = 1
                notes = my.server.eval("@SOBJECT(sthpw/note['search_type','twog/title?project=twog']['search_id','%s']['process','client']['@ORDER_BY','timestamp desc'])" % title.get('id')) 
                for note in notes:
                    if not straight_export:
                        title_row = '''%s<td id='%s_%s_note'>[%s] %s:<br/>%s</td>''' % (title_row, count, note_count + 1, note.get('timestamp').split('.')[0], note.get('login'), note.get('note').encode('utf-8'))
                    else:
                        title_row = '''%s,"[%s] %s: %s"''' % (title_row, note.get('timestamp').split('.')[0], note.get('login'), note.get('note').encode('utf-8'))
                    if note_count > highest_note_count:
                        highest_note_count = note_count
                    note_count = note_count + 1
                rows.append(title_row)
                count = count + 1
        if not straight_export:
            header = '<tr style="font-weight: bold;"><td>Client Name</td><td>Studio</td><td>Scheduler</td><td>PO#</td><td>Order</td><td>Title</td><td>Client Ref #</td><td>Territory</td><td>Platform</td><td>Due Date</td><td>Status</td>'
        else:
            header = 'Client Name,Studio,Scheduler,PO#,Order,Title,Client Ref #,Territory,Platform,Due Date,Status'
        for i in range(0, highest_note_count):
            if not straight_export:
                header = '%s<td>Note %s</td>' % (header, i + 1)
            else:
                header = '%s,Note %s' % (header, i + 1)
        if not straight_export:
            header = '%s</tr>' % header
            html = '<html><table border=1>%s' % header
            col_count = 11 + highest_note_count + 1
            for row in rows:
                rs = row.split('id=')
                row_col_count = len(rs)
                if row_col_count < col_count:
                    difference = col_count - row_col_count
                    for i in range(0, difference):
                        row = '%s<td>&nbsp;</td>' % (row)
                row = '%s</tr>' % row
                html = '%s%s' % (html, row)
            html = '%s</table></html>' % html
        else:
            html = header
            col_count = 11 + highest_note_count + 1
            for row in rows:
                if row[0] == ',':
                    row = row[1:]
                html = '%s\n%s' % (html, row)
        path = ''
        if not straight_export:
            path = '/var/www/html/client_reports/%s_order_report.html' % (my.user_name.replace('.','_'))
        else:
            path = '/var/www/html/client_reports/%s_order_report.csv' % (my.user_name.replace('.','_'))
        if os.path.exists(path):
            os.system('rm -rf %s' % path)
        new_report = open(path, 'w')
        new_report.write(html)
        new_report.close()
        if not straight_export:
            table = Table()
            table.add_row()
            do_it = table.add_cell('<input type="button" value="Open Report" path="%s"/>' % path) 
            do_it.add_attr('path',path)
            do_it.add_behavior(my.get_open_csv_page())
            return table
        else:
            os.system('cp %s %s2' % (path, path))
            return path

    def get_open_csv_page(my):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                          var path = bvr.src_el.getAttribute('path');
                          var path_cut = path.split('html/')[1];
                          var url = 'http://tactic-test.2gdigital.com/' + path_cut;
                          new_win = window.open(url,'_blank','toolbar=1,location=1,directories=1,status=1,menubar=1,scrollbars=1,resizable=1'); 
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                          //alert(err);
                }
         '''
        }
        return behavior
    
