__all__ = ["CDeliverableLauncherWdg","CDeliverableEditWdg","CDeliverableXMLGeneratorWdg"]
import tacticenv
import os, datetime
from pyasm.common import Environment
from pyasm.biz import *
from pyasm.web import Table, DivWdg
from pyasm.widget import SelectWdg, IconWdg, TextWdg, CheckboxWdg
from tactic.ui.common import BaseTableElementWdg
from tactic.ui.common import BaseRefreshWdg
class CDeliverableLauncherWdg(BaseTableElementWdg):

    def init(my):
        nothing = 'true'
        my.server = None

    def get_launch_behavior(my, order_code, title_code1):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                          var code = '%s';
                          var title_code = '%s';
                          var class_name = 'client_deliverable.client_deliverable.CDeliverableEditWdg';
                          kwargs = {};
                          if(code != '' && code != null){
                              kwargs['code'] = code;
                          }
                          if(title_code != '' && title_code != null){
                              kwargs['title_code'] = title_code;
                          }
                          spt.panel.load_popup('Client Deliverable ' + code, class_name, kwargs);
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         ''' % (order_code, title_code1)}
        return behavior


    def get_display(my):
        code = ''
        order_name = ''
        sob_sk = ''
        title_code = ''
        if 'title_code' in my.kwargs.keys():
            title_code = my.kwargs.get('title_code')
        elif 'code' in my.kwargs.keys():
            code = str(my.kwargs.get('code'))
        else: 
            sobject = my.get_current_sobject()
            code = sobject.get_code()
        widget = DivWdg()
        table = Table()
        table.add_attr('width', '50px')
        table.add_row()
        cell1 = table.add_cell('<img border="0" style="vertical-align: middle" title="" src="/context/icons/silk/door_in.png">')
        launch_behavior = my.get_launch_behavior(code, title_code)
        cell1.add_style('cursor: pointer;')
        cell1.add_behavior(launch_behavior)
        widget.add(table)
        return widget

class CDeliverableEditWdg(BaseTableElementWdg):

    def init(my):
        from tactic_client_lib import TacticServerStub
        login = Environment.get_login()
        login_name = login.get_login()
        my.code = my.kwargs.get('code')
        my.title_code = my.kwargs.get('title_code')
        my.is_insert = False
        my.client_code = None
        my.server = TacticServerStub.get()
        my.title = None
        my.client = None
        found_existing = False
        if my.title_code not in [None,'']:
            my.sob = my.server.eval("@SOBJECT(twog/client_deliverable['title_code','%s'])" % my.title_code)
            if my.sob:
                my.sob = my.sob[0]
                found_existing = True
        if not found_existing:
            my.sob = {'code': '', 'clip_id': '', 'login': login_name, 'record_id': '', 'title_id': '', 'title_type': '', 'title_name': '', 'trailer_version': '', 'trailer_type': '', 'trailer_number': '', 'title_comment': '', 'narrative': '', 'trailer_rev_number': '', 'source': '', 'aspect_ratio': '', 'audio_config': '', 'standard': '', 'run_time_calc': '', 'texted_textless': '', 'master_audio_config': '', 'client_barcode': '', 'hd': '', 'legal_right': '', 'legal_date': '', 'mpaa': '', 'legal_comment': '', 'url': '', 'he_creative_comment': '', 'mpaa_ratings': '', 'uk_ratings': '', 'australia_ratings': '', 'germany_ratings': '', 'genre': '', 'original_language': '', 'cast_info': '', 'alpha_id': '', 'release_number': '', 'language_audio': '', 'language_subtitled': '', 'language_text': '', 'platform': '', 'order_code': '', 'title_code': '', 'ancestors': '', 'original_source_code': '', 'original_source_barcode': '', 'po_number': '', 'destination': '', 'client_code': '', 'destination_client_code': '', 'client_name': ''}
            if my.title_code not in [None,'']:
                my.is_insert = True
                my.title = my.server.eval("@SOBJECT(twog/title['code','%s'])" % my.title_code)[0]
                my.client = my.server.eval("@SOBJECT(twog/client['code','%s'])" % my.title.get('client_code'))[0]
                my.sob['client_code'] = '5'
                my.sob['client_code'] = my.client.get('code')
                my.sob['client_name'] = my.client.get('name')
                my.sob['title_code'] = my.title.get('code')
                my.sob['order_code'] = my.title.get('order_code')
                my.sob['po_number'] = my.title.get('po_number')
                my.sob['title_name'] = my.title.get('title')
                if my.title.get('episode') not in [None,'']:
                    my.sob['title_name'] = '%s: %s' % (my.sob.get('title_name'), my.title.get('episode'))
                my.sob['platform'] = my.title.get('platform')
                origin_source = my.server.eval("@SOBJECT(twog/title_origin['title_code','%s'])" % my.title.get('code'))
                og_codes = ''
                og_barcodes = ''
                for orig in origin_source: 
                    og = my.server.eval("@SOBJECT(twog/source['code','%s'])" % orig.get('source_code'))
                    if og:
                        og = og[0]
                        if og_codes == '':
                            og_codes = og.get('code')
                        else:
                            og_codes = '%s,%s' % (og_codes, og.get('code'))
                        if og_barcodes == '':
                            og_barcodes = og.get('barcode')
                        else:
                            og_barcodes = '%s,%s' % (og_barcodes, og.get('barcode'))
                my.sob['original_source_code'] = og_codes
                my.sob['original_source_barcode'] = og_barcodes
            else:
                my.sob = my.server.eval("@SOBJECT(twog/client_deliverable['code','%s'])" % my.code)[0]
        my.all_clients = my.server.eval("@SOBJECT(twog/client['@ORDER_BY','name asc'])") 
        my.title_types = ['Feature','Option 2','Option 3']
        my.trailer_types = ['Clip','Trailer','Teaser','TV Spot','Promo']
        my.trailer_versions = ['Domestic','International']
        my.trailer_numbers = ['A','B','C','D','E','1','2','3','4','5','6']
        my.text_languages = ['Not Texted','Afghans/Pushto','Afrikaans','Albanian','Arabic','Bangla/Bengali','Bulgarian','Catalan','Chinese (Simplified)','Chinese (Traditional)','Croatian','Czech','Danish','Dutch (Flemish)','Dutch (Netherlands)','English (UK)','English (US)','Estonian','Finnish','French (Canadian)','French (Parisan)','Gaelic (Irish)','Gaelic (Scots)','German','Greek','Hebrew','Hindi','Hungarian','Icelandic','Indonesian','Italian','Japanese','Korean','Lao','Latvian','Lithuanian','Macedonian','Malay','Mayayalam','Mongolian','Norwegian','Persian/Farsi','Polish','Portuguese (Brazil)','Portuguese (Portugual)','Punjabi','Romainian','Russian','Serbian','Serbo-Croatian','Sindhi','Sinhalese','Slovak','Slovene','Spanish (Castilian)','Spanish (Latin Am)','Spanish (Mexican)','Swedish','Tagalog','Tamil','Telugu','Thai','Turkish','Ukrainian','Urdu','Vietnamese']
        my.subtitle_languages = ['None','Afghans/Pushto','Afrikaans','Albanian','Arabic','Bangla/Bengali','Bulgarian','Catalan','Chinese (Simplified)','Chinese (Traditional)','Croatian','Czech','Danish','Dutch (Flemish)','Dutch (Netherlands)','English','Estonian','Finnish','French (Canadian)','French (Parisan)','Gaelic (Irish)','Gaelic (Scots)','German','Greek','Hebrew','Hindi','Hungarian','Icelandic','Indonesian','Italian','Japanese','Korean','Lao','Latvian','Lithuanian','Macedonian','Malay','Mayayalam','Mongolian','Norwegian','Persian/Farsi','Polish','Portuguese (Brazil)','Portuguese (Portugual)','Punjabi','Romainian','Russian','Serbian','Serbo-Croatian','Sindhi','Sinhalese','Slovak','Slovene','Spanish (Castilian)','Spanish (Latin Am)','Spanish (Mexican)','Swedish','Tagalog','Tamil','Telugu','Thai','Turkish','Ukrainian','Urdu','Vietnamese']
        my.audio_languages = ['Afghans/Pushto','Afrikaans','Albanian','Arabic','Bangla','Bangla/Bengali','Bosnian','Bulgarian','Catalan','Chinese (Cantonese)','Chinese (Mandarin - PRC)','Chinese (Mandarin - Taiwan)','Chinese (Taiwanese)','Corsican','Croatian','Czech','Danish','Dutch (Flemish)','Dutch (Netherlands)','English','Estonian','Finnish','French (Canadian)','French (Parisan)','Gaelic (Irish)','Gaelic (Scots)','German','German (Swiss)','Greek','Hebrew','Hindi','Hungarian','Icelandic','Indonesian','Italian','Japanese','Korean','Lao','Latvian','Lithuanian','Macedonian','Malay','Malayalam','Nepali','No Dialogue','Northern Sotho','Norwegian','Persian/Farsi','Polish','Portuguese (Brazil)','Portuguese (Portugual)','Punjabi','Romainian','Russian','Serbian','Serbo-Croatian','Sindhi','Sinhalese','Slovak','Slovene','Sotho','Spanish (Castilian)','Spanish (Latin Am)','Spanish (Mexican)','Swedish','Tagalog','Tamil','Telugu','Thai','Turkish','Ukrainian','Urdu','Vietnamese']
        my.original_languages = ['Afghans/Pushto','Afrikaans','Albanian','Arabic','Bangla','Bangla/Bengali','Bosnian','Bulgarian','Catalan','Chinese (Cantonese)','Chinese (Mandarin - PRC)','Chinese (Mandarin - Taiwan)','Chinese (Taiwanese)','Corsican','Croatian','Czech','Danish','Dutch (Flemish)','Dutch (Netherlands)','English','Estonian','Finnish','French (Canadian)','French (Parisan)','Gaelic (Irish)','Gaelic (Scots)','German','German (Swiss)','Greek','Hebrew','Hindi','Hungarian','Icelandic','Indonesian','Italian','Japanese','Korean','Lao','Latvian','Lithuanian','Macedonian','Malay','Malayalam','Nepali','No Dialogue','Northern Sotho','Norwegian','Persian/Farsi','Polish','Portuguese (Brazil)','Portuguese (Portugual)','Punjabi','Romainian','Russian','Serbian','Serbo-Croatian','Sindhi','Sinhalese','Slovak','Slovene','Sotho','Spanish (Castilian)','Spanish (Latin Am)','Spanish (Mexican)','Swedish','Tagalog','Tamil','Telugu','Thai','Turkish','Ukrainian','Urdu','Vietnamese']
        my.sources = ['Theatrical (New)','Theatrical','HE','SPC','SPT','SPTI','MGM']
        my.narratives = ['Available For Digital Download','Clean','Clip','Coming Soon','Coming Soon To DVD/BD','Now Available On VOD','Now On Blu-Ray','Now On DVD','Now On DVD/BD','On Blu-Ray','On DVD','On DVD/BD','ON DVD/PSP','On DVD/PSP/Blu-Ray','On PSP','On PSP/Blu-Ray','Theatrical','Theatrical With Reference','Theatrical Without Reference','With BD Logo']
        my.aspect_ratios = ['16x9 FF','16x9 FF 1.78','16x9 LB','16x9 LB 2.35','16x9 LB 2.40','16x9 M 1.85','16x9 M 2.10','16x9 SM 1.33','16x9 SM 1.66','4x3 FF','4x3 FF 1.33','4x3 LB','4x3 LB 2.35','4x3 LB 2.40','4x3 LB 2.55','4x3 M 1.66','4x3 M 1.85','4x3 M 2.10']
        my.standards = ['HD','PAL','NTSC']
        my.mpaa_ratings = ['G-All','G-R','G-PG13','G-NC17','R-R','R-NC17','Blank']
        my.uk_ratings = ['Bland Food 5*s','G-All','G-R','G-PG13','G-NC17','R-R','R-NC17','Blank']
        my.australia_ratings = ['Thats not a knife','G-All','G-R','G-PG13','G-NC17','R-R','R-NC17','Blank']
        my.germany_ratings = ['Sprockets','G-All','G-R','G-PG13','G-NC17','R-R','R-NC17','Blank']
        my.audio_configs = ['5.1 & Comp','5.1','2','2.0 Split','Mono','Mono Split','N/A']
        my.legal_rights = ['All Media','Pending','Not Cleared']
        my.texted_textless = ['Texted','Textless']
        my.hd = ['Yes','No']
        my.mpaa = ['With MPAA','Without MPAA']

    def get_submit(my, sk):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                             var sk = '%s';
                             top_el = spt.api.get_parent(bvr.src_el, '.client_deliverable_wdg');
                             inputs = top_el.getElementsByClassName('spt_input');
                             dict = {};
                             for(var r = 0; r < inputs.length; r++){
                                 field = inputs[r].getAttribute('id');
                                 if(field == '' || field == null){
                                     field = inputs[r].getAttribute('name');
                                 }
                                 value = inputs[r].value;
                                 dict[field] = value;
                             }
                             server = TacticServerStub.get();
                             code = '';
                             if(sk == ''){
                                 //Then it is an insert
                                 new_guy = server.insert('twog/client_deliverable', dict);
                                 sk = new_guy.__search_key__;
                                 code = new_guy.code;
                             }else{
                                 //Then it is an edit
                                 server.update(sk, dict);
                                 code = sk.split('code=')[1];
                             }
                             spt.api.load_panel(top_el, 'client_deliverable.client_deliverable.CDeliverableEditWdg', {'code': code}); 
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         ''' % sk}
        return behavior

    def get_xml(my, sk):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                             var sk = '%s';
                             code = sk.split('code=')[1];
                             spt.panel.load_popup('XML', 'client_deliverable.client_deliverable.CDeliverableXMLGeneratorWdg', {'code': code, 'client': 'sony'});
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         ''' % sk}
        return behavior

    def fix_date(my, date):
        #This is needed due to the way Tactic deals with dates (using timezone info), post v4.0
        from pyasm.common import SPTDate
        return_date = ''
        date_obj = SPTDate.convert_to_local(date)
        if date_obj not in [None,'']:
            return_date = date_obj.strftime("%Y-%m-%d  %H:%M")
        return return_date

    def get_display(my):
        widget = DivWdg()
        table = Table()
        table.add_attr('class','client_deliverable_wdg')
        table.add_row()
        table2 = Table()
        table2.add_style('border-spacing: 5px;')
        table2.add_style('border-collapse: separate;')
        table2.add_row()

        c1 = table2.add_cell('Order Code:')
        c1.add_attr('nowrap','nowrap')
        tb1 = TextWdg('order_code')
        tb1.add_attr('id','order_code')
        tb1.add_attr('disabled','disabled')
        tb1.set_value(my.sob['order_code'])
        table2.add_cell(tb1)

        c1 = table2.add_cell('PO Number:')
        c1.add_attr('nowrap','nowrap')
        tb1 = TextWdg('po_number')
        tb1.add_attr('id','po_number')
        tb1.add_attr('disabled','disabled')
        tb1.set_value(my.sob['po_number'])
        table2.add_cell(tb1)

        c1 = table2.add_cell('Title Code:')
        c1.add_attr('nowrap','nowrap')
        tb1 = TextWdg('title_code')
        tb1.add_attr('id','title_code')
        tb1.add_attr('disabled','disabled')
        tb1.set_value(my.sob['title_code'])
        table2.add_cell(tb1)

        c1 = table2.add_cell('Platform:')
        c1.add_attr('nowrap','nowrap')
        tb1 = TextWdg('platform')
        tb1.add_attr('id','platform')
        tb1.add_attr('disabled','disabled')
        tb1.set_value(my.sob['platform'])
        table2.add_cell(tb1)

        c1 = table2.add_cell('Client:')
        c1.add_attr('nowrap','nowrap')
        tb1 = TextWdg('client_name')
        tb1.add_attr('id','client_name')
        tb1.add_attr('disabled','disabled')
        tb1.set_value(my.sob['client_name'])
        table2.add_cell(tb1)

        table2.add_row()
        table2.add_cell(table2.hr())
        table2.add_row()

        c1 = table2.add_cell('Title Source(s):')
        c1.add_attr('nowrap','nowrap')
        tb1 = TextWdg('original_source_code')
        tb1.add_attr('id','original_source_code')
        tb1.add_attr('disabled','disabled')
        tb1.add_style('width','200px')
        tb1.set_value(my.sob['original_source_code'])
        c2 = table2.add_cell(tb1)
        c2.add_attr('colspan','2')

        c1 = table2.add_cell('Title Source Barcodes(s):')
        c1.add_attr('nowrap','nowrap')
        tb1 = TextWdg('original_source_barcode')
        tb1.add_attr('id','original_source_barcode')
        tb1.add_attr('disabled','disabled')
        tb1.add_style('width','200px')
        tb1.set_value(my.sob['original_source_barcode'])
        c2 = table2.add_cell(tb1)
        c2.add_attr('colspan','2')

        c1 = table2.add_cell('Ancestors:')
        c1.add_attr('nowrap','nowrap')
        tb1 = TextWdg('ancestors')
        tb1.add_attr('id','ancestors')
        tb1.add_attr('disabled','disabled')
        tb1.add_style('width','300px')
        tb1.set_value(my.sob['ancestors'])
        c2 = table2.add_cell(tb1)
        c2.add_attr('colspan','3')

        table2.add_row()
        table2.add_cell(table2.hr())
        table2.add_row()

        c1 = table2.add_cell('Destination:')
        c1.add_attr('nowrap','nowrap')
        destination_sel = SelectWdg('destination')
        destination_sel.add_attr('id','destination')
        destination_sel.append_option('--Select--','')
        for c in my.all_clients:
            destination_sel.append_option(c.get('name'),c.get('name'))
        if my.sob.get('destination') == None:
            my.sob['destination'] = ''
        destination_sel.set_value(my.sob.get('destination'))
        table2.add_cell(destination_sel)


        if my.sob.get('record_id') in [None,'']:
            next_id_sob = my.server.eval("@SOBJECT(twog/global_resource['name','sony_next_unique_id'])")[0]
            next_id = int(next_id_sob.get('description'))
            my.sob['record_id'] = next_id
            my.server.update(next_id_sob.get('__search_key__'), {'description': next_id + 1}, triggers=False)
        c1 = table2.add_cell('Record ID:')
        c1.add_attr('nowrap','nowrap')
        tb1 = TextWdg('record_id')
        tb1.add_attr('id','record_id')
        tb1.set_value(my.sob['record_id'])
        table2.add_cell(tb1)

        c1 = table2.add_cell('Alpha ID:')
        c1.add_attr('nowrap','nowrap')
        tb1 = TextWdg('alpha_id')
        tb1.add_attr('id','alpha_id')
        tb1.set_value(my.sob['alpha_id'])
        table2.add_cell(tb1)

        c1 = table2.add_cell('Client Barcode:')
        c1.add_attr('nowrap','nowrap')
        tb1 = TextWdg('client_barcode')
        tb1.add_attr('id','client_barcode')
        tb1.set_value(my.sob['client_barcode'])
        table2.add_cell(tb1)

        c1 = table2.add_cell('Release Number:')
        c1.add_attr('nowrap','nowrap')
        tb1 = TextWdg('release_number')
        tb1.add_attr('id','release_number')
        tb1.set_value(my.sob['release_number'])
        table2.add_cell(tb1)

        table2.add_row()

        c1 = table2.add_cell('Title ID:')
        c1.add_attr('nowrap','nowrap')
        tb1 = TextWdg('title_id')
        tb1.add_attr('id','title_id')
        tb1.set_value(my.sob['title_id'])
        table2.add_cell(tb1)

        c1 = table2.add_cell('Title Name:')
        c1.add_attr('nowrap','nowrap')
        tb1 = TextWdg('title_name')
        tb1.add_attr('id','title_name')
        tb1.set_value(my.sob['title_name'])
        table2.add_cell(tb1)

        c1 = table2.add_cell('Title Type:')
        c1.add_attr('nowrap','nowrap')
        title_type_sel = SelectWdg('title_type')
        title_type_sel.add_attr('id','title_type')
        title_type_sel.append_option('--Select--','')
        for type in my.title_types:
            title_type_sel.append_option(type,type)
        if my.sob.get('title_type') == None:
            my.sob['title_type'] = ''
        title_type_sel.set_value(my.sob.get('title_type'))
        table2.add_cell(title_type_sel)

        c1 = table2.add_cell('Title Comment:')
        c1.add_attr('nowrap','nowrap')
        tb1 = TextWdg('title_comment')
        tb1.add_attr('id','title_comment')
        tb1.add_style('width','300px')
        tb1.set_value(my.sob['title_comment'])
        c2 = table2.add_cell(tb1)
        c2.add_attr('colspan','3')

        table2.add_row()

        c1 = table2.add_cell('Clip Id:')
        c1.add_attr('nowrap','nowrap')
        tb1 = TextWdg('clip_id')
        tb1.add_attr('id','clip_id')
        tb1.set_value(my.sob['clip_id'])
        table2.add_cell(tb1)

        table2.add_row()
        table2.add_cell(table2.hr())
        table2.add_row()

        c1 = table2.add_cell('Trailer Number:')
        c1.add_attr('nowrap','nowrap')
        trailer_number_sel = SelectWdg('trailer_number')
        trailer_number_sel.add_attr('id','trailer_number')
        trailer_number_sel.append_option('--Select--','')
        for number in my.trailer_numbers:
            trailer_number_sel.append_option(number,number)
        if my.sob.get('trailer_number') == None:
            my.sob['trailer_number'] = ''
        trailer_number_sel.set_value(my.sob.get('trailer_number'))
        table2.add_cell(trailer_number_sel)

        c1 = table2.add_cell('Trailer Rev Number:')
        c1.add_attr('nowrap','nowrap')
        tb1 = TextWdg('trailer_rev_number')
        tb1.add_attr('id','trailer_rev_number')
        tb1.set_value(my.sob['trailer_rev_number'])
        table2.add_cell(tb1)

        c1 = table2.add_cell('Trailer Type:')
        c1.add_attr('nowrap','nowrap')
        trailer_type_sel = SelectWdg('trailer_type')
        trailer_type_sel.add_attr('id','trailer_type')
        trailer_type_sel.append_option('--Select--','')
        for type in my.trailer_types:
            trailer_type_sel.append_option(type,type)
        if my.sob.get('trailer_type') == None:
            my.sob['trailer_type'] = ''
        trailer_type_sel.set_value(my.sob.get('trailer_type'))
        table2.add_cell(trailer_type_sel)

        c1 = table2.add_cell('Trailer Version:')
        c1.add_attr('nowrap','nowrap')
        trailer_version_sel = SelectWdg('trailer_version')
        trailer_version_sel.add_attr('id','trailer_version')
        trailer_version_sel.append_option('--Select--','')
        for version in my.trailer_versions:
            trailer_version_sel.append_option(version,version)
        if my.sob.get('trailer_version') == None:
            my.sob['trailer_version'] = ''
        trailer_version_sel.set_value(my.sob.get('trailer_version'))
        table2.add_cell(trailer_version_sel)

        table2.add_row()
        table2.add_cell(table2.hr())
        table2.add_row()

        c1 = table2.add_cell('Language Audio:')
        c1.add_attr('nowrap','nowrap')
        language_audio_sel = SelectWdg('language_audio')
        language_audio_sel.append_option('--Select--','')
        for language in my.audio_languages:
            language_audio_sel.append_option(language,language)
        if my.sob.get('language_audio') == None:
            my.sob['language_audio'] = ''
        language_audio_sel.set_value(my.sob.get('language_audio'))
        table2.add_cell(language_audio_sel)

        c1 = table2.add_cell('Language Subtitled:')
        c1.add_attr('nowrap','nowrap')
        language_subtitled_sel = SelectWdg('language_subtitled')
        language_subtitled_sel.add_attr('id','language_subtitled')
        language_subtitled_sel.append_option('--Select--','')
        for language in my.subtitle_languages:
            language_subtitled_sel.append_option(language,language)
        if my.sob.get('language_subtitled') == None:
            my.sob['language_subtitled'] = ''
        language_subtitled_sel.set_value(my.sob.get('language_subtitled'))
        table2.add_cell(language_subtitled_sel)

        c1 = table2.add_cell('Language Text:')
        c1.add_attr('nowrap','nowrap')
        language_text_sel = SelectWdg('language_text')
        language_text_sel.add_attr('id','language_text')
        language_text_sel.append_option('--Select--','')
        for language in my.text_languages:
            language_text_sel.append_option(language,language)
        if my.sob.get('language_text') == None:
            my.sob['language_text'] = ''
        language_text_sel.set_value(my.sob.get('language_text'))
        table2.add_cell(language_text_sel)

        c1 = table2.add_cell('Original Language:')
        c1.add_attr('nowrap','nowrap')
        original_language_sel = SelectWdg('original_language')
        original_language_sel.add_attr('id','original_language')
        original_language_sel.append_option('--Select--','')
        for language in my.original_languages:
            original_language_sel.append_option(language,language)
        if my.sob.get('original_language') == None:
            my.sob['original_language'] = ''
        original_language_sel.set_value(my.sob.get('original_language'))
        table2.add_cell(original_language_sel)

        table2.add_row()
        table2.add_cell(table2.hr())
        table2.add_row()

        c1 = table2.add_cell('Source:')
        c1.add_attr('nowrap','nowrap')
        source_sel = SelectWdg('source')
        source_sel.add_attr('id','source')
        source_sel.append_option('--Select--','')
        for s in my.sources:
            source_sel.append_option(s,s)
        if my.sob.get('source') == None:
            my.sob['source'] = ''
        source_sel.set_value(my.sob.get('source'))
        table2.add_cell(source_sel)

        c1 = table2.add_cell('Audio Config:')
        c1.add_attr('nowrap','nowrap')
        audio_config_sel = SelectWdg('audio_config')
        audio_config_sel.add_attr('id','audio_config')
        audio_config_sel.append_option('--Select--','')
        for a in my.audio_configs:
            audio_config_sel.append_option(a,a)
        if my.sob.get('audio_config') == None:
            my.sob['audio_config'] = ''
        audio_config_sel.set_value(my.sob.get('audio_config'))
        table2.add_cell(audio_config_sel)

        c1 = table2.add_cell('Master Audio Config:')
        c1.add_attr('nowrap','nowrap')
        master_audio_config_sel = SelectWdg('master_audio_config')
        master_audio_config_sel.add_attr('id','master_audio_config')
        master_audio_config_sel.append_option('--Select--','')
        for a in my.audio_configs:
            master_audio_config_sel.append_option(a,a)
        if my.sob.get('master_audio_config') == None:
            my.sob['master_audio_config'] = ''
        master_audio_config_sel.set_value(my.sob.get('master_audio_config'))
        table2.add_cell(master_audio_config_sel)
         
        c1 = table2.add_cell('Run Time Calc:')
        c1.add_attr('nowrap','nowrap')
        tb1 = TextWdg('run_time_calc')
        tb1.add_attr('id','run_time_calc')
        tb1.set_value(my.sob['run_time_calc'])
        #Might want to add the : timestamp js here -- from qc reports
        table2.add_cell(tb1)
   
        table2.add_row()
        table2.add_cell(table2.hr())
        table2.add_row()

        c1 = table2.add_cell('Narrative:')
        c1.add_attr('nowrap','nowrap')
        narrative_sel = SelectWdg('narrative')
        narrative_sel.add_attr('id','narrative')
        narrative_sel.append_option('--Select--','')
        for n in my.narratives:
            narrative_sel.append_option(n,n)
        if my.sob.get('narrative') == None:
            my.sob['narrative'] = ''
        narrative_sel.set_value(my.sob.get('narrative'))
        table2.add_cell(narrative_sel)

        c1 = table2.add_cell('Texted/Textless:')
        c1.add_attr('nowrap','nowrap')
        tt_sel = SelectWdg('texted_textless')
        tt_sel.add_attr('id','texted_textless')
        tt_sel.append_option('--Select--','')
        for t in my.texted_textless:
            tt_sel.append_option(t,t)
        if my.sob.get('texted_textless') == None:
            my.sob['texted_textless'] = ''
        tt_sel.set_value(my.sob.get('texted_textless'))
        table2.add_cell(tt_sel)

        c1 = table2.add_cell('Aspect Ratio:')
        c1.add_attr('nowrap','nowrap')
        aspect_ratio_sel = SelectWdg('aspect_ratio')
        aspect_ratio_sel.add_attr('id','aspect_ratio')
        aspect_ratio_sel.append_option('--Select--','')
        for a in my.aspect_ratios:
            aspect_ratio_sel.append_option(a,a)
        if my.sob.get('aspect_ratio') == None:
            my.sob['aspect_ratio'] = ''
        aspect_ratio_sel.set_value(my.sob.get('aspect_ratio'))
        table2.add_cell(aspect_ratio_sel)

        c1 = table2.add_cell('Standard:')
        c1.add_attr('nowrap','nowrap')
        standard_sel = SelectWdg('standard')
        standard_sel.add_attr('id','standard')
        standard_sel.append_option('--Select--','')
        for s in my.standards:
            standard_sel.append_option(s,s)
        if my.sob.get('standard') == None:
            my.sob['standard'] = ''
        standard_sel.set_value(my.sob.get('standard'))
        table2.add_cell(standard_sel)

        table2.add_row()
        table2.add_cell(table2.hr())
        table2.add_row()

        c1 = table2.add_cell('HD:')
        c1.add_attr('nowrap','nowrap')
        hd_sel = SelectWdg('hd')
        hd_sel.add_attr('id','hd')
        hd_sel.append_option('--Select--','')
        for s in my.hd:
            hd_sel.append_option(s,s)
        if my.sob.get('hd') == None:
            my.sob['hd'] = ''
        hd_sel.set_value(my.sob.get('hd'))
        table2.add_cell(hd_sel)

#        c1 = table2.add_cell('Genre:')
#        c1.add_attr('nowrap','nowrap')
#        tb1 = TextWdg('genre')
#        tb1.add_attr('id','genre')
#        tb1.set_value(my.sob['genre'])
#        table2.add_cell(tb1)

        c1 = table2.add_cell('MPAA:')
        c1.add_attr('nowrap','nowrap')
        mpaa_sel = SelectWdg('mpaa')
        mpaa_sel.add_attr('id','mpaa')
        mpaa_sel.append_option('--Select--','')
        for s in my.mpaa:
            mpaa_sel.append_option(s,s)
        if my.sob.get('mpaa') == None:
            my.sob['mpaa'] = ''
        mpaa_sel.set_value(my.sob.get('mpaa'))
        table2.add_cell(mpaa_sel)

        c1 = table2.add_cell('MPAA Ratings:')
        c1.add_attr('nowrap','nowrap')
        mpaa_ratings_sel = SelectWdg('mpaa_ratings')
        mpaa_ratings_sel.add_attr('id','mpaa_ratings')
        mpaa_ratings_sel.append_option('--Select--','')
        for s in my.mpaa_ratings:
            mpaa_ratings_sel.append_option(s,s)
        if my.sob.get('mpaa_ratings') == None:
            my.sob['mpaa_ratings'] = ''
        mpaa_ratings_sel.set_value(my.sob.get('mpaa_ratings'))
        table2.add_cell(mpaa_ratings_sel)

        table2.add_row()
        table2.add_cell(table2.hr())
#        table2.add_row()
#
#        c1 = table2.add_cell('UK Ratings:')
#        c1.add_attr('nowrap','nowrap')
#        uk_ratings_sel = SelectWdg('uk_ratings')
#        uk_ratings_sel.add_attr('id','uk_ratings')
#        uk_ratings_sel.append_option('--Select--','')
#        for s in my.uk_ratings:
#            uk_ratings_sel.append_option(s,s)
#        if my.sob.get('uk_ratings') == None:
#            my.sob['uk_ratings'] = ''
#        uk_ratings_sel.set_value(my.sob.get('uk_ratings'))
#        table2.add_cell(uk_ratings_sel)
#
#        c1 = table2.add_cell('Australia Ratings:')
#        c1.add_attr('nowrap','nowrap')
#        australia_ratings_sel = SelectWdg('australia_ratings')
#        australia_ratings_sel.add_attr('id','australia_ratings')
#        australia_ratings_sel.append_option('--Select--','')
#        for s in my.australia_ratings:
#            australia_ratings_sel.append_option(s,s)
#        if my.sob.get('australia_ratings') == None:
#            my.sob['australia_ratings'] = ''
#        australia_ratings_sel.set_value(my.sob.get('australia_ratings'))
#        table2.add_cell(australia_ratings_sel)
#
#        c1 = table2.add_cell('Germany Ratings:')
#        c1.add_attr('nowrap','nowrap')
#        germany_ratings_sel = SelectWdg('germany_ratings')
#        germany_ratings_sel.add_attr('id','germany_ratings')
#        germany_ratings_sel.append_option('--Select--','')
#        for s in my.germany_ratings:
#            germany_ratings_sel.append_option(s,s)
#        if my.sob.get('germany_ratings') == None:
#            my.sob['germany_ratings'] = ''
#        germany_ratings_sel.set_value(my.sob.get('germany_ratings'))
#        table2.add_cell(germany_ratings_sel)
#
#        table2.add_row()
#        table2.add_cell(table2.hr())
        table2.add_row()

        c1 = table2.add_cell('Legal Rights:')
        c1.add_attr('nowrap','nowrap')
        legal_rights_sel = SelectWdg('legal_right')
        legal_rights_sel.add_attr('id','legal_right')
        legal_rights_sel.append_option('--Select--','')
        for s in my.legal_rights:
            legal_rights_sel.append_option(s,s)
        if my.sob.get('legal_right') == None:
            my.sob['legal_right'] = ''
        legal_rights_sel.set_value(my.sob.get('legal_right'))
        table2.add_cell(legal_rights_sel)
        

        from tactic.ui.widget import CalendarInputWdg, ActionButtonWdg
        ld = table2.add_cell('Legal Date: ')
        ld.add_attr('nowrap','nowrap')
        legal_date = CalendarInputWdg("legal_date")
        if my.sob.get('legal_date') not in [None,'']:
            legal_date.set_option('default', my.fix_date(my.sob.get('legal_date')))
        legal_date.set_option('show_activator', True)
        legal_date.set_option('show_confirm', False)
        #legal_date.set_option('show_text', True)
        legal_date.set_option('show_today', False)
        #legal_date.set_option('read_only', False)    
        legal_date.add_attr('id','legal_date')
        table2.add_cell(legal_date)

        c1 = table2.add_cell('Legal Comment:')
        c1.add_attr('nowrap','nowrap')
        tb1 = TextWdg('legal_comment')
        tb1.add_attr('id','legal_comment')
        tb1.add_style('width','300px')
        tb1.set_value(my.sob['legal_comment'])
        c2 = table2.add_cell(tb1)
        c2.add_attr('colspan','3')

        table2.add_row()
        table2.add_cell(table2.hr())
        table2.add_row()

        c1 = table2.add_cell('HE Creative Comment:')
        c1.add_attr('nowrap','nowrap')
        tb1 = TextWdg('he_creative_comment')
        tb1.add_attr('id','he_creative_comment')
        tb1.add_style('width','300px')
        tb1.set_value(my.sob['he_creative_comment'])
        c2 = table2.add_cell(tb1)
        c2.add_attr('colspan','3')

        table2.add_row()
        table2.add_cell(table2.hr())
        table2.add_row()

        c1 = table2.add_cell('URL:')
        c1.add_attr('nowrap','nowrap')
        tb1 = TextWdg('url')
        tb1.add_attr('id','url')
        tb1.add_style('width','300px')
        tb1.set_value(my.sob['url'])
        c2 = table2.add_cell(tb1)
        c2.add_attr('colspan','3')

        table2.add_row()
        table2.add_cell(table2.hr())
        table2.add_row()
        
        #ta1 = table2.add_cell('Cast Info:')
        #table2.add_row() 
        #ta1 = table2.add_cell('<textarea cols="90" rows="10" class="spt_input" name="cast_info" id="cast_info">%s</textarea>' % my.sob.get('cast_info'))

        #table2.add_row()
        submit = table2.add_cell('<input type="button" value="Submit"/>')
        sk = ''
        if not my.is_insert:
            sk = my.sob.get('__search_key__')
        submit.add_behavior(my.get_submit(sk))
        if not my.is_insert:
            xml = table2.add_cell('<input type="button" value="Generate XML"/>')
            xml.add_behavior(my.get_xml(sk))

         


        table.add_cell(table2)
        widget.add(table)
        return widget



class CDeliverableXMLGeneratorWdg(BaseTableElementWdg):

    def init(my):
        from tactic_client_lib import TacticServerStub
        my.code = my.kwargs.get('code')
        my.client = my.kwargs.get('client')
        my.server = TacticServerStub.get()
        my.sob = my.server.eval("@SOBJECT(twog/client_deliverable['code','%s'])" % my.code)[0]
   
    def make_camel_case(my, str):
        last = ''
        rez = ''
        count = 0
        for i in str:
            if count == 0:
                rez = i.upper()
            else:
                if last == '_':
                    rez = '%s%s' % (rez, i.upper())
                else:
                    rez =  '%s%s' % (rez, i)
            count = count + 1
            last = i
        return rez

    def make_sony_xml(my):
        fields = ['record_id','Title_ID','Title_Type','Title_Name','Trailer_Version','Trailer_Type','Trailer_Number','Title_Comment','Narrative','Trailer_Rev_Number','Source','Aspect_Ratio','Audio_Config','Standard','Run_Time_Calc','Texted_Textless','Master_Audio_Config','Sony_Barcode','HD','Legal_Right','Legal_Date','MPAA','Legal_Comment','URL','HE_Creative_Comment','MPAA_Ratings','UK_Ratings','Australia_Ratings','Germany_Ratings','Genre','Original_Language','Cast_Info','Alpha ID','Release_Number','Language_Audio','Language_Subtitled','Language_Text']
        xml = '''<?xml version="1.0" encoding="utf-8" ?>\n  <ingest notify="">'''
        id = my.sob.get('clip_id') #MTM Still need to figure this out
        xml = '''%s\n    <clip id="%s">\n      <metadata>''' % (xml, id)
        for guy in fields:
            field_name = ''
            if guy == 'record_id':
                field_name = guy
            else:
                field_name = guy.replace(' ','_')
                field_name = field_name.lower() 
            if 'sony' in field_name:
                field_name = field_name.replace('sony','client')
            value = my.sob.get(field_name)
            if value not in [None,'']:
                value = value.encode('utf-8')
            #print "FIELD = %s, ACTUAL FIELD = %s, VALUE = %s" % (guy, field_name, value)
            xml = '''%s\n        <label key="%s" value="%s"/>''' % (xml, guy, value)
        xml = '''%s\n      </metadata>\n    </clip>\n  </ingest>''' % xml
           
        return xml

    def get_display(my):
        xml = ''
        if my.client in ['Sony','sony']:
            xml = my.make_sony_xml()
        widget = DivWdg()
        table = Table()
        table.add_row()
        table.add_cell('<textarea cols="120" rows="50" class="xml_display" name="xml_display" disabled="disabled">%s</textarea>' % xml)     
        widget.add(table)
        return widget
 









