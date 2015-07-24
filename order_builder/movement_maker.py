__all__ = ["MovementLauncherWdg","MovementMakerWdg","SourceAddWdg","SourcesListWdg","MovementSourceEditWdg","MovementTwogEasyCheckinWdg","OutsideBarcodesWdg","MovementScripts"]
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

class MovementLauncherWdg(BaseTableElementWdg):

    def init(my):
        nothing = 'true'

    def get_launch_behavior(my, movement_name):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                          var server = TacticServerStub.get();
                          var movement_name = '%s';
                          var my_sk = bvr.src_el.get('sk');
                          var my_code = my_sk.split('code=')[1];
                          var my_st = bvr.src_el.get('search_type');
                          var my_user = bvr.src_el.get('user');
                          var class_name = 'order_builder.movement_maker.MovementMakerWdg';
                          kwargs = {
                                           'movement_code': my_code,
                                           'sk': my_sk,
                                           'user': my_user
                                   };
                          //spt.panel.load_popup('Custom Checkin to ' + my_code, class_name, kwargs);
                          spt.tab.add_new('order_builder_' + my_code, 'Movement Tracker ' + movement_name, class_name, kwargs);
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                          //alert(err);
                }
         ''' % movement_name}
        return behavior

    def get_display(my):
        from tactic_client_lib import TacticServerStub
        sobject = my.get_current_sobject()
        code = sobject.get_code()
        movement_name = sobject.get_value('name')
        sob_sk = sobject.get_search_key()
        sob_st = sobject.get_search_type().split('?')[0]
        sob_id = sobject.get_value('id')
        widget = DivWdg()
        table = Table()
        table.add_attr('width', '50px')
        login = Environment.get_login()
        user_name = login.get_login()
        table.add_row()
        cell1 =  table.add_cell('<img border="0" style="vertical-align: middle" title="" src="/context/icons/silk/email.png">')
        cell1.add_attr('sk', sob_sk)
        cell1.add_attr('search_type', sob_st)
        cell1.add_attr('user', user_name)
        launch_behavior = my.get_launch_behavior(movement_name)
        cell1.add_style('cursor: pointer;')
        cell1.add_behavior(launch_behavior)
        widget.add(table)

        return widget

class MovementMakerWdg(BaseRefreshWdg):
    def init(my):
        from client.tactic_client_lib import TacticServerStub
        from pyasm.common import Environment
        my.server = TacticServerStub.get()
        my.login = Environment.get_login()
        my.user = my.login.get_login()
        my.movement_sk = ''
        my.movement_id = ''
        my.movement_code = ''

    def get_submit_behavior(my, movement_code):    
        behavior = {
        'type': 'click_up',
        'cbjs_action': '''
            var server = TacticServerStub.get();

            //toggle triggering boolean on and off here
            var movement_code = '%s';
            sk = server.build_search_key('twog/movement', movement_code);
            server.update(sk, {'submit_notification': 'true'});
            server.update(sk, {'submit_notification': 'false'});
            var top_tbl = document.getElementsByClassName('movement_maker_top')[0];
            spt.tab.top = top_tbl.getParent(".spt_tab_top");
            //spt.tab.top = bvr.src_el.getParent(".spt_tab_top");
            var top = spt.tab.top;
            var headers = spt.tab.get_headers();
            if (headers.length == 1) {
                return;
            }

            var headers = document.getElementsByClassName("spt_tab_header");
            header = null;
            for(var r = 0; r < headers.length; r++){
                if(headers[r].getAttribute("spt_element_name").indexOf(movement_code) != -1){
                    header = headers[r];
                }
            } 
            var element_name = header.getAttribute("spt_element_name");
            header.destroy();

            var content_top = top.getElement(".spt_tab_content_top");
            var contents = content_top.getElements(".spt_tab_content");
            for (var i = 0; i < contents.length; i++ ) {
                var content = contents[i];
                if (content.getAttribute("spt_element_name") == element_name) {
                    content.destroy();
                    break;
                }
            }

            // make the last one active
            var headers = spt.tab.get_headers();
            var last = headers[headers.length - 1].getAttribute("spt_element_name");
            spt.tab.select(last);
        ''' % movement_code
        }
        return behavior

    def get_display(my):   
        if 'movement_code' in my.kwargs.keys():
            my.movement_code = str(my.kwargs.get('movement_code'))
            mov_expr = "@SOBJECT(twog/movement['code','%s'])" % my.movement_code
            mo = my.server.eval(mov_expr)
            if len(mo) > 0:
                mo = mo[0]
                my.movement_sk = mo.get('__search_key__')
                my.movement_id = mo.get('id')
        #my.movement_code ='MOVEMENT00021' 
        insert_wdg = None
        if my.movement_code != '':
            insert_wdg = EditWdg(element_name='general', mode='edit', search_type='twog/movement', code=my.movement_code, title='Edit Movement',view='edit', widget_key='edit_layout')
        else:
            insert_wdg = EditWdg(element_name='general', mode='insert', search_type='twog/movement', title='Create Movement',view='insert', widget_key='edit_layout', cbjs_insert_path='movement/refresh_from_create')
        table = Table()
        table.add_attr('class', 'movement_maker_top');
        table.add_attr('id', 'movement_maker_top_%s' % my.movement_code);
        table.add_attr('movement_id',my.movement_id)
        table.add_attr('movement_sk',my.movement_sk)
        table.add_attr('movement_code',my.movement_code)
        table.add_row()
        ins_cell = table.add_cell(insert_wdg)
        ins_cell.add_attr('class','movement_edit_top')
        source_add_wdg = SourceAddWdg(movement_code=my.movement_code)
        source_add_row = table.add_row()
        source_add_row.add_attr('class','source_add_row')
        if my.movement_code in ['',None]:
            source_add_row.add_style('display: none;')
        source_add_cell = table.add_cell(source_add_wdg)
        source_add_cell.add_attr('class','source_add_cell')
        source_add_cell.add_attr('align','center')
        sources_list = SourcesListWdg(movement_code=my.movement_code)
        sources_row = table.add_row()
        sources_row.add_attr('class','sources_row')
        if my.movement_code in ['',None]:
            sources_row.add_style('display: none;')
        sources_list_cell = table.add_cell(sources_list)
        sources_list_cell.add_attr('class','sources_list_cell')
        sources_list_cell.add_attr('align','center')
        submit_row = table.add_row()
        sub_tbl = Table()
        sub_tbl.add_row()
        submit_pad1 = sub_tbl.add_cell(' ')
        submit_pad1.add_style('width: 50%s;' % '%')
        submit_butt = sub_tbl.add_cell('<input type="button" value="Submit"/>')
        submit_butt.add_attr('align','center')
        submit_butt.add_behavior(my.get_submit_behavior(my.movement_code))
        submit_pad2 = sub_tbl.add_cell(' ')
        submit_pad2.add_style('width: 50%s;' % '%')
        table.add_cell(sub_tbl)
        return table
        
class SourceAddWdg(BaseRefreshWdg):
    def init(my):
        from client.tactic_client_lib import TacticServerStub
        from pyasm.common import Environment
        my.server = TacticServerStub.get()
        my.login = Environment.get_login()
        my.user = my.login.get_login()
        my.movement_code = ''

    def get_on_load_js(my):
        behavior =  {
            'type': 'load',
            'cbjs_action': '''
                var top_el = spt.api.get_parent(bvr.src_el, '.movement_maker_top');
                txt_el = top_el.getElementById('source_barcode_insert');
                txt_el.focus();
            '''
            } 
        return behavior        
    
    def get_display(my):   
        table = Table()
        my.movement_code = my.kwargs.get('movement_code')
        table.add_attr('class', 'movement_add_source')
        table.add_attr('movement_id','')
        table.add_attr('movement_sk','')
        table.add_attr('movement_code','')
        top_row = table.add_row()
        top_row.add_style('background-color: #eaeaea;')
        if my.movement_code not in ['',None]:
            ms = MovementScripts(movement_code=my.movement_code)
            barcode_text_wdg = TextWdg('source_barcode_insert')
            barcode_text_wdg.add_attr('id','source_barcode_insert')
            barcode_text_wdg.add_behavior(ms.get_barcode_insert_behavior())
            table.add_cell('Barcode: ')
            table.add_cell(barcode_text_wdg)

        widget = DivWdg()
        widget.add(table)
        if my.movement_code not in ['',None]:
            widget.add_behavior(my.get_on_load_js())
        return widget

class SourcesListWdg(BaseRefreshWdg):
    def init(my):
        from client.tactic_client_lib import TacticServerStub
        from pyasm.common import Environment
        my.server = TacticServerStub.get()
        my.login = Environment.get_login()
        my.user = my.login.get_login()
        my.movement_code = ''
    
    def get_display(my):   
        table = Table()
        table.add_attr('border','1')
        table.add_style('border-width: 2px;')
        my.movement_code = my.kwargs.get('movement_code')
        table.add_attr('class', 'movement_sources_list')
        table.add_attr('movement_id','')
        table.add_attr('movement_sk','')
        table.add_attr('movement_code','')
        title_row = table.add_row()
        title_row.add_style('background-color: #6c7b8f;')
        title_cell = table.add_cell('<u><b>Sources Attached to This Movement</b></u>')
        title_cell.add_attr('colspan','6')
        title_cell.add_attr('align','center')
        title_cell.add_style('font-size: 110%s;' % '%')
        top_row = table.add_row()
        top_row.add_style('background-color: #90a0b5;')
        table.add_cell('<b>Source Name</b>')
        table.add_cell('<b>Barcode</b>')
        table.add_cell('<b>Source Type</b>')
        table.add_cell('<b>Client</b>')
        table.add_cell('')
        table.add_cell('')
        if my.movement_code not in ['',None]:
            ms = MovementScripts(movement_code=my.movement_code)
            atm_expr = "@SOBJECT(twog/asset_to_movement['movement_code','%s'])" % my.movement_code
            atms = my.server.eval(atm_expr)
            if len(atms) > 0:
                for atm in atms:
                    source_expr = "@SOBJECT(twog/source['code','%s'])" % (atm.get('source_code'))
                    sources = my.server.eval(source_expr)
                    if len(sources) > 0:
                        source = sources[0]
                        table.add_row()
                        l_edit = None
                        if not source.get('high_security'):
                            #print "SOURCE NOT HIGH: %s" % source.get('title')
                            l_edit = table.add_cell('<u><b>%s</b></u>' % source.get('title'))
                        else:
                            #print "SOURCE HIGH: %s" % source.get('title')
                            l_edit = table.add_cell('<font color="#ff0000"><u><b>!!!%s!!!</b></u></font>' % source.get('title'))
                        l_edit.add_attr('nowrap','nowrap')
                        l_edit.add_style('font-color: blue;')
                        l_edit.add_behavior(ms.get_launch_source_edit_behavior(source.get('code'), source.get('high_security')))
                        table.add_cell(source.get('barcode'))
                        table.add_cell(source.get('source_type'))
                        #print "SOURCE CLIENT CODE = %s" % source.get('client_code')
                        client_name_expr = "@GET(twog/client['code','%s'].name)" % source.get('client_code')
                        #print "CLIENT NAME EXPR = %s" % client_name_expr
                        client_name = 'Source Has No Client Code'
                        if source.get('client_code') not in [None,'']:
                            client_name = my.server.eval("@GET(twog/client['code','%s'].name)" % source.get('client_code'))[0]
                        table.add_cell(client_name)
                        rem = Table()
                        rem.add_row()
                        r1 = rem.add_cell(' ')
                        r1.add_attr('width','100%s' % '%')
                        remove_butt = rem.add_cell('<input type="button" value="Remove"/>')
                        remove_butt.add_behavior(ms.get_remove_source_behavior(atm.get('code')))
                        r2 = rem.add_cell(' ')
                        r2.add_attr('width','100%s' % '%')
                        table.add_cell(rem)
                        rem2 = Table()
                        rem2.add_row()
                        r12 = rem2.add_cell(' ')
                        r12.add_attr('width','100%s' % '%')
                        remove_butt = rem2.add_cell('<input type="button" value="Outside Barcodes"/>')
                        remove_butt.add_behavior(ms.get_launch_attach_outside_barcodes_behavior(source.get('code')))
                        r22 = rem2.add_cell(' ')
                        r22.add_attr('width','100%s' % '%')
                        table.add_cell(rem2)
                        
        return table

class MovementTwogEasyCheckinWdg(BaseRefreshWdg):
    def init(my):
        from client.tactic_client_lib import TacticServerStub
        from pyasm.common import Environment
        my.code = ''
        my.sk = ''
        my.source_contexts = []
        my.movement_code = ''

    def get_display(my):   
        from pyasm.prod.biz import ProdSetting
        my.code = str(my.kwargs.get('code'))
        my.sk = str(my.kwargs.get('sk'))
        my.movement_code = str(my.kwargs.get('movement_code'))
        my.source_contexts = ProdSetting.get_value_by_key('source_contexts').split('|')
        ms = MovementScripts(movement_code=my.movement_code)
        table = Table()
        table.add_attr('class','movement_twog_easy_checkin')
        table.add_attr('width','100%s' % '%')
        table.add_row()
        title_bar = table.add_cell('<b><u>Checkin New File</u></b>')
        title_bar.add_attr('align','center')
        title_bar.add_attr('colspan','4')
        title_bar.add_style('font-size: 110%ss' % '%')
        processes_sel = SelectWdg('source_process_select')
        for ctx in my.source_contexts:
            processes_sel.append_option(ctx,ctx)
        table.add_row()
        mini0 = Table()
        mini0.add_row()
        mini0.add_cell('Checkin Context: ')
        mini0.add_cell(processes_sel)
        table.add_cell(mini0)
        mini1 = Table()
        mini1.add_row()
        file_holder = mini1.add_cell(' ')
        file_holder.add_attr('width','100%s' % '%')
        file_holder.add_attr('align','center')
        file_holder.add_attr('class','file_holder')
        button = mini1.add_cell('<input type="button" value="Browse"/>')
        button.add_attr('align','right')
        button.add_style('cursor: pointer;')
        button.add_behavior(ms.get_easy_checkin_browse_behavior())
        big_button = mini1.add_cell('<input type="button" value="Check In" class="easy_checkin_commit" disabled/>')
        big_button.add_style('cursor: pointer;')
        big_button.add_behavior(ms.get_easy_checkin_commit_behavior(my.sk))
        table.add_cell(mini1)
        return table

class MovementSourceEditWdg(BaseRefreshWdg): 

    def init(my):
        from client.tactic_client_lib import TacticServerStub
        from pyasm.common import Environment
        my.server = TacticServerStub.get()
        my.code = ''
        my.sk = ''
        my.movement_code = ''
    def get_display(my):   
        from tactic.ui.widget import SObjectCheckinHistoryWdg
        from source_security_wdg import SourceSecurityWdg
        my.code = str(my.kwargs.get('source_code'))
        my.sk = my.server.build_search_key('twog/source',my.code)
        my.movement_code = str(my.kwargs.get('movement_code'))
        security = my.kwargs.get('security')
        edit_wdg = EditWdg(element_name='general', mode='edit', search_type='twog/source', code=my.code,\
                title='Modify Source',view='edit', widget_key='edit_layout', cbjs_edit_path='movement/reload_movement_list')
        table = Table()
        table.add_attr('class','movement_source_edit_top')
        if security:
            table.add_row()
            table.add_cell('<font color="#ff0000">!!!HIGH SECURITY!!! Make sure you are following the following requirements!</font>')
            table.add_row()
            req_list = SourceSecurityWdg(source_code=my.code)
            table.add_cell(req_list)
            table.add_row()
            table.add_cell('<font color="#ff0000">End Security Requirements</font>')
        table.add_row()
        edit_source_cell = table.add_cell(edit_wdg)
        edit_source_cell.add_attr('class','movement_edit_source_cell')
        edit_source_cell.add_attr('valign','top')
        table.add_row()
        
        history = SObjectCheckinHistoryWdg(search_key=my.sk)
        history_cell = table.add_cell(history)
        history_cell.add_attr('class','movement_history_source_cell')
        table.add_row()

        checkin = MovementTwogEasyCheckinWdg(code=my.code,sk=my.sk,movement_code=my.movement_code)
        checkin_cell = table.add_cell(checkin)
        checkin_cell.add_attr('class','movement_checkin_source_cell')
        checkin_cell.add_attr('width','100%s' % '%')
        checkin_cell.add_attr('align','center')

        return table

class OutsideBarcodesWdg(BaseRefreshWdg): 

    def init(my):
        from client.tactic_client_lib import TacticServerStub
        from pyasm.common import Environment
        my.server = TacticServerStub.get()
        my.code = ''
        my.sk = ''
        my.movement_code = ''
    def get_display(my):   
        from tactic.ui.widget import SObjectCheckinHistoryWdg
        my.code = str(my.kwargs.get('source_code'))
        my.sk = my.server.build_search_key('twog/source',my.code)
        my.movement_code = str(my.kwargs.get('movement_code'))
        ms = MovementScripts(movement_code=my.movement_code)
        clients_expr = "@SOBJECT(twog/client['@ORDER_BY','name desc'])" 
        clients = my.server.eval(clients_expr)
        client_sel = '<select class="REPLACE_ME"><option value="">--Select--</option>'
        for client in clients:
            client_sel = '%s<option value="%s">%s</option>' % (client_sel, client.get('code'), client.get('name'))
        client_sel = '%s</select>' % client_sel
        existing_expr = "@SOBJECT(twog/outside_barcode['source_code','%s'])" % my.code
        existing = my.server.eval(existing_expr)
        count = 0
        table = Table()
        table.add_attr('class','movement_outside_barcodes')
        for obc in existing:
            table.add_row()
            barcode_text_wdg = TextWdg('outside_barcode_insert_%s' % count)
            barcode_text_wdg.set_value(obc.get('barcode'))
            barcode_text_wdg.add_attr('curr_code',obc.get('code'))
            table.add_cell(barcode_text_wdg)
            new_sel = client_sel
            new_sel2 = new_sel.replace('REPLACE_ME','outside_client_%s' % count)
            found = new_sel2.find('"%s"' % obc.get('client_code'))
            if found > 0:
                part1 = new_sel2[:found]
                part2 = new_sel2[found:]
                found2 = part2.find('>')
                if found2 > 0:
                    good2 = part2[found2:]
                    new_sel2 = '%s"%s" selected="selected"%s' % (part1, obc.get('client_code'),good2)
            table.add_cell(new_sel2)
            count = count + 1
        additional_count = [1, 2, 3, 4, 5]
        for n in additional_count:
            table.add_row()
            barcode_text_wdg = TextWdg('outside_barcode_insert_%s' % count)
            barcode_text_wdg.add_attr('curr_code','')
            table.add_cell(barcode_text_wdg)
            new_sel = client_sel
            new_sel = new_sel.replace('REPLACE_ME','outside_client_%s' % count)
            table.add_cell(new_sel)
            count = count + 1
        table.add_row()
        save_tbl = Table()
        save_tbl.add_row()
        s1 = save_tbl.add_cell(' ')
        s1.add_attr('width','100%s' % '%')
        save_cell = table.add_cell('<input type="button" value="Save All"/>')
        save_cell.add_attr('align','center')
        save_cell.add_behavior(ms.get_save_outside_barcodes_behavior(my.code))
        s2 = save_tbl.add_cell(' ')
        s2.add_attr('width','100%s' % '%')
        ss = table.add_cell(save_tbl)
        ss.add_attr('colspan','2')
        ss.add_attr('align','center')
        return table

class MovementScripts(BaseRefreshWdg):
    def init(my):
        from client.tactic_client_lib import TacticServerStub
        from pyasm.common import Environment
        my.server = TacticServerStub.get()
        my.login = Environment.get_login()
        my.user = my.login.get_login()
        my.movement_code = my.kwargs.get('movement_code')
    
    def get_launch_attach_outside_barcodes_behavior(my, source_code):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                          var server = TacticServerStub.get();
                          var source_code = '%s';
                          spt.panel.load_popup('Outside Barcodes', 'order_builder.OutsideBarcodesWdg', {'source_code': source_code});
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                          //alert(err);
                }
         ''' % (source_code)}
        return behavior

    def get_save_outside_barcodes_behavior(my, source_code):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        function oc(a){
                            var o = {};
                            for(var i=0;i<a.length;i++){
                                o[a[i]]='';
                            }
                            return o;
                        }
                        try{
                          var server = TacticServerStub.get();
                          var source_code = '%s';
                          var movement_code = '%s';
                          var top_el = spt.api.get_parent(bvr.src_el, '.movement_outside_barcodes');
                          var inps = top_el.getElementsByTagName('input');
                          var pairs = {};
                          var seen = [];
                          for(var r = 0; r < inps.length; r++){
                              if(inps[r].getAttribute('type') == 'text'){
                                  if(inps[r].value != ''){
                                      var name = inps[r].getAttribute('name');
                                      var num = Number(name.split('utside_barcode_insert_')[1]);
                                      if(!(num in oc(seen))){
                                          seen.push(num);
                                          pairs[num] = [];
                                      }
                                      pairs[num].push(inps[r].getAttribute('curr_code'));
                                      pairs[num].push(inps[r].value);
                                  }
                              }
                          }
                          sels = top_el.getElementsByTagName('select');
                          for(var r = 0; r < sels.length; r++){
                              if(sels[r].value != ''){
                                  var meclass = sels[r].getAttribute('class');
                                  var num = Number(meclass.split('utside_client_')[1]);
                                  if(num in oc(seen)){
                                      pairs[num].push(sels[r].value);
                                  }
                              }
                          }
                          for(var r = 0; r < seen.length; r++){
                              if(pairs[r][0] == ''){
                                  server.insert('twog/outside_barcode',{'client_code': pairs[r][2], 'barcode': pairs[r][1], 'source_code': source_code});
                              }else{
                                  ob_sk = server.build_search_key('twog/outside_barcode', pairs[r][0]);
                                  server.update(ob_sk, {'client_code': pairs[r][2], 'barcode': pairs[r][1], 'source_code': source_code});
                              }
                          }
                          spt.popup.close(spt.popup.get_popup(bvr.src_el));
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                          //alert(err);
                }
         ''' % (source_code, my.movement_code)}
        return behavior

    def get_launch_source_edit_behavior(my, source_code, security):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                          var server = TacticServerStub.get();
                          var source_code = '%s';
                          var security = '%s';
                          var movement_code = '%s';
                          spt.panel.load_popup('Source Portal', 'order_builder.MovementSourceEditWdg', {'source_code': source_code, 'movement_code': movement_code, 'security': security});
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                          //alert(err);
                }
         ''' % (source_code, security, my.movement_code)}
        return behavior

    def get_remove_source_behavior(my, atm_code):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                           var server = TacticServerStub.get();
                           var atm_code = '%s';
                           var movement_code = '%s';
                           if(confirm("Are you sure you want to remove this item from the delivery?")){
                               server.retire_sobject(server.build_search_key('twog/asset_to_movement',atm_code));
                               var top_el = spt.api.get_parent(bvr.src_el, '.movement_maker_top');
                               sources_list_cell = top_el.getElementsByClassName('sources_list_cell')[0];
                               spt.api.load_panel(sources_list_cell, 'order_builder.SourcesListWdg', {movement_code: movement_code});
                           }
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                          //alert(err);
                }
         ''' % (atm_code, my.movement_code)}
        return behavior

    def get_barcode_insert_behavior(my):
        behavior = {'css_class': 'clickme', 'type': 'change', 'cbjs_action': '''        
                        function oc(a){
                            var o = {};
                            for(var i=0;i<a.length;i++){
                                o[a[i]]='';
                            }
                            return o;
                        }
                        try{
                          var server = TacticServerStub.get();
                          movement_code = '%s';
                          var top_el = spt.api.get_parent(bvr.src_el, '.movement_maker_top');
                          barcode_start = bvr.src_el.value;
                          barcodes = barcode_start.split(',');
                          atm_expr = "@GET(twog/asset_to_movement['movement_code','" + movement_code + "'].source_code)";
                          atm_sources = server.eval(atm_expr);
                          for(var r = 0; r < barcodes.length; r++){
				  source_expr = "@GET(twog/source['barcode','" + barcodes[r] + "'].code)";
				  sources = server.eval(source_expr);
				  if(sources.length > 1){
				      alert('Something is wrong with inventory. There are ' + sources.length + ' sources with barcode "' + barcodes[r] + '"');
				      bvr.src_el.value = '';
				  }else if(sources.length > 0){
				      source = sources[0];
				      if(source in oc(atm_sources)){
					  alert('This source has already been added to the movement.');
				      }else{ 
					  server.insert('twog/asset_to_movement', {movement_code: movement_code, source_code: source, barcode: barcodes[r]});
				      }
				  }else{
				      kwargs = {
						'barcode': barcodes[r],
                                                'default': {'barcode': barcodes[r]},
						'element_name': 'general',
						'mode': 'insert',
						'search_type': 'twog/source',
						'title': 'Create New Source',
						'view': 'insert',
						'widget_key': 'edit_layout',
						'cbjs_insert_path': 'movement/insert_new_source'
					   };
				      spt.panel.load_popup('Create New Source', 'tactic.ui.panel.EditWdg', kwargs);
				      bvr.src_el.value = '';
				  }
                          }
		          source_add_cell = top_el.getElementsByClassName('source_add_cell')[0];
			  sources_list_cell = top_el.getElementsByClassName('sources_list_cell')[0];
			  spt.api.load_panel(sources_list_cell, 'order_builder.movement_maker.SourcesListWdg', {movement_code: movement_code}); 
			  spt.api.load_panel(source_add_cell, 'order_builder.movement_maker.SourceAddWdg', {movement_code: movement_code}); 
                          bc_insert_txt = top_el.getElementById('source_barcode_insert');
                          bc_insert_txt.focus();
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                          //alert(err);
                }
         ''' % (my.movement_code)}
        return behavior

    def get_easy_checkin_commit_behavior(my, source_sk):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                           var server = TacticServerStub.get();
                           var source_sk = '%s';
                           var source_top_el = document.getElementsByClassName('movement_source_edit_top')[0];
                           var file_selected_cell = source_top_el.getElementsByClassName('file_holder')[0];
                           var file_selected = file_selected_cell.innerHTML;
                           var selects = source_top_el.getElementsByTagName('select');
                           var ctx_select = '';
                           for(var r = 0; r < selects.length; r++){
                               if(selects[r].name == 'source_process_select'){
                                   ctx_select = selects[r];
                               }
                           } 
                           var ctx = ctx_select.value;
                           server.simple_checkin(source_sk, ctx, file_selected, {'mode': 'inplace'});
                           var history = source_top_el.getElementsByClassName('movement_history_source_cell')[0];
                           //alert(history);
			   spt.api.load_panel(history, 'tactic.ui.widget.SObjectCheckinHistoryWdg', {search_key: source_sk}); 
                            

                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                          //alert(err);
                }
         ''' % (source_sk)}
        return behavior

    def get_easy_checkin_browse_behavior(my):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                           var server = TacticServerStub.get();
                           var applet = spt.Applet.get();
                           var base_dirs = server.get_base_dirs();
                           var base_sandbox = base_dirs.win32_sandbox_dir;
                           var source_top_el = document.getElementsByClassName('movement_twog_easy_checkin')[0];
                           var potential_files = applet.open_file_browser(base_sandbox);
                           var main_file = potential_files[0];
                           var file_selected_cell = source_top_el.getElementsByClassName('file_holder')[0];
                           file_selected_cell.innerHTML = main_file;
                           var commit_button = source_top_el.getElementsByClassName('easy_checkin_commit')[0];
                           commit_button.disabled = false;

                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                          //alert(err);
                }
         '''}
        return behavior
