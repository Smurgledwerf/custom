__all__ = ["SpecialDeleteWdg"]
import tacticenv
from pyasm.common import Environment
from pyasm.biz import *
from pyasm.web import Table, DivWdg
from tactic.ui.common import BaseTableElementWdg
from tactic.ui.common import BaseRefreshWdg

class SpecialDeleteWdg(BaseTableElementWdg):

    def init(my):
        nothing = 'true'
        my.server = None
        my.x_butt = "<img src='/context/icons/common/BtnKill.gif' title='Delete' name='Delete'/>"

    def get_stub(my):
        from tactic_client_lib import TacticServerStub
        my.server = TacticServerStub.get()
    
    def get_delete_behavior(my, sk):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                          var sk = '%s';
                          var code = sk.split('code=')[1];
                          var st = sk.split('?')[0];
                          var server = TacticServerStub.get();
                          var obj = server.eval("@SOBJECT(" + st + "['code','" + code + "'])")[0];
                          name = '';
                          for(var key in obj){
                              if(name == ''){
                                  if(key == 'process'){
                                      name = obj.process;
                                  }else if(key == 'title'){
                                      name = obj.process;
                                      if(obj.episode != '' && obj.episode != null){
                                          name = name + ': ' + obj.episode;
                                      } 
                                  }else if(key == 'name'){
                                      name = obj.name
                                  }else if(key == 'description'){
                                      if(obj.description != '' && obj.description != null){
                                          name = obj.description;
                                      }
                                  }
                              }
                          }
                          if(name == ''){
                              name = code;
                          }
                          if(confirm('Do you really want to delete "' + name + '" (' + code + ')?')){
                              server.retire_sobject(sk);
                              my_el = document.getElementById('sp_del_' + sk);
                              my_el.innerHTML = "DELETED";
                          }
                          
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                          //alert(err);
                }
         ''' % sk}
        return behavior

    def get_display(my):
        sobject = my.get_current_sobject()
        sk = sobject.get_search_key()
        widget = DivWdg()
        sts_to_perm = {'twog/qc_report_vars': 'compression|qc supervisor|edeliveries'}
        if '-1' not in sk:
            table = Table()
            table.add_attr('width', '50px')
            login = Environment.get_login()
            user_name = login.get_login()
            groups = Environment.get_group_names()
            st = sk.split('?')[0]; 
            perms = sts_to_perm[st] 
            allow = False
            for g in groups:
                if g in perms:
                    allow = True
            if user_name == 'admin':
                allow = True
            if allow:
                table.add_row()
                cell1 =  table.add_cell(my.x_butt)
                cell1.add_attr('id','sp_del_%s' % sk)
                launch_behavior = my.get_delete_behavior(sk)
                cell1.add_style('cursor: pointer;')
                cell1.add_behavior(launch_behavior)
                widget.add(table)
        return widget
