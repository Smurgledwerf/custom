__all__ = ["MovementPrintLauncherWdg2","MovementPrintWdg2"]
import tacticenv
import os, datetime
from pyasm.biz import *
from pyasm.web import Table, DivWdg
from pyasm.widget import SelectWdg
from tactic.ui.common import BaseTableElementWdg
from tactic.ui.common import BaseRefreshWdg
from tactic.ui.panel import EditWdg

class MovementPrintLauncherWdg2(BaseTableElementWdg):

    def init(my):
        from tactic_client_lib import TacticServerStub
        my.server = TacticServerStub.get()

    def get_launch_behavior(my):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                          var server = TacticServerStub.get();
                          var sk = bvr.src_el.get('sk');
                          var from_comp = bvr.src_el.get('from_comp');
                          var to_comp = bvr.src_el.get('to_comp');
                          var shipper = bvr.src_el.get('shipper');
                          var shipping_class = bvr.src_el.get('shipping_class');
                          var waybill = bvr.src_el.get('waybill');
                          var title = bvr.src_el.get('title');
                          var description = bvr.src_el.get('description');
                          var timestamp = bvr.src_el.get('timestamp');
                          var code = sk.split('code=')[1];
                          var class_name = 'order_builder.MovementPrintWdg2';
                          kwargs = {
                                           'sk': sk,
                                           'code': code,
                                           'from_comp': from_comp,
                                           'to_comp': to_comp,
                                           'shipper': shipper,
                                           'shipping_class': shipping_class,
                                           'title': title,
                                           'waybill': waybill,
                                           'description': description,
                                           'timestamp': timestamp
                                   };
                          spt.panel.load_popup('Print Movement Sheet for ' + title, class_name, kwargs);
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
        sk = my.server.build_search_key('twog/movement', code)
        shipping_class = sobject.get_value('shipping_class')
        title = sobject.get_value('name')
        waybill = sobject.get_value('waybill')
        sending_company_code = sobject.get_value('sending_company_code')
        receiving_company_code = sobject.get_value('receiving_company_code')
        shipper_code = sobject.get_value('shipper_code')
        description = sobject.get_value('description')
        timestamp = sobject.get_value('timestamp')
        
        widget = DivWdg()
        table = Table()
        table.add_attr('width', '50px')
        table.add_row()
        cell1 = table.add_cell('<img border="0" style="vertical-align: middle" title="" src="/context/icons/silk/printer.png">')
        launch_behavior = my.get_launch_behavior()
        cell1.add_attr('sk',sk)
        cell1.add_attr('shipping_class',shipping_class)
        cell1.add_attr('to_comp',receiving_company_code)
        cell1.add_attr('from_comp',sending_company_code)
        cell1.add_attr('waybill',waybill)
        cell1.add_attr('title',title)
        cell1.add_attr('shipper',shipper_code)
        cell1.add_attr('description',description)
        cell1.add_attr('timestamp',timestamp)
        cell1.add_style('cursor: pointer;')
        cell1.add_behavior(launch_behavior)
        widget.add(table)

        return widget

