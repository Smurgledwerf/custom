__all__ = ["LabelLauncherWdg","LabelWdg"]
import tacticenv
import os, datetime
from pyasm.biz import *
from pyasm.web import Table, DivWdg
from pyasm.widget import SelectWdg
from tactic.ui.common import BaseTableElementWdg
from tactic.ui.common import BaseRefreshWdg
from tactic.ui.panel import EditWdg

class LabelLauncherWdg(BaseTableElementWdg):

    def init(my):
        from tactic_client_lib import TacticServerStub
        my.server = TacticServerStub.get()

    def get_launch_behavior(my):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                          var server = TacticServerStub.get();
                          var code = bvr.src_el.get('code');
                          var title = bvr.src_el.get('title');
                          var class_name = 'order_builder.LabelWdg';
                          kwargs = {
                                           'code': code
                                   };
                          spt.panel.load_popup('Print Label for ' + title, class_name, kwargs);
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                          //alert(err);
                }
         '''}
        return behavior

    def get_display(my):
        sobject = my.get_current_sobject()
        code = sobject.get_code()
        title = sobject.get_value('title')
        widget = DivWdg()
        table = Table()
        table.add_attr('width', '50px')
        table.add_row()
        cell1 = table.add_cell('<img border="0" style="vertical-align: middle" title="" src="/context/icons/silk/printer.png">')
        launch_behavior = my.get_launch_behavior()
        cell1.add_attr('code',code)
        cell1.add_attr('title',title)
        cell1.add_style('cursor: pointer;')
        cell1.add_behavior(launch_behavior)
        widget.add(table)

        return widget

class LabelWdg(BaseRefreshWdg):

    def init(my):
        from client.tactic_client_lib import TacticServerStub
        from pyasm.common import Environment
        my.server = TacticServerStub.get()
        my.types = ['HDCAM','HDCAM_TV_FOX','HDCAM_FILM_FOX','HDCAM DIGIBETA','DVD','D5']
        my.template_files = {'HDCAM': '/var/www/html/source_labels/HDCAM_label.html', 'HDCAM_FILM_FOX': '/var/www/html/source_labels/HDCAM_FILM_FOX_label.html', 'HDCAM_TV_FOX': '/var/www/html/source_labels/HDCAM_TV_FOX_label.html', 'HDCAM DIGIBETA': '/var/www/html/source_labels/HDCAM_Digibeta_label.html', 'DVD': '/var/www/html/source_labels/DVD_Label.html', 'D5': '/var/www/html/source_labels/D5_label.html'}
    
    def get_display(my):   
        code = str(my.kwargs.get('code'))
        source = my.server.eval("@SOBJECT(twog/source['code','%s'])" % code)[0]
        client_name = ''
        if source.get('client_code') not in [None,'']:
            client_names = my.server.eval("@GET(twog/client['code','%s'].name)" % source.get('client_code'))
            if len(client_names) > 0:
                client_name = client_names[0]
        whole_title = source.get('title')
        if source.get('episode') not in [None,'']:
            whole_title = '%s: %s' % (whole_title, source.get('episode')) 

        chunk_lines = whole_title
        if len(whole_title) > 20:
            chunks = whole_title.split(' ')
            len_chunks = len(chunks)
            chunk_sum = 0
            last_bit = ''
            chunk_lines = ''
            for chunk in chunks:
                clen = len(chunk)
                chunk_sum = clen + chunk_sum + 1
                if chunk_sum > 20:
                    chunk_sum = 0
                    chunk_lines = '%s %s<br/>' % (chunk_lines, last_bit)
                else:
                    if chunk_lines == '':
                        chunk_lines = last_bit
                    else:
                        chunk_lines = '%s %s' % (chunk_lines, last_bit)
                last_bit = chunk

            end_part = chunks[len_chunks - 1]
            len_end = len(end_part)
            if len_end + chunk_sum > 20:
                chunk_lines = '%s<br/>%s' % (chunk_lines, end_part)
            else:
                chunk_lines = '%s %s' % (chunk_lines, end_part)
        whole_title = chunk_lines
            
        barcode = source.get('barcode')
        captioning = source.get('captioning')
        if captioning in ['',None]:
            captioning = 'N/A'
        subtitles = source.get('subtitles')
        if subtitles in ['',None]:
            subtitles = 'N/A' 
        table = Table()
        table.add_attr('class','print_label_wdg')
        table.add_row()
        select = SelectWdg('label_type')
        for guy in my.types:
            select.append_option(guy,guy)  
        selly = table.add_cell(select)
        selly.add_attr('align','center')
        table.add_row()
        date = str(datetime.datetime.now()).split(' ')[0]
        audio_lines = ''
        audio_layout = [[1,7],[2,8],[3,9],[4,10],[5,11],[6,12]]
        for layout in audio_layout:
            this_line = ''
            left = layout[0]
            left_str = '%s' % left
            left_line = ''
            found_left = False
            if len(left_str) == 1:
                left_str = '0%s' % left_str
            if source.get('audio_ch_%s' % left) not in [None, '']:
                left_line = '<div id="chleftreplace">CH%s: %s</div>' % (left_str, source.get('audio_ch_%s' % left))
                found_left = True
            right = layout[1]
            right_str = '%s' % right
            right_line = ''
            found_right = False
            if len(right_str) == 1:
                right_str = '0%s' % right_str
            if source.get('audio_ch_%s' % right) not in [None,'']:
                right_line  = '<div id="chrightreplace">CH%s: %s</div>' % (right_str, source.get('audio_ch_%s' % right))
                found_right = True
            if found_left and not found_right:
                this_line = '%s<div id="chrightreplace">&nbsp;</div>\n' % (left_line)
            if found_left and found_right:
                this_line = '%s%s\n' % (left_line, right_line)
            if not found_left and found_right:
                this_line = '<div id="chleftreplace">&nbsp;</div>%s\n' % (right_line)
            if this_line != '':
                audio_lines = '%s%s' % (audio_lines, this_line)
        mtminfo = ''
        if source.get('description') not in [None,'']:
            mtminfo = '''%s<font id="replace"><i>%s</i></font></br>''' % (mtminfo, source.get('description'))
        if source.get('aspect_ratio') not in [None,'']:
            mtminfo = '''%s<font id="replace">Aspect Ratio: %s</font><br/>''' % (mtminfo, source.get('aspect_ratio'))
        if source.get('captioning') not in [None,'']:
            mtminfo = '''%s<font id="replace">Captioning: %s</font><br/>''' % (mtminfo, source.get('captioning'))
        if source.get('textless') not in [None,'']:
            mtminfo = '''%s<font id="replace">Textless: %s</font><br/>''' % (mtminfo, source.get('textless'))
        if source.get('po_number') not in [None,'']:
            mtminfo = '''%s<font id="replace">PO #: %s</font><br/>''' % (mtminfo, source.get('po_number'))
        if barcode not in [None,'']:
            for guy in my.types:
                result = ''
                f = open(my.template_files[guy], 'r')
                for line in f:
        	        if not line.strip():
        		    continue
        	        else:
        		    line = line.rstrip('\r\n')
                            line =line.replace('[WHOLETITLE]', whole_title)
                            line =line.replace('[TITLE]',source.get('title'))
                            line =line.replace('[EPISODE]',source.get('episode'))
                            line =line.replace('[BARCODE]',barcode)
                            line =line.replace('[TOTAL_RUN_TIME]',source.get('total_run_time'))
                            line =line.replace('[TRT]',source.get('total_run_time'))
                            line =line.replace('[VERSION]',source.get('version'))
                            line =line.replace('[ASPECT_RATIO]',source.get('aspect_ratio'))
                            line =line.replace('[COLOR_SPACE]',source.get('color_space'))
                            line =line.replace('[STRAT2G_PART]',source.get('part'))
                            if '[AUDIO_CHANNELS' in line:
                                replacer = ''
                                full_tag = '[AUDIO_CHANNELS]'
                                if 'SMALL' in line:
                                    replacer = '_small'
                                    full_tag = '[AUDIO_CHANNELS_SMALL]'
                                if 'LARGE' in line:
                                    replacer = '_large'
                                    full_tag = '[AUDIO_CHANNELS_LARGE]'
                                line = line.replace(full_tag, audio_lines.replace('replace',replacer))
                            if '[MTMINFOCHUNK_' in line:
                                replacer = 'medium'
                                full_tag = '[MTMINFOCHUNK_MEDIUM]'
                                if 'SMALL' in line:
                                    replacer = 'small'
                                    full_tag = '[MTMINFOCHUNK_SMALL]'
                                elif 'LARGE' in line:
                                    replacer = 'large'
                                    full_tag = '[MTMINFOCHUNK_LARGE]'
                                line = line.replace(full_tag, mtminfo.replace('replace',replacer))
                            line =line.replace('[AUDIO_CH01]',source.get('audio_ch_1'))
                            line =line.replace('[AUDIO_CH02]',source.get('audio_ch_2'))
                            line =line.replace('[AUDIO_CH03]',source.get('audio_ch_3'))
                            line =line.replace('[AUDIO_CH04]',source.get('audio_ch_4'))
                            line =line.replace('[AUDIO_CH05]',source.get('audio_ch_5'))
                            line =line.replace('[AUDIO_CH06]',source.get('audio_ch_6'))
                            line =line.replace('[AUDIO_CH07]',source.get('audio_ch_7'))
                            line =line.replace('[AUDIO_CH08]',source.get('audio_ch_8'))
                            line =line.replace('[AUDIO_CH09]',source.get('audio_ch_9'))
                            line =line.replace('[AUDIO_CH10]',source.get('audio_ch_10'))
                            line =line.replace('[AUDIO_CH11]',source.get('audio_ch_11'))
                            line =line.replace('[AUDIO_CH12]',source.get('audio_ch_12'))
                            line =line.replace('[CH01]',source.get('audio_ch_1'))
                            line =line.replace('[CH02]',source.get('audio_ch_2'))
                            line =line.replace('[CH03]',source.get('audio_ch_3'))
                            line =line.replace('[CH04]',source.get('audio_ch_4'))
                            line =line.replace('[CH05]',source.get('audio_ch_5'))
                            line =line.replace('[CH06]',source.get('audio_ch_6'))
                            line =line.replace('[CH07]',source.get('audio_ch_7'))
                            line =line.replace('[CH08]',source.get('audio_ch_8'))
                            line =line.replace('[CH09]',source.get('audio_ch_9'))
                            line =line.replace('[CH10]',source.get('audio_ch_10'))
                            line =line.replace('[CH11]',source.get('audio_ch_11'))
                            line =line.replace('[CH12]',source.get('audio_ch_12'))
                            line =line.replace('[STANDARD]',source.get('standard'))
                            line =line.replace('[CLIENT]',client_name)
                            line =line.replace('[FRAME_RATE]',source.get('frame_rate'))
                            line =line.replace('[SOURCE_TYPE]',source.get('source_type'))
                            line =line.replace('[TYPE]',source.get('source_type'))
                            line =line.replace('[GENERATION]',source.get('generation'))
                            line =line.replace('[DESCRIPTION]',source.get('description'))
                            line =line.replace('[TEXTLESS]',source.get('textless'))
                            line =line.replace('[PO_NUMBER]',source.get('po_number'))
                            line =line.replace('[CLIENT_ASSET_ID]',source.get('client_asset_id'))
                            line =line.replace('[FORMAT]',source.get('format'))
                            line =line.replace('[CAPTIONING]',captioning)
                            line =line.replace('[SUBTITLES]',subtitles)
                            line =line.replace('[ADDITIONAL_LABEL_INFO]',source.get('additional_label_info'))
                            line =line.replace('[DATE]',str(date))
                            result = '%s%s' % (result,line)
                f.close()
                new_bc_file = '/var/www/html/source_labels/printed_labels/%s_%s.html' % (barcode, guy)
                if os.path.exists(new_bc_file):
                    os.system('rm -rf %s' % new_bc_file)
                new_guy = open(new_bc_file, 'w') 
                new_guy.write(result)
                new_guy.close()
            t1 = table.add_cell('')
            t1.add_style('width: 100%s;' % '%')
            do_it = table.add_cell('<input type="button" value="Get Label Page For %s :(%s)"/>' % (source.get('title'), barcode)) 
            do_it.add_behavior(my.get_open_barcode_label_page(barcode))
            t2 = table.add_cell('')
            t2.add_style('width: 100%s;' % '%')
        else:
            table.add_cell('This Source does not have a barcode')
        return table

    def get_open_barcode_label_page(my, barcode):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                          var barcode = '%s';
                          var top_el = spt.api.get_parent(bvr.src_el, '.print_label_wdg');
                          var sels = top_el.getElementsByTagName('select');
                          var type_sel = '';
                          for(var r = 0; r < sels.length; r++){
                              if(sels[r].name == 'label_type'){
                                  type_sel = sels[r];
                              }
                          } 
                          var type = type_sel.value;
                          var url = 'http://tactic01/source_labels/printed_labels/' + barcode + '_' + type + '.html';
                          new_win = window.open(url,'_blank','toolbar=1,location=1,directories=1,status=1,menubar=1,scrollbars=0,resizable=0'); 
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                          //alert(err);
                }
         ''' % (barcode)
        }
        return behavior
    
