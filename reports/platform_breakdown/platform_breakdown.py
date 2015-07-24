__all__ = ["PlatformBreakdownWdg"]
import tacticenv, os
from pyasm.common import Environment
from pyasm.biz import *
from pyasm.web import Table, DivWdg
from pyasm.widget import SelectWdg, IconWdg, TextWdg, CheckboxWdg
from tactic.ui.common import BaseTableElementWdg
from tactic.ui.common import BaseRefreshWdg
from pyasm.search import SearchType, Search

class PlatformBreakdownWdg(BaseRefreshWdg):
    def init(my):
        from client.tactic_client_lib import TacticServerStub
        from pyasm.common import Environment
        my.server = TacticServerStub.get()

    def get_popup_list(my, codes):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
            try{
               var codes = "%s";
               spt.panel.load_popup('Selected Titles', 'tactic.ui.panel.ViewPanelWdg', {'layout': 'fast_table', 'simple_search_view': 'simple_title_filter', 'search_type': 'twog/title', 'view': 'titles_hl', 'element_name': 'titles_hl', 'expression': "@SOBJECT(twog/title['code','in','" + codes + "'])"});
               }
               catch(err){
                         spt.app_busy.hide();
                         spt.alert(spt.exception.handler(err));
                         //alert(err);
               }
        ''' % codes}
        return behavior

    
    def get_display(my):   
        from datetime import datetime, timedelta
        now = datetime.now()
        start_date = datetime(now.year, now.month, 1)
        next_month = now.month+1
        next_year = now.year
        if next_month > 12:
            next_month = 1
            next_year += 1
        end_date = datetime(next_year, next_month, 1)

        orders = {}
        search = Search("twog/title")
        search.add_filter("expected_delivery_date", start_date, op=">=")
        search.add_filter('expected_delivery_date', end_date, op="<=")
        titles = search.get_sobjects()
        platforms = {}
        for title in titles:
            title_code = title.get_value('code')
            order_code = title.get_value('order_code')
            if order_code not in orders.keys():
                search = Search("twog/order")
                search.add_filter('code',order_code)
                this_order = search.get_sobject()
                if this_order:
                    orders[order_code] = this_order
            if order_code in orders.keys():
                classification = orders[order_code].get_value('classification')
                platform = title.get_value('platform')
                try:
                    platforms[platform][classification]['count'] = platforms[platform][classification]['count'] + 1
                    platforms[platform][classification]['codes'] = '%s|%s' % (platforms[platform][classification]['codes'], title_code)
                except:
                    platforms[platform] = {'Cancelled': {'count': 0, 'codes': ''}, 'In Production': {'count': 0, 'codes': ''}, 'On Hold': {'count': 0, 'codes': ''}, 'Completed': {'count': 0, 'codes': ''}, 'Bid': {'count': 0, 'codes': ''}, 'Master': {'count': 0, 'codes': ''}}
                    platforms[platform][classification]['count'] = platforms[platform][classification]['count'] + 1
                    platforms[platform][classification]['codes'] = title_code
                    pass
        plats = platforms.keys()
        plats.sort()
        classifications = ['Bid','In Production','On Hold','Completed','Master','Cancelled']
        
        explain = Table()
        explain.add_row()
        e1 = explain.add_cell("<b><u>Title's Order Classification Breakdown by Platform</u></b><br/>") 
        e1.add_style('font-size: 20px;')
        widget = DivWdg()
        table = Table()
        table.add_attr('border','1')
        table.add_row()
        sd = '%s' % start_date
        ed = '%s' % end_date
        first = table.add_cell('Expected Delivery Date<br/>Between<br/><u>%s</u> --- <u>%s</u>' % (sd.split(' ')[0], ed.split(' ')[0]))
        first.add_attr('align','center')
       
        for classification in classifications:
            big = table.add_cell('<b>&nbsp;%s&nbsp;</b>' % classification)
        for platform in plats:
            table.add_row()
            big = table.add_cell('<b>%s</b>' % platform)
            for classification in classifications:
                clicker = table.add_cell('<font color="#00688B"><u>%s</u></font>' % platforms[platform][classification]['count'])
                clicker.add_attr('align','center')
                clicker.add_style('cursor: pointer;')
                clicker.add_behavior(my.get_popup_list(platforms[platform][classification]['codes']))
            
        
        
        widget.add(explain)
        widget.add(table)
        return widget

