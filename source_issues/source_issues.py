__all__ = ["SourceDisplayWdg","SourceReportPopupWdg"]
import tacticenv
from pyasm.common import Environment
from pyasm.biz import *
from pyasm.web import Table, DivWdg
from pyasm.widget import SelectWdg, IconWdg, TextWdg, CheckboxWdg

from tactic.ui.common import BaseTableElementWdg
from tactic.ui.common import BaseRefreshWdg
from tactic.ui.panel import EditWdg
from tactic.ui.widget.button_new_wdg import ButtonSmallNewWdg, ButtonRowWdg
#from globaller import *

class SourceDisplayWdg(BaseTableElementWdg):

    def init(my):
        from tactic_client_lib import TacticServerStub
        my.server = TacticServerStub.get()
        my.color_lookup = {'IN': '#f9d0af','OUT': '#b9bfcc'}
        my.x_butt = "<img src='/context/icons/common/BtnKill_Black.gif' title='Delete' name='Delete'/>" 

    def get_reporter_behavior(my, work_order_code, user):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                          var work_order_code = '%s';
                          var user = '%s';
                          var class_name = 'source_issues.source_issues.SourceReportPopupWdg';
                          kwargs = {
                                           'user': user,
                                           'code': work_order_code 
                                   };
                          spt.panel.load_popup('Report Issue(s)', class_name, kwargs);
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                          //alert(err);
                }
         ''' % (work_order_code, user)}
        return behavior

    def inspect_source_popup(my, source_code, security):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''
                        try{
                          var source_code = '%s';
                          var security = '%s';
                          if(security){
                              spt.panel.load_popup('View Asset', 'order_builder.SourceSecurityEditWdg', {'source_code': source_code});
                          }else{
                              spt.panel.load_popup('View Asset', 'tactic.ui.panel.EditWdg', {element_name: 'general', mode: 'view', search_type: 'twog/source', code: source_code, title: 'Asset ' + source_code, view: 'edit', widget_key: 'edit_layout'});
                          }
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                          //alert(err);
                }
         ''' % (source_code, security)}
        return behavior

    def location_changer(my, thing_sk):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''
                        try{
                          var thing_sk = '%s';
                          st = thing_sk.split('?')[0];
                          code = thing_sk.split('code=')[1];
                          var server = TacticServerStub.get();
                          var location = server.eval("@GET(" + st + "['code','" + code + "'].location)")
                          if(location.length > 0){
                              location = location[0];
                          }else{
                              location = '';
                          }
                          var new_loc = prompt('Please enter the new location', location);
                          if(new_loc != location){
                              server.update(thing_sk, {'location': new_loc});
                              loc_cell = document.getElementsByClassName('sd_location_' + code)[0];
                              loc_cell.innerHTML = new_loc;
                          }
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                          //alert(err);
                }
         ''' % (thing_sk)}
        return behavior

   

    def inspect_intermediate_popup(my, intermediate_code):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''
                        try{
                          var intermediate_code = '%s';
                          spt.panel.load_popup('View Intermediate File', 'tactic.ui.panel.EditWdg', {element_name: 'general', mode: 'view', search_type: 'twog/intermediate_file', code: intermediate_code, title: 'Intermediate File ' + intermediate_code, view: 'edit', widget_key: 'edit_layout'});
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                          //alert(err);
                }
         ''' % (intermediate_code)}
        return behavior

    def report_missing(my, wo_code, user, platform):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''
                        try{
                          var wo_code = '%s';
                          var user = '%s';
                          var platform = '%s';
                          sources = 'MISSING SOURCE'
                          spt.panel.load_popup('View Intermediate File', 'source_issues.source_issues.SourceReportPopupWdg', {'work_order_code': wo_code, 'user': user, 'sources': sources, 'platform': platform});
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                          //alert(err);
                }
         ''' % (wo_code, user, platform)}
        return behavior


    def alert_popup(my, wo_code, user, platform):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''
                        try{
                          var wo_code = '%s';
                          var user = '%s';
                          var platform = '%s';
                          var server = TacticServerStub.get();
                          top_el = document.getElementsByClassName('source_display_' + wo_code)[0];
                          possible_checks = top_el.getElementsByClassName('SPT_BVR');
                          sources = ''
                          delim1 = 'ZXuO#'
                          delim2 = '|||'
                          at_least_one = false;
                          for(var r = 0; r < possible_checks.length; r++){
                              if(possible_checks[r].type == 'checkbox'){
                                  check = possible_checks[r];
                                  obj_code = check.getAttribute('code');
                                  obj_name = check.getAttribute('special_name');
                                  obj_location = check.getAttribute('location');
                                  if(check.checked){
                                      if(sources == ''){
                                          sources = obj_code + delim2 + obj_name + delim2 + obj_location;
                                      }else{
                                          sources = sources + delim1 + obj_code + delim2 + obj_name + delim2 + obj_location;
                                      }
                                      at_least_one = true;
                                  }
                              }
                          }
                          if(at_least_one){
                              spt.panel.load_popup('View Intermediate File', 'source_issues.source_issues.SourceReportPopupWdg', {'work_order_code': wo_code, 'user': user, 'sources': sources, 'platform': platform});
                          }else{
                              alert('Select the source(s) you want to report by checking the checkbox(es)');
                          }
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                          //alert(err);
                }
         ''' % (wo_code, user, platform)}
        return behavior

    def get_wo_barcode_insert_behavior(my, wo_code):
        behavior = {'css_class': 'clickme', 'type': 'change', 'cbjs_action': '''        
                        function oc(a){
                            var o = {};
                            for(var i=0;i<a.length;i++){
                                o[a[i]]='';
                            }
                            return o;
                        }
                        try{
                          //alert('m38');
                          var server = TacticServerStub.get();
                          wo_code = '%s';
                          wo = server.eval("@SOBJECT(twog/work_order['code','" + wo_code + "'])")[0];
                          title_code = server.eval("@GET(twog/proj['code','" + wo.proj_code + "'].title_code)")[0];
                          title_sk = server.build_search_key('twog/title', title_code);
                          barcode = bvr.src_el.value;
                          barcode = barcode.toUpperCase();
                          source_expr = "@SOBJECT(twog/source['barcode','" + barcode + "'])";
                          sources = server.eval(source_expr);
                          if(sources.length > 1){
                              alert('Something is wrong with inventory. There are ' + sources.length + ' sources with that barcode.');
                              bvr.src_el.value = '';
                          }else if(sources.length == 0){
                              source_expr = "@SOBJECT(twog/source['client_asset_id','" + barcode + "'])";
                              sources = server.eval(source_expr);
                              if(sources.length > 1){
                                  alert('Something is wrong with inventory. There are ' + sources.length + ' sources with that client_asset_id.');
                                  bvr.src_el.value = '';
                                  sources = []
                              }
                          }
                          if(sources.length == 1){
                              source = sources[0];
                              title_sources = server.eval("@GET(twog/title_origin['title_code','" + title_code + "'].source_code)");
                              if(!(source.code in oc(title_sources))){ 
                                  server.insert('twog/title_origin', {title_code: title_code, source_code: source.code});
                              }
                              wo_sources = server.eval("@GET(twog/work_order_sources['work_order_code','" + wo_code + "'].source_code)");
                              wo_passins = server.eval("@SOBJECT(twog/work_order_passin['work_order_code','" + wo_code + "'])");
                              for(var r = 0; r < wo_passins.length; r++){
                                  if(wo_passins[r].deliverable_source_code != ''){
                                      wo_sources.push(wo_passins[r].deliverable_source_code);
                                  }
                              }
                              if(!(source.code in oc(wo_sources))){ 
                                  server.insert('twog/work_order_sources', {'work_order_code': wo_code, source_code: source.code});

                                  work_o_sources_expr = "@SOBJECT(twog/work_order_sources['work_order_code','" + wo_code + "'])";
        			  work_o_sources = server.eval(work_o_sources_expr);
                                  work_o_passins = server.eval("@SOBJECT(twog/work_order_passin['work_order_code','" + wo_code + "'])");
        			  work_o_deliverables_expr = "@SOBJECT(twog/work_order_deliverables['work_order_code','" + wo_code + "'])";
        			  work_o_deliverables = server.eval(work_o_deliverables_expr);
        			  my_sources = []
        			  my_deliverables = []
        			  for(var r = 0; r < work_o_sources.length; r++){
        			      source_expr = "@SOBJECT(twog/source['code','" + work_o_sources[r].source_code + "'])";
        			      source = server.eval(source_expr)
        			      if(source.length > 0){
        				  my_sources.push(source[0])
        			      }
        			  }
        			  for(var r = 0; r < work_o_passins.length; r++){
                                      var dsc = work_o_passins[r].deliverable_source_code;
                                      if(dsc != '' && dsc != null){
        			          source_expr = "@SOBJECT(twog/source['code','" + dsc + "'])";
        			          source = server.eval(source_expr);
        			          if(source.length > 0){
        				      my_sources.push(source[0]);
        			          } 
                                      }
        			  }
        			  for(var r = 0; r < work_o_deliverables.length; r++){
        			      source_expr = "@SOBJECT(twog/source['code','" + work_o_deliverables[r].deliverable_source_code + "'])";
        			      source = server.eval(source_expr);
        			      if(source.length > 0){
        		 		  my_deliverables.push(source[0])
        			      }
        			  }
        			  for(var r = 0; r < my_sources.length; r++){
        			      kids = my_sources[r].children.split(',');
        			      new_str = my_sources[r].children;
        			      for(var t = 0; t < my_deliverables.length; t++){
        				  if(!(my_deliverables[t].code in oc(kids))){
        				      if(new_str == '' || new_str == null){
        					  new_str = my_deliverables[t].code;
        				      }else{
        					  new_str = new_str + ',' + my_deliverables[t].code;
        				      }
        				  }
        			      }
        			      server.update(my_sources[r].__search_key__, {'children': new_str});
        			  }
        			  for(var r = 0; r < my_deliverables.length; r++){
        			      ancestors = my_deliverables[r].ancestors.split(',');
        			      new_str = my_deliverables[r].ancestors;
        			      for(var t = 0; t < my_sources.length; t++){
        				  if(!(my_sources[t].code in oc(ancestors))){
        				      if(new_str == '' || new_str == null){
        					  new_str = my_sources[t].code;
        				      }else{
        					  new_str = new_str + ',' + my_sources[t].code;
        				      }
        				  }
        			      }
        			      server.update(my_deliverables[r].__search_key__, {'ancestors': new_str});
        			  }
                              }
                              the_el = document.getElementsByClassName('ov_sources_' + wo_code)[0];
        		      spt.api.load_panel(the_el, 'source_issues.SourceDisplayWdg', {'work_order_code': wo_code}); 
                          }else{
                              if(sources.length == 0){
                                  alert('There are no sources with that barcode. Try a different barcode?');
                                  bvr.src_el.value = '';
                              }
                          }
                          
                          
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                          //alert(err);
                }
         ''' % (wo_code)}
        return behavior

    def get_source_killer_behavior(my, wo_source_code, work_order_code, title): #SIDDED
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                          //alert('m44');
                          var server = TacticServerStub.get();
                          wo_source_code = '%s';
                          work_order_code = '%s';
                          title = '%s';
                          if(confirm("Are you sure you want to delete " + title + " from this work order?")){
                              wo_source_sk = server.build_search_key('twog/work_order_sources', wo_source_code);
                              server.retire_sobject(wo_source_sk);
                              the_el = document.getElementsByClassName('ov_sources_' + work_order_code)[0];
        		      spt.api.load_panel(the_el, 'source_issues.SourceDisplayWdg', {'work_order_code': work_order_code}); 
                          }
                          
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                          //alert(err);
                }
         ''' % (wo_source_code, work_order_code, title)}
        return behavior

    def get_deliverable_passin_killer_behavior(my, passin_code, work_order_code, title):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                           var server = TacticServerStub.get();
                           var passin_code = '%s';
                           var work_order_code = '%s';
                           title = '%s';
                           if(confirm("Are you sure you want to delete '" + title + "' from this work order's Passed-in elements?")){
                               passin = server.eval("@SOBJECT(twog/work_order_passin['code','" + passin_code + "'])")[0];
                               server.retire_sobject(passin.__search_key__);
                               the_el = document.getElementsByClassName('ov_sources_' + work_order_code)[0];
        		       spt.api.load_panel(the_el, 'source_issues.SourceDisplayWdg', {'work_order_code': work_order_code}); 
                           } 
                           
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                          //alert(err);
                }
         ''' % (passin_code, work_order_code, title)}
        return behavior

    def get_intermediate_passin_killer_behavior(my, passin_code, work_order_code, title):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                           var server = TacticServerStub.get();
                           var passin_code = '%s';
                           var work_order_code = '%s';
                           var title = '%s';
                           if(confirm("Are you sure you want to delete '" + title + "' from this work order's Passed-in elements?")){
                               passin = server.eval("@SOBJECT(twog/work_order_passin['code','" + passin_code + "'])")[0];
                               server.retire_sobject(passin.__search_key__);
                               the_el = document.getElementsByClassName('ov_sources_' + work_order_code)[0];
        		       spt.api.load_panel(the_el, 'source_issues.SourceDisplayWdg', {'work_order_code': work_order_code}); 
                           } 
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                          //alert(err);
                }
         ''' % (passin_code, work_order_code, title)}
        return behavior

    def make_source_unit(my, in_link, work_order_code, in_or_out, type_str):
        inlink_st = in_link.get('__search_key__').split('?')[0]
        linker = ''
        if inlink_st == 'twog/work_order_passin':
            linker = in_link.get('deliverable_source_code')
        elif inlink_st == 'twog/work_order_deliverables':
            linker = in_link.get('deliverable_source_code')
        elif inlink_st == 'twog/work_order_sources':
            linker = in_link.get('source_code')
            
        sob = my.server.eval("@SOBJECT(twog/source['code','%s'])" % linker)[0]
        st = sob.get('__search_key__').split('?')[0]
        title = sob.get('title')
        if sob.get('episode') not in [None,'']:
            title = "%s: %s" % (title, sob.get('episode'))
        part = ''
        if sob.get('part') not in [None,'']:
            part = sob.get('part') 
        table = Table()
        table.add_attr('width','100%s' % '%')
        table.add_attr('border','1')
        table.add_style('background-color: %s;' % my.color_lookup[in_or_out])
        table.add_row()
        table_src = Table()
        type_cell = table_src.add_cell(type_str)
        type_cell.add_attr('width', '25%s' % '%')
        table_src.add_row()
        checkbox = CheckboxWdg('src_disp_chk_%s' % sob.get('code'))
        checkbox.add_attr('code',sob.get('code'))
        checkbox.add_attr('special_name',sob.get('barcode'))
        checkbox.add_attr('location',sob.get('location'))
        checkbox.set_value(False)
        #checkbox.set_persistence()
        table_src.add_cell(checkbox)
        table.add_cell(table_src)

        top_tbl = Table()
        top_tbl.add_attr('width','100%s' % '%')
        top_tbl.add_row()
        top_tbl.add_cell('<u>Title:</u> %s' % title)
        if type_str == 'SRC':
            killer = top_tbl.add_cell(my.x_butt)
            killer.add_style('cursor: pointer;')
            killer.add_behavior(my.get_source_killer_behavior(in_link.get('code'), work_order_code, title))
        elif type_str == 'SRC-PASSIN':
            killer = top_tbl.add_cell(my.x_butt)
            killer.add_style('cursor: pointer;')
            killer.add_behavior(my.get_deliverable_passin_killer_behavior(in_link.get('code'), work_order_code, title))

        info_tbl = Table() 
        info_tbl.add_attr('width','100%s' % '%')
        info_tbl.add_row()
        info_tbl.add_cell(top_tbl)
        info_tbl.add_row()
        info_tbl.add_cell('<u>Part:</u> %s' % part)
        info_tbl.add_row()
        cell1 = info_tbl.add_cell('<u>Barcode: <b>%s</u></b>' % (sob.get('barcode')))
        cell1.add_style('cursor: pointer;')
        cell1.add_behavior(my.inspect_source_popup(sob.get('code'), sob.get('high_security')))
        info_tbl.add_row()
        info_tbl.add_cell('%s, %s, %s' % (sob.get('standard'), sob.get('aspect_ratio'), sob.get('total_run_time')))
        
        long_cell = table.add_cell(info_tbl)
        long_cell.add_attr('width','75%s' % '%')
        table.add_row()
        loc_cell1 = table.add_cell('&nbsp;&nbsp;<u>Location:</u>')
        loc_cell1.add_style('cursor: pointer;')
        loc_cell1.add_behavior(my.location_changer(sob.get('__search_key__')))
        loc_cell2 = table.add_cell(sob.get('location'))
        loc_cell2.add_attr('class', 'sd_location_%s' % sob.get('code'))
        loc_cell2.add_attr('colspan','2')
        
        return table

    def make_intermediate_unit(my, in_link, work_order_code, in_or_out, type_str):
        inlink_st = in_link.get('__search_key__').split('?')[0]
        if inlink_st == 'twog/work_order_intermediate':
            lookmeup = in_link.get('intermediate_file_code')
        elif inlink_st == 'twog/work_order_passin':
            lookmeup = in_link.get('intermediate_file_code')
        sob = my.server.eval("@SOBJECT(twog/intermediate_file['code','%s'])" % lookmeup)[0]
        table = Table()
        name = sob.get('name')
        description = sob.get('description')
        table.add_attr('width','100%s' % '%')
        table.add_attr('border','1')
        table.add_style('background-color: %s;' % my.color_lookup[in_or_out])
        table.add_row()
        table_src = Table()
        type_cell = table_src.add_cell(type_str)
        type_cell.add_attr('width', '25%s' % '%')
        table_src.add_row()
        checkbox = CheckboxWdg('src_disp_chk_%s' % sob.get('code'))
        checkbox.add_attr('code',sob.get('code'))
        checkbox.add_attr('special_name',name)
        checkbox.add_attr('location',sob.get('location'))
        checkbox.set_value(False)
        #checkbox.set_persistence()
        table_src.add_cell(checkbox)
        table.add_cell(table_src)

        info_tbl = Table() 
        info_tbl.add_attr('width','100%s' % '%')
        info_tbl.add_row()
        cell1 = info_tbl.add_cell('<u>Title:</u> %s' % name)
        cell1.add_style('cursor: pointer;')
        cell1.add_behavior(my.inspect_intermediate_popup(sob.get('code')))
        if in_or_out == 'IN':
            killer = info_tbl.add_cell(my.x_butt)
            killer.add_style('cursor: pointer;')
            killer.add_behavior(my.get_intermediate_passin_killer_behavior(in_link.get('code'), work_order_code, name))
            info_tbl.add_row()
            desc = info_tbl.add_cell(description)
            desc.add_attr('colspan','2')
        else:
            info_tbl.add_row()
            desc = info_tbl.add_cell(description)

        long_cell = table.add_cell(info_tbl)
        long_cell.add_attr('width','75%s' % '%')
        table.add_row()
        loc_cell1 = table.add_cell('&nbsp;&nbsp;<u>Location:</u>')
        loc_cell1.add_style('cursor: pointer;')
        loc_cell1.add_behavior(my.location_changer(sob.get('__search_key__')))
        loc_cell2 = table.add_cell(sob.get('location'))
        loc_cell2.add_attr('class', 'sd_location_%s' % sob.get('code'))
        loc_cell2.add_attr('colspan','2')
        return table

    def get_display(my):
        login = Environment.get_login()
        user_name = login.get_login()
        work_order_code = ''
        if 'work_order_code' in my.kwargs.keys():
            work_order_code = str(my.kwargs.get('work_order_code'))
        else:
            sobject = my.get_current_sobject()
            work_order_code = sobject.get_code()
        work_order = my.server.eval("@SOBJECT(twog/work_order['code','%s'])" % work_order_code)[0]
        widget = DivWdg()
        widget.add_attr('class','ov_sources_%s' % work_order_code)
        table = Table()
        table.add_attr('width','100%s' % '%')
        table.add_attr('class','source_display_%s' % work_order_code)
        at_least1 = False


        table.add_row()
        tbl_top = Table()
        tbl_top.add_row()
        missing = tbl_top.add_cell('<u>Report Missing Source</u>')
        missing.add_attr('nowrap','nowrap')
        missing.add_style('cursor: pointer;')
        missing.add_behavior(my.report_missing(work_order_code, user_name, work_order.get('platform'))) 
        middle = tbl_top.add_cell(' ')
        middle.set_style('width: 100%s;' % '%')
        right = tbl_top.add_cell('Add Source: ')
        right.add_attr('nowrap','nowrap')
        right.add_attr('align','right')
        add_tb = TextWdg('wo_barcode_insert_%s' % work_order_code)
        add_tb.add_behavior(my.get_wo_barcode_insert_behavior(work_order_code))
        adder = tbl_top.add_cell(add_tb)
        adder.add_behavior(my.get_wo_barcode_insert_behavior(work_order_code)) 
        table.add_row()
        table.add_cell(tbl_top)
        #INS
        wo_sources = my.server.eval("@SOBJECT(twog/work_order_sources['work_order_code','%s'])" % work_order_code)
        for wo_source in wo_sources:
            table.add_row()
            table.add_cell(my.make_source_unit(wo_source, work_order_code, 'IN', 'SRC'))
            at_least1 = True
            
           
        passin_deliverables = my.server.eval("@SOBJECT(twog/work_order_passin['work_order_code','%s'])" % work_order_code)
        for wo_source in passin_deliverables:
            if wo_source.get('deliverable_source_code') not in [None,'']:
                table.add_row()
                table.add_cell(my.make_source_unit(wo_source, work_order_code, 'IN', 'SRC-PASSIN'))
                at_least1 = True
            
        passin_interms = my.server.eval("@SOBJECT(twog/work_order_passin['work_order_code','%s'])" % work_order_code)
        for interm in passin_interms:
            if interm.get('intermediate_file_code') not in [None,'']:
                table.add_row()
                table.add_cell(my.make_intermediate_unit(interm, work_order_code, 'IN', 'INTM-PASSIN'))
                at_least1 = True

        #OUTS
        intermediates = my.server.eval("@SOBJECT(twog/work_order_intermediate['work_order_code','%s'])" % work_order_code)
        for interm in intermediates:
            table.add_row()
            table.add_cell(my.make_intermediate_unit(interm, work_order_code, 'OUT', 'INTM-OUT'))
            at_least1 = True

        deliverable_sources = my.server.eval("@SOBJECT(twog/work_order_deliverables['work_order_code','%s'])" % work_order_code)
        for dsource in deliverable_sources:
            table.add_row()
            table.add_cell(my.make_source_unit(dsource, work_order_code, 'OUT', 'DLV-OUT'))
            at_least1 = True
        #also need intermediates and other stuff shown in work_order_assets_wdg
        if at_least1:
            table.add_row()
            button_cell = table.add_cell('<input type="button" value="Issue Alert(s)"/>')
            button_cell.add_behavior(my.alert_popup(work_order_code, user_name, work_order.get('platform')))
            cell3 = table.add_cell(' ')
            cell3.add_attr('width','80%s' % '%') 
        widget.add(table)
        #--print "LEAVING OBLW"

        return widget

class SourceReportPopupWdg(BaseTableElementWdg):

    def init(my):
        nothing = 'true'

    def alert_problems(my, wo_code, user, platform):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''
                        try{
                          var wo_code = '%s';
                          var user = '%s';
                          var platform = '%s';
                          var server = TacticServerStub.get();
                          top_el = document.getElementsByClassName('alert_popup_' + wo_code)[0];
                          file_path_els = top_el.getElementsByClassName('report_file_' + wo_code);
                          descript_els = top_el.getElementsByClassName('report_operator_description_' + wo_code);
                          selects = top_el.getElementsByTagName('select');
                          codes = []
                          code_to_name = {};
                          code_to_file = {};
                          code_to_descript = {};
                          code_to_type = {};
                          for(var r = 0; r < file_path_els.length; r++){
                              el = file_path_els[r];
                              code = el.getAttribute('code');
                              name = el.getAttribute('name');
                              if(codes.indexOf(code) == -1){
                                  codes.push(code);
                                  code_to_name[code] = name;
                                  code_to_file[code] = el.value;
                              }
                          }
                          for(var r = 0; r < descript_els.length; r++){
                              el = descript_els[r];
                              code = el.getAttribute('code');
                              name = el.getAttribute('name');
                              code_to_descript[code] = el.value;
                          }
                          for(var r = 0; r < selects.length; r++){
                              el = selects[r];
                              code = el.getAttribute('code');
                              type = el.value;
                              code_to_type[code] = type;
                          }
                          for(var r = 0; r < codes.length; r++){
                              code = codes[r];
                              server.insert('twog/source_issues', {'reported_by': user, 'work_order_code': wo_code, 'operator_description': code_to_descript[code], 'file_path': code_to_file[code], 'status': 'New', 'lookup_code': code, 'type': code_to_type[code], 'name_or_barcode': code_to_name[code], 'platform': platform});
                          }
                          work_order = server.eval("@SOBJECT(twog/work_order['code','" + wo_code + "'])")[0];
                          scheduler = work_order.login;
                          scheduler_email = server.eval("@GET(sthpw/login['login','" + scheduler + "']['license_type','user'].email)");
                          if(scheduler_email.length > 0){
                              scheduler_email = scheduler_email[0];
                          }else{
                              scheduler_email = 'Scheduling@2gdigital.com';
                          }
                          group_emails = server.eval("@GET(sthpw/login_in_group['login_group','senior_staff'].sthpw/login.email)");
                          from = server.eval("@SOBJECT(sthpw/login['login','" + user + "'])")[0];
                          from_email = from.email;
                          from_name = from.first_name + '.' + from.last_name;
                          message = 'Source Issue Alerts for ' + wo_code + ' (' + work_order.process + ')<br/>Elements:';
                          message_2 = 'Source Issue Alerts for ' + wo_code + ' (' + work_order.process + ')\\nElements:';
                          for(var r = 0; r < codes.length; r++){
                              code = codes[r];
                              message = message + '<br/>' + code + ' Type: ' + code_to_type[code] + '<br/>Path: ' + code_to_file[code] + '<br/>Description: ' + code_to_descript[code];  
                              message_2 = message_2 + '\\n' + code + ' Type: ' + code_to_type[code] + '\\nPath: ' + code_to_file[code] + '\\nDescription: ' + code_to_descript[code];  
                          } 
                          if(scheduler_email != ''){
                              group_emails.push(scheduler_email);
                          }
                          group_emails.push('matt.misenhimer@2gdigital.com');
                          all_ccs = group_emails.join('#Xs*');
                          applet = spt.Applet.get();
                          subject = '2G-SRC-ISSUE..(' + codes.length + '..Elements)..for..' + wo_code; 
                          filled_in_email = '/var/www/html/formatted_emails/source_issue_' + wo_code + '.html';
                          server.insert('twog/bundled_message', {'filled_in_path': filled_in_email, 'message': message, 'from_email': from_email, 'to_email': from_email, 'from_name': from_name, 'subject': subject, 'all_ccs': all_ccs, 'object_code': wo_code});
                          server.insert('sthpw/note', {'context': 'Source Issues', 'note': message_2}, {'parent_key': server.build_search_key('twog/proj', work_order.proj_code)});
                          spt.popup.close(spt.popup.get_popup(bvr.src_el));
                          alert('Alert(s) Sent');
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                          //alert(err);
                }
         ''' % (wo_code, user, platform)}
        return behavior

    def get_display(my):
        from tactic_client_lib import TacticServerStub
        work_order_code = ''
        user = ''
        sources = ''
        platform = ''
        colors = {'0': '#828282', '1': '#b8b8b8'}
        types = ['Internal','Client','Platform']
        if 'work_order_code' in my.kwargs.keys():
            work_order_code = str(my.kwargs.get('work_order_code'))
        if 'user' in my.kwargs.keys():
            user = str(my.kwargs.get('user'))
        if 'sources' in my.kwargs.keys():
            sources = my.kwargs.get('sources')
        if 'platform' in my.kwargs.keys():
            platform = my.kwargs.get('platform')
        delim1 = 'ZXuO#'
        delim2 = '|||'
        sources_arr = sources.split(delim1)
        widget = DivWdg()
        table = Table()
        table.add_attr('class','alert_popup_%s' % work_order_code)
        color_count = 0
        for source in sources_arr:
            entry_tbl = Table()
            if source != 'MISSING SOURCE':
                source_code, barcode, location = source.split(delim2);
            else:
                source_code = 'MISSING SOURCE' 
                barcode = 'MISSING SOURCE' 
                location = 'UNKNOWN' 
            row00 = entry_tbl.add_row()
            nw00 = entry_tbl.add_cell('<b>Issue Type for <u>%s</u>:</b> ' % barcode)
            nw00.add_attr('nowrap','nowrap')
            type_sel = SelectWdg('report_type_%s' % work_order_code) 
            for t in types:
                type_sel.append_option(t,t)
            type_sel.add_attr('code', source_code)
            type_sel.add_attr('name', barcode)
            nw0 = entry_tbl.add_cell(type_sel)
            nw0.add_attr('align','left')
            nw0.add_attr('width','100%s' % '%')
            row1 = entry_tbl.add_row()
            nw1 = entry_tbl.add_cell('<b>File Path for <u>%s</u> (if applicable)</b>' % barcode)
            nw1.add_attr('nowrap','nowrap')
            row2 = entry_tbl.add_row()
            nw11 = entry_tbl.add_cell('<textarea cols="45" rows="2" class="report_file_%s" code="%s" name="%s">%s</textarea>' % (work_order_code, source_code, barcode, location))
            row3 = entry_tbl.add_row()
            nw2 = entry_tbl.add_cell('<b>Description of Issue for <u>%s</u></b>' % barcode)
            nw2.add_attr('nowrap','nowrap')
            row4 = entry_tbl.add_row()
            nw21 = entry_tbl.add_cell('<textarea cols="45" rows="10" class="report_operator_description_%s" code="%s" name="%s"></textarea>' % (work_order_code, source_code, barcode))
            row1.add_style('background-color: %s;' % colors[str(color_count % 2)])
            row2.add_style('background-color: %s;' % colors[str(color_count % 2)])
            row3.add_style('background-color: %s;' % colors[str(color_count % 2)])
            row4.add_style('background-color: %s;' % colors[str(color_count % 2)])
            row00.add_style('background-color: %s;' % colors[str(color_count % 2)])
            nw1.add_attr('colspan','2')
            nw11.add_attr('colspan','2')
            nw2.add_attr('colspan','2')
            nw21.add_attr('colspan','2')
            color_count = color_count + 1
            table.add_row()
            table.add_cell(entry_tbl)            

        table.add_row()
        submit_cell = table.add_cell('<input type="button" value="Submit Alert(s)"/>')
        submit_cell.add_attr('align','center')
        submit_cell.add_behavior(my.alert_problems(work_order_code, user, platform))
        widget.add(table)
        return widget

