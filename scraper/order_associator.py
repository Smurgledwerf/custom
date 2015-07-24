__all__ = ["OrderAssociatorLauncherWdg","ImdbOrderAssociatorWdg","OrderImageWdg"]
import tacticenv
import subprocess
from pyasm.common import Environment
from pyasm.biz import *
from pyasm.web import Table, DivWdg
from pyasm.widget import SelectWdg, IconWdg, TextWdg, CheckboxWdg
from pyasm.prod.biz import ProdSetting
from tactic.ui.common import BaseTableElementWdg
from tactic.ui.common import BaseRefreshWdg
from pyasm.command import *
from pyasm.search import Search
from alternative_elements.customcheckbox import *
from order_builder.order_builder import OrderBuilderLauncherWdg

class OrderAssociatorLauncherWdg(BaseTableElementWdg):
    #This is the button that launches the TitleSelectorWdg

    def init(my):
        nothing = 'true'

    def get_launch_behavior(my):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                          var my_code = bvr.src_el.get('code');
                          var my_name = bvr.src_el.get('name');
                          var sol = bvr.src_el.get('search_on_load');
                          var class_name = 'scraper.ImdbOrderAssociatorWdg';
                          kwargs = {
                                           'code': my_code,
                                           'title_of_show': my_name,
                                           'search_on_load': sol
                                   };
                          if(my_name != ''){
                              spt.app_busy.show('Searching IMDb for ' + my_name);
                          }else{
                              spt.app_busy.show('Searching IMDb');
                          }
                          spt.panel.load_popup('IMDb Order Associator', class_name, kwargs);
                          spt.app_busy.hide();
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         '''}
        return behavior

    def get_display(my):
        code = ''
        name = ''
        if 'code' in my.kwargs.keys():
            code = my.kwargs.get('code') 
        else: 
            sobject = my.get_current_sobject()
            code = sobject.get_code()
            name = sobject.get_value('name')
        if 'name' in my.kwargs.keys():
            name = my.kwargs.get('name')
        search_on_load = 'false'
        if 'search_on_load' in my.kwargs.keys():
            search_on_load = my.kwargs.get('search_on_load')
         
        widget = DivWdg()
        table = Table()
        table.add_attr('width', '50px')
        table.add_row()
        cell1 = table.add_cell('<img border="0" style="vertical-align: middle" title="" src="/context/icons/custom/imdb.png">')
        cell1.add_attr('code', code)
        cell1.add_attr('name', name)
        cell1.add_attr('search_on_load', search_on_load)
        launch_behavior = my.get_launch_behavior()
        cell1.add_style('cursor: pointer;')
        cell1.add_behavior(launch_behavior)
        widget.add(table)

        return widget

class ImdbOrderAssociatorWdg(BaseRefreshWdg):

    def init(my):
        my.title_of_show = my.kwargs.get('title_of_show')
        my.code = my.kwargs.get('code')
        search_on_load = my.kwargs.get('search_on_load')
        my.search_when_loaded = False
        if search_on_load == 'true':
            my.search_when_loaded = True

    def get_search(my):
        behavior = {'css_class': 'clickme', 'type': 'change', 'cbjs_action': '''        
             try{
                    title_of_show = bvr.src_el.value;
                    spt.app_busy.show('Searching IMDb for ' + title_of_show);
                    top_el = spt.api.get_parent(bvr.src_el, '.scraper');
                    spt.api.load_panel(top_el, 'scraper.ImdbOrderAssociatorWdg', {'title_of_show': title_of_show, 'search_on_load': 'true'}); 
                    spt.app_busy.hide();
                }
                catch(err){
                          spt.app_busy.hide();
                          alert(err);
                }
        '''}
        return behavior 

    def parse_scraper_string(my, str_in):
        str_in = str_in.strip()
        titles_chunked = str_in.split('-MTM_TITLE_MTM-')
        t_array = []
        for t in titles_chunked:
            if len(t) > 0:
                tdict = {}
                subarrays = t.split(':-MTM-SUBARRAY-:')
                for s in subarrays:
                    array_name = 'no_name'
                    if len(s) > 0:
                        array_s = s.split(':-::MTM::-')
                        array_name = array_s[0]
                        array_remainder = array_s[1]
                        tdict[array_name] = {}
                        subfields = array_remainder.split(':-MTM-FIELD-:')
                        for chunk in subfields:
                            if len(chunk) > 0:
                                chunk_s = chunk.split('=>')
                                subfield = chunk_s[0]
                                subval = chunk_s[1]
                                tdict[array_name][subfield] = subval
                t_array.append(tdict)
        return t_array
                        
                    
                            
    def get_hover_behavior(my, count):
        behavior = {'type': 'hover', 'cbjs_action_over': '''        
                        try{
                            var count = '%s';
                            top_el = spt.api.get_parent(bvr.src_el, '.scraper');
                            hiders = top_el.getElementsByClassName('hidden_info');
                            for(var r = 0; r < hiders.length; r++){
                                if(hiders[r].getAttribute('hidden_id') == count){
                                    hiders[r].style.display = 'table-row';
                                }
                            }
                      
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         ''' % count, 
         'cbjs_action_out': '''
                        try{
                            var count = '%s';
                            top_el = spt.api.get_parent(bvr.src_el, '.scraper');
                            hiders = top_el.getElementsByClassName('hidden_info');
                            for(var r = 0; r < hiders.length; r++){
                                if(hiders[r].getAttribute('hidden_id') == count){
                                    hiders[r].style.display = 'none';
                                }
                            }
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         ''' % count}
        return behavior

    def get_more_info(my, count):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                            var count = '%s';
                            top_el = spt.api.get_parent(bvr.src_el, '.scraper');
                            hiders = top_el.getElementsByClassName('hidden_info');
                            for(var r = 0; r < hiders.length; r++){
                                if(hiders[r].getAttribute('hidden_id') == count){
                                    if(hiders[r].style.display == 'table_row'){
                                        hiders[r].style.display = 'none';
                                    }else{
                                        hiders[r].style.display = 'table-row';
                                    }
                                }else{
                                    hiders[r].style.display = 'none';
                                }
                            }
                      
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         ''' % count}
        return behavior

    def get_associate_em(my):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                            refresh_image_timer = function(timelen, order_str){
                                setTimeout(function(){refresh_images(order_str)}, timelen); 
                            }
                            refresh_images = function(order_str){
                                var top_el = spt.api.get_parent(bvr.src_el, '.scraper');
                                orders = order_str.split(',');
                                for(var r = 0; r < orders.length; r++){
                                    img_cell = top_el.getElementById('img_' + orders[r]);
                                    spt.api.load_panel(img_cell, 'scraper.order_associator.OrderImageWdg', {'code': orders[r]});
                                }
                            }
                            try{
                                var top_el = spt.api.get_parent(bvr.src_el, '.scraper');
                                orders = top_el.getElementsByClassName('associated_orders');
                                imdbs = top_el.getElementsByClassName('associated_imdb');
                                selected_imdb = '';
                                for(var r = 0; r < imdbs.length; r++){
                                    if(imdbs[r].getAttribute('checked') == 'true'){
                                        selected_imdb = imdbs[r];
                                    }
                                }
                                if(selected_imdb == ''){
                                    alert("You must first select the IMDB entry to associate to the Order(s).");
                                }else{
                                    selected_orders = ''
                                    for(var r = 0; r < orders.length; r++){
                                        if(orders[r].getAttribute('checked') == 'true'){
                                            if(selected_orders == ''){
                                                selected_orders = orders[r].getAttribute('value_field');
                                            }else{
                                                selected_orders = selected_orders + ',' + orders[r].getAttribute('value_field');
                                            }
                                        }
                                    } 
                                    if(selected_orders == ''){
                                        alert("You need to select at least 1 Order to associate to the IMDB entry");
                                    }else{
                                        if(confirm("Are you sure you want to associate the selected Order(s) with the selected IMDB entry?")){
                                            imdb_id = selected_imdb.getAttribute('extra1');
                                            imdb_title = selected_imdb.getAttribute('extra2');
                                            imdb_runtime = selected_imdb.getAttribute('extra3');
                                            imdb_release_date = selected_imdb.getAttribute('extra4');
                                            imdb_url = selected_imdb.getAttribute('extra5');
                                            imdb_poster_url = selected_imdb.getAttribute('extra6');
                                            server = TacticServerStub.get();
                                            sos = selected_orders.split(',');
                                            for(var r = 0; r < sos.length; r++){
                                                server.update(server.build_search_key('twog/order',sos[r]), {'imdb_id': imdb_id, 'imdb_title': imdb_title, 'imdb_runtime': imdb_runtime, 'imdb_release_date': imdb_release_date, 'imdb_url': imdb_url, 'imdb_poster_url': imdb_poster_url});
                                            }
                                            //Now send the string of orders to the command that will upload the pics 
                                            thing = server.execute_cmd('scraper.scraper_command.IMDBImageAssociatorCmd', {'orders_to_associate': selected_orders});
                                            refresh_image_timer(6000, selected_orders);
                                        }
                                    }
                                }
                    }
                    catch(err){
                              spt.app_busy.hide();
                              spt.alert(spt.exception.handler(err));
                    }
             '''}
        return behavior


    def highlight_order_row(my, order_code):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                            try{
                                order_code = '%s'; 
                                var checked_img = '<img src="/context/icons/custom/custom_checked.png"/>'
                                var not_checked_img = '<img src="/context/icons/custom/custom_unchecked.png"/>'
                                var top_el = spt.api.get_parent(bvr.src_el, '.scraper');
                                this_row = top_el.getElementById('row_' + order_code);
                                if(bvr.src_el.getAttribute('checked') == 'true'){
                                    this_row.style.backgroundColor = '#d6ae1d';
                                    bvr.src_el.setAttribute('checked','true');
                                }else{
                                    this_row.style.backgroundColor = '#FFFFFF';
                                    bvr.src_el.setAttribute('checked','false');
                                }
                    }
                    catch(err){
                              spt.app_busy.hide();
                              spt.alert(spt.exception.handler(err));
                    }
             ''' % order_code}
        return behavior
        
    def act_like_radio(my, title_id):             
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                            try{
                                title_id = '%s'; 
                                var checked_img = '<img src="/context/icons/custom/custom_checked.png"/>'
                                var not_checked_img = '<img src="/context/icons/custom/custom_unchecked.png"/>'
                                var top_el = spt.api.get_parent(bvr.src_el, '.scraper');
                                if(bvr.src_el.getAttribute('checked') == 'true'){
                                    this_row = top_el.getElementById('row_' + title_id);
                                    this_row.style.backgroundColor = '#42d6a7';
                                    inputs = top_el.getElementsByClassName('associated_imdb');
                                    for(var r = 0; r < inputs.length; r++){
                                        that_id = inputs[r].getAttribute('value_field');
                                        if(that_id != title_id){ 
                                            inputs[r].setAttribute('checked','false');
                                            inputs[r].innerHTML = not_checked_img;
                                            that_row = top_el.getElementById('row_' + that_id);
                                            that_row.style.backgroundColor = '#FFFFFF'; 
                                        }
                                    }
                                }else{
                                    this_row = top_el.getElementById('row_' + title_id);
                                    this_row.style.backgroundColor = '#FFFFFF';
                                    bvr.src_el.setAttribute('checked','false');
                                }
                    }
                    catch(err){
                              spt.app_busy.hide();
                              spt.alert(spt.exception.handler(err));
                    }
             ''' % title_id}
        return behavior
        

    def get_multiple_title_info(my, title_of_show):
        proc = subprocess.Popen('''php /opt/spt/custom/scraper/runner.php "%s"''' % title_of_show, shell=True, stdout=subprocess.PIPE)
        delimited_str = proc.stdout.read()
        info = None 
        if 'No Titles Found' in delimited_str or delimited_str in [None,'']:
            info = []
        else:
            info = my.parse_scraper_string(delimited_str)
        return info

    def get_poster_img(my, order_code):
        from pyasm.search import Search
        img_path = ''
        order_search = Search("twog/order")
        order_search.add_filter('code',order_code)
        order = order_search.get_sobject()
        order_id = order.get_id()
        snaps_s = Search("sthpw/snapshot")
        snaps_s.add_filter('search_id',order_id)
        snaps_s.add_filter('search_type','twog/order?project=twog')
        snaps_s.add_filter('is_current','1')
        snaps_s.add_filter('version','0',op='>')
        snaps_s.add_where("\"context\" in ('publish','icon','MISC')")
        snaps_s.add_order_by('timestamp desc')
        snaps = snaps_s.get_sobjects()
        if len(snaps) > 0:
            from tactic_client_lib import TacticServerStub
            server = TacticServerStub.get()
            snap = snaps[0]
            img_path = server.get_path_from_snapshot(snap.get_code(), mode="web")
            if img_path not in [None,'']:
                img_path = 'http://tactic01%s' % img_path
        return img_path

    def get_toggler(my): 
        toggle_behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                            try{
                                var checked_img = '<img src="/context/icons/custom/custom_checked.png"/>'
                                var not_checked_img = '<img src="/context/icons/custom/custom_unchecked.png"/>'
                                var top_el = spt.api.get_parent(bvr.src_el, '.scraper');
                                inputs = top_el.getElementsByClassName('associated_orders');
                                var curr_val = bvr.src_el.getAttribute('checked');
                                image = '';
                                if(curr_val == 'false'){
                                    curr_val = false;
                                    image = not_checked_img;
                                }else if(curr_val == 'true'){
                                    curr_val = true;
                                    image = checked_img;
                                }
                                for(var r = 0; r < inputs.length; r++){
                                    inputs[r].setAttribute('checked',curr_val);
                                    inputs[r].innerHTML = image;
                                    this_row = top_el.getElementById('row_' + inputs[r].getAttribute('value_field'));
                                    if(curr_val == false){
                                        this_row.style.backgroundColor = '#FFFFFF';
                                    }else{
                                        this_row.style.backgroundColor = '#d6ae1d';
                                    }
                                }
                    }
                    catch(err){
                              spt.app_busy.hide();
                              spt.alert(spt.exception.handler(err));
                    }
        '''}
        return toggle_behavior


    def get_display(my):
        widget = DivWdg()
        table = Table()
        table.add_attr('class','scraper')
        table.add_style('background-color: #FFFFFF;')
        table.add_style('height: 1000px;')
        table.add_row()
        tb = TextWdg('title_box')
        tb.add_attr('id','title_box')
        tb.add_attr('size','45')
        multiple_titles = None
        searched_imdb = False
        orders = []
        no_img = 'http://tactic.2gdigital.com/imdb_images/no_image.png'
        if 'code' in my.kwargs.keys() and my.title_of_show in [None,'']:
            from tactic_client_lib import TacticServerStub
            server = TacticServerStub.get()
            this_order = server.eval("@SOBJECT(twog/order['code','%s'])" % my.kwargs.get('code'))[0]
            my.title_of_show = this_order.get('name')
            
        if my.title_of_show not in [None,'']:
            tb.set_value(my.title_of_show)
            if my.search_when_loaded:
                #poster_url_text = my.get_poster_url(my.title_of_show)
                #poster_url = poster_url_text.split('=')[1]
                from tactic_client_lib import TacticServerStub
                server = TacticServerStub.get()
                orders = server.eval("@SOBJECT(twog/order['name','~','%s']['classification','not in','Master|Cancelled'])" % my.title_of_show)
                #order_s = Search("twog/order")
                #order_s.add_where("\"name\" like '%s%s%s'" %  ('%', my.title_of_show.lower(), '%'))
                #statement = order_s.get_statement()
                #print "STATEMENT = %s" % statement
                #orders = order_s.get_sobjects()
                #print "ORDER LEN = %s" % len(orders)
                if len(orders) > 0:
                    multiple_titles = my.get_multiple_title_info(my.title_of_show)
                    #print "MULTIPLE TITLES = %s" % multiple_titles
                    searched_imdb = True
        tb.add_behavior(my.get_search())
        top_tbl = Table()
        top_tbl.add_attr('width','400px')
        top_tbl.add_attr('height','50px')
        top_tbl.add_attr('cellpadding','20')
        top_tbl.add_attr('cellspacing','20')
        top_tbl.add_style('background-color: #417e97;')
        top_tbl.add_row()
        if len(orders) > 0:
            butt = top_tbl.add_cell('<input type="button" value="Associate All Selected"/>')
            butt.add_behavior(my.get_associate_em())
        sn = top_tbl.add_cell('<font color="#d9af1f"><b>Search Name:</b></font>&nbsp;&nbsp;&nbsp;&nbsp;')
        sn.add_attr('align','right')
        sn.add_attr('nowrap','nowrap')
        tb_cell1 = top_tbl.add_cell(tb)
        tb_cell = table.add_cell(top_tbl)
        tb_cell.add_attr('colspan','2')
        tb_cell.add_attr('align','center')
        order_table = Table()
        order_table.add_attr('border','1')
        order_table.add_attr('cellpadding','10')
        order_table.add_row()
        if len(orders) > 0:
            toggler = CustomCheckboxWdg(name='chk_toggler',additional_js=my.get_toggler(),value_field='toggler',id='selection_toggler',checked='false',text='<b><- Select/Deselect ALL</b>',text_spot='right',text_align='left',nowrap='nowrap')
            order_table.add_cell(toggler)
            order_table.add_row()
            order_table.add_cell('Selector') 
            order_table.add_cell('Poster')
            order_table.add_cell('Order Builder') 
            order_table.add_cell('Code') 
            order_table.add_cell('Name') 
            order_table.add_cell('Client') 
            order_table.add_cell('PO Number') 
            order_table.add_cell('Classification') 
            order_table.add_cell('Platform') 
            order_table.add_cell('Due Date') 
            order_table.add_cell('Completion Ratio') 
            order_table.add_cell('Scheduler') 
        elif my.title_of_show not in [None,''] and my.search_when_loaded:
            dude = order_table.add_cell('<b>No Tactic Orders Were Found With "%s" In The Name</b>' % my.title_of_show) 
            dude.add_style('font-size: 14px;')
        else:
            dude = order_table.add_cell('<b>Please type the name of the show in the box above</b>') 
            dude.add_style('font-size: 14px;')
        for order in orders:
            checkbox = CustomCheckboxWdg(name='associate_order_%s' % order.get('code'),additional_js=my.highlight_order_row(order.get('code')),alert_name=order.get('name'),value_field=order.get('code'),checked='false',dom_class='associated_orders') 
            imarow = order_table.add_row()
            imarow.add_attr('id','row_%s' % order.get('code'))
            chk = order_table.add_cell(checkbox) 
            chk.add_attr('align','center')
            poster_cell = order_table.add_cell(OrderImageWdg(code=order.get('code')))
            poster_cell.add_attr('id','img_%s' % order.get('code'))
            ob = OrderBuilderLauncherWdg(code=order.get('code'))
            obc = order_table.add_cell(ob)
            obc.add_attr('align','center')
            order_table.add_cell(order.get('code')) 
            order_table.add_cell(order.get('name')) 
            order_table.add_cell(order.get('client_name')) 
            order_table.add_cell(order.get('po_number')) 
            order_table.add_cell(order.get('classification')) 
            order_table.add_cell(order.get('platform')) 
            order_table.add_cell(order.get('due_date')) 
            order_table.add_cell('%s/%s' % (order.get('titles_completed'), order.get('titles_total'))) 
            order_table.add_cell(order.get('login')) 
        imdb_table = Table()
        imdb_table.add_attr('border','1')
        imdb_table.add_attr('cellpadding','10')
        if multiple_titles not in [None,''] and len(multiple_titles) > 0:
            mcount = 0
            seen_titles = []
            for m in multiple_titles:
                title_id = m['TopLevel']['title_id']
                if title_id not in seen_titles:
                    seen_titles.append(title_id)
                    imarow = imdb_table.add_row()
                    imarow.add_attr('id','row_%s' % m['TopLevel']['title_id'])
                    this_img = no_img
                    if m['TopLevel']['poster'] not in [None,'']:
                        this_img = m['TopLevel']['poster']
                    checkbox = CustomCheckboxWdg(name='associate_imdb_%s' % m['TopLevel']['title_id'],additional_js=my.act_like_radio(m['TopLevel']['title_id']),alert_name=m['TopLevel']['title'],value_field=m['TopLevel']['title_id'],checked='false',dom_class='associated_imdb',extra1=m['TopLevel']['title_id'],extra2=m['TopLevel']['title'],extra3=m['TopLevel']['runtime'],extra4=m['TopLevel']['release_date'],extra5=m['TopLevel']['imdb_url'],extra6=this_img) 
                    chk = imdb_table.add_cell(checkbox)
                    chk.add_attr('align','center')
                    imdb_table.add_cell('<img src="%s"/>' % this_img)
                    info_tbl = Table()
                    info_tbl.add_row()
                    title_cell = info_tbl.add_cell('<b>Title: %s</b>' % m['TopLevel']['title'])
                    title_cell.add_style('cursor: pointer;')
                    title_cell.add_behavior(my.get_more_info(mcount))
                    info_tbl.add_row()
                    info_tbl.add_cell('<i>Original Title: %s</i>' % m['TopLevel']['original_title'])
                    info_tbl.add_row()
                    info_tbl.add_cell('<i>Run Time: %s</i>' % m['TopLevel']['runtime'])
                    info_tbl.add_row()
                    info_tbl.add_cell('<i>Release Date: %s</i>' % m['TopLevel']['release_date'])
                    info_tbl.add_row()
                    info_tbl.add_cell('<i>Rating: %s</i>' % m['TopLevel']['rating'])
                    info_tbl.add_row()
                    info_tbl.add_cell('<i>IMDb URL: %s</i>' % m['TopLevel']['imdb_url'])
                    info_tbl.add_row()
                    info_tbl.add_cell('<i>Plot: %s</i>' % m['TopLevel']['plot'])
                    info2 = Table()
                    mkeys = m.keys()
                    for k in mkeys: 
                        if k not in ['media_images','recommended_titles','videos','cinematographers','editors','producers','cast','directors','writers','stars','plot_keywords','musicians','TopLevel']:
                            info2.add_row()
                            info2.add_cell('<b><u>%s</u></b>' % k)
                            dudes = m[k]
                            dkeys = dudes.keys()
                            for d in dkeys:
                                info2.add_row()
                                info2.add_cell('%s: %s' % (d, dudes[d])) 
                    intable = imdb_table.add_cell(info_tbl)
                    intable.add_attr('valign','top')
                    intable.add_attr('align','left')
                    #intable.add_behavior(my.get_hover_behavior(mcount))
                    hidrow = imdb_table.add_row()
                    hidrow.add_attr('hidden_id',mcount)
                    hidrow.add_attr('class','hidden_info')
                    hidrow.add_style('display: none;')
                    intable2 = imdb_table.add_cell(info2)
                    intable2.add_attr('valign','top')
                    intable2.add_attr('align','left')
                    mcount = mcount + 1
        elif my.title_of_show not in [None,''] and searched_imdb:
            imdb_table.add_row()
            dude = imdb_table.add_cell('<b>No IMDb Titles Were Found With "%s" In The Name</b>' % my.title_of_show)
            dude.add_style('font-size: 14px;')
            imarow = imdb_table.add_row()
            imarow.add_attr('id','row_%s' % 'none')
            checkbox = CustomCheckboxWdg(name='associate_imdb_%s' % 'none',additional_js=my.act_like_radio('none'),alert_name='No IMDb Link',value_field='none',checked='false',dom_class='associated_imdb',extra1='none',extra2='No IMDb Link',extra3='',extra4='',extra5='none',extra6=no_img) 
            chk = imdb_table.add_cell(checkbox)
            chk.add_attr('align','center')
            imdb_table.add_cell('<img src="%s"/>' % no_img)
            info_tbl = Table()
            info_tbl.add_row()
            title_cell = info_tbl.add_cell('<b>Title: %s</b>' % 'No IMDb Link')
            title_cell.add_style('cursor: pointer;')
            intable = imdb_table.add_cell(info_tbl)
            intable.add_attr('valign','top')
            intable.add_attr('align','left')
            hidrow = imdb_table.add_row()
            hidrow.add_attr('class','hidden_info')
            hidrow.add_style('display: none;')
        elif my.title_of_show not in [None,'']:
            imdb_table.add_row()
            dude = imdb_table.add_cell("<b>No Tactic Orders Found, Didn't Query IMDb</b>")
            dude.add_style('font-size: 14px;')
        table.add_row()
        order_div = DivWdg()
        order_div.add_style('overflow-y: scroll;')
        order_div.add_style('height: 1000px;')
        order_div.add_style('width: 750px;')
        order_div.add('<font size=7><b>Tactic Orders</b></font>')
        order_div.add(order_table)
        ot = table.add_cell(order_div)
        ot.add_attr('valign','top')
        imdb_div = DivWdg()
        imdb_div.add_style('overflow-y: scroll;')
        imdb_div.add_style('height: 1000px;')
        imdb_div.add_style('width: 750px;')
        imdb_div.add('<font size=7><b>IMDb</b></font>')
        imdb_div.add(imdb_table)
        it = table.add_cell(imdb_div)
        it.add_attr('valign','top')
        widget.add(table)
        return widget


