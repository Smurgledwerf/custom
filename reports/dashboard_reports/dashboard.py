__all__ = ["DashboardWdg", "OrderReportingWdg", "WorkOrderReportingWdg","ErrorReportingWdg"]
import tacticenv, os
from pyasm.common import Environment
from pyasm.biz import *
from pyasm.web import Table, DivWdg
from pyasm.widget import SelectWdg, IconWdg, TextWdg, CheckboxWdg
from tactic.ui.common import BaseTableElementWdg
from tactic.ui.common import BaseRefreshWdg

class DashboardWdg(BaseRefreshWdg):
    def init(my):
        from client.tactic_client_lib import TacticServerStub
        from pyasm.common import Environment
        my.server = TacticServerStub.get()
        my.login = Environment.get_login()
        my.user = my.login.get_login()
        my.groups_str = ''
        my.my_groups = my.server.eval("@SOBJECT(sthpw/login_in_group['login','%s'])" % my.user)
        my.timestamp = ''
        my.today = ''
        my.this_month = ''
        my.style = 'cursor: pointer; text-decoration: underline; color: blue;'
        for mg in my.my_groups:
            if my.groups_str == '':
                my.groups_str = mg.get('login_group')
            else:
                my.groups_str = '%s,%s' % (my.groups_str, mg.get('login_group'))
        my.all_groups = my.server.eval("@GET(sthpw/login_group['@ORDER_BY','login_group].login_group)")
        my.all_users = my.server.eval("@GET(sthpw/login['location','internal']['@ORDER_BY','login'].login)")
        my.all_classifications = ['Bid','In Production','On Hold','Completed','Cancelled','Master']
        my.all_platforms = my.server.eval("@GET(twog/platform['@ORDER_BY','name'].name)")
        my.client_arr = my.server.eval("@SOBJECT(twog/client['@ORDER_BY','name'])")
        my.clients = []
        for c in my.client_arr:
            my.clients.append([c.get('code'), c.get('name')])
        my.billing_list = ['Not Billed','Billed']
        my.statuses = ['Pending','Ready','In Progress','DR In Progress','Amberfin01 In Progress','Amberfin02 In Progress','BATON In Progress','Export In Progress','On Hold','Client Response','Fix Needed','Rejected','Completed','Need Buddy Check','Buddy Check In Progress']
        my.error_types = ['Rejected','Internal Error','External Error','Fix Needed']
        my.schedulers = my.server.eval("@GET(sthpw/login_in_group['login_group','in','scheduling|scheduling supervisor'].sthpw/login['@ORDER_BY','login'].login)")

    def get_popup_behavior(my, st):
        code_pre = 'ORDER'
        filter = 'simple_order_filter'
        listoid = 'order_list'
        if st == 'twog/work_order':
            code_pre = 'WORK_ORDER'
            filter = 'simple_work_order_filter'
            listoid = 'work_order_list'
        elif st == 'twog/proj':
            code_pre = 'PROJ'
            filter = 'simple_proj_filter'
            listoid = 'proj_list'
        elif st == 'twog/title':
            code_pre = 'TITLE'
            filter = 'simple_title_filter'
            listoid = 'title_list'
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        function correct_codes( s, code_pre ){
                            s_s = s.split(':');
                            s = s_s[s_s.length - 1];
                            slength = s.length;
                            if(slength < 5){
                                for(r = 0; r < 5 - slength; r++){
                                    s = '0' + s;
                                }
                            }
                            if(s.indexOf('TITLE') == -1 && s.indexOf('ORDER') == -1 && s.indexOf('PROJ') == -1){
                                correct_code = code_pre + s;
                            }else{
                                correct_code = s;
                            }
                            return correct_code;
                        } 
                        try{
                           st = '%s';
                           code_pre = '%s';
                           filter = '%s';
                           view = '%s';
                           codes_str = bvr.src_el.getAttribute('codes');
                           codes = codes_str.split(',');
                           search_keys = [];
                           codes_str2 = '';
                           for(var x = 0; x < codes.length; x++){
                               if(codes_str2 == ''){
                                   codes_str2 = correct_codes(codes[x], code_pre);
                               }else{
                                   codes_str2 = codes_str2 + '|' + correct_codes(codes[x], code_pre);
                               }
                           }
                           spt.panel.load_popup('Selected Items', 'tactic.ui.panel.ViewPanelWdg', {'layout': 'fast_table', 'simple_search_view': filter, 'search_type': st, 'view': view, 'element_name': view, 'expression': "@SOBJECT(" + st + "['code','in','" + codes_str2 + "'])"});
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                          //alert(err);
                }
         ''' % (st, code_pre, filter, listoid)}

        return behavior

    def make_timestamp(my):
        import datetime
        now = datetime.datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S")

    def make_days_difference(my, difference):
        import datetime
        now = datetime.datetime.now()
        then = now + datetime.timedelta(days=difference)
        then_again = then.strftime("%Y-%m-%d %H:%M:%S")
        return then_again 

    def force_0(my, number):
        if number in [None,'']:
            number = 0
        str = '%s' % number
        if isinstance(number, float):
            str = '%.2f' % number
        return str

    def make_report_day(my):
        report_day = my.server.eval("@SOBJECT(twog/report_day['@ORDER_BY','timestamp desc'])")[0]
        rd = Table()
        rd.add_row()
        r1 = rd.add_cell('Quick Overview')
        rd.add_row()
        intbl = Table()
        intbl.add_attr('border','1')
        intbl.add_row()
        intbl.add_cell('Type')
        intbl.add_cell('Completed<br/>Yesterday')
        intbl.add_cell('Due<br/>Today')
        intbl.add_cell('Due<br/>Tomorrow')
        intbl.add_cell('Due<br/>In Future')
        intbl.add_cell('Past Due')
        intbl.add_cell('No Due Date')
        intbl.add_row()
        order_completed_yesterday_count = my.force_0(report_day.get('order_completed_yesterday_count'))
        order_due_today_count = my.force_0(report_day.get('order_due_today_count'))
        order_due_tomorrow_count = my.force_0(report_day.get('order_due_tomorrow_count'))
        order_due_in_future_count = my.force_0(report_day.get('order_due_in_future_count'))
        order_no_due_date_count = my.force_0(report_day.get('order_no_due_date_count'))
        order_past_due_count = my.force_0(report_day.get('orders_past_due_count'))
        labelo = intbl.add_cell('ORDERS')
        cy = intbl.add_cell(order_completed_yesterday_count)
        cy.add_attr('codes', report_day.get('order_completed_yesterday'))
        cy.set_style(my.style)
        cy.add_behavior(my.get_popup_behavior('twog/order'))
        dt = intbl.add_cell(order_due_today_count)
        dt.add_attr('codes', report_day.get('order_due_today'))
        dt.set_style(my.style)
        dt.add_behavior(my.get_popup_behavior('twog/order'))
        dm = intbl.add_cell(order_due_tomorrow_count)
        dm.add_attr('codes', report_day.get('order_due_tomorrow'))
        dm.set_style(my.style)
        dm.add_behavior(my.get_popup_behavior('twog/order'))
        df = intbl.add_cell(order_due_in_future_count)
        df.add_attr('codes', report_day.get('order_due_in_future'))
        df.set_style(my.style)
        df.add_behavior(my.get_popup_behavior('twog/order'))
        pd = intbl.add_cell(order_past_due_count)
        pd.add_attr('codes', report_day.get('orders_past_due'))
        pd.set_style(my.style)
        pd.add_behavior(my.get_popup_behavior('twog/order'))
        nd = intbl.add_cell(order_no_due_date_count)
        nd.add_attr('codes', report_day.get('order_no_due_date'))
        nd.set_style(my.style)
        nd.add_behavior(my.get_popup_behavior('twog/order'))
        intbl.add_row()
        title_completed_yesterday_count = my.force_0(report_day.get('title_completed_yesterday_count'))
        title_due_today_count = my.force_0(report_day.get('title_due_today_count'))
        title_due_tomorrow_count = my.force_0(report_day.get('title_due_tomorrow_count'))
        title_due_in_future_count = my.force_0(report_day.get('title_due_in_future_count'))
        title_no_due_date_count = my.force_0(report_day.get('title_no_due_date_count'))
        title_past_due_count = my.force_0(report_day.get('titles_past_due_count'))
        labelt = intbl.add_cell('TITLES')
        cy = intbl.add_cell(title_completed_yesterday_count)
        cy.add_attr('codes', report_day.get('title_completed_yesterday'))
        cy.set_style(my.style)
        cy.add_behavior(my.get_popup_behavior('twog/title'))
        dt = intbl.add_cell(title_due_today_count)
        dt.add_attr('codes', report_day.get('title_due_today'))
        dt.set_style(my.style)
        dt.add_behavior(my.get_popup_behavior('twog/title'))
        dm = intbl.add_cell(title_due_tomorrow_count)
        dm.add_attr('codes', report_day.get('title_due_tomorrow'))
        dm.set_style(my.style)
        dm.add_behavior(my.get_popup_behavior('twog/title'))
        df = intbl.add_cell(title_due_in_future_count)
        df.add_attr('codes', report_day.get('title_due_in_future'))
        df.set_style(my.style)
        df.add_behavior(my.get_popup_behavior('twog/title'))
        pd = intbl.add_cell(title_past_due_count)
        pd.add_attr('codes', report_day.get('titles_past_due'))
        pd.set_style(my.style)
        pd.add_behavior(my.get_popup_behavior('twog/title'))
        nd = intbl.add_cell(title_no_due_date_count)
        nd.add_attr('codes', report_day.get('title_no_due_date'))
        nd.set_style(my.style)
        nd.add_behavior(my.get_popup_behavior('twog/title'))
        intbl.add_row()
        wo_completed_yesterday_count = my.force_0(report_day.get('wo_completed_yesterday_count'))
        wo_due_today_count = my.force_0(report_day.get('wo_due_today_count'))
        wo_due_tomorrow_count = my.force_0(report_day.get('wo_due_tomorrow_count'))
        wo_due_in_future_count = my.force_0(report_day.get('wo_due_in_future_count'))
        wo_no_due_date_count = my.force_0(report_day.get('wo_no_due_date_count'))
        wo_past_due_count = my.force_0(report_day.get('wo_past_due_count'))
        labelt = intbl.add_cell('WORK ORDERS')
        cy = intbl.add_cell(wo_completed_yesterday_count)
        cy.add_attr('codes', report_day.get('wo_completed_yesterday'))
        cy.set_style(my.style)
        cy.add_behavior(my.get_popup_behavior('twog/work_order'))
        dt = intbl.add_cell(wo_due_today_count)
        dt.add_attr('codes', report_day.get('wo_due_today'))
        dt.set_style(my.style)
        dt.add_behavior(my.get_popup_behavior('twog/work_order'))
        dm = intbl.add_cell(wo_due_tomorrow_count)
        dm.add_attr('codes', report_day.get('wo_due_tomorrow'))
        dm.set_style(my.style)
        dm.add_behavior(my.get_popup_behavior('twog/work_order'))
        df = intbl.add_cell(wo_due_in_future_count)
        df.add_attr('codes', report_day.get('wo_due_in_future'))
        df.set_style(my.style)
        df.add_behavior(my.get_popup_behavior('twog/work_order'))
        pd = intbl.add_cell(wo_past_due_count)
        pd.add_attr('codes', report_day.get('wo_past_due'))
        pd.set_style(my.style)
        pd.add_behavior(my.get_popup_behavior('twog/work_order'))
        nd = intbl.add_cell(wo_no_due_date_count)
        nd.add_attr('codes', report_day.get('wo_no_due_date'))
        nd.set_style(my.style)
        nd.add_behavior(my.get_popup_behavior('twog/work_order'))
        rd.add_cell(intbl)
        return rd

    def get_rowhide_behavior(my, filter_type):
          
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        function oc(a){
                            var o = {};
                            for(var i=0;i<a.length;i++){
                                o[a[i]]='';
                            }
                            return o;
                        }
                        try{
                            var top_el = spt.api.get_parent(bvr.src_el, '.Dashboard_Table');
                            var rows = top_el.getElementsByTagName('tr');
                            filter_type = '%s';
                            if(filter_type != 'reginfo'){
                                for(var r = 0; r < rows.length; r++){
                                    if(rows[r].getAttribute('class') == filter_type){
                                        if(rows[r].style.display in oc([null,'','table-row'])){
                                            rows[r].style.display = 'none';
                                        }else{
                                            rows[r].style.display = 'table-row';
                                        }
                                    }
                                } 
                            }else{
                                for(var r = 0; r < rows.length; r++){
                                    rows[r].style.display = 'table-row';
                                } 
                            }
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                          //alert(err);
                }
         ''' % (filter_type)}

        return behavior

    def get_rerun_behavior(my):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                           bvr.src_el.innerHTML = '';
                           var server = TacticServerStub.get();
                           var cmd = "reports.dashboard_reports.DashboardReRunCmd";
                           server.execute_cmd(cmd, {});
                           alert('Re-Running Reports. Please wait approximately 2 hours to refresh.');
                            
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                          //alert(err);
                }
         '''}

        return behavior

    def get_shrink_priorities_behavior(my):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                           bvr.src_el.innerHTML = '';
                           var server = TacticServerStub.get();
                           var cmd = "manual_updaters.ShrinkPrioritiesCmd";
                           server.execute_cmd(cmd, {});
                           alert('Finished Downward Adjustment of Priorities');
                            
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                          //alert(err);
                }
         '''}

        return behavior

    def get_whats_new_email(my):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                           bvr.src_el.innerHTML = '';
                           var server = TacticServerStub.get();
                           last_wn = server.eval("@SOBJECT(twog/whats_new['@ORDER_BY','code desc'])")[0];
                           note = 'Changes have been made to Tactic. Please see the "Whats New" section in Tactic to see what has changed.';
                           thing = server.execute_cmd('operator_view.MakeBasicNoteWdg', {'obj_sk': last_wn.__search_key__, 'header': "Updates have been made to Tactic", 'note': note, 'note_ccs': '2gstaff@2gdigital.com'});
                           alert('Whats New Email Sent');
                            
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                          //alert(err);
                }
         '''}

        return behavior

    def get_refresh_behavior(my):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                           top_el = document.getElementsByClassName('Dashboard_Table')[0];
                           spt.api.load_panel(top_el, 'reports.dashboard_reports.DashboardWdg', {});
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                          //alert(err);
                }
         '''}

        return behavior
        


    def get_report_view_buttons(my):
        table = Table()
        table.add_attr('bgcolor','#9e5e2e')
        table.add_row()
        title = table.add_cell('<b>Report View Options</b>')
        title.add_attr('align','center')
        table.add_row()
        butt1 = table.add_cell('<input type="button" value="All Info"/>')
        butt1.add_behavior(my.get_rowhide_behavior('reginfo'))
        butt2 = table.add_cell('<input type="button" value="Hours"/>')
        butt2.add_behavior(my.get_rowhide_behavior('costinfo'))
        butt3 = table.add_cell('<input type="button" value="Costs"/>')
        butt3.add_behavior(my.get_rowhide_behavior('hourinfo'))
        butt4 = table.add_cell('<input type="button" value="Refresh"/>')
        butt4.add_behavior(my.get_refresh_behavior())
        t2 = Table()
        t2.add_attr('border','1')
        t2.add_row()
        t2.add_cell(table)
        return t2

    def get_command_buttons(my):
        table = Table()
        table.add_attr('bgcolor','#0e6e3e')
        table.add_row()
        title = table.add_cell('<font color="#FFFFFF"><b>Command Buttons</b></font>')
        title.add_attr('align','center')
        table.add_row()
        butt5 = table.add_cell('<input type="button" value="Re-Run Reports (2 Hours)"/>')
        butt5.add_behavior(my.get_rerun_behavior())
        butt6 = table.add_cell('<input type="button" value="Shrink Priorities"/>')
        butt6.add_behavior(my.get_shrink_priorities_behavior())
        butt7 = table.add_cell('<input type="button" value="Send Whats New Email"/>')
        butt7.add_behavior(my.get_whats_new_email())
        t2 = Table()
        t2.add_attr('border','1')
        t2.add_row()
        t2.add_cell(table)
        return t2

    def get_buttons(my):
        table = Table()
        table.add_row()
        table.add_cell(my.get_report_view_buttons())
        full_wid2 = table.add_cell(' ')
        full_wid2.add_attr('width','100%s' % '%')
        table.add_cell(my.get_command_buttons())
        return table
    
    def get_display(my):   
        my.timestamp = my.make_timestamp()
        my.today = my.timestamp.split(' ')[0]
        this_month_s = my.today.split('-')
        my.this_month = '%s-%s' % (this_month_s[0], this_month_s[1])
        widget = DivWdg()
        table = Table()
        table.add_attr('class','Dashboard_Table')
        table.add_row()
        table.add_cell(my.get_buttons())
        table.add_row()
        title_tbl = Table()
        title_tbl.add_row()
        ttb = title_tbl.add_cell('Reports for %s' % my.today)
        ttb.set_style('font-size: 20px;')
        table.add_cell(title_tbl)
        table.add_row()
        table.add_cell(my.make_report_day())
        table.add_row()
        order_report_tbl = OrderReportingWdg()
        order_report_cell = table.add_cell(order_report_tbl)
        order_report_cell.add_attr('class','order_report_cell')
        table.add_row()
        work_order_report_tbl = WorkOrderReportingWdg()
        work_order_report_cell = table.add_cell(work_order_report_tbl)
        work_order_report_cell.add_attr('class','work_order_report_cell')
        table.add_row()
        error_report_tbl = ErrorReportingWdg()
        error_report_cell = table.add_cell(error_report_tbl)
        error_report_cell.add_attr('class','error_report_cell')
        widget.add(table)
        return widget

