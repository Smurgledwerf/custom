__all__ = ["FileBrowser","FileBrowserDirectoryContents"]
import tacticenv
#import time
import os, math, commands
from datetime import datetime
from os.path import isfile, join
from pyasm.common import Environment
from pyasm.biz import *
from pyasm.web import Table, DivWdg
from pyasm.widget import SelectWdg, IconWdg, TextWdg, CheckboxWdg
from pyasm.search import Search
from tactic.ui.common import BaseRefreshWdg
from sandbox import MediaInfoFile

class FileBrowser(BaseRefreshWdg):
    def init(my):
        #my.start_dir = '/Volumes'
        my.start_dir = my.kwargs.get('start_dir')
        if my.start_dir in [None,'']:
            #my.start_dir = '/opt/spt/custom/'
            my.start_dir = '/Volumes'
        my.mode = my.kwargs.get('mode')
        my.custom_top_name = my.kwargs.get('custom_top_name')
        if my.custom_top_name in [None,'']:
            my.custom_top_name = ''
    
    def get_display(my):   
        widget = DivWdg()
        contents_div = FileBrowserDirectoryContents(dir=my.start_dir,mode=my.mode,custom_top_name=my.custom_top_name)
        table = Table()
        table.add_attr('id','top_of_file_browser_%s' % my.custom_top_name)
        table.add_row()
        con_div = table.add_cell(contents_div)
        con_div.add_attr('id','con_div')
        widget.add(table)
        return widget 

