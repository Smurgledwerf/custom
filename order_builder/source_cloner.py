__all__ = ["SourceCloneLauncherWdg"]
import tacticenv
from pyasm.common import Environment
from pyasm.biz import *
from pyasm.web import Table, DivWdg
from pyasm.widget import SelectWdg, IconWdg, TextWdg, CheckboxWdg

from tactic.ui.common import BaseTableElementWdg
from tactic.ui.common import BaseRefreshWdg
from tactic.ui.panel import EditWdg
from custom_piper import CustomPipelineToolWdg
from tactic.ui.widget.button_new_wdg import ButtonSmallNewWdg, ButtonRowWdg

class  SourceCloneLauncherWdg(BaseTableElementWdg):
    '''Launches a popup with the CustomSaatchiCheckin widget '''

    def init(my):
        nothing = 'true'

    def get_launch_behavior(my, source_code, user_name):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                          var server = TacticServerStub.get();
                          var source_code = '%s';
                          var user_name = '%s';
                          kwargs = {
                                    'source_code': source_code,
                                    'clone': 'true',
                                    'user_name': user_name
                          };
                          spt.tab.add_new('create_new_source_ob', 'Create New Source', 'order_builder.order_builder.NewSourceWdg', kwargs);
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                          //alert(err);
                }
         ''' % (source_code, user_name)}
        return behavior

    def get_display(my):
        from tactic_client_lib import TacticServerStub
        sobject = None
        code = ''
        if 'source_code' in my.kwargs.keys():
            code = str(my.kwargs.get('source_code'))    
        else:
            sobject = my.get_current_sobject()
            code = sobject.get_code()
        widget = DivWdg()
        table = Table()
        table.add_attr('width', '50px')
        login = Environment.get_login()
        user_name = login.get_login()
        table.add_row()
        cell1 =  table.add_cell('<img border="0" style="vertical-align: middle" title="Clone Source" name="Clone Source" src="/context/icons/silk/star.png">')
        cell1.add_attr('user', user_name)
        launch_behavior = my.get_launch_behavior(code,user_name)
        cell1.add_style('cursor: pointer;')
        cell1.add_behavior(launch_behavior)
        widget.add(table)

        return widget
