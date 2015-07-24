__all__ = ["SourceSecurityLaunchWdg","SourceSecurityWdg","SourceSecurityEditWdg"]
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

class SourceSecurityLaunchWdg(BaseTableElementWdg):

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
                                    'user_name': user_name
                          };
			  spt.panel.load_popup('Security Checklist', 'order_builder.source_security_wdg.SourceSecurityWdg', kwargs); 
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                          //alert(err);
                }
         ''' % (source_code, user_name)}
        return behavior

    def get_display(my):
        sobject = None
        code = ''
        show_checks = False
        if 'source_code' in my.kwargs.keys():
            code = str(my.kwargs.get('source_code'))    
        else:
            sobject = my.get_current_sobject()
            code = sobject.get_code()
        if sobject.get_value('high_security') in [True,'T','t','1']:
            show_checks = True
        widget = DivWdg()
        table = Table()
        table.add_attr('width', '50px')
        if show_checks:
            table.add_style('background-color: #ff0000;')
            login = Environment.get_login()
            user_name = login.get_login()
            table.add_row()
            cell1 =  table.add_cell('<img border="0" style="vertical-align: middle" title="Security Checklist" name="Security Checklist" src="/context/icons/32x32/lock_32_01.png">')
            cell1.add_attr('user', user_name)
            launch_behavior = my.get_launch_behavior(code,user_name)
            cell1.add_style('cursor: pointer;')
            cell1.add_behavior(launch_behavior)
        widget.add(table)

        return widget

class SourceSecurityWdg(BaseRefreshWdg):

    def init(my):
        my.x_butt = "<img src='/context/icons/common/BtnKill_Black.gif' title='Delete' name='Delete'/>" 

    def get_change_satisfied(my, check_sk):
        behavior = {'css_class': 'clickme', 'type': 'change', 'cbjs_action': '''        
                        try{
                          var server = TacticServerStub.get();
                          var check_sk = '%s';
                          var check_code = check_sk.split('code=')[1];
                          top_el = document.getElementsByClassName('source_security_wdg')[0];
                          checks = top_el.getElementsByTagName('input');
                          check = null;
                          for(var r = 0; r < checks.length; r++){
                              if(checks[r].name == 'satisfied_' + check_sk){
                                  check = checks[r];
                              }
                          }
                          bool = check.checked;
                          server.update(check_sk, {'satisfied': bool});
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                          //alert(err);
                }
         ''' % (check_sk)}
        return behavior

    def get_killer_behavior(my, sr_sk):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                          if(confirm("Do you really want to delete this requirement?")){
				  var server = TacticServerStub.get();
				  var sr_sk = '%s';
				  top_el = document.getElementsByClassName('source_security_wdg')[0];
				  the_row = top_el.getElementsByClassName('row_' + sr_sk)[0];
				  server.delete_sobject(sr_sk);
				  the_row.style.display = 'none';
                          }
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                          //alert(err);
                }
         ''' % (sr_sk)}
        return behavior

    def get_insert_new_req_from_change(my, source_code, user_name):
        behavior = {'css_class': 'clickme', 'type': 'change', 'cbjs_action': '''        
                        try{
                          var server = TacticServerStub.get();
                          var source_code = '%s';
                          var user_name = '%s';
                          top_el = document.getElementsByClassName('source_security_wdg')[0];
                          req_field = null;
                          fields = top_el.getElementsByTagName('input');
                          for(var r = 0; r < fields.length; r++){
                              if(fields[r].name == 'new_source_req'){
                                  req_field = fields[r]
                              }
                          }
                          req = req_field.value;
                          server.insert('twog/source_req', {'source_code': source_code, 'satisfied': false, 'requirement': req})
                          req_field.value = '';
                          reload_data = {'source_code': source_code, 'user_name': user_name}; 
                          if(top_el.getAttribute('from') == 'insert'){
                              reload_data['from'] = 'insert';
                          }
                          spt.api.load_panel(top_el, 'order_builder.source_security_wdg.SourceSecurityWdg', reload_data); 
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                          //alert(err);
                }
         ''' % (source_code, user_name)}
        return behavior

    def get_insert_new_req(my, source_code, user_name):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                          var server = TacticServerStub.get();
                          var source_code = '%s';
                          var user_name = '%s';
                          top_el = document.getElementsByClassName('source_security_wdg')[0];
                          req_field = null;
                          fields = top_el.getElementsByTagName('input');
                          for(var r = 0; r < fields.length; r++){
                              if(fields[r].name == 'new_source_req'){
                                  req_field = fields[r]
                              }
                          }
                          req = req_field.value;
                          server.insert('twog/source_req', {'source_code': source_code, 'satisfied': false, 'requirement': req})
                          req_field.value = '';
                          reload_data = {'source_code': source_code, 'user_name': user_name}; 
                          if(top_el.getAttribute('from') == 'insert'){
                              reload_data['from'] = 'insert';
                          }
                          spt.api.load_panel(top_el, 'order_builder.source_security_wdg.SourceSecurityWdg', reload_data); 
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
        widget = DivWdg()
        server = TacticServerStub.get()
        allowed_groups = ['admin','audio','billing and accounts receivable','compression','compression supervisor','edeliveries','edit','edit supervisor','executives','it','machine room','machine room supervisor','management','media vault','media vault supervisor','office employees','qc','qc supervisor','sales','sales supervisor','scheduling','scheduling supervisor','senior_staff','streamz','technical services']
        sobject = None
        code = None
        user_name = None 
        do_inserted_msg = False
        table = Table() 
        table.add_attr('class','source_security_wdg')
        if 'source_code' in my.kwargs.keys():
            code = str(my.kwargs.get('source_code'))    
        if code in [None,'']:
            if 'code' in my.kwargs.keys():
                code = my.kwargs.get('code')
        if 'user_name' in my.kwargs.keys():
            user_name = my.kwargs.get('user_name')
        else:
            login = Environment.get_login()
            user_name = login.get_login()
        if 'from' in my.kwargs.keys():
            if my.kwargs.get('from') == 'insert':
                do_inserted_msg = True
                table.add_attr('from','insert')
        if not do_inserted_msg:
            table.add_attr('from','i dunno')
        group = None
        login_in_groups = server.eval("@SOBJECT(sthpw/login_in_group['login','%s']['login_group','not in','user|client'])" % user_name)
        for lg in login_in_groups:
            if not group:
                group = lg.get('login_group')
            if 'supervisor' in lg.get('login_group'): 
                group = lg.get('login_group')
        
        
        checks = server.eval("@SOBJECT(twog/source_req['source_code','%s'])" % code)
        visi = 'display: none;'
        if len(checks) > 0:
            visi = 'display: table-row;';
        if do_inserted_msg:
            table.add_row()
            inserted_row = table.add_cell('<font color="#f0000">!!!Please Enter the High Security Requirements!!!</font>')
            colspan = 2
            if group in allowed_groups:
                colspan = 3
            inserted_row.add_attr('colspan',colspan)
        top_row = table.add_row()
        top_row.add_style(visi)
        if group in allowed_groups:
            table.add_cell(' ')
        table.add_cell(' ')
        table.add_cell('Satisfied?')
        for check in checks:
            check_row = table.add_row()
            check_row.add_attr('class','row_%s' % check.get('__search_key__'))
            if group in allowed_groups:
                killer = table.add_cell(my.x_butt)
                killer.add_style('cursor: pointer;')
                killer.add_behavior(my.get_killer_behavior(check.get('__search_key__')))
            table.add_cell(check.get('requirement'))
            checkbox = CheckboxWdg('satisfied_%s' % check.get('__search_key__'))
            #checkbox.set_persistence()
            if check.get('satisfied'): 
                checkbox.set_value(True)
            else:
                checkbox.set_value(False)
            checkbox.add_behavior(my.get_change_satisfied(check.get('__search_key__')))
            table.add_cell(checkbox)
        
        table.add_row()
        if group in allowed_groups:
            table.add_cell(' ')
        req_text = TextWdg('new_source_req')
        req_text.add_style('width: 500px')
        req_text.add_behavior(my.get_insert_new_req_from_change(code, user_name))
        table.add_cell(req_text)
        add_button = table.add_cell('<input type="button" class="add_req_button" value="+"/>')
        add_button.add_behavior(my.get_insert_new_req(code, user_name))
        if do_inserted_msg:
            table.add_row()
            inserted_row = table.add_cell('<font color="#f0000">!!!Please Enter the High Security Requirements!!!</font>')
            colspan = 2
            if group in allowed_groups:
                colspan = 3
            inserted_row.add_attr('colspan',colspan)
 
        widget.add(table)
        return widget

