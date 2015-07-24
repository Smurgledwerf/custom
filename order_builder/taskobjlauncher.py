__all__ = ["TaskObjLauncherWdg","TaskInspectWdg","InstructionsWdg","TitleViewWdg","OBSourceLikeNoEditWdg","TwogEasyCheckinWdg2","InspectScripts"]
import tacticenv
from pyasm.common import Environment
from pyasm.biz import *
from pyasm.web import Table, DivWdg
from tactic.ui.common import BaseTableElementWdg
from tactic.ui.common import BaseRefreshWdg
from tactic.ui.panel import EditWdg
from pyasm.widget import SelectWdg, IconWdg, TextWdg, CheckboxWdg
from tactic.ui.widget import DiscussionWdg

class TaskObjLauncherWdg(BaseTableElementWdg):

    def init(my):
        nothing = True
        my.server = None

    def get_launch_behavior(my):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                          var my_code = bvr.src_el.get('code'); 
                          var my_name = bvr.src_el.get('name');
                          var class_name = 'order_builder.TaskInspectWdg';
                          kwargs = {
                                           'code': my_code, 
                                           'name': my_name
                                   };
                          spt.panel.load_popup('Associated Info: ' + my_name, class_name, kwargs);
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                          //alert(err);
                }
         '''}
        return behavior

    def get_display(my):
        code = ''
        name = ''
        if 'code' in my.kwargs.keys():
            code = str(my.kwargs.get('code'))
            if 'name' in my.kwargs.keys():
                name = str(my.kwargs.get('name'))
        else:
            sobject = my.get_current_sobject()
            code = sobject.get_code()
            if 'WORK_ORDER' in code or 'PROJ' in code:
                name = sobject.get_value('process')
            elif 'TITLE' in code:
                name = sobject.get_value('title')
                if sobject.get_value('episode') not in [None,'']:
                    name = '%s: %s' % (name, sobject.get_value('episode'))
            elif 'ORDER' in code:
                name = sobject.get_value('name')
            if sobject.has_value('lookup_code'):
                if 'STATUS_LOG' in code:
                    from tactic_client_lib import TacticServerStub
                    my.server = TacticServerStub.get()
                    name = my.server.eval("@GET(sthpw/task['lookup_code','%s'].process)" % sobject.get_value('lookup_code')) 
                    if name:
                        name = name[0]
                    else:
                        name = 'Deleted Work Order'
                else:
                    name = sobject.get_value('process')
                code = sobject.get_value('lookup_code')
        widget = DivWdg()
        table = Table()
        #table.add_attr('width', '50px')
        table.add_row()
        cell1 = table.add_cell('<img border="0" style="vertical-align: middle" title="Inspect" name="Inspect" src="/context/icons/silk/information.png">')
        cell1.add_attr('code', code)
        cell1.add_attr('name',name)
        launch_behavior = my.get_launch_behavior()
        cell1.add_style('cursor: pointer;')
        cell1.add_behavior(launch_behavior)
        widget.add(table)

        return widget

class TaskInspectWdg(BaseRefreshWdg):

    def init(my):
        from client.tactic_client_lib import TacticServerStub
        from pyasm.common import Environment
        my.group_list = Environment.get_group_names()
        login = Environment.get_login()
        my.user = login.get_login()
        my.server = TacticServerStub.get()
        my.sk = ''
        my.code = ''
        my.st = ''
        my.is_scheduler = False
        for gname in my.group_list:
            if 'scheduling' in gname:
                my.is_scheduler = True
        if my.user == 'admin':
            my.is_scheduler = True
               
    
    def get_snapshot_file_link(my,snapshot_code):
        what_to_ret = ''
        base = '/volumes'
        rel_paths = my.server.get_all_paths_from_snapshot(snapshot_code, mode='relative')
        ctx_expr = "@GET(sthpw/snapshot['code','%s'].context)" % snapshot_code
        ctx = my.server.eval(ctx_expr)[0]; 
        if len(rel_paths) > 0:
            rel_path = rel_paths[0]
            splits = rel_path.split('/')
            if len(splits) < 2:
                splits = rel_path.split('\\')
            file_only = splits[len(splits) - 1]
            full = '%s/%s' % (base, rel_path)
            what_to_ret = '<a href="%s" title="%s" name="%s">%s: %s</a>' % (full,full,full, ctx, file_only)
        return what_to_ret

    def get_display(my):   
        from work_hours.work_hours_display import WorkHoursDisplayWdg
        from operator_view import IncompleteWOWdg
        if 'sk' in my.kwargs.keys():
            my.sk = str(my.kwargs.get('sk'))
            my.code = my.sk.split('code=')[1]
            my.st = my.sk.split('?')[0]
        elif 'code' in my.kwargs.keys():
            my.code = str(my.kwargs.get('code'))
            if 'WORK_ORDER' in my.code:
                my.st = 'twog/work_order'
            elif 'PROJ' in my.code: 
                my.st = 'twog/proj'
            my.sk = my.server.build_search_key(my.st, my.code)
        obs = InspectScripts()
        work_order = None
        proj = None
        name = ''
        st_name = ''
        if my.st == 'twog/work_order':
            work_order = my.server.eval("@SOBJECT(twog/work_order['code','%s'])" % my.code)[0]
            name = work_order.get('process')
            proj = my.server.eval("@SOBJECT(twog/proj['code','%s'])" % work_order.get('proj_code'))[0]
            st_name = "Work Order"
        elif my.st == 'twog/proj':
            proj = my.server.eval("@SOBJECT(twog/proj['code','%s'])" % my.code)[0]
            name = proj.get('process')
            st_name = "Project"
        ins = InspectScripts()
        title = my.server.eval("@SOBJECT(twog/title['code','%s'])" % proj.get('title_code'))[0]
        order = my.server.eval("@SOBJECT(twog/order['code','%s'])" % title.get('order_code'))[0]
        table = Table()
        table.add_row()
        links_table = Table()
        links_table.add_row()
        order_link = links_table.add_cell('<b><u>%s: %s</u></b>' % (order.get('name'), order.get('po_number')))
        order_link.add_style('cursor: pointer;')
        order_link.add_behavior(ins.get_launch_info_wdg(order.get('__search_key__'), order.get('name')))
        links_table.add_cell('->')
        title_link = links_table.add_cell('<b><u>%s: %s</u></b>' % (title.get('title'), title.get('episode')))
        title_link.add_style('cursor: pointer;')
        title_link.add_behavior(ins.get_launch_title_info_wdg(title.get('__search_key__'), title.get('title')))
        links_table.add_cell('->')
        proj_link = None
        if my.st == 'twog/work_order':
            proj_link = links_table.add_cell('<b><u>%s</u></b>' % proj.get('process'))
            proj_link.add_style('cursor: pointer;')
            proj_link.add_behavior(ins.get_launch_info_wdg(proj.get('__search_key__'), proj.get('process')))
            links_table.add_cell('->')
            wo_no_link = links_table.add_cell('<b>%s</b>' % work_order.get('process'))
        else:
            proj_link = links_table.add_cell(proj.get('process'))
        lynx = table.add_cell(links_table)
        lynx.add_attr('align','center')
        if my.st == 'twog/work_order':
            # Need to get the previous work_order's file location here
            proj_pipe = proj.get('pipeline_code')
            wo_process = work_order.get('process')
            wo_task = my.server.eval("@SOBJECT(sthpw/task['code','%s'])" % work_order.get('task_code'))[0]
            info = my.server.get_pipeline_processes_info(proj.get('__search_key__'), related_process=wo_process)
            input_processes = info.get('input_processes')
            input_processes.append(wo_process)
            input_tasks = my.server.query('sthpw/task', filters=[('search_type', wo_task.get('search_type')), ('search_id', wo_task.get('search_id')),('process',input_processes)])
            lead_in_files = []
            #print "INPUT TASKS = %s" % input_tasks
            for t in input_tasks:
                lookup_code = t.get('lookup_code')
                prev_wo = my.server.eval("@SOBJECT(twog/work_order['code','%s'])" % lookup_code)
                if prev_wo:
                    # THIS NEEDS TO GRAB FROM REAL CHECKIN AT SOME POINT, not 'location' on the wo
                    prev_wo = prev_wo[0]
                    if prev_wo.get('location') not in [None,'']:
                        lead_in_files.append([prev_wo.get('code'), prev_wo.get('process'), prev_wo.get('location')])
            wo_sources = my.server.eval("@SOBJECT(twog/work_order_sources['work_order_code','%s'])" % my.code)
            if len(wo_sources) > 0:
                table.add_row()
                celly0 = table.add_cell('<b><u>Sources</u></b>')
                celly0.add_attr('align','center')
                celly0.add_style('background-color: #cedb3a;')
            seen_srcs = []
            srcs = []
            src_snaps = {}
            for wos in wo_sources:
                if wos.get('source_code') not in seen_srcs:
                    sorc = my.server.eval("@SOBJECT(twog/source['code','%s'])" % wos.get('source_code'))[0]
                    srcs.append(sorc)
                    seen_srcs.append(wos.get('source_code'))
                if wos.get('snapshot_code') not in [None,'']:
                    if wos.get('source_code') not in src_snaps.keys():
                        src_snaps[wos.get('source_code')] = []
                    src_snaps[wos.get('source_code')].append(my.get_snapshot_file_link(wos.get('snapshot_code')))
            for s in srcs:
                src_tbl = Table()
                src_tbl.add_style('background-color: #cedb3a;')
                src_tbl.add_row()
                source_look = src_tbl.add_cell('<u>Title: %s, Type: %s</u>' % (s.get('title'), s.get('source_type')))
                source_look.add_attr('nowrap','nowrap')
                source_look.add_style('cursor: pointer;')
                source_look.add_behavior(obs.get_open_sob_behavior(s.get('code'),'twog/source','view'))
                if s.get('code') in src_snaps.keys():
                    for entry in src_snaps[s.get('code')]:
                        src_tbl.add_row()
                        file_cell = src_tbl.add_cell(entry)
                        file_cell.add_style('padding-left: 10px;') 
                table.add_row()
                main_celly0 = table.add_cell(src_tbl)
                main_celly0.add_attr('align','center')
            leadin_tbl = Table()
            leadin_tbl.add_style('background-color: #c44b3a;')
            # THIS NEEDS TO GRAB FROM REAL CHECKIN AT SOME POINT, not 'location' on the wo
            if len(lead_in_files) > 0:
                leadin_tbl.add_row()
                title_lead = leadin_tbl.add_cell('<b><u>Pass-in File(s)</u></b>')
                title_lead.add_attr('colspan','3')
                title_lead.add_attr('align','center')
            for l in lead_in_files:  
                leadin_tbl.add_row()
                leadin_tbl.add_cell(l[0])
                leadin_tbl.add_cell(l[1])
                leadin_tbl.add_cell(l[2])
                
            pre_expr = "@SOBJECT(twog/work_order_prereq['work_order_code','%s'])" % my.code
            prereqs = my.server.eval(pre_expr)
            if len(prereqs) > 0:
                table.add_row()
                celly = table.add_cell('<b><u>PreReqs</u></b>')
                celly.add_attr('align','center')
                celly.add_style('background-color: #ce4444;')
            for prereq in prereqs:
                pre_table = Table()
                pre_table.add_style('background-color: #ce4444;')
                pre_table.add_row()
                celly2 = pre_table.add_cell('%s: ' % prereq.get('prereq'))
                celly2.add_attr('align','left')
                sat = ''
                if prereq.get('satisfied') == True:
                    sat = 'Satisfied'
                else:
                    sat = 'Not Fulfilled'
                celly3 = pre_table.add_cell(sat)
                celly3.add_attr('align','left')
                table.add_row()
                main_celly = table.add_cell(pre_table)
                main_celly.add_attr('align','center')
        sources_expr = "@SOBJECT(twog/work_order_sources['work_order_code','%s'])" % my.code
        sources = my.server.eval(sources_expr)
  
        table.add_row()
        mo = 'view'
        if my.is_scheduler:
            mo = 'edit'
        view_edit_wdg = EditWdg(element_name='general',mode=mo,search_type=my.st,code=my.code,title="Info for %s: %s" % (st_name, my.code),view='edit',widget_key='edit_layout',search_key=my.sk)
        table.add_cell(view_edit_wdg)
        table.add_row()
        table.add_cell('<textarea rows=10 cols=92 readonly>DELIVERY SPECS (View Only):\n%s</textarea>' % title.get('delivery_specs'))
        incomplete_task_wdg = IncompleteWOWdg(search_type='twog/work_order',code=my.code,parent_view='task_view')
        notes_wdg = DiscussionWdg(search_key=title.get('__search_key__'),append_process='Client Services,Redelivery/Rejection Request,Redelivery/Rejection Completed',chronological=True)
        ta2 = Table()
        ta2.add_style('background-color: #bcbccc;')
        ta2.add_style('border-bottom-right-radius', '10px')
        ta2.add_style('border-bottom-left-radius', '10px')
        ta2.add_style('border-top-right-radius', '10px')
        ta2.add_style('border-top-left-radius', '10px')
        ta2.add_row()
        ta2.add_cell(incomplete_task_wdg)
        table.add_row()
        table.add_cell(ta2)
        table.add_row()
        table.add_cell(notes_wdg)
        table.add_row()
        hours = WorkHoursDisplayWdg(code=my.code)
        table.add_cell(hours) 
        table.add_attr('class','taskinspect_%s' % my.code)
        return table

class InstructionsWdg(BaseTableElementWdg):

    def init(my):
        from client.tactic_client_lib import TacticServerStub
        from pyasm.common import Environment
        my.server = TacticServerStub.get()
    
    def get_display(my):   
        sobject = my.get_current_sobject()
        tcode = sobject.get_code()
        wo_inst = my.server.eval("@GET(twog/work_order['task_code','%s'].instructions)" % tcode)
        instructions = ''
        if len(wo_inst) > 0:  
            if wo_inst[0] != '':
                instructions = '<textarea rows=8 cols=50 readonly>%s</textarea>' % wo_inst[0]
        table = Table()
        table.add_row()
        table.add_cell(instructions)
        return table

class TitleViewWdg(BaseTableElementWdg):

    def init(my):
        from client.tactic_client_lib import TacticServerStub
        from pyasm.common import Environment
        my.server = TacticServerStub.get()
        my.sk = ''
        my.code = ''
        my.name = ''
    
    def get_display(my):   
        my.sk = str(my.kwargs.get('search_key'))
        my.code = str(my.kwargs.get('code'))
        my.name = str(my.kwargs.get('name'))
        obs = InspectScripts()
        src_tbl = Table()
        togs = my.server.eval("@SOBJECT(twog/title_origin['title_code','%s'])" % my.code)
        sources = []
        for tog in togs:
            single = my.server.eval("@SOBJECT(twog/source['code','%s'])" % tog.get('source_code'))[0]
            sources.append(single)
        if len(sources) > 0:
            src_title = src_tbl.add_row()
            src_title.add_style('background-color: #cedb3a;')
            src_tbl.add_cell('Sources')
        for src in sources:
            src_tbl.add_row()
            source_look = src_tbl.add_cell('<u>Title: %s, Type: %s</u>' % (src.get('title'), src.get('source_type')))
            source_look.add_attr('nowrap','nowrap')
            source_look.add_style('cursor: pointer;')
            source_look.add_behavior(obs.get_open_sob_behavior(src.get('code'),'twog/source','view'))
        view_edit_wdg = EditWdg(element_name='general',mode='view',search_type='twog/title',code=my.code,title="Info for %s" % my.name,view='edit',widget_key='edit_layout',search_key=my.sk)
        delivs_tbl = Table()
        delivs = my.server.eval("@SOBJECT(twog/deliverable['title_code','%s'])" % my.code)
        if len(delivs) > 0:
            d_title = delivs_tbl.add_row()
            d_title.add_style('background-color: #3e5fc9;')
            delivs_tbl.add_cell('Deliverable(s)')
            delivs_tbl.add_cell('Satisfied?')
            
        for d in delivs:
            delivs_tbl.add_row()
            launch_look = delivs_tbl.add_cell('<u>Name: %s, Type: %s To: %s</u>' % (d.get('name'),d.get('source_type'), d.get('deliver_to'))) 
            launch_look.add_attr('nowrap','nowrap')
            launch_look.add_style('cursor: pointer;')
            launch_look.add_behavior(obs.get_open_sob_behavior(d.get('code'),'twog/deliverable','view'))
            checkbox = CheckboxWdg('satisfied_%s' % d.get('code'))
            #checkbox.set_persistence()
            if d.get('satisfied') == True:
                checkbox.set_value(True)
            else:
                checkbox.set_value(False)
            checkbox.add_behavior(obs.get_change_deliverable_satisfied_behavior(d.get('code'), d.get('satisfied')))
            satisfied_cell = delivs_tbl.add_cell(checkbox)
            satisfied_cell.add_attr('align','center')
        table = Table()
        table.add_row()
        stbl = table.add_cell(src_tbl)
        stbl.add_attr('align','center')
        table.add_row()
        table.add_cell(' ')
        table.add_row()
        dtbl = table.add_cell(delivs_tbl)
        dtbl.add_attr('align','center')
        table.add_row()
        table.add_cell(view_edit_wdg)
        return table

class OBSourceLikeNoEditWdg(BaseRefreshWdg): 

    def init(my):
        from client.tactic_client_lib import TacticServerStub
        from pyasm.common import Environment
        my.server = TacticServerStub.get()
        my.sob_code = ''
        my.st = ''
        my.open_type = ''
        my.name = ''

    def get_display(my):   
        from tactic.ui.widget import SObjectCheckinHistoryWdg
        my.sob_code = str(my.kwargs.get('sob_code'))
        my.st = str(my.kwargs.get('st'))
        my.open_type = str(my.kwargs.get('open_type'))
        my.name = str(my.kwargs.get('name'))
        sk = my.server.build_search_key(my.st, my.sob_code)
        obs = InspectScripts()
        edit_wdg = EditWdg(element_name='general', mode=my.open_type, search_type=my.st, code=my.sob_code, title=my.name, view='edit', widget_key='edit_layout')
        table = Table()
        table.add_attr('class','sob_edit_top')
        table.add_row()
        edit_sob_cell = table.add_cell(edit_wdg)
        edit_sob_cell.add_attr('valign','top')
        table.add_row()
        
        history = SObjectCheckinHistoryWdg(search_key=sk)
        history_cell = table.add_cell(history)
        history_cell.add_attr('class','history_sob_cell')
        table.add_row()

        checkin = TwogEasyCheckinWdg2(sk=sk,code=my.sob_code)
        checkin_cell = table.add_cell(checkin)
        checkin_cell.add_attr('class','checkin_sob_cell')
        checkin_cell.add_attr('width','100%s' % '%')
        checkin_cell.add_attr('align','center')

        return table

class TwogEasyCheckinWdg2(BaseRefreshWdg):
    def init(my):
        from client.tactic_client_lib import TacticServerStub
        from pyasm.common import Environment
        my.code = ''
        my.sk = ''
        my.source_contexts = []

    def get_display(my):   
        from pyasm.prod.biz import ProdSetting
        my.code = str(my.kwargs.get('code'))
        my.sk = str(my.kwargs.get('sk'))
        my.source_contexts = ProdSetting.get_value_by_key('source_contexts').split('|')
        obs = InspectScripts()
        table = Table()
        table.add_attr('class','twog_easy_checkin')
        table.add_attr('width','100%s' % '%')
        table.add_row()
        title_bar = table.add_cell('<b><u>Checkin New File</u></b>')
        title_bar.add_attr('align','center')
        title_bar.add_attr('colspan','4')
        title_bar.add_style('font-size: 110%ss' % '%')
        processes_sel = SelectWdg('sob_process_select')
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
        button.add_behavior(obs.get_easy_checkin_browse_behavior())
        big_button = mini1.add_cell('<input type="button" value="Check In" class="easy_checkin_commit" disabled/>')
        big_button.add_style('cursor: pointer;')
        big_button.add_behavior(obs.get_easy_checkin_commit_behavior(my.sk))
        table.add_cell(mini1)
        return table

class InspectScripts(BaseRefreshWdg):
    def init(my):
        from client.tactic_client_lib import TacticServerStub
        from pyasm.common import Environment
        my.server = TacticServerStub.get()

    def get_easy_checkin_commit_behavior(my, sob_sk):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                           var server = TacticServerStub.get();
                           var sob_sk = '%s';
                           var sob_top_el = document.getElementsByClassName('sob_edit_top')[0];
                           var file_selected_cell = sob_top_el.getElementsByClassName('file_holder')[0];
                           var file_selected = file_selected_cell.innerHTML;
                           var selects = sob_top_el.getElementsByTagName('select');
                           var ctx_select = '';
                           for(var r = 0; r < selects.length; r++){
                               if(selects[r].name == 'sob_process_select'){
                                   ctx_select = selects[r];
                               }
                           } 
                           var ctx = ctx_select.value;
                           server.simple_checkin(deliverable_sk, ctx, file_selected, {'mode': 'inplace'});
                           var history = sob_top_el.getElementsByClassName('history_sob_cell')[0];
                           //alert(history);
			   spt.api.load_panel(history, 'tactic.ui.widget.SObjectCheckinHistoryWdg', {search_key: deliverable_sk}); 
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                          //alert(err);
                }
         ''' % (sob_sk)}
        return behavior

    def get_easy_checkin_browse_behavior(my):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                           var server = TacticServerStub.get();
                           var applet = spt.Applet.get();
                           var base_dirs = server.get_base_dirs();
                           var base_sandbox = base_dirs.win32_sandbox_dir;
                           var sob_top_el = document.getElementsByClassName('twog_easy_checkin')[0];
                           var potential_files = applet.open_file_browser(base_sandbox);
                           var main_file = potential_files[0];
                           var file_selected_cell = sob_top_el.getElementsByClassName('file_holder')[0];
                           file_selected_cell.innerHTML = main_file;
                           var commit_button = sob_top_el.getElementsByClassName('easy_checkin_commit')[0];
                           commit_button.disabled = false;

                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                          //alert(err);
                }
         '''}
        return behavior

    def get_launch_info_wdg(my, ob_sk, name):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                          var ob_sk = '%s';
                          var name = '%s';
                          var ob_st = ob_sk.split('?')[0];
                          var ob_code = ob_sk.split('code=')[1];
                          kwargs = {element_name: 'general',
                                    mode: 'view', 
                                    search_type: ob_st, 
                                    code: ob_code, 
                                    title: 'View info for ' + name, 
                                    view: 'edit', 
                                    widget_key: 'edit_layout', 
                                    search_key: ob_sk 

                          };
                          spt.panel.load_popup('Info for ' + name, 'tactic.ui.panel.EditWdg', kwargs);
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                          //alert(err);
                }
         ''' % (ob_sk, name)
        }
        return behavior
    
    def get_launch_title_info_wdg(my, ob_sk, name):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                          var ob_sk = '%s';
                          var name = '%s';
                          var ob_st = ob_sk.split('?')[0];
                          var ob_code = ob_sk.split('code=')[1];
                          kwargs = {
                                    code: ob_code, 
                                    name: name, 
                                    search_key: ob_sk 

                          };
                          spt.panel.load_popup('Info for ' + name, 'order_builder.TitleViewWdg', kwargs);
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                          //alert(err);
                }
         ''' % (ob_sk, name)
        }
        return behavior

    def get_change_deliverable_satisfied_behavior(my, deliverable_code, current_state):
        behavior = {'css_class': 'clickme', 'type': 'change', 'cbjs_action': '''        
                        try{
                          var server = TacticServerStub.get();
                          deliverable_code = '%s';
                          state = '%s';
                          new_val = '';
                          if(state == 'False'){
                              new_val = 'True';
                          }else{
                              new_val = 'False';
                          }
                          server.update(server.build_search_key('twog/deliverable', deliverable_code), {'satisfied': new_val});
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                          //alert(err);
                }
         ''' % (deliverable_code, current_state)}
        return behavior


    def get_open_sob_behavior(my, sob_code, st, open_type):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                          var server = TacticServerStub.get();
                          sob_code = '%s';
                          st = '%s';
                          open_type = '%s';
                          name = 'Deliverable Portal'
                          if(st == 'twog/source'){
                              name = 'Source Portal'
                          } 
                          spt.panel.load_popup(name, 'order_builder.OBSourceLikeNoEditWdg', {'sob_code': sob_code, 'st': st, 'open_type': open_type, 'name': name});
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                          //alert(err);
                }
         ''' % (sob_code, st, open_type)}
        return behavior
