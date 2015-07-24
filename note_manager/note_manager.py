__all__ = ["NoteMarkerWdg"]
import tacticenv
from pyasm.common import Environment
from pyasm.web import Table, DivWdg
from tactic.ui.common import BaseTableElementWdg

class NoteMarkerWdg(BaseTableElementWdg):

    def init(my):
        nothing = 'true'
        my.unseen_txt = '<font color="#FF0000"><b>NEW!</b></font>';
        my.seen_txt = '<font color="#000000"><b>Mark Unread</b></font>';

    def get_indicate_behavior(my, login, code):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                          var login = '%s';
                          var note_code = '%s';
                          var seen = bvr.src_el.getAttribute('seen');
                          var unseen_txt = '<font color="#FF0000"><b>NEW!</b></font>';
                          var seen_txt = '<font color="#000000"><b>Mark Unread</b></font>';
                          var server = TacticServerStub.get();
                          var note = server.eval("@SOBJECT(sthpw/note['code','" + note_code + "'])")[0];
                          var seen_by = note.seen_by;
                          if(seen == '0'){
                              //update the seen_by to include login and time - indicate this is a js time with ' -js'
                              var ts = Math.round((new Date()).getTime() / 1000);
                              var new_seen_by = seen_by + '[ ' + login + ',' + ts + ' -js]';
                              server.update(note.__search_key__, {'seen_by': new_seen_by}); 

                              //change the text and variable
                              bvr.src_el.innerHTML = seen_txt; 
                              bvr.src_el.setAttribute('seen','1');
                          }else{
                             //remove self in seen_by, insert seen_by login entry (with time) into prev_seen_by
                             var seen_split = seen_by.split('[ ');
                             var less_str = '';
                             var move_str = ''; 
                             for(var r = 0; r < seen_split.length; r++){
                                 if(seen_split[r].indexOf(login) != -1){
                                     move_str = '[ ' + seen_split[r];
                                 }else{
                                     if(seen_split[r] != '[' && seen_split[r] != '[ ' && seen_split != ' '){
                                         if(less_str == ''){
                                             less_str = '[ ' + seen_split[r];
                                         }else{
                                             less_str = less_str + '[ ' + seen_split[r];
                                         }
                                     }
                                 }
                             }
                             if(less_str == '[ '){
                                 less_str = '';
                             }
                             var prev_seen = note.prev_seen_by + move_str;
                             server.update(note.__search_key__, {'prev_seen_by': prev_seen, 'seen_by': less_str});                             

                             //change the text and variable 
                              bvr.src_el.innerHTML = unseen_txt;
                              bvr.src_el.setAttribute('seen','0');
                          }
                          
                          
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                          //alert(err);
                }
         ''' % (login, code)}
        return behavior

    def get_display(my):
        
        login = Environment.get_user_name()
        sobject = my.get_current_sobject()
        seen_by = sobject.get_value('seen_by')
        code = sobject.get_code()
        txt = my.unseen_txt
        seen_intstr = '0'
        if login in seen_by:
            txt = my.seen_txt
            seen_intstr = '1'
        widget = DivWdg()
        table = Table()
        table.add_attr('width', '50px')
        table.add_row()
        cell1 = table.add_cell(txt)
        indicate_behavior = my.get_indicate_behavior(login, code)
        cell1.add_attr('seen',seen_intstr)
        cell1.add_style('cursor: pointer;')
        cell1.add_behavior(indicate_behavior)
        widget.add(table)

        return widget
