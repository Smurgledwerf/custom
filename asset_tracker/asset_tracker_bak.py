__all__ = ["AssetTrackerWdg"]
import tacticenv
from pyasm.common import Environment
from pyasm.biz import *
from pyasm.web import Table, DivWdg
from pyasm.widget import TextWdg
from tactic.ui.common import BaseTableElementWdg
from tactic.ui.common import BaseRefreshWdg

class AssetTrackerWdg(BaseTableElementWdg):

    def init(my):
        nothing = 'true'

    def get_on_load_js(my, count):
        behavior =  {
            'type': 'load',
            'cbjs_action': '''
                count = '%s';
                document.getElementById('txt_' + count).focus();
            ''' % count
            } 
        return behavior        

    def get_entry_bvr(my, login):
        behavior = {'css_class': 'clickme', 'type': 'change', 'cbjs_action': '''        
                        try{
                          var login = '%s';
                          val = bvr.src_el.value.trim();
                          var top_el = spt.api.get_parent(bvr.src_el, '.tracker_' + login);
                          bcs = '';
                          inputs = top_el.getElementsByTagName('input');
                          person_count = 0;
                          location_count = 0;
                          person_bc = '';
                          location_bc = '';
                          person_error = '';
                          location_error = '';
                          source_barcodes = [];
                          first_loc_num1 = 5660;
                          last_loc_num1 = 5991;
                          first_loc_num2 = 6020;
                          last_loc_num2 = 6037;
                          for(var r = 0; r < inputs.length; r++){
                              if(inputs[r].id.indexOf('txt') != -1){
                                  bc = inputs[r].value.trim();
                                  if(bc.indexOf('DONE') == -1){
                                      keep_going = true;
                                      if(bcs == ''){
                                          bcs = bc
                                      }else if(bcs.indexOf(bc) == -1){
                                          bcs = bcs + ',' + bc;
                                      }else{
                                          keep_going = false;
                                      }
                                      if(keep_going){
                                          if(bc.indexOf('2G') != -1){
                                              bc_num = bc.replace('2G','').replace('A','').replace('B','').replace('C','').replace('V','');
                                              if(isNaN(bc_num)){
                                                  alert(bc + " is not a valid barcode");
                                              }else{
                                                  bc_num = Number(bc_num)
                                              }
                                          }
                                          if(bc.indexOf('EMP') != -1){
                                              person_count = person_count + 1;
                                              if(person_count > 1){
                                                  person_error = String(person_count) + " PEOPLE HAVE BEEN SCANNED. USING THE LAST ONE SCANNED."; 
                                              }
                                              person_bc = bc;
                                          }else if((bc_num >= first_loc_num1 && bc_num <= last_loc_num1) || (bc_num >= first_loc_num2 && bc_num <= last_loc_num2)){
                                              location_count = location_count + 1;
                                              if(location_count > 1){
                                                  location_error = String(location_count) + " LOCATIONS HAVE BEEN SCANNED. USING THE LAST ONE SCANNED."; 
                                              }
                                              location_bc = bc;
                                          }else{
                                              source_barcodes.push(bc);
                                          }
                                      }
                                  }
                              }    
                          }
                          errs = person_error;
                          if(errs == ''){
                              errs = location_error;
                          }else if(location_error != ''){
                              errs = errs + '<br/>' + location_error;
                          }
                          if(val == 'DONE'){
                              var server = TacticServerStub.get();
                              // Here need to insert into db
                              person = server.eval("@SOBJECT(sthpw/login['barcode','" + person_bc + "'])");
                              person_fatal_error = false;
                              if(person.length > 0){
                                  person = person[0]
                              }else{
                                  person_fatal_error = true;
                                  if(errs == ''){
                                      errs = 'PERSON WITH BARCODE: "' + person_bc + '" NOT FOUND. CANNOT COMMIT CHANGES.';
                                  }else{
                                      errs = errs + '<br/>PERSON WITH BARCODE: "' + person_bc + '" NOT FOUND. CANNOT COMMIT CHANGES.';
                                  }
                              }
                              location_expr = "@SOBJECT(twog/inhouse_locations['barcode','" + location_bc + "'])";
                              location1 = server.eval(location_expr);
                              location_fatal_error = false;
                              if(location1.length > 0){
                                  location1 = location1[0]
                              }else{
                                  location_fatal_error = true;
                                  if(errs == ''){
                                      errs = 'LOCATION WITH BARCODE: "' + location_bc + '" NOT FOUND. CANNOT COMMIT CHANGES.';
                                  }else{
                                      errs = errs + '<br/>LOCATION WITH BARCODE: "' + location_bc + '" NOT FOUND. CANNOT COMMIT CHANGES.';
                                  }
                              }
                              complete = false; 
                              if(!location_fatal_error && !person_fatal_error){
                                  complete = true;
                                  for(var r = 0; r < source_barcodes.length; r++){
                                      bc = source_barcodes[r];
                                      source = server.eval("@SOBJECT(twog/source['barcode','" + bc + "'])");
                                      if(source.length > 0){
                                          source = source[0];
                                          fullname = source.title;
                                          if(source.episode != ''){
                                              fullname = fullname + " Ep: " + source.episode;
                                          }
                                          if(source.season != ''){
                                              fullname = fullname + " Season: " + source.season;
                                          }
                                          if(source.part != ''){
                                              fullname = fullname + " Part: " + source.part;
                                          }
                                          server.insert('twog/location_tracker', {'person_barcode': person_bc, 'location_barcode': location_bc, 'source_barcode': bc, 'person_name': person.login, 'location_name': location1.name, 'source_name': fullname})
                                      }else{
                                          server.insert('twog/location_tracker', {'person_barcode': person_bc, 'location_barcode': location_bc, 'source_barcode': bc, 'person_name': person.login, 'location_name': location1.name, 'source_name': 'UKNOWN SOURCE'})
                                      }
                                  } 
                              }
                              spt.api.load_panel(top_el, 'asset_tracker.AssetTrackerWdg', {'complete': complete, 'barcodes': bcs, 'errors': errs}); 
                          }else{
                              spt.api.load_panel(top_el, 'asset_tracker.AssetTrackerWdg', {'complete': false, 'barcodes': bcs, 'errors': errs}); 
                          }
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         ''' % (login)}
        return behavior

    def get_display(my):
        from tactic_client_lib import TacticServerStub
        login = Environment.get_login()
        user_name = login.get_login()
        user_name = user_name.replace('.','')
        barcodes = []
        complete = False
        errors = ''
        first_loc_num1 = 5660
        last_loc_num1 = 5991
        first_loc_num2 = 6020
        last_loc_num2 = 6037
        if 'barcodes' in my.kwargs.keys():
            barcodes = my.kwargs.get('barcodes').split(',') 
        if 'complete' in my.kwargs.keys():
            complete = my.kwargs.get('complete')
        if 'errors' in my.kwargs.keys():
            errors = my.kwargs.get('errors')
        table = Table()
        table.add_attr('id','tracker_%s' % user_name) 
        table.add_attr('class','tracker_%s' % user_name) 
        if errors not in [None,'']:
            table.add_row()
            csp1 = table.add_cell(errors)
            csp1.add_attr('colspan','2')
        count = 0
        if complete:
            server = TacticServerStub.get()
            t2 = Table()
            for bc in barcodes:
                if 'EMP' in bc:
                    that_user = server.eval("@SOBJECT(sthpw/login['barcode','%s'])" % bc)
                    if that_user:
                        that_user = that_user[0]
                    else:
                        that_user = {'login': 'UNKNOWN USER'}
                    t2.add_row()
                    t2.add_cell('USER: ')
                    t2.add_cell(that_user.get('login'))
                    t2.add_cell('BARCODE: %s' % bc)
            for bc in barcodes:
                bc_num = 555555555
                if '2G' in bc:
                    bc_num = bc.replace('2G','').replace('A','').replace('B','').replace('C','').replace('V','')
                    bc_num = int(bc_num)
                if (bc_num >= first_loc_num1 and bc_num <= last_loc_num1) or (bc_num >= first_loc_num2 and bc_num <= last_loc_num2):
                    that_location = server.eval("@SOBJECT(twog/inhouse_locations['barcode','%s'])" % bc)
                    if that_location:
                        that_location = that_location[0]
                    else:
                        that_location = {'name': 'UNKNOWN LOCATION'}
                    t2.add_row()
                    t2.add_cell('LOCATION: ')
                    t2.add_cell(that_location.get('name'))
                    t2.add_cell('BARCODE: %s' % bc)
            for bc in barcodes:
                bc_num = 555555555
                if '2G' in bc:
                    bc_num = bc.replace('2G','').replace('A','').replace('B','').replace('C','').replace('V','')
                    bc_num = int(bc_num)
                #if 'LOC' not in bc and 'EMP' not in bc:
                if not ((bc_num >= first_loc_num1 and bc_num <= last_loc_num1) or (bc_num >= first_loc_num2 and bc_num <= last_loc_num2)) and 'EMP' not in bc:
                    that_src = server.eval("@SOBJECT(twog/source['barcode','%s'])" % bc)
                    if that_src:
                        that_src = that_src[0]
                    else:
                        that_src = {'title': 'UNKNOWN SOURCE', 'episode': '', 'season': '', 'part': ''}
                    full_name = that_src.get('title')
                    if that_src.get('episode') not in [None,'']:
                        full_name = '%s EPISODE: %s' % (full_name, that_src.get('episode'))
                    if that_src.get('season') not in [None,'']:
                        full_name = '%s SEASON: %s' % (full_name, that_src.get('season'))
                    if that_src.get('part') not in [None,'']: 
                        full_name = '%s PART: %s' % (full_name, that_src.get('part'))
                    t2.add_row()
                    t2.add_cell('SOURCE: ')
                    t2.add_cell(full_name)
                    t2.add_cell('BARCODE: %s' % bc)
            table.add_row()
            csp2 = table.add_cell(t2)
            csp2.add_attr('colspan','2')
        else:                
            for bc in barcodes:
                table.add_row()
                table.add_cell('BARCODE: ')
                oldtxt = TextWdg('oldtxt')
                oldtxt.set_attr('id', 'txt_%s' % count)
                oldtxt.set_value(bc)
                table.add_cell(oldtxt)
                count = count + 1
            
        table.add_row()
        nextbc = TextWdg('nextbc')
        nextbc.add_attr('id', 'txt_%s' % count)
        nextbc.add_behavior(my.get_entry_bvr(user_name))
        table.add_cell('Barcode: ')
        table.add_cell(nextbc)

        widget = DivWdg()
        widget.add(table)
        widget.add_behavior(my.get_on_load_js(count))
        return widget


