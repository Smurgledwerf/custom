__all__ = ["OrderCheckerLauncherWdg","OrderCheckerWdg"]
import os, tacticenv
from pyasm.common import Environment
from pyasm.web import Table, DivWdg
from pyasm.widget import IconWdg
from tactic.ui.common import BaseTableElementWdg
from tactic.ui.common import BaseRefreshWdg
from tactic.ui.widget.button_new_wdg import ButtonSmallNewWdg, ButtonRowWdg

class OrderCheckerLauncherWdg(BaseTableElementWdg):

    def init(my):
        nothing = 'true'
        my.server = None

    def get_launch_behavior(my, order_name, sob_sk, user_name, code):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                          var order_name = '%s';
                          var my_sk = '%s';
                          var my_user = '%s'; 
                          var my_code = '%s'; 
                          var class_name = 'order_builder.order_checker.OrderCheckerWdg';
                          kwargs = {
                                           'sk': my_sk,
                                           'user': my_user,
                                           'code': my_code,
                                           'order_name': order_name
                                   };
                          spt.panel.load_popup('Performing Order Check for ' + order_name, class_name, kwargs);
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                          //alert(err);
                }
         ''' % (order_name, sob_sk, user_name, code)}
        return behavior

    def get_display(my):
        code = ''
        sob_sk = ''
        order_name = ''
        sob_id = ''
        sobject = None
        if 'order_code' in my.kwargs.keys():
            from client.tactic_client_lib import TacticServerStub
            my.server = TacticServerStub.get()
            code = str(my.kwargs.get('order_code'))
            sob_sk = my.server.build_search_key('twog/order', code)
            sobject = my.server.eval("@SOBJECT(twog/order['code','%s'])" % code)
            if sobject:
                sobject = sobject[0]
                order_name = sobject.get('name')
                sob_id = sobject.get('id')
        else:
            sobject = my.get_current_sobject()
            code = sobject.get_code()
            order_name = sobject.get_value('name')
            sob_sk = sobject.get_search_key()
            sob_id = sobject.get_value('id')
        widget = DivWdg()
        table = Table()
        login = Environment.get_login()
        user_name = login.get_login()
        table.add_row()
        cell1 = None
        launch_behavior = my.get_launch_behavior(order_name, sob_sk, user_name, code)
        if 'order_code' in my.kwargs.keys():
            smallbutt = ButtonSmallNewWdg(title="Order Checker", icon=IconWdg.CHECK)
            smallbutt.add_behavior(launch_behavior)
            cell1 = table.add_cell(smallbutt)
            cell1.add_attr('align','right')
        else:
            table.add_attr('width', '50px')
            cell1 =  table.add_cell('<img border="0" style="vertical-align: middle" title="" src="/context/icons/silk/tick.png">')
        cell1.add_style('cursor: pointer;')
        cell1.add_behavior(launch_behavior)
        widget.add(table)

        return widget

class OrderCheckerWdg(BaseRefreshWdg):
    def init(my):
        import datetime
        from client.tactic_client_lib import TacticServerStub
        from pyasm.common import Environment
        my.server = TacticServerStub.get()
        my.sk = ''
        my.code = ''
        my.order_code = ''
        my.sid = ''
        my.allowed_titles_str = ''
        my.allowed_titles = []
        my.login = Environment.get_login()
        my.user_name = my.login.get_login()
        my.width = '1000px'
        my.height = '300px'
        my.order_field_errors = []
        my.title_field_errors = []
        my.order = None
        my.titles = None
        my.projs = None
        my.title_proj_counts = {}
        my.proj_codes = []
        my.wo_codes = []
        my.combo_codes = []
        my.ptasks = None
        my.wos = None
        my.wtasks = None
        my.equs = None
        my.date = str(datetime.datetime.now()).split(' ')[0]
        my.date_int = int(my.date.replace('-',''))
        my.timestamp = str(datetime.datetime.now())
        my.pt_checkdata = {'status': 'status', 'bid_start_date': 'start_date', 'bid_end_date': 'due_date', 'process': 'process', 'context': 'process', 'title': 'title', 'creator_login': 'login', 'client_name': 'client_name', 'po_number': 'po_number', 'episode': 'episode', 'territory': 'territory', 'priority': 'priority', 'order_name': 'order_name', 'client_code': 'client_code', 'title_id_number': 'title_id_number', 'platform': 'platform', 'proj_code': 'code'}
        my.wt_checkdata = {'bid_end_date': 'due_date', 'process': 'process', 'context': 'process', 'title': 'title', 'creator_login': 'login', 'po_number': 'po_number', 'episode': 'episode', 'territory': 'territory', 'priority': 'priority', 'order_name': 'order_name', 'client_code': 'client_code', 'title_id_number': 'title_id_number', 'platform': 'platform', 'proj_code': 'proj_code'}
        #my.color_dict = {'Critical': '#ff0000', 'Low': '#33a1c9', 'Mid': '#fbffc9', 'High': '#f8c926'}
        my.color_dict = {'Critical': '#b52424', 'Low': '#a7cacb', 'Mid': '#fff7b7', 'High': '#f8b666'}
        my.reverse_color_dict = {'#b52424': 'Critical', '#a7cacb': 'Low', '#fff7b7': 'Mid', '#f8b666': 'High'}
        my.color_counter = {my.color_dict['Critical']: 0, my.color_dict['Low']: 0, my.color_dict['Mid']: 0, my.color_dict['High']: 0}
        my.classification_switcher = {'cancelled': 'Bid', 'master': 'Cancelled', 'bid': 'Cancelled', 'in_production': 'Cancelled', 'completed': 'Completed', 'Cancelled': 'Bid', 'Master': 'Cancelled', 'Bid': 'Cancelled', 'On Hold': 'Cancelled', 'oh hold': 'Cancelled', 'In Production': 'Cancelled', 'Completed': 'Completed'}
        my.reverse_dict = {}
        my.active_tasks = 0
        my.inactive_tasks = 0
        for key, var in my.color_dict.iteritems():
            my.reverse_dict[var] = key
        my.label_colors = {
                        'Data Entry': ['<font color="%s"><b>' % my.color_dict['Critical'],'</b></font>', my.color_dict['Critical'], '<table height="100%s" width="100%s" border="1" bordercolor="%s" style="font-size: 12px;"><tr><td valign="center" height="100%s" width="100%s" nowrap><b>' % ('%','%',my.color_dict['Critical'],'%','%'), '</b></td></tr></table>'],
                        'Data Entry Optional': ['','', my.color_dict['Low'], '<table height="100%s" width="100%s" border="0" bordercolor="%s" style="font-size: 12px;"><tr><td valign="center" height="100%s" width="100%s" nowrap><b>' % ('%','%',my.color_dict['Low'], '%', '%'), '</b></td></tr></table>'],
                        'Invalid Association':  ['<font color="%s"><b>' % my.color_dict['High'],'</b></font>', my.color_dict['High'], '<table height="100%s" width="100%s" border="1" bordercolor="%s" style="font-size: 12px;"><tr><td valign="center" height="100%s" width="100%s" nowrap><b>' % ('%','%',my.color_dict['High'], '%','%'), '</b></td></tr></table>'],
                        'Number Format':  ['<font color="%s"><b>' % my.color_dict['Critical'],'</b></font>', my.color_dict['Critical'], '<table height="100%s" width="100%s" border="1" bordercolor="%s" style="font-size: 12px;"><tr><td valign="center" height="100%s" width="100%s" nowrap><b>' % ('%','%',my.color_dict['Critical'], '%','%'), '</b></td></tr></table>'],
                        'Simple Search Difficulty': ['','', my.color_dict['Low'], '<table height="100%s" width="100%s" border="0" bordercolor="%s" style="font-size: 12px;"><tr><td valign="center" height="100%s" width="100%s" nowrap><b>' % ('%','%',my.color_dict['Low'], '%','%'), '</b></td></tr></table>'],
                        'Illegal Character':  ['<font color="%s"><b>' % my.color_dict['Critical'],'</b></font>', my.color_dict['Critical'], '<table height="100%s" width="100%s" border="1" bordercolor="%s" style="font-size: 12px;"><tr><td valign="center" height="100%s" width="100%s" nowrap><b>' % ('%','%',my.color_dict['Critical'], '%','%'), '</b></td></tr></table>'],
                        'Mismatch': ['<font color="%s">' % my.color_dict['Mid'],'</font>', my.color_dict['Mid'], '<table height="100%s" width="100%s" border="0" bordercolor="%s" style="font-size: 12px;"><tr><td valign="center" height="100%s" width="100%s" nowrap><b>' % ('%','%',my.color_dict['Mid'], '%','%'), '</b></td></tr></table>'],
                        'Date Questionable': ['<font color="%s">' % my.color_dict['Mid'],'</font>', my.color_dict['Mid'], '<table height="100%s" width="100%s" border="0" bordercolor="%s" style="font-size: 12px;"><tr><td valign="center" height="100%s" width="100%s" nowrap><b>' % ('%','%',my.color_dict['Mid'], '%','%'), '</b></td></tr></table>'],
                        'Internal Error':  ['<font color="%s"><b>' % my.color_dict['Critical'],'</b></font>', my.color_dict['Critical'], '<table height="100%s" width="100%s" border="1" bordercolor="%s" style="font-size: 12px;"><tr><td valign="center" height="100%s" width="100%s" nowrap><b>' % ('%','%',my.color_dict['Critical'], '%','%'), '</b></td></tr></table>'],
                        'Internal Stuck Var':  ['<font color="%s"><b>' % my.color_dict['High'],'</b></font>', my.color_dict['High'], '<table height="100%s" width="100%s" border="1" bordercolor="%s" style="font-size: 12px;"><tr><td valign="center" height="100%s" width="100%s" nowrap><b>' % ('%','%',my.color_dict['High'], '%','%'), '</b></td></tr></table>'],
                        'Templating Problem':  ['<font color="%s"><b>' % my.color_dict['High'],'</b></font>', my.color_dict['High'], '<table height="100%s" width="100%s" border="1" bordercolor="%s" style="font-size: 12px;"><tr><td valign="center" height="100%s" width="100%s" nowrap><b>' % ('%','%',my.color_dict['High'], '%','%'), '</b></td></tr></table>'],
                        'Login Group Assignment':  ['<font color="%s"><b>' % my.color_dict['Critical'],'</b></font>', my.color_dict['Critical'], '<table height="100%s" width="100%s" border="1" bordercolor="%s" style="font-size: 12px;"><tr><td valign="center" height="100%s" width="100%s" nowrap><b>' % ('%','%',my.color_dict['Critical'], '%','%'), '</b></td></tr></table>'],
                        'Login Group Important':  ['<font color="%s"><b>' % my.color_dict['High'],'</b></font>', my.color_dict['High'], '<table height="100%s" width="100%s" border="1" bordercolor="%s" style="font-size: 12px;"><tr><td valign="center" height="100%s" width="100%s" nowrap><b>' % ('%','%',my.color_dict['High'], '%','%'), '</b></td></tr></table>'],
                        'Task Closed':  ['<font color="%s"><b>' % my.color_dict['High'],'</b></font>', my.color_dict['High'], '<table height="100%s" width="100%s" border="1" bordercolor="%s" style="font-size: 12px;"><tr><td valign="center" height="100%s" width="100%s" nowrap><b>' % ('%','%',my.color_dict['High'], '%','%'), '</b></td></tr></table>'],
                        'Association Broken':  ['<font color="%s"><b>' % my.color_dict['High'],'</b></font>', my.color_dict['High'], '<table height="100%s" width="100%s" border="1" bordercolor="%s" style="font-size: 12px;"><tr><td valign="center" height="100%s" width="100%s" nowrap><b>' % ('%','%',my.color_dict['High'], '%','%'), '</b></td></tr></table>'],
                        'Unconnected Task':  ['<font color="%s"><b>' % my.color_dict['Critical'],'</b></font>', my.color_dict['Critical'], '<table height="100%s" width="100%s" border="1" bordercolor="%s" style="font-size: 12px;"><tr><td valign="center" height="100%s" width="100%s" nowrap><b>' % ('%','%',my.color_dict['Critical'], '%','%'), '</b></td></tr></table>'],
                        'Unlikely Hours': ['<font color="%s">' % my.color_dict['Mid'],'</font>', my.color_dict['Mid'], '<table height="100%s" width="100%s" border="0" bordercolor="%s" style="font-size: 12px;"><tr><td valign="center" height="100%s" width="100%s" nowrap><b>' % ('%','%',my.color_dict['Mid'], '%','%'), '</b></td></tr></table>'],
                        'Unconnected Equipment':  ['<font color="%s"><b>' % my.color_dict['High'],'</b></font>', my.color_dict['High'], '<table height="100%s" width="100%s" border="1" bordercolor="%s" style="font-size: 12px;"><tr><td valign="center" height="100%s" width="100%s" nowrap><b>' % ('%','%',my.color_dict['High'], '%','%'), '</b></td></tr></table>'],
                        'Partially Active':  ['<font color="%s"><b>' % my.color_dict['Critical'],'</b></font>', my.color_dict['Critical'], '<table height="100%s" width="100%s" border="1" bordercolor="%s" style="font-size: 12px;"><tr><td valign="center" height="100%s" width="100%s" nowrap><b>' % ('%','%',my.color_dict['Critical'], '%','%'), '</b></td></tr></table>'],
                        'Partially Active Fixed':  ['<font color="%s"><b>' % my.color_dict['High'],'</b></font>', my.color_dict['High'], '<table height="100%s" width="100%s" border="1" bordercolor="%s" style="font-size: 12px;"><tr><td valign="center" height="100%s" width="100%s" nowrap><b>' % ('%','%',my.color_dict['High'], '%','%'), '</b></td></tr></table>'],
                        'Infinite Loop Detected':  ['<font color="%s"><b>' % my.color_dict['Critical'],'</b></font>', my.color_dict['Critical'], '<table height="100%s" width="100%s" border="1" bordercolor="%s" style="font-size: 12px;"><tr><td valign="center" height="100%s" width="100%s" nowrap><b>' % ('%','%',my.color_dict['Critical'], '%','%'), '</b></td></tr></table>'],
                        'Need At Least 1 QC WO':  ['<font color="%s"><b>' % my.color_dict['Critical'],'</b></font>', my.color_dict['Critical'], '<table height="100%s" width="100%s" border="1" bordercolor="%s" style="font-size: 12px;"><tr><td valign="center" height="100%s" width="100%s" nowrap><b>' % ('%','%',my.color_dict['Critical'], '%','%'), '</b></td></tr></table>'],
                        'Sharing Pipeline': ['<font color="%s"><b>' % my.color_dict['High'],'</b></font>', my.color_dict['High'], '<table height="100%s" width="100%s" border="1" bordercolor="%s" style="font-size: 12px;"><tr><td valign="center" height="100%s" width="100%s" nowrap><b>' % ('%','%',my.color_dict['High'], '%','%'), '</b></td></tr></table>'],
                        'Duplicate Process Name':  ['<font color="%s"><b>' % my.color_dict['High'],'</b></font>', my.color_dict['High'], '<table height="100%s" width="100%s" border="1" bordercolor="%s" style="font-size: 12px;"><tr><td valign="center" height="100%s" width="100%s" nowrap><b>' % ('%','%',my.color_dict['High'], '%','%'), '</b></td></tr></table>'],
                        'Pipeline Missing': ['<font color="%s"><b>' % my.color_dict['Critical'],'</b></font>', my.color_dict['Critical'], '<table height="100%s" width="100%s" border="1" bordercolor="%s" style="font-size: 12px;"><tr><td valign="center" height="100%s" width="100%s" nowrap><b>' % ('%','%',my.color_dict['Critical'], '%','%'), '</b></td></tr></table>'],
                        'Pipeline Unassigned': ['<font color="%s"><b>' % my.color_dict['Critical'],'</b></font>', my.color_dict['Critical'], '<table height="100%s" width="100%s" border="1" bordercolor="%s" style="font-size: 12px;"><tr><td valign="center" height="100%s" width="100%s" nowrap><b>' % ('%','%',my.color_dict['Critical'], '%','%'), '</b></td></tr></table>']}

    def do_client_person_to_client_check(my, field_checked, person_code, client_code):
        # Make sure the person is associated with the client
        return_messages = []
        is_good = True
        client_name = 'EMPTY'
        if client_code in [None,'']:
            client_code = 'EMPTY'

        client = my.server.eval("@SOBJECT(twog/client['code','%s'])" % client_code)
        if client:
           client = client[0]
           client_name = client.get('name')
        else:
           is_good = False
           return_messages.append(['Data Entry', "Order's Client with code: %s seems to be missing. Please, contact the Admin to resolve before continuing." % (client_code)])

        person = my.server.eval("@SOBJECT(twog/person['code','%s'])" % person_code)
        if person:
            person = person[0]
            person_client_code = person.get('client_code')
            if person_client_code != client_code:
                is_good = False
                person_client = my.server.eval("@SOBJECT(twog/client['code','%s'])" % person_client_code)
                if person_client:
                    person_client = person_client[0]
                    return_messages.append(['Invalid Association', "Order's %s (%s %s) belongs to Client '%s' (%s), not '%s' (%s). Please, contact the Admin to resolve this before continuing." % (field_checked, person.get('first_name'), person.get('last_name'), person_client.get('name'), person_client_code, client_name, client_code)])
                else:
                    return_messages.append(['Invalid Association', "Order's %s's (%s %s) Client code, seems to be missing. Please, contact the Admin to resolve before continuing." % (field_checked, person.get('first_name'), person.get('last_name'))]) 
        else:
            is_good = False
            if person_code in [None,'']:
                person_code = 'EMPTY'
            return_messages.append(['Invalid Association', '%s with code: %s seems to be missing. Please, contact the Admin to resolve before continuing.' % (field_checked, person_code)])
            
        return [is_good, return_messages] 

    def fix_num(my, number_str):
        number_str = str(number_str)
        if number_str[-2:] == '.0':
            number_str = '%s0' % number_str
        if number_str[:2] == '0.':
            number_str = number_str.replace('0.','.')
        return number_str
         
    def numbers_only(my, parent_code, field_checked, possible_string):
        # strip commas, make sure there is only 1 '.' and only 1 '-', everything else must be a number
        is_good = True
        messages = []
        if not possible_string:
            possible_string = ''
        else:
            possible_string = str(possible_string)
        out_str = ''
        dot_count = 0
        dash_count = 0
        char_count = 0
        ret_str = '0.0' 
        for ch in possible_string:
            if ch  == '.':
                dot_count = dot_count + 1
                out_str = '%s%s' % (out_str, ch) 
            elif ch == '-':
                dash_count = dash_count + 1
                out_str = '%s%s' % (out_str, ch) 
            elif ch in ['0','1','2','3','4','5','6','7','8','9']:
                out_str = '%s%s' % (out_str, ch) 
            elif ch in [' ','\t',',']:
                out_str = out_str # don't add these characters back in
            else:
                is_good = False
                messages.append(['Number Format', "%s's %s should be a number. Currently, it is %s. Please correct this before proceeding." % (parent_code, field_checked, possible_string)])
                return_number = 0
            if ch == '-' and char_count > 0:
                is_good = False
                messages.append(['Number Format', "%s's %s should not have a '-' in any place other than the beginning of the number, if at all. Currently, it is %s. Please correct this before proceeding." % (parent_code, field_checked, possible_string)])
                return_number = 0
            char_count = char_count + 1
        if out_str == '' and is_good:
            out_str = 0
        if dot_count > 1:
            is_good = False
            messages.append(['Number Format', "%s's %s should not contain more than one decimal point. Currently, it is %s. Please correct this before proceeding." % (parent_code, field_checked, possible_string)])
            return_number = 0
        if dash_count > 1:
            is_good = False
            messages.append(['Number Format', "%s's %s should not contain more than one '-'. Currently, it is %s. Please correct this before proceeding." % (parent_code, field_checked, possible_string)])
            return_number = 0
        if is_good:
            if dot_count > 0:
                return_number = float(out_str)
            else:
                return_number = int(out_str)
            ret_str = str(return_number)
            if out_str in [None,'']:
                out_str = '0'
            return_number = float(out_str)
            #print "RET STR BEGIN = %s" % ret_str
            #print "RET_STR[-2:] = %s" % ret_str[-2:]
            #print "RET_STR[:2] = %s" % ret_str[:2]
            if '.' in ret_str[-2:]:
                #print "HERE 1"
                ret_str = '%s0' % ret_str
                #print "RET_STR AFTER HERE 1 = %s" % ret_str
            if ret_str[:2] == '0.':
                #print "HERE 2"
                ret_str = ret_str.replace("0.", ".")
            #print "RET_NUM = %s, RET STR = %s" % (return_number, ret_str)
        return [is_good, messages, return_number, ret_str]

    def name_char_check(my, sob):
        ok_chars = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9','_','-','+',' ']
        simple_chars = ['?','!','&','|','{','}','[',']','@','#','$','%','^','*','(',')','=',':',';','~','`','>','<',',','.','\\','/','"']
        banned_chars = ["'", '\n','\t','\r']
        banned_chars_translator = {"'": 'Apostrophe', "\n": 'New Line', "\t": 'Tab', "\r": 'Carriage Return'}
        sob_keys = sob.keys()
        sob_sk = sob.get('__search_key__')
        sob_st = sob_sk.split('?')[0]
        do_list = []
        is_good = True
        messages = []
        do_lists = {'twog/order': ['name','po_number'], 'twog/title': ['title','episode'], 'twog/proj': ['process'], 'twog/work_order': ['process']}
        do_list = do_lists[sob_st]
        for guy in do_list:
            guy_val = sob.get(guy)
            if guy_val == None:
                option = '' 
                end = 'This needs to be filled in before proceeding.'
                if guy == 'episode':
                    option = ' Optional'
                    end = 'This is optional, as it is unnecessary for many titles. Just a heads up that the field is empty.'
                messages.append(['Data Entry%s' % option, '''%s's %s is EMPTY. %s''' % (sob.get('code'), guy, end)])
            else:
                for chr in guy_val:
                    if chr not in ok_chars:
                        if chr in simple_chars:
                           messages.append(['Simple Search Difficulty', '''%s's %s (%s) contains character "%s", which is ok, but it may be difficult to search for with the Simple Search Filter later. No action needs to be taken.''' % (sob.get('code'), guy, guy_val, chr)]) 
                        elif chr in banned_chars:
                            is_good = False
                            messages.append(['Illegal Character', '''%s's %s (%s) contains character "%s". This character is not allowed in this data field. Please change it before proceeding.''' % (sob.get('code'), guy, guy_val, banned_chars_translator[chr])])
                        else:
                            is_good = False
                            messages.append(['Illegal Character', '''%s's %s (%s) contains character "%s". This character is not allowed in this data field. Please change it before proceeding.''' % (sob.get('code'), guy, guy_val, chr)])
        return [is_good, messages]
            

    def do_order_field_check(my):
        errors = []
        client_rep = my.order.get('client_rep')
        client_code = my.order.get('client_code')
        client_person_check = my.do_client_person_to_client_check('Client Rep', client_rep, client_code)
        if not client_person_check[0]:
            #Then it was rejected for some reason
            for cpc in client_person_check[1]:
                errors.append(cpc)
        if my.order.get('classification') not in ['master','Master']:
            if my.order.get('expected_price') in [None,'',0,'0']:
                errors.append(['Data Entry Optional','The Order, %s (%s), does not have an expected_price. Please set it when that information becomes available.' % (my.order.get('name'), my.order.get('code'))])
            else:
                expected_price_check = my.numbers_only(my.order.get('code'), 'expected_price', my.order.get('expected_price'))
                if expected_price_check[0]:
                    epc = '%.2f' % float(str(expected_price_check[3]))
                    oep = '%.2f' % float(my.fix_num(my.order.get('expected_price')))
                    #print "EPC = %s, OEP = %s" % (epc, oep)
                    if epc != oep:
                        if my.order.get('expected_price') not in [None, '']:
                            #my.server.update(my.order.get('__search_key__'), {'expected_price': expected_price_check[2]})
                            errors.append(['Number Format','''%s's expected_price has incorrect formatting (%s). Should it instead be this?: %s''' % (my.order.get('code'), my.order.get('expected_price'), str(expected_price_check[2]))])
                else:
                    for ep in expected_price_check[1]:
                        errors.append(ep)
                char_checks = my.name_char_check(my.order)
                if len(char_checks[1]) > 0:
                    for cc in char_checks[1]:
                        errors.append(cc) 
        return errors        

    def do_field_checks(my):
        errors = []
        my.active_tasks = 0
        my.inactive_tasks = 0
        title_active = 0
        title_inactive = 0
        classification = my.order.get('classification')
        for title in my.titles:
            #print 'FIELDCHECK %s Status: %s' % (title.get('code'), title.get('status'))
            #if 'omplete' not in title.get('status'):
            if title.get('status').strip() not in ['completed','complete','Completed','Complete','COMPLETE','COMPLETED','Completed-BILLED','COMPLETED-BILLED'] and title.get('code') in my.title_proj_counts.keys():
                #print '%s got in' % title.get('code')
                #print title.get('code')
                title_active = 0
                title_inactive = 0
                char_checks = my.name_char_check(title)
                order_proj_checkdata = {}
                order_only_checkdata = {}
                proj_wo_checkdata = {}
                order_name = my.order.get('name')
                if order_name:
                    proj_wo_checkdata['order_name'] = order_name
                if len(char_checks[1]) > 0:
                    for cc in char_checks[1]:
                        errors.append(cc)
                title_title = title.get('title')
                if title_title not in [None,'']:
                    proj_wo_checkdata['title'] = title_title
                title_episode = title.get('episode')
                if title_episode not in [None,'']:
                    proj_wo_checkdata['episode'] = title_episode
                territory = title.get('territory')
                if territory in [None,'']:
                    errors.append(['Data Entry', '''%s's territory field is EMPTY. This should be filled in before proceeding.''' % title.get('code')])
                else:
                    proj_wo_checkdata['territory'] = territory
                platform = title.get('platform')
                if platform in [None,'']:
                    errors.append(['Data Entry', '''%s's platform field is EMPTY. This should be filled in before proceeding.''' % title.get('code')])
                else:
                    order_proj_checkdata['platform'] = platform
                if classification not in ['master','Master']:
                    expected_delivery_date = title.get('expected_delivery_date')
                    if expected_delivery_date in [None,'']:
                        errors.append(['Data Entry', '''%s's expected_delivery_date field is EMPTY. This should be filled in before proceeding.''' % title.get('code')])
                    else:
                        order_only_checkdata['expected_delivery_date'] = expected_delivery_date
                        erm_int = int(expected_delivery_date.split(' ')[0].replace('-',''))
                        if int(str(my.date_int)[0:6]) > int(str(erm_int)[0:6]):
                            errors.append(['Date Questionable','''%s's expected_delivery_date is set to a time before this month. It probably shouldn't be like that. Make sure it's what you want.''' % title.get('code')])
                    due_date = title.get('due_date')
                    if due_date in [None,'']:
                        errors.append(['Data Entry', '''%s's due_date field is EMPTY. This should be filled in before proceeding.''' % title.get('code')])
                    else:
                        order_proj_checkdata['due_date'] = due_date
                        dd_int = int(due_date.split(' ')[0].replace('-','')) 
                        if my.date_int > dd_int:
                            errors.append(['Date Questionable','''%s's due_date is set to a time that has passed. That can't be right. Please correct this before continuing.''' % title.get('code')])
                    start_date = title.get('start_date')
                    if start_date in [None,'']:
                        errors.append(['Data Entry', '''%s's start_date field is EMPTY. This should be filled in before proceeding.''' % title.get('code')])
                    else:
                        order_proj_checkdata['start_date'] = start_date
                        sd_int = int(start_date.split(' ')[0].replace('-',''))
                        if my.date_int > sd_int:
                            errors.append(['Date Questionable','''%s's start_date is set to a time that has passed. Please correct this before continuing.''' % title.get('code')])
                    expected_price = title.get('expected_price')
                    if expected_price in [None,'']:
                        errors.append(['Data Entry Optional', '''%s's expected_price field is EMPTY. Please set it when that information becomes available.''' % title.get('code')])
                    else:
                        expected_price_check = my.numbers_only(title.get('code'), 'expected_price', expected_price)
                        if expected_price_check[0]:
                            epc = '%.2f' % float(str(expected_price_check[3]))
                            oep = '%.2f' % float(my.fix_num(str(expected_price)))
                            #print "EPC = %s, OEP = %s" % (epc, oep)
                            if epc != oep:
                            #    my.server.update(title.get('__search_key__'), {'expected_price': expected_price_check[2]})
                                errors.append(['Number Format','''%s's expected_price has incorrect formatting (%s). Should it instead be this?: %s''' % (title.get('code'), str(expected_price), str(expected_price_check[2]))])
                        else:
                            for ep in expected_price_check[1]:
                                errors.append(ep)
                    client_name = title.get('client_name')
                    if client_name in [None,'']:
                        errors.append(['Data Entry', '''%s's client_name field is EMPTY. This should be filled in before proceeding.''' % title.get('code')])
                    else:
                        order_proj_checkdata['client_name'] = client_name
                    client_code = title.get('client_code')
                    if client_code in [None,'']:
                        errors.append(['Data Entry', '''%s's client_code field is EMPTY. This should be filled in before proceeding.''' % title.get('code')])
                    else:
                        order_proj_checkdata['client_code'] = client_code
                    title_id_number = title.get('title_id_number')
                    if title_id_number in [None,'']:
                        errors.append(['Data Entry Optional', '''%s's title_id_number field is EMPTY. This is optional, as it is unnecessary for many titles. Just a heads up that the field is empty..''' % title.get('code')])
                    else:
                        proj_wo_checkdata['title_id_number'] = title_id_number
                    #############################################
                    for key, val in order_only_checkdata.iteritems():
                        if key == 'expected_delivery_date':
                            #print "EX REV MO = %s" % my.order.get('expected_delivery_date')
                            if my.order.get('expected_delivery_date') not in [None,'']:
                                oval_int = int(my.order.get('expected_delivery_date').split(' ')[0].replace('-',''))
                                val_int = int(val.split(' ')[0].replace('-',''))
                                if int(str(val_int)[0:6]) != int(str(oval_int)[0:6]):
                                    errors.append(['Mismatch','''%s's %s (%s) does not match %s's %s (%s)''' % (title.get('code'), key, val, my.order.get('code'), key, my.order.get(key))])
                        else:
                            if val != my.order.get(key):
                                errors.append(['Mismatch','''%s's %s (%s) does not match %s's %s (%s)''' % (title.get('code'), key, val, my.order.get('code'), key, my.order.get(key))])
                for key, val in order_proj_checkdata.iteritems():
                    if val != my.order.get(key):
                        errors.append(['Mismatch','''%s's %s (%s) does not match %s's %s (%s)''' % (title.get('code'), key, val, my.order.get('code'), key, my.order.get(key))])
                for p in my.projs:
                    if p.get('title_code') == title.get('code'):
                        #print p.get('code')
                        proj_char_checks = my.name_char_check(p)
                        if len(char_checks[1]) > 0:
                            for cc in proj_char_checks[1]:
                                errors.append(cc) 
                        for key, val in order_proj_checkdata.iteritems():
                            if val != p.get(key):
                                errors.append(['Mismatch','''%s's %s (%s) does not match %s's %s (%s)''' % (p.get('code'), key, p.get(key), title.get('code'), key, val)])
                        for key, val in proj_wo_checkdata.iteritems():
                            if val != p.get(key):
                                errors.append(['Mismatch','''%s's %s (%s) does not match %s's %s (%s)''' % (p.get('code'), key, p.get(key), title.get('code'), key, val)])
                        parent_hackup = "Manually Inserted into %s" % title.get('pipeline_code')
                        if p.get('parent_pipe') != title.get('pipeline_code') and p.get('parent_pipe') != parent_hackup:
                            errors.append(['Internal Error','''%s's parent_pipe does not match %s's pipeline_code. Contact Admin to resolve.''' % (p.get('code'), title.get('code'))])
                        if p.get('templ_me') in [True,'t',1,'1'] and classification not in ['master','Master']:
                            errors.append(['Templating Problem','''%s is set to be templated. This should not occur in anything other than a Master Order. Please report this to the Admin.''' % p.get('code')])
                        if p.get('task_code') in [None,''] and classification not in ['master','Master']:
                            errors.append(['Internal Error','''%s's task_code is empty. Contact Admin to resolve''' % p.get('code')])
                    # Need to check all tasks to make sure the fields match
                    for pt in my.ptasks:
                        if pt.get('lookup_code') == p.get('code'):
                            # now need to check all fields
                            if pt.get('assigned_login_group') in [None,'']:
                                errors.append(['Login Group Important','''%s's does not have an 'assigned_login_group'. This should be set so the correct departments will see the work.''' % p.get('code')]) 
                            for task_field, proj_field in my.pt_checkdata.iteritems():
                                if pt.get(task_field) != p.get(proj_field):
                                    errors.append(['Mismatch', '''%s's %s (%s) does not match %s's %s (%s)''' % (p.get('code'), proj_field, p.get(proj_field), pt.get('code'), task_field, pt.get(task_field))])
                            if pt.get('proj_code') != p.get('code'):
                                errors.append(['Mismatch','''%s's code does not match %s's proj_code''' % (p.get('code'), pt.get('code'))])
                            if pt.get('tripwire') not in [None,'']:
                                errors.append(['Internal Stuck Var','''%s has a tripwire set (for %s). Please report this to the Admin.''' % (pt.get('code'), pt.get('lookup_code'))])
                            if pt.get('closed'):
                                errors.append(['Task Closed','''%s has been closed. This should not be closed already. Please report this to the Admin.''' % pt.get('code')])
                            if pt.get('transfer_wo') not in [None,'']:
                                errors.append(['Internal Error','''%s's transfer_wo field is not empty, though it should be. Please report this to the Admin.''' % pt.get('code')])
                            if pt.get('creator_login') in [None,'']:
                                errors.append(['Association Broken','''%s's creator_login field is empty. It should be associated with the creator. Please report this to the Admin.''' % pt.get('code')])
                            if pt.get('active') in [True,'t',1,'1']:
                                title_active = title_active + 1
                            else:
                                title_inactive = title_inactive + 1
                            if pt.get('pipeline_code') in [None,''] and classification not in ['master','Master']:
                                errors.append(['Unconnected Task','''%s's pipeline_code is empty. Please report this to the Admin.''' % pt.get('code')])
                        elif pt.get('lookup_code') in [None,''] and classification not in ['master','Master']:
                            errors.append(['Unconnected Task','''%s does not have a lookup_code, and therefore will not work with the triggering system. Contact Admin to resolve.''' % pt.get('code')])
                    for wo in my.wos:
                        if wo.get('proj_code') == p.get('code'):
                            #print wo.get('code')
                            wo_char_checks = my.name_char_check(wo)
                            if len(char_checks[1]) > 0:
                                for cc in wo_char_checks[1]:
                                    errors.append(cc) 
                            if wo.get('templ_me') in [True,'t',1,'1'] and classification not in ['master','Master']:
                                errors.append(['Templating Problem','''%s is set to be templated. This should not occur in anything other than a Master Order. Please report this to the Admin.''' % wo.get('code')])
                            if wo.get('instructions') in [None,'']:
                                errors.append(['Data Entry Optional','''%s's has no instructions. Some Work Orders don't need them. Just a head's up.''' % wo.get('code')])
                            parent_hackup = "Manually Inserted into %s" % p.get('pipeline_code')
                            if wo.get('parent_pipe') != p.get('pipeline_code') and parent_hackup != wo.get('parent_pipe'):
                                errors.append(['Internal Error','''%s's parent_pipe does not match %s's pipeline_code. Contact Admin to resolve.''' % (wo.get('code'), p.get('code'))])
                            if wo.get('closed'):
                                errors.append(['Task Closed','''%s has been closed. This should not be closed already. Please report this to the Admin.''' % wo.get('code')])
                            if wo.get('priority') != p.get('priority'):
                                errors.append(['Mismatch','''%s's priority (%s) does not match %s's priority (%s). Please report this to the Admin.''' % (wo.get('code'), wo.get('priority'), p.get('code'), p.get('priority'))])
                            if wo.get('task_code') in [None,''] and classification not in ['master','Master']:
                                errors.append(['Internal Error','''%s's task_code is empty. Contact Admin to resolve.''' % wo.get('code')])
                            if wo.get('work_group') in [None,'']:
                                errors.append(['Login Group Assignment','''%s does not have a 'work_group'. This must be set so the correct departments will see the work.''' % wo.get('code')]) 
                                #errors.append(['Data Entry','''%s's work_group is empty. This should be filled in before proceeding.''' % wo.get('code')])
                            if wo.get('estimated_work_hours') in [None,'']:
                                #print "%s's %s EST WH EMPTY" % (title.get('code'), wo.get('code'))
                                errors.append(['Data Entry','''%s's estimated_work_hours is empty. This should be filled in before proceeding.''' % wo.get('code')])
                            else:
                                ewh_check = my.numbers_only(wo.get('code'), 'estimated_work_hours', wo.get('estimated_work_hours'))
                                if ewh_check[0]:
                                    eck = '%.2f' % float(str(ewh_check[3]))
                                    eswh = '%.2f' % float(my.fix_num(wo.get('estimated_work_hours')))
                                    #print "ECk = %s, ESWH = %s" % (eck, eswh)
                                    if eck != eswh:
                                        #my.server.update(wo.get('__search_key__'), {'estimated_work_hours': ewh_check[2]})
                                        errors.append(['Number Format','''%s's estimated_work_hours has incorrect formatting (%s). Should it instead be this?: %s''' % (wo.get('code'), wo.get('estimated_work_hours'), str(ewh_check[2]))])
                                    if ewh_check[2] > 15:
                                        errors.append(['Unlikely Hours','''%s's estimated_work_hours value (%s) is very large. Are you sure you entered hours instead of minutes?''' % (wo.get('code'), ewh_check[2])])
                                    elif ewh_check[2] < .1:
                                        errors.append(['Unlikely Hours','''%s's estimated_work_hours value (%s) is very small. Are you sure you entered the correct number?''' % (wo.get('code'), ewh_check[2])])
                                else:
                                    for ep in ewh_check[1]:
                                        errors.append(ep)
                            for key, val in proj_wo_checkdata.iteritems():
                                if val != wo.get(key):
                                    errors.append(['Mismatch','''%s's %s (%s) does not match %s's %s (%s)''' % (wo.get('code'), key, wo.get(key), title.get('code'), key, val)])
                            for key, val in order_proj_checkdata.iteritems():
                                if val != wo.get(key):
                                    errors.append(['Mismatch','''%s's %s (%s) does not match %s's %s (%s)''' % (wo.get('code'), key, wo.get(key), title.get('code'), key, val)])
                            for wt in my.wtasks:
                                if wt.get('lookup_code') == wo.get('code'):
                                    if wt.get('assigned_login_group') in [None,'']:
                                        errors.append(['Login Group Assignment','''%s does not have an 'assigned_login_group'. This must be set so the correct departments will see the work.''' % wt.get('code')]) 
                                    elif wt.get('assigned_login_group') != wo.get('work_group'):
                                        errors.append(['Internal Error', '''%s's assigned_login_group does not match %s's work_group. Please report this to the Admin.''' % (wt.get('code'), wo.get('code'))])
                                    for task_field, wo_field in my.wt_checkdata.iteritems():
                                        if wt.get(task_field) != wo.get(wo_field):
                                            errors.append(['Mismatch', '''%s's %s (%s) does not match %s's %s (%s)''' % (wo.get('code'), wo_field, wo.get(wo_field), wt.get('code'), task_field, wt.get(task_field))])
                                    if wt.get('proj_code') != p.get('code'):
                                        errors.append(['Mismatch','''%s's proj_code does not match %s's proj_code''' % (wt.get('code'), wo.get('code'))])
                                    if wt.get('tripwire') not in [None,'']:
                                        errors.append(['Internal Stuck Var','''%s has a tripwire set (for %s). Please report this to the Admin.''' % (wt.get('code'), wt.get('lookup_code'))])
                                    if wt.get('closed'):
                                        errors.append(['Task Closed','''%s has been closed. This should not be closed already. Please report this to the Admin.''' % wt.get('code')])
                                    if wt.get('transfer_wo') not in [None,'']:
                                        errors.append(['Internal Error','''%s's transfer_wo field is not empty, though it should be. Please report this to the Admin.''' % wt.get('code')])
                                    if wt.get('creator_login') in [None,'']:
                                        errors.append(['Association Broken','''%s's creator_login field is empty. It should be associated with the creator. Please report this to the Admin.''' % wt.get('code')])
                                    if wt.get('active') in [True,'t',1,'1']:
                                        title_active = title_active + 1
                                    else:
                                        title_inactive = title_inactive + 1
                                    if wt.get('pipeline_code') in [None,''] and classification not in ['master','Master']:
                                        errors.append(['Unconnected Task','''%s's pipeline_code is empty. Please report this to the Admin.''' % wt.get('code')])
                                    #if wt.get('bid_duration') != wo.get('estimated_work_hours'):
                                    #    errors.append(['Internal Error','''%s's bid_duration (%s) does not match %s's estimated_work_hours (%s). Please report this to the Admin.''' % (wt.get('code'), wt.get('bid_duration'), wo.get('code'), wo.get('estimated_work_hours'))])
                                elif wt.get('lookup_code') in [None,''] and classification not in ['master','Master']:
                                    errors.append(['Unconnected Task',''''%s does not have a lookup_code, and therefore will not work with the triggering system. Contact Admin to resolve.''' % wt.get('code')])
                            for eq in my.equs:
                                if eq.get('work_order_code') == wo.get('code'):
                                    #print eq.get('code')
                                    if eq.get('units') in [None,'']:
                                        errors.append(['Data Entry','''%s's %s has an empty unit field. This should be filled in before proceeding.''' % (wo.get('code'), eq.get('name'))])
                                    if eq.get('expected_duration') in [None,'']:
                                        errors.append(['Data Entry Optional','''%s's %s has an empty expected_duration. This should be filled in before proceeding.''' % (wo.get('code'), eq.get('name'))])
                                    else:
                                        ex_dur = eq.get('expected_duration')
                                        dur_check = my.numbers_only(eq.get('code'), 'expected_duration', eq.get('expected_duration'))
                                        if dur_check[0]:
                                            dc1 = '%.2f' % float(my.fix_num(str(dur_check[3])))
                                            dc2 = '%.2f' % float(my.fix_num(str(ex_dur)))
                                            #print "DC1 = %s, DC2 = %s" % (dc1, dc2)
                                            if dc1 != dc2:
                                                #my.server.update(eq.get('__search_key__'), {'expected_duration': dur_check[2]})
                                                errors.append(['Number Format','''%s's expected_duration has incorrect formatting (%s). Should it instead be this?: %s''' % (eq.get('code'), eq.get('expected_duration'), str(dur_check[2]))])
                                        else:
                                            for dc in dur_check[1]:
                                                errors.append(dc)
                                    if eq.get('expected_quantity') in [None,'']:
                                        errors.append(['Data Entry','''%s's %s has an empty expected_quantity. This should be filled in before proceeding.''' % (wo.get('code'), eq.get('name'))])
                                    else:
                                        ex_quan = eq.get('expected_quantity')
                                        quan_check = my.numbers_only(eq.get('code'), 'expected_quantity', eq.get('expected_quantity'))
                                        if quan_check[0]:
                                            qc1 = '%.2f' % float(str(quan_check[3]))
                                            qc2 = '%.2f' % float(my.fix_num(str(ex_quan)))
                                            #print "QC1 = %s, QC2 = %s" % (qc1, qc2)
                                            if qc1 != qc2:
                                                #my.server.update(eq.get('__search_key__'), {'expected_quantity': quan_check[2]})
                                                errors.append(['Number Format','''%s's expected_quantity has incorrect formatting (%s). Should it instead be this?: %s''' % (eq.get('code'), eq.get('expected_quantity'), str(quan_check[2]))])
                                        else:
                                            for qc in quan_check[1]:
                                                errors.append(qc)
                                elif eq.get('work_order_code') in [None,'']:
                                    errors.append(['Unconnected Equipment','''%s does not have a work_order_code, and is therefore detached. Contact Admin to resolve.''' % eq.get('code')])
                               
                                        
                                    
                        
                            # Need to look at the equipment here
                my.active_tasks = my.active_tasks + title_active 
                my.inactive_tasks = my.inactive_tasks + title_inactive 
                if title_active * title_inactive != 0:    
                    errors.append(['Partially Active','''Title %s has %s active tasks and %s inactive tasks. FIX: Set your Order's classification to 'Bid', then save. Then set it to 'In Production' and save.''' % (title.get('code'), title_active, title_inactive)])
            
        return errors

    def travel_tree(my, focus, otree, parent_code, root_line):
        errors = []
        outs = otree[focus]['outs']
        #print "FOCUS = %s, Root_line = %s" % (focus, root_line)
        if focus in root_line:
            last_entered = root_line[len(root_line) - 1]
            errors.append(['Infinite Loop Detected','''%s's pipeline contains an infinite loop. "%s" (%s) is being looped back into from "%s" (%s). Contact Admin if you need help fixing this.''' % (parent_code, otree[focus]['process'], focus, otree[last_entered]['process'], last_entered)])
        else:
            for out in outs:
                new_root_line = []
                for rl in root_line:
                    new_root_line.append(rl)
                new_root_line.append(focus)
                new_errors = my.travel_tree(out, otree, parent_code, new_root_line)
                for err in new_errors:
                    errors.append(err)
        return errors
            
    def add_to_root_line(my, focus, otree, parent_code, rl, level):
        new_level = level + 1 
        errors = []
        outs = otree[focus]['outs']
        #print "OUTS for %s: %s" % (focus, outs)
        for out in outs: 
            #print "Is %s in %s?   LEVEL: %s" % (out, rl, level)
            if len(otree[out]['outs']) > 0:
                if out not in rl:
                    rl.append(out)
                    new_errors = my.add_to_root_line(out, otree, parent_code, rl, new_level)
                    #print "NEW ERRORS = %s" % new_errors
                    for error in new_errors:
                        errors.append(error)
                else:
                    #print '''%s's pipeline contains an infinite loop. "%s" (%s) is being looped back into from "%s" (%s). Contact Admin if you need help fixing this.''' % (parent_code, otree[out]['process'], out, otree[focus]['process'], focus)
                    #print "FOCUS = %s, OUTS= %s" % (focus,outs)
                    errors.append(['Infinite Loop Detected','''%s's pipeline contains an infinite loop. "%s" (%s) is being looped back into from "%s" (%s). Contact Admin if you need help fixing this.''' % (parent_code, otree[out]['process'], out, otree[focus]['process'], focus)])
                    #print "APPENDING ERROR = %s" % errors
        #print "RL2 = %s" % rl 
        return errors

    def pipe_check(my, obj):
        from pyasm.biz import Pipeline, Task
        errors = []
        o_sk = obj.get('__search_key__')
        o_st = o_sk.split('?')[0]
        if o_st == 'twog/title':
            wo_count = my.server.eval("@COUNT(twog/proj['title_code','%s'].twog/work_order)" % obj.get('code'))
            if wo_count > 1:
                qc_wo_count = my.server.eval("@COUNT(twog/proj['title_code','%s'].twog/work_order['work_group','in','qc|qc supervisor'])" % obj.get('code'))
                if qc_wo_count == 0:
                    errors.append(['Need At Least 1 QC WO','''%s's pipeline has no QC Work Orders. It needs at least 1.''' % obj.get('code')]) 
        kid_st_dict = {'twog/title': ['twog/proj', 'title_code', 'PROJ', 'project'], 'twog/proj': ['twog/work_order', 'proj_code', 'WORK_ORDER', 'work order']}
        kid_st, kid_parent_link, matcher, kid_type = kid_st_dict[o_st]
        ocode = obj.get('code')
        o_pipe_code = obj.get('pipeline_code')
        o_pipe = my.server.eval("@SOBJECT(sthpw/pipeline['code','%s'])" % o_pipe_code)
        if o_pipe:
            o_pipe = o_pipe[0]
            opipe_obj = Pipeline.get_by_name(o_pipe_code)
            oprocesses = opipe_obj.get_process_names()
            kid_objs = my.server.eval("@SOBJECT(%s['%s','%s'])" % (kid_st, kid_parent_link, ocode))
            #print "OPROCESSES = %s" % oprocesses
            otree = {}
            #if o_pipe.get('login') != my.user_name:
            #    errors.append(['Sharing Pipeline','''%s (%s) owner is: %s. Shared pipelines may have adverse effects. Recommend that you clone the pipeline and use that one instead.''' % (ocode, o_pipe_code, o_pipe.get('login'))]) 
            o_name_count = {}
            for kid in kid_objs:
                if kid.get('process') not in o_name_count.keys():
                    o_name_count[kid.get('process')] = 1
                else:
                    o_name_count[kid.get('process')] = o_name_count[kid.get('process')] + 1
            #print "O_NAME_COUNT = %s" % o_name_count
            for key, val in o_name_count.iteritems():
                if val > 1:
                    errors.append(['Duplicate Process Name','''%s has %s %ss named "%s". This is not advised, as it can cause triggering problems and confusion for operators.''' % (ocode, val, kid_type, key)])
            for kid in kid_objs:
                kcode = kid.get('code')
                if ocode == kid.get(kid_parent_link):
                    kprocess = kid.get('process')
                    if kcode not in otree.keys():
                        otree[kcode] = {'ins': [], 'pins': [], 'outs': [], 'pouts': [], 'position': '', 'type': '', 'process': kprocess}
            deld_skss = []
            for kid in kid_objs:
                kcode = kid.get('code')
                if ocode == kid.get(kid_parent_link):
                    kprocess = kid.get('process')
                    otree[kcode]['type'] = 'hackup'
                    hack_ins = my.server.eval("@SOBJECT(twog/hackpipe_out['out_to','%s'])" % kid.get('code'))
                    for hi in hack_ins:
                        if hi.get('__search_key__') not in deld_skss:
                            if hi.get('out_to') not in my.combo_codes or hi.get('lookup_code') not in my.combo_codes:
                                my.server.delete_sobject(hi.get('__search_key__'))
                                deld_skss.append(hi.get('__search_key__'))
                            else:
                                if matcher in hi.get('lookup_code'):
                                    if hi.get('lookup_code') not in otree[kcode]['ins']:
                                        otree[kcode]['ins'].append(hi.get('lookup_code'))
                                    if kcode not in otree[hi.get('lookup_code')]['outs']:
                                        otree[hi.get('lookup_code')]['outs'].append(kcode)
                    hack_outs = my.server.eval("@SOBJECT(twog/hackpipe_out['lookup_code','%s'])" % kid.get('code'))
                    for ho in hack_outs:
                        if ho.get('__search_key__') not in deld_skss:
                            if ho.get('out_to') not in my.combo_codes or ho.get('lookup_code') not in my.combo_codes:
                                my.server.delete_sobject(ho.get('__search_key__'))
                                deld_skss.append(ho.get('__search_key__'))
                            else:
                                if matcher in ho.get('out_to'):
                                    if ho.get('out_to') not in otree[kcode]['outs']:
                                        otree[kcode]['outs'].append(ho.get('out_to'))
                                    if kcode not in otree[ho.get('out_to')]['ins']:
                                        otree[ho.get('out_to')]['ins'].append(kcode)
                    if kprocess in oprocesses:
                        kinfo = my.server.get_pipeline_processes_info(o_sk, related_process=kprocess)
                        #print "KINFO for %s, process = %s: %s" % (o_pipe_code, kprocess, kinfo)  
                        kin_ins = kinfo.get('input_processes')
                        for ki in kin_ins:
                            if ki in oprocesses: #
                                for kd in kid_objs:
                                    if ki == kd.get('process'):
                                        if kd.get('code') not in otree[kcode]['ins']:
                                            otree[kcode]['ins'].append(kd.get('code'))
                                            otree[kcode]['pins'].append(kd.get('code'))
                                        if kcode not in otree[kd.get('code')]['outs']:
                                            otree[kd.get('code')]['outs'].append(kcode)
                                            otree[kd.get('code')]['pouts'].append(kcode)
                        kin_outs = kinfo.get('output_processes')
                        for ko in kin_outs:
                            if ko in oprocesses: #
                                for kd in kid_objs:
                                    if ko == kd.get('process'):
                                        if kd.get('code') not in otree[kcode]['outs']:
                                            otree[kcode]['outs'].append(kd.get('code'))
                                            otree[kcode]['pouts'].append(kd.get('code'))
                                        if kcode not in otree[kd.get('code')]['ins']:
                                            otree[kd.get('code')]['ins'].append(kcode)
                                            otree[kd.get('code')]['pins'].append(kcode)
                        otree[kcode]['type'] = 'normal'
                 
            #print "OTREE = %s" % otree        
            roots = []
            leafs = []
            proots = []
            for kcode, kdict in otree.iteritems():
                if len(kdict['ins']) == 0:
                    otree[kcode]['position'] = 'root'
                    roots.append(kcode)
                if len(kdict['pins']) == 0 and kdict['type'] != 'hackup':
                    proots.append(kcode)
                if len(kdict['outs']) == 0:
                    otree[kcode]['position'] = 'leaf'
                    leafs.append(kcode)
            #print "ROOTS = %s" % roots                
            #print "Code = %s" % ocode
            #new_errors = my.add_to_root_line(root, otree, ocode, root_line, 0)
            for rt in roots:
                new_errors = my.travel_tree(rt, otree, ocode, [])#root_line)
                seen_errs = []
                for error in new_errors:
                    if error[1] not in seen_errs:
                        seen_errs.append(error[1])
                        errors.append(error)
            if len(roots) == 0 and len(kid_objs) > 0:
                if len(proots) > 0:
                    proot_str = ''
                    for pr in proots:
                        if proot_str == '':
                            proot_str = '"%s" (%s)' % (otree[pr]['process'], pr)
                        else:
                            proot_str = '%s, "%s" (%s)' % (proot_str, otree[pr]['process'], pr)
                    errors.append(['Infinite Loop Detected','''%s's pipeline contains an infinite loop. One of these %ss seems like it should be the beginning of the pipeline, but something is looping back into it: %s. Contact Admin if you need help fixing this.''' % (ocode, kid_type, proot_str)])
                else:
                    errors.append(['Infinite Loop Detected','''%s's pipeline contains an infinite loop amongst the %ss. The location of the loop cannot be resolved. Contact Admin to investigate..''' % (ocode, kid_type)])
        else:
            #if o_pipe_code != 'NOTHINGXsXNOTHING':
            #    errors.append(['Pipeline Missing','''%s's pipeline (%s) cannot be found. It may have had it's name changed, or could have been deleted or retired. Contact Admin to resolve.''' % (ocode, o_pipe_code)])
            if o_pipe_code == 'No Pipeline Assigned' or o_pipe_code == 'NOTHINGXsXNOTHING':
                errors.append(['Pipeline Unassigned','''%s's has no pipeline assigned. It needs a pipeline. Manual Insertions alone are not allowed.''' % (ocode)])
                #print "NO PIPELINE ASSIGNED"
            else:
                errors.append(['Pipeline Missing','''%s's pipeline (%s) cannot be found. It may have had it's name changed, or could have been deleted or retired. Contact Admin to resolve.''' % (ocode, o_pipe_code)])
        return errors

    def return_error_count_dict(my): 
        my.sk = str(my.kwargs.get('sk'))
        my.code = my.sk.split('code=')[1]
        my.order_code = my.code
        order_expr = "@SOBJECT(twog/order['code','%s'])" % my.code
        order = my.server.eval(order_expr)
        is_master = True 
        if order:
            my.order = order[0]
            order = None
            if my.order.get('classification') not in ['master','Master']:
                is_master = False

        if my.order:
            my.titles = my.server.eval("@SOBJECT(twog/title['order_code','%s'])" % my.order_code)
            my.projs = my.server.eval("@SOBJECT(twog/title['order_code','%s'].twog/proj)" % my.order_code)
            my.ptasks = my.server.eval("@SOBJECT(twog/title['order_code','%s'].twog/proj.PT:sthpw/task)" % my.order_code)
            my.wos = my.server.eval("@SOBJECT(twog/title['order_code','%s'].twog/proj.twog/work_order)" % my.order_code)
            my.wtasks = my.server.eval("@SOBJECT(twog/title['order_code','%s'].twog/proj.twog/work_order.WT:sthpw/task)" % my.order_code)
            my.equs = my.server.eval("@SOBJECT(twog/title['order_code','%s'].twog/proj.twog/work_order.twog/equipment_used)" % my.order_code)
            for p in my.projs:
                my.proj_codes.append(p.get('code'))
                my.combo_codes.append(p.get('code'))
                ptcode = p.get('title_code')
                if ptcode not in my.title_proj_counts.keys():
                    my.title_proj_counts[ptcode] = 1
                else:
                    my.title_proj_counts[ptcode] = my.title_proj_counts[ptcode] + 1
            for w in my.wos:
                my.wo_codes.append(w.get('code'))
                my.combo_codes.append(w.get('code'))
        my.pipe_errors = []
        for title in my.titles:
            #print "ERRCT %s Status = %s" % (title.get('code'), title.get('status'))
            #if 'omplete' not in title.get('status'):
            if title.get('status').strip() not in ['completed','complete','Completed','Complete','COMPLETE','COMPLETED','Completed-BILLED','COMPLETED-BILLED'] and title.get('code') in my.title_proj_counts.keys():
                #print '%s got in' % title.get('code')
                #print "%s Pipe Check" % title.get('code')
                new_errors = my.pipe_check(title)
                for error in new_errors:
                    my.pipe_errors.append(error)
                tprojs = my.server.eval("@SOBJECT(twog/proj['title_code','%s'])" % title.get('code'))
                for tp in tprojs:
                    #print "%s Pipe Check" % tp.get('code')
                    wo_errors = my.pipe_check(tp)
                    for error in wo_errors:
                        my.pipe_errors.append(error)

        my.order_field_errors = my.do_order_field_check() # Need to complete
        my.field_errors = my.do_field_checks()
        for rrr in my.pipe_errors:
            color = my.label_colors[rrr[0]]
            my.color_counter[color[2]] = my.color_counter[color[2]] + 1 
        for rrr in my.order_field_errors:
            color = my.label_colors[rrr[0]]
            my.color_counter[color[2]] = my.color_counter[color[2]] + 1 
        fix_partials = False
        for rrr in my.field_errors:
            color = my.label_colors[rrr[0]]
            if rrr[0] == 'Partially Active':
                fix_partials = True
            else:
                my.color_counter[color[2]] = my.color_counter[color[2]] + 1 
        count_dict = {}
        for hex, count in my.color_counter.iteritems():
            count_dict[my.reverse_dict[hex]] = count
        classification = my.order.get('classification')
        if fix_partials and count_dict['Critical'] == 0: 
            my.server.update(my.order.get('__search_key__'), {'classification': my.classification_switcher[classification]})
            my.server.update(my.order.get('__search_key__'), {'classification': classification})
        if classification in ['in_production','In Prodction'] and count_dict['Critical'] > 0:
            my.server.update(my.order.get('__search_key__'), {'classification': 'Bid'})
        return count_dict

    def get_display(my):   
        my.sk = str(my.kwargs.get('sk'))
        #print "MY SK = %s" % my.sk
        my.code = my.sk.split('code=')[1]
        my.order_code = my.code
        order_expr = "@SOBJECT(twog/order['code','%s'])" % my.code
        order = my.server.eval(order_expr)
        is_master = True 
        if order:
            my.order = order[0]
            order = None
            if my.order.get('classification') not in ['master','Master']:
                is_master = False

        if my.order:
            my.titles = my.server.eval("@SOBJECT(twog/title['order_code','%s'])" % my.order_code)
            my.projs = my.server.eval("@SOBJECT(twog/title['order_code','%s'].twog/proj)" % my.order_code)
            my.ptasks = my.server.eval("@SOBJECT(twog/title['order_code','%s'].twog/proj.PT:sthpw/task)" % my.order_code)
            my.wos = my.server.eval("@SOBJECT(twog/title['order_code','%s'].twog/proj.twog/work_order)" % my.order_code)
            my.wtasks = my.server.eval("@SOBJECT(twog/title['order_code','%s'].twog/proj.twog/work_order.WT:sthpw/task)" % my.order_code)
            my.equs = my.server.eval("@SOBJECT(twog/title['order_code','%s'].twog/proj.twog/work_order.twog/equipment_used)" % my.order_code)
            for p in my.projs:
                my.proj_codes.append(p.get('code'))
                my.combo_codes.append(p.get('code'))
                ptcode = p.get('title_code')
                if ptcode not in my.title_proj_counts.keys():
                    my.title_proj_counts[ptcode] = 1
                else:
                    my.title_proj_counts[ptcode] = my.title_proj_counts[ptcode] + 1
            for w in my.wos:
                my.wo_codes.append(w.get('code'))
                my.combo_codes.append(w.get('code'))
        #print "TITLES = %s" % my.titles
        #print "PROJS = %s" % my.projs
        #print "WOS = %s" % my.wos
        #print "EQUS = %s" % my.equs
        table = Table()
        #table.add_style('background-color: #ededff;')
        table.add_style('background-color: #e9e9e9;')
        #if is_master:
        #    table.add_row()
        #    table.add_cell("%s is a Master order. The Order Checker doesn't yet work on Masters." %  my.order.get('name'))
        #    return table

 
        #my.pipe_errors = my.do_pipe_checks()
        my.pipe_errors = []
        for title in my.titles:
            #print "DISP %s Status = %s" % (title.get('code'), title.get('status'))
            #if 'omplete' not in title.get('status'):
            if title.get('status').strip() not in ['completed','complete','Completed','Complete','COMPLETE','COMPLETED','Completed-BILLED','COMPLETED-BILLED'] and title.get('code') in my.title_proj_counts.keys():
                #print '%s got in' % title.get('code')
                #print "%s Pipe Check" % title.get('code')
                new_errors = my.pipe_check(title)
                for error in new_errors:
                    my.pipe_errors.append(error)
                tprojs = my.server.eval("@SOBJECT(twog/proj['title_code','%s'])" % title.get('code'))
                for tp in tprojs:
                    #print "%s Pipe Check" % tp.get('code')
                    wo_errors = my.pipe_check(tp)
                    for error in wo_errors:
                        my.pipe_errors.append(error)

        my.order_field_errors = my.do_order_field_check() # Need to complete
        my.field_errors = my.do_field_checks()
        for rrr in my.pipe_errors:
            color = my.label_colors[rrr[0]]
            my.color_counter[color[2]] = my.color_counter[color[2]] + 1 
        for rrr in my.order_field_errors:
            color = my.label_colors[rrr[0]]
            my.color_counter[color[2]] = my.color_counter[color[2]] + 1 
        fix_partials = False
        partial_errors = 0
        for rrr in my.field_errors:
            color = my.label_colors[rrr[0]]
            if rrr[0] == 'Partially Active':
                partial_errors = partial_errors + 1
                fix_partials = True
            else:
                my.color_counter[color[2]] = my.color_counter[color[2]] + 1 
        if fix_partials and my.color_counter[my.color_dict['Critical']] == 0: 
            classification = my.order.get('classification')
            my.server.update(my.order.get('__search_key__'), {'classification': my.classification_switcher[classification]})
            my.server.update(my.order.get('__search_key__'), {'classification': classification})
        elif fix_partials:
            my.color_counter[my.color_dict['Critical']] = my.color_counter[my.color_dict['Critical']] + partial_errors
        #print "NOW JUST DRAWING"
        table.add_style('font-size: 18px;') 
        table.add_row()
        code_cell = table.add_cell(my.order_code)
        code_cell.add_style('font-weight: bold;')
        code_cell.add_style('color: #FFFFFF;')
        code_cell.add_style('background-color: #000000;')
        spacer_cell1 = table.add_cell('&nbsp;&nbsp;&nbsp;') 
        spacer_cell1.add_style('background-color: #000000;')
        name_cell = table.add_cell('<font color="#FFFFFF">%s [</font><font color="%s">Critical: %s</font> <font color="%s">High: %s</font> <font color="%s">Mid: %s</font> <font color="%s">Low: %s</font><font color="#FFFFFF">]</font>' % (my.order.get('name'), my.color_dict['Critical'], my.color_counter[my.color_dict['Critical']], my.color_dict['High'], my.color_counter[my.color_dict['High']], my.color_dict['Mid'], my.color_counter[my.color_dict['Mid']], my.color_dict['Low'], my.color_counter[my.color_dict['Low']]))
        code_cell.add_attr('nowrap','nowrap')
        name_cell.add_attr('nowrap','nowrap')
        name_cell.add_style('font-weight: bold;')
        name_cell.add_style('background-color: #000000;')

        base_path = '/var/www/html/checker_errors/' 
        file_path = '%s/%s_error_log' % (base_path, my.date_int)
        log = None
        if os.path.exists(file_path):
            log = open(file_path, 'a')
        else:
            log = open(file_path, 'w')
        
        criticals_atop = False
        for porr in my.pipe_errors: 
            #print "PORR = %s" % porr
            color = my.label_colors[porr[0]]
            level = my.reverse_color_dict[color[2]]
            if level == 'Critical':
                criticals_atop = True
                table.add_row()
                err_type_cell = table.add_cell('%s%s%s' % (color[3], porr[0], color[4]))
                spacer_cell2 = table.add_cell('&nbsp;&nbsp;&nbsp;') 
                err_msg_cell = table.add_cell('%s%s%s' % (color[3], porr[1], color[4]))
                err_type_cell.add_attr('nowrap','nowrap')
                err_msg_cell.add_attr('nowrap','nowrap')
                err_type_cell.add_attr('height','100%')
                err_msg_cell.add_attr('height','100%')
                err_type_cell.add_attr('valign','center')
                err_msg_cell.add_attr('valign','center')
                err_type_cell.add_style('background-color: %s;' % color[2])
                spacer_cell2.add_style('background-color: %s;' % color[2])
                err_type_cell.add_style('padding-bottom: 5px;')
                spacer_cell2.add_style('padding-bottom: 5px;')
                err_msg_cell.add_style('padding-bottom: 5px;')
                err_type_cell.add_style('padding-top: 5px;')
                spacer_cell2.add_style('padding-top: 5px;')
                err_msg_cell.add_style('padding-top: 5px;')

        for rorr in my.order_field_errors: 
            #print "RORR = %s" % rorr
            color = my.label_colors[rorr[0]]
            level = my.reverse_color_dict[color[2]]
            if level == 'Critical':
                criticals_atop = True
                table.add_row()
                err_type_cell = table.add_cell('%s%s%s' % (color[3], rorr[0], color[4]))
                spacer_cell2 = table.add_cell('&nbsp;&nbsp;&nbsp;') 
                err_msg_cell = table.add_cell('%s%s%s' % (color[3], rorr[1], color[4]))
                err_type_cell.add_attr('nowrap','nowrap')
                err_msg_cell.add_attr('nowrap','nowrap')
                err_type_cell.add_attr('height','100%')
                err_msg_cell.add_attr('height','100%')
                err_type_cell.add_attr('valign','center')
                err_msg_cell.add_attr('valign','center')
                err_type_cell.add_style('background-color: %s;' % color[2])
                spacer_cell2.add_style('background-color: %s;' % color[2])
                err_type_cell.add_style('padding-bottom: 5px;')
                spacer_cell2.add_style('padding-bottom: 5px;')
                err_msg_cell.add_style('padding-bottom: 5px;')
                err_type_cell.add_style('padding-top: 5px;')
                spacer_cell2.add_style('padding-top: 5px;')
                err_msg_cell.add_style('padding-top: 5px;')
    
        for torr in my.field_errors: 
            color = my.label_colors[torr[0]]
            level = my.reverse_color_dict[color[2]]
            if level == 'Critical' and not (torr[0] == 'Partially Active' and my.color_counter[my.color_dict['Critical']] == 0):
                criticals_atop = True
                table.add_row()
                err_type_cell = table.add_cell('%s%s%s' % (color[3], torr[0], color[4]))
                spacer_cell2 = table.add_cell('&nbsp;&nbsp;&nbsp;') 
                err_msg_cell = table.add_cell('%s%s%s' % (color[3], torr[1], color[4]))
                err_type_cell.add_attr('nowrap','nowrap')
                err_msg_cell.add_attr('nowrap','nowrap')
                err_type_cell.add_attr('height','100%')
                err_msg_cell.add_attr('height','100%')
                err_type_cell.add_attr('valign','center')
                err_msg_cell.add_attr('valign','center')
                err_type_cell.add_style('background-color: %s;' % color[2])
                spacer_cell2.add_style('background-color: %s;' % color[2])
                err_type_cell.add_style('padding-bottom: 5px;')
                spacer_cell2.add_style('padding-bottom: 5px;')
                err_msg_cell.add_style('padding-bottom: 5px;')
                err_type_cell.add_style('padding-top: 5px;')
                spacer_cell2.add_style('padding-top: 5px;')
                err_msg_cell.add_style('padding-top: 5px;')

        if criticals_atop:
            table.add_row()
            table.add_cell('OTHER ERRORS BELOW')
    
        for porr in my.pipe_errors: 
            color = my.label_colors[porr[0]]
            level = my.reverse_color_dict[color[2]]
            log.write('''[%s %s]{%s} %s: %s\n''' % (my.order_code, my.timestamp, level, porr[0], porr[1]))
            table.add_row()
            err_type_cell = table.add_cell('%s%s%s' % (color[3], porr[0], color[4]))
            spacer_cell2 = table.add_cell('&nbsp;&nbsp;&nbsp;') 
            err_msg_cell = table.add_cell('%s%s%s' % (color[3], porr[1], color[4]))
            err_type_cell.add_attr('nowrap','nowrap')
            err_msg_cell.add_attr('nowrap','nowrap')
            err_type_cell.add_attr('height','100%')
            err_msg_cell.add_attr('height','100%')
            err_type_cell.add_attr('valign','center')
            err_msg_cell.add_attr('valign','center')
            err_type_cell.add_style('background-color: %s;' % color[2])
            spacer_cell2.add_style('background-color: %s;' % color[2])
            err_type_cell.add_style('padding-bottom: 5px;')
            spacer_cell2.add_style('padding-bottom: 5px;')
            err_msg_cell.add_style('padding-bottom: 5px;')
            err_type_cell.add_style('padding-top: 5px;')
            spacer_cell2.add_style('padding-top: 5px;')
            err_msg_cell.add_style('padding-top: 5px;')

        for rorr in my.order_field_errors: 
            color = my.label_colors[rorr[0]]
            level = my.reverse_color_dict[color[2]]
            log.write('''[%s %s]{%s} %s: %s\n''' % (my.order_code, my.timestamp, level, rorr[0], rorr[1]))
            table.add_row()
            err_type_cell = table.add_cell('%s%s%s' % (color[3], rorr[0], color[4]))
            spacer_cell2 = table.add_cell('&nbsp;&nbsp;&nbsp;') 
            err_msg_cell = table.add_cell('%s%s%s' % (color[3], rorr[1], color[4]))
            err_type_cell.add_attr('nowrap','nowrap')
            err_msg_cell.add_attr('nowrap','nowrap')
            err_type_cell.add_attr('height','100%')
            err_msg_cell.add_attr('height','100%')
            err_type_cell.add_attr('valign','center')
            err_msg_cell.add_attr('valign','center')
            err_type_cell.add_style('background-color: %s;' % color[2])
            spacer_cell2.add_style('background-color: %s;' % color[2])
            err_type_cell.add_style('padding-bottom: 5px;')
            spacer_cell2.add_style('padding-bottom: 5px;')
            err_msg_cell.add_style('padding-bottom: 5px;')
            err_type_cell.add_style('padding-top: 5px;')
            spacer_cell2.add_style('padding-top: 5px;')
            err_msg_cell.add_style('padding-top: 5px;')

        for torr in my.field_errors: 
            color = my.label_colors[torr[0]]
            level = my.reverse_color_dict[color[2]]
            if torr[0] == 'Partially Active' and my.color_counter[my.color_dict['Critical']] == 0:
                torr[0] = 'Partially Active Fixed'
                torr[1] = 'Auto Fixed: %s' % torr[1]
                color = my.label_colors[torr[0]]
                level = 'High' 
            log.write('''[%s %s]{%s} %s: %s\n''' % (my.order_code, my.timestamp, level, torr[0], torr[1]))
            table.add_row()
            err_type_cell = table.add_cell('%s%s%s' % (color[3], torr[0], color[4]))
            spacer_cell2 = table.add_cell('&nbsp;&nbsp;&nbsp;') 
            err_msg_cell = table.add_cell('%s%s%s' % (color[3], torr[1], color[4]))
            err_type_cell.add_attr('nowrap','nowrap')
            err_msg_cell.add_attr('nowrap','nowrap')
            err_type_cell.add_attr('height','100%')
            err_msg_cell.add_attr('height','100%')
            err_type_cell.add_attr('valign','center')
            err_msg_cell.add_attr('valign','center')
            err_type_cell.add_style('background-color: %s;' % color[2])
            spacer_cell2.add_style('background-color: %s;' % color[2])
            err_type_cell.add_style('padding-bottom: 5px;')
            spacer_cell2.add_style('padding-bottom: 5px;')
            err_msg_cell.add_style('padding-bottom: 5px;')
            err_type_cell.add_style('padding-top: 5px;')
            spacer_cell2.add_style('padding-top: 5px;')
            err_msg_cell.add_style('padding-top: 5px;')
        log.close()
        if my.order.get('classification') in ['in_production','In Production'] and my.color_counter[my.color_dict['Critical']] > 0:
            my.server.update(my.order.get('__search_key__'), {'classification': 'Bid'})
        # DO title source check. Each should have a source attached - check before implementing here
        return table

