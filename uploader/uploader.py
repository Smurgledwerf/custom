__all__ = ["CustomHTML5UploadButtonWdg","CustomHTML5UploadWdg","SnapshotViewerWdg"]
import tacticenv
from pyasm.biz import *
from pyasm.web import Table, DivWdg
from pyasm.widget import SelectWdg, IconWdg, TextWdg, CheckboxWdg
from tactic.ui.common import BaseTableElementWdg

class CustomHTML5UploadButtonWdg(BaseTableElementWdg):

    def init(my):
        nothing = 'true'

    def get_launch_behavior(my):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                          var my_sk = bvr.src_el.get('sk');
                          var processes = bvr.src_el.get('processes');
                          var class_name = 'uploader.CustomHTML5UploadWdg';
                          kwargs = {
                                           'sk': my_sk,
                                           'processes': processes
                                   };
                          spt.panel.load_popup('Upload', class_name, kwargs);
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         '''}
        return behavior

    def get_display(my):
        sob_sk = ''
        name = ''
        height = 20
        if 'sk' in my.kwargs.keys():
            sob_sk = str(my.kwargs.get('sk'))
        else: 
            sobject = my.get_current_sobject()
            sob_sk = sobject.get_search_key() 
        if 'name' in my.kwargs.keys():
            name = my.kwargs.get('name')
            if 'height' in my.kwargs.keys():
                height = my.kwargs.get('height') 
        processes = ''
        if 'processes' in my.kwargs.keys():
            processes = my.kwargs.get('processes')
            
        widget = DivWdg()
        table = Table()
        table.add_attr('width', '50px')
        table.add_row()
        cell1 = None
        if name == '':
            cell1 = table.add_cell('<img border="0" style="vertical-align: middle" title="" src="/context/icons/silk/_spt_upload.png">')
        else:
            cell1 = table.add_cell('<input type="button" value="%s" style="height: %spx"/>' % (name, height))
        cell1.add_attr('sk', sob_sk)
        cell1.add_attr('processes', processes)
        launch_behavior = my.get_launch_behavior()
        cell1.add_style('cursor: pointer;')
        cell1.add_behavior(launch_behavior)
        widget.add(table)
        return widget

class CustomHTML5UploadWdg(BaseTableElementWdg):
    def init(my):
        nothing = 'true'
        my.on_complete_js = '''
            try{
                var top = bvr.src_el.getParent(".html5_uploader_wdg");
                var processes = top.getAttribute('processes');
                var file_list = top.getElementById("html5_files_tbl");
                var values = spt.api.get_input_values(top);
                var files = values.upload;
                var inner = file_list.innerHTML;
                var new_files = '';
                if(processes == ''){
                    processes = ['--Select--','PO','QC','MISC'];
                }else{
                    cs = processes.split(',');
                    processes = [];
                    if(cs.length > 1){
                        processes.push('--Select--');
                    }
                    for(var r = 0; r < cs.length; r++){
                        processes.push(cs[r]);
                    }
                }
                var options = '';
                for(var r = 0; r < processes.length; r++){
                    options = options + '<option value="' + processes[r] + '">' + processes[r] + '</option>';
                }
                for(var r = 0; r < files.length; r++){
                    new_files = '<tr><td><input type="checkbox" class="do_chk" file="' + files[r] + '" checked/></td><td>' + files[r] + '</td><td>' + '<select class="context_sel" file="' + files[r] + '">' + options + '</select></td></tr>';  
                }
                file_list.innerHTML = inner + new_files;
                spt.app_busy.hide();
            }catch(e) {
                spt.alert(spt.exception.handler(e));
                server.abort();
            }
        '''

    def get_finish(my):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
            try{
                var top = bvr.src_el.getParent(".html5_uploader_wdg");
                var file_list = top.getElementById("html5_files_tbl");
                var good_to_go = true;
                var checks = file_list.getElementsByClassName("do_chk");
                var sels = file_list.getElementsByClassName("context_sel");
                pairs = [];
                none_selected = true;
                for(var r = 0; r < checks.length; r++){
                    if(checks[r].checked){
                        none_selected = false;
                        for(var p = 0; p < sels.length; p++){
                            if(sels[p].getAttribute('file') == checks[r].getAttribute('file')){
                                if(sels[p].value == "--Select--"){
                                    good_to_go = false;
                                }else{
                                    pairs.push([sels[p].getAttribute('file'), sels[p].value]);
                                }
                            }
                        }
                    }
                }
                if(!good_to_go){
                    spt.alert("Please choose a context for each selected file.");
                }
                if(none_selected){
                    good_to_go = false;
                    spt.alert("Please select the file(s) you want to assign the context(s) to.");
                }
                if(good_to_go){
                    if(confirm("Ready to go? Please hit 'Cancel' if any of your selected files has an incorrect context selection.")){
                        var server = TacticServerStub.get();
                        var sk = top.getAttribute('sk');
                        var ticket = top.getAttribute('ticket');
                        server.start({"title": "Uploading...", "description": "uploading_html5", "transaction_ticket": ticket});
                        for(var r = 0; r < pairs.length; r++){
                            var filename = pairs[r][0];
                            var context = pairs[r][1];
                            spt.app_busy.show("Adding " + filename);
                            server.simple_checkin(sk, context, filename, {'mode': 'uploaded'});
                        }
                        spt.app_busy.hide();
                        server.finish();
                        spt.api.load_panel(top, 'uploader.CustomHTML5UploadWdg', {'sk': sk});
                    }
                }
            }catch(e) {
                spt.alert(spt.exception.handler(e));
                server.abort();
            }'''}
        return behavior

    def get_display(my):
        from client.tactic_client_lib import TacticServerStub
        from tactic.ui.input import UploadButtonWdg
        server = TacticServerStub.get()
        ticket = server.generate_ticket()
        sk = str(my.kwargs.get('sk'))
        processes = str(my.kwargs.get('processes'))
        code = sk.split('code=')[1];
        #sobject = server.get_by_search_key(sk)
        widget = DivWdg()
        table = Table()
        table.add_attr('class','html5_uploader_wdg')
        table.add_attr('sk',sk)
        table.add_attr('processes',processes)
        table.add_attr('ticket',ticket)
        table.add_row()
        snaps = SnapshotViewerWdg(sk=sk)
        longcell1 = table.add_cell(snaps)
        longcell1.add_attr('colspan','2')
        table.add_row()
        context = 'PO'
        upload_button = UploadButtonWdg(context=context, ticket=ticket, on_complete=my.on_complete_js, search_key=sk, title="Select a File for %s" % code, stupid_button=True) 
        table.add_cell(upload_button)
        files_tbl = Table()
        files_tbl.add_attr('id','html5_files_tbl')
        table.add_row()
        files = table.add_cell(files_tbl)
        files.add_attr('colspan','2')
        table.add_row()
        uno = table.add_cell(' ')
        uno.add_attr('width','100%s' % '%')
        butt = table.add_cell('<input type="button" value="Assign Context & Finish"/>') 
        butt.add_behavior(my.get_finish())
        tres = table.add_cell(' ')
        tres.add_attr('width','100%s' % '%')
       
        #table.add_cell(sk)
        widget.add(table)
        return widget