class MovementPrintWdg2(BaseRefreshWdg):

    def init(my):
        from client.tactic_client_lib import TacticServerStub
        from pyasm.common import Environment
        my.server = TacticServerStub.get()
        my.sk = ''
        my.types = ['Movement']
        my.template_files = {'Movement': '/var/www/html/source_labels/movements.html'}
        my.code = ''
        my.from_comp = ''
        my.to_comp = ''
        my.shipper = ''
        my.title = ''
        my.shipping_class = ''
        my.waybill = ''
        my.description = ''
        my.timestamp = ''
    
    def get_display(my):   
        #print "IN MOVEMENT PRINT WDG. KWARGS = %s" % my.kwargs
        #os.system('echo "IN MOVEMENT PRINT WDG. KWARGS = %s" >> print_troubles' % my.kwargs)
        table = Table()
        my.sk = str(my.kwargs.get('sk'))
        my.code = str(my.kwargs.get('code'))
        my.from_comp = str(my.kwargs.get('from_comp'))
        my.to_comp = str(my.kwargs.get('to_comp'))
        my.shipper = str(my.kwargs.get('shipper'))
        my.title = str(my.kwargs.get('title'))
        my.shipping_class = str(my.kwargs.get('shipping_class'))
        my.waybill = str(my.kwargs.get('waybill'))
        my.description = str(my.kwargs.get('description'))
        my.timestamp = str(my.kwargs.get('timestamp'))

        from_name_poss = my.server.eval("@SOBJECT(twog/company['code','%s'])" % my.from_comp)
        from_name = 'Could Not Find Name of Sender'
        from_address = 'No Address in System'
        from_suite = 'No Suite in System'
        from_city = 'No City in System'
        from_state = 'No State in System'
        from_country = 'No Country in System'
        from_zip = 'No Zip in System'
        from_phone = 'No Phone in System'
        from_main_contact_name = 'No Main Contact Setup for this Company'
        if len(from_name_poss) > 0:
            from_name = from_name_poss[0].get('name')
            from_address = from_name_poss[0].get('street_address')
            from_suite = from_name_poss[0].get('suite')
            from_city = from_name_poss[0].get('city')
            from_state = from_name_poss[0].get('state')
            from_country = from_name_poss[0].get('country')
            from_zip = from_name_poss[0].get('zip')
            from_phone = from_name_poss[0].get('phone')
            from_main_contact_code = from_name_poss[0].get('main_contact')
            main_contact_expr = "@SOBJECT(twog/person['code','%s'])" % from_main_contact_code
            from_main_contact = my.server.eval(main_contact_expr)
            if len(from_main_contact) > 0:
                from_main_contact = from_main_contact[0]
                from_main_contact_name = '%s %s' % (from_main_contact.get('first_name'), from_main_contact.get('last_name'))

        to_name_poss = my.server.eval("@SOBJECT(twog/company['code','%s'])" % my.to_comp)
        to_name = 'Could Not Find Name of Receiver'
        to_address = 'No Address in System'
        to_suite = 'No Suite in System'
        to_city = 'No City in System'
        to_state = 'No State in System'
        to_country = 'No Country in System'
        to_zip = 'No Zip in System'
        to_phone = 'No Phone in System'
        to_main_contact_name = 'No Main Contact Setup for this Company'
        if len(to_name_poss) > 0:
            to_name = to_name_poss[0].get('name')
            to_address = to_name_poss[0].get('street_address')
            to_suite = to_name_poss[0].get('suite')
            to_city = to_name_poss[0].get('city')
            to_state = to_name_poss[0].get('state')
            to_country = to_name_poss[0].get('country')
            to_zip = to_name_poss[0].get('zip')
            to_phone = to_name_poss[0].get('phone')
            to_main_contact_code = to_name_poss[0].get('main_contact')
            main_contact_expr = "@SOBJECT(twog/person['code','%s'])" % to_main_contact_code
            to_main_contact = my.server.eval(main_contact_expr)
            #os.system('echo "MAIN CONTACT EXPR = %s:::TO MAIN CONTACT = %s" >> print_troubles' % (main_contact_expr, to_main_contact))
            if len(to_main_contact) > 0:
                to_main_contact = to_main_contact[0]
                #os.system('echo "TO MAIN CONTACT = %s" >> print_troubles' % to_main_contact)
                to_main_contact_name = '%s %s' % (to_main_contact.get('first_name'), to_main_contact.get('last_name'))
        shipper_name_poss = my.server.eval("@SOBJECT(twog/shipper['code','%s'])" % my.shipper)
        shipper_name = 'Could Not Find Name of Shipping Company'
        if len(shipper_name_poss) > 0:
            shipper_name = shipper_name_poss[0].get('name')
        table.add_attr('class','print_movement_wdg')
        table.add_row()
        all_sources_expr = "@SOBJECT(twog/asset_to_movement['movement_code','%s'])" % my.code
        all_sources = my.server.eval(all_sources_expr)
        all_sources_str = ''
        for lynk in all_sources:
            source = my.server.eval("@SOBJECT(twog/source['code','%s'])" % lynk.get('source_code'))[0]
            out_bar = ''
            obars = my.server.eval("@SOBJECT(twog/outside_barcode['source_code','%s'])" % source.get('code'))
            for obar in obars:
                out_bar = '%s,%s' % (out_bar, obar.get('barcode'))
            if out_bar != '':
                if out_bar[0] == ',':
                    out_bar = out_bar[1:]
            source_client_poss = my.server.eval("@SOBJECT(twog/client['code','%s'])" % source.get('client_code'))
            source_client = 'This Source Has No Client Attached'
            if len(source_client_poss) > 0:
                source_client = source_client_poss[0].get('name')
            source_title = '%s: %s' % (source.get('title'), source.get('episode'))
            if all_sources_str == '':
                all_sources_str = '<div id="source"><div id="barcode">%s</div><div id="title">%s</div><div id="episode">%s</div><div id="type">%s</div><div id="outside_barcode">%s</div><div id="client">%s</div></div>' % (source.get('barcode'), source.get('title'), source.get('episode'), source.get('format'), out_bar, source_client)
                #all_sources_str = '<div id="source"><div id="barcode">%s</div><div id="title">%s</div><div id="episode">%s</div><div id="type">%s</div><div id="outside_barcode">%s</div><div id="client">%s</div></div>' % (source.get('barcode'), source.get('title'), source.get('episode'), source.get('source_type'), out_bar, source_client)
            else:
                all_sources_str = '%s<div id="source"><div id="barcode">%s</div><div id="title">%s</div><div id="episode">%s</div><div id="type">%s</div><div id="outside_barcode">%s</div><div id="client">%s</div></div>' % (all_sources_str, source.get('barcode'), source.get('title'), source.get('episode'), source.get('format'), out_bar, source_client)
                #all_sources_str = '%s<div id="source"><div id="barcode">%s</div><div id="title">%s</div><div id="episode">%s</div><div id="type">%s</div><div id="outside_barcode">%s</div><div id="client">%s</div></div>' % (all_sources_str, source.get('barcode'), source.get('title'), source.get('episode'), source.get('source_type'), out_bar, source_client)
            
        select = SelectWdg('print_type')
        for guy in my.types:
            select.append_option(guy,guy)  
        selly = table.add_cell(select)
        selly.add_attr('align','center')
        table.add_row()
        date = str(datetime.datetime.now()).split(' ')[0]
        for guy in my.types:
            result = ''
            f = open(my.template_files[guy], 'r')
            for line in f:
                if not line.strip():
        	    continue
                else:
                    line = line.rstrip('\r\n')
                    line =line.replace('[FROM]',from_name)
                    line =line.replace('[FROM_STREET_ADDRESS]',from_address)
                    line =line.replace('[FROM_SUITE]',from_suite)
                    line =line.replace('[FROM_CITY]',from_city)
                    line =line.replace('[FROM_STATE]',from_state)
                    line =line.replace('[FROM_COUNTRY]',from_country)
                    line =line.replace('[FROM_ZIP]',from_zip)
                    line =line.replace('[FROM_PHONE]',from_phone)
                    line =line.replace('[FROM_MAIN_CONTACT]',from_name)
                    line =line.replace('[TO]',to_name)
                    line =line.replace('[TO_STREET_ADDRESS]',to_address)
                    line =line.replace('[TO_SUITE]',to_suite)
                    line =line.replace('[TO_CITY]',to_city)
                    line =line.replace('[TO_STATE]',to_state)
                    line =line.replace('[TO_COUNTRY]',to_country)
                    line =line.replace('[TO_ZIP]',to_zip)
                    line =line.replace('[TO_PHONE]',to_phone)
                    line =line.replace('[TO_MAIN_CONTACT]',to_name)
                    line =line.replace('[SHIPPER_CODE]',shipper_name)
                    line =line.replace('[SHIPPING_CLASS]',my.shipping_class)
                    line =line.replace('[WAYBILL]',my.waybill)
                    line =line.replace('[DESCRIPTION]',my.description)
                    line =line.replace('[MOVEMENT_CODE]', my.code)
                    line =line.replace('[TIMESTAMP]', my.timestamp)
                    line =line.replace('<!-- SOURCES/ELEMENTS GO HERE -->', all_sources_str)
                    result = '%s%s' % (result,line)
            f.close()
            new_mov_file = '/var/www/html/source_labels/movements/%s_%s.html' % (my.code, guy)
            if os.path.exists(new_mov_file):
                os.system('rm -rf %s' % new_mov_file)
            new_guy = open(new_mov_file, 'w') 
            new_guy.write(result)
            new_guy.close()
        t1 = table.add_cell('')
        t1.add_style('width: 100%s;' % '%')
        do_it = table.add_cell('<input type="button" value="Get Movement Page For %s"/>' % (my.title)) 
        do_it.add_behavior(my.get_open_movement_print_page())
        t2 = table.add_cell('')
        t2.add_style('width: 100%s;' % '%')
        return table

    def get_open_movement_print_page(my):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                          var code = '%s';
                          var top_el = spt.api.get_parent(bvr.src_el, '.print_movement_wdg');
                          var sels = top_el.getElementsByTagName('select');
                          var type_sel = '';
                          for(var r = 0; r < sels.length; r++){
                              if(sels[r].name == 'print_type'){
                                  type_sel = sels[r];
                              }
                          } 
                          var type = type_sel.value;
                          var url = 'http://tactic01/source_labels/movements/' + code + '_' + type + '.html';
                          new_win = window.open(url,'_blank','toolbar=1,location=1,directories=1,status=1,menubar=1,scrollbars=0,resizable=0'); 
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                          //alert(err);
                }
         ''' % (my.code)
        }
        return behavior