class OrderReportingWdg(BaseRefreshWdg):
    def init(my):
        from client.tactic_client_lib import TacticServerStub
        from pyasm.common import Environment
        my.timestamp = my.make_timestamp()
        my.today = my.timestamp.split(' ')[0]
        this_month_s = my.today.split('-')
        my.this_month = '%s-%s' % (this_month_s[0], this_month_s[1])
        my.server = TacticServerStub.get()
        my.login = Environment.get_login()
        my.user = my.login.get_login()
        my.groups_str = ''
        my.my_groups = my.server.eval("@SOBJECT(sthpw/login_in_group['login','%s'])" % my.user)
        my.style = 'cursor: pointer; text-decoration: underline; color: blue;'
        for mg in my.my_groups:
            if my.groups_str == '':
                my.groups_str = mg.get('login_group')
            else:
                my.groups_str = '%s,%s' % (my.groups_str, mg.get('login_group'))
        my.all_groups = my.server.eval("@GET(sthpw/login_group['@ORDER_BY','login_group].login_group)")
        my.all_users = my.server.eval("@GET(sthpw/login['location','internal']['@ORDER_BY','login'].login)")
        my.all_classifications = ['Bid','In Production','On Hold','Completed','Cancelled','Master']
        my.all_platforms = my.server.eval("@GET(twog/platform['@ORDER_BY','name'].name)")
        my.client_arr = my.server.eval("@SOBJECT(twog/client['@ORDER_BY','name'])")
        my.clients = []
        my.client_codes = []
        my.client_dict = {}
        for c in my.client_arr:
            my.clients.append([c.get('code'), c.get('name')])
            my.client_dict[c.get('code')] = c.get('name')
            my.client_codes.append(c.get('code'))
        my.billing_list = ['Not Billed','Billed']
        my.statuses = ['Pending','Ready','In Progress','DR In Progress','Amberfin01 In Progress','Amberfin02 In Progress','BATON In Progress','Export In Progress','On Hold','Client Response','Fix Needed','Rejected','Completed','Need Buddy Check','Buddy Check In Progress']
        my.error_types = ['Rejected','Internal Error','External Error','Fix Needed']
        my.schedulers = my.server.eval("@GET(sthpw/login_in_group['login_group','in','scheduling|scheduling supervisor'].sthpw/login['@ORDER_BY','login'].login)")
        my.finder = {'group': my.all_groups, 'login_name': my.all_users, 'classification': my.all_classifications, 'platform': my.all_platforms, 'client_code': my.client_codes, 'billed': my.billing_list} 

    def get_popup_behavior(my, st):
        code_pre = 'ORDER'
        filter = 'simple_order_filter'
        listoid = 'order_list'
        if st == 'twog/work_order':
            code_pre = 'WORK_ORDER'
            filter = 'simple_work_order_filter'
            listoid = 'work_order_list'
        elif st == 'twog/proj':
            code_pre = 'PROJ'
            filter = 'simple_proj_filter'
            listoid = 'proj_list'
        elif st == 'twog/title':
            code_pre = 'TITLE'
            filter = 'simple_title_filter'
            listoid = 'title_list'
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        function correct_codes( s, code_pre ){
                            s_s = s.split(':');
                            s = s_s[s_s.length - 1];
                            slength = s.length;
                            if(slength < 5){
                                for(r = 0; r < 5 - slength; r++){
                                    s = '0' + s;
                                }
                            }
                            if(s.indexOf('TITLE') == -1 && s.indexOf('ORDER') == -1 && s.indexOf('PROJ') == -1){
                                correct_code = code_pre + s;
                            }else{
                                correct_code = s;
                            }
                            return correct_code;
                        } 
                        try{
                           st = '%s';
                           code_pre = '%s';
                           filter = '%s';
                           view = '%s';
                           codes_str = bvr.src_el.getAttribute('codes');
                           codes = codes_str.split(',');
                           search_keys = [];
                           codes_str2 = '';
                           for(var x = 0; x < codes.length; x++){
                               if(codes_str2 == ''){
                                   codes_str2 = correct_codes(codes[x], code_pre);
                               }else{
                                   codes_str2 = codes_str2 + '|' + correct_codes(codes[x], code_pre);
                               }
                           }
                           spt.panel.load_popup('Selected Items', 'tactic.ui.panel.ViewPanelWdg', {'layout': 'fast_table', 'simple_search_view': filter, 'search_type': st, 'view': view, 'element_name': view, 'expression': "@SOBJECT(" + st + "['code','in','" + codes_str2 + "'])"});
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                          //alert(err);
                }
         ''' % (st, code_pre, filter, listoid)}

        return behavior

    def make_timestamp(my):
        import datetime
        now = datetime.datetime.now()
        #print "NOW = %s" % now
        return now.strftime("%Y-%m-%d %H:%M:%S")

    def make_days_difference(my, difference):
        import datetime
        now = datetime.datetime.now()
        then = now + datetime.timedelta(days=difference)
        then_again = then.strftime("%Y-%m-%d %H:%M:%S")
        return then_again 

    def force_0(my, number):
        str = '%s' % number
        if number == 0:
            str = '0'
        if isinstance(number, float):
            str = '%.2f' % number
        return str


    def make_order_tbl(my, sobs, title, focus_col):
        rtbl = Table()
        rtbl.add_attr('border','1')
        rtbl.add_row()
        top = rtbl.add_cell('<u><b>%s</b></u>' % title)
        top.add_attr('colspan', len(sobs))
        top.add_attr('align','center')
        d = {'completion_date': 'Completion Date', 'due_date': 'Due Date', 'count': 'Order Count', 'total_cost': 'Total Cost', 'billable_cost': 'Billable Cost', 'estimated_cost': 'Estimated Cost', 't_actual_cost': 'Triggered Actual Cost', 't_expected_cost': 'Triggered Expected Cost', 'price': 'Price', 'expected_price': 'Expected Price', 'wh_total_hours': 'Total Work Hours', 'wh_billable_hours': 'Billable Work Hours', 'wh_estimated_hours': 'Estimated Work Hours', 'wh_total_cost': 'Total WH Cost', 'wh_billable_cost': 'Billable WH Cost', 'wh_estimated_cost': 'Estimated WH Cost', 'eq_actual_hours': 'Actual EQ Hours', 'eq_expected_hours': 'Estimated EQ Hours', 'eq_actual_cost': 'Actual EQ Cost', 'eq_expected_cost': 'Estimated EQ Cost'}
        report_cols = ['count','total_cost','billable_cost','estimated_cost','t_actual_cost','t_expected_cost','price','expected_price','wh_total_hours','wh_billable_hours','wh_estimated_hours','wh_total_cost','wh_billable_cost','wh_estimated_cost','eq_actual_hours','eq_expected_hours','eq_actual_cost','eq_expected_cost']
        totals = {'order_codes': ''}      
        rtbl.add_row()
        rtbl.add_cell(d[focus_col].replace(' ','<br/>'))
        for sob in sobs:
            rtbl.add_cell(sob.get(focus_col).split(' ')[0])
        rtbl.add_cell('TOTAL')
        for guy in report_cols:
            if guy not in totals.keys():
                totals[guy] = 0
            name = d[guy]
            row_class = 'reginfo'
            if 'Hour' in name:
                row_class = 'hourinfo'
            elif 'Cost' in name:
                row_class = 'costinfo'
            color = '#FFFFFF'
            if 'EQ' in name:
                color = '#f8dd9f'
            elif 'WH' in name or 'Work Hour' in name:
                color = '#aff8f0'
            elif 'Price' in name:
                color = '#c6f8af'
            the_row = rtbl.add_row()
            the_row.add_attr('class',row_class)
            the_row.add_style('background-color: %s;' % color)
            rtbl.add_cell(name)
            for sob in sobs:
                val = my.force_0(sob.get(guy))
                totals[guy] = totals[guy] + float(val)
                dyn = rtbl.add_cell(val)
                if guy == 'count':
                    order_codes = sob.get('order_codes')
                    if totals['order_codes'] == '':
                        totals['order_codes'] = order_codes
                    else:
                        totals['order_codes'] = '%s,%s' % (totals['order_codes'], order_codes)
                    dyn.add_attr('codes',sob.get('order_codes'))
                    dyn.set_style(my.style)
                    dyn.add_behavior(my.get_popup_behavior('twog/order'))
            if guy == 'count':
                ttl = rtbl.add_cell(int(totals[guy]))
                ttl.add_attr('codes',totals['order_codes'])
                ttl.set_style(my.style)
                ttl.add_behavior(my.get_popup_behavior('twog/order'))
            else:
                ttl = rtbl.add_cell(totals[guy])
        return rtbl

    def get_redo_dates_behavior(my):
        behavior = {'css_class': 'clickish', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                               hashish = {}
                               selectors_el = document.getElementsByClassName('order_selectors')[0];
                               selectors = selectors_el.getElementsByTagName('select');
                               for(var r = 0; r < selectors.length; r++){
                                   name = selectors[r].getAttribute('name');
                                   field = name.split('_sel')[0];
                                   hashish[field] = selectors[r].value;
                               }
                               days_past_el = selectors_el.getElementsByClassName('days_past')[0];
                               days_future_el = selectors_el.getElementsByClassName('days_future')[0];
                               date1 = days_past_el.value; 
                               date2 = days_future_el.value;
                               if(isNaN(date1)){
                                   date1 = -15;
                               }else{
                                   date1 = Number(date1) * -1;
                               }
                               if(isNaN(date2)){
                                   date2 = 15;
                               }else{
                                   date2 = Number(date2);
                               }
                               hashish['date1'] = date1;
                               hashish['date2'] = date2; 
                               order_report_cell = document.getElementsByClassName('order_report_cell')[0];
                               spt.api.load_panel(order_report_cell, 'reports.dashboard_reports.OrderReportingWdg', hashish);
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                          //alert(err);
                }
         '''}
        return behavior

    def get_sel_change_behavior(my):
        behavior = {'css_class': 'sel_change', 'type': 'change', 'cbjs_action': '''        
                        try{
                               hashish = {}
                               selectors_el = document.getElementsByClassName('order_selectors')[0];
                               selectors = selectors_el.getElementsByTagName('select');
                               for(var r = 0; r < selectors.length; r++){
                                   name = selectors[r].getAttribute('name');
                                   field = name.split('_sel')[0];
                                   hashish[field] = selectors[r].value;
                               }
                               days_past_el = selectors_el.getElementsByClassName('days_past')[0];
                               days_future_el = selectors_el.getElementsByClassName('days_future')[0];
                               date1 = days_past_el.value; 
                               date2 = days_future_el.value;
                               if(isNaN(date1)){
                                   date1 = -15;
                               }else{
                                   date1 = Number(date1) * -1;
                               }
                               if(isNaN(date2)){
                                   date2 = 15;
                               }else{
                                   date2 = Number(date2);
                               }
                               hashish['date1'] = date1;
                               hashish['date2'] = date2; 
                               order_report_cell = document.getElementsByClassName('order_report_cell')[0];
                               spt.api.load_panel(order_report_cell, 'reports.dashboard_reports.OrderReportingWdg', hashish);
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                          //alert(err);
                }
         '''}
        return behavior

    def get_str_pair(my, key, val):
        str_out = ''
        if 'client' in key:
            str_out = 'CLIENT: %s' % my.client_dict[val].upper()
        else:
            str_out = '%s: %s' % (key.upper(), val.upper())
        return str_out

    def get_search_dicts(my, search_dict):
        alls = []
        search_dicts = []
        for key in search_dict.keys():
            if 'date' not in key:
                if search_dict[key] == 'ALL':
                    alls.append(key)
        lenall = len(alls)
        sd_count = 0
        if lenall == 1:
            list = my.finder[alls[0]]
            for guy in list:
                new_dict = {alls[0]: guy}
                new_str = my.get_str_pair(alls[0], guy)
                for k2 in search_dict.keys():
                    if k2 not in new_dict.keys():
                        new_dict[k2] = search_dict[k2]
                        if search_dict[k2] != '-1' and 'date' not in k2:
                            new_str = '%s, %s' % (new_str, my.get_str_pair(k2, search_dict[k2]))
                new_dict['search_string'] = new_str
                search_dicts.append(new_dict)
                sd_count = sd_count + 1
        elif lenall == 2:
            list1 = my.finder[alls[0]]
            list2 = my.finder[alls[1]]
            for guy1 in list1:
                for guy2 in list2:
                    new_dict = {alls[0]: guy1, alls[1]: guy2}
                    new_str = '%s, %s' % (my.get_str_pair(alls[0], guy1), my.get_str_pair(alls[1], guy2))
                    for k2 in search_dict.keys():
                        if k2 not in new_dict.keys():
                            new_dict[k2] = search_dict[k2]
                            if search_dict[k2] != '-1' and 'date' not in k2:
                                new_str = '%s, %s' % (new_str, my.get_str_pair(k2, search_dict[k2]))
                    new_dict['search_string'] = new_str
                    search_dicts.append(new_dict)
                    sd_count = sd_count + 1
        elif lenall == 3:
            list1 = my.finder[alls[0]]
            list2 = my.finder[alls[1]]
            list3 = my.finder[alls[2]]
            for guy1 in list1:
                for guy2 in list2:
                    for guy3 in list3:
                        new_dict = {alls[0]: guy1, alls[1]: guy2, alls[2]: guy3}
                        new_str = '%s, %s, %s' % (my.get_str_pair(alls[0], guy1), my.get_str_pair(alls[1], guy2), my.get_str_pair(alls[2], guy3))
                        for k2 in search_dict.keys():
                            if k2 not in new_dict.keys():
                                new_dict[k2] = search_dict[k2]
                                if search_dict[k2] != '-1' and 'date' not in k2:
                                    new_str = '%s, %s' % (new_str, my.get_str_pair(k2, search_dict[k2]))
                        new_dict['search_string'] = new_str
                        search_dicts.append(new_dict)
                        sd_count = sd_count + 1
        elif lenall == 4:
            list1 = my.finder[alls[0]]
            list2 = my.finder[alls[1]]
            list3 = my.finder[alls[2]]
            list4 = my.finder[alls[3]]
            for guy1 in list1:
                for guy2 in list2:
                    for guy3 in list3:
                        for guy4 in list4:
                            new_dict = {alls[0]: guy1, alls[1]: guy2, alls[2]: guy3, alls[3]: guy4}
                            new_str = '%s, %s, %s, %s' % (my.get_str_pair(alls[0], guy1), my.get_str_pair(alls[1], guy2), my.get_str_pair(alls[2], guy3), my.get_str_pair(alls[3], guy4))
                            for k2 in search_dict.keys():
                                if k2 not in new_dict.keys():
                                    new_dict[k2] = search_dict[k2]
                                    if search_dict[k2] != '-1' and 'date' not in k2:
                                        new_str = '%s, %s' % (new_str, my.get_str_pair(k2, search_dict[k2]))
                            new_dict['search_string'] = new_str
                            search_dicts.append(new_dict)
                            sd_count = sd_count + 1
        if sd_count == 0:
            search_dict['search_string'] = 'Totals'
            search_dicts.append(search_dict)
        return search_dicts

    def get_display(my):
        date1_int = -15
        date1 = my.make_days_difference(date1_int) 
        date2_int = 15
        date2 = my.make_days_difference(date2_int)
        search_dict = {'date1': date1, 'date2': date2, 'classification': '-1', 'platform': '-1', 'client_code': '-1', 'billed': '-1'}
        if 'date1' in my.kwargs.keys():
            date1_int = int(my.kwargs.get('date1')) 
            search_dict['date1'] = my.make_days_difference(date1_int)
            date1 = search_dict['date1']
        if 'date2' in my.kwargs.keys():
            date2_int = int(my.kwargs.get('date2'))
            search_dict['date2'] = my.make_days_difference(date2_int)
            date2 = search_dict['date2']
        if 'platform' in my.kwargs.keys():
            search_dict['platform'] = my.kwargs.get('platform')
        if 'classification' in my.kwargs.keys():
            search_dict['classification'] = my.kwargs.get('classification')
        if 'client_code' in my.kwargs.keys():
            search_dict['client_code'] = my.kwargs.get('client_code')
        if 'billed' in my.kwargs.keys():
            search_dict['billed'] = my.kwargs.get('billed')
        search_dict_clone = search_dict
        search_dicts = my.get_search_dicts(search_dict)
        #print "SEARCH DICTS = %s" % search_dicts

        selectors = Table()
        selectors.add_attr('class','order_selectors')
        selectors.add_row()
        dates = Table()
        dates.add_attr('class','order_dates')
        dates.add_attr('align','center')
        dates.add_row()
        dates.add_cell('Days into past:')
        date1_str = '%s' % date1_int
        date1_str = date1_str.replace('-','')
        dates.add_cell('<input type="text" value="%s" class="days_past" style="width: 35px;"/>' % date1_str)
        dates.add_cell('Days into future:')
        dates.add_cell('<input type="text" value="%s" class="days_future" style="width: 35px;"/>' % date2_int)
        set_dates = dates.add_cell('<input type="button" value="Set Dates"/>')
        set_dates.add_behavior(my.get_redo_dates_behavior())
        dates_cell =selectors.add_cell(dates)
        dates_cell.add_attr('colspan','8')
        selectors.add_row()

        classification_sel = SelectWdg('classification_sel')
        classification_sel.append_option('Ignore','-1')
        classification_sel.append_option('Show All','ALL')
        classification_sel.append_option('Not Set','0')
        for c in my.all_classifications:
            classification_sel.append_option(c,c)
        classification_sel.set_value(search_dict_clone['classification'])
        classification_sel.add_behavior(my.get_sel_change_behavior())
        selectors.add_cell('Classification: ')
        selectors.add_cell(classification_sel)

        platform_sel = SelectWdg('platform_sel')
        platform_sel.append_option('Ignore','-1')
        platform_sel.append_option('Show All','ALL')
        platform_sel.append_option('Not Set','0')
        for p in my.all_platforms:
            if p != '0':
                platform_sel.append_option(p,p)
        platform_sel.set_value(search_dict_clone['platform'])
        platform_sel.add_behavior(my.get_sel_change_behavior())
        selectors.add_cell(' Platform: ')
        selectors.add_cell(platform_sel)

        client_sel = SelectWdg('client_code_sel')
        client_sel.append_option('Ignore','-1')
        client_sel.append_option('Show All','ALL')
        client_sel.append_option('Not Set','0')
        for c in my.clients:
            if c[1] != '0':
                client_sel.append_option(c[1],c[0])
        client_sel.set_value(search_dict_clone['client_code'])
        client_sel.add_behavior(my.get_sel_change_behavior())
        selectors.add_cell(' Client: ')
        selectors.add_cell(client_sel)

        billing_sel = SelectWdg('billed_sel')
        billing_sel.append_option('Ignore','-1')
        billing_sel.append_option('Show All','ALL')
        billing_sel.append_option('Not Set','0')
        for b in my.billing_list:
            billing_sel.append_option(b,b)
        billing_sel.set_value(search_dict_clone['billed'])
        billing_sel.add_behavior(my.get_sel_change_behavior())
        selectors.add_cell(' Billed: ')
        selectors.add_cell(billing_sel)

        od = Table()
        #od.add_attr('bgcolor','#FF0000')
        count = 0
        for s in search_dicts:
            sob_count = 0
            compl_expr = "@SOBJECT(twog/order_report['completion_date','>=','%s']['completion_date','<=','%s']" % (s['date1'], s['date2'])
            fields = ['classification','platform','client_code','billed']
            for f in fields:
                compl_expr = "%s['%s','%s']" % (compl_expr, f, s[f])
            compl_expr = "%s['@ORDER_BY','completion_date'])" % compl_expr
            completion_reports = my.server.eval(compl_expr)
            sob_count = len(completion_reports)
            due_expr = "@SOBJECT(twog/order_report['due_date','>=','%s']['due_date','<=','%s']" % (my.today, s['date2'])
            for f in fields:
                due_expr = "%s['%s','%s']" % (due_expr, f, s[f])
            due_expr = "%s['@ORDER_BY','due_date'])" % due_expr
            due_reports = my.server.eval(due_expr)
            sob_count = sob_count + len(due_reports)
            if sob_count > 0:
                extra_str = s['search_string']
                if extra_str != '':
                    extra_str = '%s<br/>' % extra_str
                od.add_row()
                od1 = od.add_cell("ORDERS BY DAY<br/>%sStart Date: %s<br/>&nbsp;&nbsp;End Date: %s" % (extra_str, date1, date2))
                od1.add_attr('align','center')
                od1.add_attr('colspan','2')
                if count == 0:
                    od.add_row()
                    od2 = od.add_cell(selectors)
                    od2.add_attr('align','center')
                    od2.add_attr('colspan','2')
                od.add_row()
                completed = od.add_cell(my.make_order_tbl(completion_reports, 'Completion Dates', 'completion_date'))
                completed.add_attr('valign','top')
                due = od.add_cell(my.make_order_tbl(due_reports, 'Due Dates', 'due_date'))
                due.add_attr('valign','top')
                count = count + 1
        if count == 0:
            od.add_row()
            od1 = od.add_cell("ORDERS BY DAY<br/>Start Date: %s<br/>&nbsp;&nbsp;End Date: %s" % (date1, date2))
            od1.add_attr('align','center')
            od1.add_attr('colspan','2')
            od.add_row()
            od2 = od.add_cell(selectors)
            od2.add_attr('align','center')
            od2.add_attr('colspan','2')
            od.add_row()
            od3 = od.add_cell('NO REPORTS FOUND')
            od3.add_attr('colspan','2')
            od3.add_attr('align','center')
                
        return od