class SnapshotViewerWdg(BaseTableElementWdg):
    def init(my):
        nothing = 'true'

    def get_display(my):
        import re
        from client.tactic_client_lib import TacticServerStub
        from tactic.ui.panel import FastTableLayoutWdg
        server = TacticServerStub.get()
        sk = str(my.kwargs.get('sk'))
        splits = sk.split('code=')
        search_type = splits[0].split('?')[0];
        code = splits[1];
        search_id = re.findall(r'\d+', code)
        search_id = int(search_id[0])
        widget = DivWdg()
        table = Table()
        table.add_attr('class','snapshot_viewer_wdg')
        table.add_attr('sk',sk)
        #ftl = FastTableLayoutWdg(search_type='sthpw/snapshot', view='table', element_names='preview,process,description,web_path,timestamp,login', show_row_select=True, search_key=sk, show_gear=False, show_shelf=False, show_select=True, width='100%s' % '%', show_column_manager=False, expression="@UNION(@SOBJECT(sthpw/snapshot),@SOBJECT(sthpw/note.sthpw/snapshot))", temp=True)
        if search_type == 'sthpw/note':
            expression = "@SOBJECT(sthpw/snapshot)"
        else:
            expression="@UNION(@SOBJECT(sthpw/snapshot),@SOBJECT(sthpw/note.sthpw/snapshot))"
        ftl = FastTableLayoutWdg(search_type='sthpw/snapshot', view='snapshot_by_process', show_row_select=True, search_key=sk, show_gear=False, show_shelf=False, show_select=True, height='300px', width='100%s' % '%', show_column_manager=False, expression=expression, temp=True)
        table.add_row()
        table.add_cell(ftl) 
        widget.add(table)
        return widget
