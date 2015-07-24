__all__ = ["IndieBigBoardSelectWdg","BigBoardSingleWOSelectWdg","BigBoardViewWdg","BigBoardSelectWdg","BigBoardWOSelectWdg","BigBoardWdg"]
import tacticenv
import time, datetime
#from pyasm.common import Environment
#from pyasm.biz import *
from pyasm.web import Table, DivWdg
from tactic.ui.common import BaseTableElementWdg
from tactic.ui.common import BaseRefreshWdg
#from pyasm.search import Search
#from tactic.ui.widget import DiscussionWdg
#from operator import itemgetter

class IndieBigBoardSelectWdg(BaseTableElementWdg):

    def init(my):
        nothing = 'true'
        my.server = None

    def get_stub(my):
        from tactic_client_lib import TacticServerStub
        my.server = TacticServerStub.get()
    
    def get_launch_behavior(my, search_key, title_code, lookup_code):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{ 
                          var server = TacticServerStub.get();
                          var search_key = "%s";
                          var title_code = "%s";
                          var lookup_code = "%s";
                          var task_code = search_key.split('code=')[1];
                          var state = bvr.src_el.get('state');
                          var checked = '/context/icons/custom/small_blue_racecar_alpha.png';
                          var unchecked = '/context/icons/custom/small_grey_racecar_alpha.png';
                          changed = false
                          if(state == 'checked'){
                              if(confirm("Do you really want to take this off the Hot Today Board?")){
                                  img = unchecked;
                                  server.update(search_key, {'indie_bigboard': 'false'}); 
                                  indies = server.eval("@SOBJECT(twog/indie_bigboard['task_code','" + task_code + "']['indie_bigboard','true'])");
                                  for(var r = 0; r < indies.length; r++){
                                      server.update(indies[r].__search_key__, {'indie_bigboard': 'false'});
                                  }
                                  bvr.src_el.setAttribute('state', 'unchecked');
                                  changed = true
                              }
                          }else{
                              new_prio = prompt("Please assign a priority to this Work Order");
                              if(new_prio != null && new_prio != ''){
                                  if(!(isNaN(new_prio))){
                                      img = checked; 
                                      new_prio = Number(new_prio);
                                      server.update(search_key, {'indie_bigboard': 'true', 'indie_priority': new_prio}); 
                                      server.insert('twog/indie_bigboard', {'indie_bigboard': 'true', 'indie_priority': new_prio, 'title_code': title_code, 'lookup_code': lookup_code, 'task_code': task_code}); 
                                      title = server.eval("@SOBJECT(twog/title['code','" + title_code + "'])")[0];
                                      title_sk = title.__search_key__;
                                      task = server.eval("@SOBJECT(sthpw/task['code','" + task_code + "'])")[0];
                                      asl = task.assigned_login_group;
                                      adps = title.active_dept_priorities;
                                      asl_prio = asl.replace(' ','_') + '_priority';
                                      data_out = {}
                                      data_out[asl_prio] = new_prio; 
                                      if(adps.indexOf(asl) == -1){
                                          if(adps == ''){
                                              adps = asl;
                                          }else{
                                              adps = adps + ',' + asl;
                                          }
                                          data_out['active_dept_priorities'] = adps;
                                      }
                                      server.update(title_sk, data_out);
                                      bvr.src_el.setAttribute('state', 'checked');
                                      changed = true;
                                  }else{
                                      alert(new_prio + " is not a number. Work Order not placed on Hot Today.");
                                  }
                              }
                          } 
                          if(changed){
                              var inner = bvr.src_el.innerHTML;
                              in1 = inner.split('src="')[0];
                              in1 = in1 + 'src="' + img + '"/>';
                              bvr.src_el.innerHTML = in1;
                          }
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         ''' % (search_key, title_code, lookup_code)}
        return behavior

    def get_display(my):
        is_on = False
        search_key = my.kwargs.get('search_key')
        task_code = search_key.split('code=')[1]
        title_code = my.kwargs.get('title_code')
        lookup_code = my.kwargs.get('lookup_code')
        if 'indie_bigboard' in my.kwargs.keys():
            if my.kwargs.get('indie_bigboard') in [True,'true','t','T',1]:
                is_on = True
        else:
            my.get_stub()
            task = my.server.eval("@SOBJECT(sthpw/task['code','%s'])" % task_code)[0]
            if task.get('indie_bigboard') in [True,'true','t','T',1]:
                is_on = True

        widget = DivWdg()
        table = Table()

        img = '/context/icons/custom/small_grey_racecar_alpha.png'
        state = 'unchecked'
        if is_on:
            img = '/context/icons/custom/small_blue_racecar_alpha.png'
            state = 'checked'
        table.add_row()
        cell1 = table.add_cell('<img border="0" style="vertical-align: middle" title="" src="%s">' % img)
        cell1.add_attr('search_key', search_key)
        cell1.add_attr('state',state)
        launch_behavior = my.get_launch_behavior(search_key, title_code, lookup_code)
        cell1.add_style('cursor: pointer;')
        cell1.add_behavior(launch_behavior)
        widget.add(table)
        return widget

class BigBoardSingleWOSelectWdg(BaseTableElementWdg):

    def init(my):
        nothing = 'true'
        my.server = None

    def get_stub(my):
        from tactic_client_lib import TacticServerStub
        my.server = TacticServerStub.get()

    def get_launch_behavior(my, search_key, title_code, lookup_code):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{ 
                          var server = TacticServerStub.get();
                          var search_key = "%s";
                          var title_code = "%s";
                          var lookup_code = "%s";
                          var task_code = search_key.split('code=')[1];
                          var state = bvr.src_el.get('state');
                          var checked = '/context/icons/silk/rosette.png';
                          var unchecked = '/context/icons/silk/rosette_grey.png';
                          changed = false
                          if(state == 'checked'){
                              if(confirm("Do you really want to take this off the Hot Today Board?")){
                                  img = unchecked;
                                  server.update(search_key, {'bigboard': 'false'}); 
                                  bvr.src_el.setAttribute('state', 'unchecked');
                                  changed = true
                              }
                          }else{
                              img = checked; 
                              server.update(search_key, {'bigboard': 'true'}); 
                              bvr.src_el.setAttribute('state', 'checked');
                              changed = true;
                              title = server.eval("@SOBJECT(twog/title['code','" + title_code + "'])")[0];
                              if(!(title.bigboard)){
                                  alert('Placing the Title on the BigBoard as well.');
                                  server.update(title.__search_key__, {'bigboard': 'true'});
                                  tc_str = 'title_bigboard_' + title_code;
                                  title_bbs = document.getElementById(tc_str);
                                  if(title_bbs){
                                      title_bb_inner = title_bbs.innerHTML;
                                      in1 = title_bb_inner.split('src="')[0];
                                      in1 = in1 + 'src="' + img + '"/>';
                                      title_bbs.innerHTML = in1;
                                      title_bbs.setAttribute('state','checked');
                                  }
                              }
                          } 
                          if(changed){
                              var inner = bvr.src_el.innerHTML;
                              in1 = inner.split('src="')[0];
                              in1 = in1 + 'src="' + img + '"/>';
                              bvr.src_el.innerHTML = in1;
                          }
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         ''' % (search_key, title_code, lookup_code)}
        return behavior
    
    def get_display(my):
        is_on = False
        search_key = my.kwargs.get('search_key')
        task_code = search_key.split('code=')[1]
        title_code = my.kwargs.get('title_code')
        lookup_code = my.kwargs.get('lookup_code')
        if 'bigboard' in my.kwargs.keys():
            if my.kwargs.get('bigboard') in [True,'true','t','T',1]:
                is_on = True
        else:
            my.get_stub()
            task = my.server.eval("@SOBJECT(sthpw/task['code','%s'])" % task_code)[0]
            if task.get('bigboard') in [True,'true','t','T',1]:
                is_on = True

        widget = DivWdg()
        table = Table()

        img = '/context/icons/silk/rosette_grey.png'
        state = 'unchecked'
        if is_on:
            img = '/context/icons/silk/rosette.png'
            state = 'checked'
        table.add_row()
        cell1 = table.add_cell('<img border="0" style="vertical-align: middle" title="" src="%s">' % img)
        cell1.add_attr('search_key', search_key)
        cell1.add_attr('state',state)
        launch_behavior = my.get_launch_behavior(search_key, title_code, lookup_code)
        cell1.add_style('cursor: pointer;')
        cell1.add_behavior(launch_behavior)
        widget.add(table)
        return widget

