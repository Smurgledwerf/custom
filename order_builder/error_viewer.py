__all__ = ["ErrorDetailEditLauncherWdg","ErrorDetailEditWdg","FaultFilesWdg"]
import tacticenv
from pyasm.common import Environment
from pyasm.biz import *
from pyasm.web import Table, DivWdg
from tactic.ui.common import BaseTableElementWdg
from tactic.ui.common import BaseRefreshWdg
from tactic.ui.panel import EditWdg
from pyasm.widget import SelectWdg, IconWdg, TextWdg, CheckboxWdg

class ErrorDetailEditLauncherWdg(BaseTableElementWdg):

    def init(my):
        nothing = True 

    def get_launch_behavior(my):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                          var server = TacticServerStub.get();
                          var my_code = bvr.src_el.get('code');
                          var class_name = 'order_builder.ErrorDetailEditWdg';
                          kwargs = {
                                           'code': my_code
                                   };
                          spt.panel.load_popup('Edit Error Information', class_name, kwargs);
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         '''}
        return behavior

    def get_display(my):
        sobject = my.get_current_sobject()
        code = sobject.get_code()
        widget = DivWdg()
        table = Table()
        table.add_attr('width', '50px')
        table.add_row()
        #cell1 = table.add_cell('<img border="0" style="vertical-align: middle" title="" src="/context/icons/custom/work.png">')
        cell1 =  table.add_cell('<img border="0" style="vertical-align: middle" title="" src="/context/icons/silk/page_white_edit.png">')
        cell1.add_attr('code',code)
        launch_behavior = my.get_launch_behavior()
        cell1.add_style('cursor: pointer;')
        cell1.add_behavior(launch_behavior)
        widget.add(table)

        return widget

class ErrorDetailEditWdg(BaseRefreshWdg):

    def init(my):
        from client.tactic_client_lib import TacticServerStub
        from pyasm.common import Environment
        my.server = TacticServerStub.get()
        my.sk = ''
        my.code = ''
        my.video_reasons = {'Cropping': 'video_cropping_reason','Digital Hits / Macroblocking': 'video_digihits_reason', 'Dropped Frames': 'video_dropped_frames_reason', 'Dropout': 'video_dropout_reason', 'Duplicate Frames': 'video_duplicate_frames_reason', 'Interlacing on a progressive file': 'video_interlacing_progressive_reason', 'Motion/Image Lag': 'video_motion_lag_reason', 'Missing elements': 'video_missing_elements_reason', 'Corrupt file': 'video_corrupt_file_reason', 'Incorrect aspect ratio': 'video_bad_aspect_ratio_reason', 'Incorrect resolution': 'video_bad_resolution_reason', 'Incorrect pixel aspect ratio': 'video_bad_pixel_aspect_ratio_reason', 'Incorrect specifications': 'video_bad_specifications_reason', ' Incorrect head/tail format': 'video_bad_head_tail_reason', 'Other issue': 'video_other_reason'}
        my.video_reasons_arr = ['Cropping','Digital Hits / Macroblocking', 'Dropped Frames', 'Dropout', 'Duplicate Frames', 'Interlacing on a progressive file', 'Motion/Image Lag', 'Missing elements', 'Corrupt file', 'Incorrect aspect ratio', 'Incorrect resolution', 'Incorrect pixel aspect ratio', 'Incorrect specifications', ' Incorrect head/tail format', 'Other issue']
        my.audio_reasons = {'Incorrect Audio Mapping': 'audio_bad_mapping_reason', 'Missing Audio Channel': 'audio_missing_audio_channel_reason', 'Crackle/Hiss/Pop/Static/Ticks': 'audio_crackle_reason', 'Distortion': 'audio_distortion_reason', 'Dropouts': 'audio_dropouts_reason', 'Sync issue': 'audio_sync_reason', 'Missing elements': 'audio_missing_elements_reason', 'Corrupt file / missing file': 'audio_corrupt_missing_file_reason', 'Incorrect specifications': 'audio_bad_specifications_reason', 'Other Issue': 'audio_other_reason'}
        my.audio_reasons_arr = ['Incorrect Audio Mapping', 'Missing Audio Channel', 'Crackle/Hiss/Pop/Static/Ticks', 'Distortion', 'Dropouts', 'Sync issue', 'Missing elements', 'Corrupt file / missing file', 'Incorrect specifications', 'Other Issue']
        my.metadata_reasons = {'Missing information': 'metadata_missing_info_reason', 'Incorrect information': 'metadata_bad_info_reason', 'Incorrect formatting': 'metadata_bad_formatting_reason', 'Other Issue': 'metadata_other_reason'}
        my.metadata_reasons_arr = ['Missing information', 'Incorrect information', 'Incorrect formatting', 'Other Issue']
        my.subtitle_reasons = {'Interlacing on subtitles': 'subtitle_interlacing_reason', 'Incorrect subtitles': 'subtitle_bad_subtitles_reason', 'Sync issue': 'subtitle_sync_issue_reason', 'Overlapping other text': 'subtitle_overlapping_reason', 'Other issue': 'subtitle_other_reason'}
        my.subtitle_reasons_arr = ['Interlacing on subtitles', 'Incorrect subtitles', 'Sync issue', 'Overlapping other text', 'Other issue']
        my.cc_reasons = {'Sync issue': 'cc_sync_issue_reason','Incorrect CC': 'cc_bad_cc_reason', 'Overlapping other text': 'cc_overlapping_reason','Other issue': 'cc_other_reason'}
        my.cc_reasons_arr = ['Sync issue','Incorrect CC', 'Overlapping other text','Other issue']
        my.rejection_causes = ['Client Error','Machine Error','Manager Error','Operator Error','Process Error','Scheduler Error']
        my.root_cause_types = ['Machine Error','Operator Error','Incorrect Instructions','Source Issue','No Issue Found']
        my.statuses = ['Open','Investigating','Waiting for Source','Needs Corrective Action','Closed']

    def get_reason_check_behavior(my, field):
        behavior = {'css_class': 'clickme', 'type': 'change', 'cbjs_action': '''        
                        try{
                            var server = TacticServerStub.get();
                            field = bvr.src_el.getAttribute('field');
                            code = bvr.src_el.getAttribute('code');
                            st = 'twog/production_error';
                            if(code.indexOf('EXTERNAL_REJECTION') != -1){
                                st = 'twog/external_rejection'
                            }
                            sk = server.build_search_key(st, code);
                            server.update(sk, {'%s': bvr.src_el.checked}, {'triggers': false});
                     
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         ''' % field}
        return behavior

    def get_make_responsible_behavior(my):
        behavior = {'css_class': 'clickme', 'type': 'change', 'cbjs_action': '''        
                        try{
                            var server = TacticServerStub.get();
                            login = bvr.src_el.getAttribute('login');
                            code = bvr.src_el.getAttribute('code');
                            sk = server.build_search_key('twog/production_error', code);
                            p_e = server.eval("@SOBJECT(twog/production_error['code','" + code + "'])")[0];
                            responsible = p_e.responsible_users;
                            re_arr = responsible.split(',');
                            already_in = false;
                            checked = bvr.src_el.checked;
                            new_str = ''
                            for(var r = 0; r < re_arr.length; r++){
                                if(login == re_arr[r]){
                                    already_in = true;
                                }
                            }  
                            if(checked && !already_in){
                                new_str = responsible + ',' + login;
                                if(new_str == ',' + login){
                                    new_str = login;
                                }
                            }
                            if(!checked && already_in){
                                for(var r = 0; r < re_arr.length; r++){
                                    if(re_arr[r] != login){
                                        if(new_str == ''){
                                            new_str = re_arr[r];
                                        }else{
                                            new_str = new_str + ',' + re_arr[r];
                                        }
                                    }
                                }
                            }
                            server.update(sk, {'responsible_users': new_str});
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         '''}
        return behavior

    def get_sel_change_behavior(my, code, st, field):
        behavior = {'css_class': 'sel_change', 'type': 'change', 'cbjs_action': '''        
                        try{
                          var server = TacticServerStub.get();
                          var code = '%s';
                          var st = '%s';
                          sk = server.build_search_key(st, code)
                          value = bvr.src_el.value;
                          field = '%s';
                          if(value == '--Select--'){
                              value = '';
                          }
                          update_dict = {'%s': value};
                          if(field == 'assigned' || field == 'corrective_action_assigned' || field == 'status'){
                              server.update(sk, update_dict);
                          }else{
                              server.update(sk, update_dict, {'triggers': false});
                          }
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         ''' % (code, st, field, field)}
        return behavior

    def get_save_description_behavior(my, code):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                          var server = TacticServerStub.get();
                          var code = '%s';
                          description = document.getElementsByClassName(code + '_description')[0];
                          action_taken = document.getElementsByClassName(code + '_action_taken')[0];
                          time_spent = document.getElementsByClassName(code + '_time_spent')[0];
                          update_dict = {'description': description.value, 'action_taken': action_taken.value, 'time_spent': time_spent.value};
                          sk = server.build_search_key('twog/production_error', code);
                          if(code.indexOf('EXTERNAL_REJECTION') != -1){
                              update_dict =  {'root_cause': description.value, 'corrective_action': action_taken.value, 'time_spent': time_spent.value};
                              sk = server.build_search_key('twog/external_rejection', code);
                          }
                          server.update(sk, update_dict);
                          spt.popup.close(spt.popup.get_popup(bvr.src_el));
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         ''' % code}
        return behavior

    def get_save_external_rejection(my, code):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                          var server = TacticServerStub.get();
                          var code = '%s';
                          top_el = document.getElementById('error_tbl_' + code);
                          //description = top_el.getElementsByClassName(code + '_description')[0];
                          //action_taken = top_el.getElementsByClassName(code + '_action_taken')[0];
                          time_spent = top_el.getElementsByClassName(code + '_time_spent')[0];
                          replacement_order = top_el.getElementsByClassName(code + '_replacement_order_code')[0];
                          replacement_title = top_el.getElementsByClassName(code + '_replacement_title_code')[0];
                          //update_dict =  {'root_cause': description.value, 'corrective_action': action_taken.value, 'time_spent': time_spent.value, 'replacement_order_code': replacement_order.value, 'replacement_title_code': replacement_title.value};
                          update_dict =  {'time_spent': time_spent.value, 'replacement_order_code': replacement_order.value, 'replacement_title_code': replacement_title.value};
                          selects = top_el.getElementsByTagName('select');
                          for(var r = 0; r < selects.length; r++){
                              name = selects[r].getAttribute('name');
                              value = selects[r].value;
                              update_dict[name] = value;    
                          }
                          checks = top_el.getElementsByClassName('spt_input');
                          for(var r = 0; r < checks.length; r++){
                               if(checks[r].type == 'checkbox'){
                                   field = checks[r].getAttribute('field');
                                   value = checks[r].checked;
                                   update_dict[field] = value;
                               }
                          } 
                          sk = server.build_search_key('twog/external_rejection', code);
                          server.update(sk, update_dict);
                          fault_files = top_el.getElementsByClassName('fault_files');
                          for(var r = 0; r < fault_files.length; r++){
                              tb = fault_files[r].getElementById('file_path-' + fault_files[r].getAttribute('line'));
                              if(tb){
                                  prev = fault_files[r].getAttribute('prev');
                                  if(fault_files[r].getAttribute('sk') != '' && tb.value != prev){
                                      //Then it already existed, just update it
                                      server.update(fault_files[r].getAttribute('sk'), {'file_path': tb.value});
                                  }else if(fault_files[r].getAttribute('sk') == '' && tb.value != ''){
                                      //Then it is a new entry, so create it
                                      server.insert('twog/external_rej_at_fault_files', {'file_path': tb.value, 'external_rejection_code': code});
                                  }
                              }
                          }
                          //spt.popup.close(spt.popup.get_popup(bvr.src_el));
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         ''' % code}
        return behavior

    def make_check_table(my, dictoid, arr, sob, my_name, color, is_external_rejection=False):
        table = Table()
        table.add_style('background-color: %s;' % color)
        max_width = 3
        table.add_row()
        top_cell = table.add_cell('<b><u>%s</u></b>' % my_name)
        top_cell.add_attr('colspan',max_width)
        top_cell.add_attr('align','center')
        count = 0
        for entry in arr:
            if count % max_width == 0:
                table.add_row()
            checker = CheckboxWdg('check_%s' % dictoid[entry])
            checker.add_attr('code', sob.get('code'))
            checker.add_attr('field', dictoid[entry])
            #checker.set_persistence()
            if sob.get(dictoid[entry]):
                checker.set_value(True)
            else:
                checker.set_value(False)
            if not is_external_rejection:
                checker.add_behavior(my.get_reason_check_behavior(dictoid[entry]))
            check_hold = table.add_cell(checker)
            check_hold.add_attr('code', sob.get('code'))
            check_hold.add_attr('field', dictoid[entry])
            label = table.add_cell(entry)
            label.add_attr('nowrap','nowrap')
            label.add_attr('width','190px')
            count = count + 1 
        return table

    def make_login_table(my, sob):
        table = Table()
        table.add_style('background-color: #fffff1;')
        max_width = 4
        table.add_row()
        top_cell = table.add_cell('<b><u>Responsible</u></b>')
        top_cell.add_attr('colspan',max_width)
        top_cell.add_attr('align','center')
        count = 0
        users = my.server.eval("@SOBJECT(sthpw/login['location','internal']['license_type','user']['@ORDER_BY','login'])")
        for u in users:
            if count % max_width == 0:
                table.add_row()
            checker = CheckboxWdg('responsible_%s' % u.get('login'))
            checker.add_attr('login',u.get('login'))
            checker.add_attr('code',sob.get('code'))
            checker.add_attr('current_list', sob.get('responsible_users'))
            #checker.set_persistence()
            if sob.get('responsible_users') not in [None,'']:
                if u.get('login') in sob.get('responsible_users'):
                    checker.set_value(True)
                else:
                    checker.set_value(False)
            else:
                checker.set_value(False)
            checker.add_behavior(my.get_make_responsible_behavior())
            table.add_cell(checker)
            label = table.add_cell(u.get('login'))
            label.add_attr('nowrap','nowrap')
            label.add_attr('width','137px')
            count = count + 1
        return table
      
                  
    def get_display(my):   
        my.code = str(my.kwargs.get('code'))
        is_external_rejection = False
        sob = None
        my.sk = None
        operator_description = 'operator_description'
        scheduler_description = 'scheduler_description'
        pre_type = 'Operator Description'
        rejection_cause_str = 'Rejection Cause'
        rejection_cause_field = 'rejection_cause'
        description_str = 'Description'
        description_field = 'description'
        action_taken_str = 'Action Taken'
        action_taken_field = 'action_taken'
        client_name = ''
        if 'EXTERNAL_REJECTION' in my.code:
            is_external_rejection = True
            sob = my.server.eval("@SOBJECT(twog/external_rejection['code','%s'])" % my.code)[0]
            operator_description = 'reported_issue'
            scheduler_description = 'reported_issue'
            pre_type = 'Reported Issue'
            rejection_cause_str = 'Root Cause Type'
            rejection_cause_field = 'root_cause_type'
            description_str = 'Root Cause'
            description_field = 'root_cause'
            action_taken_str = 'Corrective Action'
            action_taken_field = 'corrective_action'
            the_order = my.server.eval("@SOBJECT(twog/order['code','%s'])" % sob.get('order_code'))[0]
            client_name = the_order.get('client_name')
        else:
            sob = my.server.eval("@SOBJECT(twog/production_error['code','%s'])" % my.code)[0]
        my.sk = sob.get('__search_key__') 
        table = Table()
        table.add_attr('id','error_tbl_%s' % my.code)
        #table.add_style('background-color: #86a6da;')
        video_tbl = my.make_check_table(my.video_reasons, my.video_reasons_arr, sob, 'Video', '#ffef91', is_external_rejection)
        audio_tbl =  my.make_check_table(my.audio_reasons, my.audio_reasons_arr, sob, 'Audio', '#ffefa1', is_external_rejection)
        metadata_tbl =  my.make_check_table(my.metadata_reasons, my.metadata_reasons_arr, sob, 'MetaData', '#ffefb1', is_external_rejection)
        subtitle_tbl =  my.make_check_table(my.subtitle_reasons, my.subtitle_reasons_arr, sob, 'Subtitle', '#ffefc1', is_external_rejection)
        cc_tbl =  my.make_check_table(my.cc_reasons, my.cc_reasons_arr, sob, 'CC', '#ffefd1', is_external_rejection)
        if not is_external_rejection:
            login_tbl = my.make_login_table(sob)
        cause_sel = None
        assigned_sel = None
        corrective_action_sel = None
        status_sel = None
        if not is_external_rejection:
            cause_sel = SelectWdg('rejection_cause')
            cause_sel.append_option('--Select--','--Select--')
            for cause in my.rejection_causes:
                cause_sel.append_option(cause, cause)
                if cause == sob.get('rejection_cause'):
                    cause_sel.set_value(cause)
            cause_sel.add_behavior(my.get_sel_change_behavior(my.code, 'twog/production_error', 'rejection_cause')) 
        else:
            cause_sel = SelectWdg('root_cause_type')
            cause_sel.append_option('--Select--','--Select--')
            for cause in my.root_cause_types:
                cause_sel.append_option(cause, cause)
                if cause == sob.get('root_cause_type'):
                    cause_sel.set_value(cause)
            #cause_sel.add_behavior(my.get_sel_change_behavior(my.code, 'twog/external_rejection', 'root_cause_type')) 

            status_sel = SelectWdg('status')
            status_sel.append_option('--Select--','--Select--')
            for status in my.statuses:
                status_sel.append_option(status, status)
                if status == sob.get('status'):
                    status_sel.set_value(status)
            #status_sel.add_behavior(my.get_sel_change_behavior(my.code, 'twog/external_rejection','status')) 

            logins = my.server.eval("@GET(sthpw/login['location','internal']['license_type','!=','disabled']['@ORDER_BY','login asc'].login)")
            groups = my.server.eval("@GET(sthpw/login_group['login_group','not in','client|user|admin']['@ORDER_BY','login_group asc'].login_group)")
            assigned_sel = SelectWdg('assigned')
            assigned_sel.append_option('--Select--','--Select--')
            for login_str in logins:
                assigned_sel.append_option(login_str, login_str)
                if login_str == sob.get('assigned'):
                    assigned_sel.set_value(login_str)
            for group in groups:
                group = group.upper()
                assigned_sel.append_option(group, group)
                if group == sob.get('assigned'):
                    assigned_sel.set_value(group)
            #assigned_sel.add_behavior(my.get_sel_change_behavior(my.code, 'twog/external_rejection', 'assigned')) 

            corrective_action_sel = SelectWdg('corrective_action_assigned')
            corrective_action_sel.append_option('--Select--','--Select--')
            for login_str in logins:
                corrective_action_sel.append_option(login_str, login_str)
                if login_str == sob.get('corrective_action_assigned'):
                    corrective_action_sel.set_value(login_str)
            for group in groups:
                group = group.upper()
                corrective_action_sel.append_option(group, group)
                if group == sob.get('assigned'):
                    corrective_action_sel.set_value(group)
            #corrective_action_sel.add_behavior(my.get_sel_change_behavior(my.code, 'twog/external_rejection', 'corrective_action_assigned')) 

        cause_sel.add_style('width: 175px;')
        info_table = Table()
        info_table.add_row()
        info_table.add_cell('<b><u>Order:</u> %s [%s]</b>' % (sob.get('order_name'), sob.get('order_code')))
        my_title = sob.get('title')
        if sob.get('episode') not in [None,'']:
            my_title = '%s, %s' % (my_title, sob.get('episode'))
        info_table.add_cell('<b><u>Title:</u> %s [%s]</b>' % (my_title, sob.get('title_code')))
        
        if sob.get('work_order_code') not in [None,''] and not is_external_rejection:
            info_table.add_cell('<b><u>Work Order:</u> %s [%s]</b>' % (sob.get('process'), sob.get('work_order_code')))
        if is_external_rejection:
            from history import SObjectHistoryLauncherWdg
            histy = SObjectHistoryLauncherWdg(search_key=my.sk)
            hi = info_table.add_cell(histy)
            hi.add_attr('align','right')
        info_table.add_row()
        info1 = info_table.add_cell('<b><u>Client:</u> %s</b>' % client_name)
        info1.add_attr('nowrap','nowrap')
        if not is_external_rejection:
            info_table.add_cell('<b><u>Scheduler:</u> %s</b>' % sob.get('scheduler_login'))
            info_table.add_cell('<b><u>Operator:</u> %s</b>' % sob.get('operator_login'))
            info_table.add_row()
            info_table.add_cell('<b><u>Type:</u><font color="#ff0000"> %s</font></b>' % sob.get('error_type'))
        else:
            tb1 = Table()
            tb1.add_row()
            tb1.add_cell('Assigned:')
            tb1.add_cell(assigned_sel)
            info_table.add_cell(tb1)
            tb2 = Table()
            tb2.add_row()
            tt2 = tb2.add_cell('Corrective Action Assigned:')
            tt2.add_attr('nowrap','nowrap')
            tb2.add_cell(corrective_action_sel)
            info_table.add_cell(tb2)
            info_table.add_row()
            tb23 = Table()
            tb23.add_attr('width','100%s' % '%')
            tb23.add_row()
            tb231 = tb23.add_cell('&nbsp;')
            tb231.add_attr('width','20%s' % '%')
            tb23.add_cell('Replacement Order:')
            tb23.add_cell('<input type="text" value="%s" class="%s_replacement_order_code"/>' % (sob.get('replacement_order_code'), sob.get('code')))
            tb23.add_cell('&nbsp;')
            tb23.add_cell('Replacement Title:')
            tb23.add_cell('<input type="text" value="%s" class="%s_replacement_title_code"/>' % (sob.get('replacement_title_code'), sob.get('code')))
            info_table.add_cell(tb23)
        initial_descript = sob.get(operator_description)
        if initial_descript in [None,''] and not is_external_rejection:
            initial_descript = sob.get(scheduler_description)
            pre_type = 'Scheduler Description'
            if initial_descript in [None,'']:
                initial_descript = sob.get('client_description')
                pre_type = 'Client Description'
        info_table.add_row()
        #info_table.add_cell('<textarea cols="120" rows="4" style="background-color: #86a6da;" readonly>[%s]: %s</textarea>' % (pre_type, initial_descript)) 
        info_table.add_cell('<textarea cols="120" rows="4" style="background-color: #959595;" readonly>[%s]: %s</textarea>' % (pre_type, initial_descript)) 
        if is_external_rejection:
            info_table.add_row()
            files_tbl = FaultFilesWdg(external_rejection_code=sob.get('code'))
            info_table.add_cell(files_tbl)
        cause_tbl = Table()
        cause_tbl.add_attr('width','100%s' % '%')
        cause_tbl.add_style('background-color: #fefefe;')
        cause_tbl.add_row()
        rc = cause_tbl.add_cell('<b><u>%s:</u></b>' % rejection_cause_str)
        rc.add_attr('nowrap','nowrap')
        cause_tbl.add_cell(cause_sel)
        cause_tbl.add_cell('&nbsp;')
        ts = cause_tbl.add_cell('Time Spent: ')
        ts.add_attr('nowrap','nowrap')
        cause_tbl.add_cell('<input type="text" value="%s" class="%s_time_spent"/>' % (sob.get('time_spent'), sob.get('code')))
        if not is_external_rejection:
            longguy = cause_tbl.add_cell(' ')
            longguy.add_attr('width','100%s' % '%')
        else:
            tb3 = Table()
            tb3.add_row()
            tb3.add_cell('Status:')
            tb3.add_cell(status_sel)
            cause_tbl.add_cell(tb3)
        table.add_row()
        table.add_cell(info_table)
        table.add_row()
        table.add_cell(cause_tbl)
        table.add_row()
        table.add_cell(video_tbl)
        table.add_row()
        table.add_cell(audio_tbl)
        table.add_row()
        table.add_cell(metadata_tbl)
        table.add_row()
        table.add_cell(subtitle_tbl)
        table.add_row()
        table.add_cell(cc_tbl)
        if not is_external_rejection:
            table.add_row()
            table.add_cell(login_tbl)
        table.add_row()
        if not is_external_rejection:
            cme = table.add_cell('<b><u>%s</u></b>' % description_str)
            cme.add_attr('align','center')
            table.add_row()
            table.add_cell('<textarea cols="120" rows="10" class="%s_description">%s</textarea>' % (my.code, sob.get(description_field)))
            table.add_row()
            ame = table.add_cell('<b><u>%s</u></b>' % action_taken_str)
            ame.add_attr('align','center')
            table.add_row()
            table.add_cell('<textarea cols="120" rows="10" class="%s_action_taken">%s</textarea>' % (my.code, sob.get(action_taken_field)))
            table.add_row()
        else:
            from tactic.ui.widget import DiscussionWdg
            table.add_cell("<u><b>Root Cause</b></u>")
            table.add_row()
            root_cause_wdg = DiscussionWdg(search_key=my.sk,process='Root Cause',chronological=True)
            table.add_cell(root_cause_wdg)
            table.add_row()
            table.add_cell("<u><b>Corrective Action</b></u>")
            table.add_row()
            action_taken_wdg = DiscussionWdg(search_key=my.sk,process='Corrective Action',chronological=True)
            table.add_cell(action_taken_wdg)
            table.add_row()
            

        button = table.add_cell('<input type="button" value="Save"/>')
        button.add_attr('align','right')
        if not is_external_rejection:
            button.add_behavior(my.get_save_description_behavior(my.code))
        else:
            button.add_behavior(my.get_save_external_rejection(my.code))
        return table

class FaultFilesWdg(BaseTableElementWdg):
    def init(my):
        nothing = 'true'

    def get_kill_bvr(my, rowct, err_code, ff_code):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                            var rowct = Number('%s');
                            var err_code = '%s';
                            var ff_code = '%s';
                            if(confirm("Do you really want to delete this evaluation line?")){
                                server = TacticServerStub.get();
                                server.retire_sobject(server.build_search_key('twog/external_rej_at_fault_files',ff_code));
                                top_el = document.getElementById('error_tbl_' + err_code);
                                fftable = top_el.getElementsByClassName('fftable')[0];
                                fault_files = fftable.getElementsByClassName('fault_files');
                                for(var r = 0; r < fault_files.length; r++){
                                    if(fault_files[r].getAttribute('line') == rowct){
                                        fault_files[r].innerHTML = '';
                                        fault_files[r].style.display = 'none';
                                    }
                                }
                            }
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         ''' % (rowct, err_code, ff_code)}
        return behavior

    def get_add_line(my, rowct, err_code, ff_code):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                            bvr.src_el.innerHTML = '';
                            var rowct = Number('%s');
                            var err_code = '%s';
                            var ff_code = '%s';
                            top_el = document.getElementById('error_tbl_' + err_code);
                            fftable = top_el.getElementsByClassName('fftable');
                            lastfftable = fftable[fftable.length - 1];
                            addportions = top_el.getElementsByClassName('new_ff_line');
                            addportion = addportions[addportions.length - 1];
                            addportion.setAttribute('class','fault_files');
                            addportion.setAttribute('line',Number(rowct) + 1);
                            addportion.setAttribute('code','');
                            addportion.setAttribute('sk','');
                            new_row_ct = rowct + 1
                            //alert(new_row_ct);
                            send_data = {'rowct': new_row_ct, 'external_rejection_code': err_code, 'adding': 'true'};
                            spt.api.load_panel(addportion, 'order_builder.error_viewer.FaultFilesWdg', send_data); 
                            newrow = lastfftable.insertRow(-1);
                            newrow.setAttribute('class','new_ff_line');
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         ''' % (rowct, err_code, ff_code)}
        return behavior

    def txtbox(my, name, val, width='200px'):
        txt = TextWdg(name)
        txt.add_attr('id',name)
        txt.add_style('width: %s;' % width)
        txt.set_value(val)
        return txt

    def get_display(my):
        import time, datetime
        from tactic_client_lib import TacticServerStub
        from pyasm.common import Environment
        code = ''
        fault_files = None
        rowct = 1
        server = TacticServerStub.get()
        if 'external_rejection_code' in my.kwargs.keys():
            code = my.kwargs.get('external_rejection_code')
            fault_files = server.eval("@SOBJECT(twog/external_rej_at_fault_files['external_rejection_code','%s'])" % code) 
        if 'rowct' in my.kwargs.keys():
            rowct = int(my.kwargs.get('rowct'))
        adding = False
        if 'adding' in my.kwargs.keys():
            if my.kwargs.get('adding') == 'true':
                adding = True
        table = Table()
        table.add_attr('class','fftable')
        table.add_attr('border','1')
        if rowct == 1 and not adding:
            table.add_row()
            table.add_cell("<b>List of At-Fault Files:</b>")
        if code not in [None,''] and not adding:
            for ff in fault_files:
                brow = table.add_row()
                brow.add_attr('line',rowct)
                brow.add_attr('code',ff.get('code'))
                brow.add_attr('prev',ff.get('file_path'))
                brow.add_attr('sk',ff.get('__search_key__'))
                brow.add_attr('class','fault_files')
                table.add_cell(my.txtbox('file_path-%s' % rowct, ff.get('file_path'),width='700px'))
                killer = table.add_cell('<b>X</b>')#This must delete the entry
                killer.add_style('cursor: pointer;')
                killer.add_behavior(my.get_kill_bvr(rowct, code, ff.get('code')))
                rowct = rowct + 1
        erow = table.add_row()
        erow.add_attr('line',rowct)
        erow.add_attr('code','')
        erow.add_attr('prev','')
        erow.add_attr('sk','')
        erow.add_attr('class','fault_files')
        table.add_cell(my.txtbox('file_path-%s' % rowct, '',width='700px'))
        addnew = table.add_cell('<b>+</b>')#This must add new entry
        addnew.add_style('cursor: pointer;')
        addnew.add_behavior(my.get_add_line(rowct, code, ''))
        erow2 = table.add_row()
        erow2.add_attr('class','new_ff_line')
        return table
