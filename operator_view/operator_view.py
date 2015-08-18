__all__ = ["OperatorViewWdg","TitleSidebarWdg","ChecklistWdg","SourceListWdg","InstructionsWdg","WorkOrderHoursWdg","EquipmentUsedMultiAdderWdg","WorkOrderEquipmentWdg","StatusAndAssignmentWdg","TitleBarWrap"]
import tacticenv
from pyasm.common import Environment
from pyasm.biz import *
from pyasm.web import Table, DivWdg
from pyasm.widget import SelectWdg, IconWdg, TextWdg, CheckboxWdg

from tactic.ui.common import BaseTableElementWdg
from tactic.ui.common import BaseRefreshWdg
from tactic.ui.panel import EditWdg
from tactic.ui.widget.button_new_wdg import ButtonSmallNewWdg, ButtonRowWdg
from tactic.ui.widget import DiscussionWdg
from source_issues import SourceDisplayWdg


class OperatorViewWdg(BaseRefreshWdg):
    def init(my):
        from client.tactic_client_lib import TacticServerStub
        from pyasm.common import Environment
        my.server = TacticServerStub.get()
        my.login_obj = Environment.get_login()
        my.user_name = my.login_obj.get_login()
        my.task_sk = ''
        my.order = None
        my.titles = None
        my.projs = None
        my.wos = None
        my.main_wo = None
        my.work_order_code = ''
        my.main_proj = None
        my.main_title = None
        my.task = None
        my.groups_str = ''
        my.my_groups = my.server.eval("@SOBJECT(sthpw/login_in_group['login','%s'])" % my.user_name)
        for mg in my.my_groups:
            if my.groups_str == '':
                my.groups_str = mg.get('login_group')
            else:
                my.groups_str = '%s,%s' % (my.groups_str, mg.get('login_group'))
    
    def get_display(my):   
        my.task_sk = my.kwargs.get('task_sk')
        widget = DivWdg()
        table = Table()
        table.add_style('background-color: #d1d7e2;')
        table.add_row()
        my.task = my.server.get_by_search_key(my.task_sk)
        mw = my.server.eval("@SOBJECT(twog/work_order['code','%s'])" % my.task.get('lookup_code'))
        if mw:
            my.main_wo = mw[0]
            my.work_order_code = my.main_wo.get('code')
            table.add_attr('class','panel_%s' % my.main_wo.get('code'))
            mt = my.server.eval("@SOBJECT(twog/title['code','%s'])" % my.main_wo.get('title_code'))
            if mt:
                my.main_title = mt[0]
                menu = TitleSidebarWdg(title=my.main_title, user_name=my.user_name, groups_str=my.groups_str, work_order_code=my.work_order_code)
                my.wos, my.projs = menu.figure()
                my.wos = menu.get_wos()
                my.projs = menu.get_projs()
                for proj in my.projs:
                    if my.main_wo.get('proj_code') == proj.get('code'):
                        my.main_proj = proj
                    
                menu_cell = table.add_cell(menu)
                #Don't need this, because reloading the TitleSidebar doesn't work..
#                menu_cell.add_attr('id','ov_title_bar_%s' % my.main_title.get('code'))
#                menu_cell.add_attr('title_code', my.main_title.get('code'))
#                menu_cell.add_attr('user_name', my.user_name)
#                menu_cell.add_attr('groups_str', my.groups_str)
#                menu_cell.add_attr('work_order_code', my.work_order_code)
                
                right_table = Table()
                right_table.add_attr('cellspacing','0px')
                right_table.add_attr('cellpadding','0px')
                right_table.add_row()
                h2 = table.h2('WO# %s: %s' % (my.main_wo.get('id'), my.main_wo.get('process')))
                h2.add_attr('width','100%%')
                top_cell = right_table.add_cell(h2)
                top_cell.add_attr('class','ovw_main_title')
                top_cell.add_attr('colspan','4')
                top_cell.add_attr('valign','top')
                top_cell.add_attr('align','center')
                top_cell.add_attr('width','100%%')

                first_tbl = Table()
                first_tbl.add_row()
                ckw = ChecklistWdg(work_order_code=my.work_order_code)
                checklist = first_tbl.add_cell(ckw)
                first_tbl.add_row()
                sourcelist = SourceListWdg(work_order_code=my.work_order_code)
                first_tbl.add_cell(sourcelist)

                requires_mastering = 'false'
                if my.main_title.get('requires_mastering_qc') not in ['False','false','0',None,False]:
                   requires_mastering = 'true'
                second_tbl = Table()
                second_tbl.add_row()
                stass = StatusAndAssignmentWdg(task=my.task, work_order_code=my.work_order_code, requires_mastering=requires_mastering)
                status_reloader = second_tbl.add_cell(stass)
                status_reloader.add_attr('class','status_panel_%s' % my.work_order_code)
                status_reloader.add_attr('requires_mastering',requires_mastering)
                instructions = InstructionsWdg(instructions='%s\n\nDELIVERABLE SPECS:\n%s' % (my.main_wo.get('instructions'), my.main_title.get('delivery_specs')))
                second_tbl.add_row()
                second_tbl.add_cell(instructions)
                
                third_tbl = Table()
                third_tbl.add_row()
                hrs = WorkOrderHoursWdg(task=my.task,process=my.main_proj.get('process'),user_name=my.user_name)
                hours = third_tbl.add_cell(hrs)
                third_tbl.add_row()
                eq = WorkOrderEquipmentWdg(work_order_code=my.work_order_code,work_order_name=my.main_wo.get('name'))
                eq_reloader = third_tbl.add_cell(eq)
                eq_reloader.add_attr('class','eq_panel_%s' % my.work_order_code)
                

                right_table.add_row()
                right_table.add_cell(first_tbl)
                right_table.add_cell(second_tbl)
                right_table.add_cell(third_tbl)
                notes_wdg = DiscussionWdg(search_key=my.main_title.get('__search_key__'),append_process='Client Services,Redelivery/Rejection Request,Redelivery/Rejection Completed',preppend='%s: %s' % (my.main_wo.get('name'), my.work_order_code),chronological=True)
                wrapped = TitleBarWrap(htmlelement=notes_wdg)
                notes_wdg = wrapped.get_title_wrap('Title Notes')
                right_table.add_cell(notes_wdg)
                

                tc1 = table.add_cell(right_table)
                tc1.add_attr('colspan','2')
                #Get the sidebar menu here
            else:
                table.add_cell("Important connections are broken. Title not found. Please contact the Admin.") 
        else:
            table.add_cell("Important connections are broken. Please contact the Admin.") 
        table.add_attr('cellspacing','0px')
        table.add_attr('cellpadding','0px')
        widget.add(table)
        widget.add_attr('id','OVPanel_%s' % (my.main_title.get('code')))
        return widget

