__all__ = ["AssetTrackerWdg","LocationInventoryWdg"]
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
                                          bc_num = 0;
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
                                          }else if((bc_num >= first_loc_num1 && bc_num <= last_loc_num1) || (bc_num >= first_loc_num2 && bc_num <= last_loc_num2) || bc.indexOf('LOC') != -1){
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
                              sources_fatal_error = false;
                              if(bcs.indexOf('2G') == -1){
                                  sources_fatal_error = true;
                                  if(errs == ''){
                                      errs = 'NO SOURCES SCANNED';
                                  }else{
                                      errs = errs + '<br/>NO SOURCES SCANNED';
                                  }
                              }
                              complete = false; 
                              if(!location_fatal_error && !person_fatal_error && !sources_fatal_error){
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
                                          server.insert('twog/location_tracker', {'person_barcode': person_bc, 'location_barcode': location_bc, 'source_barcode': bc, 'person_name': person.login, 'location_name': location1.name, 'source_name': 'UNKNOWN SOURCE'})
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
            csp1 = table.add_cell('<b><u>%s</b></u><br/>' % errors)
            csp1.add_attr('colspan','2')
            csp1.add_style('background-color: #FF0000;')
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
                if (bc_num >= first_loc_num1 and bc_num <= last_loc_num1) or (bc_num >= first_loc_num2 and bc_num <= last_loc_num2) or 'LOC' in bc:
                #if 'LOC' in bc:
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
                if not ((bc_num >= first_loc_num1 and bc_num <= last_loc_num1) or (bc_num >= first_loc_num2 and bc_num <= last_loc_num2) or 'LOC' in bc) and 'EMP' not in bc:
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
                celler = None
                if 'EMP' in bc:
                    celler = table.add_cell('<b>EMPLOYEE BARCODE:</b> ')
                elif 'LOC' in bc:
                    celler = table.add_cell('<b>LOCATION BARCODE:</b> ')
                elif '2G' in bc:
                    celler = table.add_cell('<b>SOURCE BARCODE:</b> ')
                else:
                    celler = table.add_cell('<b>UNKNOWN BARCODE:</b> ')
                celler.add_attr('nowrap','nowrap')
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


class LocationInventoryWdg(BaseTableElementWdg):

    def init(my):
        nothing = 'true'

    def get_entry_bvr(my):
        behavior = {'css_class': 'clickme', 'type': 'change', 'cbjs_action': '''        
                        try{
                          barcode = bvr.src_el.value;
                          server = TacticServerStub.get();
                          loca = server.eval("@SOBJECT(twog/inhouse_locations['barcode','" + barcode + "'])");
                          if(loca.length == 1){
                              top_el = spt.api.get_parent(bvr.src_el, '.location_inventory_wdg');
                              spt.app_busy.show("Retrieving inventory");
                              spt.api.load_panel(top_el, 'asset_tracker.LocationInventoryWdg', {'barcode': barcode});  
                              spt.app_busy.hide();
                          }else if(loca.length > 1){
                              alert("WARNING!!! There are more than 1 Locations in Tactic with this Barcode!");
                          }else{
                              alert("There Are No Locations With That Barcode");
                          }
                          spt.app_busy.hide();
                          
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         '''}
        return behavior

    def get_display(my):
        from pyasm.search import Search
        #from tactic_client_lib import TacticServerStub
        barcode = ''
        sources = []
        bad_sources = []
        if 'barcode' in my.kwargs.keys():
            barcode = my.kwargs.get('barcode')
            tracker_s = Search("twog/location_tracker")
            tracker_s.add_filter('location_barcode',barcode)
            trackers = tracker_s.get_sobjects()
            #print "BARCODE = %s" % barcode
            #print "LEN TRACKERS = %s" % len(trackers)
            for t in trackers:
                tdate = t.get('timestamp')
                source_barcode = t.get('source_barcode')
                other_tracks = Search("twog/location_tracker")
                other_tracks.add_filter('source_barcode',source_barcode)
                other_tracks.add_filter('timestamp',tdate, op=">")
                others = other_tracks.get_sobjects()
                if len(others) == 0:
                    source_s = Search("twog/source")
                    source_s.add_filter('barcode',source_barcode)
                    source = source_s.get_sobject()
                    if source:
                        if source.get_value('in_house') in [True,'true','True',1,'1']:
                            sources.append(source)
                    else:
                        bad_sources.append({'barcode': source_barcode, 'title': 'UNKNOWN SOURCE'})
        
        table = Table()
        table.add_attr('class','location_inventory_wdg')
        table.add_row()
        bc = TextWdg('nextbc')
        bc.add_attr('id', 'location_inventory_txtbox')
        bc.add_behavior(my.get_entry_bvr())
        bc.set_value(barcode)
        table.add_cell(bc)
        #print "LEN SOURCES = %s" % len(sources)
        if len(sources) > 0:
            table.add_row()
            table.add_cell("<b>TOTAL: %s (UNKNOWN: %s)</b>" % (len(sources), len(bad_sources)))
        for source in sources:
            table.add_row()
            table.add_cell('Barcode: %s, Code: %s, Name: %s: %s' % (source.get_value('barcode'), source.get_code(), source.get_value('title'), source.get_value('episode')))
        if len(bad_sources) > 0:
            table.add_row()
            table.add_cell("<b>UNKNOWN SOURCES</b>")
            for b in bad_sources:
                table.add_row()
                table.add_cell('Barcode: %s, Name: %s' % (b.get('barcode'), b.get('title')))
        widget = DivWdg()
        widget.add(table)
        return widget


















