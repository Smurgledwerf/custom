__all__ = ["ClassificationChangeInfoWdg"]
import os, tacticenv
from pyasm.common import Environment
from pyasm.search import Search
from pyasm.web import Table, DivWdg
from tactic.ui.common import BaseRefreshWdg

class ClassificationChangeInfoWdg(BaseRefreshWdg):
    def init(my):
        my.order_sks = []

    def get_on_load(my):
        behavior = {
                'type': 'load',
                'cbjs_action': '''
                top_kill_timer = function(timelen){
                    setTimeout('top_killer()', timelen);
                }
                top_killer = function(){
                    var top_el = spt.api.get_parent(bvr.src_el, '.spt_popup');
                    close_n_min = top_el.getElementsByClassName('glyphicon');
                    for(var r = 0; r < close_n_min.length; r++){
                        close_n_min[r].style.display = 'none';
                    }
                }
                top_killer();
                top_kill_timer(1000);

                '''
        }
        return behavior

    def get_save_behavior(my, user, timestamp):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        function oc(a){
                            var o = {};
                            for(var i=0;i<a.length;i++){
                                o[a[i]]='';
                            }
                            return o;
                        }
                        try{
                          login = '%s';
                          timestamp = '%s';
                          var top_el = spt.api.get_parent(bvr.src_el, '.classification_info');
                          text_areas = top_el.getElementsByTagName('textarea');
                          reasons = {};
                          new_classifications = {};
                          sks = [];
                          not_all_filled = false;
                          for(var r = 0; r < text_areas.length; r++){
                              sk = text_areas[r].getAttribute('sk');
                              new_classification = text_areas[r].getAttribute('new_classification');
                              value = text_areas[r].value;
                              if(value == '' || value == null){
                                  not_all_filled = true;
                              }else{
                                  if(!(sk in oc(sks))){
                                      sks.push(sk);
                                      reasons[sk] = value;
                                      new_classifications[sk] = new_classification;
                                  }  
                              }
                          }
                          if(not_all_filled){
                              alert("Please tell us why each Order's classification changed.");
                          }else{
                              server = TacticServerStub.get();
                              spt.app_busy.show("Saving...");
                              for(var r = 0; r < sks.length; r++){
                                  sk = sks[r];
                                  order = server.get_by_search_key(sk);
                                  ccr = order.classification_change_reasons;
                                  if(ccr == '' || ccr == null){
                                      ccr = 'Change to "' + new_classifications[sk] + '" by ' + login + ' on ' + timestamp + '.\\nReason: ' + reasons[sk]; 
                                  }else{                    
                                      ccr = ccr + '\\n\\nChange to "' + new_classifications[sk] + '" by ' + login + ' on ' + timestamp + '.\\nReason: ' + reasons[sk]; 
                                  }
                                  server.update(sk, {'classification_change_reasons': ccr}, {'triggers': false});
                              }
                              spt.app_busy.hide();
                              spt.popup.close(spt.popup.get_popup(bvr.src_el));
                          }
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
         ''' % (user, timestamp)}
        return behavior

    def make_timestamp(my):
        import datetime
        now = datetime.datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S")

    def get_display(my):   
        login = Environment.get_login()
        user = login.get_login()
        time_changed = my.make_timestamp()
        my.order_sks = str(my.kwargs.get('order_sks'))
        search_keys = my.order_sks.split(',')
        widget = DivWdg()
        widget.add_class('classification_info')
        table = Table()
        for sk in search_keys:
            order = Search.get_by_search_key(sk);
            code = order.get_code()
            table.add_row()
            table.add_cell("Reason for %s's classification change to %s<br/>(Name: %s)" % (code, order.get_value('classification'), order.get_value('name')))
            table.add_row()
            table.add_cell('<textarea cols="45" rows="10" sk="%s" new_classification="%s"></textarea>' % (sk, order.get_value('classification')))
        table.add_row()
        save_butt = table.add_cell('<input type="button" value="Save"/>')
        save_butt.add_attr('align','center')
        save_butt.add_behavior(my.get_save_behavior(user, time_changed))
        widget.add(table)
        widget.add_behavior(my.get_on_load())
        return widget

