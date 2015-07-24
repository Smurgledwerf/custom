__all__ = ["NoEditSourceViewLauncherWdg"]
import tacticenv
from pyasm.common import Environment
from pyasm.biz import *
from pyasm.web import Table, DivWdg
from pyasm.widget import SelectWdg, IconWdg, TextWdg, CheckboxWdg

from tactic.ui.common import BaseTableElementWdg
from tactic.ui.common import BaseRefreshWdg
from tactic.ui.panel import EditWdg
from tactic.ui.widget.button_new_wdg import ButtonSmallNewWdg, ButtonRowWdg
#from globaller import *
class NoEditSourceViewLauncherWdg(BaseTableElementWdg):

    def init(my):
        nothing = 'true'
        my.server = None

    def get_stub(my):
        from tactic_client_lib import TacticServerStub
        my.server = TacticServerStub.get()
    
    def get_launch_behavior(my, sob_sk, full_name, barcode):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                          spt.app_busy.show("Loading Details...");
                          var sob_sk = '%s';
                          var code = sob_sk.split('code=')[1];
                          var full_name = '%s';
                          var barcode = '%s';
                          var kwargs = {
                                   'element_name': 'general',
                                   'mode': 'view',
                                   'search_type': 'twog/source', 
                                   'code': code, 
                                   'title': full_name,
                                   'view': 'edit',
                                   'widget_key': 'edit_layout', 
                                   'search_key': sob_sk,
                                   'ignore': 'synerg_client|synerg_in_house|synerg_index|synerg_info_dump|synerg_type',
                                   'scroll_height': '1000px',
                                   'make_uneditable': 'true'
                                   };
                          spt.panel.load_popup(full_name + ' Barcode: ' + barcode, 'tactic.ui.panel.EditWdg', kwargs);
                          spt.app_busy.hide();
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                          //alert(err);
                }
         ''' % (sob_sk, full_name, barcode)}
        return behavior

    def get_display(my):
        sob_sk = ''
        title = ''
        episode = ''
        full_name = ''
        barcode = '' 
        if 'search_key' in my.kwargs.keys():
            my.get_stub()
            sob_sk = my.kwargs.get('search_key')
            sobject = my.server.get_by_search_key(sob_sk)
            if sobject:
                code = sobject.get('code')
                title = sobject.get('title')
                episode = sobject.get('episode')
                barcode = sobject.get('barcode')
        else: 
            sobject = my.get_current_sobject()
            code = sobject.get_code()
            sob_sk = sobject.get_search_key()
            title = sobject.get_value('title')
            episode = sobject.get_value('episode')
            barcode = sobject.get_value('barcode')
        full_name = title
        if episode not in [None,'']:
            full_name = '%s: %s' % (full_name, episode)
        widget = DivWdg()
        table = Table()
        table.add_attr('width', '50px')
        table.add_row()
        cell1 =  table.add_cell('<u><b>View All Details</b></u>')
        cell1.add_attr('sk', sob_sk)
        cell1.add_attr('nowrap', 'nowrap')
        cell1.add_style('cursor: pointer;')
        launch_behavior = my.get_launch_behavior(sob_sk, full_name, barcode)
        cell1.add_behavior(launch_behavior)
        widget.add(table)
        #--print "LEAVING OBLW"

        return widget