class OrderImageWdg(BaseRefreshWdg):

    def init(my):
        my.code = my.kwargs.get('code')

    def get_poster_img(my, order_code):
        from pyasm.search import Search
        img_path = ''
        order_search = Search("twog/order")
        order_search.add_filter('code',order_code)
        order = order_search.get_sobject()
        order_id = order.get_id()
        snaps_s = Search("sthpw/snapshot")
        snaps_s.add_filter('search_id',order_id)
        snaps_s.add_filter('search_type','twog/order?project=twog')
        snaps_s.add_filter('is_current','1')
        snaps_s.add_filter('version','0',op='>')
        snaps_s.add_where("\"context\" in ('publish','icon','MISC')")
        snaps_s.add_order_by('timestamp desc')
        snaps = snaps_s.get_sobjects()
        if len(snaps) > 0:
            from tactic_client_lib import TacticServerStub
            server = TacticServerStub.get()
            snap = snaps[0]
            img_path = server.get_path_from_snapshot(snap.get_code(), mode="web")
            if img_path not in [None,'']:
                img_path = 'http://tactic01%s' % img_path
        return img_path


    def get_display(my):
        widget = DivWdg()
        table = Table()
        order_poster = my.get_poster_img(my.code)
        order_poster_entry = 'None'
        if order_poster not in [None,'']:
            order_poster_entry = '<img src="%s" width="135" height="200"/>' % order_poster
        table.add_cell(order_poster_entry)
        widget.add(table)
        return widget