class FileBrowserDirectoryContents(BaseRefreshWdg):
    def init(my):
        my.start_dir = '/Volumes'
        my.dir = '/Volumes'
        my.old_dir = '/Volumes'
        my.folder_icon = '<img src="/context/icons/silk/folder.png" title="TITLE" name="TITLE"/>'
        my.file_icon = '<img src="/context/icons/silk/page_white_text.png" title="TITLE" name="TITLE"/>'
        my.mode = 'classic'
        my.custom_top_name = my.kwargs.get('custom_top_name')

    def dir_click(my):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                               var custom_top_name = '%s';
                               var new_dir = bvr.src_el.getAttribute('dir'); 
                               if(new_dir.indexOf('/Volumes') == 0){
                                   var top_el = document.getElementById("top_of_file_browser_" + custom_top_name);
                                   dir_list = top_el.getElementById('dir_div');
                                   contents_list = top_el.getElementById('con_div');
                                   spt.api.load_panel(contents_list, 'file_browser.file_browser.FileBrowserDirectoryContents', {'dir': new_dir, 'custom_top_name': custom_top_name}); 
                               }else{
                                   spt.alert("You do not have permission to navigate those realms.");
                               }
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         ''' % my.custom_top_name}
        return behavior

    def select_fp(my, fr_ending):
        behavior = {'type': 'double_click', 'cbjs_action': '''        
                        try{
                               var fr_ending = '%s';
                               var path = bvr.src_el.getAttribute('path_name'); 
                               var tbs = document.getElementsByClassName('forced_response');
                               for(var r = 0; r < tbs.length; r++){
                                   if(tbs[r].getAttribute('mode') == 'file_path' && tbs[r].id == 'forced_response_' + fr_ending){
                                       val = tbs[r].value;
                                       if(val == '' || val == null){
                                           val = path;
                                       }else{
                                           val = val + '\\n' + path;
                                       }
                                       tbs[r].value = val;
                                   }
                               }
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         ''' % fr_ending}
        return behavior

    def click_anywhere(my):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                               var custom_top_name = '%s';
                               top_el = document.getElementById('whole_fb_container_' + custom_top_name);
                               all_els = top_el.getElementsByTagName('td');
                               for(var r = 0; r < all_els.length; r++){
                                   if(all_els[r].getAttribute('name') == 'clickable'){
                                       all_els[r].setAttribute('highlight','off');
                                       all_els[r].style.backgroundColor = '#FFFFFF';
                                   }
                               }
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         ''' % my.custom_top_name}
        return behavior

    def change_location(my, current_location):
        behavior = {'css_class': 'clickme', 'type': 'change', 'cbjs_action': '''        
                        try{
                               var current_location = '%s';
                               var custom_top_name = '%s';
                               var new_dir = bvr.src_el.value; 
                               if(new_dir.indexOf('/Volumes') == 0){
                                   var top_el = document.getElementById("top_of_file_browser_" + custom_top_name);
                                   dir_list = top_el.getElementById('dir_div');
                                   contents_list = top_el.getElementById('con_div');
                                   spt.api.load_panel(contents_list, 'file_browser.file_browser.FileBrowserDirectoryContents', {'dir': new_dir, 'old_dir': current_location, 'custom_top_name': custom_top_name}); 
                               }else{
                                   spt.alert("You do not have permission to navigate those realms.");
                               }
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         ''' % (current_location, my.custom_top_name)}
        return behavior

    # When we start moving a file to a folder we need to know its path and extension
    # With an extension, we can determine if we could move the file as it has to be a movie one
    # We attach drag_controller on all the div elements that can be used as dropin bins and 
    def drag_controller(my):
        behavior = {
        'type': 'load',
                'cbjs_action': '''

                try{
                var custom_top_name = '%s';
                spt.drag = {};


                spt.getExtension = function(filename){

                    // We need this function so we can check for the spt 

                    var a = filename.split(".");
                    if( a.length === 1 || ( a[0] === "" && a.length === 2 ) ) {
                        return "";
                    }
                    return a.pop();

                };

                spt.drag.ondragstart = function(evt, el, arg) 
                {       
                        top_el = document.getElementById('whole_fb_container_' + custom_top_name);
                        all_els = top_el.getElementsByTagName("td");
                        all_paths = ''
                        for(var r = 0; r < all_els.length; r++){
                            if(all_els[r].getAttribute('name') == 'clickable'){
                                if(all_els[r].getAttribute('highlight') == 'on'){
                                    attr = 'path_name';
                                    if(all_els[r].getAttribute('type') == 'dir'){
                                        attr = 'dir';
                                    }
                                    if(all_paths != ''){
                                        all_paths = all_paths + ',' + all_els[r].getAttribute(attr);
                                    }else{
                                        all_paths = all_els[r].getAttribute(attr);
                                    }
                                }
                            }
                        }
                        //evt.dataTransfer.setData('text/plain', arg.path_name);
                        if(all_paths != ''){
                            evt.dataTransfer.setData('text/plain', all_paths);
                        }else{
                            evt.dataTransfer.setData('text/plain', arg.path_name);
                        }
                };

                spt.drag.ondrop = function(evt, el, arg) 
                {
      
                       // Logic: When we drop an item to the folder we need to check for an extension, if it is video - allow to execute move 
                       // While it is moving we need to show some type of loading modal page
                       // When it is done - Confirmation of move 

                       // To-do: Connect each move to a database by generating hash of a filename and trying to access it in the database

                        var new_dir = bvr.src_el.getAttribute('dir'); 

                        if (evt.preventDefault) 
                        {
                            evt.preventDefault(); 
                        }

                         // Getting the server, file_path and destination path
                        var server = TacticServerStub.get();

                        var destination_location = arg.destination_location;
                        destination_location =  escape(destination_location);

                        var file_locations = evt.dataTransfer.getData('text/plain');
                        //file_locations = escape(file_locations);
                        fl_s = file_locations.split(',');
                        //alert("FL_S = " + fl_s);
                        for(var r = 0; r < fl_s.length; r++){
                            file_location = escape(fl_s[r]);
                            //alert('Dropped: ' + file_location);
                            //alert('Into: ' + destination_location);

                            //server.execute_cmd('sandbox.Sandbox_File.MediaInfoFile.copy2', {origin: file_location, destination: destination_location})
                            server.execute_cmd('sandbox.Sandbox_File.MediaInfoFile', {'origin': file_location, 'destination': destination_location, 'mode': 'copy2'})
                        }
                        var top_el = document.getElementById("top_of_file_browser_" + custom_top_name);
                        reload_dir_el = top_el.getElementById('dir_path');
                        reload_dir = reload_dir_el.value;
                        spt.api.load_panel(contents_list, 'file_browser.file_browser.FileBrowserDirectoryContents', {'dir': reload_dir, 'custom_top_name': custom_top_name}); 

                        return false;
                };

                spt.drag.allowDrop = function(evt)
                {
                        evt.stopPropagation();
                        evt.preventDefault();
                };
                }
                
                catch(e){
                    alert(spt.exception.handler(e));
                }
                

                ''' % my.custom_top_name}
        return behavior

    def hover_highlighter(my):
        behavior = {'type': 'hover', 'cbjs_action_over': '''        
                               highlighted = bvr.src_el.getAttribute('highlight');
                               if(highlighted == 'on'){
                                   bvr.src_el.style.backgroundColor = '#81DDBA';
                               }else{
                                   bvr.src_el.style.backgroundColor = '#FFEE77';
                               } 
         ''', 'cbjs_action_out': '''
                               highlighted = bvr.src_el.getAttribute('highlight');
                               if(highlighted == 'on'){
                                   bvr.src_el.style.backgroundColor = '#00ccff';
                               }else{
                                   bvr.src_el.style.backgroundColor = '#FFFFFF';
                               }
             '''
            }
        return behavior

    def highlighter_ctrl(my):
        behavior = {'type': 'click_up', 'mouse_btn': 'LMB', 'modkeys': 'CTRL', 'cbjs_action': '''        
                        try{
                               highlighted = bvr.src_el.getAttribute('highlight');
                               if(highlighted == 'on'){
                                   //Then turn it off
                                   bvr.src_el.style.backgroundColor = '#FFFFFF';
                                   bvr.src_el.setAttribute('highlight','off');
                               }else{
                                   //Then turn it on
                                   bvr.src_el.style.backgroundColor = '#00ccff';
                                   bvr.src_el.setAttribute('highlight','on');
                               } 
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         '''}
        return behavior
 
    def convertSize(my, size, type):
       if size not in [0,'0','',None]:
           size_name = ("KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
           if type == 'file':
               size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
           i = int(math.floor(math.log(size,1024)))
           p = math.pow(1024,i)
           s = round(size/p,2)
           if (s > 0):
               return '%s %s' % (s,size_name[i])
           else:
               return '0 B'
       else:
           return '0 B'

    def normalize_size(my, size_str):
        return size_str.replace('K',' KB').replace('M',' MB').replace('G',' GB').replace('T',' TB').replace('P',' PB')

    def get_display(my):   
        widget = DivWdg()
        widget.add_attr('id','whole_fb_container_%s' % my.custom_top_name)
        if 'dir' in my.kwargs.keys():
            my.dir = my.kwargs.get('dir')
        if 'old_dir' in my.kwargs.keys():
            my.old_dir = my.kwargs.get('old_dir')
        else:
            my.old_dir = my.dir
        if 'mode' in my.kwargs.keys():
            my.mode = my.kwargs.get('mode')
            if my.mode in [None,'']:
                my.mode = 'classic'
        #print "DIR = %s, OLD DIR = %s" % (my.dir, my.old_dir)
        
        err_msg = ''
        if not os.path.isdir(my.dir):
            err_msg = '%s is not a valid directory' % my.dir 
            my.dir = my.old_dir
       
        trimmed_dir = my.dir
        if trimmed_dir[len(trimmed_dir) - 1] == '/' and len(trimmed_dir) > 1:
            trimmed_dir = trimmed_dir[:-1]
        
        prev_dir_s = trimmed_dir.split('/')
        prev_dir_s = prev_dir_s[:-1]
        prev_dir = ''
        
        for ct in range(0,len(prev_dir_s)):
            if prev_dir_s[ct] not in [None,'']:
                if prev_dir == '':
                    prev_dir = '/%s' % prev_dir_s[ct]
                else:   
                    prev_dir = '%s/%s' % (prev_dir, prev_dir_s[ct])
        if prev_dir in [None,'','//']:
            prev_dir = '/'
        #print "PREV DIR = %s" % prev_dir
        
        files_list = []
        dir_list = []
        
        files_dict = {}
        dirs_dict = {}
        
        longest_name_len = 0
        
        for f in os.listdir(my.dir):
            joined = join(my.dir,f)
            if os.path.isfile(joined):
                files_list.append(joined)
                last_modified = 'N/A'
                created = 'N/A'
                size = 'N/A'
                if joined.count('/') > 3:
                    last_modified =  datetime.fromtimestamp(os.path.getmtime(joined)).strftime('%Y-%m-%d %H:%M:%S')
                    created =  datetime.fromtimestamp(os.path.getctime(joined)).strftime('%Y-%m-%d %H:%M:%S')
                    size = my.convertSize(os.path.getsize(joined),'file')
                file_name_s = joined.split('/')
                file_name = file_name_s[len(file_name_s) - 1]
                file_path = joined
                files_dict[joined] = {'last_modified': last_modified, 'created': created, 'size': size, 'name': file_name, 'path': joined}
                if len(file_name) > longest_name_len:
                    longest_name_len = len(file_name)
            
            elif os.path.isdir(joined):
                dir_name_s = joined.split('/')
                dir_name = dir_name_s[len(dir_name_s) - 1]
                if dir_name[0] != '.':
                    dir_list.append(joined)
                    size = 'N/A'
                    created = 'N/A'
                    last_modified = 'N/A'
                   
                    #This is to keep us from calculating the size of the huge base directories
                    #Probably want a way to turn directory sizes on and off
                    if joined.count('/') > 5:
                        last_modified =  datetime.fromtimestamp(os.path.getmtime(joined)).strftime('%Y-%m-%d %H:%M:%S')
                        created =  datetime.fromtimestamp(os.path.getctime(joined)).strftime('%Y-%m-%d %H:%M:%S')
                        prepresize = commands.getoutput('du -s %s' % joined).split()[0]
                        try:
                            presize = float(prepresize)
                            if not math.isnan(presize):
                                size = my.convertSize(float(presize),'dir')
                        except ValueError:
                            print "GOT AN ERROR FOR %s" % joined
                            pass
                    dir_path = joined
                    dirs_dict[joined] = {'size': size, 'created': created, 'last_modified': last_modified, 'name': dir_name, 'path' : dir_path}
                    if len(dir_name) > longest_name_len:
                        longest_name_len = len(dir_name)
        
        #print "LONGEST NAME LEN = %s" % longest_name_len
        name_len = longest_name_len * 10
        
        # Displaying the table of the folders and files 
        top_tbl = Table()
        if err_msg != '':
            top_tbl.add_row()
            top_tbl.add_cell('<b><font color="#FF0000">%s</font></b>' % err_msg)
        top_tbl.add_row()
        dir_path_txt = TextWdg('dir_path')
        dir_path_txt.add_attr('id','dir_path')
        dir_path_txt.set_value(my.dir)
        dir_path_txt.set_option('size','100')
        dir_path_txt.add_behavior(my.change_location(my.old_dir))
        top_tbl.add_cell('Location: ')
        top_tbl.add_cell(dir_path_txt)
        
        div = DivWdg()
        
        back_tbl = Table()
        back_dir = back_tbl.add_cell("<-Back...")
        back_dir.add_attr('dir',prev_dir)
        back_dir.add_style('cursor: pointer;')
        back_dir.add_style('width: %spx;' % name_len)
        back_dir.add_behavior(my.dir_click())
        back_size = back_tbl.add_cell('Size')
        back_size.add_style('width: 100px;')
        back_created = back_tbl.add_cell('Created')
        back_created.add_style('width: 150px;')
        back_modified = back_tbl.add_cell('Last Modified')
        back_modified.add_style('width: 150px;')
        div.add(back_tbl)
    
        content_counter = 0
        dir_list.sort()
        files_list.sort()
        mult_dirs = DivWdg()
        mult_dirs.add_attr('class','DragContainer')
        mult_dirs.add_attr('id','DragContainer1')

        # Getting all the directories displayed, adding drag and drop attributes to each folder 
        for dr in dir_list:
         
            tbl = Table()
            tbl.add_row()
            dir_name = dirs_dict[dr]['name']
            dir_path = dirs_dict[dr]['path']
            FOLDER_ICON = my.folder_icon.replace("TITLE",dir_name)
            lil_tbl = Table()
            lil_tbl.add_row()
            lil_tbl.add_cell(FOLDER_ICON)
            
            directory_div = lil_tbl.add_cell('<b>%s</b>' % dir_name)
            
            if my.mode not in ['select']:
                directory_div.add_behavior(my.drag_controller())
                directory_div.add_style("-khtml-user-drag: element;")
                directory_div.add_attr("draggable", "true")
                directory_div.add_attr("ondragstart", "spt.drag.ondragstart(event, this, {path_name : '%s'}) "% dir_path)
                directory_div.add_attr("ondragover", "spt.drag.allowDrop(event, this)")
                directory_div.add_attr("ondrop", "spt.drag.ondrop(event, this, {destination_location: '%s'})" % dir_path)

            lil_cell = tbl.add_cell(lil_tbl)
            lil_cell.add_attr('name','clickable')
            lil_cell.add_attr('dir',dr)
            lil_cell.add_attr('type','dir')
            lil_cell.add_attr('path_name',dr)
            lil_cell.add_attr('highlight','off')
            #lil_cell.add_attr('class','biotches')
            lil_cell.add_style('cursor: pointer;')
            lil_cell.add_style('width: %spx;' % name_len)
            lil_cell.add_behavior(my.dir_click())
            lil_cell.add_behavior(my.highlighter_ctrl());
            lil_cell.add_behavior(my.hover_highlighter());
            if my.mode in ['select']:
                lil_cell.add_behavior(my.select_fp(my.custom_top_name))
            
            sc = tbl.add_cell('<i>%s</i>' % dirs_dict[dr]['size'])
            sc.add_attr('nowrap','nowrap')
            sc.add_attr('title','Size of Contents')
            sc.add_attr('name','Size of Contents')
            sc.add_style('width: 100px;')
           
            cc = tbl.add_cell(dirs_dict[dr]['created'])
            cc.add_attr('nowrap','nowrap')
            cc.add_attr('title','Created')
            cc.add_attr('name','Created')
            cc.add_style('width: 150px;')
         
            mc = tbl.add_cell(dirs_dict[dr]['last_modified'])
            mc.add_attr('nowrap','nowrap')
            mc.add_attr('title','Last Modified')
            mc.add_attr('name','Last Modified')
            mc.add_style('width: 150px;')
            div_dir = DivWdg()
            div_dir.add(tbl)
            mult_dirs.add(div_dir)
            content_counter = content_counter + 1
        div.add(mult_dirs)
        mult_files = DivWdg()
        mult_files.add_attr('class','DragContainer')
        mult_files.add_attr('id','DragContainer2')
        
        for fl in files_list:
            tbl = Table()
            tbl.add_row()

            file_name = files_dict[fl]['name']
            path_name = files_dict[fl]['path']

            text_wdg_file_name = DivWdg(file_name)
            if my.mode not in ['select']:
                text_wdg_file_name.add_behavior(my.drag_controller())
                text_wdg_file_name.add_style("-khtml-user-drag: element;")
                text_wdg_file_name.add_attr("draggable", "true")
                text_wdg_file_name.add_attr("ondragstart", "spt.drag.ondragstart(event, this, {path_name : '%s'}) "% path_name)
            
            FILE_ICON = my.file_icon.replace("TITLE",file_name)
            lil_tbl = Table()
            lil_tbl.add_row()
            lil_tbl.add_cell(FILE_ICON)
            file_div = lil_tbl.add_cell(text_wdg_file_name)
            lil_cell = tbl.add_cell(lil_tbl)
            lil_cell.add_attr('name','clickable')
            lil_cell.add_attr('file',fl)
            lil_cell.add_attr('type','file')
            lil_cell.add_attr('file_name',file_name)
            lil_cell.add_attr('path_name',path_name)
            lil_cell.add_attr('highlight','off')
            #lil_cell.add_attr('class','biotches')
            lil_cell.add_style('cursor: pointer;')
            lil_cell.add_style('width: %spx;' % name_len)
            lil_cell.add_behavior(my.highlighter_ctrl())
            lil_cell.add_behavior(my.hover_highlighter());
            if my.mode in ['select']:
                lil_cell.add_behavior(my.select_fp(my.custom_top_name))
            else:
                lil_cell.add_behavior(my.select_fp(my.custom_top_name))
             
            sc = tbl.add_cell('<i>%s</i>' % files_dict[fl]['size'])
            sc.add_attr('nowrap','nowrap')
            sc.add_attr('title','Size')
            sc.add_attr('name','Size')
            sc.add_style('width: 100px;')
            cc = tbl.add_cell(files_dict[fl]['created'])
            cc.add_attr('nowrap','nowrap')
            cc.add_attr('title','Created')
            cc.add_attr('name','Created')
            cc.add_style('width: 150px;')
            mc = tbl.add_cell(files_dict[fl]['last_modified'])
            mc.add_attr('nowrap','nowrap')
            mc.add_attr('title','Last Modified')
            mc.add_attr('name','Last Modified')
            mc.add_style('width: 150px;')
            div_fl = DivWdg()
            div_fl.add(tbl)
            mult_files.add(div_fl)
            content_counter = content_counter + 1
        div.add(mult_files)
        widget.add(top_tbl)
        widget.add(div)
        widget.add_behavior(my.click_anywhere())
        return widget 