class BigBoardViewWdg(BaseTableElementWdg):

    def init(my):
        nothing = 'true'

    def get_display(my):
        sobject = my.get_current_sobject()
        code = sobject.get_code()
        widget = DivWdg()
        table = Table()
        bigboard = sobject.get_value('bigboard')
        img = '/context/icons/silk/rosette_grey.png'
        if bigboard == True:
            img = '/context/icons/silk/rosette.png'
        table.add_row()
        cell1 =  table.add_cell('<img border="0" style="vertical-align: middle" title="" src="%s">' % img)
        widget.add(table)
        return widget

class BigBoardSelectWdg(BaseTableElementWdg):

    def init(my):
        nothing = 'true'
        my.server = None

    def get_stub(my):
        from tactic_client_lib import TacticServerStub
        my.server = TacticServerStub.get()
    
    def get_launch_behavior(my, title_name, in_bigboard):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{ 
                          var server = TacticServerStub.get();
                          var title_name = "%s";
                          var in_bigboard = "%s";
                          var my_sk = bvr.src_el.get('sk');
                          var state = bvr.src_el.get('state');
                          var class_name = 'nighttime_hotlist.nighttime_hotlist.BigBoardWOSelectWdg';
                          var checked = '/context/icons/silk/rosette.png';
                          var unchecked = '/context/icons/silk/rosette_grey.png';
                          nothing_else = false;
                          changed = false
                          if(state == 'checked'){
                              img = unchecked;
                              if(in_bigboard != 'Yep'){
                                  if(confirm("Do you really want to take this off the Hot Today list?")){
                                      server.update(my_sk, {'bigboard': 'false'}); 
                                      bvr.src_el.setAttribute('state', 'unchecked');
                                      changed = true;
                                  }
                              }else{
                                  if(confirm("Do you really want to take this off the Hot Today list?")){
                                      server.update(my_sk, {'bigboard': 'false'}); 
                                      changed = true;
                                      var buttons_el = document.getElementsByClassName('auto_buttons')[0]; 
                                      auto_el = buttons_el.getElementById('auto_refresh');
                                      auto = auto_el.getAttribute('auto');
                                      scroll_el = buttons_el.getElementById('scroll_el');
                                      scroll = scroll_el.getAttribute('scroll');
                                      group_el = buttons_el.getElementById('group_select');
                                      group = group_el.value;
                                      board_els = document.getElementsByClassName('bigboard');     
                                      nothing_else = true;
                                      spt.app_busy.show("Refreshing...");
                                      spt.api.load_panel(board_els[0], 'nighttime_hotlist.BigBoardWdg', {'auto_refresh': auto, 'auto_scroll': scroll, 'groups': group});
                                      spt.app_busy.hide();
                                  }
                              }
                          }else{
                              img = checked; 
                              server.update(my_sk, {'bigboard': 'true'}); 
                              bvr.src_el.setAttribute('state', 'checked');
                              kwargs = {
                                           'sk': my_sk
                                   };
                              spt.panel.load_popup('Select Big Board Work Orders for ' + title_name, class_name, kwargs);
                              changed = true;
                          } 
                          if(!nothing_else && changed){
                              var inner = bvr.src_el.innerHTML;
                              in1 = inner.split('src="')[0];
                              in1 = in1 + 'src="' + img + '"/>';
                              bvr.src_el.innerHTML = in1;
                          }
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         ''' % (title_name, in_bigboard)}
        return behavior

    def get_display(my):
        expression_lookup = {'twog/title': "@SOBJECT(twog/title['code','REPLACE_ME'])", 'twog/proj': "@SOBJECT(twog/proj['code','REPLACE_ME'].twog/title)", 'twog/work_order': "@SOBJECT(twog/work_order['code','REPLACE_ME'].twog/proj.twog/title)", 'twog/equipment_used': "@SOBJECT(twog/equipment_used['code','REPLACE_ME'].twog/work_order.twog/proj.twog/title)"}
        search_type = 'twog/title'
        code = ''
        order_name = ''
        sob_sk = ''
        not_title = True
        bad_code = False
        if 'search_type' in my.kwargs.keys():
            my.get_stub()
            search_type = str(my.kwargs.get('search_type'))
            code = str(my.kwargs.get('code'))
            sobject = my.server.eval(expression_lookup[search_type].replace('REPLACE_ME',code))
            if sobject:
                sobject = sobject[0]
                code = sobject.get('code')
                sob_sk = sobject.get('__search_key__')
        else: 
            sobject = my.get_current_sobject()
            sob_sk = sobject.get_search_key()
            code = sobject.get_code()
            not_title = False
            if 'TITLE' not in code:
                not_title = True
                my.get_stub()
                if 'WORK_ORDER' in code:
                    sobject = my.server.eval(expression_lookup['twog/work_order'].replace('REPLACE_ME',code))
                elif 'EQUIPMENT_USED' in code:
                    sobject = my.server.eval(expression_lookup['twog/equipment_used'].replace('REPLACE_ME',code))
                elif 'PROJ' in code:
                    sobject = my.server.eval(expression_lookup['twog/proj'].replace('REPLACE_ME',code))
                try:
                    if sobject:
                        sobject = sobject[0]
                        code = sobject.get('code')
                        sob_sk = sobject.get('__search_key__')
                except:
                    bad_code = True
                    pass
        widget = DivWdg()
        table = Table()
        if not bad_code:
            in_bigboard = 'Nope'
            if 'in_bigboard' in my.kwargs.keys():
                if my.kwargs.get('in_bigboard') in ['Yes','yes','true','True']:
                    in_bigboard = 'Yep' 
            img = '/context/icons/silk/rosette_grey.png'
            state = 'unchecked'
            bigboard = ''
            title_name = ''
            episode = ''
            if not not_title:
                bigboard = sobject.get_value('bigboard')
                title_name = sobject.get_value('title')
                episode = sobject.get_value('episode')
            else:
                bigboard = sobject.get('bigboard')
                title_name = sobject.get('title')
                episode = sobject.get('episode')
            if episode not in [None,'']:
                title_name = '%s Episode: %s' % (title_name, episode) 
            if bigboard == True:
                img = '/context/icons/silk/rosette.png'
                state = 'checked'
            #table.add_attr('width', '50px')
            table.add_row()
            cell1 =  table.add_cell('<img border="0" style="vertical-align: middle" title="" src="%s">' % img)
            cell1.add_attr('id', 'title_bigboard_%s' % code)
            cell1.add_attr('sk', sob_sk)
            cell1.add_attr('state',state)
            launch_behavior = my.get_launch_behavior(title_name, in_bigboard)
            cell1.add_style('cursor: pointer;')
            cell1.add_behavior(launch_behavior)
        widget.add(table)
        return widget

class BigBoardWOSelectWdg(BaseRefreshWdg):
    def init(my):
        #from client.tactic_client_lib import TacticServerStub
        #from pyasm.common import Environment
        #from pyasm.search import Search
        #my.server = TacticServerStub.get()
        #my.login = Environment.get_login()
        #my.user = my.login.get_login()
        my.sk = ''

    def get_switcher_behavior(my, title_sk):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{ 
                          var title_sk = '%s';
                          var top_el = document.getElementsByClassName('bigboard_wo_selector_' + title_sk)[0];
                          var checkboxes = top_el.getElementsByTagName('input');
                          inner = bvr.src_el.innerHTML;
                          doing = inner.split('value="')[1];
                          doing = doing.split('"')[0];
                          for(var r = 0; r < checkboxes.length; r++){
                              if(checkboxes[r].type == 'checkbox'){
                                  if(doing == 'Select All'){
                                      checkboxes[r].checked = true;
                                  }else{
                                      checkboxes[r].checked = false;
                                  }
                              }
                          }
                          if(doing == 'Select All'){
                              bvr.src_el.innerHTML = '<input type="button" value="Deselect All"/>';
                          }else{
                              bvr.src_el.innerHTML = '<input type="button" value="Select All"/>';
                          }
                          
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                          //alert(err);
                }
         ''' % title_sk}
        return behavior

    def get_bigboardem_behavior(my, title_sk):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{ 
                          var server = TacticServerStub.get();
                          var title_sk = '%s';
                          var top_el = document.getElementsByClassName('bigboard_wo_selector_' + title_sk)[0];
                          var checkboxes = top_el.getElementsByTagName('input');
                          for(var r = 0; r < checkboxes.length; r++){
                              if(checkboxes[r].type == 'checkbox'){
                                  task_sk = checkboxes[r].getAttribute('sk');
                                  cname = checkboxes[r].name;
                                  if(cname.indexOf('bigboard_wo_select_') != -1){
                                      if(checkboxes[r].checked){
                                          server.update(task_sk, {'bigboard': 'true'});
                                      }else{
                                          server.update(task_sk, {'bigboard': 'false'});
                                      }
                                  }
                               }
                          }
                          //alert('Done adding to the BigBoard');
                          spt.popup.close(spt.popup.get_popup(bvr.src_el));
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                          //alert(err);
                }
         ''' % title_sk}
        return behavior
    
    def get_display(my):   
        #THE SEARCH KEY BEING PASSED IN SHOULD BELONG TO A TITLE
        from pyasm.search import Search
        from pyasm.widget import CheckboxWdg
        my.sk = str(my.kwargs.get('sk'))
        code = my.sk.split('code=')[1]
        #tasks = my.server.eval("@SOBJECT(sthpw/task['title_code','%s']['search_type','twog/proj?project=twog']['status','!=','Completed']['active','1'])" % code)
        search = Search("sthpw/task")
        search.add_filter('title_code',code)
        search.add_filter('status', 'Completed', op="!=")
        search.add_filter('active','1')
        search.add_filter('search_type','twog/proj?project=twog')
        tasks = search.get_sobjects()
        
        table = Table()
        if len(tasks) > 0:
            table.add_row()
            switcher = table.add_cell('<input type="button" value="Select All"/>')
            switcher.add_behavior(my.get_switcher_behavior(my.sk))
            for task in tasks:
                table.add_row()
                #checkbox = CheckboxWdg('bigboard_wo_select_%s' % task.get('__search_key__'))
                checkbox = CheckboxWdg('bigboard_wo_select_%s' % task.get_search_key())
                checkbox.set_persistence()
                #if task.get('bigboard'):
                if task.get_value('bigboard'):
                    checkbox.set_value(True) 
                else:
                    checkbox.set_value(False) 
                #checkbox.add_attr('sk',task.get('__search_key__'))
                checkbox.add_attr('sk',task.get_search_key())
                table.add_cell(checkbox)
                #assigned_login_group = task.get('assigned_login_group')
                assigned_login_group = task.get_value('assigned_login_group')
                #assigned = task.get('assigned')
                assigned = task.get_value('assigned')
                if assigned_login_group in [None,'']:
                    assigned_login_group = 'No Group?'
                if assigned in [None,'']:
                    assigned = 'Unassigned'
                #t1 = table.add_cell('[%s]: %s, %s, %s, %s' % (task.get('lookup_code'), task.get('process'), assigned_login_group, assigned, task.get('status')))
                t1 = table.add_cell('[%s]: %s, %s, %s, %s' % (task.get_value('lookup_code'), task.get_value('process'), assigned_login_group, assigned, task.get_value('status')))
                t1.add_attr('nowrap','nowrap')
        cover_table = Table()
        cover_table.add_attr('class','bigboard_wo_selector_%s' % my.sk)
        cover_table.add_row()
        cover_cell = cover_table.add_cell(table)
        cover_table.add_row()
        buttont = Table()
        buttont.add_row()
        c1 = buttont.add_cell(' ')
        c1.add_attr('width','40%s' % '%')
        button = buttont.add_cell('<input type="button" value="BigBoard Selected Work Orders"/>')
        button.add_behavior(my.get_bigboardem_behavior(my.sk)) 
        c2 = buttont.add_cell(' ')
        c2.add_attr('width','40%s' % '%')
        cover_table.add_cell(buttont)
        return cover_table

class BigBoardWdg(BaseRefreshWdg):
    def init(my):
        from pyasm.common import Environment
        my.login = Environment.get_login()
        my.user = my.login.get_login()
        my.sk = ''
        my.seen_groups = []
        my.bigdict = {}
        my.indi_pct = 0.0
        my.stat_colors = {'Pending':'#d7d7d7','In Progress':'#f5f3a4','In_Progress':'#f5f3a4','On Hold':'#e8b2b8','On_Hold':'#e8b2b8','Client Response': '#ddd5b8', 'Completed':'#b7e0a5','Need Buddy Check':'#e3701a','Ready':'#b2cee8','Internal Rejection':'#ff0000','External Rejection':'#ff0000','Fix Needed':'#c466a1','Failed QC':'#ff0000','Rejected': '#ff0000','DR In_Progress': '#d6e0a4', 'BATON In_Progress': '#c6e0a4', 'Export In_Progress': '#796999', 'Buddy Check In_Progress': '#1aade3'}
        my.stat_relevance = {'Pending': 0,'In Progress': 4,'In_Progress': 4,'On Hold': 1,'On_Hold': 1,'Client Response': 2, 'Completed': -1,'Need Buddy Check': 8, 'Buddy Check In_Progress': 9, 'Ready': 3,'Internal Rejection': 10,'External Rejection': 11,'Failed QC': 12,'Fix Needed': 14,'Rejected': 13,'DR In_Progress': 5, 'BATON In_Progress': 6, 'Export In_Progress': 7}
        my.timestamp = my.make_timestamp()
        my.date = my.timestamp.split(' ')[0]
        my.real_date = datetime.datetime.strptime(my.date, '%Y-%m-%d')
        my.all_groups = []
        my.big_user = False

    def make_timestamp(my):
        import datetime
        now = datetime.datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S")
        
    def trow_top(my):
        table = Table()
        table.add_attr('width','100%s' % '%')
        table.add_attr('border','2')
        table.add_style('font-size: 16px;')
        table.add_style('font-family: Helvetica;')
        #table.add_style('color: #FFFFFF;')
        table.add_style('color: #000000;')
        table.add_style('background-color: #f2f2f2;')
        #table.add_style('background-color: #000000;')
        table.add_class('spt_group_row')
        table.add_row()
        tcol = table.add_cell('<b>TITLE</b>')
        tpct = (my.indi_pct * 2)
        tcol.add_attr('width','%s%s' % (tpct, '%'))
        for sg in my.seen_groups:
            sgcol = table.add_cell('<b>%s</b>' % sg.upper())
            sgcol.add_attr('width','%s%s' % ((my.indi_pct), '%'))
        t2 = Table()
        t2.add_attr('width','100%s' % '%')
        t2.add_attr('border','2')
        t2.add_style('font-size: 16px;')
        t2.add_style('font-family: Helvetica;')
        t2.add_style('color: #000000;')
        t2.add_style('background-color: #f2f2f2;')
        t2.add_row()
        t2.add_cell(table)
        t2c = t2.add_cell('&nbsp;&nbsp;&nbsp;&nbsp;')
        t2c.add_attr('width','10px')
       
        return t2

    def get_launch_note_behavior(my, sk, name):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                          var sk = '%s';
                          var name = '%s';
                          kwargs =  {'search_key': sk, 'append_process': 'Client Services,Redelivery/Rejection Request,Redelivery/Rejection Completed', 'treedown': 'treedown', 'chronological': true};
                          spt.panel.load_popup('Notes for ' + name, 'tactic.ui.widget.DiscussionWdg', kwargs);
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                          //alert(err);
                }
         ''' % (sk, name)}
        return behavior

    def shorten_text(my, text, max_len):
        ret_val = text
        if len(text) > max_len - 3 :
            ret_val = '%s...' % text[:max_len -3]
        return ret_val

    def fix_date(my, date):
        #This is needed due to the way Tactic deals with dates (using timezone info), post v4.0
        from pyasm.common import SPTDate
        return_date = ''
        date_obj = SPTDate.convert_to_local(date)
        if date_obj not in [None,'']:
            return_date = date_obj.strftime("%Y-%m-%d  %H:%M")
        return return_date

    def wrow(my, task, expected_delivery_date, count):
        from order_builder.order_builder import OrderBuilderLauncherWdg
        from order_builder.taskobjlauncher import TaskObjLauncherWdg
        expected_delivery_date = my.fix_date(expected_delivery_date)
        code = task.get_value('code')
        name = task.get_value('title')
        episode = task.get_value('episode')
        if episode not in [None,'']:
            name = '%s Episode %s' % (name, episode)
        tdue_date = expected_delivery_date.split(' ')[0]
        ddreal_date = ''
        better_lookin_dd = 'NO DELIVERY DATE'
        dd_color = '#FFFFFF'
        if tdue_date not in [None,'']:
            ddreal_date = datetime.datetime.strptime(tdue_date, '%Y-%m-%d')
            if ddreal_date == my.real_date:
                dd_color = "#FFFF00"
            elif ddreal_date < my.real_date:
                dd_color = "#FF0000"
            else:
                dd_color = "#66CD00"
            tdds = tdue_date.split('-')
            tyear = ''
            tmonth = ''
            tday = ''
            if len(tdds) == 3:
                tyear = tdds[0]
                tmonth = tdds[1]
                tday = tdds[2]
            better_lookin_dd = '%s/%s/%s' % (tmonth, tday, tyear)
            if better_lookin_dd == '//':
                better_lookin_dd = 'NO DELIVERY DATE'
        tpct = my.indi_pct * 2
        table = Table()
        table.add_attr('width','100%s' % '%')
        table.add_attr('border','2')
        table.add_style('color: #000000;')
        table.add_style('font-family: Helvetica;')
        table.add_row()
        dbl = Table()
        dbl.add_attr('width','100%s' % '%')
        dbl.add_style('font-size: 16px;')
        dbl.add_style('color: #000000;')
        dbl.add_row()
        d1 = dbl.add_cell('<b><font style="size: 36px; color: #ff0000;">%s.</font> <u>%s</u></b>' % (count, name))
        d1.add_attr('width','100%s' % '%')
        dbl.add_row()
        lil_tbl = Table()
        lil_tbl.add_attr('cellpadding','5')
        lil_tbl.set_style('color: #000000; font-size: 14px;')
        lil_tbl.add_row()
        lil_tbl.add_cell(code)
        lil_tbl.add_cell("<i>Platform: %s</i>" % task.get_value('platform'))
        lil_tbl.add_cell("<b>Client: %s</b>" % task.get_value('client_name'))
        lil_tbl.add_row()
        obt = Table()
        obt.add_attr('cellpadding','5')
        obt.set_style('color: #000000; font-size: 14px;')
        obt.add_row()
        delb = obt.add_cell('<font color="%s"><b>Deliver By: %s</b></font>' % (dd_color, better_lookin_dd)) 
        delb.add_attr('colspan','2')
        delb.add_attr('nowrap','nowrap')
        ob = OrderBuilderLauncherWdg(code=task.get_value('order_code'))
        obt.add_attr('width','260px')
        obt.add_cell(ob)
        notes = obt.add_cell('<img src="/context/icons/silk/note_add.png"/>')
        notes.add_style('cursor: pointer;')
        tsearch = Search('twog/title')
        tsearch.add_filter('code',task.get_value('title_code'))
        task_tit = tsearch.get_sobject()
        notes.add_behavior(my.get_launch_note_behavior(task_tit.get_search_key(),name)) 
        lil_tbl.add_cell(obt)  
        if task_tit.get_value('no_charge') and task_tit.get_value('redo'):
            lil_tbl.add_row()
            lil_tbl.add_cell('<font color="#FF0000"><b>REDO - NO CHARGE</b></font>')
        d2 = dbl.add_cell(lil_tbl)
        d2.add_attr('width','100%s' % '%')
        if my.big_user:
            dbl.add_row()
            offbutt = IndieBigBoardSelectWdg(search_key=task.get_search_key(),title_code=task.get_value('title_code'),lookup_code=task.get_value('lookup_code'),indie_bigboard=task.get_value('indie_bigboard'))
            dblbb = dbl.add_cell(offbutt)
            dblbb.add_attr('width','20px')
            dblpr = dbl.add_cell('Priority: %s' % task.get_value('indie_priority'))
            dblpr.add_attr('align','left')
            prioid = 'prio_%s' % count
        else: 
            dbl.add_row()
            dbl4 = dbl.add_cell('Priority: %s' % task.get_value('priority'))
            dbl4.add_attr('align','left')
            prioid = 'prio_%s' % count
        titl = table.add_cell(dbl)
        titl.add_attr('valign','top')
        titl.add_attr('width','%s%s' % (tpct, '%'))
        for sg in my.seen_groups:
            if sg != task.get_value('assigned_login_group'):
                black = table.add_cell(' ')
                black.add_attr('width','%s%s' % (my.indi_pct, '%'))
                #black.add_style('background-color: #000000;')
                black.add_style('background-color: #fcfcfc;')
            else:
                tat = Table()
                tat.add_attr('border','2')
                tat.add_attr('width','100%s' % '%')
                tat.add_style('border-color: #909111;')
                tat.add_style('background-color: #0000FF;')
                tat.add_style('color: #000000;')
                tat.add_style('font-weight: bold;')
                tat.add_style('font-size: 10px;')
                wo_code = task.get_value('lookup_code')
                status = task.get_value('status')
                process = task.get_value('process')
                assigned = task.get_value('assigned')
                due_date = my.fix_date(task.get_value('bid_end_date')).split(' ')[0]
                tat.add_row()
                inspect_button = TaskObjLauncherWdg(code=wo_code, name=process)
                inspect = tat.add_cell(inspect_button)
                pro = tat.add_cell(process)
                pro.add_style('background-color: %s;' % my.stat_colors[status])
                pro.add_style('color: #000000;')
                stcell = tat.add_cell(status)
                stcell.add_attr('width','100%s' % '%')
                stcell.add_style('background-color: %s;' % my.stat_colors[status])
                stcell.add_style('color: #000000;')
                tat.add_row()
                wcell = tat.add_cell(wo_code.split('WORK_ORDER')[1])
                wcell.add_attr('width','100%s' % '%')
                acell = tat.add_cell(assigned)
                acell.add_attr('width','100%s' % '%')
                acell.add_style('background-color: %s;' % my.stat_colors[status])
                acell.add_style('color: #000000;')
                dcell = tat.add_cell(due_date)
                dcell.add_attr('width','100%s' % '%')
                dcell.add_style('background-color: %s;' % my.stat_colors[status])
                dcell.add_style('color: #000000;')
                tatcell1 = table.add_cell(tat) 
                tatcell1.add_attr('valign','top')
                tatcell1.add_attr('width','%s%s' % (my.indi_pct, '%'))
                tatcell1.add_style('background-color: #0000F0;')
        return table

    def trow(my, title, expected_delivery_date, count, client_thumbnail_clippings):
        from order_builder.order_builder import OrderBuilderLauncherWdg
        from order_builder.taskobjlauncher import TaskObjLauncherWdg
        expected_delivery_date = my.fix_date(expected_delivery_date)
        code = title.get_value('code')
        name = title.get_value('title')
        episode = title.get_value('episode')
        if episode not in [None,'']:
            name = '%s Episode %s' % (name, episode)
        tdue_date = expected_delivery_date.split(' ')[0]
        ddreal_date = ''
        better_lookin_dd = 'NO DELIVERY DATE'
        dd_color = '#FFFFFF'
        if tdue_date not in [None,'']:
            ddreal_date = datetime.datetime.strptime(tdue_date, '%Y-%m-%d')
            if ddreal_date == my.real_date:
                dd_color = "#FFFF00"
            elif ddreal_date < my.real_date:
                dd_color = "#FF0000"
            else:
                dd_color = "#66CD00"
            tdds = tdue_date.split('-')
            tyear = ''
            tmonth = ''
            tday = ''
            if len(tdds) == 3:
                tyear = tdds[0]
                tmonth = tdds[1]
                tday = tdds[2]
            better_lookin_dd = '%s/%s/%s' % (tmonth, tday, tyear)
            if better_lookin_dd == '//':
                better_lookin_dd = 'NO DELIVERY DATE'
        tpct = my.indi_pct * 2
        table = Table()
        table.add_attr('width','100%s' % '%')
        table.add_attr('border','2')
        table.add_style('color: #000000;')
        table.add_style('background-color: #fcfcfc;')
        table.add_style('font-family: Helvetica;')
        table.add_row()
        dbl = Table()
        dbl.add_attr('width','100%s' % '%')
        dbl.add_style('font-size: 14px;')
        dbl.add_style('color: #000000;')
        dbl.add_style('background-color: #fcfcfc;')
        dbl.add_row()
        d1 = dbl.add_cell('<b><font style="size: 36px; color: #ff0000;">%s.</font> <u>%s</u></b>' % (count, name))
        d1.add_attr('width','100%s' % '%')
        dbl.add_row()
        lil_tbl = Table()
        lil_tbl.set_style('color: #000000; font-size: 12px;')
        lil_tbl.add_style('background-color: #fcfcfc;')
        lil_tbl.add_row()
        lil_tbl.add_cell(code)
        lil_tbl.add_cell("&nbsp;&nbsp;<i>Platform: %s</i>" % title.get_value('platform'))
        lil_tbl.add_cell("&nbsp;&nbsp;<b>Client: %s</b>" % title.get_value('client_name'))
        lil_tbl.add_row()
        obt = Table()
        obt.add_attr('cellpadding','5')
        obt.set_style('color: #000000; font-size: 14px;')
        obt.add_style('background-color: #fcfcfc;')
        obt.add_row()
        delb = obt.add_cell('<font color="%s"><b>Deliver By: %s</b></font>' % (dd_color, better_lookin_dd)) 
        delb.add_attr('colspan','2')
        delb.add_attr('nowrap','nowrap')
        ob = OrderBuilderLauncherWdg(code=title.get_value('order_code'))
        obt.add_attr('width','260px')
        obt.add_cell(ob)
        notes = obt.add_cell('<img src="/context/icons/silk/note_add.png"/>')
        notes.add_style('cursor: pointer;')
        notes.add_behavior(my.get_launch_note_behavior(title.get_search_key(),name)) 
        lil_tbl.add_cell(obt)  
        if title.get_value('no_charge') and title.get_value('redo'):
            lil_tbl.add_row()
            lil_tbl.add_cell('<font color="#FF0000"><b>REDO - NO CHARGE</b></font>')
        d2 = dbl.add_cell(lil_tbl)
        d2.add_attr('width','100%s' % '%')
        if my.big_user:
            dbl.add_row()
            smtbl = Table()
            smtbl.add_style('font-size: 16px;')
            smtbl.add_style('color: #000000;')
            smtbl.add_row()
            offbutt = BigBoardSelectWdg(search_type='twog/title',code=title.get_value('code'),in_bigboard='Yes')
            dblbb = dbl.add_cell(offbutt)
            dblbb.add_attr('width','20px')
            dblpr = smtbl.add_cell('Priority: ')
            dblpr.add_attr('align','left')
            prioid = 'prio_%s' % count
            dbltxt = smtbl.add_cell('<input type="text" value="%s" title_sk="%s" current_priority="%s" class="title_priority" id="%s"/>' % (title.get_value('priority'), title.get_search_key(), title.get_value('priority'), prioid))
            dbltxt.add_attr('align','left')
            dbltxt.add_behavior(my.show_change(prioid))
            dbl.add_cell(smtbl)
        else: 
            dbl.add_row()
            dbl.add_cell('Priority: %s' % title.get_value('priority'))
        tripl = Table()
        tripl.add_attr('width','100%s' % '%')
        #if client_thumbnail_clippings not in [None,'']:
        #    tripl.add_attr('background',client_thumbnail_clippings.split('src="')[1].split('"')[0])
        tripl.add_row()
        ctc = tripl.add_cell(client_thumbnail_clippings)
        ctc.add_attr('valign','top')
        ctc.add_attr('align','left')
        ctc.add_attr('width','25px')
        dc = tripl.add_cell(dbl)
        dc.add_attr('align','left')
        #titl = table.add_cell(dbl)
        titl = table.add_cell(tripl)
        titl.add_attr('valign','top')
        titl.add_attr('width','%s%s' % (tpct, '%'))
        group_keys = my.bigdict[code]['groups'].keys()
        for sg in my.seen_groups:
            if sg not in group_keys:
                black = table.add_cell(' ')
                black.add_attr('width','%s%s' % (my.indi_pct, '%'))
                black.add_style('background-color: #fcfcfc;')
            else:
                tat = Table()
                tat.add_attr('border','2')
                tat.add_attr('width','100%s' % '%')
                tat.add_attr('cellpadding','5')
                tat.add_style('border-color: #909111;')
                tat.add_style('background-color: %s;' % my.bigdict[code]['groups'][sg]['relevant_status_color'])
                tat.add_style('color: #000000;')
                tat.add_style('font-weight: bold;')
                tat.add_style('font-size: 10px;')
                tat.add_style('border-bottom-right-radius', '10px')
                tat.add_style('border-bottom-left-radius', '10px')
                tat.add_style('border-top-right-radius', '10px')
                tat.add_style('border-top-left-radius', '10px')
                tasks = my.bigdict[code]['groups'][sg]['tasks']
                for t in tasks:
                    wo_code = t.get_value('lookup_code')
                    status = t.get_value('status')
                    process = t.get_value('process')
                    assigned = t.get_value('assigned')
                    due_date = my.fix_date(t.get_value('bid_end_date')).split(' ')[0]
                    tat.add_row()
                    inspect_button = TaskObjLauncherWdg(code=wo_code, name=process)
                    inspect = tat.add_cell(inspect_button)
                    wcell = tat.add_cell(wo_code.split('WORK_ORDER')[1])
                    #wcell.add_attr('nowrap','nowrap')
                    pro = tat.add_cell(my.shorten_text(process,10))
                    pro.add_attr('nowrap','nowrap')
                    pro.add_attr('title',process)
                    pro.add_attr('name',process)
                    pro.add_style('background-color: %s;' % my.stat_colors[status])
                    stcell = tat.add_cell(my.shorten_text(status,10))
                    #stcell.add_attr('nowrap','nowrap')
                    stcell.add_attr('title',status)
                    stcell.add_attr('name',status)
                    stcell.add_style('background-color: %s;' % my.stat_colors[status])
                    acell = tat.add_cell(assigned)
                    #acell.add_attr('nowrap','nowrap')
                    acell.add_style('background-color: %s;' % my.stat_colors[status])
                    dcell = tat.add_cell(due_date)
                    #dcell.add_attr('nowrap','nowrap')
                    dcell.add_style('background-color: %s;' % my.stat_colors[status])
                tatcell1 = table.add_cell(tat) 
                tatcell1.add_attr('valign','top')
                tatcell1.add_attr('width','%s%s' % (my.indi_pct, '%'))
                tatcell1.add_style('background-color: #fcfcfc;')
        return table

    def get_onload(my):            
        return r'''
            mytimer = function(timelen){
                setTimeout('refresh_bigboard()', timelen); // uncomment me
            }
            refresh_bigboard = function(){
                board_els = document.getElementsByClassName('bigboard');     
                auto_el = document.getElementById('auto_refresh');
                auto = auto_el.getAttribute('auto');
                scroll_el = document.getElementById('scroll_el');
                scroll = scroll_el.getAttribute('scroll');
                if(auto == 'yes'){
                    for(var r = 0; r < 1; r++){
                        spt.app_busy.show("Refreshing...");
                        spt.api.load_panel(board_els[r], 'nighttime_hotlist.BigBoardWdg', {'auto_refresh': auto, 'scroll': scroll});
                        spt.app_busy.hide();
                    }
                }
                //mytimer(120000);
            }
            mytimer(120000);
        '''

    def get_scroll_by_row(my):
        behavior = {'type': 'load', 'cbjs_action': '''     
            try{ 
                hctime = 500;
                timer2 = function(timelen, next_count, up_or_down, element, origtime){
                    send_str = 'do_scroll(' + next_count + ', ' + up_or_down + ', ' + timelen + ', ' + origtime + ')';  
                    if(element != ''){
                        //element.scrollIntoView();
                        if(element.getAttribute('viz') == 'true'){
                            element.setAttribute('viz','false');
                            element.style.display = 'none';
                        }else{
                            element.setAttribute('viz','true');
                            element.style.display = 'table-row';
                        }
                    }
                    setTimeout(send_str, timelen);
                }
                do_scroll = function(next_count, up_or_down, timelen, origtime){
                    buttons = document.getElementsByClassName('auto_buttons')[0];
                    scroll_el = buttons.getElementById('scroll_el');
                    scroll = scroll_el.getAttribute('scroll');
                    if(scroll == 'yes'){
                        element = '';
                        trs = document.getElementsByClassName('trow');
                        trslen = trs.length;
                        preup = up_or_down;
                        if((trslen - 9 < next_count && up_or_down == 1) || (next_count == 1 && up_or_down == -1)){
                            up_or_down = up_or_down * -1;
                        } 
                        if(preup == up_or_down){
                            next_count = next_count + up_or_down;
                        }
                        for(var r = 0; r < trslen - 1; r++){
                            if(trs[r].getAttribute('num') == next_count){
                                element = trs[r];
                            }
                        }
                        nexttime = 0;
                        if(next_count == 1 || next_count == trslen - 8){
                            nexttime = origtime * 8;
                        }else{
                            nexttime = origtime;
                        }
                        timer2(nexttime, next_count, up_or_down, element, origtime);
                    }
                }
                timer2(hctime, 0, 1, '', hctime); 
            }catch(err){
                      spt.app_busy.hide();
                      spt.alert(spt.exception.handler(err));
            }
         '''}
        return behavior


    def save_priorities(my):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
            try{ 
                var server = TacticServerStub.get();
                var buttons_el = spt.api.get_parent(bvr.src_el, '.auto_buttons');
                auto_el = buttons_el.getElementById('auto_refresh');
                auto = auto_el.getAttribute('auto');
                scroll_el = buttons_el.getElementById('scroll_el');
                scroll = scroll_el.getAttribute('scroll');
                //group_el = buttons_el.getElementById('group_select');
                //group = group_el.value;
                tbs = document.getElementsByClassName('title_priority');
                for(var r = 0; r < tbs.length; r++){
                    val = tbs[r].value;
                    old_val = tbs[r].getAttribute('current_priority');
                    if(old_val != val && Number(val)){
                        t_sk = tbs[r].getAttribute('title_sk');
                        t_code = t_sk.split('code=')[1];
                        server.update(t_sk, {'priority': val});  
                        projects = server.eval("@SOBJECT(twog/proj['title_code','" + t_code + "'])");
                        for(var w = 0; w < projects.length; w++){
                           wts_expr = "@SOBJECT(twog/work_order['proj_code','" + projects[w].code + "'].WT:sthpw/task['bigboard','True']['status','!=','Completed'])"
                           wts = server.eval(wts_expr);
                           if(wts.length > 0){
                               server.update(projects[w].__search_key__, {'priority': val});
                           }
                        }
                    }
                }
                board_els = document.getElementsByClassName('bigboard');     
                for(var r = 0; r < 1; r++){
                    spt.app_busy.show("Refreshing...");
                    //spt.api.load_panel(board_els[r], 'nighttime_hotlist.BigBoardWdg', {'auto_refresh': auto, 'auto_scroll': scroll, 'groups': group});
                    spt.api.load_panel(board_els[r], 'nighttime_hotlist.BigBoardWdg', {'auto_refresh': auto, 'auto_scroll': scroll, 'groups': 'ALL'});
                    spt.app_busy.hide();
                }
            }
            catch(err){
                      spt.app_busy.hide();
                      spt.alert(spt.exception.handler(err));
            }
         '''}
        return behavior

    def show_change(my, ider):
        behavior = {'css_class': 'clickme', 'type': 'change', 'cbjs_action': '''        
                try{
                    var ider = '%s';
                    moi = document.getElementById(ider);
                    moi.style.backgroundColor = "#ff0000";
                    if(moi.value != moi.getAttribute('current_priority')){
                        if(isNaN(moi.value)){
                            moi.value = moi.getAttribute('current_priority');
                            moi.style.backgroundColor = "#ffffff";
                        }
                    }
            }
            catch(err){
                      spt.app_busy.hide();
                      spt.alert(spt.exception.handler(err));
            }
         ''' % ider}
        return behavior

    def set_scroll(my):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
            try{ 
                var buttons_el = spt.api.get_parent(bvr.src_el, '.auto_buttons');
                auto_el = buttons_el.getElementById('auto_refresh');
                auto = auto_el.getAttribute('auto');
                scroll_el = buttons_el.getElementById('scroll_el');
                scroll = scroll_el.getAttribute('scroll');
                //group_el = buttons_el.getElementById('group_select');
                //group = group_el.value;
                if(scroll == 'no'){
                    bvr.src_el.innerHTML = '<input type="button" value="Unset Auto-Scroll"/>';
                    bvr.src_el.setAttribute('scroll','yes');
                    scroll = 'yes';
                }else{
                    bvr.src_el.innerHTML = '<input type="button" value="Set Auto-Scroll"/>';
                    bvr.src_el.setAttribute('scroll','no');
                    scroll = 'no';
                }
                board_els = document.getElementsByClassName('bigboard');     
                for(var r = 0; r < 1; r++){
                    spt.app_busy.show("Refreshing...");
                    //spt.api.load_panel(board_els[r], 'nighttime_hotlist.BigBoardWdg', {'auto_refresh': auto, 'auto_scroll': scroll, 'groups': group});
                    spt.api.load_panel(board_els[r], 'nighttime_hotlist.BigBoardWdg', {'auto_refresh': auto, 'auto_scroll': scroll, 'groups': 'ALL'});
                    spt.app_busy.hide();
                }
            }
            catch(err){
                      spt.app_busy.hide();
                      spt.alert(spt.exception.handler(err));
            }
         '''}
        return behavior

    def get_reload(my):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
            try{ 
                var buttons_el = spt.api.get_parent(bvr.src_el, '.auto_buttons');
                auto = bvr.src_el.get('auto');
                scroll_el = buttons_el.getElementById('scroll_el');
                scroll = scroll_el.getAttribute('scroll');
                //group_el = buttons_el.getElementById('group_select');
                //group = group_el.value;
                if(auto == 'no'){
                    bvr.src_el.innerHTML = '<input type="button" value="Unset Auto-Refresh"/>';
                    bvr.src_el.setAttribute('auto','yes');
                    auto = 'yes';
                }else{
                    bvr.src_el.innerHTML = '<input type="button" value="Set Auto-Refresh"/>';
                    bvr.src_el.setAttribute('auto','no');
                    auto = 'no';
                }
                board_els = document.getElementsByClassName('bigboard');     
                for(var r = 0; r < 1; r++){
                    spt.app_busy.show("Refreshing...");
                    //spt.api.load_panel(board_els[r], 'nighttime_hotlist.BigBoardWdg', {'auto_refresh': auto, 'auto_scroll': scroll, 'groups': group});
                    spt.api.load_panel(board_els[r], 'nighttime_hotlist.BigBoardWdg', {'auto_refresh': auto, 'auto_scroll': scroll, 'groups': 'ALL'});
                    spt.app_busy.hide();
                }
            }
            catch(err){
                      spt.app_busy.hide();
                      spt.alert(spt.exception.handler(err));
            }
         '''}
        return behavior

    def change_group(my):
        behavior = {'css_class': 'clickme', 'type': 'change', 'cbjs_action': '''        
                try{
                var buttons_el = spt.api.get_parent(bvr.src_el, '.auto_buttons');
                auto = bvr.src_el.get('auto');
                scroll_el = buttons_el.getElementById('scroll_el');
                scroll = scroll_el.getAttribute('scroll');
                group_el = buttons_el.getElementById('group_select');
                group = group_el.value;
                board_els = document.getElementsByClassName('bigboard');     
                for(var r = 0; r < 1; r++){
                    spt.app_busy.show("Refreshing...");
                    spt.api.load_panel(board_els[r], 'nighttime_hotlist.BigBoardWdg', {'auto_refresh': auto, 'auto_scroll': scroll, 'groups': group});
                    spt.app_busy.hide();
                }
            }
            catch(err){
                      spt.app_busy.hide();
                      spt.alert(spt.exception.handler(err));
            }
         '''}
        return behavior

    def bring_to_top(my):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                try{
                    body = document.getElementById('title_body');
                    body.scrollTop = 0;
            }
            catch(err){
                      spt.app_busy.hide();
                      spt.alert(spt.exception.handler(err));
            }
         '''}
        return behavior

    def get_buttons(my, auto_refresh, auto_scroll, kgroups):
        from pyasm.widget import SelectWdg
        btns = Table()
        btns.add_attr('class','auto_buttons')
        btns.add_row()
        auto_text = "Set Auto-Refresh"
        if auto_refresh == 'yes':
            auto_text = "Unset Auto-Refresh"
        auto = btns.add_cell('<input type="button" value="%s"/>' % auto_text)
        auto.add_attr('id','auto_refresh')
        auto.add_attr('name','auto_refresh')
        auto.add_attr('auto',auto_refresh)
        auto.add_behavior(my.get_reload())
        scroll_text = "Set Auto-Scroll"
        if auto_scroll == 'yes':
            scroll_text = "Unset Auto-Scroll"
        scroll = btns.add_cell('<input type="button" value="%s"/>' % scroll_text)
        scroll.add_attr('id','scroll_el')
        scroll.add_attr('name','scroll_el')
        scroll.add_attr('scroll',auto_scroll)
        scroll.add_behavior(my.set_scroll())
        to_top = btns.add_cell('<input type="button" value="Go To Top"/>')
        to_top.add_behavior(my.bring_to_top())
        if my.big_user:
            saveit = btns.add_cell('<input type="button" value="Save Priorities"/>')
            saveit.add_behavior(my.save_priorities())
