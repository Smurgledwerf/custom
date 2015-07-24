__all__ = ['CalendarDeliveryWdg','TitleCalendarLaunchWdg']

from pyasm.web import *
from pyasm.widget import *
from pyasm.search import SearchType, Search
from pyasm.prod.web import *
from pyasm.biz import Project
#from tactic.ui.widget import SObjectCalendarWdg
from tactic.ui.widget import *
from tactic.ui.common import BaseRefreshWdg

class CalendarDeliveryWdg(BaseRefreshWdg):


    def init(my):
        nothing = True

    def get_display(my):
        div = DivWdg()
        #dude = SObjectCalendarWdg(view='table',sobject_display_expr="@GET(twog/title['expected_delivery_date','>','$PREV_MONTH'].sthpw/task)",order_by="bid_end_date",search_type="sthpw/task",mode="simple")
        #dude = ExpectedDeliveryCalendarWdg(login='marcl')
        #dude = ExpectedDeliveryCalendarWdg(login='marcl')
        dude = ExpectedDeliveryCalendarWdg()
        #dude = CalendarWdg()
        div.add(dude)
        return div

class TitleCalendarLaunchWdg(BaseTableElementWdg):

    def init(my):
        nothing = 'true'

    def get_display(my):
        from tactic_client_lib import TacticServerStub
        server = TacticServerStub.get()
        print "MY.KWARGS = %s" % my.kwargs
        title_codes = my.kwargs.get('title_codes').split('|')
        order_titles = {}
        for title_code in title_codes:
            title = server.eval("@SOBJECT(twog/title['code','%s'])" % title_code)
            if title:
                title = title[0]
                order_code = title.get('order_code')
                if order_code not in order_titles.keys():
                    order = server.eval("@SOBJECT(twog/order['code','%s'])" % order_code)[0]
                    order_titles[order_code] = {'order': order, 'titles': []}
                order_titles[order_code]['titles'].append(title)
        widget = DivWdg()
        table = Table()
        for order_code in order_titles.keys():
            table.add_row()
            table.add_cell('ORDER: %s' % order_titles[order_code]['order'].get('name'))
            for title in order_titles[order_code]['titles']:
                table.add_row() 
                title_name = title.get('title')
                if title.get('episode') not in [None,'']:
                    title_name = '%s: %s' % (title_name, title.get('episode'))
                table.add_cell('TITLE: %s' % title_name)
                
        widget.add(table)
        return widget
            
                        
            
        

