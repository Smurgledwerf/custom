__all__ = ['ClientViewOpenButtonWdg']
import tacticenv
from tactic.ui.common import BaseTableElementWdg
from pyasm.web import Table, DivWdg

class ClientViewOpenButtonWdg(BaseTableElementWdg):

    def init(my):
        nothing = 'true'
        my.button_image = '/context/icons/oo_prev/stock_navigator_purple.png'

    def get_launch_behavior(my):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                           window.open('http://tactic.2gdigital.com/tactic/twog/client_view', '_blank');
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         '''}
        return behavior

    def get_display(my):
        widget = DivWdg()
        table = Table()
        table.add_row()
        cell1 = table.add_cell('<img border="0" style="vertical-align: middle" title="" src="%s">' % my.button_image)
        launch_behavior = my.get_launch_behavior()
        cell1.add_style('cursor: pointer;')
        cell1.add_behavior(launch_behavior)
        widget.add(table)
        return widget