class WorkOrderReportingWdg(BaseRefreshWdg):
    def init(my):
        from client.tactic_client_lib import TacticServerStub
        from pyasm.common import Environment
        my.timestamp = my.make_timestamp()
        my.today = my.timestamp.split(' ')[0]
        this_month_s = my.today.split('-')
        my.this_month = '%s-%s' % (this_month_s[0], this_month_s[1])
        my.server = TacticServerStub.get()
        my.login = Environment.get_login()
        my.user = my.login.get_login()
        my.groups_str = ''
        my.my_groups = my.server.eval("@SOBJECT(sthpw/login_in_group['login','%s'])" % my.user)
        my.style = 'cursor: pointer; text-decoration: underline; color: blue;'
        for mg in my.my_groups:
            if my.groups_str == '':
                my.groups_str = mg.get('login_group')
            else:
                my.groups_str = '%s,%s' % (my.groups_str, mg.get('login_group'))
        my.all_groups = my.server.eval("@GET(sthpw/login_group['@ORDER_BY','login_group].login_group)")
        my.all_users = my.server.eval("@GET(sthpw/login['location','internal']['@ORDER_BY','login'].login)")
        my.all_classifications = ['Bid','In Production','On Hold','Completed','Cancelled','Master']
        my.all_platforms = my.server.eval("@GET(twog/platform['@ORDER_BY','name'].name)")
        my.client_arr = my.server.eval("@SOBJECT(twog/client['@ORDER_BY','name'])")
        my.clients = []
        my.client_dict = {}
        my.client_codes = []
        for c in my.client_arr:
            my.clients.append([c.get('code'), c.get('name')])
            my.client_dict[c.get('code')] = c.get('name')
            my.client_codes.append(c.get('code'))
        my.billing_list = ['Not Billed','Billed']
        my.statuses = ['Pending','Ready','In Progress','DR In Progress','Amberfin01 In Progress','Amberfin02 In Progress','BATON In Progress','Export In Progress','On Hold','Client Response','Fix Needed','Rejected','Completed','Need Buddy Check','Buddy Check In Progress']
        my.error_types = ['Rejected','Internal Error','External Error','Fix Needed']
        my.schedulers = my.server.eval("@GET(sthpw/login_in_group['login_group','in','scheduling|scheduling supervisor'].sthpw/login['@ORDER_BY','login'].login)")
        my.finder = {'group': my.all_groups, 'login_name': my.all_users, 'classification': my.all_classifications, 'platform': my.all_platforms, 'client_code': my.client_codes, 'billed': my.billing_list, 'status': my.statuses} 

    def get_popup_behavior(my, st):
        code_pre = 'ORDER'
        filter = 'simple_order_filter'
        listoid = 'order_list'
        if st == 'twog/work_order':
            code_pre = 'WORK_ORDER'
            filter = 'simple_work_order_filter'
            listoid = 'work_order_list'
        elif st == 'twog/proj':
            code_pre = 'PROJ'
            filter = 'simple_proj_filter'
            listoid = 'proj_list'
        elif st == 'twog/title':
            code_pre = 'TITLE'
            filter = 'simple_title_filter'
            listoid = 'title_list'
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        function correct_codes( s, code_pre ){
                            s_s = s.split(':');
                            s = s_s[s_s.length - 1];
                            slength = s.length;
                            if(slength < 5){
                                for(r = 0; r < 5 - slength; r++){
                                    s = '0' + s;
                                }
                            }
                            if(s.indexOf('TITLE') == -1 && s.indexOf('ORDER') == -1 && s.indexOf('PROJ') == -1){
                                correct_code = code_pre + s;
                            }else{
                                correct_code = s;
                            }
                            return correct_code;
                        } 
                        try{
                           st = '%s';
                           code_pre = '%s';
                           filter = '%s';
                           view = '%s';
                           codes_str = bvr.src_el.getAttribute('codes');
                           codes = codes_str.split(',');
                           search_keys = [];
                           codes_str2 = '';
                           for(var x = 0; x < codes.length; x++){
                               if(codes_str2 == ''){
                                   codes_str2 = correct_codes(codes[x], code_pre);
                               }else{
                                   codes_str2 = codes_str2 + '|' + correct_codes(codes[x], code_pre);
                               }
                           }
                           spt.panel.load_popup('Selected Items', 'tactic.ui.panel.ViewPanelWdg', {'layout': 'fast_table', 'simple_search_view': filter, 'search_type': st, 'view': view, 'element_name': view, 'expression': "@SOBJECT(" + st + "['code','in','" + codes_str2 + "'])"});
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                          //alert(err);
                }
         ''' % (st, code_pre, filter, listoid)}

        return behavior

    def make_timestamp(my):
        import datetime
        now = datetime.datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S")

    def make_days_difference(my, difference):
        import datetime
        now = datetime.datetime.now()
        then = now + datetime.timedelta(days=difference)
        then_again = then.strftime("%Y-%m-%d %H:%M:%S")
        return then_again 

    def force_0(my, number):
        str = '%s' % number
        if number == 0:
            str = '0'
        if isinstance(number, float):
            str = '%.2f' % number
        return str

    def get_str_pair(my, key, val):
        str_out = ''
        if 'client' in key:
            str_out = 'CLIENT: %s' % my.client_dict[val].upper()
        else:
            str_out = '%s: %s' % (key.upper(), val.upper())
        return str_out

    def get_search_dicts(my, search_dict):
        alls = []
        search_dicts = []
        for key in search_dict.keys():
            if 'date' not in key:
                if search_dict[key] == 'ALL':
                    alls.append(key)
        lenall = len(alls)
        sd_count = 0
        if lenall == 1:
            list = my.finder[alls[0]]
            for guy in list:
                new_dict = {alls[0]: guy}
                new_str = my.get_str_pair(alls[0], guy)
                for k2 in search_dict.keys():
                    if k2 not in new_dict.keys():
                        new_dict[k2] = search_dict[k2]
                        if search_dict[k2] != '-1' and 'date' not in k2:
                            new_str = '%s, %s' % (new_str, my.get_str_pair(k2, search_dict[k2]))
                new_dict['search_string'] = new_str
                search_dicts.append(new_dict)
                sd_count = sd_count + 1
        elif lenall == 2:
            list1 = my.finder[alls[0]]
            list2 = my.finder[alls[1]]
            for guy1 in list1:
                for guy2 in list2:
                    new_dict = {alls[0]: guy1, alls[1]: guy2}
                    new_str = '%s, %s' % (my.get_str_pair(alls[0], guy1), my.get_str_pair(alls[1], guy2))
                    for k2 in search_dict.keys():
                        if k2 not in new_dict.keys():
                            new_dict[k2] = search_dict[k2]
                            if search_dict[k2] != '-1' and 'date' not in k2:
                                new_str = '%s, %s' % (new_str, my.get_str_pair(k2, search_dict[k2]))
                    new_dict['search_string'] = new_str
                    search_dicts.append(new_dict)
                    sd_count = sd_count + 1
        elif lenall == 3:
            list1 = my.finder[alls[0]]
            list2 = my.finder[alls[1]]
            list3 = my.finder[alls[2]]
            for guy1 in list1:
                for guy2 in list2:
                    for guy3 in list3:
                        new_dict = {alls[0]: guy1, alls[1]: guy2, alls[2]: guy3}
                        new_str = '%s, %s, %s' % (my.get_str_pair(alls[0], guy1), my.get_str_pair(alls[1], guy2), my.get_str_pair(alls[2], guy3))
                        for k2 in search_dict.keys():
                            if k2 not in new_dict.keys():
                                new_dict[k2] = search_dict[k2]
                                if search_dict[k2] != '-1' and 'date' not in k2:
                                    new_str = '%s, %s' % (new_str, my.get_str_pair(k2, search_dict[k2]))
                        new_dict['search_string'] = new_str
                        search_dicts.append(new_dict)
                        sd_count = sd_count + 1
        elif lenall == 4:
            list1 = my.finder[alls[0]]
            list2 = my.finder[alls[1]]
            list3 = my.finder[alls[2]]
            list4 = my.finder[alls[3]]
            for guy1 in list1:
                for guy2 in list2:
                    for guy3 in list3:
                        for guy4 in list4:
                            new_dict = {alls[0]: guy1, alls[1]: guy2, alls[2]: guy3, alls[3]: guy4}
                            new_str = '%s, %s, %s, %s' % (my.get_str_pair(alls[0], guy1), my.get_str_pair(alls[1], guy2), my.get_str_pair(alls[2], guy3), my.get_str_pair(alls[3], guy4))
                            for k2 in search_dict.keys():
                                if k2 not in new_dict.keys():
                                    new_dict[k2] = search_dict[k2]
                                    if search_dict[k2] != '-1' and 'date' not in k2:
                                        new_str = '%s, %s' % (new_str, my.get_str_pair(k2, search_dict[k2]))
                            new_dict['search_string'] = new_str
                            search_dicts.append(new_dict)
                            sd_count = sd_count + 1
        if sd_count == 0:
            search_dict['search_string'] = 'Totals'
            search_dicts.append(search_dict)
        return search_dicts


    def make_work_order_tbl(my, sobs, title, focus_col):
        rtbl = Table()
        rtbl.add_attr('border','1')
        rtbl.add_row()
        top = rtbl.add_cell('<u><b>%s</b></u>' % title)
        top.add_attr('colspan', len(sobs))
        top.add_attr('align','center')
        d = {'completion_date': 'Completion Date', 'due_date': 'Due Date', 'count': 'WO Count', 'total_cost': 'Total Cost', 'billable_cost': 'Billable Cost', 'estimated_cost': 'Estimated Cost', 'wh_total_hours': 'Total Work Hours', 'wh_billable_hours': 'Billable Work Hours', 'wh_estimated_hours': 'Estimated Work Hours', 'wh_total_cost': 'Total WH Cost', 'wh_billable_cost': 'Billable WH Cost', 'wh_estimated_cost': 'Estimated WH Cost', 'eq_actual_hours': 'Actual EQ Hours', 'eq_expected_hours': 'Estimated EQ Hours', 'eq_actual_cost': 'Actual EQ Cost', 'eq_expected_cost': 'Estimated EQ Cost', 'status': 'Status', 'login_name': 'Employee', 'group': 'Department'}
        report_cols = ['count','total_cost','billable_cost','estimated_cost','wh_total_hours','wh_billable_hours','wh_estimated_hours','wh_total_cost','wh_billable_cost','wh_estimated_cost','eq_actual_hours','eq_expected_hours','eq_actual_cost','eq_expected_cost']
        rtbl.add_row()
        rtbl.add_cell(d[focus_col].replace(' ','<br/>'))
        totals = {'wo_codes': ''}


        for sob in sobs:
            rtbl.add_cell(sob.get(focus_col).split(' ')[0])
        rtbl.add_cell('TOTAL')
        for guy in report_cols:
            if guy not in totals.keys():
                totals[guy] = 0
            name = d[guy]
            row_class = 'reginfo'
            if 'Hour' in name:
                row_class = 'hourinfo'
            elif 'Cost' in name:
                row_class = 'costinfo'
            color = '#FFFFFF'
            if 'EQ' in name:
                color = '#f8dd9f'
            elif 'WH' in name or 'Work Hour' in name:
                color = '#aff8f0'
            elif 'Price' in name:
                color = '#c6f8af'
            the_row = rtbl.add_row()
            the_row.add_attr('class',row_class)
            the_row.add_style('background-color: %s;' % color)
            rtbl.add_cell(name)
            for sob in sobs:
                val = my.force_0(sob.get(guy))
                dyn = rtbl.add_cell(val)
                totals[guy] = totals[guy] + float(val)
                if guy == 'count':
                    wo_codes = sob.get('wo_codes')
                    if totals['wo_codes'] == '':
                        totals['wo_codes'] = wo_codes
                    else:
                        totals['wo_codes'] = '%s,%s' % (totals['wo_codes'], wo_codes)
                    dyn.add_attr('codes',sob.get('wo_codes'))
                    dyn.set_style(my.style)
                    dyn.add_behavior(my.get_popup_behavior('twog/work_order'))
            if guy == 'count':
                ttl = rtbl.add_cell(int(totals[guy]))
                ttl.add_attr('codes',totals['wo_codes'])
                ttl.set_style(my.style)
                ttl.add_behavior(my.get_popup_behavior('twog/work_order'))
            else:
                ttl = rtbl.add_cell(totals[guy])
        return rtbl

    def get_redo_dates_behavior(my):
        behavior = {'css_class': 'clickish', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                               hashish = {}
                               selectors_el = document.getElementsByClassName('work_order_selectors')[0];
                               selectors = selectors_el.getElementsByTagName('select');
                               for(var r = 0; r < selectors.length; r++){
                                   name = selectors[r].getAttribute('name');
                                   field = name.split('_sel')[0];
                                   hashish[field] = selectors[r].value;
                               }
                               days_past_el = selectors_el.getElementsByClassName('days_past')[0];
                               days_future_el = selectors_el.getElementsByClassName('days_future')[0];
                               date1 = days_past_el.value; 
                               date2 = days_future_el.value;
                               if(isNaN(date1)){
                                   date1 = -15;
                               }else{
                                   date1 = Number(date1) * -1;
                               }
                               if(isNaN(date2)){
                                   date2 = 15;
                               }else{
                                   date2 = Number(date2);
                               }
                               hashish['date1'] = date1;
                               hashish['date2'] = date2; 
                               order_report_cell = document.getElementsByClassName('work_order_report_cell')[0];
                               spt.api.load_panel(order_report_cell, 'reports.dashboard_reports.WorkOrderReportingWdg', hashish);
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                          //alert(err);
                }
         '''}
        return behavior

    def get_sel_change_behavior(my):
        behavior = {'css_class': 'sel_change', 'type': 'change', 'cbjs_action': '''        
                        try{
                               hashish = {}
                               selectors_el = document.getElementsByClassName('work_order_selectors')[0];
                               selectors = selectors_el.getElementsByTagName('select');
                               for(var r = 0; r < selectors.length; r++){
                                   name = selectors[r].getAttribute('name');
                                   field = name.split('_sel')[0];
                                   hashish[field] = selectors[r].value;
                               }
                               days_past_el = selectors_el.getElementsByClassName('days_past')[0];
                               days_future_el = selectors_el.getElementsByClassName('days_future')[0];
                               date1 = days_past_el.value; 
                               date2 = days_future_el.value;
                               if(isNaN(date1)){
                                   date1 = -15;
                               }else{
                                   date1 = Number(date1) * -1;
                               }
                               if(isNaN(date2)){
                                   date2 = 15;
                               }else{
                                   date2 = Number(date2);
                               }
                               hashish['date1'] = date1;
                               hashish['date2'] = date2; 
                               order_report_cell = document.getElementsByClassName('work_order_report_cell')[0];
                               spt.api.load_panel(order_report_cell, 'reports.dashboard_reports.WorkOrderReportingWdg', hashish);
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                          //alert(err);
                }
         '''}
        return behavior

    def get_display(my):
        date1_int = -15
        date1 = my.make_days_difference(date1_int) 
        date2_int = 15
        date2 = my.make_days_difference(date2_int)
        search_dict = {'date1': date1, 'date2': date2, 'login_name': '-1', 'platform': '-1', 'status': '-1', 'group': '-1', 'client_code': '-1'}
        if 'date1' in my.kwargs.keys():
            date1_int = int(my.kwargs.get('date1')) 
            search_dict['date1'] = my.make_days_difference(date1_int)
            date1 = search_dict['date1']
        if 'date2' in my.kwargs.keys():
            date2_int = int(my.kwargs.get('date2'))
            search_dict['date2'] = my.make_days_difference(date2_int)
            date2 = search_dict['date2']
        if 'platform' in my.kwargs.keys():
            search_dict['platform'] = my.kwargs.get('platform')
        if 'login_name' in my.kwargs.keys():
            search_dict['login_name'] = my.kwargs.get('login_name')
        if 'group' in my.kwargs.keys():
            search_dict['group'] = my.kwargs.get('group')
        if 'client_code' in my.kwargs.keys():
            search_dict['client_code'] = my.kwargs.get('client_code')
        if 'status' in my.kwargs.keys():
            search_dict['status'] = my.kwargs.get('status')
        search_dict_clone = search_dict
        search_dicts = my.get_search_dicts(search_dict)


        selectors = Table()
        selectors.add_attr('class','work_order_selectors')
        selectors.add_row()
        dates = Table()
        dates.add_attr('class','work_order_dates')
        dates.add_attr('align','center')
        dates.add_row()
        dates.add_cell('Days into past:')
        date1_str = '%s' % date1_int
        date1_str = date1_str.replace('-','')
        dates.add_cell('<input type="text" value="%s" class="days_past" style="width: 35px;"/>' % date1_str)
        dates.add_cell('Days into future:')
        dates.add_cell('<input type="text" value="%s" class="days_future" style="width: 35px;"/>' % date2_int)
        set_dates = dates.add_cell('<input type="button" value="Set Dates"/>')
        set_dates.add_behavior(my.get_redo_dates_behavior())
        dates_cell =selectors.add_cell(dates)
        dates_cell.add_attr('colspan','8')
        selectors.add_row()

        platform_sel = SelectWdg('platform_sel')
        platform_sel.append_option('Ignore','-1')
        platform_sel.append_option('Show All','ALL')
        platform_sel.append_option('Not Set','0')
        for p in my.all_platforms:
            if p != '0':
                platform_sel.append_option(p,p)
        platform_sel.set_value(search_dict['platform'])
        platform_sel.add_behavior(my.get_sel_change_behavior())
        selectors.add_cell(' Platform: ')
        selectors.add_cell(platform_sel)

        client_sel = SelectWdg('client_code_sel')
        client_sel.append_option('Ignore','-1')
        client_sel.append_option('Show All','ALL')
        client_sel.append_option('Not Set','0')
        for c in my.clients:
            if c[1] != '0':
                client_sel.append_option(c[1],c[0])
        client_sel.set_value(search_dict['client_code'])
        client_sel.add_behavior(my.get_sel_change_behavior())
        selectors.add_cell(' Client: ')
        selectors.add_cell(client_sel)
 
        status_sel = SelectWdg('status_sel')
        status_sel.append_option('Ignore','-1')
        status_sel.append_option('Show All','ALL')
        status_sel.append_option('Not Set','0')
        for s in my.statuses:
            status_sel.append_option(s,s)
        status_sel.set_value(search_dict['status'])
        status_sel.add_behavior(my.get_sel_change_behavior())
        selectors.add_cell(' Status: ')
        selectors.add_cell(status_sel)

        group_sel = SelectWdg('group_sel')
        group_sel.append_option('Ignore','-1')
        group_sel.append_option('Show All','ALL')
        group_sel.append_option('Not Set','0')
        for s in my.all_groups:
            group_sel.append_option(s,s)
        group_sel.set_value(search_dict['group'])
        group_sel.add_behavior(my.get_sel_change_behavior())
        selectors.add_cell(' Dept: ')
        selectors.add_cell(group_sel)

        login_name_sel = SelectWdg('login_name_sel')
        login_name_sel.append_option('Ignore','-1')
        login_name_sel.append_option('Show All','ALL')
        login_name_sel.append_option('Not Set','0')
        for s in my.all_users:
            login_name_sel.append_option(s,s)
        login_name_sel.set_value(search_dict['login_name'])
        login_name_sel.add_behavior(my.get_sel_change_behavior())
        selectors.add_cell(' Employee: ')
        selectors.add_cell(login_name_sel)
        

        wd = Table()
        #wd.add_attr('bgcolor','#0FF000')
        count = 0
        #fyl = open('/var/www/html/source_labels/searches', 'w')
        for s in search_dicts:
            sob_count = 0
            compl_expr = "@SOBJECT(twog/wo_report['completion_date','>=','%s']['completion_date','<=','%s']" % (s['date1'], s['date2'])
            fields = ['platform','client_code','status','group','login_name']
            for f in fields:
                compl_expr = "%s['%s','%s']" % (compl_expr, f, s[f])
            compl_expr = "%s['@ORDER_BY','completion_date'])" % compl_expr
            completion_reports = my.server.eval(compl_expr)
            #fyl.write('%s\n' % compl_expr)
            #fyl.write('%s\n' % completion_reports)
            sob_count = len(completion_reports)
            due_expr = "@SOBJECT(twog/wo_report['due_date','>=','%s']['due_date','<=','%s']" % (my.today, s['date2'])
            for f in fields:
                due_expr = "%s['%s','%s']" % (due_expr, f, s[f])
            due_expr = "%s['@ORDER_BY','due_date'])" % due_expr
            due_reports = my.server.eval(due_expr)
            #fyl.write('%s\n' % due_expr)
            #fyl.write('%s\n' % due_reports)
            sob_count = sob_count + len(due_reports)
            if sob_count > 0:
                extra_str = s['search_string']
                if extra_str != '':
                    extra_str = '%s<br/>' % extra_str
                wd.add_row()
                wd1 = wd.add_cell("WORK ORDERS BY DAY<br/>%sStart Date: %s<br/>&nbsp;&nbsp;End Date: %s" % (extra_str, date1, date2))
                wd1.add_attr('align','center')
                wd1.add_attr('colspan','2')
                wd.add_row()
                wd2 = wd.add_cell(selectors)
                wd2.add_attr('align','center')
                wd2.add_attr('colspan','2')
                wd.add_row()
                completed = wd.add_cell(my.make_work_order_tbl(completion_reports, 'Completion Dates','completion_date'))
                completed.add_attr('valign','top')
                due = wd.add_cell(my.make_work_order_tbl(due_reports, 'Due Dates', 'due_date'))
                due.add_attr('valign','top')
                count = count + 1
        #fyl.close()
        if count == 0:
            wd.add_row()
            wd1 = wd.add_cell("WORK ORDERS BY DAY<br/>Start Date: %s<br/>&nbsp;&nbsp;End Date: %s" % (date1, date2))
            wd1.add_attr('align','center')
            wd1.add_attr('colspan','2')
            wd.add_row()
            wd2 = wd.add_cell(selectors)
            wd2.add_attr('align','center')
            wd2.add_attr('colspan','2')
            wd.add_row()
            wd3 = wd.add_cell('NO REPORTS FOUND')
            wd3.add_attr('colspan','2')
            wd3.add_attr('align','center')
        return wd