class TitleSidebarWdg(BaseRefreshWdg):
    def init(my):
        from client.tactic_client_lib import TacticServerStub
        my.server = TacticServerStub.get()
        my.main_title = None
        my.title_str = ''
        my.projs = None
        my.wos = None
        my.status_colors = {
          "Assignment": "#fcaf88", 
          "Pending": "#d7d7d7", 
          "In_Progress": "#f5f3a4",
          "In Progress": "#f5f3a4",
          "Waiting": "#ffd97f",
          "Need Assistance": "#fc88bf",
          "Review": "#888bfc",
          "Approved": "#d4b5e7",
          "Completed": "#b7e0a5",
          "Failed QC": "#ff0000",
          "Rejected": "#ff0000",
          "Fix Needed": "#c466a1",
          "On_Hold": "#e8b2b8",
          "On Hold": "#e8b2b8",
          "Client Response": "#ddd5b8",
          "Ready": "#b2cee8",
          "DR In_Progress": "#d6e0a4",
          "DR In Progress": "#d6e0a4",
          "Amberfin01_In_Progress": "#d8f1a8",
          "Amberfin01 In Progress": "#d8f1a8",
          "Amberfin02_In_Progress": "#f3d291",
          "Amberfin02 In Progress": "#f3d291",
          "BATON In_Progress": "#c6e0a4",
          "BATON In Progress": "#c6e0a4",
          "Export In_Progress": "#796999",
          "Export In Progress": "#796999",
          "Need Buddy Check": "#e3701a",
          "Buddy Check In_Progress": "#1aade3",
          "Buddy Check In Progress": "#1aade3",
          "crap": "#e20ff0"
        } 
        if 'title' in my.kwargs.keys():
            my.main_title = my.kwargs.get('title')
            my.title_str = my.main_title.get('title')
            if my.main_title.get('episode') not in [None,'']:
                my.title_str = '%s: %s' % (my.title_str, my.main_title.get('episode'))

        my.user_name = ''
        if 'user_name' in my.kwargs.keys():
            my.user_name = my.kwargs.get('user_name')

        my.groups_str = ''
        if 'groups_str' in my.kwargs.keys():
            my.groups_str = my.kwargs.get('groups_str')
        
        my.work_order_code = my.kwargs.get('work_order_code')

    def get_switch_panel_behavior(my, search_key, title_code):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
            try{
                spt.app_busy.show("Loading...", "")
            
                var server = TacticServerStub.get()
            
                var search_key = '%s'; 
                var title_code = '%s'; 
            
                var task_so = server.get_by_search_key(search_key)
                var tab_title = task_so.process;
                var tab_name = task_so.code;
                var top_el = bvr.src_el.getParent(".ovw_main")
                var kwargs = {
                  'task_sk': search_key
                }
                var class_name = "operator_view.OperatorViewWdg";
                panel_el = top_el.getElementById('OVPanel_' + title_code);
                spt.panel.load(panel_el, class_name, kwargs)
            
                spt.app_busy.hide()
               }catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
               }
            
            ''' % (search_key, title_code)}
        return behavior

    def figure(my):
        if my.projs in [None,'']:
            my.projs = my.server.eval("@SOBJECT(twog/proj['title_code','%s']['@ORDER_BY','order_in_pipe'])" % my.main_title.get('code'))
        if my.wos in [None,'']:
            my.wos = my.server.eval("@SOBJECT(twog/work_order['title_code','%s']['@ORDER_BY','order_in_pipe'])" % my.main_title.get('code'))
        return [my.projs, my.wos]

    def get_projs(my):
        return my.projs

    def get_wos(my):
        return my.wos

    def get_proj_row(my, proj):
        table = Table()
        table.add_attr('class','OVPR_%s' % proj.get('code'))
        table.add_attr('width','100%%')
        row = table.add_row()
        row.add_style('background-color: #d9ed8b;')
        name_cell = table.add_cell('<b><i>%s</i></b>' % proj.get('process'))
        if 'scheduling' in my.groups_str:
            tools = Table()
            tools.add_row()
            tools.add_cell('DueDateChange')
            tools.add_cell('SetPriority')
            table.add_cell(tools)
        return table

    def get_wo_row(my, wo, modder):
        wo_task = my.server.eval("@SOBJECT(sthpw/task['code','%s'])" % wo.get('task_code'))
        if wo_task:
            wo_task = wo_task[0]
        else:
            wo_task = {'process': wo.get('process'), 'status': 'crap', 'assigned_login_group': 'TASK NOT FOUND', 'priority': wo.get('priority'), 'due_date': wo.get('due_date')}
        table = Table()
        table.add_attr('class','OVWO_%s' % wo.get('code'))
        table.add_attr('width','100%%')
        row = table.add_row()
        row.add_behavior(my.get_switch_panel_behavior(wo_task.get('__search_key__'),my.main_title.get('code')))
        bgcolor = '#c6eda0'
        if modder % 2 == 0:
            bgcolor = '#b3d691'
        row.add_style('background-color: %s;' % bgcolor)
        inner_tbl = Table()
        inner_tbl.add_attr('border','1')
        inner_tbl.add_style('border-color: %s;' % bgcolor)
        inner_tbl.add_row()
        status_cell = inner_tbl.add_cell("&nbsp;")
        status_cell.add_attr('width','16px')
        status_cell.add_attr('id','status_color_block_%s' % wo.get('code'))
        status_cell.add_style('background-color: %s;' % my.status_colors[wo_task.get('status')])
        inner_tbl2 = Table()
        inner_tbl2.add_row()
        inner_tbl2.add_cell(inner_tbl)
        name_cell = inner_tbl2.add_cell('<b>%s</b>' % wo.get('process'))
        name_cell.add_attr('align','left')
        name_cell.add_attr('nowrap','nowrap')
        if wo.get('code') == my.work_order_code:
            name_cell.add_style('background-color: #00bfff;')
        stat_container = table.add_cell(inner_tbl2)
        spacer = table.add_cell('&nbsp;')
        spacer.add_attr('width','30px')
        assigned_cell = table.add_cell('<u>%s</u>' % wo_task.get('assigned'))
        assigned_cell.add_attr('align','right')
        assigned_cell.add_attr('nowrap','nowrap')
        assigned_cell.add_attr('id','task_assigned_%s' % wo.get('code'))
        dept_cell = table.add_cell('<i>%s</i>' % wo_task.get('assigned_login_group'))
        dept_cell.add_attr('align','right')
        dept_cell.add_attr('nowrap','nowrap')
        return table

    def save_trts(my, code):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                          var code = '%s';
                          var top = bvr.src_el.getParent(".ovw_main")
                          trt_el = top.getElementById('trt_ov_' + code);
                          trtwtl_el = top.getElementById('trtwtl_ov_' + code);
                          var server = TacticServerStub.get();
                          var sk = server.build_search_key('twog/title', code);
                          if(trt_el.old_value != trt_el.value || trtwtl_el.old_value != trtwtl_el.value){
                              server.update(sk, {'total_program_runtime': trt_el.value, 'total_runtime_w_textless': trtwtl_el.value});
                              spt.alert('Saved');
                              find_str = 'standard_incomplete_tasks_' + code;
                              standards = document.getElementsByClassName(find_str);
                              for(var r = 0; r < standards.length; r++){
                                  trt_inc_el = standards[r].getElementById('trt_top');
                                  trtwtl_inc_el = standards[r].getElementById('trtwtl_top');
                                  trt_inc_el.value = trt_el.value;
                                  trtwtl_inc_el.value = trtwtl_el.value;
                              }
                          }
                          pulled_el = top.getElementById('pulled_blacks_ov_' + code);
                          if(pulled_el.value != pulled_el.old_value){
                              server.update(sk, {'pulled_blacks': pulled_el.value});
                          }
                          file_size_el = top.getElementById('file_size_ov_' + code);
                          if(file_size_el.value != file_size_el.old_value){
                              server.update(sk, {'file_size': file_size_el.value});
                          }
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         ''' % (code)}
        return behavior

    def get_display(my):
        trt = my.main_title.get('total_program_runtime')
        trtwtl = my.main_title.get('total_runtime_w_textless')
        pulled_blacks = my.main_title.get('pulled_blacks')
        file_size = my.main_title.get('file_size')
        if trt in [None,'']:
            trt = ''
        if trtwtl in [None,'']:
            trtwtl = ''
        if pulled_blacks in [None,'']:
            pulled_blacks = ''
        if file_size in [None,'']:
            file_size = ''
        title_code = my.main_title.get('code')
        dudes = my.figure()
        widget = DivWdg()
        table = Table()
        trt_table = Table()
        trt_rowin = trt_table.add_row()
        trt_rowin.add_attr('id','%s_ov_trt_row' % title_code)
        tt1 = trt_table.add_cell('TRT: ')
        tt1.add_style('font-size: 9px;')
        trt_table.add_cell('''<input type="text" maxlength=12 style="width: 80px; height: 16px; border-radius: 5px; font-size: 10px;" size=5 id="trt_ov_%s" value="%s" old_value="%s"/>''' % (title_code, trt, trt))
        tt2 = trt_table.add_cell('TRT W/Textless: ')
        tt2.add_style('font-size: 9px;')
        trt_table.add_cell('''<input type="text" maxlength=12 style="width: 80px; height: 16px; border-radius: 5px; font-size: 10px;" size=5 id="trtwtl_ov_%s" value="%s" old_value="%s"/>''' % (title_code, trtwtl, trtwtl))
        trt_table.add_row()
        tt3 = trt_table.add_cell('File Size: ')
        tt3.add_style('font-size: 9px;')
        trt_table.add_cell('''<input type="text" maxlength=3 style="width: 50px; height: 16px; border-radius: 5px; font-size: 10px;" size=5 id="file_size_ov_%s" value="%s" old_value="%s"/>''' % (title_code, file_size, file_size))
        tt4 = trt_table.add_cell('Pulled Blacks/Edits: ')
        tt4.add_style('font-size: 9px;')
        trt_table.add_cell('''<input type="text" maxlength=3 style="width: 35px; height: 16px; border-radius: 5px; font-size: 10px;" size=5 id="pulled_blacks_ov_%s" value="%s" old_value="%s"/>''' % (title_code, pulled_blacks, pulled_blacks))
        save_text = 'Save Title Information'
        save_butt = trt_table.add_cell('<input type="button" value="%s" style="font-size: 9px;"/>' % save_text)
        save_butt.add_behavior(my.save_trts(title_code))
        table.add_row()
        top_cell = table.add_cell(table.h2(my.title_str))
        top_cell.add_attr('class','ovw_main_title')
        table2 = Table() 
        table2.add_attr('width','100%%')
        table2.add_attr('border','1')
        trt_row = table.add_row()
        trt_long = table.add_cell(trt_table)
        for proj in my.projs:
            table2.add_row()
            proj_cell = table2.add_cell(my.get_proj_row(proj))
            proj_cell.add_attr('width','100%%')
            count = 0
            for wo in my.wos:
                if wo.get('proj_code') == proj.get('code'):
                    table2.add_row()
                    wo_cell = table2.add_cell(my.get_wo_row(wo, count))
                    wo_cell.add_style('width','100%%')
                    count = count + 1
        table.add_row()
        table.add_cell(table2)
        widget.add(table) 
        return widget

class ChecklistWdg(BaseRefreshWdg):
    def init(my):
        from client.tactic_client_lib import TacticServerStub
        my.server = TacticServerStub.get()
        my.wo_code = my.kwargs.get('work_order_code')
        my.checklist_items = None
    
    def get_toggle_behavior(my, prereq_sk):
        toggle_behavior = {'css_class': 'clickme', 'type': 'change', 'cbjs_action': '''        
                        try{
                            var prereq_sk = '%s';
                            var curr_val = bvr.src_el.checked;
                            var server = TacticServerStub.get();
                            server.update(prereq_sk, {'satisfied': curr_val});
                            
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
        ''' % prereq_sk}
        return toggle_behavior
        
    def get_display(my):
        my.checklist_items = my.server.eval("@SOBJECT(twog/work_order_prereq['work_order_code','%s'])" % my.wo_code) 
        table = Table()
        for ci in my.checklist_items:
            table.add_row()
            checker = CheckboxWdg('prereq_box')
            #checker.set_persistence()
            if ci.get('satisfied') == True:
                checker.set_value(True)
            else:
                checker.set_value(False)
            checker.add_behavior(my.get_toggle_behavior(ci.get('__search_key__')))
            table.add_cell(checker)
            table.add_cell(ci.get('prereq'))
        wrapped = TitleBarWrap(htmlelement=table)
        table = wrapped.get_title_wrap('Checklist')
        return table

class SourceListWdg(BaseRefreshWdg):
    def init(my):
        from client.tactic_client_lib import TacticServerStub
        my.server = TacticServerStub.get()
        my.work_order_code = my.kwargs.get('work_order_code')

    def get_display(my):
        table = SourceDisplayWdg(work_order_code=my.work_order_code)
        wrapped = TitleBarWrap(htmlelement=table)
        table = wrapped.get_title_wrap('Assets')
        return table

class InstructionsWdg(BaseRefreshWdg):
    def init(my):
        my.instructions = ''
        if 'instructions' in my.kwargs.keys():
            my.instructions = my.kwargs.get('instructions')
        elif 'work_order_code' in my.kwargs.keys():
            from client.tactic_client_lib import TacticServerStub
            my.server = TacticServerStub.get()
            my.instructions = my.server.eval("@GET(twog/work_order['code','%s'].instructions)" % my.kwargs.get('work_order_code'))[0]

    def get_display(my):
        #try:
        #    unicode(my.instructions, "ascii")
        #except UnicodeError:
        #    my.instructions = unicode(my.instructions, "utf-8")
        #else:
            # value was valid ASCII data
        #    pass
        table = Table()
        table.add_attr('height','100%%')
        table.add_attr('width','300px')
        table.add_row()
        tall_cell = table.add_cell('<textarea rows=20 cols=50 readonly>%s</textarea>' % my.instructions)
        tall_cell.add_attr('height','100%%')
        wrapped = TitleBarWrap(htmlelement=table)
        table = wrapped.get_title_wrap('Work Order Instructions')
        return table

