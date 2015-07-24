__all__ = ["CostBuilderLauncherWdg","CostBuilder","CostTable","TitleCostRow","ProjCostRow","WorkOrderCostRow","EquipmentUsedCostRow","LaborCostRow","ProjPricingWdg","PriceWdg","CostTools","CBScripts"]
import tacticenv
from pyasm.common import Environment
from pyasm.biz import *
from pyasm.web import Table, DivWdg
from pyasm.widget import SelectWdg, IconWdg, TextWdg, CheckboxWdg
from tactic.ui.common import BaseTableElementWdg
from tactic.ui.common import BaseRefreshWdg
from tactic.ui.panel import EditWdg
from tactic.ui.widget.button_new_wdg import ButtonSmallNewWdg, ButtonRowWdg

class CostBuilderLauncherWdg(BaseTableElementWdg):

    def init(my):
        nothing = 'true'

    def get_launch_behavior(my, order_name):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                          var server = TacticServerStub.get();
                          var order_name = '%s';
                          var my_sk = bvr.src_el.get('sk');
                          var my_code = my_sk.split('code=')[1];
                          var my_user = bvr.src_el.get('user');
                          var class_name = 'cost_builder.cost_builder.CostBuilder';
                          kwargs = {
                                           'sk': my_sk,
                                           'user': my_user
                                   };
                          spt.tab.add_new('cost_builder_' + my_code, 'Cost Builder For ' + order_name, class_name, kwargs);
                }
                catch(err){
                          spt.app_busy.hide();
                          alert(err);
                }
         ''' % order_name}
        return behavior

    def get_display(my):
        sobject = my.get_current_sobject()
        code = sobject.get_code()
        order_name = sobject.get_value('name')
        sob_sk = sobject.get_search_key()
        sob_st = sobject.get_search_type().split('?')[0]
        sob_id = sobject.get_value('id')
        widget = DivWdg()
        table = Table()
        table.add_attr('width', '50px')
        login = Environment.get_login()
        user_name = login.get_login()
        table.add_row()
        cell1 =  table.add_cell('<img border="0" style="vertical-align: middle" title="" src="/context/icons/custom/dollar.png">')
        cell1.add_attr('sk', sob_sk)
        cell1.add_attr('search_type', sob_st)
        cell1.add_attr('user', user_name)
        launch_behavior = my.get_launch_behavior(order_name)
        cell1.add_style('cursor: pointer;')
        cell1.add_behavior(launch_behavior)
        widget.add(table)

        return widget

class CostBuilder(BaseRefreshWdg):
    def init(my):
        from client.tactic_client_lib import TacticServerStub
        from pyasm.common import Environment
        my.server = TacticServerStub.get()
        my.sk = ''
        my.user = '' 
        my.width = 1484
        my.ordered_groups = ['admin','development','technical services','it','management','sales supervisor','billing and accounts receivable','scheduling supervisor','qc supervisor','media vault supervisor','machine room supervisor','edit supervisor','compression supervisor','scheduling', 'sales','compression','edeliveries','edit','audio','executives','machine room','media vault','qc','office employees','streamz','vault','senior_staff']
        my.visibles =  {'admin': 'actual,estimate,price','development': 'actual,estimate,price', 'technical services': 'actual,estimate,price','it': 'actual,estimate,price', 'management': 'actual,estimate,price', 'sales supervisor': 'actual,estimate,price', 'billing and accounts receivable': 'actual,estimate,price', 'scheduling supervisor': 'actual,estimate,price', 'qc supervisor': 'actual,estimate,price', 'media vault supervisor': 'actual,estimate,price', 'machine room supervisor': 'actual,estimate,price', 'edit supervisor': 'actual,estimate,price', 'compression supervisor': 'actual,estimate,price', 'scheduling': 'actual,estimate,price', 'sales': 'actual,estimate,price', 'streamz': 'actual,estimate,price', 'compression': 'actual,estimate,price','edeliveries': 'actual,estimate,price', 'edit': 'actual,estimate,price', 'audio': 'actual,estimate,price', 'executives': 'actual,estimate,price', 'machine room': 'actual,estimate,price', 'media vault': 'actual,estimate,price', 'qc': 'actual,estimate,price', 'office employees': 'actual,estimate,price', 'vault': 'actual,estimate,price', 'senior_staff': 'actual,estimate,price'}
    
    def get_display(my):   
        my.sk = str(my.kwargs.get('sk'))
        my.user = str(my.kwargs.get('user'))
        #need to determine here what group they are in and pass the info along with the login along
        grp_expr = "@SOBJECT(sthpw/login_in_group['login','%s']['login_group','not in','client|user'])" % my.user
        groups = my.server.eval(grp_expr)
        top_group = ''
        top_num = 1000
        #print "GROUPS = %s" % groups
        for group in groups:
            grp_name = group.get('login_group')
            #print "GRP_NAME = %s" % grp_name
            this_num = my.ordered_groups.index(grp_name)
            #print "THIS_NUM = %s" % this_num
            if this_num < top_num:
                top_group = grp_name
                top_num = this_num
        code = my.sk.split('code=')[1]
        sob_expr = "@SOBJECT(twog/order['code','%s'])" % code
        sob = my.server.eval(sob_expr)[0]
        order_search_id = sob.get('id')
        table = Table()
        table.add_attr('cellspacing','0')
        table.add_attr('cellpadding','0')
        table.add_attr('class','twog_cost_builder twog_cost_builder_%s' % my.sk)
        table.add_attr('order_sk',my.sk)
        table.add_attr('client',sob.get('client_code'))
        table.add_attr('order_code',code)
        table.add_style('width: %spx;' % my.width)
        #table.add_style('width: 100%s;' % '%')
        top = Table()
        top.add_attr('width','100%s' % '%') 
        tool_row = top.add_row()
        tool_row.add_attr('toolrow','yep')
        tool_row.add_style('width: 100%s' % '%')
        tools = CostTools(order_sk=my.sk)
        top.add_cell(tools)
        toprow = table.add_row()
        toprow.add_style('width: 100%s;' % '%')
        tc2 = table.add_cell(top)
        tc2.add_style('width: 100%s;' % '%')
        wholerow = table.add_row()
        wholerow.add_attr('wholerow','yep')
        wholerow.add_style('width: 100%s' % '%')
        order_obj = CostTable(sk=my.sk, group=top_group, user=my.user, visibles=my.visibles[top_group]) 
        whole_order = Table()
        whole_order.add_row()
        whole = whole_order.add_cell(order_obj)
        whole.add_attr('class','whole_%s' % code)
        whole.add_attr('sk',my.sk)
        whole.add_attr('group',top_group)
        whole.add_attr('user',my.user)
        whole.add_attr('visibles',my.visibles[top_group])
        div = DivWdg()
        div.add_style('overflow-y: scroll;')
        div.add_style('height: 1000px;')
        div.add(whole_order)
        ord_cell = table.add_cell(div)
        cover_table = Table()
        cover_table.add_attr('class','twog_cost_builder_cover_%s' % my.sk)
        cover_table.add_row()
        cover_cell = cover_table.add_cell(table)
        cover_cell.add_attr('class','cover_cell')
        return cover_table

        
class CostTable(BaseRefreshWdg): 
    ''' This is the top level view of the dynamic cost builder part ''' 

    def init(my):
        from client.tactic_client_lib import TacticServerStub
        from pyasm.common import Environment
        my.server = TacticServerStub.get()
        my.search_type = 'twog/order'
        my.title = "Order"
        my.sk = ''
        my.user = ''
        my.group = ''
        my.visibles = ''
        my.division_length = 1 
        my.first_cell_length = 997
        my.full_length = 1484 - my.first_cell_length

    def get_display(my):   
        my.sk = str(my.kwargs.get('sk'))
        my.group = str(my.kwargs.get('group'))
        my.user = str(my.kwargs.get('user'))
        my.visibles = str(my.kwargs.get('visibles'))
        cb = CBScripts(order_sk=my.sk)
        divisions_count = len(my.visibles.split(','))
        my.division_length = 1484/divisions_count
        code = my.sk.split('code=')[1]
        main_obj = my.server.eval("@SOBJECT(twog/order['code','%s'])" % code)[0]
        titles_expr = "@SOBJECT(twog/title['order_code','%s'])" % (code)
        titles = my.server.eval(titles_expr)
        table = Table()
        table.add_attr('cellpadding','0')
        table.add_attr('cellspacing','0')
        #table.add_style('border-collapse', 'separate')
        #table.add_style('border-spacing', '25px 0px')
        table.add_style('color: #00033a;')
        table.add_style('background-color: #d9edf7;')
        table.add_style('width: 100%s;' % '%')
        table.add_style('border-bottom-right-radius', '10px')
        table.add_style('border-bottom-left-radius', '10px')
        table.add_style('border-top-right-radius', '10px')
        table.add_style('border-top-left-radius', '10px')
        table.add_style('font-size: 20px;')
        order_name_row = table.add_row()
        toggler = table.add_cell('<img border="0" style="vertical-align: middle" title="" src="/context/icons/custom/MinusIcon.png">')
        toggler.add_behavior(cb.get_toggle_bottom(my.sk))
        order_name_cell = table.add_cell('<b><u>Order: %s</u><b><br/> &nbsp;&nbsp;&nbsp;Code: %s' % (main_obj.get('name'), main_obj.get('code')))
        #order_name_cell.add_attr('nowrap','nowrap')
        order_name_cell.add_style('cursor: pointer;')
        #order_name_cell.add_style('background-color: #e4a120;')
        order_name_cell.add_style('width: %spx;' % (my.first_cell_length))
        if 'estimate' in my.visibles:
            e_tbl = Table()
            e_tbl.add_style('font-size: 20px;')
            e_tbl.add_row()
            e1 = e_tbl.add_cell('Estimated')
            #e1.add_attr('align','center')
            e_tbl.add_row()
            expected_c = main_obj.get('expected_cost')
            if expected_c in ['',None]:
                expected_c = 0.0
            else:
                expected_c = float(expected_c)
            e_tbl.add_cell('%.2f' % expected_c)
            
            #estimate_cell = table.add_cell('%s&nbsp;' % e_tbl)
            estimate_cell = table.add_cell(e_tbl)
            estimate_cell.add_attr('align','right')
            estimate_cell.add_style('width: %spx;' % (my.division_length))
            #estimate_cell.add_style('background-color: #fa0011;')
        if 'actual' in my.visibles:
            a_tbl = Table()
            a_tbl.add_style('font-size: 20px;')
            a_tbl.add_row()
            a_tbl.add_cell('Actual')
            a_tbl.add_row()
            actual_c = main_obj.get('actual_cost')
            if actual_c in ['',None]:
                actual_c = 0.0
            else:
                actual_c = float(actual_c)
            a_tbl.add_cell('%.2f' % actual_c)
            #actual_cell = table.add_cell('%s&nbsp;&nbsp;' % a_tbl)
            actual_cell = table.add_cell(a_tbl)
            actual_cell.add_attr('align','right')
            actual_cell.add_style('width: %spx;' % (my.division_length))
            #actual_cell.add_style('background-color: #eadc11;')
        if 'price' in my.visibles:
            inner_table = PriceWdg(order_sk=my.sk, sk=my.sk, price=main_obj.get('price'), name=main_obj.get('name'), parent_sk='top')
            p_tbl = Table()
            p_tbl.add_style('font-size: 20px;')
            p_tbl.add_row()
            p_tbl.add_cell('Price')
            p_tbl.add_row()
            p_tbl.add_cell(inner_table)
            #price_cell = table.add_cell('%s&nbsp;&nbsp;&nbsp;' % p_tbl)
            price_cell = table.add_cell(p_tbl)
            price_cell.add_attr('align','right')
            price_cell.add_style('width: %spx;' % (my.division_length - 8))
            #price_cell.add_style('background-color: #da3e14;')
        if my.user in ['brian','matt.misenhimer','admin','gena','philip.rowe']:
            exp = main_obj.get('expected_cost')
            act = main_obj.get('actual_cost')
            alert_col = '#e0f127'
            if exp in [None,'']:
                exp = 0.0
            else:
                exp = float(exp)
            if act in [None,'']:
                act = 0.0
            else:
                act = float(act)
            if act > exp:
                alert_col = '#fa0011'
            elif act < exp:
                alert_col = '#0099ee'
            ck = table.add_cell('&nbsp;&nbsp;')
            ck.add_style('background-color: %s;' % alert_col)
            ck.add_style('font-size: 12;')
        
        bottom = Table()
        bottom.add_attr('width','100%s' % '%')
        bottom.add_attr('cellpadding','0')
        bottom.add_attr('cellspacing','0')
        for title in titles:
            title_sk = title.get('__search_key__')
            title_row  = bottom.add_row()
            title_row.add_attr('width', '100%s' % '%')
            title_row.add_attr('class','row_%s' % title_sk)
            title_obj = TitleCostRow(sk=title_sk, parent_sk=my.sk, order_sk=my.sk, user=my.user, group=my.group, visibles=my.visibles) 
            content_cell = bottom.add_cell(title_obj)
            content_cell.add_attr('width','100%s' % '%')
            content_cell.add_attr('sk', title_sk)
            content_cell.add_attr('order_sk', my.sk)
            content_cell.add_attr('parent_sk', my.sk)
            content_cell.add_attr('call_me', title.get('title'))
            content_cell.add_attr('episode',title.get('episode'))
            content_cell.add_attr('my_class','TitleCostRow')
            content_cell.add_attr('client_code',title.get('client_code'))
            content_cell.add_attr('class','costcell_%s' % title_sk)
        tab2ret = Table()
        tab2ret.add_attr('width','100%s' % '%')
        tab2ret.add_row()
        tab2ret.add_cell(table)
        tab2ret.add_row()
        bot_row = tab2ret.add_row()
        bot_row.add_attr('class','bot_%s' % my.sk)
        bot_row.add_style('display: table-row;')
        bot = tab2ret.add_cell(bottom)
        bot.add_style('padding-left: 40px;')
        return tab2ret

class TitleCostRow(BaseRefreshWdg):
    def init(my):
        from client.tactic_client_lib import TacticServerStub
        from pyasm.common import Environment
        my.server = TacticServerStub.get()
        my.search_type = 'twog/title'
        my.title = "Title"
        my.sk = ''
        my.parent_sk = ''
        my.order_sk = ''
        my.user = ''
        my.group = ''
        my.visibles = ''
        my.division_length = 1
        my.first_cell_length = 568
        my.full_length = 1484 - 40 - my.first_cell_length

    def assign_trt(my, title_sk):
        behavior = {'css_class': 'clickme', 'type': 'change', 'cbjs_action': '''        
                        try{
                          var server = TacticServerStub.get();
                          title_sk = '%s';
                          trt = bvr.src_el.value;
                          server.update(title_sk, {'trt_pricing': trt});
                          alert('updated');
                }
                catch(err){
                          spt.app_busy.hide();
                          alert(err);
                }
         ''' % title_sk}
        return behavior

    def get_display(my):   
        my.sk = str(my.kwargs.get('sk'))
        my.parent_sk = str(my.kwargs.get('parent_sk'))
        my.order_sk = str(my.kwargs.get('order_sk'))
        my.group = str(my.kwargs.get('group'))
        my.user = str(my.kwargs.get('user'))
        my.visibles = str(my.kwargs.get('visibles'))
        code = my.sk.split('code=')[1]
        trt_titles = ''
        t_origs = my.server.eval("@SOBJECT(twog/title_origin['title_code','%s'])" % code)
        for t in t_origs:
            source_code = t.get('source_code')
            source = my.server.eval("@SOBJECT(twog/source['code','%s'])" % source_code)
            if source:
                source = source[0]
                if trt_titles == '':
                    trt_titles = '[%s] %s: %s \tTRT: %s' % (source.get('code'), source.get('title'), source.get('episode'), source.get('total_run_time'))
                else: 
                    trt_titles = '%s\n[%s] %s: %s \tTRT: %s' % (trt_titles, source.get('code'), source.get('title'), source.get('episode'), source.get('total_run_time'))
        cb = CBScripts(order_sk=my.order_sk)
        divisions_count = len(my.visibles.split(','))
        my.division_length = my.full_length/divisions_count
        code = my.sk.split('code=')[1]
        main_obj = my.server.eval("@SOBJECT(twog/title['code','%s'])" % code)[0]
        proj_expr = "@SOBJECT(twog/proj['title_code','%s'])" % (code)
        projs = my.server.eval(proj_expr)
        trt_pricing = main_obj.get('trt_pricing')
        if trt_pricing in [None,'']:
            trt_pricing = ''
        table = Table()
        table.add_attr('cellpadding','0')
        table.add_attr('cellspacing','0')
        #table.add_style('border-collapse', 'separate')
        #table.add_style('border-spacing', '25px 0px')
        table.add_style('color: #00033a;')
        table.add_style('background-color: #d9edcf;')
        table.add_style('width: 100%s;' % '%')
        table.add_style('border-bottom-right-radius', '10px')
        table.add_style('border-bottom-left-radius', '10px')
        table.add_style('border-top-right-radius', '10px')
        table.add_style('border-top-left-radius', '10px')
        table.add_style('font-size: 18px;')
        table.add_row()
        toggler =  table.add_cell('<img border="0" style="vertical-align: middle" title="" src="/context/icons/custom/MinusIcon.png">')
        toggler.add_behavior(cb.get_toggle_bottom(my.sk))
        first_col_tbl = Table()
        first_col_tbl.add_attr('cellpadding','0')
        first_col_tbl.add_attr('cellspacing','0')
        first_col_tbl.add_attr('border','0')
        first_col_tbl.add_style('width: 100%s;' % '%')
        first_col_tbl.add_row()
        title_cell = first_col_tbl.add_cell('<b><u>Title: %s: %s</u><b><br/> &nbsp;&nbsp;&nbsp;Code: %s' % (main_obj.get('title'), main_obj.get('episode'), main_obj.get('code')))
        #title_cell.add_attr('nowrap','nowrap')
        title_cell.add_attr('align','left')
        another_table = Table()
        help_cell = another_table.add_cell('<img border="0" style="vertical-align: middle" alt="%s" title="%s" name="%s" src="/context/icons/silk/help.png">' % (trt_titles, trt_titles, trt_titles))
        help_cell.add_attr('align','right')
        trt_text = TextWdg('trt_%s' % main_obj.get('code'))
        trt_text.set_value(trt_pricing)
        trt_text.add_behavior(my.assign_trt(my.sk))
        trt_cell = another_table.add_cell(trt_text)
        trt_cell.add_attr('align','right')
        trter = first_col_tbl.add_cell(another_table)
        trter.add_attr('align','center')
        title_cell2 = table.add_cell(first_col_tbl)
        #title_cell2.add_style('background-color: #e4a120;')
        title_cell2.add_style('width: %spx;' % (my.first_cell_length))
        if 'estimate' in my.visibles:
            expected_c = main_obj.get('expected_cost')
            if expected_c in ['',None]:
                expected_c = 0.0
            else:
                expected_c = float(expected_c)
            estimate_cell = table.add_cell('%.2f' % expected_c)
            estimate_cell.add_attr('align','right')
            estimate_cell.add_style('width: %spx;' % (my.division_length))
            #estimate_cell.add_style('background-color: #fa0011;')
        if 'actual' in my.visibles:
            actual_c = main_obj.get('actual_cost')
            if actual_c in ['',None]:
                actual_c = 0.0
            else:
                actual_c = float(actual_c)
            actual_cell = table.add_cell('%.2f' % actual_c)
            actual_cell.add_attr('align','right')
            actual_cell.add_style('width: %spx;' % (my.division_length))
            #actual_cell.add_style('background-color: #eadc11;')
        if 'price' in my.visibles:
            inner_table = PriceWdg(order_sk=my.order_sk, sk=my.sk, price=main_obj.get('price'), name='%s: %s' % (main_obj.get('title'), main_obj.get('episode')), parent_sk=my.parent_sk)
            price_cell = table.add_cell(inner_table)
            price_cell.add_attr('align','right')
            price_cell.add_style('width: %spx;' % (my.division_length - 8))
            #price_cell.add_style('background-color: #da3e14;')
        if my.user in ['brian','matt.misenhimer','admin','gena','philip.rowe']:
            exp = main_obj.get('expected_cost')
            act = main_obj.get('actual_cost')
            alert_col = '#e0f127'
            if exp in [None,'']:
                exp = 0.0
            else:
                exp = float(exp)
            if act in [None,'']:
                act = 0.0
            else:
                act = float(act)
            if act > exp:
                alert_col = '#fa0011'
            elif act < exp:
                alert_col = '#0099ee'
            ck = table.add_cell('&nbsp;&nbsp;')
            ck.add_style('background-color: %s;' % alert_col)
            ck.add_style('font-size: 12;')
#            checkbox = CheckboxWdg('checkbox_%s' % main_obj.get('code'))
#            checkbox.set_persistence()
#            if False == True:
#                checkbox.set_value(True)
#            else:
#                checkbox.set_value(False)
#            ck = table.add_cell(checkbox)
        bottom = Table()
        bottom.add_attr('width','100%s' % '%')
        bottom.add_attr('cellpadding','0')
        bottom.add_attr('cellspacing','0')
        for proj in projs: 
            proj_sk = proj.get('__search_key__')
            proj_row  = bottom.add_row()
            proj_row.add_attr('width', '100%s' % '%')
            proj_row.add_attr('class','row_%s' % proj_sk)
            proj_obj = ProjCostRow(sk=proj_sk, parent_sk=my.sk, order_sk=my.order_sk, group=my.group, user=my.user, visibles=my.visibles) 
            content_cell = bottom.add_cell(proj_obj)
            content_cell.add_attr('width','100%s' % '%')
            content_cell.add_attr('sk', proj_sk)
            content_cell.add_attr('order_sk', my.order_sk)
            content_cell.add_attr('parent_sk', my.sk)
            content_cell.add_attr('call_me', proj.get('process'))
            content_cell.add_attr('my_class','ProjCostRow')
            content_cell.add_attr('client_code',proj.get('client_code'))
            content_cell.add_attr('class','costcell_%s' % proj_sk)
        

        tab2ret = Table()
        tab2ret.add_attr('width','100%s' % '%')
        tab2ret.add_row()
        tab2ret.add_cell(table)
        tab2ret.add_row()
        bot_row = tab2ret.add_row()
        bot_row.add_attr('class','bot_%s' % my.sk)
        bot_row.add_style('display: table-row;')
        bot = tab2ret.add_cell(bottom)
        bot.add_style('padding-left: 40px;')
        return tab2ret

class ProjCostRow(BaseRefreshWdg):
    def init(my):
        from client.tactic_client_lib import TacticServerStub
        from pyasm.common import Environment
        my.server = TacticServerStub.get()
        my.search_type = 'twog/proj'
        my.title = "Proj"
        my.sk = ''
        my.parent_sk = ''
        my.order_sk = ''
        my.user = ''
        my.group = ''
        my.visibles = ''
        my.division_length = 1
        my.first_cell_length = 531
        my.full_length = 1484 - 80 - my.first_cell_length


    def get_display(my):   
        my.sk = str(my.kwargs.get('sk'))
        my.parent_sk = str(my.kwargs.get('parent_sk'))
        my.order_sk = str(my.kwargs.get('order_sk'))
        my.group = str(my.kwargs.get('group'))
        my.user = str(my.kwargs.get('user'))
        my.visibles = str(my.kwargs.get('visibles'))
        cb = CBScripts(order_sk=my.order_sk)
        divisions_count = len(my.visibles.split(','))
        my.division_length = my.full_length/divisions_count
        code = my.sk.split('code=')[1]
        main_obj = my.server.eval("@SOBJECT(twog/proj['code','%s'])" % code)[0]
        wo_expr = "@SOBJECT(twog/work_order['proj_code','%s'])" % (code)
        wos = my.server.eval(wo_expr)
        table = Table()
        table.add_attr('cellpadding','0')
        table.add_attr('cellspacing','0')
        #table.add_style('border-collapse', 'separate')
        #table.add_style('border-spacing', '25px 0px')
        table.add_style('color: #00033a;')
        table.add_style('background-color: #d9ed8b;')
        table.add_style('width: 100%s;' % '%')
        table.add_style('border-bottom-right-radius', '10px')
        table.add_style('border-bottom-left-radius', '10px')
        table.add_style('border-top-right-radius', '10px')
        table.add_style('border-top-left-radius', '10px')
        table.add_style('font-size: 16px;')
        table.add_row()
        toggler =  table.add_cell('<img border="0" style="vertical-align: middle" title="" src="/context/icons/custom/MinusIcon.png">')
        toggler.add_behavior(cb.get_toggle_bottom(my.sk))
        title_cell = table.add_cell('<b><u>Project: %s</u><b><br/> &nbsp;&nbsp;&nbsp;Code: %s' % (main_obj.get('process'), main_obj.get('code')))
        #title_cell.add_attr('nowrap','nowrap')
        title_cell.add_style('cursor: pointer;')
        #title_cell.add_style('background-color: #e4a120;')
        title_cell.add_style('width: %spx;' % (my.first_cell_length))
        if 'estimate' in my.visibles:
            expected_c = main_obj.get('expected_cost')
            if expected_c in ['',None]:
                expected_c = 0.0
            else:
                expected_c = float(expected_c)
            estimate_cell = table.add_cell('%.2f' % expected_c)
            estimate_cell.add_attr('align','right')
            estimate_cell.add_style('width: %spx;' % (my.division_length))
            #estimate_cell.add_style('background-color: #fa0011;')
        if 'actual' in my.visibles:
            actual_c = main_obj.get('actual_cost')
            if actual_c in ['',None]:
                actual_c = 0.0
            else:
                actual_c = float(actual_c)
            actual_cell = table.add_cell('%.2f' % actual_c)
            actual_cell.add_attr('align','right')
            actual_cell.add_style('width: %spx;' % (my.division_length))
            #actual_cell.add_style('background-color: #eadc11;')
        if 'price' in my.visibles:
            inner_table = PriceWdg(order_sk=my.order_sk, sk=my.sk, price=main_obj.get('price'), name=main_obj.get('process'), parent_sk=my.parent_sk)
            price_cell = table.add_cell(inner_table)
            price_cell.add_attr('align','right')
            price_cell.add_style('width: %spx;' % (my.division_length - 8))
            #price_cell.add_style('background-color: #da3e14;')
            
        if my.user in ['brian','matt.misenhimer','admin','gena','philip.rowe']:
            exp = main_obj.get('expected_cost')
            act = main_obj.get('actual_cost')
            alert_col = '#e0f127'
            if exp in [None,'']:
                exp = 0.0
            else:
                exp = float(exp)
            if act in [None,'']:
                act = 0.0
            else:
                act = float(act)
            if act > exp:
                alert_col = '#fa0011'
            elif act < exp:
                alert_col = '#0099ee'
            ck = table.add_cell('&nbsp;&nbsp;')
            ck.add_style('background-color: %s;' % alert_col)
            ck.add_style('font-size: 12;')
#            checkbox = CheckboxWdg('checkbox_%s' % main_obj.get('code'))
#            checkbox.set_persistence()
#            if False == True:
#                checkbox.set_value(True)
#            else:
#                checkbox.set_value(False)
#            ck = table.add_cell(checkbox)
        bottom = Table()
        bottom.add_attr('width','100%s' % '%')
        bottom.add_attr('cellpadding','0')
        bottom.add_attr('cellspacing','0')
        for wo in wos: 
            wo_sk = wo.get('__search_key__')
            wo_row  = bottom.add_row()
            wo_row.add_attr('width', '100%s' % '%')
            wo_row.add_attr('class','row_%s' % wo_sk)
            wo_obj = WorkOrderCostRow(sk=wo_sk, parent_sk=my.sk, order_sk=my.order_sk, group=my.group, user=my.user, visibles=my.visibles) 
            content_cell = bottom.add_cell(wo_obj)
            content_cell.add_attr('width','100%s' % '%')
            content_cell.add_attr('sk', wo_sk)
            content_cell.add_attr('order_sk', my.order_sk)
            content_cell.add_attr('parent_sk', my.sk)
            content_cell.add_attr('call_me', wo.get('process'))
            content_cell.add_attr('my_class','WorkOrderCostRow')
            content_cell.add_attr('client_code',wo.get('client_code'))
            content_cell.add_attr('class','costcell_%s' % wo_sk)
        
        tab2ret = Table()
        tab2ret.add_attr('width','100%s' % '%')
        tab2ret.add_row()
        tab2ret.add_cell(table)
        tab2ret.add_row()
        bot_row = tab2ret.add_row()
        bot_row.add_attr('class','bot_%s' % my.sk)
        bot_row.add_style('display: table-row;')
        bot = tab2ret.add_cell(bottom)
        bot.add_style('padding-left: 40px;')
        return tab2ret

class WorkOrderCostRow(BaseRefreshWdg):
    def init(my):
        from client.tactic_client_lib import TacticServerStub
        from pyasm.common import Environment
        my.server = TacticServerStub.get()
        my.search_type = 'twog/work_order'
        my.title = "WorkOrder"
        my.sk = ''
        my.parent_sk = ''
        my.order_sk = ''
        my.user = ''
        my.group = ''
        my.visibles =''
        my.division_length = 1
        my.first_cell_length = 490
        my.full_length = 1484 - 120 - my.first_cell_length

    def get_display(my):   
        my.sk = str(my.kwargs.get('sk'))
        my.parent_sk = str(my.kwargs.get('parent_sk'))
        my.order_sk = str(my.kwargs.get('order_sk'))
        my.group = str(my.kwargs.get('group'))
        my.user = str(my.kwargs.get('user'))
        my.visibles = str(my.kwargs.get('visibles'))
        cb = CBScripts(order_sk=my.order_sk)
        divisions_count = len(my.visibles.split(','))
        my.division_length = my.full_length/divisions_count
        code = my.sk.split('code=')[1]
        main_obj = my.server.eval("@SOBJECT(twog/work_order['code','%s'])" % code)[0]
        eq_expr = "@SOBJECT(twog/equipment_used['work_order_code','%s'])" % (code)
        eqs = my.server.eval(eq_expr)
        table = Table()
        table.add_attr('cellpadding','0')
        table.add_attr('cellspacing','0')
        #table.add_style('border-collapse', 'separate')
        #table.add_style('border-spacing', '25px 0px')
        table.add_style('color: #00033a;')
        table.add_style('background-color: #c6eda0;')
        table.add_style('width: 100%s;' % '%')
        table.add_style('border-bottom-right-radius', '10px')
        table.add_style('border-bottom-left-radius', '10px')
        table.add_style('border-top-right-radius', '10px')
        table.add_style('border-top-left-radius', '10px')
        table.add_style('font-size: 14px;')
        table.add_row()
        toggler =  table.add_cell('<img border="0" style="vertical-align: middle" title="" src="/context/icons/custom/MinusIcon.png">')
        toggler.add_behavior(cb.get_toggle_bottom(my.sk))
        title_cell = table.add_cell('<b><u>Work Order: %s</u><b><br/> &nbsp;&nbsp;&nbsp;Code: %s' % (main_obj.get('process'), main_obj.get('code')))
        #title_cell.add_attr('nowrap','nowrap')
        title_cell.add_style('cursor: pointer;')
        #title_cell.add_style('background-color: #e4a120;')
        title_cell.add_style('width: %spx;' % (my.first_cell_length))
        if 'estimate' in my.visibles:
            expected_c = main_obj.get('expected_cost')
            if expected_c in ['',None]:
                expected_c = 0.0
            else:
                expected_c = float(expected_c)
            estimate_cell = table.add_cell('%.2f' % expected_c)
            estimate_cell.add_attr('align','right')
            estimate_cell.add_style('width: %spx;' % (my.division_length))
            #estimate_cell.add_style('background-color: #fa0011;')
        if 'actual' in my.visibles:
            actual_c = main_obj.get('actual_cost')
            if actual_c in ['',None]:
                actual_c = 0.0
            else:
                actual_c = float(actual_c)
            actual_cell = table.add_cell('%.2f' % actual_c)
            actual_cell.add_attr('align','right')
            actual_cell.add_style('width: %spx;' % (my.division_length))
            #actual_cell.add_style('background-color: #eadc11;')
        if 'price' in my.visibles:
            price_cell = table.add_cell(' ')
            price_cell.add_attr('align','right')
            price_cell.add_style('width: %spx;' % (my.division_length))
            #price_cell.add_style('background-color: #da3e14;')
        if my.user in ['brian','matt.misenhimer','admin','gena','philip.rowe']:
            exp = main_obj.get('expected_cost')
            act = main_obj.get('actual_cost')
            alert_col = '#e0f127'
            if exp in [None,'']:
                exp = 0.0
            else:
                exp = float(exp)
            if act in [None,'']:
                act = 0.0
            else:
                act = float(act)
            if act > exp:
                alert_col = '#fa0011'
            elif act < exp:
                alert_col = '#0099ee'
            ck = table.add_cell('&nbsp;&nbsp;')
            ck.add_style('background-color: %s;' % alert_col)
            ck.add_style('font-size: 12;')
#            checkbox = CheckboxWdg('checkbox_%s' % main_obj.get('code'))
#            checkbox.set_persistence()
#            if False == True:
#                checkbox.set_value(True)
#            else:
#                checkbox.set_value(False)
#            ck = table.add_cell(checkbox)
        bottom = Table()
        bottom.add_attr('width','100%s' % '%')
        bottom.add_attr('cellpadding','0')
        bottom.add_attr('cellspacing','0')
        task = my.server.eval("@SOBJECT(sthpw/task['code','%s'])" % main_obj.get('task_code'))
        if len(task) > 0:
            task = task[0]
            task_sk = task.get('__search_key__')
            task_row = bottom.add_row()
            task_row.add_attr('width', '100%s' % '%')
            task_row.add_attr('class','row_%s' % task_sk)
            task_obj = LaborCostRow(sk=task_sk, parent_sk=my.sk, order_sk=my.order_sk, group=my.group, user=my.user, visibles=my.visibles) 
            content_cell = bottom.add_cell(task_obj)
            content_cell.add_attr('width','100%s' % '%')
            content_cell.add_attr('sk', task_sk)
            content_cell.add_attr('order_sk', my.order_sk)
            content_cell.add_attr('parent_sk', my.sk)
            content_cell.add_attr('call_me', task.get('process'))
            content_cell.add_attr('my_class','LaborCostRow')
            content_cell.add_attr('class','costcell_%s' % task_sk)
        for eq in eqs: 
            eq_sk = eq.get('__search_key__')
            eq_row  = bottom.add_row()
            eq_row.add_attr('width', '100%s' % '%')
            eq_row.add_attr('class','row_%s' % eq_sk)
            eq_obj = EquipmentUsedCostRow(sk=eq_sk, parent_sk=my.sk, order_sk=my.order_sk, group=my.group, user=my.user, visibles=my.visibles)
            content_cell = bottom.add_cell(eq_obj)
            content_cell.add_attr('width','100%s' % '%')
            content_cell.add_attr('sk', eq_sk)
            content_cell.add_attr('order_sk', my.order_sk)
            content_cell.add_attr('parent_sk', my.sk)
            content_cell.add_attr('call_me', eq.get('name'))
            content_cell.add_attr('my_class','EquipmentUsedCostRow')
            content_cell.add_attr('client_code',eq.get('client_code'))
            content_cell.add_attr('class','equipmentrow costcell_%s' % eq_sk)
        
        tab2ret = Table()
        tab2ret.add_attr('width','100%s' % '%')
        tab2ret.add_row()
        tab2ret.add_cell(table)
        tab2ret.add_row()
        bot_row = tab2ret.add_row()
        bot_row.add_attr('class','bot_%s' % my.sk)
        bot_row.add_style('display: table-row;')
        bot = tab2ret.add_cell(bottom)
        bot.add_style('padding-left: 40px;')
        return tab2ret

class EquipmentUsedCostRow(BaseRefreshWdg):
    def init(my):
        from client.tactic_client_lib import TacticServerStub
        from pyasm.common import Environment
        my.server = TacticServerStub.get()
        my.search_type = 'twog/equipment_used'
        my.title = "EquipmentUsed"
        my.sk = ''
        my.parent_sk = ''
        my.order_sk = ''
        my.user = ''
        my.group = ''
        my.visibles = ''
        my.division_length = 1
        my.first_cell_length = 469
        my.full_length = 1484 - 160 - my.first_cell_length

    def get_display(my):   
        my.sk = str(my.kwargs.get('sk'))
        my.parent_sk = str(my.kwargs.get('parent_sk'))
        my.order_sk = str(my.kwargs.get('order_sk'))
        my.group = str(my.kwargs.get('group'))
        my.user = str(my.kwargs.get('user'))
        my.visibles = str(my.kwargs.get('visibles'))
        cb = CBScripts(order_sk=my.order_sk)
        divisions_count = len(my.visibles.split(','))
        my.division_length = my.full_length/divisions_count
        code = my.sk.split('code=')[1]
        main_obj = my.server.eval("@SOBJECT(twog/equipment_used['code','%s'])" % code)[0]
        table = Table()
        table.add_attr('cellpadding','0')
        table.add_attr('cellspacing','0')
        #table.add_style('border-collapse', 'separate')
        #table.add_style('border-spacing', '25px 0px')
        table.add_style('color: #00033a;')
        table.add_style('background-color: #c6aeae;')
        table.add_style('width: 100%s;' % '%')
        table.add_style('border-bottom-right-radius', '10px')
        table.add_style('border-bottom-left-radius', '10px')
        table.add_style('border-top-right-radius', '10px')
        table.add_style('border-top-left-radius', '10px')
        table.add_style('font-size: 12px;')
        table.add_row()
        title_cell = table.add_cell('<b><u>Equipment: %s</u><b>' % main_obj.get('name'))
        #title_cell.add_attr('nowrap','nowrap')
        title_cell.add_style('cursor: pointer;')
        #title_cell.add_style('background-color: #e4a120;')
        title_cell.add_style('width: %spx;' % (my.first_cell_length))
        if 'estimate' in my.visibles:
            expected_c = main_obj.get('expected_cost')
            if expected_c in ['',None]:
                expected_c = 0.0
            else:
                expected_c = float(expected_c)
            estimate_cell = table.add_cell('%.2f' % expected_c)
            estimate_cell.add_attr('align','right')
            estimate_cell.add_style('width: %spx;' % (my.division_length))
            #estimate_cell.add_style('background-color: #fa0011;')
        if 'actual' in my.visibles:
            actual_c = main_obj.get('actual_cost')
            if actual_c in ['',None]:
                actual_c = 0.0
            else:
                actual_c = float(actual_c)
            actual_cell = table.add_cell('%.2f' % actual_c)
            actual_cell.add_attr('align','right')
            actual_cell.add_style('width: %spx;' % (my.division_length))
            #actual_cell.add_style('background-color: #eadc11;')
        if 'price' in my.visibles:
            price_cell = table.add_cell(' ')
            price_cell.add_attr('align','right')
            price_cell.add_style('width: %spx;' % (my.division_length))
            #price_cell.add_style('background-color: #da3e14;')
        if my.user in ['brian','matt.misenhimer','admin','gena','philip.rowe']:
            exp = main_obj.get('expected_cost')
            act = main_obj.get('actual_cost')
            alert_col = '#e0f127'
            if exp in [None,'']:
                exp = 0.0
            else:
                exp = float(exp)
            if act in [None,'']:
                act = 0.0
            else:
                act = float(act)
            if act > exp:
                alert_col = '#fa0011'
            elif act < exp:
                alert_col = '#0099ee'
            ck = table.add_cell('&nbsp;&nbsp;')
            ck.add_style('background-color: %s;' % alert_col)
            ck.add_style('font-size: 12;')
#            checkbox = CheckboxWdg('checkbox_%s' % main_obj.get('code'))
#            checkbox.set_persistence()
#            if False == True:
#                checkbox.set_value(True)
#            else:
#                checkbox.set_value(False)
#            ck = table.add_cell(checkbox)
        tab2ret = Table()
        tab2ret.add_attr('width','100%s' % '%')
        tab2ret.add_row()
        tab2ret.add_cell(table)
        return tab2ret

class LaborCostRow(BaseRefreshWdg):
    def init(my):
        from client.tactic_client_lib import TacticServerStub
        from pyasm.common import Environment
        my.server = TacticServerStub.get()
        my.search_type = 'sthpw/task'
        my.title = "Labor"
        my.sk = ''
        my.parent_sk = ''
        my.order_sk = ''
        my.user = ''
        my.group = ''
        my.visibles = ''
        my.division_length = 1
        my.first_cell_length = 450
        my.full_length = 1484 - 160 - my.first_cell_length

    def get_display(my):   
        my.sk = str(my.kwargs.get('sk'))
        my.parent_sk = str(my.kwargs.get('parent_sk'))
        my.order_sk = str(my.kwargs.get('order_sk'))
        my.group = str(my.kwargs.get('group'))
        my.user = str(my.kwargs.get('user'))
        my.visibles = str(my.kwargs.get('visibles'))
        cb = CBScripts(order_sk=my.order_sk)
        divisions_count = len(my.visibles.split(','))
        my.division_length = my.full_length/divisions_count
        code = my.sk.split('code=')[1]
        main_obj = my.server.eval("@SOBJECT(sthpw/task['code','%s'])" % code)[0]
        wo_obj = None
        if main_obj.get('lookup_code') not in [None,'']:
            wo_obj = my.server.eval("@SOBJECT(twog/work_order['code','%s'])" % main_obj.get('lookup_code'))[0]
        else:
            wo_objs = my.server.eval("@SOBJECT(twog/work_order['task_code','%s'])" % main_obj.get('code'))
            #print "LEN WO_OBJS = %s" % len(wo_objs)
            for ob in wo_objs:
                if ob.get('process') == main_obj.get('process'):
                    wo_obj = ob 
        grp_expr = "@SOBJECT(sthpw/login_group['code','%s'])" % main_obj.get('assigned_login_group')
        #print "GRP_EXPR = %s" % grp_expr
        grp_obj = my.server.eval(grp_expr)
        grp_hourly = 0
        if grp_obj:
            grp_obj = grp_obj[0]
            grp_hourly = grp_obj.get('hourly_rate') 
            if grp_hourly in [None,'']:
                grp_hourly = 0
            else:
                grp_hourly = float(grp_hourly)
        table = Table()
        table.add_attr('cellpadding','0')
        table.add_attr('cellspacing','0')
        #table.add_style('border-collapse', 'separate')
        #table.add_style('border-spacing', '25px 0px')
        table.add_style('color: #00033a;')
        table.add_style('background-color: #eac26a;')
        table.add_style('width: 100%s;' % '%')
        table.add_style('border-bottom-right-radius', '10px')
        table.add_style('border-bottom-left-radius', '10px')
        table.add_style('border-top-right-radius', '10px')
        table.add_style('border-top-left-radius', '10px')
        table.add_style('font-size: 12px;')
        table.add_row()
        title_cell = table.add_cell('<b><u>Labor: %s</u><b>' % main_obj.get('process'))
        #title_cell.add_attr('nowrap','nowrap')
        title_cell.add_style('cursor: pointer;')
        #title_cell.add_style('background-color: #e4a120;')
        title_cell.add_style('width: %spx;' % (my.first_cell_length))
        est_cost = 0
        actual_cost = 0
        if 'estimate' in my.visibles:
            est_work_hours = wo_obj.get('estimated_work_hours')
            if est_work_hours in [None,'']:
                est_work_hours = 0
            est_cost = float(est_work_hours) * float(grp_hourly)    
            estimate_cell = table.add_cell('%.2f' % est_cost)
            estimate_cell.add_attr('align','right')
            estimate_cell.add_style('width: %spx;' % (my.division_length))
            #estimate_cell.add_style('background-color: #fa0011;')
        if 'actual' in my.visibles:
            wh_sum = 0
            work_hours_expr = "@SOBJECT(sthpw/work_hour['task_code','%s'])" % main_obj.get('code')
            #print "WORK HOURS EXPR = %s" % work_hours_expr
            work_hours = my.server.eval(work_hours_expr)
            #print "WORK HOURS = %s" % work_hours
            for work_hour in work_hours:
                wh_sum = wh_sum + float(work_hour.get('straight_time')) 
            actual_cost = float(wh_sum) * float(grp_hourly)
            actual_cell = table.add_cell('%.2f' % actual_cost)
            actual_cell.add_attr('align','right')
            actual_cell.add_style('width: %spx;' % (my.division_length))
            #actual_cell.add_style('background-color: #eadc11;')
        if 'price' in my.visibles:
            price_cell = table.add_cell(' ')
            price_cell.add_attr('align','right')
            price_cell.add_style('width: %spx;' % (my.division_length))
            #price_cell.add_style('background-color: #da3e14;')
        if my.user in ['brian','matt.misenhimer','admin','gena','philip.rowe']:
            exp = est_cost
            act = actual_cost 
            alert_col = '#e0f127'
            if exp in [None,'']:
                exp = 0.0
            else:
                exp = float(exp)
            if act in [None,'']:
                act = 0.0
            else:
                act = float(act)
            if act > exp:
                alert_col = '#fa0011'
            elif act < exp:
                alert_col = '#0099ee'
            ck = table.add_cell('&nbsp;&nbsp;')
            ck.add_style('background-color: %s;' % alert_col)
            ck.add_style('font-size: 12;')
#            checkbox = CheckboxWdg('checkbox_%s' % main_obj.get('code'))
#            checkbox.set_persistence()
#            if False == True:
#                checkbox.set_value(True)
#            else:
#                checkbox.set_value(False)
#            ck = table.add_cell(checkbox)
        tab2ret = Table()
        tab2ret.add_attr('width','100%s' % '%')
        tab2ret.add_row()
        tab2ret.add_cell(table)
        return tab2ret


class ProjPricingWdg(BaseRefreshWdg):
    def init(my):
        from client.tactic_client_lib import TacticServerStub
        from pyasm.common import Environment
        my.server = TacticServerStub.get()
        my.proj_sk = ''
        my.order_sk = ''
        my.rate_card_code = ''
        my.x_butt = "<img src='/context/icons/common/BtnKill.gif' title='Delete' name='Delete'/>" 


    def select_item(my, proj_sk, trt_pricing, rate_card_code): #NO SID NECC
        behavior = {'css_class': 'sel_change', 'type': 'change', 'cbjs_action': '''        
                        function make_money(money){
                              money = money + '';
                              dot_idx = money.indexOf('.');
                              if(dot_idx == -1){
                                  money = money + '.00';
                              }else{
                                  change = money.split('.');
                                  if(change[1].length < 2){
                                      money = money + '0';
                                  }
                                  if(change[1].length > 2){
                                      money = change[0] + '.' + change[1].substr(0,2);
                                  }
                              } 
                            return money;
                        }
                        try{
                          var server = TacticServerStub.get();
                          var order_sk = '%s';
                          proj_sk = '%s';
                          proj_code = proj_sk.split('code=')[1];
                          trt_pricing = '%s';
                          rate_card_code = '%s';
                          if(trt_pricing != '' && trt_pricing != null){
                              var top_el = spt.api.get_parent(bvr.src_el, '.pricing_popout_' + proj_code);
                              dollas = '';
                              inputs = top_el.getElementsByTagName('input');
                              for(var r= 0; r < inputs.length; r++){
                                  if(inputs[r].name == 'dollas_' + proj_code){
                                      dollas = inputs[r];
                                  } 
                              }
                              new_price_cell = top_el.getElementsByClassName('new_price_' + proj_code)[0];
                              current_price = new_price_cell.innerHTML.split(': ')[1];
                              item_code = bvr.src_el.value.split('XsX')[1];
                              dollar_amt = 0;
                              if(item_code != 'NOTHING'){
                                  item = server.eval("@SOBJECT(twog/rate_card_item['code','" + item_code + "'])")[0];
                                  trts = trt_pricing.split(':')
                                  trt = 0
                                  if(trts.length > 2){
                                      trt = (Number(trts[0]) * 60) + Number(trts[1]);
                                  }else{
                                      trt = Number(trts[0]);
                                  }
                                  dollar_amt = trt * Number(item.rate_per_minute);
                                  dollar_amt = make_money(dollar_amt);
                              }else{
                                  dollar_amt = 0.00;
                              }
                              dollas.value = dollar_amt;
                              if(new_price_cell.getAttribute('affected') == 'nope'){
                                  updated_price = Number(current_price) + Number(dollar_amt);
                                  new_price_cell.setAttribute('affected',dollar_amt);
                                  updated_price = make_money(updated_price)
                              }else{
                                  updated_price = Number(current_price) - Number(new_price_cell.getAttribute('affected')) + Number(dollar_amt);
                                  new_price_cell.setAttribute('affected',dollar_amt);
                                  updated_price = make_money(updated_price)
                              }
                              new_price_cell.innerHTML = '&nbsp;&nbsp;New Proj Price: ' + updated_price;
                                   
                          }else{
                              alert('The title must have a Total Run Time (TRT) assigned first');
                          }
                }
                catch(err){
                          spt.app_busy.hide();
                          alert(err);
                }
         ''' % (my.order_sk, proj_sk, trt_pricing, rate_card_code)}
        return behavior

    def price_changed(my, proj_sk):
        behavior = {'css_class': 'clickme', 'type': 'change', 'cbjs_action': '''        
                        try{
                        function make_money(money){
                              money = money + '';
                              dot_idx = money.indexOf('.');
                              if(dot_idx == -1){
                                  money = money + '.00';
                              }else{
                                  change = money.split('.');
                                  if(change[1].length < 2){
                                      money = money + '0';
                                  }
                                  if(change[1].length > 2){
                                      money = change[0] + '.' + change[1].substr(0,2);
                                  }
                              } 
                            return money;
                        }
                          proj_sk = '%s';
                          price = bvr.src_el.value;
                          proj_code = proj_sk.split('code=')[1];
                          var top_el = spt.api.get_parent(bvr.src_el, '.pricing_popout_' + proj_code);
                          var new_price_cell = top_el.getElementsByClassName('new_price_' + proj_code)[0];
                          current_price = new_price_cell.innerHTML.split(': ')[1];
                          newer_price = ''
                          if(new_price_cell.getAttribute('affected') != 'nope'){
                              newer_price = Number(current_price) - Number(new_price_cell.getAttribute('affected')) + Number(price);
                              newer_price = make_money(newer_price);    
                          }else{
                              newer_price = make_money(price);
                          }
                          new_price_cell.setAttribute('affected',price);
                          new_price_cell.innerHTML = '&nbsp;&nbsp;New Proj Price: ' + newer_price;
                }
                catch(err){
                          spt.app_busy.hide();
                          alert(err);
                }
         ''' % proj_sk}
        return behavior

    def save_line(my, proj_sk):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        function make_money(money){
                              money = money + '';
                              dot_idx = money.indexOf('.');
                              if(dot_idx == -1){
                                  money = money + '.00';
                              }else{
                                  change = money.split('.');
                                  if(change[1].length < 2){
                                      money = money + '0';
                                  }
                                  if(change[1].length > 2){
                                      money = change[0] + '.' + change[1].substr(0,2);
                                  }
                              } 
                            return money;
                        }
                        try{
                          var server = TacticServerStub.get();
                          var order_sk = '%s';
                          var proj_sk = '%s';
                          var proj_code = proj_sk.split('code=')[1];
                          var order_code = order_sk.split('code=')[1];
                          var document_top = document.getElementsByClassName('twog_cost_builder_' + order_sk)[0];
                          var top_el = spt.api.get_parent(bvr.src_el, '.pricing_popout_' + proj_code);
                          var new_price_cell = top_el.getElementsByClassName('new_price_' + proj_code)[0];
                          dollas = '';
                          inputs = top_el.getElementsByTagName('input');
                          for(var r= 0; r < inputs.length; r++){
                              if(inputs[r].name == 'dollas_' + proj_code){
                                  dollas = inputs[r];
                              } 
                          }
                          if(dollas.value != '' && dollas.value != null){
                              select = '';
                              selects = top_el.getElementsByTagName('select');
                              for(var r= 0; r < selects.length; r++){
                                  if(selects[r].name == 'items_pulldown_' + proj_code){
                                      select = selects[r];
                                  } 
                              }
                              sel_vals = select.value.split('XsX');
                              rate_card_code = sel_vals[0];
                              rate_card_item_code = sel_vals[1];
                              rate_card_name = select.options[select.selectedIndex].text;
                              price = make_money(dollas.value);
                              //now insert the new proj_pricing, then refresh both tables
                              server.insert('twog/proj_pricing', {'rate_card_code': rate_card_code, 'rate_card_item_code': rate_card_item_code, 'name': rate_card_name, 'proj_code': proj_code, 'price': price})
                              holder = document.getElementsByClassName('pricing_holder_' + proj_code)[0];
                              spt.api.load_panel(holder, 'cost_builder.ProjPricingWdg', {'order_sk': order_sk, 'proj_sk': proj_sk, 'rate_card_code': rate_card_code});
                              
                              price_cell = document_top.getElementsByClassName('price_' + proj_code)[0];
                              old_price = 0;
                              if(price_cell.innerHTML != '' && price_cell.innerHTML != null){
                                  old_price = Number(price_cell.innerHTML);
                              }
                              new_price = Number(new_price_cell.innerHTML.split(': ')[1]);
                              price_cell.innerHTML = new_price; 
                              price_cell.setAttribute('price',new_price);

                              proj_parent = price_cell.getAttribute('parent_sk');
                              p_p_code = proj_parent.split('code=')[1];
                              title_price_cell = document_top.getElementsByClassName('price_' + p_p_code)[0];
                              title_price = 0;
                              if(title_price_cell.innerHTML != '' && title_price_cell.innerHTML != null){ 
                                  title_price = Number(title_price_cell.getAttribute('price'));
                              }
                              new_title_price = Number(title_price) - Number(old_price) + Number(new_price);
                              title_price_cell.innerHTML = new_title_price;
                              title_price_cell.setAttribute('price',new_title_price);
  
                              title_parent = title_price_cell.getAttribute('parent_sk');
                              t_p_code = title_parent.split('code=')[1];
                              order_price_cell = document_top.getElementsByClassName('price_' + t_p_code)[0];
                              order_price = 0;
                              if(order_price_cell.innerHTML != '' && order_price_cell.innerHTML != null){
                                  order_price = Number(order_price_cell.getAttribute('price'));
                              }
                              new_order_price = Number(order_price) - Number(title_price) + Number(new_title_price);
                              order_price_cell.innerHTML = new_order_price;
                              order_price_cell.setAttribute('price', new_order_price);
                          }
                }
                catch(err){
                          spt.app_busy.hide();
                          alert(err);
                }
         ''' % (my.order_sk, proj_sk)}
        return behavior

    def kill_proj_pricing(my, proj_sk, proj_pricing_code, rate_card_code, price):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                          var server = TacticServerStub.get();
                          var order_sk = '%s';
                          var proj_sk = '%s';
                          var proj_pricing_code = '%s';
                          var rate_card_code = '%s';
                          var price = '%s';
                          var proj_code = proj_sk.split('code=')[1];
                          var order_code = order_sk.split('code=')[1];
                          proj_pricing_sk = server.build_search_key('twog/proj_pricing', proj_pricing_code);
                          server.delete_sobject(proj_pricing_sk);
                          holder = document.getElementsByClassName('pricing_holder_' + proj_code)[0];
                          spt.api.load_panel(holder, 'cost_builder.ProjPricingWdg', {'order_sk': order_sk, 'proj_sk': proj_sk, 'rate_card_code': rate_card_code});
                          var document_top = document.getElementsByClassName('twog_cost_builder_' + order_sk)[0];


                          price_cell = document_top.getElementsByClassName('price_' + proj_code)[0];
                          old_price = Number(price_cell.innerHTML);
                          new_price = old_price - Number(price); 
                          price_cell.innerHTML = new_price; 
                          price_cell.setAttribute('price',new_price);

                          proj_parent = price_cell.getAttribute('parent_sk');
                          p_p_code = proj_parent.split('code=')[1];
                          title_price_cell = document_top.getElementsByClassName('price_' + p_p_code)[0];
                          title_price = Number(title_price_cell.getAttribute('price'));
                          new_title_price = Number(title_price) - Number(price);
                          title_price_cell.innerHTML = new_title_price;
                          title_price_cell.setAttribute('price',new_title_price);
  
                          title_parent = title_price_cell.getAttribute('parent_sk');
                          t_p_code = title_parent.split('code=')[1];
                          order_price_cell = document_top.getElementsByClassName('price_' + t_p_code)[0];
                          order_price = Number(order_price_cell.getAttribute('price'));
                          new_order_price = Number(order_price) - Number(price);
                          order_price_cell.innerHTML = new_order_price;
                          order_price_cell.setAttribute('price', new_order_price);

