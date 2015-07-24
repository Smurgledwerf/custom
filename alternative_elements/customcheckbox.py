__all__ = ["CustomCheckboxWdg"]
from pyasm.web import Table, DivWdg
from tactic.ui.common import BaseTableElementWdg

class CustomCheckboxWdg(BaseTableElementWdg):
    #This is an alternative to the Tactic Checkbox, which is slow because it hits the database when you click it

    def init(my):
        my.checked = '<img src="/context/icons/custom/custom_checked.png"/>'
        my.not_checked = '<img src="/context/icons/custom/custom_unchecked.png"/>'

    def get_check_behavior(my):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                          checked_img = '%s';
                          unchecked_img = '%s';
                          if(bvr.src_el.getAttribute('checked') == 'false'){
                              bvr.src_el.innerHTML = checked_img;
                              bvr.src_el.setAttribute('checked','true'); 
                          }else{
                              bvr.src_el.innerHTML = unchecked_img;
                              bvr.src_el.setAttribute('checked','false'); 
                          }
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                }
        ''' % (my.checked, my.not_checked)}
        return behavior

    def get_display(my):
        name = ''
        alert_name = ''
        id = ''
        value_field = ''
        additional_js = ''
        checked = ''
        text = ''
        text_spot = ''
        text_align = ''
        nowrap = ''
        dom_class = 'custom_checkbox'
        parent_table = ''
        selected_color = ''
        normal_color = ''
        field = ''
        code = ''
        ntype = ''
        search_key = ''
        in_or_out = ''
        linked = ''
        task_sk = ''
        work_group = ''
        process = ''
        proj_code = ''
        title_code = ''
        order_code = ''
        task_code = ''
        woi_code = ''
        inter_code = ''
        wod_code = ''
        src_code = ''
        wo_code = ''
        task_code = ''
        sk = ''
        extra1 = ''
        extra2 = '' 
        extra3 = '' 
        extra4 = '' 
        extra5 = '' 
        extra6 = '' 
        extra7 = '' 
        extra8 = '' 
        
        if 'wo_code' in my.kwargs.keys():
            wo_code = my.kwargs.get('wo_code')
        if 'sk' in my.kwargs.keys():
            sk = my.kwargs.get('sk')
        if 'work_group' in my.kwargs.keys():
            work_group = my.kwargs.get('work_group')
        if 'process' in my.kwargs.keys():
            process = my.kwargs.get('process')
        if 'woi_code' in my.kwargs.keys():
            woi_code = my.kwargs.get('woi_code')
        if 'inter_code' in my.kwargs.keys():
            inter_code = my.kwargs.get('inter_code')
        if 'proj_code' in my.kwargs.keys():
            proj_code = my.kwargs.get('proj_code')
        if 'title_code' in my.kwargs.keys():
            title_code = my.kwargs.get('title_code')
        if 'order_code' in my.kwargs.keys():
            order_code = my.kwargs.get('order_code')
        if 'task_code' in my.kwargs.keys():
            task_code = my.kwargs.get('task_code')
        if 'name' in my.kwargs.keys():
            name = my.kwargs.get('name')
        if 'code' in my.kwargs.keys():
            code = my.kwargs.get('code')
        if 'ntype' in my.kwargs.keys():
            ntype = my.kwargs.get('ntype')
        if 'search_key' in my.kwargs.keys():
            search_key = my.kwargs.get('search_key')
        if 'alert_name' in my.kwargs.keys():
            alert_name = my.kwargs.get('alert_name')
        if 'id' in my.kwargs.keys():
            id = my.kwargs.get('id')
        if 'value_field' in my.kwargs.keys():
            value_field = my.kwargs.get('value_field')
        if 'additional_js' in my.kwargs.keys():
            additional_js = my.kwargs.get('additional_js')
        if 'checked' in my.kwargs.keys():
            checked = my.kwargs.get('checked') 
        if 'text' in my.kwargs.keys():
            text = my.kwargs.get('text') 
        if 'text_spot' in my.kwargs.keys():
            text_spot = my.kwargs.get('text_spot')
        if 'text_align' in my.kwargs.keys():
            text_align = my.kwargs.get('text_align')
        if 'nowrap' in my.kwargs.keys():
            nowrap = my.kwargs.get('nowrap')
        if 'dom_class' in my.kwargs.keys():
            dom_class = my.kwargs.get('dom_class')
        if 'parent_table' in my.kwargs.keys():
            parent_table = my.kwargs.get('parent_table')
        if 'selected_color' in my.kwargs.keys():
            selected_color = my.kwargs.get('selected_color')
        if 'normal_color' in my.kwargs.keys():
            normal_color = my.kwargs.get('normal_color')
        if 'field' in my.kwargs.keys():
            field = my.kwargs.get('field')
        if 'in_or_out' in my.kwargs.keys():
            in_or_out = my.kwargs.get('in_or_out')
        if 'linked' in my.kwargs.keys():
            linked = my.kwargs.get('linked')
        if 'task_sk' in my.kwargs.keys():
            task_sk = my.kwargs.get('task_sk')
        if 'wod_code' in my.kwargs.keys():
            wod_code = my.kwargs.get('wod_code')
        if 'src_code' in my.kwargs.keys():
            src_code = my.kwargs.get('src_code')
        if 'extra1' in my.kwargs.keys():
            extra1 = my.kwargs.get('extra1')
        if 'extra2' in my.kwargs.keys():
            extra2 = my.kwargs.get('extra2')
        if 'extra3' in my.kwargs.keys():
            extra3 = my.kwargs.get('extra3')
        if 'extra4' in my.kwargs.keys():
            extra4 = my.kwargs.get('extra4')
        if 'extra5' in my.kwargs.keys():
            extra5 = my.kwargs.get('extra5')
        if 'extra6' in my.kwargs.keys():
            extra6 = my.kwargs.get('extra6')
        if 'extra7' in my.kwargs.keys():
            extra7 = my.kwargs.get('extra7')
        if 'extra8' in my.kwargs.keys():
            extra8 = my.kwargs.get('extra8')
        if 'checked_img' in my.kwargs.keys():
            my.checked = '<img src="%s"/>' % my.kwargs.get('checked_img') 
        if 'unchecked_img' in my.kwargs.keys():
            my.not_checked = '<img src="%s"/>' % my.kwargs.get('unchecked_img') 

        if text_spot in ['Right','right','R','r']:
            text_spot = 'right'
        else:
            text_spot = 'left'

        if nowrap not in [None,'']:
            nowrap = 'nowrap'

        widget = DivWdg()
        table = Table()
        table.add_row()
        if text_spot == 'left':
            tcell = table.add_cell(text)
            if text_align not in [None,'']:
                tcell.add_attr('align',text_align)
            if nowrap not in [None,'']:
                tcell.add_attr('nowrap',nowrap)

        check_img = my.not_checked
        check_val = 'false'
        if checked in [True,'true','checked',1,'1']:
            check_img = my.checked
            check_val = 'true'
        cell1 = table.add_cell(check_img)
        cell1.add_attr('name', name)
        cell1.add_attr('alert_name', alert_name)
        cell1.add_attr('id', id)
        cell1.add_attr('value_field', value_field)
        cell1.add_attr('checked', check_val)
        cell1.add_attr('parent_table', parent_table)
        cell1.add_attr('selected_color', selected_color)
        cell1.add_attr('normal_color', normal_color)
        cell1.add_attr('field', field)
        cell1.add_attr('code', code)
        cell1.add_attr('ntype', ntype)
        cell1.add_attr('search_key', search_key)
        cell1.add_attr('in_or_out', in_or_out)
        cell1.add_attr('linked', linked)
        cell1.add_attr('task_sk', task_sk)
        cell1.add_attr('task_code', task_code)
        cell1.add_attr('order_code', order_code)
        cell1.add_attr('title_code', title_code)
        cell1.add_attr('proj_code', proj_code)
        cell1.add_attr('process', process)
        cell1.add_attr('work_group', work_group)
        cell1.add_attr('woi_code', woi_code)
        cell1.add_attr('inter_code', inter_code)
        cell1.add_attr('wod_code', wod_code)
        cell1.add_attr('src_code', src_code)
        cell1.add_attr('wo_code', wo_code)
        cell1.add_attr('sk', sk)
        cell1.add_attr('extra1', extra1)
        cell1.add_attr('extra2', extra2)
        cell1.add_attr('extra3', extra3)
        cell1.add_attr('extra4', extra4)
        cell1.add_attr('extra5', extra5)
        cell1.add_attr('extra6', extra6)
        cell1.add_attr('extra7', extra7)
        cell1.add_attr('extra8', extra8)
        if dom_class not in [None,'']:
            cell1.add_class(dom_class)
        launch_behavior = my.get_check_behavior()
        cell1.add_behavior(launch_behavior)
        if additional_js not in [None,'']:
            cell1.add_behavior(additional_js)

        if text_spot == 'right':
            tcell = table.add_cell(text)
            if text_align not in [None,'']:
                tcell.add_attr('align',text_align)
            if nowrap not in [None,'']:
                tcell.add_attr('nowrap',nowrap)
        widget.add(table)
        return widget

