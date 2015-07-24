__all__ = ["ImdbScraperWdg"]
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

class ImdbScraperWdg(BaseRefreshWdg):

    def init(my):
        from client.tactic_client_lib import TacticServerStub
        my.title_of_show = my.kwargs.get('title_of_show')

    def get_search(my):
        behavior = {'css_class': 'clickme', 'type': 'change', 'cbjs_action': '''        
             try{
                    title_of_show = bvr.src_el.value;
                    top_el = spt.api.get_parent(bvr.src_el, '.scraper');
                    spt.api.load_panel(top_el, 'scraper.ImdbScraperWdg', {'title_of_show': title_of_show}); 
                }
                catch(err){
                          spt.app_busy.hide();
                          alert(err);
                }
        '''}
        return behavior 

    def parse_scraper_string(my, str_in):
        print "STR = %s" % str_in
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
                        print "SUBFIELDS = %s" % subfields
                        for chunk in subfields:
                            if len(chunk) > 0:
                                chunk_s = chunk.split('=>')
                                print "CHUNK_S = %s" % chunk_s
                                subfield = chunk_s[0]
                                subval = chunk_s[1]
                                tdict[array_name][subfield] = subval
                t_array.append(tdict)
        return t_array
                        
                    
                            
                         
        

    def get_multiple_title_info(my, title_of_show):
        proc = subprocess.Popen('''php /opt/spt/custom/scraper/runner.php "%s"''' % title_of_show, shell=True, stdout=subprocess.PIPE)
        delimited_str = proc.stdout.read()
        info = my.parse_scraper_string(delimited_str)
        return info


    def get_display(my):
        widget = DivWdg()
        table = Table()
        table.add_attr('class','scraper')
        table.add_row()
        tb = TextWdg('title_box')
        tb.add_attr('id','title_box')
        multiple_titles = None
        print "MY.TITLE_OF_SHOW = %s" % my.title_of_show
        if my.title_of_show not in [None,'']:
            tb.set_value(my.title_of_show)
            #poster_url_text = my.get_poster_url(my.title_of_show)
            #poster_url = poster_url_text.split('=')[1]
            multiple_titles = my.get_multiple_title_info(my.title_of_show)
        print "MULTIPLE_TITLES = %s" % multiple_titles
        tb.add_behavior(my.get_search())
        table.add_cell(tb)
        if multiple_titles not in [None,''] and len(multiple_titles) > 0:
            for m in multiple_titles:
                table.add_row()
                table.add_cell('<img src="%s"/>' % m['TopLevel']['poster'])
                mkeys = m.keys()
                for k in mkeys: 
                    table.add_row()
                    table.add_cell('<b><u>%s</u></b>' % k)
                    dudes = m[k]
                    dkeys = dudes.keys()
                    for d in dkeys:
                        table.add_row()
                        table.add_cell('%s: %s' % (d, dudes[d])) 
        widget.add(table)
        return widget