//                          whole_order = document_top.getElementsByClassName('whole_' + order_code)[0];
//                          user = whole_order.getAttribute('user');
//                          sk = whole_order.getAttribute('sk');
//                          group = whole_order.getAttribute('group');
//                          visibles = whole_order.getAttribute('visibles');
//                          spt.api.load_panel(whole_order, 'cost_builder.CostTable', {'sk': sk, 'group': group, 'user': user, 'visibles': visibles});
                          
                }
                catch(err){
                          spt.app_busy.hide();
                          alert(err);
                }
         ''' % (my.order_sk, proj_sk, proj_pricing_code, rate_card_code, price)}
        return behavior

    def get_display(my):   
        my.proj_sk = str(my.kwargs.get('proj_sk'))
        my.order_sk = str(my.kwargs.get('order_sk'))
        my.rate_card_code = str(my.kwargs.get('rate_card_code'))
        proj_code = my.proj_sk.split('code=')[1]
        main_obj = my.server.eval("@SOBJECT(twog/proj['code','%s'])" % proj_code)[0]
        title_obj = my.server.eval("@SOBJECT(twog/title['code','%s'])" % main_obj.get('title_code'))[0]
        trt_pricing = title_obj.get('trt_pricing')
        #print "TITLE OBJ = %s" % title_obj
        #print "TITLE PRICING TRT = %s" % trt_pricing
        code = my.proj_sk.split('code=')[1]
        main_obj = my.server.eval("@SOBJECT(twog/proj['code','%s'])" % code)[0]

        items = my.server.eval("@SOBJECT(twog/rate_card_item['rate_card_code','%s']['@ORDER_BY','name'])" % my.rate_card_code) 
        items_pulldown = SelectWdg('items_pulldown_%s' % code)
        items_pulldown.append_option('--Select--','NOTHINGXsXNOTHING')
        for item in items:
            items_pulldown.append_option('%s: %s/min' % (item.get('name'), item.get('rate_per_minute')), '%sXsX%s' % (my.rate_card_code, item.get('code')))  
        items_pulldown.add_behavior(my.select_item(my.proj_sk, trt_pricing, my.rate_card_code)) 
        
        current_lines = my.server.eval("@SOBJECT(twog/proj_pricing['proj_code','%s'])" % proj_code)
        table = Table()
        table.add_attr('class','pricing_popout_%s' % proj_code)
        table.add_row()
        table.add_cell('Assign Prices for %s [%s]' % (main_obj.get('process'), trt_pricing))
        table.add_row()
        list_table = Table()
        list_table.add_style('background-color: #FFFFFF;')
        current_total = 0
        line_count = len(current_lines)
        count = 0
        for line in current_lines:
            line_price = line.get('price')
            if line_price in [None,'']:
                line_price = 0
            else:
                line_price = float(line_price)
            list_table.add_row()
            killer_cell = list_table.add_cell(my.x_butt)
            killer_cell.add_style('cursor: pointer;')
            killer_cell.add_behavior(my.kill_proj_pricing(my.proj_sk, line.get('code'), my.rate_card_code, line.get('price')))
            list_table.add_cell('%s = %s' % (line.get('name').replace(': ',' @ '), line_price))
            current_total = current_total + line_price
            if count < line_count - 1:
                list_table.add_row()
                list_table.add_cell('<hr/>')
            count = count + 1
        table.add_cell(list_table)
        
        if current_total in [None,'']:
            current_total = 0.0
        else:
            current_total = float(current_total)
        maker_table = Table()
        maker_table.add_row()
        items_cell = maker_table.add_cell(items_pulldown)
        dollas_txt = TextWdg('dollas_%s' % proj_code)
        dollas_txt.add_behavior(my.price_changed(my.proj_sk))
        dbag = maker_table.add_cell('$')
        dtext = maker_table.add_cell(dollas_txt)
        new_price_cell = maker_table.add_cell('&nbsp;&nbsp;New Proj Price: %.2f' % current_total) 
        new_price_cell.add_attr('class','new_price_%s' % proj_code)
        new_price_cell.add_attr('affected','nope')
        new_price_cell.add_attr('nowrap','nowrap')
        save_butt = maker_table.add_cell('<input type="button" value="Assign Price"/>')
        save_butt.add_behavior(my.save_line(my.proj_sk))

        table.add_row()
        table.add_cell(maker_table)
        holder = Table()
        holder.add_row()
        holder_cell = holder.add_cell(table)
        holder_cell.add_attr('class','pricing_holder_%s' % proj_code)
        
        return holder

class PriceWdg(BaseRefreshWdg):

    def init(my):
        from client.tactic_client_lib import TacticServerStub
        my.server = TacticServerStub.get()
        my.order_sk = ''
        my.sk = ''
        my.price = ''
        my.name = ''
        my.parent_sk = ''

    def launch_proj_line_item(my, proj_sk, proj_name):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                          var proj_sk = '%s';
                          var order_sk = '%s';
                          var proj_name = '%s';
                          proj_code = proj_sk.split('code=')[1];
                          var top_el = document.getElementsByClassName('twog_cost_builder_' + order_sk)[0];
                          var sels = top_el.getElementsByTagName('select');
                          var rate_card_code = 'NOTHING';
                          for(var r = 0; r < sels.length; r++){
                              if(sels[r].name == 'rate_card_select'){
                                  rate_card_code = sels[r].value;
                              }
                          }
                          if(rate_card_code != 'NOTHING' && rate_card_code != ''){
                              spt.panel.load_popup('Assign Rate Card Line Items for ' + proj_name + ' [' + proj_code + ']', 'cost_builder.ProjPricingWdg', {'order_sk': order_sk, 'proj_sk': proj_sk, 'rate_card_code': rate_card_code});
                          }else{
                              alert('You must choose a rate card before assigning prices.');
                          } 
                }
                catch(err){
                          spt.app_busy.hide();
                          alert(err);
                }
         ''' % (proj_sk, my.order_sk, proj_name)}
        return behavior

    def get_display(my):   
        my.order_sk = str(my.kwargs.get('order_sk'))
        my.sk = str(my.kwargs.get('sk'))
        my.name = str(my.kwargs.get('name'))
        my.parent_sk = str(my.kwargs.get('parent_sk'))
        code = my.sk.split('code=')[1]
        if 'price' in my.kwargs.keys():
            my.price = str(my.kwargs.get('price'))
        else:
            main_obj = my.server.eval("@SOBJECT(%s['code','%s'])" % (st, code))[0]
            my.price = main_obj.get('price')
        if my.price in ['',None]:
            my.price = 0.0
        else:
            my.price = float(my.price)
        st = my.sk.split('?')[0]
        table = Table()
        table.add_style('width: 100%s;' % '%')
        table.add_row()
        cell1 = table.add_cell(' ')
        cell1.add_style('width: 100%s;' % '%')
        cell2 = table.add_cell('%.2f' % my.price)   
        cell2.add_attr('class','price_%s' % code)
        cell2.add_attr('price', my.price)
        cell2.add_attr('parent_sk',my.parent_sk)
        if st == 'twog/proj':
            cell3 = table.add_cell('<img border="0" style="vertical-align: middle" src="/context/icons/silk/text_columns.png">')
            cell3.add_style('cursor: pointer;')
            cell3.add_behavior(my.launch_proj_line_item(my.sk, my.name))
      
        return table

        
        
