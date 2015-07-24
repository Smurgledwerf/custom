__all__ = ["InboxTitleWdg"]
import tacticenv
import re, datetime, types, string, os, operator
from pyasm.common import Xml, Container, Environment, Config
from pyasm.search import Search, SearchException, SearchKey
from pyasm.biz import *
from pyasm.web import DivWdg, HtmlElement, Table, Html, SpanWdg, AjaxWdg, WebContainer, AjaxLoader, FloatDivWdg, Widget
from pyasm.widget import CheckboxWdg, SelectWdg

from tactic.ui.common import BaseTableElementWdg
from tactic.ui.common import BaseRefreshWdg

class InboxTitleWdg(BaseRefreshWdg):
    def init(my):
        from client.tactic_client_lib import TacticServerStub
        from pyasm.common import Environment
        my.server = TacticServerStub.get()
        my.number = 0
        my.code = ''
        my.login = Environment.get_login()
        my.user = my.login.get_login()
        my.width = '1000px'
        my.height = '300px'
    
    def get_updater_behavior(my): 
        behavior = {'type': 'mouseleave', 'cbjs_action': '''        
                        function load_again() {
                            var inbox_el = document.getElementsByClassName('inbox_container')[0];
                            var counter_el = document.getElementsByClassName('inbox_counter')[0];
                            var splits = counter_el.innerHTML.split('\\(');
                            var curr_num = Number(splits[1].replace('\\)',''));
                            var new_num = curr_num + 1;
                            spt.api.load_panel(inbox_el, 'inbox.InboxTitleWdg', {element_name: 'general', number:new_num}); 

                            setTimeout("load_again(" + new_num + ")", 1000);
                            return new_num;
                        }
                        var newest = load_again();
                        //window.onload = load_again;
         '''}
        behavior2 = {'type': 'load', 'cbjs_action': '''        
                        function load_again() {
                            var inbox_el = document.getElementsByClassName('inbox_container')[0];
                            var counter_el = document.getElementsByClassName('inbox_counter')[0];
                            var splits = counter_el.innerHTML.split('\\(');
                            var curr_num = Number(splits[1].replace('\\)',''));
                            var new_num = curr_num + 1;
                            spt.api.load_panel(inbox_el, 'inbox.InboxTitleWdg', {element_name: 'general', number:new_num}); 

                            //setTimeout(spt.api.load_panel(inbox_el, 'inbox.InboxTitleWdg', {element_name: 'general', number:new_num}), 1125000);
                            setInterval(spt.api.load_panel(inbox_el, 'inbox.InboxTitleWdg', {element_name: 'general', number:new_num}), 1125000);
                        }
                        load_again();
                        //window.onload = load_again;
         '''}
        return behavior

    def get_display(my):   
        from tactic.ui.widget import SObjectCheckinHistoryWdg
        from pyasm.web import DivWdg, HtmlElement, Table, Html, Widget
        new_number = 0
        if 'number' in my.kwargs.keys():
            new_number = int(my.kwargs.get('number'))
        table = Table()
        table.add_behavior(my.get_updater_behavior())
        table.add_style('width: 100%s;' % '%')
        table.add_row()
        mr_cell = table.add_cell('Inbox (%s)' % new_number)
        mr_cell.add_attr('class','inbox_counter')
        #mr_cell.add_behavior(my.get_updater_behavior())
        return table