class WorkOrderHoursWdg(BaseRefreshWdg):
    def init(my):
        from client.tactic_client_lib import TacticServerStub
        my.server = TacticServerStub.get()

    def get_submit_behavior(my, title_code, task_code, search_id, user_name, pop):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                            var title_code = '%s';
                            var task_code = '%s';
                            var search_id = '%s';
                            var user_name = '%s';
                            var popper = '%s';
                            var top_el = spt.api.get_parent(bvr.src_el, '.houradd_' + title_code);
                            var hours_el = top_el.getElementById('hours_txt');
                            var hours = hours_el.value;
                            var bad_hours = false;
                            if(hours != ''){
                                if(hours != 0){
                                    if(hours != '0'){
                                        if(hours != null){
                                            if(!(isNaN(hours))){
                                                var client_pull = top_el.getElementById('client_pull');
                                                var scheduler_pull = top_el.getElementById('scheduler_pull')
                                                var title_pull = top_el.getElementById('title_pull');
                                                var tcode = title_pull.value;
                                                var scheduler = scheduler_pull.value;
                                                var client_code = client_pull.value;
                                                var client_name = client_pull.options[client_pull.selectedIndex].text;
                                                if(client_name == '--Select--'){
                                                    client_name = '';
                                                }
                                                if(popper == 'popup'){
                                                    var is_billable_el = top_el.getElementById('billable_check');
                                                    var is_billable = is_billable_el.checked;
                                                }else{
                                                    var is_billable = true;
                                                }
                                                var work_description_el = top_el.getElementById('summary_txt');
                                                var work_description = work_description_el.value;
                                                var op_note_el = top_el.getElementById('op_note');
                                                var op_note = op_note_el.value; 
                                                var server = TacticServerStub.get();
                                                order_code = '';
                                                if(tcode != ''){
                                                    order = server.eval("@SOBJECT(twog/title['code','" + tcode + "'].twog/order)")[0]; 
                                                    order_code = order.code
                                                }
                                                var today = new Date(); 
                                                var dd = today.getDate(); 
                                                var mm = today.getMonth() + 1; 
                                                var yyyy = today.getFullYear(); 
                                                var day = yyyy + '-' + mm + '-' + dd + ' ' + today.getHours() + ':' + today.getMinutes() + ':' + today.getSeconds();
                                                data = {'is_billable': is_billable, 'client_code': client_code, 'client_name': client_name, 'title_code': tcode, 'category': work_description, 'scheduler': scheduler, 'straight_time': hours, 'order_code': order_code, 'login': user_name, 'description': op_note, 'day': day}; 
                                                eq_row = null;
                                                eq_cell = null;
                                                if(popper != 'popup'){
                                                    data['search_type'] = 'sthpw/task';
                                                    data['task_code'] = task_code;
                                                    data['search_id'] = search_id;
                                                } 
                                                work_hour = server.insert('sthpw/work_hour', data); 
                                                if(popper == 'popup'){
                                                    eq_row = top_el.getElementById('eq_row');
                                                    eq_cell = top_el.getElementById('eq_cell');
                                                    spt.api.load_panel(eq_cell, 'operator_view.WorkOrderEquipmentWdg', {'work_hour_code': work_hour.code, 'work_order_name': ''})
                                                    trow = top_el.getElementById('trow');
                                                    crow = top_el.getElementById('crow');
                                                    srow = top_el.getElementById('srow');
                                                    wdrow = top_el.getElementById('wdrow');
                                                    chrow = top_el.getElementById('chrow');
                                                    orow = top_el.getElementById('orow');
                                                    subrow = top_el.getElementById('subrow');
                                                    trow.style.display = 'none';
                                                    crow.style.display = 'none';
                                                    srow.style.display = 'none';
                                                    wdrow.style.display = 'none';
                                                    chrow.style.display = 'none';
                                                    orow.style.display = 'none';
                                                    subrow.style.display = 'none';
                                                }else{
                                                    user_hr_cell = top_el.getElementById('user_hr');
                                                    total_hr_cell = top_el.getElementById('total_hr');
                                                    user_contents = user_hr_cell.innerHTML;
                                                    user_arr = user_contents.split(': ')
                                                    user = user_arr[0];
                                                    user_count = parseFloat(user_arr[1]);
                                                    total_hr_contents = total_hr_cell.innerHTML;
                                                    total_arr = total_hr_contents.split(': ')
                                                    total_count = parseFloat(total_arr[1]);
                                                    new_hours = parseFloat(hours);
                                                    new_user_hours = user_count + new_hours;
                                                    new_total_hours = total_count + new_hours;
                                                    user_hr_cell.innerHTML = user + ': ' + new_user_hours;
                                                    total_hr_cell.innerHTML = 'Total Hrs: ' + new_total_hours;
                                                }
                                                hours_el.value = '';
                                                op_note_el.value = '';
                                                top_el.setAttribute('work_hour_code', work_hour.code);
                                                if(popper == 'popup'){
                                                    if(!is_billable){
                                                        spt.popup.close(spt.popup.get_popup(bvr.src_el));
                                                    }else{
                                                        //Here need to load the equipment wdg, pass in the work_hour_code
                                                        eq_row.style.display = 'table-row';
                                                        spt.api.load_panel(eq_cell, 'operator_view.WorkOrderEquipmentWdg', {'work_hour_code': work_hour.code})
                                                    }
                                                }
                                            }else{
                                                bad_hours = true;
                                            }
                                        }else{
                                            bad_hours = true;
                                        }
                                    }else{
                                        bad_hours = true;
                                    }
                                }else{
                                    bad_hours = true;
                                }
                            }else{
                                bad_hours = true;
                            }
                            if(bad_hours){
                                spt.alert('Numbers only please.');
                            }
                              
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
        ''' % (title_code, task_code, search_id, user_name, pop)}
        return behavior

    def get_change_title_behavior(my, title_code):
        behavior = {'css_class': 'clickme', 'type': 'change', 'cbjs_action': '''        
                        try{
                            var title_code = '%s';
                            var top_el = spt.api.get_parent(bvr.src_el, '.houradd_' + title_code);
                            client_pull = top_el.getElementById('client_pull');
                            scheduler_pull = top_el.getElementById('scheduler_pull')
                            tcode = bvr.src_el.value;
                            if(tcode != ''){
                                var server = TacticServerStub.get();
                                order = server.eval("@SOBJECT(twog/title['code','" + tcode + "'].twog/order)")[0]; 
                                scheduler_pull.value = order.login;
                                client_pull.value = order.client_code;
                            }
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
        ''' % title_code}
        return behavior

    def get_change_scheduler_behavior(my, title_code):
        behavior = {'css_class': 'clickme', 'type': 'change', 'cbjs_action': '''        
                        try{
                            var title_code = '%s';
                            var top_el = spt.api.get_parent(bvr.src_el, '.houradd_' + title_code);
                            client_pull = top_el.getElementById('client_pull');
                            scheduler_pull = top_el.getElementById('scheduler_pull')
                            sched = bvr.src_el.value;
                            if(sched == 'In House'){
                                var server = TacticServerStub.get();
                                client = server.eval("@SOBJECT(twog/client['name','2G Digital Post'])")[0];
                                client_pull.value = client.code;
                            }
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
        ''' % title_code}
        return behavior
    
    def get_display(my):
        client_pull = SelectWdg('client_pull')
        client_pull.add_attr('id','client_pull')
        client_pull.append_option('--Select--','')
        scheduler_pull = SelectWdg('scheduler_pull')
        scheduler_pull.add_attr('id','scheduler_pull')
        scheduler_pull.append_option('--Select--','')
        scheduler_pull.append_option('In House','In House')
        title_pull = SelectWdg('title_pull')
        title_pull.add_attr('id','title_pull')
        title_pull.append_option('--Select--','')
        title_code = ''
        client_code = ''
        scheduler = ''
        work_summary = ''
        user_name = ''
        pop = ''
        task_code = ''
        search_id = ''
        if 'popup' in my.kwargs.keys():
            title_codes = my.server.eval("@GET(twog/title['@ORDER_BY','code'].code)")
            pop = 'popup'
            title_code = 'STATIC'
        if 'task' in my.kwargs.keys():
            task = my.kwargs.get('task')
            work_summary = task.get('process')
            task_code = task.get('code')
            search_id = task.get('id')
            work_order_code = task.get('lookup_code')
            title = my.server.eval("@SOBJECT(twog/title['code','%s'])" % task.get('title_code'))[0]
            title_code = title.get('code')
            order_code = title.get('order_code')
            title_codes = my.server.eval("@GET(twog/title['order_code','%s']['@ORDER_BY','code'].code)" % order_code)
            order = my.server.eval("@SOBJECT(twog/order['code','%s'])" % order_code)[0]
            client_code = order.get('client_code')
            client_name = order.get('client_name')
            scheduler = order.get('login')
        if 'process' in my.kwargs.keys():
            work_summary = my.kwargs.get('process')
        if 'user_name' in my.kwargs.keys():
            user_name = my.kwargs.get('user_name')
        if user_name in [None,'']:
            from pyasm.common import Environment
            login_obj = Environment.get_login()
            user_name = login_obj.get_login()

        for tcode in title_codes:
            title_pull.append_option(tcode, tcode)
        if title_code not in [None,'','STATIC']:
            title_pull.set_value(title_code)
        tpull_behavior = my.get_change_title_behavior(title_code)
        title_pull.add_behavior(tpull_behavior)

        clients = my.server.eval("@SOBJECT(twog/client['@ORDER_BY','name'])")
        for c in clients:
            client_pull.append_option(c.get('name'), c.get('code'))
        if client_code not in [None,'']:
            client_pull.set_value(client_code)
        schedulers = my.server.eval("@SOBJECT(sthpw/login_in_group['login_group','in','scheduling|scheduling supervisor'].sthpw/login['license_type','user'])")
        for s in schedulers:
            scheduler_pull.append_option(s.get('login'), s.get('login'))
        if scheduler not in [None,'']:
            scheduler_pull.set_value(scheduler)
        scheduler_pull.add_behavior(my.get_change_scheduler_behavior(title_code))

        table = Table()
        table.add_attr('class','houradd_%s' % title_code)
        table.add_attr('id','houradd_%s' % title_code)
        trow = table.add_row()
        trow.add_attr('id','trow')
        table.add_cell('Title: ')
        table.add_cell(title_pull)
        crow = table.add_row()
        crow.add_attr('id','crow')
        table.add_cell('Client: ')
        table.add_cell(client_pull)
        srow = table.add_row()
        srow.add_attr('id','srow')
        table.add_cell('Scheduler: ')
        table.add_cell(scheduler_pull)
        chrow = table.add_row()
        chrow.add_attr('id','chrow')
        crunch_tbl = Table()
        crunch_tbl.add_row()
        hrtxt = TextWdg('hours_txt')
        hrtxt.add_attr('id','hours_txt')
        hrtxt.add_attr('maxlength','5')
        hrtxt.add_attr('size','5')
        crunch_tbl.add_cell(hrtxt)
        if 'popup' in my.kwargs.keys():
            crunch_tbl.add_cell('&nbsp;&nbsp;&nbsp;')
            crunch_tbl.add_cell('Billable?')
            billable_check = CheckboxWdg('billable_check')
            billable_check.add_attr('id','billable_check')
            #billable_check.set_persistence()
            billable_check.set_value(True)
            crunch_tbl.add_cell(billable_check)
        else:
            all_hours = my.server.eval("@SOBJECT(sthpw/work_hour['task_code','%s'])" % task_code)
            total_hours = 0
            user_hours = 0
            for ah in all_hours:
                total_hours = total_hours + float(ah.get('straight_time'))
                if ah.get('login') == user_name:
                    user_hours = user_hours + float(ah.get('straight_time'))
            small_tbl = Table()
            small_tbl.add_row()
            user_hr = small_tbl.add_cell('%s Hrs: %s' % (user_name, user_hours))
            user_hr.add_attr('id','user_hr')
            user_hr.add_style('font-size: 9px;')
            small_tbl.add_row()
            total_hr = small_tbl.add_cell('Total Hrs: %s' % (total_hours)) 
            total_hr.add_attr('id','total_hr')
            total_hr.add_style('font-size: 9px;')
            crunch_tbl.add_cell('&nbsp;&nbsp;')
            crunch_tbl.add_cell(small_tbl)
        adh = table.add_cell('Add Hours: ')
        adh.add_attr('nowrap','nowrap')
        ll = table.add_cell(crunch_tbl)
        wdrow = table.add_row()
        wdrow.add_attr('id','wdrow')
        wd = table.add_cell('Work Description: ')
        wd.add_attr('nowrap','nowrap')
        table.add_cell('<input type="text" value="%s" id="summary_txt"/>' % work_summary)
        orow = table.add_row()
        orow.add_attr('id','orow')
        opn = table.add_cell('Explanation (if needed): ')
        opn.add_attr('nowrap','nowrap')
        table.add_cell('<textarea id="op_note" cols="25" rows="3" ></textarea>')
        subrow = table.add_row()
        subrow.add_attr('id','subrow')
        lil_tbl = Table()
        lil_tbl.add_row()
        one = lil_tbl.add_cell()
        one.add_attr('width','40%%')
        submit_cell = lil_tbl.add_cell('<input type="button" value="Submit"/>') 
        submit_cell.add_attr('align','center')
        submit_behavior = my.get_submit_behavior(title_code, task_code, search_id, user_name, pop) 
        #submit_change = submit_behavior
        #submit_change['type'] = 'change'
        #hrtxt.add_behavior(submit_change)
        submit_cell.add_behavior(submit_behavior)
        two = lil_tbl.add_cell()
        two.add_attr('width','40%%')
        longboy = table.add_cell(lil_tbl)
        longboy.add_attr('colspan','2')
        if 'popup' not in my.kwargs.keys():
            trow.add_style('display: none;')
            crow.add_style('display: none;')
            srow.add_style('display: none;')
            wdrow.add_style('display: none;')
            wrapped = TitleBarWrap(htmlelement=table)
            table = wrapped.get_title_wrap('Work Order Hours')
        else:
            eq_row = table.add_row()
            eq_row.add_attr('id','eq_row')
            eq_row.add_style('display: none;')
            eq_cell = table.add_cell()
            eq_cell.add_attr('id','eq_cell')
            eq_cell.add_attr('colspan','2')
        
        return table

class WorkOrderEquipmentWdg(BaseRefreshWdg):
    def init(my):
        from client.tactic_client_lib import TacticServerStub
        my.server = TacticServerStub.get()
        my.wo_code = ''
        my.wo_name = ''
        my.wh_code = ''
        my.equipment = []
        my.is_popup = 'false'
        if 'work_order_code' in my.kwargs.keys():
            my.wo_code = my.kwargs.get('work_order_code')
            my.wo_name = my.kwargs.get('work_order_name')
            my.equipment = my.server.eval("@SOBJECT(twog/equipment_used['work_order_code','%s'])" % my.wo_code)
        if 'work_hour_code' in my.kwargs.keys():
            my.wh_code = my.kwargs.get('work_hour_code')
            my.is_popup = 'true'
            my.equipment = my.server.eval("@SOBJECT(twog/equipment_used['work_order_code','%s'])" % my.wh_code)
        
   
    def get_change_behavior(my, eq_sk):
        behavior = {'css_class': 'clickme', 'type': 'change', 'cbjs_action': '''        
                        try{
                          var server = TacticServerStub.get();
                          eq_sk = '%s';
                          add_hours = bvr.src_el.value;
                          bvr.src_el.value = '';
                          bad_num = false;
                          if(add_hours != ''){
                              if(add_hours != 0){
                                  if(add_hours != '0'){
                                      if(add_hours != null){
                                          if(!(isNaN(add_hours))){
                                              eq = server.get_by_search_key(eq_sk);
                                              current_hours = eq.actual_duration;
                                              if(current_hours == '' || current_hours == null){
                                                  current_hours = 0;
                                              }
                                              new_hours = parseFloat(current_hours) + parseFloat(add_hours);
                                              server.update(eq_sk, {'actual_duration': new_hours});
                
                                              var top_el = spt.api.get_parent(bvr.src_el, '.ov_eq');
                                              actual_el = top_el.getElementById('actual_' + eq_sk);
                                              actual_el.innerHTML = 'Actual: ' + new_hours;
                                              horh = 'hours';
                                              if(add_hours == '1'){
                                                  horh = 'hour';
                                              }
                                          }else{
                                              bad_num = true;
                                          }
                                      }else{
                                          bad_num = true;
                                      }
                                  }else{
                                      bad_num = true;
                                  }
                              }else{
                                  bad_num = true;
                              }
                          }else{
                              bad_num = true;
                          }
                          if(bad_num){
                              spt.alert('Numbers only please.');
                          }
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
        ''' % (eq_sk)}
        return behavior

    def get_click_behavior(my, eq_sk):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                          var server = TacticServerStub.get();
                          eq_sk = '%s';
                          var top_el = spt.api.get_parent(bvr.src_el, '.ov_eq');
                          add_box = top_el.getElementById('add_' + eq_sk);
                          add_hours = add_box.value;
                          add_box.value = ''; 
                          bad_num = false;
                          if(add_hours != ''){
                              if(add_hours != 0){
                                  if(add_hours != '0'){
                                      if(add_hours != null){
                                          if(!(isNaN(add_hours))){
                                              eq = server.get_by_search_key(eq_sk);
                                              current_hours = eq.actual_duration;
                                              if(current_hours == '' || current_hours == null){
                                                  current_hours = 0;
                                              }
                                              new_hours = parseFloat(current_hours) + parseFloat(add_hours);
                                              server.update(eq_sk, {'actual_duration': new_hours});
                                              actual_el = top_el.getElementById('actual_' + eq_sk);
                                              actual_el.innerHTML = 'Actual: ' + new_hours;
                                              horh = 'hours';
                                              if(add_hours == '1'){
                                                  horh = 'hour';
                                              }
                                          }else{
                                              bad_num = true;
                                          }
                                      }else{
                                          bad_num = true;
                                      }
                                  }else{
                                      bad_num = true;
                                  }
                              }else{
                                  bad_num = true;
                              }
                          }else{
                              bad_num = true;
                          }
                          if(bad_num){
                              spt.alert('Numbmers only please.');
                          }
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
        ''' % (eq_sk)}
        return behavior

    def get_add_behavior(my, wo_code, wo_name, is_popup):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                            var wo_code = '%s';
                            var wo_name = '%s';
                            var is_popup = '%s';
                            data = {'work_order_code': wo_code};
                            if(is_popup == 'true'){
                                data['popup'] = 'true';
                            }
                            spt.panel.load_popup('Add Equipment to ' + wo_name, 'operator_view.EquipmentUsedMultiAdderWdg', data);
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
        ''' % (wo_code, wo_name, is_popup)}
        return behavior

    def get_done_behavior(my):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                            var top_el = spt.api.get_parent(bvr.src_el, '.houradd_STATIC');
                            spt.popup.close(spt.popup.get_popup(bvr.src_el));
                            spt.api.load_panel(top_el, 'operator_view.WorkOrderHoursWdg', {'popup': 'true'})
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
        '''}
        return behavior
 

    def get_display(my):
        table = Table()
        table.add_attr('class','ov_eq')
        table.add_style('background-color: #FFFFFF;')
        unit_lookup = {'hr': 'Hour', 'mb': 'MB', 'gb': 'GB', 'tb': 'TB'}
        if my.is_popup == 'true':
            hour = my.server.eval("@SOBJECT(sthpw/work_hour['code','%s'])" % my.wh_code)[0]
            table.add_row()
            c1 = table.add_cell('')
            c1.add_attr('width','20%%')
            title_cell = table.add_cell('<b>Add Equipment to the %s hours you just added?</b>' % hour.get('straight_time'))
            title_cell.add_attr('nowrap','nowrap')
            title_cell.add_attr('align','center')
            title_cell.add_attr('width','60%%')
            c2 = table.add_cell('')
            c2.add_attr('width','20%%')
            
        for eq in my.equipment:
            eq_sk = eq.get('__search_key__')
            units = eq.get('units')
            if units == 'items':
                units = 'hr'
            table.add_row()
            top_cell = table.add_cell('%s | Quantity: %s' % (eq.get('name'), int(eq.get('expected_quantity'))))
            top_cell.add_attr('colspan','5')
            top_cell.add_attr('align','left')
            top_cell.add_style('background-color: #bbbbbb;')
            table.add_row()
            dur = eq.get('actual_duration')
            if dur in [None,'']:
                dur = 0
            ad = None
            if units == 'length':
                ad = table.add_cell('Length: %s' % eq.get('length'))
            else:
                ad = table.add_cell('Actual %ss: %s' % (unit_lookup[units] , dur))
            ad.add_attr('id','actual_%s' % eq_sk)
            ad.add_attr('nowrap','nowrap')
            spacer = table.add_cell('&nbsp;')
            spacer.add_attr('width','100%%')
            if units != 'length':
                ah = table.add_cell("Add %ss: " % unit_lookup[units])
                ah.add_attr('nowrap','nowrap')
                txt = TextWdg('eq_hours_%s' % eq.get('code'))
                txt.add_attr('id','add_%s' % eq_sk)
                change_behavior = my.get_change_behavior(eq_sk)
                txt.add_behavior(change_behavior)
                hour_txt = table.add_cell(txt)
                action_bttn = table.add_cell('<img src="/context/icons/custom/plus_bw.png" />')
                click_behavior = my.get_click_behavior(eq_sk)
                action_bttn.add_style('cursor: pointer;')
                action_bttn.add_behavior(click_behavior)
        table.add_row()
        fc = table.add_cell('&nbsp;')
        fc.add_attr('width', '20%%')
        middle_cell = table.add_cell('<input type="button" value="Add/Edit Equipment" />')
        middle_cell.add_attr('colspan','3')
        middle_cell.add_attr('align','center')
        if my.wh_code != '':
            my.wo_code = my.wh_code
        middle_cell.add_behavior(my.get_add_behavior(my.wo_code, my.wo_name, my.is_popup)) 
        lc = table.add_cell('&nbsp;')
        lc.add_attr('width', '20%%')
        if my.is_popup == 'true':
            table.add_row()
            table.add_cell('&nbsp;')
            table.add_row()
            table.add_cell('&nbsp;')
            table.add_row()
            pad1 = table.add_cell(' ')
            pad1.add_attr('width', '20%%')
            donebutt = table.add_cell('<input type="button" value="Done With Equipment" />')
            donebutt.add_attr('colspan','3')
            donebutt.add_attr('align','center')
            donebutt.add_behavior(my.get_done_behavior())
            pad2 = table.add_cell(' ')
            pad2.add_attr('width', '20%%')
        wrapped = TitleBarWrap(htmlelement=table)
        table = wrapped.get_title_wrap('Work Order Equipment')
            
        return table

class EquipmentUsedMultiAdderWdg(BaseRefreshWdg):
    def init(my):
        from client.tactic_client_lib import TacticServerStub
        my.server = TacticServerStub.get()
        my.work_order_code = ''
        my.wo_codes = ''
        my.wo_name = ''
        my.is_popup = 'false'
        my.width = '1000px'
        my.height = '300px'
        my.submit_eu = "<input type='button' value='Submit'/>"
        my.x_butt = "<img src='/context/icons/common/BtnKill_Black.gif' title='Delete' name='Delete'/>" 
    
    def get_save_multi_eq_changes_behavior_for_single(my, work_order_code, work_order_name):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                           var work_order_code = '%s';
                           var work_order_name = '%s';
                           var class_name = 'order_builder.TaskInspectWdg';
                           kwargs = {
                                           'code': work_order_code, 
                                           'name': work_order_name
                                   };
                           spt.popup.close(spt.popup.get_popup(bvr.src_el));
                           findstr = 'taskinspect_' + work_order_code;
                           task_panel = document.getElementsByClassName(findstr)[0];
                           spt.api.load_panel(task_panel, class_name, kwargs);
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         ''' % (work_order_code, work_order_name)}
        return behavior

    def get_save_multi_eq_changes_behavior(my, work_order_code, work_order_name, definer, title_code, parent_view):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                           var server = TacticServerStub.get();
                           var work_order_code = '%s';
                           var work_order_name = '%s';
                           var definer = '%s';
                           var title_code = '%s';
                           var parent_view = '%s';
                           wos = definer.split(',');
                           top_el = null;
                           inc_el = null;
                           if(wos.length == 1){
                               top_el = document.getElementsByClassName('panel_' + work_order_code);
                           }else{
                               for(var r = 0; r < wos.length; r++){
                                   top_el_tmp = document.getElementsByClassName('panel_' + wos[r]);
                                   if(top_el_tmp != null){
                                       r = wos.length - 1;
                                       work_order_code = wos[r];
                                       top_el = top_el_tmp;
                                   }
                               }
                           }
                           find_str = parent_view + '_innerds_' + title_code;
                           incs = document.getElementsByClassName(find_str);
                           for(var r = 0; r < incs.length; r++){
                               spt.api.load_panel(incs[r], 'operator_view.IncompleteWOWdg', {'search_type': 'twog/title', 'code': title_code, 'parent_view': parent_view});
                           } 
                           if(wos.length < 2){ 
                               if(top_el.length > 0){
                                   top_el = top_el[0];
                                   eq_el = top_el.getElementsByClassName('eq_panel_' + work_order_code)[0];
                                   spt.api.load_panel(eq_el, 'operator_view.WorkOrderEquipmentWdg', {'work_order_code': work_order_code, 'work_order_name': work_order_name})
                               }else{
                                   top_el = document.getElementById('houradd_STATIC');
                                   if(top_el){
                                       eq_el = top_el.getElementById('eq_cell');
                                       eq_row = top_el.getElementById('eq_row');
                                       spt.api.load_panel(eq_el, 'operator_view.WorkOrderEquipmentWdg', {'work_order_code': work_order_code, 'work_order_name': ''})
                                       eq_row.style.display = 'table-row';
                                   }
                               }
                           }else{
                               if(top_el.length > 0){
                                   top_el = top_el[0];
                                   eq_el = top_el.getElementsByClassName('eq_panel_' + work_order_code)[0];
                                   spt.api.load_panel(eq_el, 'operator_view.WorkOrderEquipmentWdg', {'work_order_code': work_order_code, 'work_order_name': work_order_name})
                               }
                           }
                           spt.popup.close(spt.popup.get_popup(bvr.src_el));
                           // then reload operator_view_titles_incomplete_tasks_wdg_TITLECODE
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         ''' % (work_order_code, work_order_name, definer, title_code, parent_view)}
        return behavior

    def get_add_eq_from_multi_behavior(my, type_base, work_order_code, definer, title_code, parent_view):
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
                           var type_base = '%s';
                           var work_order_code = '%s';
                           var definer = '%s';
                           var title_code = '%s';
                           var parent_view = '%s';
                           var top_el = document.getElementsByClassName('equipment_used_multi_adder_top_' + definer)[0];
                           my_selects = top_el.getElementsByTagName('select');
                           my_code = '';
                           my_units = '';
                           my_name = '';
                           my_length = '';
                           find_str = parent_view + '_innerds_' + title_code;
                           incs = document.getElementsByClassName(find_str);
                           work_order_codes = [];
                           if(incs.length > 0){
                               incs = incs[0];
                               if(parent_view != 'operator_view_titles'){
                                   inputs = incs.getElementsByTagName('input');
                                   for(var r = 0; r < inputs.length; r++){
                                       if(inputs[r].type == 'checkbox' && (inputs[r].getAttribute('name').indexOf('select_all_') == -1)){
                                           wo_code = inputs[r].getAttribute('wo_code');
                                           if(inputs[r].checked){
                                               if(wo_code != '' && wo_code != null && !(wo_code in oc(work_order_codes))){
                                                   work_order_codes.push(wo_code);
                                               }
                                           }
                                       }
                                   } 
                               }
                           }
                           if(work_order_codes.length == 0){
                               if(parent_view != 'operator_view_titles'){
                                   if(incs.length > 0){
                                       incs = incs[0];
                                   }
                                   inputs = incs.getElementsByClassName('iwow_checkbox');
                                   for(var r = 0; r < inputs.length; r++){
                                       if(inputs[r].getAttribute('name').indexOf('select_all_') == -1){
                                           wo_code = inputs[r].getAttribute('wo_code');
                                           if(inputs[r].getAttribute('checked') == 'true'){
                                               if(wo_code != '' && wo_code != null){
                                                   work_order_codes.push(wo_code);
                                               }
                                           }
                                       }
                                   } 
                               }else{
                                   work_order_codes.push(work_order_code);
                               }
                           }
                           if(work_order_codes.length == 0){
                               if(definer.indexOf('WORK_ORDER') != -1 && definer.indexOf(',') == -1){
                                   work_order_codes.push(definer);
                               }
                           }
                           for(var r = 0; r < my_selects.length; r++){
                               if(my_selects[r].getAttribute('name') == type_base + '_select'){
                                   my_code = my_selects[r].value;
                                   my_name = my_selects[r].options[my_selects[r].selectedIndex].text;
                               }
                               if(my_selects[r].getAttribute('name') == type_base + '_units_select'){
                                   my_units = my_selects[r].value;
                               }
                               if(my_selects[r].getAttribute('name') == type_base + '_length'){
                                   my_length = my_selects[r].value;
                               }
                           }
                           if(my_name.indexOf('WORKSTATION') != -1 || my_name.indexOf('MACHINEROOM') != -1){
                               my_units = 'hr';
                           }else if(my_name.indexOf('MEDIA') != -1 && my_name.indexOf('MONORAIL') == -1){
                               my_units = 'length';
                           }
                           if(my_code != 'NOTHINGXsXNOTHING'){
                               if(my_units == 'gb' || my_units == 'tb'){
                                   quantity = 1
                               }else{
                                   quant_el = top_el.getElementsByClassName(type_base + '_quant')[0];
                                   quantity = quant_el.value;
                               }
                               if(quantity == '' || quantity == null){
                                   quantity = 1;
                               }
                               if(work_order_codes.length == 0){
                                   work_order_codes.push(work_order_code);
                               }
                               //work_order_codes_str = work_order_codes.join(',');
                               work_order_codes_str = '';
                               for(var r = 0; r < work_order_codes.length; r++){
                                   if(work_order_codes_str == ''){
                                       work_order_codes_str = work_order_codes[r];
                                   }else if(work_order_codes_str.indexOf(work_order_codes[r]) == -1){
                                       work_order_codes_str = work_order_codes_str + ',' + work_order_codes[r];
                                   }
                               }
                               go_ahead = false
                               if(work_order_code != '' && work_order_code != null){
                                   go_ahead = true;
                               }else if(work_order_codes_str == ''){
                                   go_ahead = false;
                                   spt.alert('Please select the work order you want to add equipment to by clicking on the corresponding checkbox'); 
                               }else if(confirm("Do you want to add this equipment to " + work_order_codes_str + "?")){
                                   go_ahead = true;
                                   splits = work_order_codes_str.split(',');
                                   if(splits.length == 1){
                                       work_order_code = splits[0];
                                   }
                               }
                               if(go_ahead){
                                   for(var r = 0; r < work_order_codes.length; r++){
                                       data = {'work_order_code': work_order_codes[r], 'expected_quantity': quantity, 'units': my_units, 'name': my_name, 'equipment_code': my_code};
                                       if(my_units != 'length'){
                                           duration_el = top_el.getElementsByClassName(type_base + '_duration')[0];
                                           duration = duration_el.value;
                                           if(duration != '' && duration != null){
                                               data['expected_duration'] = duration;
                                               data['actual_duration'] = duration;
                                           }
                                       }else{
                                           data['length'] = my_length;
                                       }
                                       server.insert('twog/equipment_used', data);
                                   }
                                   if(parent_view == 'task_view'){
                                       spt.api.load_panel(top_el, 'operator_view.EquipmentUsedMultiAdderWdg', {'work_order_code': work_order_code, 'parent_view': parent_view}); 
                                   }else{
                                       if(work_order_code != '' && work_order_code != null){
                                           spt.api.load_panel(top_el, 'operator_view.EquipmentUsedMultiAdderWdg', {'work_order_code': work_order_code, 'parent_view': parent_view}); 
                                       }else{
                                           spt.api.load_panel(top_el, 'operator_view.EquipmentUsedMultiAdderWdg', {'wo_codes': work_order_codes_str, 'parent_view': parent_view}); 
                                       }
                                       if(parent_view.indexOf('operator_view_titles') != -1){
                                           spt.api.load_panel(incs, 'operator_view.incomplete_wo_wdg.IncompleteWOWdgInnerds', {'code': title_code, 'parent_view': parent_view, 'search_type': 'twog/title'}); 
                                       }
                                   }
                               }
                           }else{
                               spt.alert('You must select the type of equipment you want to add.');
                           }
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         ''' % (type_base, work_order_code, definer, title_code, parent_view)}
        return behavior

    def get_eq_multi_kill_behavior(my, eqsk, eqname, definer):  
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                           var server = TacticServerStub.get();
                           var eqsk = '%s';
                           var eqname = '%s';
                           var definer = '%s';
                           if(confirm('Do you really want to delete ' + eqname + ' from this list?')){
                              var top_el = document.getElementsByClassName('equipment_used_multi_adder_top_' + definer)[0];
                              data = {}
                              if(top_el.getAttribute('work_order_code') != '' && top_el.getAttribute('work_order_code') != null){
                                  data['work_order_code'] = top_el.getAttribute('work_order_code');
                              }else{
                                  data['wo_codes'] = top_el.getAttribute('wo_codes');
                              }
                              server.delete_sobject(eqsk);
                              spt.api.load_panel(top_el, 'operator_view.EquipmentUsedMultiAdderWdg', data); 
                           } 
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         ''' % (eqsk, eqname, definer)}
        return behavior

    def get_change_length_pull_behavior(my, definer):
        behavior = {'css_class': 'clickme', 'type': 'change', 'cbjs_action': '''        
                        try{
                           var server = TacticServerStub.get();
                           var definer = '%s';
                           var eq_code = bvr.src_el.value;
                           lengths = server.eval("@GET(twog/equipment['code','" + eq_code + "'].lengths)")[0].split(',');
                           new_inner = ''
                           for(var r =0; r < lengths.length; r++){
                               new_inner = new_inner + '<option value="' + lengths[r] + '">' + lengths[r] + '</option>';
                           }
                           var top_el = document.getElementsByClassName('equipment_used_multi_adder_top_' + definer)[0];
                           my_selects = top_el.getElementsByTagName('select');
                           for(var r = 0; r < my_selects.length; r++){
                               if(my_selects[r].getAttribute('name') == 'media_length'){
                                   my_length_pull = my_selects[r];
                               }
                           }
                           my_length_pull.innerHTML = new_inner;
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         ''' % (definer)}
        return behavior

    def get_display(my):   
        definer = ''
        title_code = ''
        alt_wdg_wo_code = ''
        parent_view = 'operator_view_titles'
        if 'parent_view' in my.kwargs.keys():
            parent_view = str(my.kwargs.get('parent_view'))
        if 'alt_wdg' in my.kwargs.keys():
            alt_wdg_wo_code = str(my.kwargs.get('alt_wdg'))
            definer = alt_wdg_wo_code
            my.work_order_code = definer
        elif 'work_order_code' in my.kwargs.keys():
            my.work_order_code = str(my.kwargs.get('work_order_code'))
            title_code = my.server.eval("@GET(twog/work_order['code','%s'].title_code)" % (my.work_order_code))[0]
            definer = my.work_order_code
        elif 'wo_codes' in my.kwargs.keys():
            my.wo_codes = str(my.kwargs.get('wo_codes'))
            definer = my.wo_codes
            title_code = my.server.eval("@GET(twog/work_order['code','%s'].title_code)" % (my.wo_codes.split(',')[0]))[0]
        if 'popup' in my.kwargs.keys():
            my.is_popup = 'true'
        wo_sobj = None
        if 'WORK_HOUR' in my.work_order_code:
            wo_sobj = {'process': 'Adding to Hours'}
            my.wo_name = wo_sobj.get('process')
        elif parent_view == 'task_view':
            wo_sobj = my.server.eval("@SOBJECT(twog/work_order['code','%s'])" % my.work_order_code)[0]
            my.wo_name = wo_sobj.get('process')
            wo_eqs = my.server.eval("@SOBJECT(twog/equipment_used['work_order_code','%s'])" % my.work_order_code)
        elif my.wo_codes not in [None,'']:
            #Then do not look at existing equipment, just allow adding?
            wo_eqs = my.server.eval("@SOBJECT(twog/equipment_used['work_order_code','in','%s'])" % my.wo_codes.replace(',','|'))
            my.wo_name = 'Multiple WOs'
        else:
            wo_sobj = my.server.eval("@SOBJECT(twog/work_order['code','%s'])" % my.work_order_code)[0]
            my.wo_name = wo_sobj.get('process')
            wo_eqs = my.server.eval("@SOBJECT(twog/equipment_used['work_order_code','%s'])" % my.work_order_code)
            
        all_equip_expr = "@SOBJECT(twog/equipment['@ORDER_BY','name desc'])"
        all_equip = my.server.eval(all_equip_expr)
        table = Table()
        table.add_attr('class', 'equipment_used_multi_adder_top_%s' % definer)
        if my.work_order_code not in [None,'']:
            table.add_attr('work_order_code', my.work_order_code)
        else:
            table.add_attr('wo_codes', my.wo_codes)
        list_table = Table()
        list_table.add_style('cellpadding: 10px;')
        for woeq in wo_eqs:
            list_table.add_row()
            killer = list_table.add_cell(my.x_butt)
            killer.add_style('cursor: pointer;')
            killer.add_behavior(my.get_eq_multi_kill_behavior(woeq.get('__search_key__'), woeq.get('name'), definer))
            type_eq = ''
            eq_parent = my.server.eval("@SOBJECT(twog/equipment['code','%s'])" % woeq.get('equipment_code'))
            if eq_parent:
                eq_parent = eq_parent[0]
                type_eq = eq_parent.get('type')
                if type_eq == 'Equipment':
                    type_eq = 'EQUIP'
                elif type_eq == 'Storage':
                    type_eq = 'STOR'
                elif type_eq == 'Media':
                    type_eq = 'MEDIA'

            list_table.add_cell('%s:' %  type_eq)
            name_to_use = woeq.get('name')
            if woeq.get('length') not in [None,'']:
                name_to_use = '%s: %s' % (name_to_use, woeq.get('length'))
            solid1 = list_table.add_cell('<input type="text" value="%s" disabled="disabled" size="40"/>' % name_to_use)
            solid1.add_style('width: 100px;')
            solid2 = list_table.add_cell('<input type="text" value="UNITS: %s" disabled="disabled" style="width: 100px;"/>' % woeq.get('units'))
            solid2.add_style('width: 50px;')
            solid4 = None
            if woeq.get('length') not in [None,'']:
                solid4 = list_table.add_cell('<input type="text" value="LENGTH: %s" disabled="disabled" style="width: 120px;"/>' % woeq.get('length'))
            else:
                if woeq.get('units') in ['mb','gb','tb']:
                    solid4 = list_table.add_cell('<input type="text" value="AMT: %s" disabled="disabled" style="width: 120px;"/>' % woeq.get('expected_duration'))
                else:    
                    solid4 = list_table.add_cell('<input type="text" value="N/A" disabled="disabled" style="width: 120px;"/>')
            solid3 = list_table.add_cell('<input type="text" value="QUANT: %s" disabled="disabled" style="width: 120;"/>' % woeq.get('expected_quantity'))
            solid3.add_style('width: 80px;')
            list_table.add_cell(woeq.get('work_order_code'))
        units = ['items','mb','gb','tb']
        table.add_row()
        table.add_cell(list_table)
        ctable = Table()
        ctable.add_row()
        ctable.add_cell(' ')
        ctable.add_cell('Name')
        ctable.add_cell('Length')
        ctable.add_cell('Quantity')
        ctable.add_cell(' ')

        ctable.add_row()
        ctable.add_cell('Media: ')
        media_sel = SelectWdg('media_select')
        media_sel.add_style('width: 370px;')
        media_sel.add_behavior(my.get_change_length_pull_behavior(definer))
        media_sel.append_option('--Select--','NOTHINGXsXNOTHING')
        for eq in all_equip:
            if eq.get('type') == 'Media':
                media_sel.append_option(eq.get('name'),eq.get('code'))
        ctable.add_cell(media_sel)
        len_sel = SelectWdg('media_length')
        len_sel.add_style('width: 77px;')
        len_sel.append_option('Name 1st','NOTHINGXsXNOTHING')
        ctable.add_cell(len_sel)
        ctable.add_cell('<input type="text" class="media_quant" value="1" style="width: 42px;"/>')
        create_media = ctable.add_cell('<input type="button" value="Create"/>')
        create_media.add_behavior(my.get_add_eq_from_multi_behavior('media',my.work_order_code, definer, title_code, parent_view))

        ctable.add_row()
        ctable.add_cell(' ')
        ctable.add_cell('Name')
        ctable.add_cell('Duration (hrs)')
        ctable.add_cell('Quantity')
        ctable.add_cell(' ')

        ctable.add_row()
        ctable.add_cell('Equip: ')
        equip_sel = SelectWdg('equip_select')
        equip_sel.add_style('width: 370px;')
        equip_sel.append_option('--Select--','NOTHINGXsXNOTHING')
        for eq in all_equip:
            if eq.get('type') == 'Equipment':
                equip_sel.append_option(eq.get('name'),eq.get('code'))
        ctable.add_cell(equip_sel)
        ctable.add_cell('<input type="text" class="equip_duration" style="width: 77px;"/>')
        ctable.add_cell('<input type="text" class="equip_quant" value="1" style="width: 42px;"/>')
        create_equip = ctable.add_cell('<input type="button" value="Create"/>')
        create_equip.add_behavior(my.get_add_eq_from_multi_behavior('equip',my.work_order_code, definer, title_code, parent_view))

        ctable.add_row()
        ctable.add_cell(' ')
        ctable.add_cell('Name')
        ctable.add_cell('Units')
        ctable.add_cell('Size')
        ctable.add_cell(' ')

        ctable.add_row()
        ctable.add_cell('Storage: ')
        stor_sel = SelectWdg('stor_select')
        stor_sel.add_style('width: 370px;')
        stor_sel.append_option('--Select--','NOTHINGXsXNOTHING')
        for eq in all_equip:
            if eq.get('type') == 'Storage':
                stor_sel.append_option(eq.get('name'),eq.get('code'))
        ctable.add_cell(stor_sel)
        stor_units_sel = SelectWdg('stor_units_select')
        stor_units_sel.add_style('width: 77px;')
        stor_units_sel.append_option('gb','gb')
        stor_units_sel.append_option('tb','tb')
        ctable.add_cell(stor_units_sel)
        ctable.add_cell('<input type="text" class="stor_duration"  style="width: 42px;"/>')
        #ctable.add_cell('<input type="text" class="stor_quant" value="1" style="width: 42px;"/>')
        create_media = ctable.add_cell('<input type="button" value="Create"/>')
        create_media.add_behavior(my.get_add_eq_from_multi_behavior('stor',my.work_order_code, definer, title_code, parent_view))
        table.add_row()
        table.add_cell(ctable)
        table.add_row()
        tbl2 = Table()
        tbl2.add_row()
        save_changes = tbl2.add_cell('<input type="button" value="Save Changes"/>')
        if parent_view == 'task_view':
            save_changes.add_behavior(my.get_save_multi_eq_changes_behavior_for_single(my.work_order_code, my.wo_name))
        else:
            save_changes.add_behavior(my.get_save_multi_eq_changes_behavior(my.work_order_code, my.wo_name, definer, title_code, parent_view))
        t22 = tbl2.add_cell(' ')
        t22.add_attr('width','100%s' % '%')
        table.add_cell(tbl2)
        return table