class CostTools(BaseRefreshWdg):
    def init(my):
        from client.tactic_client_lib import TacticServerStub
        my.server = TacticServerStub.get()
        my.order_sk = ''

    def get_collapser_behavior(my): #NO SID NECC
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                          var order_sk = '%s';
                          var top_el = document.getElementsByClassName('twog_cost_builder_' + order_sk)[0];
                          var trs = top_el.getElementsByTagName('tr');
                          for(var r = 0; r < trs.length; r++){
                              if(trs[r].style.display == 'table-row'){
                                  trs[r].style.display = 'none';
                              }
                          }
                          rows =  top_el.getElementsByClassName('equipmentrow');
                          for(var r =0; r < rows.length; r++){
                              rows[r].style.display = 'none';
                          } 
                }
                catch(err){
                          spt.app_busy.hide();
                          alert(err);
                }
         ''' % my.order_sk}
        return behavior
    def get_expander_behavior(my): # NO SID NECC
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                          var order_sk = '%s';
                          var top_el = document.getElementsByClassName('twog_cost_builder_' + order_sk)[0];
                          var trs = top_el.getElementsByTagName('tr');
                          for(var r = 0; r < trs.length; r++){
                              if(trs[r].style.display == 'none'){
                                  trs[r].style.display = 'table-row';
                              }
                          }
                          rows =  top_el.getElementsByClassName('equipmentrow');
                          for(var r =0; r < rows.length; r++){
                              rows[r].style.display = 'table-row';
                          } 
                }
                catch(err){
                          spt.app_busy.hide();
                          alert(err);
                }
         ''' % my.order_sk}
        return behavior
    def get_equipment_collapser_behavior(my): #NO SID NECC
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                          var order_sk = '%s';
                          var top_el = document.getElementsByClassName('twog_cost_builder_' + order_sk)[0];
                          rows =  top_el.getElementsByClassName('equipmentrow');
                          for(var r =0; r < rows.length; r++){
                              rows[r].style.display = 'none';
                          } 
                }
                catch(err){
                          spt.app_busy.hide();
                          alert(err);
                }
         ''' % my.order_sk}
        return behavior
    def get_equipment_expander_behavior(my): # NO SID NECC
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                          var order_sk = '%s';
                          var top_el = document.getElementsByClassName('twog_cost_builder_' + order_sk)[0];
                          rows =  top_el.getElementsByClassName('equipmentrow');
                          for(var r =0; r < rows.length; r++){
                              rows[r].style.display = 'table-row';
                          } 
                }
                catch(err){
                          spt.app_busy.hide();
                          alert(err);
                }
         ''' % my.order_sk}
        return behavior

    def get_calc_costs_behavior(my): # NO SID NECC
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                          spt.app_busy.show('Calculating Costs...Please wait.')
                          unit_lookup = {'items': 'disc|tape|mile|miles|hr', 'gb': 'gb', 'mb': 'gb', 'tb': 'gb'}
                          var server = TacticServerStub.get();
                          var order_sk = '%s';
                          order_code = order_sk.split('code=')[1];
                          order  = server.eval("@SOBJECT(twog/order['code','" + order_code + "'])")[0];
                          order_expected_cost = 0;
                          order_actual_cost = 0;
                          titles = server.eval("@SOBJECT(twog/title['order_code','" + order_code + "'])")
                          for(var r= 0; r < titles.length; r++){
                              title_code = titles[r].code;
                              title_expected_cost = 0;
                              title_actual_cost = 0;
                              projs = server.eval("@SOBJECT(twog/proj['title_code','" + title_code + "'])")
                              for(var v = 0; v < projs.length; v++){
                                  proj_code = projs[v].code;
                                  proj_expected_cost = 0;
                                  proj_actual_cost = 0;
                                  wos = server.eval("@SOBJECT(twog/work_order['proj_code','" + proj_code + "'])")
                                  for(var x = 0; x < wos.length; x++){
                                      wo_code = wos[x].code;
                                      wo_expected_cost = 0;
                                      wo_actual_cost = 0;
                                      eqs = server.eval("@SOBJECT(twog/equipment_used['work_order_code','" + wo_code + "'])")
                                      for(var p = 0; p < eqs.length; p++){
                                          eq_used_code = eqs[p].code;
                                          units = eqs[p].units
                                          eq_code = eqs[p].equipment_code;
                                          if(eq_code == '' || eq_code == null){
                                              ek = server.eval("@SOBJECT(twog/equipment['name','" + eqs[p].name + "'])")
                                              if(ek.length > 0){
                                                  eq_code = ek[0].code
                                                  server.update(eqs[p].__search_key__, {'equipment_code': eq_code});
                                              }
                                          }
                                          //alert('EQU CODE = ' + eqs[p].code + ' EQ CODE = ' + eq_code);
                                          eq_expected_cost = 0;
                                          eq_actual_cost = 0;
                                          euc_expr = "@SOBJECT(twog/equipment_unit_cost['equipment_code','" + eq_code + "']['unit','in','" + unit_lookup[units] + "'])"
                                          //alert(euc_expr);
                                          unit_cost_obj = server.eval(euc_expr);
                                          if(unit_cost_obj.length < 1){
                                              euc_expr2 = "@SOBJECT(twog/equipment_unit_cost['equipment_code','" + eq_code + "']['unit','hr'])"
                                              //alert(euc_expr2);
                                              unit_cost_obj = server.eval(euc_expr2);
                                          }
                                          if(unit_cost_obj.length > 0){
                                              unit_cost = unit_cost_obj[0].cost;
                                              if(unit_cost == null || unit_cost == ''){
                                                  unit_cost = 0
                                              }else{
                                                  unit_cost = Number(unit_cost);
                                              }
                                          }else{
                                              unit_cost = 0
                                          }
                                          expected_quantity = 0;
                                          if(eqs[p].expected_quantity != '' || eqs[p].expected_quantity != null){
                                              expected_quantity = Number(eqs[p].expected_quantity); 
                                          }
                                          actual_quantity = 0;
                                          if(eqs[p].actual_quantity != '' || eqs[p].actual_quantity != null){
                                              actual_quantity = Number(eqs[p].actual_quantity); 
                                          }
                                          expected_duration = 0;
                                          if(eqs[p].expected_duration != '' || eqs[p].expected_duration != null){
                                              expected_duration = Number(eqs[p].expected_duration); 
                                          }
                                          actual_duration = 0;
                                          if(eqs[p].actual_duration != '' || eqs[p].actual_duration != null){
                                              actual_duration = Number(eqs[p].actual_duration); 
                                          }
                                          if(units == 'mb'){
                                              expected_quantity = expected_quantity/1000;
                                              actual_quantity = actual_quantity/1000;
                                          }else if(units == 'tb'){
                                              expected_quantity = expected_quantity * 1000;
                                              actual_quantity = actual_quantity * 1000;
                                          }
                                          
                                          eq_expected_cost = 0;
                                          eq_actual_cost = 0;
                                          if(units == 'items'){
                                              //alert('expected quant = ' + expected_quantity + ' *  unit_cost = ' + unit_cost + ' = ' + (expected_quantity * unit_cost));
                                              eq_expected_cost = expected_quantity * unit_cost;
                                              //alert('actual quant = ' + actual_quantity + ' *  unit_cost = ' + unit_cost + ' = ' + (actual_quantity * unit_cost));
                                              eq_actual_cost = actual_quantity * unit_cost;
                                          }else{
                                              //alert('expected quant = ' + expected_quantity + ' expected_dur = ' + expected_duration + ' *  unit_cost = ' + unit_cost + ' = ' + (expected_quantity * expected_duration * unit_cost));
                                              eq_expected_cost = expected_duration * expected_quantity * unit_cost;
                                              //alert('actual quant = ' + actual_quantity + ' actual_dur = ' + actual_duration + ' *  unit_cost = ' + unit_cost + ' = ' + (actual_quantity * actual_duration * unit_cost));
                                              eq_actual_cost = actual_duration * actual_quantity * unit_cost;
                                          }
                                          wo_actual = Number(wo_actual_cost); 
                                          wo_expected = Number(wo_expected_cost); 
                                          wo_actual_cost = wo_actual + eq_actual_cost;
                                          wo_expected_cost = wo_expected + eq_expected_cost;
                                          //alert('updating eq with expected: ' + eq_expected_cost + ' actual = ' + eq_actual_cost);
                                          server.update(eqs[p].__search_key__, {'expected_cost': eq_expected_cost, 'actual_cost': eq_actual_cost});
                                      }
                                      //Do expected for labor
                                      work_group = wos[x].work_group;
                                      est_whs = wos[x].estimated_work_hours;
                                      //alert('work group = ' + work_group + ' est_whs = ' + est_whs);
                                      if(est_whs == null || est_whs == ''){
                                          est_whs = 0
                                      }else{
                                          est_whs = Number(est_whs); 
                                      }
                                      login_group = server.eval("@SOBJECT(sthpw/login_group['login_group','" + work_group + "'])")
                                      hourly_rate = 0 
                                      if(login_group.length > 0){
                                          login_group = login_group[0];
                                          hourly_rate_part = login_group.hourly_rate;
                                          if(hourly_rate_part != '' && hourly_rate_part != null){
                                              hourly_rate = Number(hourly_rate_part);
                                          }
                                      }
                                      wo_expected_cost = Number(wo_expected_cost) + (hourly_rate * est_whs);

                                      //Do actual for labor
                                      wo_task = server.eval("@SOBJECT(sthpw/task['lookup_code','" + wo_code + "'])")
                                      if(wo_task.length > 0){
                                          task_code = wo_task[0].code;
                                          work_hours = server.eval("@SOBJECT(sthpw/work_hour['task_code','" + task_code + "'])")
                                          for(var w = 0; w < work_hours.length; w++){
                                              wh_login = work_hours[w].login;
                                              straight_time = work_hours[w].straight_time; 
                                              if(straight_time != '' && straight_time != null){
                                                  straight_time = Number(straight_time);
                                              }else{
                                                  straight_time = 0;
                                              }
                                              login_groups = server.eval("@SOBJECT(sthpw/login_in_group['login','" + wh_login + "'])")
                                              highest_rate = 0;
                                              for(var q = 0; q < login_groups.length; q++){
                                                  lg = server.eval("@SOBJECT(sthpw/login_group['login_group','" + login_groups[q].login_group + "'])")
                                                  rate = 0;
                                                  if(lg.length > 0){
                                                      rate_perhaps = lg[0].hourly_rate;
                                                      if(rate_perhaps != null && rate_perhaps != ''){
                                                          rate = Number(rate_perhaps);
                                                      }
                                                  }
                                                  if(rate > highest_rate){
                                                      highest_rate = rate;
                                                  } 
                                              }
                                              this_amt = straight_time * highest_rate;
                                              wo_actual_amount = Number(wo_actual_amount) + this_amt;
                                          }
                                      }
                                      //alert('updating wo with expected: ' + wo_expected_cost + ' actual = ' + wo_actual_cost);
                                      server.update(wos[x].__search_key__, {'actual_cost': wo_actual_cost, 'expected_cost': wo_expected_cost});
                                      proj_actual_cost = proj_actual_cost + wo_actual_cost;    
                                      proj_expected_cost = proj_expected_cost + wo_expected_cost;    
                                  }
                                  //alert('updating proj with expected: ' + proj_expected_cost + ' actual = ' + proj_actual_cost);
                                  server.update(projs[v].__search_key__,  {'actual_cost': proj_actual_cost, 'expected_cost': proj_expected_cost});
                                  title_actual_cost = title_actual_cost + proj_actual_cost;    
                                  title_expected_cost = title_expected_cost + proj_expected_cost;    

                              }
                              //alert('updating title with expected: ' + title_expected_cost + ' actual = ' + title_actual_cost);
                              server.update(titles[r].__search_key__,  {'actual_cost': title_actual_cost, 'expected_cost': title_expected_cost});
                              order_actual_cost = order_actual_cost + title_actual_cost;    
                              order_expected_cost = order_expected_cost + title_expected_cost;    
                          }
                          //alert('updating order with expected: ' + order_dict['expected_cost'] + ' actual = ' + order_dict['actual_cost']);
                          server.update(order_sk, {'actual_cost': order_actual_cost, 'expected_cost': order_expected_cost});
                          var document_top = document.getElementsByClassName('twog_cost_builder_' + order_sk)[0];
                          //alert(document_top);
                          whole_order = document_top.getElementsByClassName('whole_' + order_code)[0];
                          //alert(whole_order);
                          user = whole_order.getAttribute('user');
                          sk = whole_order.getAttribute('sk');
                          group = whole_order.getAttribute('group');
                          visibles = whole_order.getAttribute('visibles');
                          //alert('going to reload');
                          spt.api.load_panel(whole_order, 'cost_builder.CostTable', {'sk': sk, 'group': group, 'user': user, 'visibles': visibles});
                          //alert('reloaded');
                          spt.app_busy.hide();
                }
                catch(err){
                          spt.app_busy.hide();
                          //alert(err);
                }
         ''' % my.order_sk}
        return behavior

    def get_display(my):
        #--print "IN BUILDER TOOLS"
        my.order_sk = my.kwargs.get('order_sk')
        table = Table()
        table.add_attr('cellspacing','3')
        table.add_attr('cellpadding','3')
        table.add_attr('height','100%s' % '%')
        table.add_attr('bgcolor','#e4e6f0')
        table.add_style('border-bottom-right-radius', '10px')
        table.add_style('border-bottom-left-radius', '10px')
        table.add_style('border-top-right-radius', '10px')
        table.add_style('border-top-left-radius', '10px')

        #NEW START 
        table.add_row()
        title = table.add_cell(' &nbsp;&nbsp;&nbsp;<i><b>2G Cost Builder</b></i> ')
        title.add_attr('nowrap','nowrap')
        title.add_style('font-size: 120%s;' % '%')
        selected_obj = table.add_cell('')
        selected_obj.add_attr('class','selected_sobject')
        selected_obj.add_attr('width','100%s' % '%')
        #cc = table.add_cell('<u><b>Calculate Costs</b></u>')
        #cc.add_attr('align','right') 
        #cc.add_attr('nowrap','nowrap') 
        #cc.add_style('cursor: pointer;')
        #cc.add_behavior(my.get_calc_costs_behavior())
        rct = table.add_cell('Rate Card: ')
        rct.add_attr('align','right') 
        rct.add_attr('nowrap','nowrap') 
        rate_cards = my.server.eval("@SOBJECT(twog/rate_card)")
        rate_card_sel = SelectWdg('rate_card_select')
        rate_card_sel.append_option('--Select--','NOTHING')
        for rate_card in rate_cards:
            rate_card_sel.append_option(rate_card.get('name'),rate_card.get('code'))
        rc = table.add_cell(rate_card_sel)
        rc.add_attr('align','right') 
        eq_exp = ButtonSmallNewWdg(title="Show Equipment", icon=IconWdg.ARROW_OUT_EQUIPMENT)
        eq_exp.add_behavior(my.get_equipment_expander_behavior())
        eqb = table.add_cell(eq_exp)
        eqb.add_attr('align','right')

        eq_coll = ButtonSmallNewWdg(title="Hide Equipment", icon=IconWdg.ARROW_UP_EQUIPMENT)
        eq_coll.add_behavior(my.get_equipment_collapser_behavior())
        eqlb = table.add_cell(eq_coll)
        eqlb.add_attr('align','right')

        expander_button = ButtonSmallNewWdg(title="Expand All", icon=IconWdg.ARROW_OUT)
        expander_button.add_behavior(my.get_expander_behavior())
        exb = table.add_cell(expander_button)
        exb.add_attr('align','right')

        collapser_button = ButtonSmallNewWdg(title="Collapse All", icon=IconWdg.ARROW_UP_GREEN)
        collapser_button.add_behavior(my.get_collapser_behavior())
        clb = table.add_cell(collapser_button)
        clb.add_attr('align','right')

        space = table.add_cell(' ')
        space.add_attr('width','100%s' % '%') 
        #--print "LEAVING BUILDER TOOLS"
        return table

class CBScripts(BaseRefreshWdg):
    def init(my):
        my.order_sk = ''
        if 'order_sk' in my.kwargs.keys():
            my.order_sk = str(my.kwargs.get('order_sk'))
    def get_toggle_bottom(my, sk):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                          sk = '%s';
                          order_sk = '%s';
                          search_type = sk.split('?')[0];
                          var top_el = document.getElementsByClassName('twog_cost_builder_' + order_sk)[0];
                          if(search_type != 'sthpw/task' && search_type != 'twog/equipment_used'){
                              var bot = top_el.getElementsByClassName('bot_' + sk)[0];
                              if(bot.style.display == 'none'){
                                  bot.style.display = 'table-row';
                                  bvr.src_el.innerHTML = '<img border="0" style="vertical-align: middle" title="" src="/context/icons/custom/MinusIcon.png">';
                              }else{
                                  bot.style.display = 'none';
                                  bvr.src_el.innerHTML = '<img border="0" style="vertical-align: middle" title="" src="/context/icons/custom/PlusIcon.png">';
                              }
                          }
                          spt.app_busy.hide();
                }
                catch(err){
                          spt.app_busy.hide();
                          alert(err);
                }
         ''' % (sk, my.order_sk)}
        return behavior
