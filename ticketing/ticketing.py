__all__ = ["TicketingLauncherWdg","TicketingWdg"]
import tacticenv
from pyasm.common import Environment
from pyasm.biz import *
from pyasm.web import Table, DivWdg
from pyasm.widget import SelectWdg, IconWdg, TextWdg, CheckboxWdg

from tactic.ui.common import BaseTableElementWdg
from tactic.ui.common import BaseRefreshWdg

class TicketingLauncherWdg(BaseTableElementWdg):

    def init(my):
        nothing = 'true'
        my.server = None

    def get_launch_behavior(my):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                          var class_name = 'ticketing.ticketing.TicketingWdg';
                          kwargs = {};
                          spt.panel.load_popup('Report An Issue', class_name, kwargs);
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         '''}
        return behavior

    def get_display(my):
        widget = DivWdg()
        from tactic.ui.widget import SingleButtonWdg
        button = SingleButtonWdg(title='Report An Issue', icon=IconWdg.TAG_ORANGE, show_arrow=False)
        button.add_behavior(my.get_launch_behavior())
        widget.add(button)
        return widget

class TicketingWdg(BaseTableElementWdg):

    def init(my):
        nothing = 'true'

    def get_submit(my, sk):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        function oc(a){
                            var o = {};
                            for(var i=0;i<a.length;i++){
                                o[a[i]]='';
                            }
                            return o;
                        }
                        try{
                          var sk = '%s';
                          top_el = document.getElementById('ticket_window');
                          required_list = ['severity', 'description', 'work_order_code', 'computer_os', 'what_browser', 'how_many_tabs_open', 'last_time_computer_rebooted', 'what_page_in_tactic', 'workstation', 'location', 'applications_running', 'supervisor'];

                          dic = {};
                          dickeys = [];

                          selects = top_el.getElementsByTagName('select');
                          for(var r = 0; r < selects.length; r++){
                              name = selects[r].name;
                              dic[name] = selects[r].value;
                              dickeys.push(name);
                          }

                          inputs = top_el.getElementsByTagName('input');
                          for(var r = 0; r < inputs.length; r++){
                              if(inputs[r].type == 'text'){
                                  name = inputs[r].id;
                                  dic[name] = inputs[r].value;
                                  dickeys.push(name);
                              }
                          }

                          description = top_el.getElementById('description');
                          dic['description'] = description.value;
                          dickeys.push('description');

                          troubleshooting_attempted = top_el.getElementById('troubleshooting_attempted');
                          dic['troubleshooting_attempted'] = troubleshooting_attempted.value;
                          dickeys.push('troubleshooting_attempted');

                          html = document.documentElement.innerHTML;
                          dic['html'] = '<html>' + html + '</html>';
                          dickeys.push('html');
                          fields_to_fill = '';
                          for(var r = 0; r < dickeys.length; r++){
                              name = dickeys[r];
                              if(name in oc(required_list)){
                                  valyew = dic[name];
                                  if(valyew == null || valyew == ''){
                                      if(fields_to_fill == ''){
                                          fields_to_fill = name
                                      }else{
                                          fields_to_fill = fields_to_fill + ', ' + name; 
                                      }
                                  }
                              }
                          }
                          if(fields_to_fill == ''){
                              server = TacticServerStub.get();
                              spt.app_busy.show("Submitting & Reloading...");
                              server.update(sk, dic);
                              var class_name = 'ticketing.ticketing.TicketingWdg';
                              spt.api.load_panel(top_el, class_name, {'search_key': sk}); 
                              spt.app_busy.hide();
                          }else{
                              alert("The following fields are required: " + fields_to_fill);
                              spt.app_busy.show("Checking form...");
                              server = TacticServerStub.get();
                              server.update(sk, dic);
                              var class_name = 'ticketing.ticketing.TicketingWdg';
                              spt.api.load_panel(top_el, class_name, {'search_key': sk}); 
                              spt.app_busy.hide();
                          }
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         ''' % sk}
        return behavior

    def get_close(my):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                          spt.popup.close(spt.popup.get_popup(bvr.src_el));
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         '''}
        return behavior

    def get_on_load_js(my):
        behavior =  {
            'type': 'load',
            'cbjs_action': '''
            var top = bvr.src_el.getParent(".spt_popup");
            top.style.left = 0;
            top.style.top = 0;
            '''
            } 
        return behavior        

    def get_sel(my, id_name, arr, default, alpha_sort):
        this_sel = SelectWdg(id_name)
        this_sel.add_attr('id',id_name)
        if default not in arr and default not in [None,'']:
            arr.append(default)
        if alpha_sort:
            arr.sort()
        arr2 = []
        for a in arr:
            arr2.append(a)
        this_sel.append_option('--Select--','')
        for a in arr2:
            this_sel.append_option(a,a)
        this_sel.set_value(default)
        return this_sel
 

    def get_display(my):
        from tactic_client_lib import TacticServerStub
        server = TacticServerStub.get()
        login = Environment.get_login()
        login_name = login.get_login()
        sk = ''
        picture_path = ''
        picture_html = ''
        dood = None
        get_it = True
        red_star = '<font color="#FF0000">*</font>'
        if 'search_key' in my.kwargs.keys():
            sk = my.kwargs.get('search_key')
            dood = server.get_by_search_key(sk)
            description = dood.get('description')
        else:
            dood = server.insert('twog/ticket', {'login': login_name})
            sk = dood.get('__search_key__')
            get_it = False
        if get_it:
            snap = server.get_snapshot(dood,'ticket') 
            path = server.get_path_from_snapshot(snap.get('code'), mode="web") 
            if path not in [None,'']:
                picture_path = path
                picture_html = '<img src="%s" height="150" width="200"/>' % picture_path
        widget = DivWdg()
        table = Table()
        table.add_attr('id','ticket_window')
        from uploader import CustomHTML5UploadButtonWdg 
        files_butt = CustomHTML5UploadButtonWdg(processes="ticket",sk=sk,name="Upload Screen Shot")
        table.add_row()

        pic = table.add_cell(picture_html)
        pic.add_attr('align','center')

        table.add_row()
        files = table.add_cell(files_butt)
        files.add_attr('align','center')
        files.add_attr('valign','bottom')

        table.add_row()
        table.add_cell("<b><u>Please fill in as much as possible.</u></b>")
        table.add_row()
        table.add_cell("<b><u>Fields with a red asterix</u> (%s)<u> are required.</u></b>" % red_star)

        table.add_row()
        supervisor_sel = my.get_sel('supervisor', server.eval("@GET(sthpw/login['location','internal']['license_type','user'].login)"), dood.get('supervisor'), True)       
        table.add_cell('Supervisor %s' % red_star)
        table.add_row()
        r0 = table.add_cell(supervisor_sel)

        table.add_row()
        table.add_cell('Location %s' % red_star)
        table.add_row()
        r01 = table.add_cell('<input type="text" id="location" value="%s" style="width: 295px;"/>' % dood.get('location'))

        table.add_row()
        table.add_cell('Workstation/Computer %s' % red_star)
        table.add_row()
        r02 = table.add_cell('<input type="text" id="workstation" value="%s" style="width: 295px;"/>' % dood.get('workstation'))

        os_sel = my.get_sel('computer_os', ['Windows 7','Windows 8','Windows XP','Mac OS 10','Mac OS - Other'], dood.get('computer_os'), True)
        table.add_row()
        rw = table.add_cell('What Operating System? %s' % red_star)
        rw.add_attr('nowrap','nowrap')
        table.add_row()
        r50 = table.add_cell(os_sel)

        what_browser_sel = my.get_sel('what_browser', ['Firefox','Chrome','Internet Explorer','Safari','Other'], dood.get('what_browser'), True)
        table.add_row()
        rw1 = table.add_cell('What Browser? %s' % red_star)
        rw1.add_attr('nowrap','nowrap')
        table.add_row()
        r5 = table.add_cell(what_browser_sel)

        table.add_row()
        table.add_cell('Order Code ')
        table.add_row()
        r1 = table.add_cell('<input type="text" id="order_code" value="%s" style="width: 295px;"/>' % dood.get('order_code'))

        table.add_row()
        table.add_cell('Title Code ')
        table.add_row()
        r2 = table.add_cell('<input type="text" id="title_code" value="%s" style="width: 295px;"/>' % dood.get('title_code'))

        table.add_row()
        rw2 = table.add_cell('Work Order Code %s (N/A if not applicable)' % red_star)
        rw2.add_attr('nowrap','nowrap')
        table.add_row()
        r3 = table.add_cell('<input type="text" id="work_order_code" value="%s" style="width: 295px;"/>' % dood.get('work_order_code'))

        table.add_row()
        table.add_cell('What Page Did The Error Come From? %s' % red_star)
        table.add_row()
        r30 = table.add_cell('<input type="text" id="what_page_in_tactic" value="%s" style="width: 295px;"/>' % dood.get('what_page_in_tactic'))

        table.add_row()
        table.add_cell('Description of Problem %s' % red_star)
        table.add_row()
        txt = table.add_cell('<textarea id="description" cols="50" rows="7">%s</textarea>' % dood.get('description'))

        table.add_row()
        rw4 = table.add_cell("Troubleshooting You've Attempted")
        rw4.add_attr('nowrap','nowrap')
        table.add_row()
        txt2 = table.add_cell('<textarea id="troubleshooting_attempted" cols="50" rows="7">%s</textarea>' % dood.get('troubleshooting_attempted'))

        happen_anyone_sel = my.get_sel('happen_for_anyone_else', ['Yes','No'], dood.get('happen_for_anyone_else'), False)
        table.add_row()
        table.add_cell('Happens For Anyone Else? ')
        table.add_row()
        r4 = table.add_cell(happen_anyone_sel)

        table.add_row()
        table.add_cell('If so, how often? ')
        table.add_row()
        r41 = table.add_cell('<input type="text" id="happens_how_often" value="%s" style="width: 295px;"/>' % dood.get('happens_how_often'))

        table.add_row()
        table.add_cell('How Many Tabs Are Open In Tactic? %s' % red_star)
        table.add_row()
        r42 = table.add_cell('<input type="text" id="how_many_tabs_open" value="%s" style="width: 295px;"/>' % dood.get('how_many_tabs_open'))

        table.add_row()
        table.add_cell('What Applications Are Running On The Computer? %s (ex: Excel, iTunes, Chrome, Photoshop, The Sims, etc)' % red_star)
        table.add_row()
        r44 = table.add_cell('<input type="text" id="applications_running" value="%s" style="width: 295px;"/>' % dood.get('applications_running'))

        table.add_row()
        table.add_cell('When Was Computer Rebooted Last? %s' % red_star)
        table.add_row()
        r43 = table.add_cell('<input type="text" id="last_time_computer_rebooted" value="%s" style="width: 295px;"/>' % dood.get('last_time_computer_rebooted'))


        severity_sel = my.get_sel('severity', ['1 - Needs Immediate Action','2 - Needs Attention Within 1 Hour','3 - Needs Service In Next Couple Hours','4 - Needs Service Within 8 Hours','5 - Needs Service Within 24 Hours','6 - Needs Service Within 1 Week','7 - Minor Error, Needs To Be Addressed','8 - Suggestion'], dood.get('severity'), True)       
        table.add_row()
        table.add_cell('Severity %s ' % red_star)
        table.add_row()
        r6 = table.add_cell(severity_sel)

        table.add_row()
        button = table.add_cell('<input type="button" value="Submit"/>')
        button.add_behavior(my.get_submit(sk))
        t1 = table.add_cell(' ')
        t1.add_attr('width','35%s' % '%')
        close = table.add_cell('<input type="button" value="Close"/>') 
        close.add_behavior(my.get_close())
        widget.add(table)
        widget.add_behavior(my.get_on_load_js())

        return widget

