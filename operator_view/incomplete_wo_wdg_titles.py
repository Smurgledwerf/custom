__all__ = ["IncompleteWOWdg"]
#NEED TO MAKE THIS HANDLE SINGLE WORK ORDERS/TASKS. RIGHT NOW IT ASSUMES THAT THE CODE BEING PASSED IN IS ALWAYS A TITLE
import tacticenv
from pyasm.common import Environment
from pyasm.biz import *
from pyasm.web import Table, DivWdg
from pyasm.widget import SelectWdg, IconWdg, TextWdg, CheckboxWdg
from tactic.ui.common import BaseTableElementWdg
from tactic.ui.common import BaseRefreshWdg
from tactic.ui.widget.button_new_wdg import ButtonSmallNewWdg
from qc_reports import QCReportLauncherWdg
from pyasm.search import SearchType, Search
from time import gmtime, strftime

class IncompleteWOWdg(BaseTableElementWdg):
    def init(my):
        nothing = 'true'
        my.search_type = 'twog/title'
        my.parent_view = ''
        my.code = '' 
        my.show_all = 'false'
        my.workers = []
        my.groups = []
        my.groups_str = ''
        my.piped_groups_str = ''
        my.active_department = ''
        my.user_name = ''
        my.is_scheduler = False
        my.title_obj = None
        my.date = strftime("%Y-%m-%d", gmtime())
        my.stat_colors = {'Pending':'#d7d7d7','In Progress':'#f5f3a4','In_Progress':'#f5f3a4','On Hold':'#e8b2b8','On_Hold':'#e8b2b8','Client Response': '#ddd5b8', 'Completed':'#b7e0a5','Need Buddy Check':'#e3701a','Ready':'#b2cee8','Internal Rejection':'#ff0000','External Rejection':'#ff0000','Fix Needed':'#c466a1','Failed QC':'#ff0000','Rejected': '#ff0000','DR In_Progress': '#d6e0a4','DR In Progress': '#d6e0a4','Amberfin01_In_Progress':'#D8F1A8','Amberfin01 In Progress':'#D8F1A8','Amberfin02_In_Progress':'#F3D291','Amberfin02 In Progress':'#F3D291', 'BATON In_Progress': '#c6e0a4','BATON In Progress': '#c6e0a4', 'Export In_Progress': '#796999', 'Export In Progress': '#796999','Buddy Check In_Progress': '#1aade3','Buddy Check In Progress': '#1aade3'}
        my.title_tasks = {}

    def fix_date(my, date):
        #This is needed due to the way Tactic deals with dates (using timezone info), post v4.0
        from pyasm.common import SPTDate
        return_date = ''
        date_obj = SPTDate.convert_to_local(date)
        if date_obj not in [None,'']:
            return_date = date_obj.strftime("%Y-%m-%d  %H:%M")
        return return_date

    def get_alter_wo_behavior(my, wo_code, process):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                          var server = TacticServerStub.get();
                          wo_code = '%s';
                          alert(wo_code);
                          process = '%s';
                          alert(process);
                          title_code = bvr.src_el.getAttribute('title_code');
                          alert(title_code);
                          wo_sk = server.build_search_key('twog/work_order', wo_code);
                          alert(wo_sk);
                          spt.panel.load_popup('Associated Info: ' + process, 'order_builder.TaskInspectWdg', {'code': wo_code, 'name': process}); 
                          //spt.panel.load_popup('Edit ' + wo_code, 'tactic.ui.panel.EditWdg', {element_name: 'general', mode: 'edit', 'search_key': wo_sk, search_type: 'twog/work_order', title: 'Edit ' + wo_code, view: 'edit', widget_key: 'edit_layout', cbjs_edit_path: 'builder/reload_incomplete_wo_table'}); 
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         ''' % (wo_code, process)}
        return behavior

    def get_see_wo_behavior(my, wo_code, process):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                          var server = TacticServerStub.get();
                          wo_code = '%s';
                          process = '%s';
                          title_code = bvr.src_el.getAttribute('title_code');
                          wo_sk = server.build_search_key('twog/work_order', wo_code);
                          spt.panel.load_popup('Associated Info: ' + process, 'order_builder.TaskInspectWdg', {'code': wo_code, 'name': process}); 
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         ''' % (wo_code, process)}
        return behavior

    def get_save_behavior(my, code, parent_view, user_name, st):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        function oc(a){
                            var o = {};
                            for(var i=0;i<a.length;i++){
                                o[a[i]]='';
                            }
                            return o;
                        }
                        try{
                          var code = '%s';
                          var parent_view = '%s';
                          var login_name = '%s';
                          var st = '%s';
                          var group_email_lookup = {'admin': 'administrator@2gdigital.com', 'it': 'IT@2gdigital.com', 'qc': 'QC@2gdigital.com', 'qc supervisor': 'QC@2gdigital.com', 'compression': 'Compression@2gdigital.com', 'billing and accounts receivable': '2GSales@2gdigital.com', 'audio': 'Audio@2gdigital.com', 'compression supervisor': 'Compression@2gdigital.com', 'edeliveries': 'Edeliveries@2gdigital.com', 'machine room': 'MR@2gdigital.com', 'media vault': 'Mediavault@2gdigital.com', 'media vault supervisor': 'Mediavault@2gdigital.com', 'edit supervisor': 'Editors@2gdigital.com', 'machine room supervisor': 'MR@2gdigital.com', 'office employees': 'jaime.torres@2gdigital.com;adriana.amador@2gdigital.com', 'edit': 'Editors@2gdigital.com', 'sales': '2GSales@2gdigital.com', 'senior_staff': 'fernando.vasquez@2gdigital.com;jaime.torres@2gdigital.com;adriana.amador@2gdigital.com;stephen.buchsbaum@2gdigital.com', 'executives': 'stephen.buchsbaum@2gdigital.com', 'management': 'jaime.torres@2gdigital.com;adriana.amador@2gdigital.com', 'scheduling': 'scheduling@2gdigital.com', 'streamz': 'MR@2gdigital.com;QC@2gdigital.com;Editors@2gdigital.com', 'technical services': 'IT@2gdigital.com', 'sales supervisor': '2GSales@2gdigital.com', 'scheduling supervisor': 'scheduling@2gdigital.com', 'vault': 'Mediavault@2gdigital.com'}
                          var top = document.getElementsByClassName(parent_view + '_incomplete_tasks_' + code)[0];
                          trt_el = top.getElementById('trt_top');
                          trtwtl_el = top.getElementById('trtwtl_top');
                          spt.app_busy.show("Saving...");
                          var server = TacticServerStub.get();
                          var title_sk = '';
                          if(st == 'twog/title'){
                              title_sk = server.build_search_key('twog/title', code);
                          }else if(st == 'twog/work_order'){
                              wo_title_code = server.eval("@GET(twog/work_order['code','" + code + "'].title_code)");
                              if(wo_title_code){ 
                                  title_sk = server.build_search_key('twog/title', wo_title_code[0]) 
                              }
                          }
                          if(trt_el.old_value != trt_el.value || trtwtl_el.old_value != trtwtl_el.value){
                              server.update(title_sk, {'total_program_runtime': trt_el.value, 'total_runtime_w_textless': trtwtl_el.value});
                              trt_row = top.getElementById(code + '_trt_row');
                              trt_row.setAttribute('bgcolor','#ededed');
                          }
                          pulled_el = top.getElementById('pulled_blacks_top');
                          if(pulled_el.value != pulled_el.old_value){
                              server.update(title_sk, {'pulled_blacks': pulled_el.value});
                          }
                          file_size_el = top.getElementById('file_size_top');
                          if(file_size_el.value != file_size_el.old_value){
                              server.update(title_sk, {'file_size': file_size_el.value});
                          }
                          var rows = top.getElementsByClassName('inc_row');
                          completed_one = false;
                          updated = false;
                          fix_needed = false;
                          fix_code = '';
                          for(var r = 0; r < rows.length; r++){
                              task_sk = rows[r].getAttribute('sk');
                              task_code = task_sk.split('code=')[1];
                              sels = rows[r].getElementsByTagName('select');
                              assigned_val = '';
                              old_assigned = '';
                              status_val = ''; 
                              old_status = '';
                              worker_sel = null;
                              status_sel = null;
                              for(var x = 0; x < sels.length; x++){
                                  if(sels[x].name == 'worker_' + task_sk){
                                      assigned_val = sels[x].value;
                                      old_assigned = sels[x].getAttribute('old');
                                      worker_sel = sels[x];
                                  }else if(sels[x].name == 'status_' + task_sk){
                                      status_val = sels[x].value;
                                      old_status = sels[x].getAttribute('old');
                                      status_sel = sels[x];
                                  } 
                              }
                              hours = rows[r].getElementById('hours');
                              hour_val = hours.value;
                              data = {};
                              if(old_status != status_val){
                                  data['status'] = status_val;
                              }
                              if(old_assigned != assigned_val){
                                  data['assigned'] = assigned_val;
                              } 
                              if((hour_val == '' || hour_val == null) && ('status' in data || 'assigned' in data)){
                                  server.update(task_sk, data);
                                  if('status' in data){
                                      status_sel.setAttribute('old',data['status']);
                                  }
                                  updated = true;
                                  task = server.eval("@SOBJECT(sthpw/task['code','" + task_code + "'])")[0]
                                  if(data['status'] == 'Failed QC' || data['status'] == 'Rejected'){
                                      entered = false;
                                      while(!entered){
                                          operator_description = prompt("Please tell us why " + task.process + " (" + task.lookup_code + ") was rejected.");
                                          if(operator_description != '' && operator_description != null){
                                              entered = true;
                                          } 
                                      }
                                      error_entries = server.eval("@SOBJECT(twog/production_error['work_order_code','" + task.lookup_code + "'])")
                                      error_entry = error_entries[error_entries.length - 1];
                                      server.update(error_entry.__search_key__, {'operator_description': operator_description});
                                  }else if(data['status'] == 'Fix Needed'){
                                      fix_needed = true; 
                                      fix_code = task.lookup_code;
                                      //kgs = {'wo_code': task.lookup_code};
                                      //spt.panel.load_popup('Select Work Order To Go Back To', 'operator_view.resetter.WOResetWdg', kgs);
                                  }else if(data['status'] == 'On_Hold' || data['status'] == 'On Hold'){
                                      entered = false;
                                      while(!entered){
                                          operator_description = prompt("Please tell us why " + task.process + " (" + task.lookup_code + ") is On Hold.");
                                          if(operator_description != '' && operator_description != null){
                                              entered = true;
                                          } 
                                      }
                                      //if(operator_description == ''){
                                      //    operator_description = login_name + ' did not enter a reason for the On Hold Status';
                                      //}
                                      scheduler_email = server.eval("@GET(sthpw/login['login','" + login_name + "'].email)")[0];
                                      ccs = scheduler_email + ';' + group_email_lookup[task.assigned_login_group]; 
                                      server.execute_cmd('operator_view.MakeNoteWdg', {'obj_sk': title_sk, 'header': task.process + ' - On Hold', 'note': operator_description, 'note_ccs': ccs}); 
                                  }else if(data['status'] != old_status && data['status'] == 'Completed' && task.assigned_login_group in oc(['compression','compression supervisor','machine room','machine room supervisor','audio','edit','edit supervisor'])){
                                      gotit = false;
                                      file_path = '';
                                      while(!gotit){
                                          file_path = prompt("Please Enter the Path to the File(s) for " + task.process);
                                          if(file_path != '' && file_path != null){
                                              gotit = true;
                                          }
                                      }
                                      scheduler_email = server.eval("@GET(sthpw/login['login','" + login_name + "'].email)")[0];
                                      //ccs = scheduler_email + ';' + group_email_lookup[task.assigned_login_group]; 
                                      ccs = scheduler_email;
                                      server.execute_cmd('operator_view.MakeNoteWdg', {'obj_sk': title_sk, 'header': task.process + ' - Completed', 'note': 'File Path: ' +  file_path, 'note_ccs': ccs}); 
                                      completed_one = true;
                                  }else if(data['status'] == 'Completed'){
                                      completed_one = true;
                                  }
                              }else{
                                  hour = Number(hour_val);
                                  if(hour == '' || hour == null){
                                      //nothing happening here
                                  }else if(isNaN(hour)){
                                      spt.alert('Please only enter numbers into the hour entry box. ' + hour_val + ' is not a number.');
                                  }else{
                                      var today = new Date(); 
                                      var dd = today.getDate(); 
                                      var mm = today.getMonth() + 1; 
                                      var yyyy = today.getFullYear(); 
                                      var day = yyyy + '-' + mm + '-' + dd;
                                      task_code = task_sk.split('code=')[1];
                                      task = server.eval("@SOBJECT(sthpw/task['code','" + task_code + "'])")[0];
                                      server.insert('sthpw/work_hour', {'day': day, 'search_type': 'sthpw/task', 'project_code': 'twog', 'process': task.process, 'task_code': task_code, 'search_id': task.id, 'straight_time': hour, 'login': login_name, 'is_billable': 'true'});  
                                      if(data != null && data != {}){
                                          server.update(task_sk, data);
                                          if('status' in data){
                                              status_sel.setAttribute('old',data['status']);
                                          }
                                          if(data['status'] == 'Failed QC' || data['status'] == 'Rejected'){
                                              entered = false;
                                              while(!entered){
                                                  operator_description = prompt("Please tell us why " + task.process + " (" + task.lookup_code + ") was rejected.");
                                                  if(operator_description != '' && operator_description != null){
                                                      entered = true;
                                                  }
                                              }
                                              error_entries = server.eval("@SOBJECT(twog/production_error['work_order_code','" + task.lookup_code + "'])")
                                              error_entry = error_entries[error_entries.length - 1];
                                              server.update(error_entry.__search_key__, {'operator_description': operator_description});
                                          }else if(data['status'] == 'Fix Needed'){
                                              fix_code = task.lookup_code;
                                              fix_needed = true; 
                                              //kgs = {'wo_code': task.lookup_code};
                                              //spt.panel.load_popup('Select Work Order To Go Back To', 'operator_view.resetter.WOResetWdg', kgs);
                                          }else if(data['status'] == 'On_Hold' || data['status'] == 'On Hold'){
                                              entered = false;
                                              while(!entered){
                                                  operator_description = prompt("Please tell us why " + task.process + " (" + task.lookup_code + ") is On Hold.");
                                                  if(operator_description != '' && operator_description != null){
                                                      entered = true;
                                                  }
                                              }
                                              //if(operator_description == ''){
                                              //    operator_description = login_name + ' did not enter a reason for the On Hold Status';
                                              //}
                                              scheduler_email = server.eval("@GET(sthpw/login['login','" + login_name + "'].email)")[0];
                                              ccs = scheduler_email + ';' + group_email_lookup[task.assigned_login_group]; 
                                              server.execute_cmd('operator_view.MakeNoteWdg', {'obj_sk': title_sk, 'header': task.process + ' - On Hold', 'note': operator_description, 'note_ccs': ccs}); 
                                          }else if(data['status'] != old_status && data['status'] == 'Completed' && task.assigned_login_group in oc(['compression','compression supervisor','machine room','machine room supervisor','audio','edit','edit supervisor'])){
                                              gotit = false;
                                              file_path = '';
                                              while(!gotit){
                                                  file_path = prompt("Please Enter the Path to the File(s) for " + task.process);
                                                  if(file_path != '' && file_path != null){
                                                      gotit = true;
                                                  }
                                              }
                                              scheduler_email = server.eval("@GET(sthpw/login['login','" + login_name + "'].email)")[0];
                                              //ccs = scheduler_email + ';' + group_email_lookup[task.assigned_login_group]; 
                                              ccs = scheduler_email;
                                              server.execute_cmd('operator_view.MakeNoteWdg', {'obj_sk': title_sk, 'header': task.process + ' - Completed', 'note': 'File Path: ' +  file_path, 'note_ccs': ccs}); 
                                              completed_one = true;
                                          }else if(data['status'] == 'Completed'){
                                              completed_one = true;
                                          }
                                      }
                                      updated = true;
                                  }
                              }
                              eq_durs = rows[r].getElementsByClassName('eq_duration');
                              for(var d = 0; d < eq_durs.length; d++){
                                  seg = eq_durs[d];
                                  orig_val = seg.getAttribute('orig_val');
                                  seg_id = seg.getAttribute('id');
                                  new_val = seg.value; 
                                  if(new_val != orig_val){
                                      eq_code = seg_id.split('FFF')[0];
                                      dur = Number(new_val);
                                      if(isNaN(dur)){
                                          spt.alert('Please only enter numbers into the entry box for equipment');
                                          seg.value = orig_val;
                                          seg.style.background="#ff0000";
                                      }else{
                                          eq_sk = server.build_search_key('twog/equipment_used', eq_code);
                                          server.update(eq_sk, {'actual_duration': dur});
                                          updated = true;
                                      }
                                  }
                              }
                          }
                          if(updated){
                              for(var r = 0; r < rows.length; r++){
                                  rows[r].setAttribute('bgcolor','#ededed');
                                  hours = rows[r].getElementById('hours'); 
                                  hours.value = '';
                              }
                              if(fix_needed){
                                  kgs = {'wo_code': fix_code, 'allow_close': false};
                                  spt.panel.load_popup('Select Work Order To Go Back To', 'operator_view.resetter.WOResetWdg2', kgs);
                              }
                          }
                          if(completed_one){
                              //refresh the widget
                              search_type = st;
                              inc_wdg_1 = document.getElementsByClassName(parent_view + '_innerds_' + code);
                              inc_wdg = '';
                              for(var r = 0; r < inc_wdg_1.length; r++){
                                  if(inc_wdg_1[r].tagName == 'TABLE'){
                                      inc_wdg = inc_wdg_1[r];
                                  }
                              }
                              if(inc_wdg != ''){
                                  top_el = document.getElementsByClassName(parent_view + '_incomplete_tasks_' + code)[0];
                                  show_all = top_el.getAttribute('show_all');
                                  spt.api.load_panel(inc_wdg, 'operator_view.IncompleteWOWdg', {'search_type': search_type, 'code': code, 'parent_view': parent_view, 'show_all': show_all}); 
                              }
                          }
                          spt.app_busy.hide();
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         ''' % (code, parent_view, user_name, st)}
        return behavior

    def get_add_multi_eq(my, title_code, piped_groups_str, parent_view, code):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                try{
                    title_code = '%s';
                    piped_groups_str = '%s';
                    parent_view = '%s';
                    alt_code = '%s';
                    var server = TacticServerStub.get();
                    var expr = '';
                    if(parent_view == 'task_view'){
                        expr = "@SOBJECT(sthpw/task['lookup_code','" + alt_code + "'])";
                    }else{
                        expr = "@SOBJECT(sthpw/task['title_code','" + title_code + "']['search_type','twog/proj?project=twog']['assigned_login_group','in','" + piped_groups_str + "']['status','!=','Completed'])";
                    }
                    wos = server.eval(expr);
                    wo_codes = '';
                    for(var r = 0; r < wos.length; r++){
                        if(wo_codes == ''){
                            wo_codes = wos[r].lookup_code;
                        }else{
                            wo_codes = wo_codes + ',' + wos[r].lookup_code;
                        }
                    } 
                    data = {}
                    if(parent_view == 'task_view'){
                        data['work_order_code'] = alt_code;
                    }else{
                        data['wo_codes'] = wo_codes;
                    }
                    data['parent_view'] = parent_view;
                    //data['popup'] = 'true';
                    spt.panel.load_popup('Add Equipment to Selected Work Orders', 'operator_view.EquipmentUsedMultiAdderWdg', data);
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         ''' % (title_code, piped_groups_str, parent_view, code)}
        return behavior

    def select_all_behavior(my, parent_view, code):
        behavior = {'css_class': 'clickme', 'type': 'change', 'cbjs_action': '''        
                try{
                    parent_view = '%s';
                    code = '%s';
                    top_el = document.getElementsByClassName(parent_view + '_incomplete_tasks_' + code)[0];
                    checkboxes = [];
                    inputs = top_el.getElementsByTagName('input');
                    selval = bvr.src_el.checked;
                    status = '';
                    assigned = '';
                    hours = '';
                    colors = {'Pending':'#d7d7d7','In Progress':'#f5f3a4','In_Progress':'#f5f3a4','On Hold':'#e8b2b8','On_Hold':'#e8b2b8','Client Response': '#ddd5b8', 'Completed':'#b7e0a5','Need Buddy Check':'#e3701a','Ready':'#b2cee8','Internal Rejection':'#ff0000','External Rejection':'#ff0000','Fix Needed':'#c466a1','Failed QC':'#ff0000','Rejected': '#ff0000','DR In_Progress': '#d6e0a4','DR In Progress': '#d6e0a4','Amberfin01_In_Progress':'#D8F1A8','Amberfin01 In Progress':'#D8F1A8','Amberfin02_In_Progress':'#F3D291','Amberfin02 In Progress':'#F3D291', 'BATON In_Progress': '#c6e0a4','BATON In Progress': '#c6e0a4', 'Export In_Progress': '#796999', 'Export In Progress': '#796999','Buddy Check In_Progress': '#1aade3','Buddy Check In Progress': '#1aade3'}
                    if(selval){
                        status = top_el.getElementById('status_top_' + code).value; 
                        assigned_el = top_el.getElementById('worker_top'); 
                        assigned = assigned_el.value; 
                        hours = top_el.getElementById('hours_top').value; 
                    }
                    for(var r = 0; r < inputs.length; r++){
                        if(inputs[r].type == 'checkbox' && (inputs[r].name != 'select_all_' + code)){
                            inputs[r].checked = selval;
                            sk = inputs[r].getAttribute('sk');
                            inkrow = top_el.getElementById('inc_row_' + sk); 
                            thours_el = inkrow.getElementById('hours');
                            tassigned_el = inkrow.getElementById('worker_' + sk);
                            tstatus_el = inkrow.getElementById('status_' + sk);
                            changed = false;
                            if(status != ''){
                                tstatus_el.value = status
                                tstatus_el.style.backgroundColor = colors[status];
                                changed = true;
                            }
                            if(assigned != ''){
                                tassigned_el.value = assigned;
                                changed = true;
                            }
                            if(hours != '' && hours != null && hours != '0'){
                                thours_el.value = hours;
                                changed = true;
                            }
                            if(changed){
                                inkrow.setAttribute('bgcolor','#909977');
                            }
                        }
                    }
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         ''' % (parent_view, code)}
        return behavior

    def changed_behavior(my, sk):
        behavior = {'css_class': 'clickme', 'type': 'change', 'cbjs_action': '''        
                try{
                    sk = '%s';
                    top_el = document.getElementById('inc_row_' + sk);
                    top_el.setAttribute('bgcolor','#909977');
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         ''' % sk}
        return behavior

    def get_show_all(my, parent_view, search_type, code):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        function oc(a){
                            var o = {};
                            for(var i=0;i<a.length;i++){
                                o[a[i]]='';
                            }
                            return o;
                        }
                        try{
                            parent_view = '%s';
                            search_type = '%s';
                            code = '%s';
                            inc_wdg_1 = document.getElementsByClassName(parent_view + '_innerds_' + code);
                            inc_wdg = '';
                            for(var r = 0; r < inc_wdg_1.length; r++){
                                if(inc_wdg_1[r].tagName == 'TABLE'){
                                    inc_wdg = inc_wdg_1[r];
                                }
                            }
                            
                            if(inc_wdg != ''){
                                show_all = 'true';
                                top_el = document.getElementsByClassName(parent_view + '_incomplete_tasks_' + code)[0];
                                show_all = top_el.getAttribute('show_all');
                                if(show_all in oc(['True','true','1','t'])){
                                    show_all = 'false';
                                }else{
                                    show_all = 'true';
                                }
                                spt.api.load_panel(inc_wdg, 'operator_view.IncompleteWOWdg', {'search_type': search_type, 'code': code, 'parent_view': parent_view, 'show_all': show_all}); 
                            }
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         ''' % (parent_view, search_type, code)}
        return behavior

    def get_refresh_behavior(my, parent_view, search_type, code):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                            parent_view = '%s';
                            search_type = '%s';
                            code = '%s';
                            inc_wdg_1 = document.getElementsByClassName(parent_view + '_innerds_' + code);
                            inc_wdg = '';
                            for(var r = 0; r < inc_wdg_1.length; r++){
                                if(inc_wdg_1[r].tagName == 'TABLE'){
                                    inc_wdg = inc_wdg_1[r];
                                }
                            }
                            if(inc_wdg != ''){
                                top_el = document.getElementsByClassName(parent_view + '_incomplete_tasks_' + code)[0];
                                show_all = top_el.getAttribute('show_all');
                                spt.api.load_panel(inc_wdg, 'operator_view.IncompleteWOWdg', {'search_type': search_type, 'code': code, 'parent_view': parent_view, 'show_all': show_all}); 
                            }
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         ''' % (parent_view, search_type, code)}
        return behavior

    def get_onload_js(my):
        return r'''
        do_something = function() {
             alert('123');
        }
        '''

    def handle_layout_behaviors(my, layout):
         layout.add_behavior( {
        'type': 'load',
        'cbjs_action': my.get_onload_js()
         } )

    def do_innerds(my):
        search_type = 'twog/order'
        parent_view = my.parent_view
        show_all = my.show_all
        show_all_butt_txt = 'Show All'
        if parent_view in ['titles_hl','bigboard_hl']:
            show_all = True
        if show_all in [True,'true','True','1',1]:
            show_all = True
            show_all_butt_txt = 'Show Incompleted WOs'
        else:
            show_all = False 
        groups = my.groups
        piped_groups_str = my.piped_groups_str   
        active_department = my.active_department   
        groups_str = my.groups_str   
        user_name = my.user_name
        is_scheduler = my.is_scheduler 
        title_obj = my.title_obj


        code = ''
        sob_sk = ''
        tasks = []
        trt = title_obj.get_value('total_program_runtime')
        trtwtl = title_obj.get_value('total_runtime_w_textless')
        pulled_blacks = title_obj.get_value('pulled_blacks')
        file_size = title_obj.get_value('file_size')
        if pulled_blacks in [None,'None','']:
            pulled_blacks = ''
        if file_size in [None,'None','']:
            file_size = ''

        search_type = ''
        additional_group = ''
        title_code = title_obj.get_code()
        is_single = False
        search_type = my.search_type
        code = my.code
        if 'WORK_ORDER' in code:
            search = Search("sthpw/task")
            search.add_filter('lookup_code', code)
            ttask = search.get_sobject()
            additional_group = ttask.get_value('assigned_login_group')
            title_code = ttask.get_value('title_code')
            is_single = True
        elif 'TITLE' in code:
            title_code = code
            #1additional_group = my.server.eval("@GET(sthpw/task['lookup_code','%s'].assigned_login_group)" % code)[0]

                  
        if additional_group not in [None,'']:
            if piped_groups_str == '':
                piped_groups_str = additional_group
                groups_str = "('%s'" % additional_group
            else:
                piped_groups_str = '%s|%s' % (piped_groups_str, additional_group)
                groups_str = "%s,'%s'" % (groups_str, additional_group) 
        groups_str = '%s)' % groups_str

        if search_type == '': 
            if 'WORK_ORDER' in code:
                search_type = 'twog/work_order'
            elif 'PROJ' in code:
                search_type = 'twog/proj'
            elif 'TITLE' in code: 
                search_type = 'twog/title'
            elif 'ORDER' in code:
                search_type = 'twog/order'
        search_code = ''
        if search_type == 'twog/order':
            search_code = 'order_code'
        elif search_type == 'twog/title':
            search_code = 'title_code'
        elif search_type == 'twog/proj':
            search_code = 'proj_code'
        elif search_type == 'twog/work_order':
            search_code = 'lookup_code'

        if my.show_all in [True,'true','t',1]:
            task_search = Search("sthpw/task")
            task_search.add_filter('search_type','twog/proj?project=twog')
            task_search.add_filter(search_code, code)
            if not show_all:
                if not is_single:
                    task_search.add_where("\"status\" not in ('Completed','Pending')")
                    #task_search.add_where("\"assigned_login_group\" in %s" % groups_str)
                if active_department != '' and not is_single:
                    task_search.add_filter('assigned_login_group',active_department)
                else:
                    task_search.add_where("\"assigned_login_group\" in %s" % groups_str)
            task_search.add_order_by("order_in_pipe")
            tasks = task_search.get_sobjects()
        else:
            tasks_dict = my.title_tasks[code]
            tasks_keys = tasks_dict.keys()
            tasks_keys.sort()
            tasks = []
            for tk in tasks_keys:
                tasks.append(tasks_dict[tk])
        widget = DivWdg()
        select_all = CheckboxWdg('select_all_%s' % code) 
        #select_all.set_persistence()
        select_all.set_value(False)
        select_all.add_behavior(my.select_all_behavior(parent_view, code))
        #workers = my.server.eval("@GET(sthpw/login['license_type','user']['location','internal']['@ORDER_BY','login'].login)")
        status_top_pull = '''<select id="status_top_%s" name="status_top" style="border-radius: 5px;" onChange="code='%s';parent_view='%s';colors={'Pending':'#d7d7d7','In Progress':'#f5f3a4','In_Progress':'#f5f3a4','On Hold':'#e8b2b8','On_Hold':'#e8b2b8','Client Response':'#ddd5b8','Completed':'#b7e0a5','Need Buddy Check':'#e3701a','Ready':'#b2cee8','Internal Rejection':'#ff0000','External Rejection':'#ff0000','Rejected':'#ff0000','Fix Needed':'#c466a1','Failed QC':'#ff0000','DR In_Progress':'#d6e0a4','DR In Progress':'#d6e0a4','Amberfin01_In_Progress':'#D8F1A8','Amberfin01 In Progress':'#D8F1A8','Amberfin02_In_Progress':'#F3D291','Amberfin02 In Progress':'#F3D291','BATON In_Progress':'#c6e0a4','BATON In Progress':'#c6e0a4','Export In_Progress':'#796999','Export In Progress':'#796999','Buddy Check In_Progress':'#1aade3','Buddy Check In Progress':'#1aade3'};this.style.backgroundColor=colors[this.value];top_el=document.getElementsByClassName(parent_view+'_incomplete_tasks_'+code)[0];checkboxes=[];clicked_on=false;inputs=top_el.getElementsByTagName('input');selval=false;for(r=0;r<inputs.length;r++){if(inputs[r].type=='checkbox'){if(inputs[r].checked){if(inputs[r].name=='select_all_'+code){clicked_on=true;}else{checkboxes.push(inputs[r]);}}}}if(clicked_on){for(r=0;r<checkboxes.length;r++){sk=checkboxes[r].getAttribute('sk');corresp=top_el.getElementById('status_'+sk);status=this.value;corresp.value=status;corresp.style.backgroundColor=colors[status];row_el=document.getElementById('inc_row_'+sk);row_el.setAttribute('bgcolor','#909977');}}"><option value="">--Status--</option>''' % (code, code, parent_view)
        for val in ['Pending','Ready','On Hold','Client Response','Fix Needed','Rejected','In Progress','DR In Progress','Amberfin01 In Progress','Amberfin02 In Progress','BATON In Progress','Export In Progress','Need Buddy Check','Buddy Check In Progress','Completed']:
            if val == 'On Hold':
                if 'scheduling' in groups or 'scheduling supervisor' in groups:
                    status_top_pull = '%s<option value="%s" style="background-color: %s;">%s</option>' % (status_top_pull, val, my.stat_colors[val], val)
            else:
                status_top_pull = '%s<option value="%s" style="background-color: %s;">%s</option>' % (status_top_pull, val, my.stat_colors[val], val)
        status_top_pull = '%s</select>' % status_top_pull
        worker_top_pull = '''<select name="worker_top" id="worker_top" style="border-radius: 5px;" onChange="code='%s';parent_view='%s';top_el=document.getElementsByClassName(parent_view+'_incomplete_tasks_'+code)[0];checkboxes=[];clicked_on=false;inputs=top_el.getElementsByTagName('input');selval=false;for(r=0;r<inputs.length;r++){if(inputs[r].type=='checkbox'){if(inputs[r].checked){if(inputs[r].name=='select_all_'+code){clicked_on=true;}else{checkboxes.push(inputs[r]);}}}}if(clicked_on){for(r=0;r<checkboxes.length;r++){sk=checkboxes[r].getAttribute('sk');corresp=top_el.getElementById('worker_'+sk);worker=this.value;corresp.value=worker;row_el=document.getElementById('inc_row_'+sk);row_el.setAttribute('bgcolor','#909977');}}"><option value="">--Assign--</option>''' % (code, parent_view)
        for worker in my.workers:
            worker_top_pull = '%s<option value="%s">%s</option>' % (worker_top_pull, worker, worker)
        worker_top_pull = '%s</select>' % worker_top_pull
        hour_top = '''<input type="text" maxlength=5 style="width: 50px; height: 16px; border-radius: 5px;" size=5 id="hours_top" onChange="code='%s';parent_view='%s';top_el=document.getElementsByClassName(parent_view+'_incomplete_tasks_'+code)[0];checkboxes=[];clicked_on=false;inputs=top_el.getElementsByTagName('input');selval=false;for(r=0;r<inputs.length;r++){if(inputs[r].type=='checkbox'){if(inputs[r].checked){if(inputs[r].name=='select_all_'+code){clicked_on=true;}else{checkboxes.push(inputs[r]);}}}}if(clicked_on){for(r=0;r<checkboxes.length;r++){sk=checkboxes[r].getAttribute('sk');row_el=document.getElementById('inc_row_'+sk);corresp=row_el.getElementById('hours');hrs=this.value;corresp.value=hrs;row_el.setAttribute('bgcolor','#909977');}}"/>''' % (code, parent_view)
        client_billing = ''
        client_color = ''
        client_str = ''
        if title_obj:
            client_search = Search("twog/client")
            client_search.add_filter('code', title_obj.get_value('client_code'))
            client = client_search.get_sobject()
            #client = my.server.eval("@SOBJECT(twog/client['code','%s'])" % title_obj.get('client_code'))
            if client:
                client_billing = client.get_value('billing_status')
        if 'edeliveries' in piped_groups_str:
            if 'On Hold' in client_billing:
                client_str = 'DO NOT WORK ON ANY OF THIS - POTENTIAL CLIENT BILLING ISSUE<br/>PLEASE CONTACT THE ACCOUNTING DEPT'
                if 'Do Not Ship' in client_billing:
                    client_color = '#ffaa00'
                elif 'Do Not Book' in client_billing:
                    client_color = '#e31919'
        else:
            if 'On Hold - Do Not Book' in client_billing:
                client_str = 'DO NOT WORK ON ANY OF THIS - POTENTIAL CLIENT BILLING ISSUE<br/>PLEASE CONTACT THE ACCOUNTING DEPT'
                client_color = '#e31919'
                        
        len_tasks = len(tasks)
        #if len(tasks) > 0:
        table = Table()
        table.add_attr('class','%s_incomplete_tasks_%s %s_incomplete_tasks_wdg_%s' % (parent_view, code, parent_view, code))
        table.add_attr('parent_view', parent_view)
        table.add_attr('show_all', show_all)
        if client_str != '':
            table.add_style('background-color: %s;' % client_color)
            table.add_row()
            topcell = table.add_cell('<b>%s</b>' % client_str)
            topcell.add_attr('nowrap','nowrap')
            topcell.add_attr('colspan','6')
        if len_tasks > 1:
            table.add_row()
            table2 = Table()
            t02r = table2.add_row()
            t02r.add_style('font-size: 9px;')
            table2.add_cell(select_all)
            tt0 = table2.add_cell('Status: ')
            tt0.add_style('font-size: 9px;')
            table2.add_cell(status_top_pull)
            table2.add_cell(worker_top_pull)
            table2.add_cell(hour_top)
            longcell = table.add_cell(table2)
            longcell.add_attr('colspan','6')
        if title_code not in [None,'']:
            if title_obj:
                if title_obj.get_value('no_charge') and title_obj.get_value('redo'):
                    table.add_row()
                    nc_cell = table.add_cell('<font color="#FF0000"><b>REDO - NO CHARGE</b></font>')
            table.add_row()
            table3 = Table()
            trt_row = table3.add_row()
            trt_row.add_attr('id','%s_trt_row' % code)
            tt1 = table3.add_cell('TRT: ')
            tt1.add_style('font-size: 9px;')
            table3.add_cell('''<input type="text" maxlength=12 style="width: 80px; height: 16px; border-radius: 5px; font-size: 10px;" size=5 id="trt_top" onChange="top_el=document.getElementById('%s_trt_row'); top_el.setAttribute('bgcolor','#909977');" value="%s" old_value="%s"/>''' % (code, trt, trt))
            tt2 = table3.add_cell('TRT W/Textless: ')
            tt2.add_style('font-size: 9px;')
            table3.add_cell('''<input type="text" maxlength=12 style="width: 80px; height: 16px; border-radius: 5px; font-size: 10px;" size=5 id="trtwtl_top" onChange="top_el=document.getElementById('%s_trt_row'); top_el.setAttribute('bgcolor','#909977');" value="%s" old_value="%s"/>''' % (code, trtwtl, trtwtl))
            tt3 = table3.add_cell('File Size: ')
            tt3.add_style('font-size: 9px;')
            table3.add_cell('''<input type="text" maxlength=3 style="width: 50px; height: 16px; border-radius: 5px; font-size: 10px;" size=5 id="file_size_top" onChange="top_el=document.getElementById('%s_trt_row'); top_el.setAttribute('bgcolor','#909977');" value="%s" old_value="%s"/>''' % (code, file_size, file_size))
            tt4 = table3.add_cell('Pulled Blacks: ')
            tt4.add_style('font-size: 9px;')
            table3.add_cell('''<input type="text" maxlength=3 style="width: 35px; height: 16px; border-radius: 5px; font-size: 10px;" size=5 id="pulled_blacks_top" onChange="top_el=document.getElementById('%s_trt_row'); top_el.setAttribute('bgcolor','#909977');" value="%s" old_value="%s"/>''' % (code, pulled_blacks, pulled_blacks))
            if len_tasks > 0:
                add_eq = table3.add_cell('<input type="button" value="+EQ" style="font-size: 9px;"/>')
                add_eq.add_behavior(my.get_add_multi_eq(title_code, piped_groups_str, parent_view, code))
            show_butt = table3.add_cell('<input type="button" value="%s" style="font-size: 9px;"/>' % show_all_butt_txt)
            show_butt.add_behavior(my.get_show_all(parent_view, search_type, code))
            refresher = ButtonSmallNewWdg(title="Refresh", icon=IconWdg.REFRESH)
            refresher.add_behavior(my.get_refresh_behavior(parent_view, search_type, code))
            refr = table3.add_cell(refresher)
            refr.add_attr('align','right')
            if len_tasks == 0:
                qc_launcher = QCReportLauncherWdg(code=title_code)
                qcl = table3.add_cell(qc_launcher)
                qcl.add_attr('align','left') 
            longcell2 = table.add_cell(table3)
            longcell2.add_attr('colspan','6')
        for task in tasks:
            assigned = task.get_value('assigned')
            assigned_login_group = task.get_value('assigned_login_group')
            bid_end_date = my.fix_date(task.get_value('bid_end_date'))
            due_date = bid_end_date.split(' ')[0]
            status = task.get_value('status')
            name = task.get_value('process')
            wo_code = task.get_value('lookup_code')
            tacode = task.get_value('code')
            tabigboard = task.get_value('bigboard')
            indbigboard = task.get_value('indie_bigboard')
            taprocess = task.get_value('process')
            #eq_info = my.server.eval("@GET(twog/work_order['code','%s'].eq_info)" % wo_code)[0]
            wo_search = Search('twog/work_order')
            wo_search.add_filter('code', wo_code)
            wo = wo_search.get_sobject()
            eq_info = wo.get_value('eq_info') 
            sk = task.get_search_key()
            status_pull = '''<select name="status_%s" old="%s" id="status_%s" style="background-color: %s; border-radius: 5px;" onChange="colors={'Pending':'#d7d7d7','In Progress':'#f5f3a4','In_Progress':'#f5f3a4','On Hold':'#e8b2b8','On_Hold':'#e8b2b8','Client Response':'#ddd5b8','Completed':'#b7e0a5','Need Buddy Check':'#e3701a','Ready':'#b2cee8','Internal Rejection':'#ff0000','External Rejection':'#ff0000','Rejected': '#ff0000','Fix Needed':'#c466a1','Failed QC':'#ff0000','DR In_Progress': '#d6e0a4','DR In Progress': '#d6e0a4','Amberfin01_In_Progress':'#D8F1A8','Amberfin01 In Progress':'#D8F1A8','Amberfin02_In_Progress':'#F3D291','Amberfin02 In Progress':'#F3D291', 'BATON In_Progress': '#c6e0a4','BATON In Progress': '#c6e0a4', 'Export In_Progress': '#796999','Export In Progress': '#796999', 'Buddy Check In_Progress': '#1aade3','Buddy Check In Progress': '#1aade3'};top_el=document.getElementById('inc_row_%s'); top_el.setAttribute('bgcolor','#909977'); me_stat=top_el.getElementById('status_%s');me_stat.style.backgroundColor=colors[me_stat.value];">''' % (sk, status, sk, my.stat_colors[status], sk, sk)
            for val in ['Pending','Ready','On Hold','Client Response','Fix Needed','Rejected','In Progress','DR In Progress','Amberfin01 In Progress','Amberfin02 In Progress','BATON In Progress','Export In Progress','Need Buddy Check','Buddy Check In Progress','Completed']:
                selected = ''
                if status == val:
                    selected = 'selected'
                if (val == 'On Hold' and status == 'On Hold') or val != 'On Hold':
                    status_pull = '%s<option value="%s" style="background-color: %s;" %s>%s</option>' % (status_pull, val, my.stat_colors[val], selected, val)
                elif val == 'On Hold' and ('scheduling' in groups or 'scheduling supervisor' in groups):
                        status_top_pull = '%s<option value="%s" style="background-color: %s;">%s</option>' % (status_top_pull, val, my.stat_colors[val], val)
            status_pull = '%s</select>' % status_pull
            worker_pull = '''<select name="worker_%s" id="worker_%s" old="%s" style="border-radius: 5px;" onChange="top_el=document.getElementById('inc_row_%s'); top_el.setAttribute('bgcolor','#909977');"><option value="">--Assign--</option>''' % (sk, sk, assigned, sk)
            for worker in my.workers:
                selected = ''
                if worker == assigned:
                    selected = 'selected' 
                worker_pull = '%s<option value="%s" %s>%s</option>' % (worker_pull, worker, selected, worker)
            worker_pull = '%s</select>' % worker_pull
            r1 = table.add_row()
            r1.add_attr('class','inc_row')
            r1.add_attr('id','inc_row_%s' % sk)
            r1.add_attr('sk', sk)
            r1.add_style('font-size: 9px;')
            #checkbox = '<input type="checkbox" name="inc_selector_%s" sk="%s" wo_code="%s" task_code="%s"/>' % (wo_code, sk, wo_code, task.get('code'))
            checkbox = CheckboxWdg('inc_selector_%s' % wo_code)
            checkbox.add_attr('task_code', tacode)
            checkbox.add_attr('wo_code', wo_code)
            checkbox.add_attr('sk', sk)
            #checkbox.set_persistence()
            if len_tasks > 1:
                checkbox.set_value(False)
            else:
                checkbox.set_value(True)
            #checkbox.add_behavior(my.changed_behavior(sk))
            tats = Table()
            tats.add_row()
            tats.add_cell(checkbox)
            if indbigboard in [True,'t','T','1','true','True']:
                tats.add_cell('<img src="/context/icons/custom/small_blue_racecar_alpha.png" title="Hot Hot" name="Hot Hot"/>')
            if tabigboard in [True,'t','T','1','true','True']:
                tats.add_cell('<img src="/context/icons/silk/rosette.png" title="Hot Today" name="Hot Today"/>')
            cell0 = table.add_cell(tats)
            cell1 = table.add_cell('%s<br/>%s<br/>%s' % (wo_code, name, due_date))
            cell1.add_attr('id',wo_code)
            cell1.add_attr('class','alter_wo')
            cell1.add_attr('wo_code',wo_code)
            cell1.add_attr('process',taprocess)
            cell1.add_style('font-size: 8px;')
            cell1.add_attr('title_code', title_code)
            if my.date >= due_date:
                cell1.add_style('color: #ff0000;')
            if is_scheduler:
                cell1.add_style('cursor: pointer;')
                cell1.add_behavior(my.get_alter_wo_behavior(wo_code, taprocess))
            else:
                cell1.add_style('cursor: pointer;')
                cell1.add_behavior(my.get_see_wo_behavior(wo_code, taprocess))
            cell2 = table.add_cell(status_pull)
            cell3 = table.add_cell(worker_pull)
            cell4 = table.add_cell('''<input type="text" maxlength=5 style="width: 50px; height: 16px; border-radius: 5px;" size=5 id="hours" onChange="top_el=document.getElementById('inc_row_%s'); top_el.setAttribute('bgcolor','#909977');"/>''' % sk) 
            cell5 = table.add_cell('EQ:')
            info_s = eq_info.split('Z,Z')
            if len(info_s) > 0:
                if info_s[0] != '':
                    for info in info_s:
                        info_bits = info.split('X|X')
                        eq_code = info_bits[0]
                        eq_name = info_bits[1]
                        eq_units = info_bits[2] 
                        eq_unit_str = '%ss' % eq_units
                        if eq_units == 'LEN':
                            eq_unit_str = ''
                        else:
                            eq_duration = info_bits[3]
                            cellx = table.add_cell('<u>%s</u> <i>%s</i>' % (eq_name, eq_unit_str))
                            cellx.add_style('font-size: 8px;')
                            if eq_unit_str != '':
                                celly = table.add_cell('''<input type="text" class="eq_duration" maxlength=5 style="width: 40px; height: 16px; border-radius: 5px;" size=5 id="%sFFFhours" onChange="top_el=document.getElementById('inc_row_%s'); top_el.setAttribute('bgcolor','#909977');" orig_val="%s" value="%s"/>''' % (eq_code, sk, eq_duration, eq_duration))
                            cellspace = table.add_cell('&nbsp;')
            #if 'qc' in assigned_login_group:
            table.add_cell(' ')
            qc_launcher = QCReportLauncherWdg(code=wo_code)
            qcl = table.add_cell(qc_launcher)
            qcl.add_attr('align','right') 
        if client_str == '':
            table.add_row()
            scell1 = table.add_cell('<input type="button" value="Save"/>')
            launch_behavior = my.get_save_behavior(code, parent_view, user_name, search_type)
            scell1.add_style('cursor: pointer;')
            scell1.add_behavior(launch_behavior)
        #widget.add(table)
        #widget.add_class('%s_incomplete_tasks_wdg_%s' % (parent_view, code))

        #return widget
        return table

    def preprocess(my):
        my.show_all = False
        my.title_obj = None
        if 'show_all' in my.kwargs.keys():
            my.show_all = my.kwargs.get('show_all')
        login = Environment.get_login()
        my.user_name = login.get_login()
        workers_search = Search("sthpw/login")
        workers_search.add_filter('license_type','user')
        workers_search.add_filter('location','internal')
        workers_search.add_order_by('login')
        workers = workers_search.get_sobjects()
        my.workers = [] 
        for worker in workers:
            my.workers.append(worker.get_value('login'))

        if 'parent_view' in my.kwargs.keys():
            my.parent_view = str(my.kwargs.get('parent_view'))
        else: 
            parent = my.get_parent_wdg()
            if parent:
                my.parent_view = parent.view
            else:
                my.parent_view = 'unknown'

        my.groups = Environment.get_group_names()
        my.groups_str = ''
        my.piped_groups_str = ''
        my.active_department = ''
        view_lookup = {'audio': 'audio', 'all_titles': '', 'title': '', 'compression': 'compression', 'edel': 'edeliveries', 'edit': 'edit', 'mr': 'machine room', 'media_vault': 'media_vault', 'media vault': 'media vault', 'qc': 'qc', 'sales': 'sales', 'vault': 'vault'}
        for group in my.groups:
            if group != 'default':
                if 'supervisor' in group:
                    #1???group = '%s|%s' % (group, group.split(' ')[0])
                    group = group.split(' ')[0]
                if my.piped_groups_str == '':
                    my.piped_groups_str = group
                    my.groups_str = "('%s'" % group 
                else:
                    my.piped_groups_str = '%s|%s' % (my.piped_groups_str, group)
                    my.groups_str = "%s,'%s'" % (my.groups_str, group) 
        if 'operator_view_titles' in my.parent_view:
            for group in my.groups:
                if group != 'default':
                    if 'supervisor' in group:
                        #1???group = '%s|%s' % (group, group.split(' ')[0])
                        group = group.split(' ')[0]
                    if my.piped_groups_str == '':
                        my.piped_groups_str = group
                        my.groups_str = "('%s'" % group
                    else:
                        my.piped_groups_str = '%s|%s' % (my.piped_groups_str, group)
                        my.groups_str = "%s,'%s'" % (my.groups_str, group) 
        elif my.parent_view in ['bigboard_hotlist','bigboard_hl','task_view','hot_today']:
            do_nothing_here = True
        else:
            name_split = my.parent_view.split('_')
            remainder = ''
            for i in range(0,len(name_split) - 1):
                if remainder == '':
                    remainder = name_split[i]
                else:
                    remainder = '%s_%s' % (remainder, name_split[i])
            rem2 = remainder.replace('_',' ')
            if rem2 in view_lookup.keys():
                vll = view_lookup[rem2]
                if rem2 in view_lookup.keys() and rem2 not in ['title','sales']:
                    my.active_department = view_lookup[rem2] 
                my.piped_groups_str = vll
                my.groups_str = "('%s'" % vll
            else:
                my.piped_groups_str = ''
                my.groups_str = "('NOTHING'"
        if my.active_department == '':
            lsearch = Search("sthpw/login")
            lsearch.add_filter('login',my.user_name)
            lsearch.add_filter('location','internal')
            login_obj = lsearch.get_sobject()
            my.active_department = login_obj.get_value('active_department')
        if my.active_department in [None,'','admin','billing and accounts receivable','client','executives','it','management','office employees','sales','scheduling','senior_staff','streamz','technical services','user']:
            my.active_department = ''
        if 'scheduling' in my.piped_groups_str or 'admin' in my.piped_groups_str or my.user_name == 'admin':
            my.is_scheduler = True
        title_code_str = ''
        for sob in my.sobjects:
            if title_code_str == '':
                title_code_str = "('%s'" % sob.get_code()
            else:
                title_code_str = "%s,'%s'" % (title_code_str, sob.get_code())
        title_code_str = "%s)" % title_code_str
        task_search = Search("sthpw/task")
        task_search.add_filter('search_type','twog/proj?project=twog')
        #task_search.add_filter(search_code, code)
        task_search.add_where("\"title_code\" in %s" % title_code_str)
        if not my.show_all:
            task_search.add_where("\"status\" not in ('Completed','Pending')")
            if my.active_department != '':
                task_search.add_filter('assigned_login_group',my.active_department)
            else:
                task_search.add_where("\"assigned_login_group\" in %s" % my.groups_str)
        tasks = task_search.get_sobjects()
        my.title_tasks = {}
        for task in tasks:
            title_code = task.get_value('title_code')
            order_in_pipe = task.get_value("order_in_pipe")
            process = task.get_value('process')
            aslg = task.get_value('assigned_login_group')
            task_spot = '%s_%s_%s' % (aslg, process, order_in_pipe)
            try:
                my.title_tasks[title_code][task_spot] = task
            except:
                my.title_tasks[title_code] = {task_spot: task}
                pass


    def get_display(my):
        my.show_all = False
        my.title_obj = None
        if 'show_all' in my.kwargs.keys():
            my.show_all = my.kwargs.get('show_all')
        class_code = ''
        if 'search_type' in my.kwargs.keys():
            my.search_type = str(my.kwargs.get('search_type'))
            my.code = str(my.kwargs.get('code'))
            if 'WORK_ORDER' in my.code: 
                search = Search("twog/work_order")
                search.add_filter('code', my.code)
                wo = search.get_sobjects()
                class_code = wo[0].get_value('title_code')
                title_search = Search('twog/title')
                title_search.add_filter('code', class_code)
                my.title_obj = title_search.get_sobject()
        else: 
            sobject = my.get_current_sobject()
            my.code = sobject.get_code()
            class_code = my.code
            if 'TITLE' in my.code:
                my.title_obj = sobject
        
        widget = DivWdg()
        table = Table()
        if my.code not in  [-1,'-1']: 
            table.add_attr('class','%s_innerds_%s' % (my.parent_view, class_code))
            table.add_row()

            my.groups = Environment.get_group_names()
            innerds = my.do_innerds() 
            #innerds = IncompleteWOWdgInnerds(search_type=my.search_type, code=my.code, parent_view=my.parent_view,show_all=my.show_all,workers=my.workers,groups=my.groups,piped_groups_str=my.piped_groups_str,active_department=my.active_department,user_name=my.user_name,is_scheduler=my.is_scheduler,title_obj=my.title_obj)
            table.add_cell(innerds) 
        widget.add(table)
        return widget
