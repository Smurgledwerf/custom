__all__ = ["MyPreferencesWdg"]
import tacticenv
from pyasm.common import Environment
from pyasm.biz import *
from pyasm.web import Table, DivWdg
from pyasm.widget import SelectWdg, IconWdg, TextWdg, CheckboxWdg
from pyasm.prod.biz import ProdSetting
from tactic.ui.common import BaseTableElementWdg
from tactic.ui.common import BaseRefreshWdg

class MyPreferencesWdg(BaseRefreshWdg):

    def init(my):
        from client.tactic_client_lib import TacticServerStub
        my.login_obj = Environment.get_login()
        my.login = my.login_obj.get_login()
        my.server = TacticServerStub.get()
        my.login_obj = my.server.eval("@SOBJECT(sthpw/login['login','%s'])" % my.login)[0]
        my.key_dict = {'highlight_notes': 'Highlight Notes - Record What I Have Seen (Slower)]:', 'show_note_counts': 'Show Top Section of Notes, Showing Count Breakdown:'}

    def get_save_preferences(my):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                               login = '%s';
                               var top_el = spt.api.get_parent(bvr.src_el, '.my_preferences_wdg');
                               selects = top_el.getElementsByTagName('select');
                               final_str = ''
                               for(var r = 0; r < selects.length; r++){
                                   if(final_str == ''){
                                       final_str = selects[r].getAttribute('id') + '=' + selects[r].value;
                                   }else{
                                       final_str = final_str + ',' + selects[r].getAttribute('id') + '=' + selects[r].value;
                                   }
                               } 
                               server = TacticServerStub.get();
                               login_sk = server.build_search_key('sthpw/login', login);
                               server.update(login_sk, {'twog_preferences': final_str}, {triggers: false});
                               spt.alert("Your Preferences have been saved. Please wait 5 minutes, then reload your browser tab for changes to take effect.");
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         ''' % (my.login)}
        return behavior

    def get_display(my):
        widget = DivWdg()
        table = Table()
        table.add_attr('class','my_preferences_wdg')
       
        prefs = my.login_obj.get('twog_preferences').split(',')
        for pref in prefs:
            if pref not in [None,'']:
                kv = pref.split('=')
                key = kv[0]
                val = kv[1]
                table.add_row()
                desc = table.add_cell(my.key_dict[key])
                desc.add_attr('nowrap','nowrap')
                this_sel = SelectWdg(key)
                this_sel.add_attr('id',key)
                this_sel.add_style('width: 100px;')
                this_sel.append_option('True','true')
                this_sel.append_option('False','false')
                this_sel.set_value(val)
                table.add_cell(this_sel)
        table.add_row()
        t2 = Table()
        t2.add_row()
        t2.add_cell()
        tc = t2.add_cell('<input type="button" name="Save My Preferences" value="Save My Preferences"/>')
        tc.add_attr('width', '50px')
        tc.add_behavior(my.get_save_preferences())
        t2.add_cell()
        table.add_cell(t2)
        widget.add(table)
        return widget
        