class ErrorReportingWdg(BaseRefreshWdg):
    def init(my):
        from client.tactic_client_lib import TacticServerStub
        from pyasm.common import Environment
        my.timestamp = my.make_timestamp()
        my.today = my.timestamp.split(' ')[0]
        this_month_s = my.today.split('-')
        my.this_month = '%s-%s' % (this_month_s[0], this_month_s[1])
        my.server = TacticServerStub.get()
        my.login = Environment.get_login()
        my.user = my.login.get_login()
        my.groups_str = ''
        my.my_groups = my.server.eval("@SOBJECT(sthpw/login_in_group['login','%s'])" % my.user)
        my.style = 'cursor: pointer; text-decoration: underline; color: blue;'
        for mg in my.my_groups:
            if my.groups_str == '':
                my.groups_str = mg.get('login_group')
            else:
                my.groups_str = '%s,%s' % (my.groups_str, mg.get('login_group'))
        my.all_groups = my.server.eval("@GET(sthpw/login_group['@ORDER_BY','login_group].login_group)")
        my.all_users = my.server.eval("@GET(sthpw/login['location','internal']['@ORDER_BY','login'].login)")
        my.all_platforms = my.server.eval("@GET(twog/platform['@ORDER_BY','name'].name)")
        my.client_arr = my.server.eval("@SOBJECT(twog/client['@ORDER_BY','name'])")
        my.clients = []
        my.client_dict = {}
        my.client_codes = []
        for c in my.client_arr:
            my.clients.append([c.get('code'), c.get('name')])
            my.client_dict[c.get('code')] = c.get('name')
            my.client_codes.append(c.get('code'))
        my.error_types = ['Rejected','Internal Error','External Error','Fix Needed']
        my.schedulers = my.server.eval("@GET(sthpw/login_in_group['login_group','in','scheduling|scheduling supervisor'].sthpw/login['@ORDER_BY','login'].login)")
        my.finder = {'group': my.all_groups, 'login_name': my.all_users, 'platform': my.all_platforms, 'client_code': my.client_codes, 'scheduler': my.schedulers, 'error_type': my.error_types} 

    def get_popup_behavior(my, st):
        code_pre = 'ORDER'
        filter = 'simple_order_filter'
        listoid = 'order_list'
        if st == 'twog/work_order':
            code_pre = 'WORK_ORDER'
            filter = 'simple_work_order_filter'
            listoid = 'work_order_list'
        elif st == 'twog/proj':
            code_pre = 'PROJ'
            filter = 'simple_proj_filter'
            listoid = 'proj_list'
        elif st == 'twog/title':
            code_pre = 'TITLE'
            filter = 'simple_title_filter'
            listoid = 'title_list'
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        function correct_codes( s, code_pre ){
                            s_s = s.split(':');
                            s = s_s[s_s.length - 1];
                            slength = s.length;
                            if(slength < 5){
                                for(r = 0; r < 5 - slength; r++){
                                    s = '0' + s;
                                }
                            }
                            if(s.indexOf('TITLE') == -1 && s.indexOf('ORDER') == -1 && s.indexOf('PROJ') == -1){
                                correct_code = code_pre + s;
                            }else{
                                correct_code = s;
                            }
                            return correct_code;
                        } 
                        try{
                           st = '%s';
                           code_pre = '%s';
                           filter = '%s';
                           view = '%s';
                           codes_str = bvr.src_el.getAttribute('codes');
                           codes = codes_str.split(',');
                           search_keys = [];
                           codes_str2 = '';
                           for(var x = 0; x < codes.length; x++){
                               if(codes_str2 == ''){
                                   codes_str2 = correct_codes(codes[x], code_pre);
                               }else{
                                   codes_str2 = codes_str2 + '|' + correct_codes(codes[x], code_pre);
                               }
                           }
                           spt.panel.load_popup('Selected Items', 'tactic.ui.panel.ViewPanelWdg', {'layout': 'fast_table', 'simple_search_view': filter, 'search_type': st, 'view': view, 'element_name': view, 'expression': "@SOBJECT(" + st + "['code','in','" + codes_str2 + "'])"});
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                          //alert(err);
                }
         ''' % (st, code_pre, filter, listoid)}

        return behavior

    def make_timestamp(my):
        import datetime
        now = datetime.datetime.now()
        #print "NOW = %s" % now
        return now.strftime("%Y-%m-%d %H:%M:%S")

    def make_days_difference(my, difference):
        import datetime
        now = datetime.datetime.now()
        then = now + datetime.timedelta(days=difference)
        then_again = then.strftime("%Y-%m-%d %H:%M:%S")
        return then_again 

    def force_0(my, number):
        str = '%s' % number
        if number == 0:
            str = '0'
        if isinstance(number, float):
            str = '%.2f' % number
        return str

    def get_str_pair(my, key, val):
        str_out = ''
        if 'client' in key:
            str_out = 'CLIENT: %s' % my.client_dict[val].upper()
        else:
            str_out = '%s: %s' % (key.upper(), val.upper())
        return str_out

    def get_search_dicts(my, search_dict):
        alls = []
        search_dicts = []
        for key in search_dict.keys():
            if 'date' not in key:
                if search_dict[key] == 'ALL':
                    alls.append(key)
        lenall = len(alls)
        sd_count = 0
        if lenall == 1:
            list = my.finder[alls[0]]
            for guy in list:
                new_dict = {alls[0]: guy}
                new_str = my.get_str_pair(alls[0], guy)
                for k2 in search_dict.keys():
                    if k2 not in new_dict.keys():
                        new_dict[k2] = search_dict[k2]
                        if search_dict[k2] != '-1' and 'date' not in k2:
                            new_str = '%s, %s' % (new_str, my.get_str_pair(k2, search_dict[k2]))
                new_dict['search_string'] = new_str
                search_dicts.append(new_dict)
                sd_count = sd_count + 1
        elif lenall == 2:
            list1 = my.finder[alls[0]]
            list2 = my.finder[alls[1]]
            for guy1 in list1:
                for guy2 in list2:
                    new_dict = {alls[0]: guy1, alls[1]: guy2}
                    new_str = '%s, %s' % (my.get_str_pair(alls[0], guy1), my.get_str_pair(alls[1], guy2))
                    for k2 in search_dict.keys():
                        if k2 not in new_dict.keys():
                            new_dict[k2] = search_dict[k2]
                            if search_dict[k2] != '-1' and 'date' not in k2:
                                new_str = '%s, %s' % (new_str, my.get_str_pair(k2, search_dict[k2]))
                    new_dict['search_string'] = new_str
                    search_dicts.append(new_dict)
                    sd_count = sd_count + 1
        elif lenall == 3:
            list1 = my.finder[alls[0]]
            list2 = my.finder[alls[1]]
            list3 = my.finder[alls[2]]
            for guy1 in list1:
                for guy2 in list2:
                    for guy3 in list3:
                        new_dict = {alls[0]: guy1, alls[1]: guy2, alls[2]: guy3}
                        new_str = '%s, %s, %s' % (my.get_str_pair(alls[0], guy1), my.get_str_pair(alls[1], guy2), my.get_str_pair(alls[2], guy3))
                        for k2 in search_dict.keys():
                            if k2 not in new_dict.keys():
                                new_dict[k2] = search_dict[k2]
                                if search_dict[k2] != '-1' and 'date' not in k2:
                                    new_str = '%s, %s' % (new_str, my.get_str_pair(k2, search_dict[k2]))
                        new_dict['search_string'] = new_str
                        search_dicts.append(new_dict)
                        sd_count = sd_count + 1
        elif lenall == 4:
            list1 = my.finder[alls[0]]
            list2 = my.finder[alls[1]]
            list3 = my.finder[alls[2]]
            list4 = my.finder[alls[3]]
            for guy1 in list1:
                for guy2 in list2:
                    for guy3 in list3:
                        for guy4 in list4:
                            new_dict = {alls[0]: guy1, alls[1]: guy2, alls[2]: guy3, alls[3]: guy4}
                            new_str = '%s, %s, %s, %s' % (my.get_str_pair(alls[0], guy1), my.get_str_pair(alls[1], guy2), my.get_str_pair(alls[2], guy3), my.get_str_pair(alls[3], guy4))
                            for k2 in search_dict.keys():
                                if k2 not in new_dict.keys():
                                    new_dict[k2] = search_dict[k2]
                                    if search_dict[k2] != '-1' and 'date' not in k2:
                                        new_str = '%s, %s' % (new_str, my.get_str_pair(k2, search_dict[k2]))
                            new_dict['search_string'] = new_str
                            search_dicts.append(new_dict)
                            sd_count = sd_count + 1
        if sd_count == 0:
            search_dict['search_string'] = 'Totals'
            search_dicts.append(search_dict)
        return search_dicts

    def make_error_tbl(my, sobs, title, focus_col):
        rtbl = Table()
        rtbl.add_attr('border','1')
        rtbl.add_row()
        top = rtbl.add_cell('<u><b>%s</b></u>' % title)
        top.add_attr('colspan', len(sobs))
        top.add_attr('align','center')
        d = {'date': 'Date', 'count': 'Error Count', 'total_cost': 'Total Cost', 'billable_cost': 'Billable Cost', 'estimated_cost': 'Estimated Cost', 'wh_total_hours': 'Total Work Hours', 'wh_billable_hours': 'Billable Work Hours', 'wh_estimated_hours': 'Estimated Work Hours', 'wh_total_cost': 'Total WH Cost', 'wh_billable_cost': 'Billable WH Cost', 'wh_estimated_cost': 'Estimated WH Cost', 'eq_actual_hours': 'Actual EQ Hours', 'eq_expected_hours': 'Estimated EQ Hours', 'eq_actual_cost': 'Actual EQ Cost', 'eq_expected_cost': 'Estimated EQ Cost', 'status': 'Status', 'login_name': 'Employee', 'group': 'Department'}
        report_cols = ['count','total_cost','billable_cost','estimated_cost','wh_total_hours','wh_billable_hours','wh_estimated_hours','wh_total_cost','wh_billable_cost','wh_estimated_cost','eq_actual_hours','eq_expected_hours','eq_actual_cost','eq_expected_cost']
        rtbl.add_row()
        rtbl.add_cell(d[focus_col].replace(' ','<br/>'))
        totals = {'wo_codes': ''}

        for sob in sobs:
            rtbl.add_cell(sob.get(focus_col).split(' ')[0])
        rtbl.add_cell('TOTAL')
        for guy in report_cols:
            if guy not in totals.keys():
                totals[guy] = 0
            name = d[guy]
            row_class = 'reginfo'
            if 'Hour' in name:
                row_class = 'hourinfo'
            elif 'Cost' in name:
                row_class = 'costinfo'
            color = '#FFFFFF'
            if 'EQ' in name:
                color = '#f8dd9f'
            elif 'WH' in name or 'Work Hour' in name:
                color = '#aff8f0'
            elif 'Price' in name:
                color = '#c6f8af'
            the_row = rtbl.add_row()
            the_row.add_attr('class',row_class)
            the_row.add_style('background-color: %s;' % color)
            rtbl.add_cell(name)
            for sob in sobs:
                val = my.force_0(sob.get(guy))
                totals[guy] = totals[guy] + float(val)
                dyn = rtbl.add_cell(val)
                if guy == 'count':
                    wo_codes = sob.get('wo_codes')
                    if totals['wo_codes'] == '':
                        totals['wo_codes'] = wo_codes
                    else:
                        totals['wo_codes'] = '%s,%s' % (totals['wo_codes'], wo_codes)
                    dyn.add_attr('codes',wo_codes)
                    dyn.set_style(my.style)
                    dyn.add_behavior(my.get_popup_behavior('twog/work_order'))
            if guy == 'count':
                ttl = rtbl.add_cell(int(totals[guy]))
                ttl.add_attr('codes',sob.get('wo_codes'))
                ttl.set_style(my.style)
                ttl.add_behavior(my.get_popup_behavior('twog/work_order'))
            else:
                ttl = rtbl.add_cell(totals[guy])
        return rtbl
            
    def get_redo_dates_behavior(my):
        behavior = {'css_class': 'clickish', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                               hashish = {}
                               selectors_el = document.getElementsByClassName('error_selectors')[0];
                               selectors = selectors_el.getElementsByTagName('select');
                               for(var r = 0; r < selectors.length; r++){
                                   name = selectors[r].getAttribute('name');
                                   field = name.split('_sel')[0];
                                   hashish[field] = selectors[r].value;
                               }
                               days_past_el = selectors_el.getElementsByClassName('days_past')[0];
                               date = days_past_el.value; 
                               if(isNaN(date)){
                                   date = -15;
                               }else{
                                   date = Number(date) * -1;
                               }
                               hashish['date'] = date;
                               error_report_cell = document.getElementsByClassName('error_report_cell')[0];
                               spt.api.load_panel(error_report_cell, 'reports.dashboard_reports.ErrorReportingWdg', hashish);
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                          //alert(err);
                }
         '''}
        return behavior

    def get_sel_change_behavior(my):
        behavior = {'css_class': 'sel_change', 'type': 'change', 'cbjs_action': '''        
                        try{
                               hashish = {}
                               selectors_el = document.getElementsByClassName('error_selectors')[0];
                               selectors = selectors_el.getElementsByTagName('select');
                               for(var r = 0; r < selectors.length; r++){
                                   name = selectors[r].getAttribute('name');
                                   field = name.split('_sel')[0];
                                   hashish[field] = selectors[r].value;
                               }
                               days_past_el = selectors_el.getElementsByClassName('days_past')[0];
                               date = days_past_el.value; 
                               if(isNaN(date)){
                                   date = -15;
                               }else{
                                   date = Number(date) * -1;
                               }
                               hashish['date'] = date;
                               error_report_cell = document.getElementsByClassName('error_report_cell')[0];
                               spt.api.load_panel(error_report_cell, 'reports.dashboard_reports.ErrorReportingWdg', hashish);
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                          //alert(err);
                }
         '''}
        return behavior

    def get_display(my):
        date_int = -15
        date = my.make_days_difference(date_int) 
        search_dict = {'date': date, 'login_name': '-1', 'platform': '-1', 'scheduler': '-1', 'group': '-1', 'client_code': '-1', 'error_type': '-1', }
        if 'date' in my.kwargs.keys():
            date_int = int(my.kwargs.get('date')) 
            search_dict['date'] = my.make_days_difference(date_int)
            date = search_dict['date']
        if 'platform' in my.kwargs.keys():
            search_dict['platform'] = my.kwargs.get('platform')
        if 'login_name' in my.kwargs.keys():
            search_dict['login_name'] = my.kwargs.get('login_name')
        if 'group' in my.kwargs.keys():
            search_dict['group'] = my.kwargs.get('group')
        if 'client_code' in my.kwargs.keys():
            search_dict['client_code'] = my.kwargs.get('client_code')
        if 'scheduler' in my.kwargs.keys():
            search_dict['scheduler'] = my.kwargs.get('scheduler')
        if 'error_type' in my.kwargs.keys():
            search_dict['error_type'] = my.kwargs.get('error_type')
        search_dict_clone = search_dict
        search_dicts = my.get_search_dicts(search_dict)


        selectors = Table()
        selectors.add_attr('class','error_selectors')
        selectors.add_row()
        dates = Table()
        dates.add_attr('class','error_dates')
        dates.add_attr('align','center')
        dates.add_row()
        dates.add_cell('Days into past:')
        date_str = '%s' % date_int
        date_str = date_str.replace('-','')
        dates.add_cell('<input type="text" value="%s" class="days_past" style="width: 35px;"/>' % date_str)
        set_dates = dates.add_cell('<input type="button" value="Set Dates"/>')
        set_dates.add_behavior(my.get_redo_dates_behavior())
        dates_cell =selectors.add_cell(dates)
        dates_cell.add_attr('colspan','8')
        selectors.add_row()

        error_type_sel = SelectWdg('error_type_sel')
        error_type_sel.append_option('Ignore','-1')
        error_type_sel.append_option('Show All','ALL')
        error_type_sel.append_option('Not Set','0')
        for s in my.error_types:
            error_type_sel.append_option(s,s)
        error_type_sel.set_value(search_dict['error_type'])
        error_type_sel.add_behavior(my.get_sel_change_behavior())
        selectors.add_cell(' Error Type: ')
        selectors.add_cell(error_type_sel)

        platform_sel = SelectWdg('platform_sel')
        platform_sel.append_option('Ignore','-1')
        platform_sel.append_option('Show All','ALL')
        platform_sel.append_option('Not Set','0')
        for p in my.all_platforms:
            if p != '0':
                platform_sel.append_option(p,p)
        platform_sel.set_value(search_dict['platform'])
        platform_sel.add_behavior(my.get_sel_change_behavior())
        selectors.add_cell(' Platform: ')
        selectors.add_cell(platform_sel)

        client_sel = SelectWdg('client_code_sel')
        client_sel.append_option('Ignore','-1')
        client_sel.append_option('Show All','ALL')
        client_sel.append_option('Not Set','0')
        for c in my.clients:
            if c[1] != '0':
                client_sel.append_option(c[1],c[0])
        client_sel.set_value(search_dict['client_code'])
        client_sel.add_behavior(my.get_sel_change_behavior())
        selectors.add_cell(' Client: ')
        selectors.add_cell(client_sel)
 
        group_sel = SelectWdg('group_sel')
        group_sel.append_option('Ignore','-1')
        group_sel.append_option('Show All','ALL')
        group_sel.append_option('Not Set','0')
        for s in my.all_groups:
            group_sel.append_option(s,s)
        group_sel.set_value(search_dict['group'])
        group_sel.add_behavior(my.get_sel_change_behavior())
        selectors.add_cell(' Dept: ')
        selectors.add_cell(group_sel)

        login_name_sel = SelectWdg('login_name_sel')
        login_name_sel.append_option('Ignore','-1')
        login_name_sel.append_option('Show All','ALL')
        login_name_sel.append_option('Not Set','0')
        for s in my.all_users:
            login_name_sel.append_option(s,s)
        login_name_sel.set_value(search_dict['login_name'])
        login_name_sel.add_behavior(my.get_sel_change_behavior())
        selectors.add_cell(' Employee: ')
        selectors.add_cell(login_name_sel)

        scheduler_sel = SelectWdg('scheduler_sel')
        scheduler_sel.append_option('Ignore','-1')
        scheduler_sel.append_option('Show All','ALL')
        scheduler_sel.append_option('Not Set','0')
        for s in my.schedulers:
            scheduler_sel.append_option(s,s)
        scheduler_sel.set_value(search_dict['scheduler'])
        scheduler_sel.add_behavior(my.get_sel_change_behavior())
        selectors.add_cell(' Scheduler: ')
        selectors.add_cell(scheduler_sel)

        

        wd = Table()
        count = 0
        for s in search_dicts:
            sob_count = 0
            expr = "@SOBJECT(twog/error_report['date','>=','%s']" % s['date']
            fields = ['platform','client_code','scheduler','error_type','group','login_name']
            for f in fields:
                expr = "%s['%s','%s']" % (expr, f, s[f])
            expr = "%s['@ORDER_BY','date'])" % expr
            reports = my.server.eval(expr)
            sob_count = len(reports)
            if sob_count > 0:
                extra_str = s['search_string']
                if extra_str != '':
                    extra_str = '%s<br/>' % extra_str
                wd.add_row()
                wd1 = wd.add_cell("ERRORS BY DAY<br/>%sStart Date: %s<br/>&nbsp;&nbsp;End Date: Today" % (extra_str, date))
                wd1.add_attr('align','center')
                wd1.add_attr('colspan','2')
                wd.add_row()
                wd2 = wd.add_cell(selectors)
                wd2.add_attr('align','center')
                wd2.add_attr('colspan','2')
                wd.add_row()
                errs = wd.add_cell(my.make_error_tbl(reports, 'Error Dates','date'))
                errs.add_attr('valign','top')
                count = count + 1
        if count == 0:
            wd.add_row()
            wd1 = wd.add_cell("ERRORS BY DAY<br/>Start Date: %s<br/>&nbsp;&nbsp;End Date: Today" % (date))
            wd1.add_attr('align','center')
            wd1.add_attr('colspan','2')
            wd.add_row()
            wd2 = wd.add_cell(selectors)
            wd2.add_attr('align','center')
            wd2.add_attr('colspan','2')
            wd.add_row()
            wd3 = wd.add_cell('NO REPORTS FOUND')
            wd3.add_attr('colspan','2')
            wd3.add_attr('align','center')
        return wd
