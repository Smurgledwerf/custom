__all__ = ["SObjectHistoryLauncherWdg","SObjectHistoryWdg"]
import tacticenv
from pyasm.common import Environment
from pyasm.biz import *
from pyasm.web import Table, DivWdg
from tactic.ui.common import BaseRefreshWdg
from tactic.ui.common import BaseTableElementWdg
from pyasm.search import Search
from pyasm.widget import SelectWdg, IconWdg, TextWdg, CheckboxWdg

class SObjectHistoryLauncherWdg(BaseTableElementWdg):

    def init(my):
        nothing = 'true'

    def get_launch_behavior(my):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                          var my_sk = bvr.src_el.get('sk');
                          var class_name = 'history.history_wdg.SObjectHistoryWdg';
                          kwargs = {
                                           'sk': my_sk
                                   };
                          spt.panel.load_popup('History', class_name, kwargs);
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         '''}
        return behavior

    def get_display(my):
        sk = ''
        if 'search_key' in my.kwargs.keys():
            sk = my.kwargs.get('search_key') 
        else: 
            sobject = my.get_current_sobject()
            sk = sobject.get_search_key()
            
        widget = DivWdg()
        table = Table()
        table.add_attr('width', '50px')
        table.add_row()
        cell1 = table.add_cell('<img border="0" style="vertical-align: middle" title="" src="/context/icons/custom/history_log_button.png">')
        cell1.add_attr('sk', sk)
        launch_behavior = my.get_launch_behavior()
        cell1.add_style('cursor: pointer;')
        cell1.add_behavior(launch_behavior)
        widget.add(table)

        return widget

class SObjectHistoryWdg(BaseRefreshWdg):

    def init(my):
        my.sk = ''
        my.st = ''
        my.code = ''

    def make_history_table(my, db_entry):
        actions = db_entry.split('???]')
        table = Table()
        count = 1
        for action in actions:
            color = '#e4e4e4'
            if count % 2 == 0:
                color = '#cfcfcf'
            if action not in [None,'']:
                r1 = table.add_row()
                r1.add_style('background-color: %s;' % color)
                bits = action.split('x^]')
                login = ''
                timestamp = ''
                others = {}
                for b in bits:
                    if b not in [None,'']:
                        b = b.split('[^x')[1]
                        field = b.split(':')[0]
                        val = b.split(': ')[1]
                        if field == 'LOGIN':
                            login = val
                        elif field == 'TIMESTAMP':
                            timestamp = val.split('.')[0]
                        else:
                            others[field.upper()] = val
                table.add_cell("Login:")
                table.add_cell('&nbsp;&nbsp;&nbsp;&nbsp;')
                lg = table.add_cell(login)
                lg.add_attr('nowrap','nowrap')
                r2 = table.add_row()
                r2.add_style('background-color: %s;' % color)
                table.add_cell("Time:")
                table.add_cell('&nbsp;&nbsp;&nbsp;&nbsp;')
                ts = table.add_cell(timestamp)
                ts.add_attr('nowrap','nowrap')
                ok = others.keys()
                for o in ok:
                    r3 = table.add_row()
                    r3.add_style('background-color: %s;' % color)
                    table.add_cell(o)
                    table.add_cell('&nbsp;&nbsp;&nbsp;&nbsp;')
                    table.add_cell(others[o])
#                if count < len(actions) - 1:
#                    table.add_row()
#                    table.add_cell("<HR/>")
                count = count + 1
        return table

    def get_display(my):
        my.sk = my.kwargs.get('sk')
        splits1 = my.sk.split('code=')
        splits2 = my.sk.split('?')
        my.code = splits1[1]
        my.st = splits2[0]
        obj_search = Search(my.st)
        obj_search.add_filter('code',my.code)
        obj = obj_search.get_sobject()
        new_table = 'No History'
        if obj:
            column_info = obj.get_column_info()
            if 'history_log' in column_info.keys():
                history_log = obj.get_value('history_log')
                new_table = my.make_history_table(history_log)
                
        
        widget = DivWdg()
        table = Table()
        table.add_row()
        table.add_cell(new_table)
        widget.add(table)
        return widget