class SourceSecurityEditWdg(BaseRefreshWdg):

    def init(my):
        nothing = 'true'

    def get_display(my):
        from tactic_client_lib import TacticServerStub
        server = TacticServerStub.get()
        source_code = ''
        source_id = ''
        source_sk = ''
        user_name = ''
        if 'source_code' in my.kwargs.keys():
            source_code = str(my.kwargs.get('source_code'))    
        if 'source_id' in my.kwargs.keys():
            source_id = str(my.kwargs.get('source_id'))
        if 'source_sk' in my.kwargs.keys():
            source_sk = str(my.kwargs.get('source_sk'))
        if 'user_name' in my.kwargs.keys():
            user_name = my.kwargs.get('user_name')
        else:
            login = Environment.get_login()
            user_name = login.get_login()

        source = None
        if source_sk not in [None,'']:
            source = server.get_by_search_key(source_sk)
            source_code = source.get('code')
            #source = server.eval("@SOBJECT(twog/source['code','%s'])" % source_code)[0]
        elif source_id not in [None,'']:
            source = server.eval("@SOBJECT(twog/source['id','%s'])" % source_id)[0]
        elif source_code not in [None,'']:
            source = server.eval("@SOBJECT(twog/source['code','%s'])" % source_code)[0]
        widget = DivWdg()
        table = Table()
        if source.get('high_security'):
            table.add_row()
            table.add_cell('<font color=#ff0000">!!!HIGH SECURITY!!! Make sure you are following the following requirements!</font>')
            table.add_row()
            securitywdg = SourceSecurityWdg(user_name=user_name, source_code=source_code)
            table.add_cell(securitywdg)
            table.add_row()
            table.add_cell('<font color="#ff0000">End Security Requirements</font>') 
        table.add_row()
        editwdg = EditWdg(element_name='general', mode='edit', search_type='twog/source', code=source_code, title='Edit Source', view='edit', widget_key='edit_layout')
        table.add_cell(editwdg)
        widget.add(table)

        return widget
