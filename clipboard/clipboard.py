__all__ = ["ClipboarderSelectWdg","ClipboardWdg"]
import tacticenv
from pyasm.web import Table, DivWdg
from tactic.ui.common import BaseTableElementWdg
from tactic.ui.common import BaseRefreshWdg

class ClipboarderSelectWdg(BaseTableElementWdg):

    def init(my):
        nothing = 'true'

    def get_launch_behavior(my):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                          var my_code = bvr.src_el.get('code');
                          var my_st = bvr.src_el.get('st');
                          server = TacticServerStub.get();
                          kwargs = {
                                           'code': my_code,
                                           'st': my_st
                                   };
                          thing = server.execute_cmd('manual_updaters.ClipboardAddCmd', kwargs);
                          bvr.src_el.innerHTML = '<img src="/context/icons/custom/add_red.png"/>';
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         '''}
        return behavior

    def get_display(my):
        code = ''
        st = ''
        if 'code' in my.kwargs.keys():
            code = my.kwargs.get('code') 
        else: 
            sobject = my.get_current_sobject()
            st = sobject.get_search_type()
            code = sobject.get_code()
        widget = DivWdg()
        table = Table()
        table.add_attr('width', '50px')
        table.add_row()
        cell1 = table.add_cell('<img border="0" style="vertical-align: middle" title="" src="/context/icons/silk/add.png">')
        cell1.add_attr('code', code)
        cell1.add_attr('st', st)
        launch_behavior = my.get_launch_behavior()
        cell1.add_style('cursor: pointer;')
        cell1.add_behavior(launch_behavior)
        widget.add(table)

        return widget

class ClipboardWdg(BaseTableElementWdg):

    def init(my):
        my.st_lookup = {'twog/action tracker': 'Action Tracker','twog/archived files': 'Archived Files','twog/asset to movement': 'Asset To Movement','twog/barcode': 'Barcode','twog/bigboard record': 'Bigboard Record','twog/bundled message': 'Bundled Message','twog/client': 'Client','twog/client pipes': 'Client Pipes','twog/client rep dash': 'Client Rep Dash','twog/combo pipe': 'Combo Pipe','twog/company': 'Company','twog/custom property': 'Custom Property','twog/custom script': 'Custom Script','twog/deliverable': 'Deliverable','twog/deliverable spec': 'Deliverable Spec','twog/deliverable templ': 'Deliverable Templ','twog/element eval': 'Element Eval','twog/element eval audio': 'Element Eval Audio','twog/element eval barcodes': 'Element Eval Barcodes','twog/element eval lines': 'Element Eval Lines','twog/equipment': 'Equipment','twog/equipment unit cost': 'Equipment Unit Cost','twog/equipment used': 'Equipment Used','twog/equipment used templ': 'Equipment Used Templ','twog/error report': 'Error Report','twog/global resource': 'Global Resource','twog/hackpipe in': 'Hackpipe In','twog/hackpipe out': 'Hackpipe Out','twog/indie bigboard': 'Indie Bigboard','twog/inhouse locations': 'Inhouse Locations','twog/intermediate file': 'Intermediate File','twog/intermediate file templ': 'Intermediate File Templ','twog/language': 'Language','twog/location tracker': 'Location Tracker','twog/metadata report': 'Metadata Report','twog/movement': 'Movement','twog/naming': 'Naming','twog/order': 'Order','twog/order report': 'Order Report','twog/outside barcode': 'Outside Barcode','twog/payment': 'Payment','twog/person': 'Person','twog/pipeline prereq': 'Pipeline Prereq','twog/platform': 'Platform','twog/prequal eval': 'Prequal Eval','twog/prequal eval lines': 'Prequal Eval Lines','twog/priority log': 'Priority Log','twog/prod setting': 'Prod Setting','twog/production error': 'Production Error','twog/proj': 'Proj','twog/proj pricing': 'Proj Pricing','twog/proj templ': 'Proj Templ','twog/proj transfer': 'Proj Transfer','twog/proj translation': 'Proj Translation','twog/qc report vars': 'Qc Report Vars','twog/rate card': 'Rate Card','twog/rate card item': 'Rate Card Item','twog/report day': 'Report Day','twog/shipper': 'Shipper','twog/simplify pipe': 'Simplify Pipe','twog/source': 'Source','twog/source issues': 'Source Issues','twog/source log': 'Source Log','twog/source req': 'Source Req','twog/status log': 'Status Log','twog/tech eval': 'Tech Eval','twog/ticket': 'Ticket','twog/title': 'Title','twog/title origin': 'Title Origin','twog/title prereq': 'Title Prereq','twog/title templ': 'Title Templ','twog/whats new': 'Whats New','twog/widget config': 'Widget Config','twog/wo instruction changes': 'WO Instruction Changes','twog/wo report': 'WO Report','twog/work order': 'Work Order','twog/work order deliverables': 'Work Order Deliverables','twog/work order intermediate': 'Work Order Intermediate','twog/work order passin': 'Work Order Passin','twog/work order passin templ': 'Work Order Passin Templ','twog/work order prereq': 'Work Order Prereq','twog/work order prereq templ': 'Work Order Prereq Templ','twog/work order sources': 'Work Order Sources','twog/work order templ': 'Work Order Templ','twog/work order transfer': 'Work Order Transfer','twog/work order translation': 'Work Order Translation','sthpw/access log': 'Access Log','sthpw/access rule': 'Access Rule','sthpw/access rule in group': 'Access Rule In Group','sthpw/annotation': 'Annotation','sthpw/cache': 'Cache','sthpw/clipboard': 'Clipboard','sthpw/command': 'Command','sthpw/command log': 'Command Log','sthpw/connection': 'Connection','sthpw/custom property': 'Custom Property','sthpw/custom script': 'Custom Script','sthpw/db resource': 'DB Resource','sthpw/debug log': 'Debug Log','sthpw/doc': 'Doc','sthpw/exception log': 'Exception Log','sthpw/file': 'File','sthpw/file access': 'File Access','sthpw/group notification': 'Group Notification','sthpw/login': 'Login','sthpw/login group': 'Login Group','sthpw/login in group': 'Login In Group','sthpw/milestone': 'Milestone','sthpw/naming': 'Naming','sthpw/note': 'Note','sthpw/notification': 'Notification','sthpw/notification log': 'Notification Log','sthpw/notification login': 'Notification Login','sthpw/pg ts cfg': 'Pg Ts Cfg','sthpw/pg ts cfgmap': 'Pg Ts Cfgmap','sthpw/pga diagrams': 'Pga Diagrams','sthpw/pga forms': 'Pga Forms','sthpw/pga graphs': 'Pga Graphs','sthpw/pga images': 'Pga Images','sthpw/pga layout': 'Pga Layout','sthpw/pga queries': 'Pga Queries','sthpw/pga reports': 'Pga Reports','sthpw/pga schema': 'Pga Schema','sthpw/pga scripts': 'Pga Scripts','sthpw/pipeline': 'Pipeline','sthpw/pref list': 'Pref List','sthpw/pref setting': 'Pref Setting','sthpw/prod setting': 'Prod Setting','sthpw/project': 'Project','sthpw/project type': 'Project Type','sthpw/queue': 'Queue','sthpw/remote repo': 'Remote Repo','sthpw/repo': 'Repo','sthpw/retire log': 'Retire Log','sthpw/schema': 'Schema','sthpw/search object': 'Search Object','sthpw/snapshot': 'Snapshot','sthpw/snapshot type': 'Snapshot Type','sthpw/sobject list': 'Sobject List','sthpw/sobject log': 'Sobject Log','sthpw/special day': 'Special Day','sthpw/spt client trigger': 'Spt Client Trigger','sthpw/spt ingest rule': 'Spt Ingest Rule','sthpw/spt ingest session': 'Spt Ingest Session','sthpw/spt plugin': 'Spt Plugin','sthpw/spt process': 'Spt Process','sthpw/spt trigger': 'Spt Trigger','sthpw/spt url': 'Spt Url','sthpw/status log': 'Status Log','sthpw/task': 'Task','sthpw/template': 'Template','sthpw/ticket': 'Ticket','sthpw/timecard': 'Timecard','sthpw/transaction log': 'Transaction Log','sthpw/transaction state': 'Transaction State','sthpw/translation': 'Translation','sthpw/trigger': 'Trigger','sthpw/trigger in command': 'Trigger In Command','sthpw/wdg settings': 'Wdg Settings','sthpw/widget config': 'Widget Config','sthpw/widget extend': 'Widget Extend','sthpw/work hour': 'Work Hour'}
        my.x_butt = "<img src='/context/icons/common/BtnKill.gif' title='Remove' name='Remove'/>" 

    def get_remove_behavior(my, sk, user_name):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                          var sk = '%s';
                          user_name = '%s';
                          code = sk.split('code=')[1];
                          st = sk.split('?')[0];
                          top_el = document.getElementById('object_clipboard_' + user_name);
                          server = TacticServerStub.get();
                          login_obj = server.eval("@SOBJECT(sthpw/login['location','internal']['login','" + user_name + "'])")[0];
                          clipboard = login_obj.clipboard;
                          clipboard = clipboard.replace('|' + code,'').replace(code + '|','').replace(code,'');
                          other_codes_s = clipboard.split('[' + st + ']')[1]; 
                          other_codes = other_codes_s.split('[')[0];
                          if(other_codes == '' || other_codes == null || other_codes == '|' || other_codes == '||'){
                              clipboard = clipboard.replace('[' + st + ']' + other_codes,'');
                          }
                          server.update(login_obj.__search_key__, {'clipboard': clipboard});
                          row_el = top_el.getElementById('clip_' + sk);
                          row_el.style.display = 'none';
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         ''' % (sk, user_name)}
        return behavior

    def get_close(my):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                          spt.popup.close(spt.popup.get_popup(bvr.src_el));
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         '''}
        return behavior
    
    def get_clear_st(my, st, user_name):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                          server = TacticServerStub.get();
                          st = '%s';
                          user_name = '%s';
                          kwargs = {
                                           'search_type': st
                                   };
                          thing = server.execute_cmd('manual_updaters.ClipboardEmptySearchTypeCmd', kwargs);
                          parent_el = document.getElementById('object_clipboard_' + user_name);
                          spt.api.load_panel(parent_el, 'clipboard.ClipboardWdg', {}); 
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         ''' % (st, user_name)}
        return behavior

    def get_make_movement(my, user_name):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                          user_name = '%s';
                          server = TacticServerStub.get();
                          new_movement = server.insert('twog/movement', {'login': user_name});
                          thing = server.execute_cmd('manual_updaters.ClipboardMovementMakerCmd', {'movement_code': new_movement.code});
                          kwargs = {
                                           'movement_code': new_movement.code,
                                           'sk': new_movement.__search_key__,
                                           'user': user_name
                                   };
                          
                          var class_name = 'order_builder.movement_maker.MovementMakerWdg';
                          spt.tab.add_new('order_builder_' + new_movement.code, 'Movement Tracker ' + new_movement.code, class_name, kwargs);
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         ''' % (user_name)}
        return behavior

    def get_display(my):
        from tactic_client_lib import TacticServerStub
        from pyasm.common import Environment
        server = TacticServerStub.get()
        login = Environment.get_login()
        login_name = login.get_login()
        login = server.eval("@SOBJECT(sthpw/login['login','%s'])" % login_name)[0]
        st_dict = {}
        widget = DivWdg()
        table = Table()
        table.add_attr('id','object_clipboard_%s' % login_name)
        if login.get('clipboard') not in [None,'']:
            clipboard_text = login.get('clipboard')
            cs = clipboard_text.split('[')
            for c in cs:
                chunker = c.split(']')
                if chunker not in [None,'',['']]:
                    search_type = chunker[0]
                    codes = ''
                    if len(chunker) > 1:
                        codes = chunker[1]
                    if search_type not in st_dict.keys():
                        st_dict[search_type] = {'name': my.st_lookup[search_type.replace('_',' ')], 'codes': codes, 'objs': {}}
                    code_arr = codes.split('|')
                    seen_codes = []
                    for code in code_arr:
                        if code not in seen_codes and code not in [None,'']:
                            obj = server.eval("@SOBJECT(%s['code','%s'])" % (search_type, code))
                            if not obj:
                                obj = {'name': 'DELETED OR REMOVED', 'process': 'DELETED OR REMOVED', 'title': 'DELETED OR REMOVED', 'code': code}
                            else:
                                obj = obj[0]
                            st_dict[search_type]['objs'][code] = obj 
                            seen_codes.append(code)
                    
            for st in st_dict.keys():
                record = st_dict[st]
                table.add_row()
                head_cell = table.add_cell('<b><u>%s</u></b' % record['name'])
                clear_cell = table.add_cell('<input type="button" value="Clear %s"/>' % record['name'])
                clear_cell.add_behavior(my.get_clear_st(st, login_name))
                colspan = 2
                if st == 'twog/source':
                    colspan = 1
                    movement_cell = table.add_cell('<input type="button" value="Create Movement"/>')
                    movement_cell.add_behavior(my.get_make_movement(login_name))
                head_cell.add_attr('colspan',colspan)
                for code in record['objs'].keys():
                    obj = record['objs'][code]
                    name = ''
                    if 'name' in obj.keys():
                        name = obj.get('name')
                    if name in [None,''] or 'title' in obj.keys():
                        if 'title' in obj.keys():
                            name = obj.get('title')
                            if 'episode' in obj.keys():
                                episode = obj.get('episode')
                                if episode not in [None,'']:
                                    name = '%s: %s' % (name, episode)
                        elif 'process' in obj.keys():
                            name = obj.get('process') 
                    row = table.add_row()
                    row.add_attr('id','clip_%s' % obj.get('__search_key__'))
                    xb = table.add_cell(my.x_butt)
                    xb.add_style('cursor: pointer;')
                    xb.add_behavior(my.get_remove_behavior(obj.get('__search_key__'), login_name))
                    table.add_cell('%s: ' % code)
                    n = table.add_cell(name)
                    n.add_attr('nowrap','nowrap')
        widget.add(table)
        return widget