class StatusAndAssignmentWdg(BaseRefreshWdg):
    def init(my):
        from client.tactic_client_lib import TacticServerStub
        my.server = TacticServerStub.get()
        my.work_order_code = ''
        my.task = None
        my.colors = {
          "Assignment": "#fcaf88", 
          "Pending": "#d7d7d7", 
          "In_Progress": "#f5f3a4",
          "In Progress": "#f5f3a4",
          "Waiting": "#ffd97f",
          "Need Assistance": "#fc88bf",
          "Review": "#888bfc",
          "Approved": "#d4b5e7",
          "Completed": "#b7e0a5",
          "Failed QC": "#ff0000",
          "Rejected": "#ff0000",
          "Fix Needed": "#c466a1",
          "On_Hold": "#e8b2b8",
          "On Hold": "#e8b2b8",
          "Client Response": "#ddd5b8",
          "Ready": "#b2cee8",
          "DR In_Progress": "#d6e0a4",
          "DR In Progress": "#d6e0a4",
          "Amberfin01_In_Progress": "#d8f1a8",
          "Amberfin01 In Progress": "#d8f1a8",
          "Amberfin02_In_Progress": "#f3d291",
          "Amberfin02 In Progress": "#f3d291",
          "BATON In_Progress": "#c6e0a4",
          "BATON In Progress": "#c6e0a4",
          "Export In_Progress": "#796999",
          "Export In Progress": "#796999",
          "Need Buddy Check": "#e3701a",
          "Buddy Check In_Progress": "#1aade3",
          "Buddy Check In Progress": "#1aade3",
          "crap": "#e20ff0"
        } 

    def get_status_change_behavior(my, search_key, work_order_code, title_sk, login_name):
        behavior = {'css_class': 'sel_change', 'type': 'change', 'cbjs_action': '''
                function oc(a){
                    var o = {};
                    for(var i=0;i<a.length;i++){
                        o[a[i]]='';
                    }
                    return o;
                }
                try{
                    colors = {
                      "Assignment": "#fcaf88", 
                      "Pending": "#d7d7d7", 
                      "In_Progress": "#f5f3a4",
                      "In Progress": "#f5f3a4",
                      "Waiting": "#ffd97f",
                      "Need Assistance": "#fc88bf",
                      "Review": "#888bfc",
                      "Approved": "#d4b5e7",
                      "Completed": "#b7e0a5",
                      "Failed QC": "#ff0000",
                      "Rejected": "#ff0000",
                      "Fix Needed": "#c466a1",
                      "On_Hold": "#e8b2b8",
                      "On Hold": "#e8b2b8",
                      "Client Response": "#ddd5b8",
                      "Ready": "#b2cee8",
                      "DR In_Progress": "#d6e0a4",
                      "DR In Progress": "#d6e0a4",
                      "Amberfin01_In_Progress": "#d8f1a8",
                      "Amberfin01 In Progress": "#d8f1a8",
                      "Amberfin02_In_Progress": "#f3d291",
                      "Amberfin02 In Progress": "#f3d291",
                      "BATON In_Progress": "#c6e0a4",
                      "BATON In Progress": "#c6e0a4",
                      "Export In_Progress": "#796999",
                      "Export In Progress": "#796999",
                      "Need Buddy Check": "#e3701a",
                      "Buddy Check In_Progress": "#1aade3",
                      "Buddy Check In Progress": "#1aade3",
                      "crap": "#e20ff0"
                    } 
                    var server= TacticServerStub.get();
                    var search_key = '%s';
                    var work_order_code = '%s';
                    var title_sk = '%s';
                    var login_name = '%s';
                    var task_code = search_key.split('code=')[1];
                    var title_code = title_sk.split('code=')[1];
                    var task = server.eval("@SOBJECT(sthpw/task['code','" + task_code + "'])")[0]
                    new_status = bvr.src_el.value;
                    old_status = bvr.src_el.getAttribute('old_status');
                    var group_email_lookup = {'admin': 'administrator@2gdigital.com', 'it': 'IT@2gdigital.com', 'qc': 'QC@2gdigital.com', 'qc_supervisor': 'QC@2gdigital.com', 'compression': 'Compression@2gdigital.com', 'billing_and_accounts_receivable': '2GSales@2gdigital.com', 'audio': 'Audio@2gdigital.com', 'compression_supervisor': 'Compression@2gdigital.com', 'edeliveries': 'Edeliveries@2gdigital.com', 'machine_room': 'MR@2gdigital.com', 'media_vault': 'Mediavault@2gdigital.com', 'media_vault_supervisor': 'Mediavault@2gdigital.com', 'edit_supervisor': 'Editors@2gdigital.com', 'machine_room_supervisor': 'MR@2gdigital.com', 'office_employees': 'jaime.torres@2gdigital.com;adriana.amador@2gdigital.com', 'edit': 'Editors@2gdigital.com', 'sales': '2GSales@2gdigital.com', 'senior_staff': 'fernando.vasquez@2gdigital.com;jaime.torres@2gdigital.com;adriana.amador@2gdigital.com;stephen.buchsbaum@2gdigital.com', 'executives': 'stephen.buchsbaum@2gdigital.com', 'management': 'jaime.torres@2gdigital.com;adriana.amador@2gdigital.com', 'scheduling': 'scheduling@2gdigital.com', 'streamz': 'MR@2gdigital.com;QC@2gdigital.com;Editors@2gdigital.com', 'technical_services': 'IT@2gdigital.com', 'sales_supervisor': '2GSales@2gdigital.com', 'scheduling_supervisor': 'scheduling@2gdigital.com', 'vault': 'Mediavault@2gdigital.com'}
                    server.update(search_key, {'status': new_status});
                    completed_one = false;
                    some_special_statuses = false;
                    some_path_prompts = false;
                    force_response_strings = '';
                    if(new_status in oc(['Rejected','Fix Needed','On Hold','Client Response'])){
                        //Get a forced response as to why
                        //Get production error generated prior to this, if applicable and send production error code to ForceResponseWdg
                        some_special_statuses = true;
                        production_error_code = '';
                        if(new_status in oc(['Rejected','Fix Needed'])){
                            error_entries = server.eval("@SOBJECT(twog/production_error['work_order_code','" + task.lookup_code + "'])")
                            if((error_entries.length > 0)){
                                error_entry = error_entries[error_entries.length - 1];
                                production_error_code = error_entry.code;
                            }
                        }
                        this_row_str = 'MTMX-Prompt:Please tell us why the new status for ' + task.process + ' is going to ' + new_status + 'MTMX-production_error_code:' + production_error_code + 'MTMX-work_order_code:' + task.lookup_code + 'MTMX-process:' + task.process + 'MTMX-new_status:' + new_status + 'MTMX-old_status:' + old_status;
                        if(force_response_strings == ''){
                            force_response_strings = this_row_str;
                        }else{
                            force_response_strings = force_response_strings + 'MTM_NEXT_MTM' + this_row_str;
                        }
                    }else if(old_status in oc(['Rejected','Fix Needed','On Hold','Client Response'])){
                        //Get a forced response as to why
                        //Probably no production error here, so no need to send production error code
                        some_special_statuses = true;
                        production_error_code = '';
                        this_row_str = 'MTMX-Prompt:Please tell us why the new status for ' + task.process + ' is going to ' + new_status + ' from ' + old_status + 'MTMX-production_error_code:' + production_error_code + 'MTMX-work_order_code:' + task.lookup_code + 'MTMX-process:' + task.process + 'MTMX-new_status:' + new_status + 'MTMX-old_status:' + old_status;
                        if(force_response_strings == ''){
                            force_response_strings = this_row_str;
                        }else{
                            force_response_strings = force_response_strings + 'MTM_NEXT_MTM' + this_row_str;
                        }
                    }
                    if(new_status == 'Completed' && task.assigned_login_group in oc(['compression','compression supervisor','machine room','machine room supervisor','audio','edit','edit supervisor'])){
                        this_row_str = 'MTMX-Prompt:Please Enter the Path to the File(s) for ' + task.process + '.\\nStatus went to ' + new_status + ' from ' + old_status + 'MTMX-work_order_code:' + task.lookup_code + 'MTMX-process:' + task.process + 'MTMX-new_status:' + new_status + 'MTMX-old_status:' + old_status;
                        if(force_response_strings == ''){
                            force_response_strings = this_row_str;
                        }else{
                            force_response_strings = force_response_strings + 'MTM_NEXT_MTM' + this_row_str;
                        }
                        some_path_prompts = true;
                        //gotit = false;
                        //file_path = '';
                        //while(!gotit){
                        //    file_path = prompt("Please Enter the Path to the File(s)");
                        //    if(file_path != '' && file_path != null){
                        //        gotit = true;
                        //    }
                        //}
                        //scheduler_email = server.eval("@GET(sthpw/login['login','" + login_name + "'].email)")[0];
                        //ccs = scheduler_email + ';' + group_email_lookup[task.assigned_login_group]; 
                        //ccs = scheduler_email;
                        //server.execute_cmd('operator_view.MakeNoteWdg', {'obj_sk': title_sk, 'header': task.process + ' - Completed', 'note': 'File Path: ' + file_path, 'note_ccs': ccs}); 
                        completed_one = true;
                    }else if(new_status == 'Completed'){
                        completed_one = true;
                    }
                    if(some_special_statuses || some_path_prompts){
                        //Send to ForceResponseWdg
                        add_str = '';
                        if(some_path_prompts){
                            add_str = ' or enter a file path where prompted';
                        } 
                        spt.panel.load_popup('Please tell us why this work order is getting a special status' + add_str, 'operator_view.resetter.ForceResponseWdg', {'string_to_parse': force_response_strings});
                    }
                    top_el = document.getElementsByClassName('panel_' + work_order_code)[0];
                    status_color_el = top_el.getElementById('status_color_block_' + work_order_code);
                    status_color_el.style.backgroundColor = colors[new_status];
                    status_el = top_el.getElementsByClassName('status_panel_' + work_order_code)[0];
                    spt.api.load_panel(status_el, 'operator_view.StatusAndAssignmentWdg', {'work_order_code': work_order_code, 'requires_mastering': status_el.getAttribute('requires_mastering')})
                    if(completed_one){
                        assigned_login_group_view = task.assigned_login_group;
                        assigned_login_group_view = assigned_login_group_view.replace(' supervisor','').replace(' ','_');
                        vlist = ['operator_view_titles','operator_view_titles_' + assigned_login_group_view];
                        inc_wdg = '';
                        parent_view = '';
                        for(var x = 0; x < vlist.length; x++){
                            parent_view = vlist[x];
                            inc_wdg_1 = document.getElementsByClassName(parent_view + '_innerds_' + title_code);
                            for(var r = 0; r < inc_wdg_1.length; r++){
                                if(inc_wdg_1[r].tagName == 'TABLE'){
                                    inc_wdg = inc_wdg_1[r];
                                }
                            }
                            if(inc_wdg_1.length > 0){
                                break;
                            }
                        }
                        if(inc_wdg != ''){
                            top_el2 = document.getElementsByClassName(parent_view + '_incomplete_tasks_' + title_code);
                            if(top_el2.length > 0){
                                top_el2 = top_el2[0];
                                show_all = top_el2.getAttribute('show_all');
                                spt.api.load_panel(inc_wdg, 'operator_view.IncompleteWOWdg', {'search_type': 'twog/title', 'code': title_code, 'parent_view': parent_view, 'show_all': show_all}); 
                            }
                        }
                        //Reloading the title bar doesn't work because it hates America
//                        title_bar = document.getElementById('ov_title_bar_' + title_code);
//                        if(title_bar){
//                            work_order_code = title_bar.work_order_code;
//                            groups_str = title_bar.groups_str;
//                            user_name = title_bar.user_name;
//                            title_code = title_bar.title_code;
//                            spt.api.load_panel(title_bar, 'operator_view.TitleSidebarWdg', {'title_code': title_code, 'user_name': user_name, 'groups_str': groups_str, 'work_order_code': work_order_code}); 
//                        }
                    }
       
        }
        catch(err){
                  spt.app_busy.hide();
                  spt.alert(spt.exception.handler(err));
        }
                ''' % (search_key, work_order_code, title_sk, login_name)}
        return behavior

    def get_assignment_change_behavior(my, search_key, work_order_code):
        behavior = {'css_class': 'sel_change', 'type': 'change', 'cbjs_action': '''
                try{
                    var server= TacticServerStub.get();
                    var search_key = '%s';
                    var work_order_code = '%s';
                    new_assigned = bvr.src_el.value;
                    server.update(search_key, {'assigned': new_assigned});
                    top_el = document.getElementsByClassName('panel_' + work_order_code)[0];
                    assigned_el = top_el.getElementById('task_assigned_' + work_order_code);
                    assigned_el.innerHTML = '<u>' + new_assigned + '</u>';
        }
        catch(err){
                  spt.app_busy.hide();
                  spt.alert(spt.exception.handler(err));
        }
        ''' % (search_key, work_order_code)}
        return behavior 

    def get_bad_client_behavior(my, work_order_code):
        behavior = {'css_class': 'sel_change', 'type': 'change', 'cbjs_action': '''
                try{
                    var work_order_code = '%s';
                    spt.alert("Due To A Potential Billing Error, You Cannot Work On This. Please Contact Accounting.");
                    top_el = document.getElementsByClassName('panel_' + work_order_code)[0];
                    status_el = top_el.getElementsByClassName('status_panel_' + work_order_code)[0];
                    spt.api.load_panel(status_el, 'operator_view.StatusAndAssignmentWdg', {'work_order_code': work_order_code, 'requires_mastering': status_el.getAttribute('requires_mastering')})
        }
        catch(err){
                  spt.app_busy.hide();
                  spt.alert(spt.exception.handler(err));
        }
        ''' % (work_order_code)}
        return behavior 
    
    def get_display(my):
        login_obj = Environment.get_login()
        user_name = login_obj.get_login()
        groups = Environment.get_group_names()
        my.work_order_code = str(my.kwargs.get('work_order_code'))
        if 'task' in my.kwargs.keys():
            my.task = my.kwargs.get('task')
        else:
            my.task = my.server.eval("@SOBJECT(sthpw/task['lookup_code','%s'])" % my.work_order_code)
            if my.task:
                my.task = my.task[0]
            else:
                my.task = None
        requires_mastering = False
        if 'requires_mastering' in my.kwargs.keys():
            if my.kwargs.get('requires_mastering') == 'true':
                requires_mastering = True
        task_assigned = my.task.get('assigned') 
        task_status = my.task.get('status')
        task_alg = my.task.get('assigned_login_group')
        client_str = ''
        client_color = ''
        client_billing = ''
        if 'edeliveries' in task_alg:
            the_order = my.server.eval("@SOBJECT(twog/order['code','%s'])" % my.task.get('order_code'))[0]
            client = my.server.eval("@SOBJECT(twog/client['code','%s'])" % the_order.get('client_code'))[0]
            client_billing = client.get('billing_status')
            if 'On Hold' in client_billing:
                client_str = 'DO NOT WORK ON ANY OF THIS - POTENTIAL CLIENT BILLING ISSUE<br/>PLEASE CONTACT THE ACCOUNTING DEPT'
                if 'Do Not Ship' in client_billing:
                    client_color = '#ffaa00'
                elif 'Do Not Book' in client_billing:
                    client_color = '#e31919'
        elif 'nobook' in my.task.get('client_hold'):
            client_str = 'DO NOT WORK ON ANY OF THIS - POTENTIAL CLIENT BILLING ISSUE<br/>PLEASE CONTACT THE ACCOUNTING DEPT'
            client_color = '#e31919'
            
            
        color_arr = ["Pending","Ready","On Hold","Client Response","Fix Needed","Rejected","In Progress","DR In Progress","Amberfin01 In Progress","Amberfin02 In Progress","BATON In Progress","Export In Progress","Need Buddy Check","Buddy Check In Progress","Completed"]
        status_select = SelectWdg('matt_status_select')
        status_select.add_attr('old_status',task_status)
        status_select.add_attr('id','status_%s' % my.task.get('__search_key__'))
        for c in color_arr:
            if c == task_status:
                status_select.set_value(task_status)
            if c == task_status and c in ['On Hold','Pending','Client Response']:
                status_select.append_option(c,c)
            elif c != task_status and c in ['On Hold','Pending','Client Response'] and ('scheduling' in groups or 'scheduling supervisor' in groups):
                status_select.append_option(c,c)
            elif c not in ['On Hold','Pending','Client Response']: 
                status_select.append_option(c,c)
             
        if client_str == '':
            status_select.add_behavior(my.get_status_change_behavior(my.task.get('__search_key__'), my.work_order_code, my.server.build_search_key('twog/title',my.task.get('title_code')), user_name))
        else:
            status_select.add_behavior(my.get_bad_client_behavior(my.work_order_code))

        logins = my.server.eval("@SOBJECT(sthpw/login['location','internal']['license_type','user']['@ORDER_BY','login'])")
        login_select = SelectWdg('login_select')
        login_select.append_option('--SELECT--','')
        for lg in logins:
            login_select.append_option(lg.get('login'), lg.get('login'))
            if lg.get('login') == task_assigned:
                login_select.set_value(task_assigned)
        if client_str == '':
            login_select.add_behavior(my.get_assignment_change_behavior(my.task.get('__search_key__'), my.work_order_code)) 
        else:
            login_select.add_behavior(my.get_bad_client_behavior(my.work_order_code))

        table = Table()
        if client_str != '':
            table.add_style('background-color: %s;' % client_color)
            topcell = table.add_cell(client_str)
            topcell.add_attr('nowrap','nowrap')
            topcell.add_attr('colspan','2')
            
        table.add_row()
        table.add_cell(status_select)
        table.add_cell(login_select)
        table.add_row()
        tbl = Table()
        tbl.add_attr('border','1')
        tbl.add_attr('width','100%%')
        tbl.add_row()
        show_status = tbl.add_cell(task_status)
        show_status.add_style('background-color: %s;' % my.colors[task_status])
        show_status.add_attr('align','center')
        ss = table.add_cell(tbl)
        ss.add_attr('colspan','2')
        ss.add_attr('align','center')
        ss.add_attr('width','100%%')
        wrapped = TitleBarWrap(htmlelement=table)
        table = wrapped.get_title_wrap('Status And Assignment')
        returner = table
        if requires_mastering:
            table2 = Table()
            table2.add_row()
            centered = table2.add_cell('<font color="#FF0000"><b>Requires QC Mastering<b></font>')
            centered.add_attr('align','center')
            table2.add_row()
            table2.add_cell(table)
            returner = table2
        return returner

class TitleBarWrap(BaseRefreshWdg):
    def init(my):
        my.htmlelement = my.kwargs.get('htmlelement')

    def get_title_wrap(my, title):
       table = Table()
       table.add_attr('width','100%%')
       table.add_row()
       title_cell = table.add_cell(title)
       title_cell.add_attr('class','ovw_title')
       title_cell.add_attr('width','100%%')
       title_cell.add_attr('nowrap','nowrap')
       table.add_row()
       center_me = table.add_cell(my.htmlelement)
       center_me.add_attr('align','center')
       return table

