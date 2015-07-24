__all__ = ["EquipmentHoursDisplayWdg"]
import tacticenv
from pyasm.common import Environment
from pyasm.biz import *
from pyasm.web import Table, DivWdg
from tactic.ui.common import BaseTableElementWdg
from tactic.ui.common import BaseRefreshWdg

class EquipmentHoursDisplayWdg(BaseTableElementWdg):
    def init(my):
        from client.tactic_client_lib import TacticServerStub
        my.server = TacticServerStub.get()
        my.login = Environment.get_login()
        my.user = my.login.get_login()
        my.work_order_code = ''
    def get_display(my):
        sobject = None
        total_only = False
        if 'work_order_code' in my.kwargs.keys():
            my.work_order_code = str(my.kwargs.get('work_order_code'))
            #print "WOC = %s" % my.work_order_code
        else:
            sobject = my.get_current_sobject()
            my.code = sobject.get_code()
            if 'WORK_ORDER' in my.code:
                my.work_order_code = my.code
            elif sobject.has_value('lookup_code'):
                lookup_code = sobject.get_value('lookup_code')
                if 'WORK_ORDER' in lookup_code:
                    my.work_order_code = lookup_code 
                else:
                    total_only = True
            else:
                total_only = True
                
        widget = DivWdg()
        table = Table()
        e_data_tbl = Table()
        e_data_tbl.add_attr('border','1')
        e_data_tbl.add_style('border-width: 1px;')
        est_dur_sum = 0
        act_dur_sum = 0
        if my.work_order_code not in [-1,'-1',None,'']:
            e_data_tbl.add_row()
            #e_data_tbl.add_cell('Code')
            e_data_tbl.add_cell('Name')
            e_data_tbl.add_cell('Quant&nbsp;&nbsp;')
            e_data_tbl.add_cell('Est. Hours&nbsp;&nbsp;')
            e_data_tbl.add_cell('Act. Hours&nbsp;&nbsp;')
            equipment = my.server.eval("@SOBJECT(twog/equipment_used['work_order_code','%s'])" % my.work_order_code)
            for equip in equipment:
                e_code = equip.get('code')
                e_name = equip.get('name')
                e_actdur = equip.get('actual_duration') 
                e_estdur = equip.get('expected_duration')
                e_quant = equip.get('expected_quantity')
                if e_estdur not in [None,'',0,'0']:
                    edf = float(e_estdur)
                    est_dur_sum = est_dur_sum + edf
                else:
                    e_estdur = '0'
                if e_actdur not in [None,'',0,'0']:
                    adf = float(e_actdur)
                    act_dur_sum = act_dur_sum + adf
                else:
                    e_actdur = '0'
                if e_quant in [None,'']:
                    e_quant = '0'
                e_data_tbl.add_row()
                #e_data_tbl.add_cell(e_code)
                name_cell = e_data_tbl.add_cell(e_name)
                name_cell.add_attr('title',e_code)
                e_data_tbl.add_cell(e_quant)
                e_data_tbl.add_cell(e_estdur)
                e_data_tbl.add_cell(e_actdur)
            if not equipment:
                e_data_tbl = Table()
        else:
            e_data_tbl = Table()
        table.add_row()
        if not total_only:     
            total_cell = table.add_cell('<b>TOTAL: %.2f</b>' % act_dur_sum) 
        else:
            total_cell = table.add_cell('<b>TOTAL: 0.00</b>')
        total_cell.add_attr('nowrap','nowrap')
	total_cell.add_style('font-size: 16px;')
        if not total_only:
            table.add_row()
            details = table.add_cell(e_data_tbl)
            details.add_style('padding-left: 10px;')
        widget.add(table)
        return widget
        
        
