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
                          var sk = bvr.src_el.get('sk');
                          var barcode = bvr.src_el.get('barcode');
                          var title = bvr.src_el.get('title');
                          var episode = bvr.src_el.get('episode');
                          var textless = bvr.src_el.get('textless');
                          var total_run_time = bvr.src_el.get('total_run_time');
                          var part = bvr.src_el.get('part');
                          var client_name = bvr.src_el.get('client_name');
                          var audio_ch_1 = bvr.src_el.get('audio_ch_1');
                          var audio_ch_2 = bvr.src_el.get('audio_ch_2');
                          var audio_ch_3 = bvr.src_el.get('audio_ch_3');
                          var audio_ch_4 = bvr.src_el.get('audio_ch_4');
                          var audio_ch_5 = bvr.src_el.get('audio_ch_5');
                          var audio_ch_6 = bvr.src_el.get('audio_ch_6');
                          var audio_ch_7 = bvr.src_el.get('audio_ch_7');
                          var audio_ch_8 = bvr.src_el.get('audio_ch_8');
                          var audio_ch_9 = bvr.src_el.get('audio_ch_9');
                          var audio_ch_10 = bvr.src_el.get('audio_ch_10');
                          var audio_ch_11 = bvr.src_el.get('audio_ch_11');
                          var audio_ch_12 = bvr.src_el.get('audio_ch_12');
                          var standard = bvr.src_el.get('standard');
                          var description = bvr.src_el.get('description');
                          var frame_rate = bvr.src_el.get('frame_rate');
                          var version = bvr.src_el.get('version');
                          var generation = bvr.src_el.get('generation');
                          var source_type = bvr.src_el.get('source_type');
                          var aspect_ratio = bvr.src_el.get('aspect_ratio');
                          var color_space = bvr.src_el.get('color_space');
                          var po_number = bvr.src_el.get('po_number');
                          var client_asset_id = bvr.src_el.get('client_asset_id');
                          var format = bvr.src_el.get('format');
                          var captioning = bvr.src_el.get('captioning');
                          var subtitles = bvr.src_el.get('subtitles');
                          var additional_label_info = bvr.src_el.get('additional_label_info');
                          var code = sk.split('code=')[1];
                          var class_name = 'order_builder.LabelWdg';
                          kwargs = {
                                           'sk': sk,
                                           'code': code,
                                           'title': title,
                                           'episode': episode,
                                           'textless': textless,
                                           'trt': total_run_time,
                                           'part': part,
                                           'version': version,
                                           'client_name': client_name,
                                           'aspect_ratio': aspect_ratio,
                                           'color_space': color_space,
                                           'audio_ch_1': audio_ch_1,
                                           'audio_ch_2': audio_ch_2,
                                           'audio_ch_3': audio_ch_3,
                                           'audio_ch_4': audio_ch_4,
                                           'audio_ch_5': audio_ch_5,
                                           'audio_ch_6': audio_ch_6,
                                           'audio_ch_7': audio_ch_7,
                                           'audio_ch_8': audio_ch_8,
                                           'audio_ch_9': audio_ch_9,
                                           'audio_ch_10': audio_ch_10,
                                           'audio_ch_11': audio_ch_11,
                                           'audio_ch_12': audio_ch_12,
                                           'standard': standard,
                                           'generation': generation,
                                           'po_number': po_number,
                                           'client_asset_id': client_asset_id,
                                           'format': format,
                                           'captioning': captioning,
                                           'subtitles': subtitles,
                                           'source_type': source_type,
                                           'frame_rate': frame_rate,
                                           'description': description,
                                           'additional_label_info': additional_label_info,
                                           'barcode': barcode
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
        barcode = sobject.get_value('barcode')
        total_run_time = sobject.get_value('total_run_time')
        version = sobject.get_value('version')
        part = sobject.get_value('part')
        title = sobject.get_value('title')
        episode = sobject.get_value('episode')
        textless = sobject.get_value('textless')
        aspect_ratio = sobject.get_value('aspect_ratio')
        color_space = sobject.get_value('color_space')
        audio_ch_1 = sobject.get_value('audio_ch_1')
        audio_ch_2 = sobject.get_value('audio_ch_2')
        audio_ch_3 = sobject.get_value('audio_ch_3')
        audio_ch_4 = sobject.get_value('audio_ch_4')
        audio_ch_5 = sobject.get_value('audio_ch_5')
        audio_ch_6 = sobject.get_value('audio_ch_6')
        audio_ch_7 = sobject.get_value('audio_ch_7')
        audio_ch_8 = sobject.get_value('audio_ch_8')
        audio_ch_9 = sobject.get_value('audio_ch_9')
        audio_ch_10 = sobject.get_value('audio_ch_10')
        audio_ch_11 = sobject.get_value('audio_ch_11')
        audio_ch_12 = sobject.get_value('audio_ch_12')
        description = sobject.get_value('description')
        client_code = sobject.get_value('client_code')
        additional_label_info = sobject.get_value('additional_label_info')
        po_number = sobject.get_value('po_number')#
        client_asset_id = sobject.get_value('client_asset_id')#
        format = sobject.get_value('format')#
        captioning = sobject.get_value('captioning')#
        subtitles = sobject.get_value('subtitles')#
        client_name = 'No Client Name'
        if client_code not in [None,'']:
            client_names = my.server.eval("@GET(twog/client['code','%s'].name)" % client_code)
            if len(client_names) > 0:
                client_name = client_names[0]
        
        standard = sobject.get_value('standard')
        frame_rate = sobject.get_value('frame_rate')
        generation = sobject.get_value('generation')
        source_type = sobject.get_value('source_type')
        widget = DivWdg()
        table = Table()
        table.add_attr('width', '50px')
        table.add_row()
        cell1 = table.add_cell('<img border="0" style="vertical-align: middle" title="" src="/context/icons/silk/printer.png">')
        launch_behavior = my.get_launch_behavior()
        cell1.add_attr('total_run_time',total_run_time)
        cell1.add_attr('description',description)
        cell1.add_attr('barcode',barcode)
        cell1.add_attr('title',title)
        cell1.add_attr('episode',episode)
        cell1.add_attr('textless',textless)
        cell1.add_attr('version',version)
        cell1.add_attr('part',part)
        cell1.add_attr('aspect_ratio',aspect_ratio)
        cell1.add_attr('color_space',color_space)
        cell1.add_attr('sk',my.server.build_search_key('twog/source', code))
        cell1.add_attr('client_name',client_name)
        cell1.add_attr('audio_ch_1',audio_ch_1)
        cell1.add_attr('audio_ch_2',audio_ch_2)
        cell1.add_attr('audio_ch_3',audio_ch_3)
        cell1.add_attr('audio_ch_4',audio_ch_4)
        cell1.add_attr('audio_ch_5',audio_ch_5)
        cell1.add_attr('audio_ch_6',audio_ch_6)
        cell1.add_attr('audio_ch_7',audio_ch_7)
        cell1.add_attr('audio_ch_8',audio_ch_8)
        cell1.add_attr('audio_ch_9',audio_ch_9)
        cell1.add_attr('audio_ch_10',audio_ch_10)
        cell1.add_attr('audio_ch_11',audio_ch_11)
        cell1.add_attr('audio_ch_12',audio_ch_12)
        cell1.add_attr('standard',standard)
        cell1.add_attr('frame_rate',frame_rate)
        cell1.add_attr('generation',generation)
        cell1.add_attr('source_type',source_type)
        cell1.add_attr('po_number',po_number)
        cell1.add_attr('client_asset_id',client_asset_id)
        cell1.add_attr('format',format)
        cell1.add_attr('captioning',captioning)
        cell1.add_attr('subtitles',subtitles)
        cell1.add_attr('additional_label_info',additional_label_info)
        cell1.add_style('cursor: pointer;')
        cell1.add_behavior(launch_behavior)
        widget.add(table)

        return widget

class LabelWdg(BaseRefreshWdg):

    def init(my):
        from client.tactic_client_lib import TacticServerStub
        from pyasm.common import Environment
        my.server = TacticServerStub.get()
        my.sk = ''
        my.code = ''
        my.barcode = ''
        my.title = ''
        my.episode = ''
        my.textless = ''
        my.trt = ''
        my.version = ''
        my.client_name = ''
        my.audio_ch_1 = ''
        my.audio_ch_2 = ''
        my.audio_ch_3 = ''
        my.audio_ch_4 = ''
        my.audio_ch_5 = ''
        my.audio_ch_6 = ''
        my.audio_ch_7 = ''
        my.audio_ch_8 = ''
        my.audio_ch_9 = ''
        my.audio_ch_10 = ''
        my.audio_ch_11 = ''
        my.audio_ch_12 = ''
        my.standard = ''
        my.frame_rate = ''
        my.generation = ''
        my.source_type = ''
        my.aspect_ratio = ''
        my.color_space = ''
        my.description = ''
        my.po_number = ''
        my.client_asset_id = ''
        my.format = ''
        my.captioning = ''
        my.subtitles = ''
        my.part = ''
        my.types = ['HDCAM','HDCAM_TV_FOX','HDCAM_FILM_FOX','HDCAM DIGIBETA','DVD','D5']
        my.template_files = {'HDCAM': '/var/www/html/source_labels/HDCAM_label.html', 'HDCAM_FILM_FOX': '/var/www/html/source_labels/HDCAM_FILM_FOX_label.html', 'HDCAM_TV_FOX': '/var/www/html/source_labels/HDCAM_TV_FOX_label.html', 'HDCAM DIGIBETA': '/var/www/html/source_labels/HDCAM_Digibeta_label.html', 'DVD': '/var/www/html/source_labels/DVD_Label.html', 'D5': '/var/www/html/source_labels/D5_label.html'}
    
    def get_display(my):   
        my.sk = str(my.kwargs.get('sk'))
        my.code = str(my.kwargs.get('code'))
        my.title = str(my.kwargs.get('title'))
        my.episode = str(my.kwargs.get('episode'))
        my.barcode = str(my.kwargs.get('barcode'))
        my.trt = str(my.kwargs.get('trt'))
        my.version = str(my.kwargs.get('version'))
        my.part = str(my.kwargs.get('part'))
        my.textless = str(my.kwargs.get('textless'))
        my.client_name = str(my.kwargs.get('client_name'))
        my.audio_ch_1 = str(my.kwargs.get('audio_ch_1'))
        my.audio_ch_2 = str(my.kwargs.get('audio_ch_2'))
        my.audio_ch_3 = str(my.kwargs.get('audio_ch_3'))
        my.audio_ch_4 = str(my.kwargs.get('audio_ch_4'))
        my.audio_ch_5 = str(my.kwargs.get('audio_ch_5'))
        my.audio_ch_6 = str(my.kwargs.get('audio_ch_6'))
        my.audio_ch_7 = str(my.kwargs.get('audio_ch_7'))
        my.audio_ch_8 = str(my.kwargs.get('audio_ch_8'))
        my.audio_ch_9 = str(my.kwargs.get('audio_ch_9'))
        my.audio_ch_10 = str(my.kwargs.get('audio_ch_10'))
        my.audio_ch_11 = str(my.kwargs.get('audio_ch_11'))
        my.audio_ch_12 = str(my.kwargs.get('audio_ch_12'))
        my.standard = str(my.kwargs.get('standard'))
        my.aspect_ratio = str(my.kwargs.get('aspect_ratio'))
        my.color_space = str(my.kwargs.get('color_space'))
        my.frame_rate = str(my.kwargs.get('frame_rate'))
        my.generation = str(my.kwargs.get('generation'))
        my.po_number = str(my.kwargs.get('po_number'))
        my.client_asset_id = str(my.kwargs.get('client_asset_id'))
        my.format = str(my.kwargs.get('format'))
        my.captioning = str(my.kwargs.get('captioning'))
        my.subtitles = str(my.kwargs.get('subtitles'))
        my.description = str(my.kwargs.get('description'))
        my.additional_label_info = str(my.kwargs.get('additional_label_info'))
        if my.captioning in ['',None]:
            my.captioning = 'N/A'
        if my.subtitles in ['',None]:
            my.subtitles = 'N/A' 
        my.source_type = str(my.kwargs.get('source_type'))
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
        if my.barcode not in [None,'']:
            for guy in my.types:
                result = ''
                f = open(my.template_files[guy], 'r')
                for line in f:
        	        if not line.strip():
        		    continue
        	        else:
        		    line = line.rstrip('\r\n')
                            line =line.replace('[TITLE]',my.title)
                            line =line.replace('[EPISODE]',my.episode)
                            line =line.replace('[BARCODE]',my.barcode)
                            line =line.replace('[TOTAL_RUN_TIME]',my.trt)
                            line =line.replace('[TRT]',my.trt)
                            line =line.replace('[VERSION]',my.version)
                            line =line.replace('[ASPECT_RATIO]',my.aspect_ratio)
                            line =line.replace('[COLOR_SPACE]',my.color_space)
                            line =line.replace('[STRAT2G_PART]',my.part)
                            line =line.replace('[AUDIO_CH01]',my.audio_ch_1)
                            line =line.replace('[AUDIO_CH02]',my.audio_ch_2)
                            line =line.replace('[AUDIO_CH03]',my.audio_ch_3)
                            line =line.replace('[AUDIO_CH04]',my.audio_ch_4)
                            line =line.replace('[AUDIO_CH05]',my.audio_ch_5)
                            line =line.replace('[AUDIO_CH06]',my.audio_ch_6)
                            line =line.replace('[AUDIO_CH07]',my.audio_ch_7)
                            line =line.replace('[AUDIO_CH08]',my.audio_ch_8)
                            line =line.replace('[AUDIO_CH09]',my.audio_ch_9)
                            line =line.replace('[AUDIO_CH10]',my.audio_ch_10)
                            line =line.replace('[AUDIO_CH11]',my.audio_ch_11)
                            line =line.replace('[AUDIO_CH12]',my.audio_ch_12)
                            line =line.replace('[CH01]',my.audio_ch_1)
                            line =line.replace('[CH02]',my.audio_ch_2)
                            line =line.replace('[CH03]',my.audio_ch_3)
                            line =line.replace('[CH04]',my.audio_ch_4)
                            line =line.replace('[CH05]',my.audio_ch_5)
                            line =line.replace('[CH06]',my.audio_ch_6)
                            line =line.replace('[CH07]',my.audio_ch_7)
                            line =line.replace('[CH08]',my.audio_ch_8)
                            line =line.replace('[CH09]',my.audio_ch_9)
                            line =line.replace('[CH10]',my.audio_ch_10)
                            line =line.replace('[CH11]',my.audio_ch_11)
                            line =line.replace('[CH12]',my.audio_ch_12)
                            line =line.replace('[STANDARD]',my.standard)
                            line =line.replace('[CLIENT]',my.client_name)
                            line =line.replace('[FRAME_RATE]',my.frame_rate)
                            line =line.replace('[SOURCE_TYPE]',my.source_type)
                            line =line.replace('[TYPE]',my.source_type)
                            line =line.replace('[GENERATION]',my.generation)
                            line =line.replace('[DESCRIPTION]',my.description)
                            line =line.replace('[TEXTLESS]',my.textless)
                            line =line.replace('[PO_NUMBER]',my.po_number)
                            line =line.replace('[CLIENT_ASSET_ID]',my.client_asset_id)
                            line =line.replace('[FORMAT]',my.format)
                            line =line.replace('[CAPTIONING]',my.captioning)
                            line =line.replace('[SUBTITLES]',my.subtitles)
                            line =line.replace('[ADDITIONAL_LABEL_INFO]',my.additional_label_info)
                            line =line.replace('[DATE]',str(date))
                            result = '%s%s' % (result,line)
                f.close()
                new_bc_file = '/var/www/html/source_labels/printed_labels/%s_%s.html' % (my.barcode, guy)
                if os.path.exists(new_bc_file):
                    os.system('rm -rf %s' % new_bc_file)
                new_guy = open(new_bc_file, 'w') 
                new_guy.write(result)
                new_guy.close()
            t1 = table.add_cell('')
            t1.add_style('width: 100%s;' % '%')
            do_it = table.add_cell('<input type="button" value="Get Label Page For %s :(%s)"/>' % (my.title, my.barcode)) 
            do_it.add_behavior(my.get_open_barcode_label_page())
            t2 = table.add_cell('')
            t2.add_style('width: 100%s;' % '%')
        else:
            table.add_cell('This Source does not have a barcode')
        return table

    def get_open_barcode_label_page(my):
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
         ''' % (my.barcode)
        }
        return behavior
    

























