#        group_sel = SelectWdg('group_select')
#        group_sel.add_attr('id','group_select')
#        group_sel.append_option('ALL','ALL')
#        for g in my.all_groups:
#            group_sel.append_option(g,g)
#        group_sel.set_value(kgroups[0])
#        group_sel.add_behavior(my.change_group())
#        btns.add_cell(group_sel)
        return btns

    def get_client_img(my, client_code):
        from pyasm.search import Search
        img_path = ''
        client_search = Search("twog/client")
        client_search.add_filter('code',client_code)
        client = client_search.get_sobject()
        client_id = client.get_id()
        snaps_s = Search("sthpw/snapshot")
        snaps_s.add_filter('search_id',client_id)
        snaps_s.add_filter('search_type','twog/client?project=twog')
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
        from operator import itemgetter
        from pyasm.search import Search
        my.big_user = False
        search = Search("twog/global_resource")
        search.add_filter('name','Usernames Allowed Hot Today Changes')
        allowed = search.get_sobjects()
        if allowed:
            allowed = allowed[0].get_value('description').split(',')
            if my.user in allowed:
                my.big_user = True

        auto_refresh = 'no'
        auto_scroll = 'no'
        kgroups = ['ALL']
        if 'auto_refresh' in my.kwargs.keys():
            auto_refresh = my.kwargs.get('auto_refresh')
        if 'auto_scroll' in my.kwargs.keys():
            auto_scroll = my.kwargs.get('auto_scroll')
        divvy = DivWdg()
        if auto_refresh == 'yes':
            beh = {'type': 'load', 'cbjs_action': my.get_onload()}
            divvy.add_behavior(beh)
        if 'groups' in my.kwargs.keys():
            kgroups = my.kwargs.get('groups').split(',')
        search = Search("sthpw/login_group")
        search.add_where("\"login_group\" not in ('client','default','user')")
        all_groups1 = search.get_sobjects()
        my.all_groups = []
        for ag1 in my.all_groups:
            ag = ag1.get_value('login_group')
            if 'supervisor' not in ag:
                my.all_groups.append(ag)

        thumbnail_clippings = {}

        divvy2 = DivWdg()
        divvy2.add_behavior(my.get_scroll_by_row())
        table = Table()
        table.add_attr('class','bigboard')
        table.add_attr('width','100%s' % '%')
        table.add_attr('bgcolor','#fcfcfc')
        table.add_style('color: #000000;')
        table.add_style('font-family: Helvetica;')
        inorder = []
        bigbox = {}
        bigbox_prios = []
        #title_time = time.time()
        search = Search("twog/title")
        search.add_filter('bigboard',True)
        search.add_order_by("priority")
        bigboarders = search.get_sobjects()
        #end_title_time = time.time() - title_time
        #print "END TITLE TIME = %s" % end_title_time


        #indie_time = time.time()
        search2 = Search("twog/indie_bigboard")
        search2.add_filter('indie_bigboard',True)
        search2.add_order_by("indie_priority")
        bigboarders2 = search2.get_sobjects()
        #end_indie_time = time.time() - indie_time
        #print "END INDIE TIME = %s" % end_indie_time

        #indie_process_time = time.time()
        for b2 in bigboarders2:
            task_code = b2.get_value('task_code')
            ts = Search("sthpw/task")
            ts.add_filter('code',task_code)
            b2_task = ts.get_sobject()
            alg = b2_task.get_value('assigned_login_group')
            if kgroups[0] == 'ALL' or kgroups[0] in alg:
                bigbox[task_code] = b2_task
                bigbox_prios.append({'code': task_code, 'priority': b2.get_value('indie_priority')}) 
                if alg not in my.seen_groups and 'supervisor' not in alg:
                    my.seen_groups.append(alg)
        #end_indie_process_time = time.time() - indie_process_time
        #print "END INDIE PROCESS TIME = %s" % end_indie_process_time

        #test_time = time.time() 
        ########TEST
        tit_to_task = {}
        in_str = ''
        for bb in bigboarders:
            code = bb.get_value('code')
            if in_str == '':
                in_str = "('%s'" % code
            else:
                in_str = "%s,'%s'"% (in_str, code)
        in_str = "%s)" % in_str    
        tq = Search("sthpw/task")
        tq.add_filter('bigboard',True)
        tq.add_filter('active','1')
        tq.add_filter('status','Completed', op="!=")
        if kgroups[0] != 'ALL':
            tq.add_where("\"assigned_login_group\" in ('%s','%s')" % (kgroups[0], kgroups[0]))
        tq.add_where("\"title_code\" in %s" % in_str)
        bigkids4 = tq.get_sobjects()
        for bk in bigkids4:
            titcode = bk.get_value('title_code')
            ord = bk.get_value('order_in_pipe')
            asslg = bk.get_value('assigned_login_group')
            proj_code_linked = bk.get('proj_code')
            ord_name = '%s_%s_%s' % (ord, proj_code_linked, asslg) 
            try:
                tit_to_task[titcode][ord_name] = bk        
            except:
                tit_to_task[titcode] = {ord_name: bk}        
                pass
        
            #try:
            #    tit_to_task[titcode].append(bk)
            #except:
            #    tit_to_task[titcode] = [bk]
            #    pass
        ########END TEST
        #end_test_time = time.time() - test_time
        #print "END TEST TIME = %s" % end_test_time
        
        gorder = ['machine room','media vault','compression','edit','audio','qc','streamz','vault','edeliveries']
        bbc = 0
        #bb_mull_time = time.time()
        for bb in bigboarders:
            code = bb.get_value('code') 
            #search = Search("sthpw/task")
            #search.add_filter('title_code',code)
            #search.add_filter('bigboard',True)
            #search.add_filter('active','1')
            #search.add_filter('status','Completed', op="!=")
            #if kgroups[0] != 'ALL':
            #    search.add_where("\"assigned_login_group\" in ('%s','%s')" % (kgroups[0], kgroups[0]))
            #search.add_order_by('order_in_pipe')
            #bigkids = search.get_sobjects()
            if code in tit_to_task.keys():
                tobs = tit_to_task[code]
            else:
                tobs = {}
            tob_keys = tobs.keys()
            tob_keys.sort()
            bigkids = []
            for tk in tob_keys:
                bigkids.append(tobs[tk])
            if len(bigkids) > 0:
                my.bigdict[code] = {'title_obj': bb, 'groups': {}}
                for bigkid in bigkids:
                    alg = bigkid.get_value('assigned_login_group')
                    status = bigkid.get_value('status')
                    if kgroups[0] == 'ALL':
                        if alg not in my.bigdict[code]['groups'].keys() and 'supervisor' not in alg:
                            my.bigdict[code]['groups'][alg] = {'tasks': [], 'relevant_status': 0, 'relevant_status_color': ''}
                        if alg not in my.seen_groups and 'supervisor' not in alg:
                            my.seen_groups.append(alg)
                        if my.stat_relevance[status] >= my.bigdict[code]['groups'][alg]['relevant_status']:
                            my.bigdict[code]['groups'][alg]['relevant_status'] = my.stat_relevance[status]
                            my.bigdict[code]['groups'][alg]['relevant_status_color'] = my.stat_colors[status]
                        my.bigdict[code]['groups'][alg]['tasks'].append(bigkid)
                        if code not in inorder:
                            inorder.append(code)
                            bigbox[code] = bb
                            bigbox_prios.append({'code': code, 'priority': bb.get_value('priority')}) 
                    else:
                        if kgroups[0] in alg:
                            if alg not in my.bigdict[code]['groups'].keys() and 'supervisor' not in alg:
                                my.bigdict[code]['groups'][alg] = {'tasks': [], 'relevant_status': 0, 'relevant_status_color': ''}
                            if alg not in my.seen_groups and 'supervisor' not in alg:
                                my.seen_groups.append(alg)
                            if my.stat_relevance[status] >= my.bigdict[code]['groups'][alg]['relevant_status']:
                                my.bigdict[code]['groups'][alg]['relevant_status'] = my.stat_relevance[status]
                                my.bigdict[code]['groups'][alg]['relevant_status_color'] = my.stat_colors[status]
                            my.bigdict[code]['groups'][alg]['tasks'].append(bigkid)
                            if code not in inorder:
                                inorder.append(code)
                                bigbox[code] = bb
                                bigbox_prios.append({'code': code, 'priority': bb.get_value('priority')}) 
            bbc = bbc + 1
        #end_bb_mull_time = time.time() - bb_mull_time
        #print "END BB MULL TIME = %s" % end_bb_mull_time
        tmparr = my.seen_groups
        my.seen_groups = []
        for g in gorder:
            if g in tmparr:
                my.seen_groups.append(g)
        for guy in tmparr:
            if guy not in gorder:
                my.seen_groups.append(guy)
   
        if len(kgroups) > 0 and kgroups[0] != 'ALL':
            my.seen_groups = kgroups
        sg_len = len(my.seen_groups)
        col_len = sg_len + 2
        my.indi_pct = float(100/col_len)
        btns = my.get_buttons(auto_refresh, auto_scroll, kgroups) 
        button_top = table.add_row()
        table.add_cell(btns)
        toprow = table.add_row()
        toprow.add_attr('class','trow_nomove')
        table.add_cell(my.trow_top())

        t2div = DivWdg()
        t2div.add_attr('id','title_body')
        t2div.add_attr('width','100%s' % '%')
        t2div.add_attr('bgcolor','#fcfcfc')
        t2div.add_style('color: #000000;')
        t2div.add_style('font-family: Helvetica;')
        t2div.add_style('overflow-y: scroll;')
        t2div.add_style('height: 1400px;')

        t2 = Table()
        t2.add_attr('width','100%s' % '%')
        t2.add_attr('bgcolor','#fcfcfc')
        t2.add_style('color: #000000;')
        t2.add_style('font-family: Helvetica;')
        if my.seen_groups not in [None,'',[]]:
            new_ordering = sorted(bigbox_prios, key=itemgetter('priority')) 
            count = 1
            #for code in inorder:
            for bp in new_ordering:
                code = bp.get('code')
                if 'TITLE' in code:
                    client_thumbnail_clippings = ''
                    bb = my.bigdict[code]['title_obj']
                    client_code = bb.get_value('client_code')
                    if client_code not in thumbnail_clippings.keys():
                        img_path = my.get_client_img(client_code)
                        if img_path not in [None,'']:
                            img_str = '<img src="%s"/>' % img_path
                            thumbnail_clippings[client_code] = img_str      
                            client_thumbnail_clippings = img_str
                    else:
                        client_thumbnail_clippings = thumbnail_clippings[client_code]
                    search = Search("twog/order")
                    search.add_filter('code',bb.get_value('order_code'))
                    title_order = search.get_sobjects()
                    expected_delivery_date = bb.get_value('expected_delivery_date')
                    if title_order:
                        title_order = title_order[0]
                        expected_delivery_date = title_order.get_value('expected_delivery_date')
                    row = my.trow(bb, expected_delivery_date, count, client_thumbnail_clippings)
                    trower = t2.add_row()
                    trower.add_attr('class','trow')
                    trower.add_attr('num',count)
                    trower.add_attr('viz','true')
                    trower.add_style('display: table-row;')
                    rcell = t2.add_cell(row)
                    rcell.add_attr('width','100%s' % '%')
                    count = count + 1
                else:
                    #bb = my.bigdict[code]['task_obj']
                    bb = bigbox[code]
                    search = Search("twog/order")
                    search.add_filter('code',bb.get_value('order_code'))
                    task_order = search.get_sobjects()
                    expected_delivery_date = bb.get_value('bid_end_date')
                    if task_order:
                        task_order = task_order[0]
                        expected_delivery_date = task_order.get_value('expected_delivery_date')
                    row = my.wrow(bb, expected_delivery_date, count)
                    trower = t2.add_row()
                    trower.add_attr('class','trow')
                    trower.add_attr('num',count)
                    trower.add_attr('viz','true')
                    trower.add_style('display: table-row;')
                    rcell = t2.add_cell(row)
                    rcell.add_attr('width','100%s' % '%')
                    count = count + 1
        t2div.add(t2)
        table.add_row()
        table.add_cell(t2div)
        table.add_row() 
        btns = my.get_buttons(auto_refresh, auto_scroll, kgroups) 
        table.add_row()
        table.add_cell(btns)
        divvy2.add(table)
        divvy.add(divvy2)
        return divvy

