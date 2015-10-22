__all__ = ['CustomPipelineToolWdg','CustomPipelineListWdg','CustomPipelineEditorWdg','CustomPipelinePropertyWdg','CustomConnectorPropertyWdg','CustomPipelineToolCanvasWdg','CustomPipeEditWdg','CustomPipelineSaveCbk']

import re
from custom_pipeline_canvas_wdg import CustomPipelineCanvasWdg
from tactic.ui.common import BaseRefreshWdg
from pyasm.common import Environment, Common, TacticException, jsonloads

from pyasm.widget import WidgetConfigView
from pyasm.biz import Pipeline, Project
from pyasm.web import DivWdg, WebContainer, Table, SpanWdg, HtmlElement
from pyasm.search import Search, SearchType, SearchKey, SObject
from tactic.ui.panel import FastTableLayoutWdg

from pyasm.widget import ProdIconButtonWdg, IconWdg, TextWdg, CheckboxWdg, HiddenWdg, SelectWdg

from tactic.ui.container import DialogWdg, TabWdg, SmartMenu, Menu, MenuItem, ResizableTableWdg
from tactic.ui.widget import ActionButtonWdg, SingleButtonWdg, IconButtonWdg
from client.tactic_client_lib import TacticServerStub

class CustomPipelineToolWdg(BaseRefreshWdg):
    '''This is the entire tool, including the sidebar and tabs, used to
    edit the various pipelines that exists'''

    def init(my):
        # to display pipelines of a certain search_type on load
        my.search_type = ''
        my.order_code = my.kwargs.get('order_code')
        my.order_sk = my.kwargs.get('order_sk')
        my.pipeline_code = my.kwargs.get('pipeline_code')

    def get_display(my):

        my.search_type = my.kwargs.get('search_type')
        top = my.top
        my.set_as_panel(top)
        top.add_class("spt_pipeline_tool_top")
        top.add_attr('st2',my.search_type)
        top.add_attr('order_code',my.order_code)
        top.add_attr('pipe_xmls','')
        #top.add_style("margin-top: 10px")

        #table = Table()
        table = ResizableTableWdg()

        #table.add_style("width: 100%")
        table.add_color("background", "background")
        table.add_color("color", "color")
        top.add(table)

        my.save_event = top.get_unique_event()

        cbjs_action = '''
        var el = bvr.firing_element;
        var edit_top = el.getParent(".spt_edit_top")

        var values = spt.api.get_input_values(edit_top, null, false);

        var group_name = values['edit|code'];
        var color = values['edit|color'];

        var top = bvr.src_el;
        var wrapper = top.getElement(".spt_pipeline_wrapper");
        spt.pipeline.init_cbk(wrapper);
        var group = spt.pipeline.get_group(group_name);
        if (group) {
            group.set_color(color);
        }

        var list = top.getElement(".spt_pipeline_list");
        spt.panel.refresh(list);
        '''

        top.add_behavior( {
        'type': 'listen',
        'event_name': my.save_event,
        'cbjs_action': cbjs_action
        } )
#        if my.pipeline_code not in [None,'']:
#            load_action = '''
#               pipeline_code = '%s';
#               jabberwocky = '1';
#               alert("JABBERWOCKY");
#               spt.pipeline.import_pipeline(pipeline_code);
#            ''' % my.pipeline_code
#            table.add_behavior( {
#            'type': 'load',
#            'cbjs_action': load_action
#            } )


        # only for new pipeline creation so that it gets clicked on after the UI refreshes
        save_new_cbjs_action = '''
        %s
        var server = TacticServerStub.get();
        var latest_pipeline_code = server.eval("@GET(sthpw/pipeline['@ORDER_BY','timestamp desc'].code)", {'single': true});
       
        spt.pipeline.remove_group("default");
        spt.named_events.fire_event('pipeline_' + latest_pipeline_code + '|click', bvr);
        '''%cbjs_action


        save_new_event = '%s_new' %my.save_event
        top.add_named_listener(save_new_event,  save_new_cbjs_action)


        # only for editing pipelines for a particular Stype when the UI refreshes
        load_event = '%s_load' %my.save_event
       
        

        table.add_row()
        left = table.add_cell()
        left.add_style("width: 200px")
        left.add_style("min-width: 200px")
        left.add_style("vertical-align: top")
        left.add_style("height: 400px;")
        left.add_border()

        pipeline_list = CustomPipelineListWdg(save_event=my.save_event, save_new_event=save_new_event, client_code=my.kwargs.get('client_code'), search_type=my.search_type, order_code=my.order_code)
        left.add(pipeline_list)

        right = table.add_cell()
        right.add_border()

        pipeline_wdg = CustomPipelineEditorWdg(height=my.kwargs.get('height'), width=my.kwargs.get('width'), save_new_event=save_new_event, order_code=my.order_code, order_sk=my.order_sk, pipeline_code=my.pipeline_code, pipeline=my.pipeline_code)
        right.add(pipeline_wdg)
        return top




    def get_extra_tab_menu(my):
        menu = Menu(width=180)

        menu_item = MenuItem(type='title', label='Raw Data')
        menu.add(menu_item)

        menu_item = MenuItem(type='action', label='Show Site Wide Pipelines')
        menu_item.add_behavior( {
        'cbjs_action': '''
        var class_name = 'tactic.ui.panel.ViewPanelWdg';
        var kwargs = {
            search_type: 'sthpw/pipeline',
            view: 'site_wide',
            show_search: 'false',
            expression: "@SOBJECT(sthpw/pipeline['project_code is NULL'])"
        }
        var header = spt.smenu.get_activator(bvr);
        var top = header.getParent(".spt_tab_top");
        spt.tab.set_tab_top(top);
        spt.tab.add_new("site_wide_pipeline", "Site Wide Pipelines", class_name, kwargs);

        '''
        } )
        menu.add(menu_item)



        menu_item = MenuItem(type='action', label='Show Raw Processes')
        menu_item.add_behavior( {
        'cbjs_action': '''
        var class_name = 'tactic.ui.panel.ViewPanelWdg';
        var kwargs = {
            search_type: 'config/process',
            view: 'table',
        }
        var header = spt.smenu.get_activator(bvr);
        var top = header.getParent(".spt_tab_top");
        spt.tab.set_tab_top(top);
        spt.tab.add_new("processes", "Processes", class_name, kwargs);

        '''
        } )
        menu.add(menu_item)


        menu_item = MenuItem(type='action', label='Show Raw Naming')
        menu_item.add_behavior( {
        'cbjs_action': '''
        var class_name = 'tactic.ui.panel.ViewPanelWdg';
        var kwargs = {
            search_type: 'config/naming',
            view: 'table',
        }
        var header = spt.smenu.get_activator(bvr);
        var top = header.getParent(".spt_tab_top");
        spt.tab.set_tab_top(top);
        spt.tab.add_new("naming", "Naming", class_name, kwargs);

        '''
        } )
        menu.add(menu_item)

        menu_item = MenuItem(type='action', label='Show Raw Triggers')
        menu_item.add_behavior( {
        'cbjs_action': '''
        var class_name = 'tactic.ui.panel.ViewPanelWdg';
        var kwargs = {
            search_type: 'config/trigger',
            view: 'table',
        }
        var header = spt.smenu.get_activator(bvr);
        var top = header.getParent(".spt_tab_top");
        spt.tab.set_tab_top(top);
        spt.tab.add_new("trigger", "Triggers", class_name, kwargs);

        '''
        } )
        menu.add(menu_item)


        menu_item = MenuItem(type='action', label='Show Raw Notification')
        menu_item.add_behavior( {
        'cbjs_action': '''
        var class_name = 'tactic.ui.panel.ViewPanelWdg';
        var kwargs = {
            search_type: 'sthpw/notification',
            view: 'table',
        }
        var header = spt.smenu.get_activator(bvr);
        var top = header.getParent(".spt_tab_top");
        spt.tab.set_tab_top(top);
        spt.tab.add_new("notification", "Notifications", class_name, kwargs);

        '''
        } )
        menu.add(menu_item)




        return menu



class CustomPipelineListWdg(BaseRefreshWdg):

        
    def init(my):
        my.server = TacticServerStub.get()
        my.save_event = my.kwargs.get("save_event")
        my.order_code = my.kwargs.get('order_code')
        my.save_new_event = my.kwargs.get("save_new_event")
        my.client_code = my.kwargs.get('client_code')
        my.client_name = my.kwargs.get('client_name')
        my.search_type = my.kwargs.get('search_type')

    def get_display(my):
        my.client_name = 'No Client Name'
        client_name_expr = "@GET(twog/client['code','%s'].name)" % my.client_code 
        cl_res = my.server.eval(client_name_expr)
        if len(cl_res) > 0:
            my.client_name = cl_res[0]
       

        top = my.top
        top.add_class("spt_pipeline_list")
        my.set_as_panel(top)

        title_div = DivWdg()


        button = ActionButtonWdg(title="+", tip="Add a new pipeline", size='small')
        button.add_style("float: right")
        button.add_style("margin-top: -8px")

        button.add_behavior( {
        'type': 'click_up',
        'save_event': my.save_new_event,
        'cbjs_action': '''
        var order_code = '%s';
        var client_name = '%s';
        var holder = '';
        var holders = document.getElementsByClassName("spt_pipeline_tool_top");
        for(var r= 0; r < holders.length; r++){
            if(holders[r].getAttribute('order_code') == order_code){
                holder = holders[r];
            }
        }
        var st2 = holder.getAttribute('st2');
        var class_name = 'order_builder.CustomPipeEditWdg';
        var kwargs = {
            st2: st2,
            client_name: client_name,
            order_code: order_code,
            search_type: 'sthpw/pipeline',
            view: 'insert',
            single: true,
            save_event: bvr.save_event
        }
        spt.api.load_popup("Add New Pipeline", class_name, kwargs);
        ''' % (my.order_code, my.client_name)
        } )



        title_div.add(button)

        top.add(title_div)
        title_div.add_style("height: 20px")
        title_div.add_style("padding-left: 5px")
        title_div.add_style("padding-top: 8px")
        title_div.add_gradient("background", "background")
        title_div.add("<b>Pipelines</b>")



        top.add("<br/>")

        pipelines_div = DivWdg()
        top.add(pipelines_div)
        pipelines_div.add_class("spt_resizable")
        #pipelines_div.add_style("overflow: auto")
        pipelines_div.add_style("overflow-y: scroll")
        pipelines_div.add_style("overflow-x: scroll")
        pipelines_div.add_style("min-height: 290px")
        pipelines_div.add_style("min-width: 200px")
        pipelines_div.add_style("width: 200px;")
        pipelines_div.add_style("height: 500px;")

        inner = DivWdg()
        inner.add_class("spt_pipeline_list_top")
        inner.add_style("width: 300px")
        inner.add_style("height: 290px")
        pipelines_div.add(inner)


        # add in a context menu
        menu = my.get_pipeline_context_menu()
        menus = [menu.get_data()]
        menus_in = {
            'PIPELINE_CTX': menus,
        }
        from tactic.ui.container.smart_menu_wdg import SmartMenu
        SmartMenu.attach_smart_context_menu( pipelines_div, menus_in, False )


        project_code = Project.get_project_code()


        # project_specific  pipelines
        from pyasm.widget import SwapDisplayWdg
        swap = SwapDisplayWdg(on_event_name='proj_pipe_on', off_event_name='proj_pipe_off')
        # open by default
        inner.add(swap)
        swap.add_style("float: left")

        title = DivWdg("<b>2G Pipelines</b>")
        title.add_style("padding-bottom: 2px")
        inner.add(title)
        #inner.add(HtmlElement.br())
        content_div = DivWdg()
        content_div.add_styles('padding-left: 8px; padding-top: 6px') 
        SwapDisplayWdg.create_swap_title(title, swap, content_div, is_open=True)
        inner.add(content_div)
        try:
            #search = Search("config/pipeline")
            #pipelines = search.get_sobjects()
            search = Search("sthpw/pipeline")
            search.add_filter("project_code", project_code)
            search.add_filter("search_type", "sthpw/task", op="!=")
            #search.add_filter("hide", ['True','true','T','t','1'], op='not in')
            # This pretty weird that != does not find NULL values
            search.add_filter("search_type", "NULL", op='is', quoted=False)
            search.add_op("or")
            pipelines = search.get_sobjects()
 
             
            client_pipes = {'twog/title': [], 'twog/proj': [], 'other': []}
            other_pipes = {'twog/title': {}, 'twog/proj': {}, 'other': {}}
            translate = {'twog/title': 'Title', 'twog/proj': 'Project', 'other': 'Other'}
            translate_open = {'twog/title': False, 'twog/proj': False, 'twog/order': False, 'other': False}
            translate_open[my.search_type] = True
            beginnings = []
            f_seq = False
            for pipeline in pipelines:
                if not pipeline.get_value('hide'):
                    pcode = pipeline.get_code()
                    pcode = pcode.rstrip(' ')
                    pcode = pcode.strip(' ')
                    beginning = pcode.split('_')[0]
                    if len(beginning) == len(pcode):
                        beginning = pcode.split(' ')[0]
                    st = pipeline.get_value('search_type')
                    if st not in ['twog/proj','twog/title']:
                        st = 'other'
                    if beginning == my.client_name:
                        client_pipes[st].append(pipeline)
                    else:
                        if 'twog/' not in beginning:
                            if beginning not in beginnings:
                                beginnings.append(beginning)
                            if beginning not in other_pipes[st].keys():
                                other_pipes[st][beginning] = []
                            other_pipes[st][beginning].append(pipeline)
            
            beginnings.sort()
            client_title = DivWdg("<b>%s</b>" % my.client_name)
            client_title.add_style('padding-bottom: 2px;')
            content_div.add(client_title)
            client_content_div = DivWdg()
            client_content_div.add_styles('padding-left: 12px; padding-top: 6px') 
            swap1 = SwapDisplayWdg()
            swap1.add_style("float: left")
            SwapDisplayWdg.create_swap_title(client_title, swap1, client_content_div, is_open=True)
            content_div.add(client_content_div) 
            for k in client_pipes.keys():
                sub_title = DivWdg("<b>%s</b>" % translate[k])
                sub_title.add_style('padding-bottom: 2px;')
                client_content_div.add(sub_title)
                sub_content_div = DivWdg()
                sub_content_div.add_styles('padding-left: 16px; padding-top: 6px') 
                swap2 = SwapDisplayWdg()
                swap2.add_style("float: left")
                SwapDisplayWdg.create_swap_title(sub_title, swap2, sub_content_div, is_open=translate_open[k])
                client_content_div.add(sub_content_div) 
                for pipeline in client_pipes[k]:
                    pipeline_div = my.get_pipeline_wdg(pipeline)
                    sub_content_div.add(pipeline_div)
                
            for beginning in beginnings:
                client_title = DivWdg("<b>%s</b>" % beginning)
                client_title.add_style('padding-bottom: 2px;')
                content_div.add(client_title)
                client_content_div = DivWdg()
                client_content_div.add_styles('padding-left: 12px; padding-top: 6px') 
                swap3 = SwapDisplayWdg()
                swap3.add_style("float: left")
                SwapDisplayWdg.create_swap_title(client_title, swap3, client_content_div, is_open=False)
                content_div.add(client_content_div) 
                for k in other_pipes.keys():
                    sub_title = DivWdg("<b>%s</b>" % translate[k])
                    sub_title.add_style('padding-bottom: 2px;')
                    client_content_div.add(sub_title)
                    sub_content_div2 = DivWdg()
                    sub_content_div2.add_styles('padding-left: 16px; padding-top: 6px') 
                    swap4 = SwapDisplayWdg()
                    swap4.add_style("float: left")
                    SwapDisplayWdg.create_swap_title(sub_title, swap4, sub_content_div2, is_open=False)
                    client_content_div.add(sub_content_div2) 
                    if beginning in other_pipes[k].keys():
                        for pipeline in other_pipes[k][beginning]:
                            pipeline_div = my.get_pipeline_wdg(pipeline)
                            sub_content_div2.add(pipeline_div)
                      
 

            if not pipelines:
                no_items = DivWdg()
                no_items.add_style("padding: 3px 0px 3px 20px")
                content_div.add(no_items)
                no_items.add("<i>-- No Items --</i>")

        except:
            none_wdg = DivWdg("<i>&nbsp;&nbsp;-- No Items --</i>")
            none_wdg.add_style("font-size: 11px")
            none_wdg.add_color("color", "color", 20)
            none_wdg.add_style("padding", "5px")
            content_div.add( none_wdg )

        inner.add("<br clear='all'/>")

        # task status pipelines
        swap = SwapDisplayWdg()
        inner.add(swap)
        swap.add_style("float: left")

        title = DivWdg("<b>Task Status Pipelines</b>")
        title.add_style("padding-bottom: 2px")
        inner.add(title)
        content_div = DivWdg()
        content_div.add_styles('padding-left: 8px; padding-top: 6px') 
        SwapDisplayWdg.create_swap_title(title, swap, content_div, is_open=False)
        inner.add(content_div)

        search = Search("sthpw/pipeline")
        search.add_filter("project_code", project_code)
        search.add_filter("search_type", "sthpw/task")
        pipelines = search.get_sobjects()

        colors = {}
        for pipeline in pipelines:
            if not pipeline.get_value('hide'):
                pipeline_div = my.get_pipeline_wdg(pipeline)
                content_div.add(pipeline_div)
                colors[pipeline.get_code()] = pipeline.get_value("color")

        if not pipelines:
            no_items = DivWdg()
            no_items.add_style("padding: 3px 0px 3px 20px")
            content_div.add(no_items)
            no_items.add("<i>-- No Items --</i>")




        inner.add("<br clear='all'/>")



        # site-wide  pipelines
        search = Search("sthpw/pipeline")
        search.add_filter("project_code", "NULL", op="is", quoted=False)
        pipelines = search.get_sobjects()

        swap = SwapDisplayWdg()

        title = DivWdg()
        inner.add(swap)
        swap.add_style("margin-top: -2px")
        inner.add(title)
        swap.add_style("float: left")
        title.add("<b>Site Wide Pipelines</b><br/>")
      
        site_wide_div = DivWdg()
        site_wide_div.add_styles('padding-left: 8px; padding-top: 6px') 
        SwapDisplayWdg.create_swap_title(title, swap, site_wide_div, is_open=False)

        colors = {}
        inner.add(site_wide_div)
        site_wide_div.add_class("spt_pipeline_list_site")

        for pipeline in pipelines:
            if not pipeline.get_value('hide'):
                pipeline_div = my.get_pipeline_wdg(pipeline)
                site_wide_div.add(pipeline_div)
                colors[pipeline.get_code()] = pipeline.get_value("color")

        # this is done in spt.pipeline.first_init() already
        """
        inner.add_behavior( {
        'type': 'load',
        'colors': colors,
        'cbjs_action': '''
        var top = bvr.src_el.getParent(".spt_pipeline_tool_top");
        var wrapper = top.getElement(".spt_pipeline_wrapper");
        spt.pipeline.init_cbk(wrapper);
        var data = spt.pipeline.get_data();
        data.colors = bvr.colors;
        '''
        } )
        """

        return top




    def get_pipeline_wdg(my, pipeline):
        '''build each pipeline menu item'''
        pipeline_div = DivWdg()
        pipeline_div.add_class('spt_pipeline_link')
        pipeline_div.add_attr('spt_pipeline', pipeline.get_code())
        pipeline_div.add_style("padding: 3px")
        pipeline_div.add_class("hand")
        description = pipeline.get_value("description")
        if not description:
            description = pipeline.get_code()
        
        # remove weird symbols in description
        description = re.sub(r'\W', '', description)
        
        pipeline_div.add_attr("title", description)

        color = pipeline_div.get_color("background", -20)
        pipeline_div.add_behavior( {
            'type': 'hover',
            'color': color,
            'cbjs_action_over': '''
            bvr.src_el.setStyle("background", bvr.color);
            ''',
            'cbjs_action_out': '''
            bvr.src_el.setStyle("background", "");
            ''',
        } )

        color_div = DivWdg()
        color_div.add_style("height: 20px")
        color_div.add_style("width: 20px")
        color_div.add_style("float: left")
        color = pipeline.get_value("color")
        if not color:
            color = ""
        color_div.add_border()
        color_div.add_style("background: %s" % color)
        pipeline_div.add(color_div)

        pipeline_code = pipeline.get_code()
        title = pipeline_code.split("/")[-1]
        pipeline_div.add("&nbsp;&nbsp;&nbsp;%s" % title)

        pipeline_div.add_behavior( {
        'type': 'listen',
        'pipeline_code': pipeline_code,
        'event_name': 'pipeline_%s|click' %pipeline_code,
        'cbjs_action': '''
        //var src_el = bvr.firing_element;
        var top = null;
        // they could be different when inserting or just clicked on
        [bvr.firing_element, bvr.src_el].each(function(el) {

            top = el.getParent(".spt_pipeline_tool_top");
            if (top) return top;
        }
        );
        if (!top)
            top = spt.get_element(document, '.spt_pipeline_tool_top');
        var wrapper = top.getElement(".spt_pipeline_wrapper");
        spt.pipeline.init_cbk(wrapper);

        //bvr.src_el.setStyle("border", "dashed 1px #AAA");

        // check if the group already exists
        var group_name = bvr.pipeline_code;
        var group = spt.pipeline.get_group(bvr.pipeline_code);
        if (group != null) {

            // if it already exists, then select all from the group
            spt.pipeline.select_nodes_by_group(group_name);
            spt.pipeline.fit_to_canvas(group_name);
            return;

            /*
            var flag = confirm("Pipeline ["+bvr.pipeline_code+"] is already loaded.  Do you wish to reload? (Changes will be lost)");
            if (!flag) {
                return;
            } else {
                spt.pipeline.remove_group(bvr.pipeline_code);
            }
            */
        }

        spt.pipeline.import_pipeline(bvr.pipeline_code);
        pipe_xmls = top.getAttribute('pipe_xmls');
        //alert('pipe_xmls = ' + pipe_xmls);
        pxs = pipe_xmls.split('XsX');
        pipes = {};
        pipe_arr = []
        got_it = false;
        for(var r = 0; r < pxs.length; r++){
            //alert('pxs[r] = ' + pxs[r] + ' bvr.pipeline_code = ' + bvr.pipeline_code);
            if(pxs[r] == bvr.pipeline_code){
                pipes[pxs[r]] = spt.pipeline.export_groups();
                pipe_arr.push(bvr.pipeline_code);
                got_it = true;
            } 
            else if(r %s 2 == 0){
                pipe_arr.push(pxs[r]);
                pipes[pxs[r]] = pxs[r+1];
            }
        }
        pipe_str = '';
        if(pxs.length > 1){
            for(var r = 0; r < pipe_arr.length; r++){
                if(pipe_str == ''){
                    //alert('pipe_str has nothing');
                    pipe_str = pipe_arr[r] + 'XsX' + pipes[pipe_arr[r]];
                }else{
                    //alert('pipe_str has something: ' + pipe_str);
                    pipe_str = pipe_str + 'XsX' + pipe_arr[r] + 'XsX' + pipes[pipe_arr[r]];
                }
            }
        }
        //alert('got_it = ' + got_it);
        if(!got_it){
            this_xml = spt.pipeline.export_groups();
            //alert(this_xml);
            if(pipe_str == ''){
                pipe_str = bvr.pipeline_code + 'XsX' + this_xml;
            }else{
                pipe_str = 'XsX' + bvr.pipeline_code + 'XsX' + this_xml;
            }
        }
        //alert('diff sect pipe_str = ' + pipe_str);
        top.setAttribute('pipe_xmls',pipe_str);


        // add to the current list
        var value = bvr.pipeline_code;
        var select = top.getElement(".spt_pipeline_editor_current");
        for ( var i = 0; i < select.options.length; i++) {
            var select_value = select.options[i].value;
            if (select_value == value) {
                alert("Pipeline ["+value+"] already exists");
                return;
            }
        }

        var option = new Option(value, value);
        select.options[select.options.length] = option;

        select.value = value;
        spt.pipeline.set_current_group(value);
        ''' % '%'
        })

        
        pipeline_div.add_behavior( {'type': 'click_up',
            
            'event': 'pipeline_%s|click' %pipeline_code,
            'cbjs_action': '''
             spt.named_events.fire_event(bvr.event, bvr);
             '''
             })

        search_type = pipeline.get_value("search_type")
        if search_type:
            span = SpanWdg()
            span.add_style("font-size: 11px")
            span.add_style("opacity: 0.75")
            pipeline_div.add(span)
            span.add(" (%s)" % search_type)

        pipeline_div.add("<br clear='all'/>")

        pipeline_div.add_attr("spt_element_name", pipeline_code)
        from tactic.ui.container.smart_menu_wdg import SmartMenu
        SmartMenu.assign_as_local_activator( pipeline_div, 'PIPELINE_CTX' )

        return pipeline_div




    def get_pipeline_context_menu(my):

        menu = Menu(width=180)
        menu.set_allow_icons(False)
        menu.set_setup_cbfn( 'spt.dg_table.smenu_ctx.setup_cbk' )


        menu_item = MenuItem(type='title', label='Actions')
        menu.add(menu_item)

        """
        menu_item = MenuItem(type='action', label='Copy to Project')
        menu_item.add_behavior( {
            'cbjs_action': '''
            alert('Not implemented');
            '''
        } )
        menu.add(menu_item)
        """


        

        menu_item = MenuItem(type='action', label='Edit Pipeline Data')
        menu_item.add_behavior( {
            'cbjs_action': '''
            var order_code = '%s';
            var client_name = '%s';
            var holder = '';
            var holders = document.getElementsByClassName("spt_pipeline_tool_top");
            for(var r= 0; r < holders.length; r++){
                if(holders[r].getAttribute('order_code') == order_code){
                    holder = holders[r];
                }
            }
            var st2 = holder.getAttribute('st2');
            var activator = spt.smenu.get_activator(bvr);
            var code = activator.getAttribute("spt_pipeline");
            var search_type = 'sthpw/pipeline';
            var kwargs = {
                'st2': st2,
                'order_code': order_code,
                'client_name': client_name,
                'search_type': search_type,
                'code': code,
                'view': 'pipeline_edit_tool',
                'save_event': '%s'
            };
            var class_name = 'order_builder.CustomPipeEditWdg';
            spt.panel.load_popup("Edit Pipeline", class_name, kwargs);
            ''' % (my.order_code, my.client_name, my.save_event)
        } )
        menu.add(menu_item)

        return menu




class CustomPipelineEditorWdg(BaseRefreshWdg):
    '''This is the pipeline on its own, with various buttons and interface
    to help in building the pipelines.  It contains the CustomPipelineCanvasWdg'''
    def init(my):
        my.order_code = ''
        my.order_sk = ''
        my.pipeline_code = ''

    def get_display(my):
        my.order_code = my.kwargs.get('order_code')
        my.order_sk = my.kwargs.get('order_sk')
        my.pipeline_code = my.kwargs.get('pipeline_code')
        top = DivWdg()
        my.set_as_panel(top)
        top.add_class("spt_pipeline_editor_top")

        my.save_new_event = my.kwargs.get("save_new_event")


        top.add(my.get_shelf_wdg() )


        top.add("<br clear='all'/>")
        my.width = my.kwargs.get("width")
        if not my.width:
            my.width = 1400
        my.height = my.kwargs.get("height")
        if not my.height:
            my.height = 600

        
        #search_type_wdg = my.get_search_type_wdg()
        #top.add(search_type_wdg)

        from tactic.ui.tools.schema_wdg import SchemaToolCanvasWdg
        schema_top = DivWdg()
        top.add(schema_top)
        schema_top.add_class("spt_schema_wrapper")
        schema_top.add_style("display: none")
        schema_top.add_style("position: relative")
        schema = SchemaToolCanvasWdg(height='150')
        schema_top.add(schema)

        schema_title = DivWdg()
        schema_top.add(schema_title)
        schema_title.add("Schema")
        schema_title.add_border()
        schema_title.add_style("padding: 3px")
        schema_title.add_style("position: absolute")
        schema_title.add_style("font-weight: bold")
        schema_title.add_style("top: 0px")
        schema_title.add_style("left: 0px")


        canvas_top = DivWdg()
        top.add(canvas_top)
        canvas_top.add_class("spt_pipeline_wrapper")
        canvas_top.add_style("position: relative")
        canvas = my.get_canvas()
        canvas_top.add(canvas)


        canvas_title = DivWdg()
        canvas_top.add(canvas_title)
        canvas_title.add("Pipelines")
        canvas_title.add_border()
        canvas_title.add_style("padding: 3px")
        canvas_title.add_style("position: absolute")
        canvas_title.add_style("font-weight: bold")
        canvas_title.add_style("top: 0px")
        canvas_title.add_style("left: 0px")





        div = DivWdg()
        pipeline_str = my.kwargs.get("pipeline")
        if pipeline_str:
            pipelines = pipeline_str.split("|")

            div.add_behavior( {
            'type': 'load',
            'pipelines': pipelines,
            'cbjs_action': '''
            var top = bvr.src_el.getParent(".spt_pipeline_tool_top");
            var wrapper = top.getElement(".spt_pipeline_wrapper");
            spt.pipeline.init_cbk(wrapper);

            for (var i=0; i<bvr.pipelines.length; i++) {
                spt.pipeline.import_pipeline(bvr.pipelines[i]);
            }
            '''
            } )
            top.add(div)

        return top


    def get_shelf_wdg(my):
 
        shelf_wdg = DivWdg()
        shelf_wdg.add_style("padding: 5px")

        my.properties_dialog = DialogWdg(display=False)
        my.properties_dialog.add_title("Edit Properties")
        props_div = DivWdg()
        my.properties_dialog.add(props_div)
        properties_wdg = CustomPipelinePropertyWdg(pipeline_code='', process='')
        my.properties_dialog.add(properties_wdg )
        connector_wdg = CustomConnectorPropertyWdg()
        my.properties_dialog.add(connector_wdg )

        props_div.add_behavior( {
            'type': 'listen',
            'dialog_id': my.properties_dialog.get_id(),
            'event_name': 'pipeline|show_properties',
            'cbjs_action': '''
            var node = bvr.firing_element;
            var top = node.getParent(".spt_pipeline_editor_top");
            var wrapper = top.getElement(".spt_pipeline_wrapper");
            spt.pipeline.init_cbk(wrapper);

            spt.pipeline.clear_selected();
            spt.pipeline.select_node(node);

            spt.show( $(bvr.dialog_id) );
            spt.pipeline_properties.show_node_properties(node);
            '''
        } )





        spacing_divs = []
        for i in range(0, 3):
            spacing_div = DivWdg()
            spacing_divs.append(spacing_div)
            spacing_div.add_style("height: 32px")
            spacing_div.add_style("width: 2px")
            spacing_div.add_style("margin: 0 10 0 20")
            spacing_div.add_style("border-style: solid")
            spacing_div.add_style("border-width: 0 0 0 1")
            spacing_div.add_style("border-color: %s" % spacing_div.get_color("border"))
            spacing_div.add_style("float: left")


        button_div = my.get_buttons_wdg();
        button_div.add_style("float: left")
        shelf_wdg.add(button_div)

        shelf_wdg.add(spacing_divs[0])

        group_div = my.get_pipeline_select_wdg();
        group_div.add_style("float: left")
        group_div.add_style("margin-top: 1px")
        group_div.add_style("margin-left: 10px")
        shelf_wdg.add(group_div)

        shelf_wdg.add(spacing_divs[1])

        button_div = my.get_zoom_buttons_wdg();
        button_div.add_style("margin-left: 10px")
        button_div.add_style("margin-right: 15px")
        button_div.add_style("float: left")
        shelf_wdg.add(button_div)

        # Show schema for reference.  This does not work very well.
        # Disabling
        """
        shelf_wdg.add(spacing_divs[2])

        button_div = my.get_schema_buttons_wdg();
        button_div.add_style("margin-left: 10px")
        button_div.add_style("float: left")
        shelf_wdg.add(button_div)
        """

        help_button = ActionButtonWdg(title="?", tip="Show Workflow Editor Help", size='s')
        shelf_wdg.add(help_button)
        help_button.add_behavior( {
            'type': 'click_up',
            'cbjs_action': '''
            spt.help.set_top();
            spt.help.load_alias("project-workflow|project-workflow-introduction|pipeline-process-options");
            '''
        } )



        return shelf_wdg


    def get_canvas(my):
        canvas = CustomPipelineToolCanvasWdg(height=my.height, width=my.width)
        return canvas



    def get_buttons_wdg(my):
        from pyasm.widget import IconWdg
        from tactic.ui.widget.button_new_wdg import ButtonNewWdg, ButtonRowWdg
        login = Environment.get_login()
        user_name = login.get_login()


        button_row = ButtonRowWdg(show_title=True)

        project_code = Project.get_project_code()

        button = ButtonNewWdg(title="Save Pipeline", icon=IconWdg.SAVE)
        button_row.add(button)

        button.add_behavior( {
        'type': 'click_up',
        'project_code': project_code,
        'save_event': my.save_new_event,
        'cbjs_action': '''
        //alert('IN SAVE PIPELINE 1');
	server = TacticServerStub.get();
        var top = bvr.src_el.getParent(".spt_pipeline_editor_top");
        var wrapper = top.getElement(".spt_pipeline_wrapper");
        spt.pipeline.init_cbk(wrapper);
        var order_code = '%s';
        var order_sk = '%s';
        var user_name = '%s';
        var current_group_name = spt.pipeline.get_current_group();
        var top_el = document.getElementsByClassName('twog_order_builder_' + order_sk)[0];
        var holder = top_el.getElementsByClassName("spt_pipeline_tool_top")[0];
        pipe_xmls = holder.getAttribute('pipe_xmls');
        pxs = pipe_xmls.split('XsX');
        pipes = {};
        pipes['default'] = '';
        pipe_arr = []
        for(var r = 0; r < pxs.length; r++){
            if(r %s 2 == 0){
                pipe_arr.push(pxs[r]);
                pipes[pxs[r]] = pxs[r+1];
            }
        }
        var group_count = 0;
	var groups = spt.pipeline.get_groups();
        for(group_name in groups){
	    group_count = group_count + 1;
	}
        ord = server.eval("@SOBJECT(twog/order['code','" + order_code + "'])")[0];
        classification = ord.classification;
        is_master = false;
         if(classification == 'Master' || classification == 'master'){
             is_master = true;
         }
        if(is_master || pipes[current_group_name] == this_xml || pipe_xmls == ''){ //MTM JUST ADDED PIPE_XMLS
		var st2 = holder.getAttribute('st2');
		var sob_sk = top_el.getAttribute('pipefocus_sob_sk');
		var sob_code = sob_sk.split('code=')[1];
		var class_type = top_el.getAttribute('pipefocus_class_type');
		var client_code = top_el.get('client');
		expr = "@GET(twog/client['code','" + client_code + "'].name)";
		var client = server.eval(expr)[0];
		if (group_count > 2) {
		    var xml = spt.pipeline.export_groups();
		    var class_name = 'order_builder.CustomPipeEditWdg';

		    var kwargs = {
			'st2': st2,
			'order_code': order_code,
			'client_name': client,
			search_type: 'sthpw/pipeline',
			view: 'insert',
			single: true,
			'default': {
			    code: client + '_',
			    pipeline: xml,
                            search_type: st2
			},
			save_event: bvr.save_event
		    }
		    spt.api.load_popup("Add New Pipeline", class_name, kwargs);
		}
		else if (current_group_name == 'default') {
		    var xml = spt.pipeline.export_groups();

		    var class_name = 'order_builder.CustomPipeEditWdg';

		    var kwargs = {
			'st2': st2,
			'order_code': order_code,
			'client_name': client,
			search_type: 'sthpw/pipeline',
			view: 'insert',
			single: true,
			'default': {
			    code: client + '_',
			    pipeline: xml,
                            search_type: st2
			},
			save_event: bvr.save_event
		    }
		    spt.api.load_popup("Add New Pipeline", class_name, kwargs);
		}
		else {
		    var data = spt.pipeline.get_data();
		    var color = data.colors[current_group_name];

		    server = TacticServerStub.get();
		    spt.app_busy.show("Saving project-specific pipeline ["+current_group_name+"]",null);
		    
		    var xml = spt.pipeline.export_groups();
		    var search_key = server.build_search_key("sthpw/pipeline", current_group_name);

		    nodes = spt.pipeline.get_all_nodes();
		    desc_dict = {};
                    if(is_master){
                        desc_dict['is_master'] = 'True';
                    }
		    for (var i=0; i<nodes.length; i++) {
			var name = spt.pipeline.get_node_name(nodes[i]);
			var desc = spt.pipeline.get_node_property(nodes[i], 'description');
			if(desc == 'undefined' || desc == 'NULL' || desc == null){
			    desc = 'No Description';
			}
			desc_dict[name] = spt.pipeline.kill_bad_chars(desc);
		    }

		    try {
			var args = {search_key: search_key, pipeline:xml, color:color, project_code: bvr.project_code, desc_dict: desc_dict};
			//server.execute_cmd('tactic.ui.tools.PipelineSaveCbk', args);
			server.execute_cmd('order_builder.CustomPipelineSaveCbk', args);
			server.update(sob_sk, {'pipe_create_method': ''})
			//server.update(sob_sk, {'trigger_me': 'pipe_update'})
		        server.update(sob_sk, {'pipeline_code': current_group_name});
		    } catch(e) {
			spt.alert(spt.exception.handler(e));
		    }
		    spt.named_events.fire_event('pipeline|save', {});
		    // The following code also exists in the custom edit wdg at bottom, so inserts of pipelines will also be saved onto the object you launched them from
		    var reload_cell = top_el.getElementsByClassName('cell_' + sob_sk)[0];
		    //server.update(sob_sk, {'pipeline_code': current_group_name});
		    spt.api.load_panel(reload_cell, 'order_builder.' + class_type, {sk: sob_sk, parent_sk: reload_cell.getAttribute('parent_sk'), order_sk: reload_cell.getAttribute('order_sk'), parent_sid: reload_cell.getAttribute('parent_sid'), allowed_titles: top_el.getAttribute('allowed_titles'), display_mode: top_el.getAttribute('display_mode'), classification: top_el.getAttribute('classification')});
		} 
                // MTM - THIS MAY NEED TO BE TURNED OFF IF APPENDING...
                proj_transfers = server.eval("@SOBJECT(twog/proj_transfer['login','" + user_name + "'])");
                wo_transfers = server.eval("@SOBJECT(twog/work_order_transfer['login','" + user_name + "'])");
                for(var r = 0; r < proj_transfers.length; r++){
                    server.delete_sobject(proj_transfers[r].__search_key__);
                }
                for(var r = 0; r < wo_transfers.length; r++){
                    server.delete_sobject(wo_transfers[r].__search_key__);
                }
                clone_actions = server.eval("@SOBJECT(twog/action_tracker['login','" + user_name + "']['action','cloning'])");
                for(var r = 0; r < clone_actions.length; r++){
                    server.delete_sobject(clone_actions[r].__search_key__);
                }
		bot = top_el.getElementsByClassName('bot_' + sob_sk)[0];
		bot.style.display = 'table-row'; 
        }else{
            alert('This is not a Master Order, and you have made changes to the pipeline(s). I cannot save this. Please clone the pipeline you wish to change inside a master order, then you can use that pipeline here.');
        }
        spt.app_busy.hide();

        ''' % (my.order_code, my.order_sk, user_name, '%')
        } )
 
        icon = button.get_icon_wdg()    
        # makes it glow
        glow_action = ''' 
        bvr.src_el.setStyles(
        {'outline': 'none', 
        'border-color': '#CF7e1B', 
        'box-shadow': '0 0 8px #CF7e1b'});
        '''

        icon.add_named_listener('pipeline|change', glow_action)

        unglow_action = ''' 
        bvr.src_el.setStyle('box-shadow', '0 0 0 #fff');
        '''

        icon.add_named_listener('pipeline|save', unglow_action)

        #button.set_show_arrow_menu(True)
        menu = Menu(width=200)

        button = ButtonNewWdg(title="Append Pipeline", icon=IconWdg.CONNECT)
        button_row.add(button)

        button.add_behavior( {
        'type': 'click_up',
        'project_code': project_code,
        'save_event': my.save_new_event,
        'cbjs_action': '''
        //alert('IN APPEND PIPELINE 1');
        server = TacticServerStub.get();
        var top = bvr.src_el.getParent(".spt_pipeline_editor_top");
        var wrapper = top.getElement(".spt_pipeline_wrapper");
        spt.pipeline.init_cbk(wrapper);
        var order_code = '%s';
        var order_sk = '%s';
        var user_name = '%s';
        var current_group_name = spt.pipeline.get_current_group();
        var top_el = document.getElementsByClassName('twog_order_builder_' + order_sk)[0];
        var holder = top_el.getElementsByClassName("spt_pipeline_tool_top")[0];
        pipe_xmls = holder.getAttribute('pipe_xmls');
        pxs = pipe_xmls.split('XsX');
        pipes = {};
        pipes['default'] = '';
        pipe_arr = []
        for(var r = 0; r < pxs.length; r++){
            if(r %s 2 == 0){
                pipe_arr.push(pxs[r]);
                pipes[pxs[r]] = pxs[r+1];
            }
        }
        var group_count = 0;
        var groups = spt.pipeline.get_groups();
        for(group_name in groups){
            group_count = group_count + 1;
        }
        ord = server.eval("@SOBJECT(twog/order['code','" + order_code + "'])")[0];
        classification = ord.classification;
        is_master = false;
         if(classification == 'Master' || classification == 'master'){
             is_master = true;
         }
        if(!is_master){
            really = confirm("Are you sure you want to append this pipe to the existing pipe?");
            if(really){
                if(pipes[current_group_name] == this_xml || pipe_xmls == ''){
                    var st2 = holder.getAttribute('st2');
                    var sob_sk = top_el.getAttribute('pipefocus_sob_sk');
                    var sob_code = sob_sk.split('code=')[1];
                    var class_type = top_el.getAttribute('pipefocus_class_type');
                    var client_code = top_el.get('client');
                    expr = "@GET(twog/client['code','" + client_code + "'].name)";
                    var client = server.eval(expr)[0];
                    if (group_count > 2) {
                        var xml = spt.pipeline.export_groups();
                        var class_name = 'order_builder.CustomPipeEditWdg';
    
                        var kwargs = {
                            'st2': st2,
                            'order_code': order_code,
                            'client_name': client,
                            search_type: 'sthpw/pipeline',
                            view: 'insert',
                            single: true,
                            'default': {
                                code: client + '_',
                                pipeline: xml,
                                search_type: st2
                            },
                            save_event: bvr.save_event
                        }
                        spt.api.load_popup("Add New Pipeline", class_name, kwargs);
                    }
                    else if (current_group_name == 'default') {
                        var xml = spt.pipeline.export_groups();
    
                        var class_name = 'order_builder.CustomPipeEditWdg';
    
                        var kwargs = {
                            'st2': st2,
                            'order_code': order_code,
                            'client_name': client,
                            search_type: 'sthpw/pipeline',
                            view: 'insert',
                            single: true,
                            'default': {
                                code: client + '_',
                                pipeline: xml,
                                search_type: st2
                            },
                            save_event: bvr.save_event
                        }
                        spt.api.load_popup("Add New Pipeline", class_name, kwargs);
                    }
                    else {
                        var data = spt.pipeline.get_data();
                        var color = data.colors[current_group_name];
    
                        server = TacticServerStub.get();
                        spt.app_busy.show("Saving project-specific pipeline ["+current_group_name+"]",null);
    	            //THIS NEEDS TO BE ON TO TURN EXISTING PIPE INTO HACKPIPE  (STILL NEEDS TO BE FINISHED)
                        server.execute_cmd('manual_updaters.NormalPipeToHackPipeCmd', {'sob_sk': sob_sk, 'new_pipe': current_group_name});
                        
                        var xml = spt.pipeline.export_groups();
                        var search_key = server.build_search_key("sthpw/pipeline", current_group_name);
    
                        nodes = spt.pipeline.get_all_nodes();
                        desc_dict = {};
                        if(is_master){
                            desc_dict['is_master'] = 'True';
                        }
                        process_names = ''
                        for (var i=0; i<nodes.length; i++) {
                            var name = spt.pipeline.get_node_name(nodes[i]);
                            var desc = spt.pipeline.get_node_property(nodes[i], 'description');
                            if(desc == 'undefined' || desc == 'NULL' || desc == null){
                                desc = 'No Description';
                            }
                            desc_dict[name] = spt.pipeline.kill_bad_chars(desc);
                            if(process_names == ''){
                                process_names = name;
                            }else{
                                process_names = process_names + '|' + name;
                            }
                        }
                        append_connectors = server.eval("@GET(" + st2 + "['code','" + sob_code + "'].append_connectors)")[0];
                        append_connectors2 = append_connectors.split(',');
                        //spt.named_events.fire_event('pipeline|save', {});
                        server.update(sob_sk, {'pipe_create_method': 'append'});
                        server.update(sob_sk, {'pipeline_code': current_group_name});
                        server.update(sob_sk, {'append_connectors': '', 'pipe_create_method': ''});
                        //HERE NEED TO CONNECT LAST PIPE TO NEW PIPE THROUGH HACKPIPE
                        jc_expr = '';
                        if(st2 == 'twog/title'){
                            if(nodes.length > 1){
                                jc_expr = "@SOBJECT(twog/proj['title_code','" + sob_code + "']['process','in','" + process_names + "'])"; 
                            }else{
                                jc_expr = "@SOBJECT(twog/proj['title_code','" + sob_code + "']['process','" + process_names + "'])"; 
                            }
                        }else{
                            if(nodes.length > 1){
                                jc_expr = "@SOBJECT(twog/work_order['proj_code','" + sob_code + "']['process','in','" + process_names + "'])"; 
                            }else{
                                jc_expr = "@SOBJECT(twog/work_order['proj_code','" + sob_code + "']['process','" + process_names + "'])"; 
                            }
                        }
                        just_created = [];
                        while(just_created.length < nodes.length){
                            just_created = server.eval(jc_expr); 
                        }
                        for(var q = 0; q < append_connectors2.length; q++){
                            for(var t = 0; t < just_created.length; t++){
                                if(just_created[t].creation_type != 'hackup'){
                                    server.insert('twog/hackpipe_out', {'lookup_code': append_connectors2[q], 'out_to': just_created[t].code});
                                }
                            }
                        }
                        //HERE NEED TO RE-ESTABLISH THE "ORDER_IN_PIPE" for all items - old and new - in the pipe -- DONE by inserting new "twog/simplify_pipe"
                        if(sob_sk.indexOf('TITLE') != -1){
                            server.insert('twog/simplify_pipe', {'title_code': sob_code, 'do_all': 'yes'});
                        }else{
                            server.insert('twog/simplify_pipe', {'proj_code': sob_code, 'do_all': 'yes'});
                        }
                        // The following code also exists in the custom edit wdg at bottom, so inserts of pipelines will also be saved onto the object you launched them from
                        var reload_cell = top_el.getElementsByClassName('cell_' + sob_sk)[0];
                        spt.api.load_panel(reload_cell, 'order_builder.' + class_type, {sk: sob_sk, parent_sk: reload_cell.getAttribute('parent_sk'), order_sk: reload_cell.getAttribute('order_sk'), parent_sid: reload_cell.getAttribute('parent_sid'), allowed_titles: top_el.getAttribute('allowed_titles'), display_mode: top_el.getAttribute('display_mode'), classification: top_el.getAttribute('classification')});
                    } 
                    // MTM - THIS MAY NEED TO BE TURNED OFF IF APPENDING...
                    proj_transfers = server.eval("@SOBJECT(twog/proj_transfer['login','" + user_name + "'])");
                    wo_transfers = server.eval("@SOBJECT(twog/work_order_transfer['login','" + user_name + "'])");
                    for(var r = 0; r < proj_transfers.length; r++){
                        server.delete_sobject(proj_transfers[r].__search_key__);
                    }
                    for(var r = 0; r < wo_transfers.length; r++){
                        server.delete_sobject(wo_transfers[r].__search_key__);
                    }
                    clone_actions = server.eval("@SOBJECT(twog/action_tracker['login','" + user_name + "']['action','cloning'])");
                    for(var r = 0; r < clone_actions.length; r++){
                        server.delete_sobject(clone_actions[r].__search_key__);
                    }
                    bot = top_el.getElementsByClassName('bot_' + sob_sk)[0];
                    bot.style.display = 'table-row'; 
                }
            }
        }else{
            alert("Nuh Uh. Can't append within a Master Order.");
        }
        spt.app_busy.hide();

        ''' % (my.order_code, my.order_sk, user_name, '%')
        } )
        

        menu_item = MenuItem(type='action', label='No Changes Made - Assign Pipeline to Selected Object')
        menu.add(menu_item)
        # no project code here
        menu_item.add_behavior( {
            'cbjs_action': '''
        //alert('in NO CHANGES MADE -- not dealing with transfers');
        var order_sk = '%s';
        var act = spt.smenu.get_activator(bvr);
        var top = act.getParent(".spt_pipeline_editor_top");
        var wrapper = top.getElement(".spt_pipeline_wrapper");
        spt.pipeline.init_cbk(wrapper);
        var group_name = spt.pipeline.get_current_group();
        if(group_name != 'default'){
            //var top_el = spt.api.get_parent(bvr.src_el, '.twog_order_builder');
            //var top_el = spt.api.get_parent(bvr.src_el, '.twog_order_builder_' + order_sk);
            var top_el = document.getElementsByClassName('twog_order_builder_' + order_sk)[0];
            var sob_sk = top_el.getAttribute('pipefocus_sob_sk');
            var sob_name = top_el.getAttribute('pipefocus_name');
            var sob_code = sob_sk.split('code=')[1];
            var sob_st = sob_sk.split('?')[0];
            spt.app_busy.show('Attaching Pipeline to ' + sob_code + '...');
            server = TacticServerStub.get();
            if(confirm('Assign "' + group_name + '" to ' + sob_code + '?')){
		    var sob = server.eval("@SOBJECT(" + sob_st + "['code','" + sob_code + "'])")[0]; 
		    var class_type = top_el.getAttribute('pipefocus_class_type');
		    if(group_name == sob.pipeline_code){
			server.update(sob_sk, {'trigger_me': 'pipe_update'})
		    }else{
			server.update(sob_sk, {'pipeline_code': group_name});
		    }
		    var reload_cell = top_el.getElementsByClassName('cell_' + sob_sk)[0];
		    spt.api.load_panel(reload_cell, 'order_builder.' + class_type, {sk: sob_sk, parent_sk: reload_cell.getAttribute('parent_sk'), order_sk: reload_cell.getAttribute('order_sk'), parent_sid: reload_cell.getAttribute('parent_sid'), allowed_titles: top_el.getAttribute('allowed_titles'), display_mode: top_el.getAttribute('display_mode'), classification: top_el.getAttribute('classification')});
		    bot = top_el.getElementsByClassName('bot_' + sob_sk)[0];
		    bot.style.display = 'table-row'; 
            }
            spt.app_busy.hide();
            alert('LEAVING NO CHANGES MADE');
        }else{
            alert('You have not made an original save of the current pipeline. Try "Save as New Pipeline" to save pipeline and assign to object. Aborting Assignment...');
        }
        ''' % my.order_sk
        } )


        menus = [menu.get_data()]
        SmartMenu.add_smart_menu_set( button.get_arrow_wdg(), { 'DG_BUTTON_CTX': menus } )
        SmartMenu.assign_as_local_activator( button.get_arrow_wdg(), "DG_BUTTON_CTX", True )
 

        button = ButtonNewWdg(title="Save As New Pipeline", icon=IconWdg.INSERT)
        button_row.add(button)

        button.add_behavior( {
        'type': 'click_up',
        'project_code': project_code,
        'save_event': my.save_new_event,
        'cbjs_action': '''
        //alert('IN SAVE AS NEW');
        server = TacticServerStub.get();
        var top = bvr.src_el.getParent(".spt_pipeline_editor_top");
        var wrapper = top.getElement(".spt_pipeline_wrapper");
        spt.pipeline.init_cbk(wrapper);
        var order_code = '%s';
        var order_sk = '%s';
        var user_name = '%s';
        var current_group_name = spt.pipeline.get_current_group();
        var top_el = document.getElementsByClassName('twog_order_builder_' + order_sk)[0];
        var classification = top_el.getAttribute('classification');
        var holder = top_el.getElementsByClassName("spt_pipeline_tool_top")[0];
        var st2 = holder.getAttribute('st2');
        var sob_sk = top_el.getAttribute('pipefocus_sob_sk');
        var sob_code = sob_sk.split('code=')[1];
        var class_type = top_el.getAttribute('pipefocus_class_type');
        var client_code = top_el.get('client');
        expr = "@GET(twog/client['code','" + client_code + "'].name)";
        var client = server.eval(expr)[0];
        var group_count = 0;
        var groups = spt.pipeline.get_groups();
        var is_master = false;
        if(classification == 'master' || classification == 'Master'){
            is_master = true;
        }
        for(group_name in groups){
            group_count = group_count + 1;
        }
        if (true) {
            var xml = spt.pipeline.export_groups();
            //alert(xml);

            var class_name = 'order_builder.CustomPipeEditWdg';

            var kwargs = {
                'st2': st2,
                'order_code': order_code,
                'client_name': client,
                search_type: 'sthpw/pipeline',
                view: 'insert',
                single: true,
                'default': {
                    code: client + '_',
                    pipeline: xml,
                    search_type: st2
                },
                save_event: bvr.save_event
            }
            spt.api.load_popup("Add New Pipeline", class_name, kwargs);
        }
        else if (current_group_name == 'default') {
            var xml = spt.pipeline.export_groups();
           // alert(xml);

            var class_name = 'order_builder.CustomPipeEditWdg';

            var kwargs = {
                'st2': st2,
                'order_code': order_code,
                'client_name': client,
                search_type: 'sthpw/pipeline',
                view: 'insert',
                single: true,
                'default': {
                    code: client + '_',
                    pipeline: xml,
                    search_type: st2
                },
                save_event: bvr.save_event
            }
            spt.api.load_popup("Add New Pipeline", class_name, kwargs);
        }
        else {
            var data = spt.pipeline.get_data();
            var color = data.colors[current_group_name];

            server = TacticServerStub.get();
            spt.app_busy.show("Saving project-specific pipeline ["+current_group_name+"]",null);
            
            //var xml = spt.pipeline.export_group(current_group_name); // did changing from this to the next line really fix the problem?
            var xml = spt.pipeline.export_groups();
           // alert(xml);
            var search_key = server.build_search_key("sthpw/pipeline", current_group_name);

            nodes = spt.pipeline.get_all_nodes();
            desc_dict = {};
            if(is_master){
                desc_dict['is_master'] = 'True';
            }
            for (var i=0; i<nodes.length; i++) {
               // alert('Node ' + i);
                var name = spt.pipeline.get_node_name(nodes[i]);
                var desc = spt.pipeline.get_node_property(nodes[i], 'description');
                if(desc == 'undefined' || desc == 'NULL' || desc == null){
                    desc = 'No Description';
                    //new_desc = prompt('Please enter the Description for ' + name);
                    //if(new_desc != ''){
                    //    desc = new_desc;
                    //}
                }
                desc_dict[name] = spt.pipeline.kill_bad_chars(desc);
            }

            try {
               // alert('before try 1');
                var args = {search_key: search_key, pipeline:xml, color:color, project_code: bvr.project_code, desc_dict: desc_dict};
                //server.execute_cmd('tactic.ui.tools.PipelineSaveCbk', args);
                server.execute_cmd('order_builder.CustomPipelineSaveCbk', args);
               // alert('after try 1');
               // alert('before try 2');
                server.update(sob_sk, {'trigger_me': 'pipe_update'})
               // alert('after try 2');
            } catch(e) {
                spt.alert(spt.exception.handler(e));
            }
            spt.named_events.fire_event('pipeline|save', {});
            // The following code also exists in the custom edit wdg at bottom, so inserts of pipelines will also be saved onto the object you launched them from
            var reload_cell = top_el.getElementsByClassName('cell_' + sob_sk)[0];
           // alert('before try 3');
            server.update(sob_sk, {'pipeline_code': current_group_name});
           // alert('after try 3');
            spt.api.load_panel(reload_cell, 'order_builder.' + class_type, {sk: sob_sk, parent_sk: reload_cell.getAttribute('parent_sk'), order_sk: reload_cell.getAttribute('order_sk'), parent_sid: reload_cell.getAttribute('parent_sid'), allowed_titles: top_el.getAttribute('allowed_titles'), display_mode: top_el.getAttribute('display_mode'), classification: top_el.getAttribute('classification')});
        } 
        bot = top_el.getElementsByClassName('bot_' + sob_sk)[0];
        bot.style.display = 'table-row'; 
        // MTM - THIS MAY NEED TO BE TURNED OFF IF APPENDING...
        proj_transfers = server.eval("@SOBJECT(twog/proj_transfer['login','" + user_name + "'])");
        wo_transfers = server.eval("@SOBJECT(twog/work_order_transfer['login','" + user_name + "'])");
        for(var r = 0; r < proj_transfers.length; r++){
            server.delete_sobject(proj_transfers[r].__search_key__);
        }
        for(var r = 0; r < wo_transfers.length; r++){
            server.delete_sobject(wo_transfers[r].__search_key__);
        }
        clone_actions = server.eval("@SOBJECT(twog/action_tracker['login','" + user_name + "']['action','cloning'])");
        for(var r = 0; r < clone_actions.length; r++){
            server.delete_sobject(clone_actions[r].__search_key__);
        }

        spt.app_busy.hide();
        //alert('LEAVING SAVE AS NEW');

        ''' % (my.order_code, my.order_sk, user_name)
        } )

        button = ButtonNewWdg(title="Clone Pipeline", icon=IconWdg.STAR)
        button_row.add(button)
        button.add_behavior( {
        'type': 'click_up',
        'project_code': project_code,
        'save_event': my.save_new_event,
        'cbjs_action': '''
        //alert('IN CLONE');
        function oc(a){
            var o = {};
            for(var i=0;i<a.length;i++){
                o[a[i]]='';
            }
            return o;
        }
        function kill_nulls(dict){
            keys = Object.keys(dict);
            for(var r = 0; r < keys.length; r++){
                if(dict[keys[r]] == null){
                    dict[keys[r]] = '';
                }
            }
            return dict;
        }
        server = TacticServerStub.get();
        var top = bvr.src_el.getParent(".spt_pipeline_editor_top");
        var wrapper = top.getElement(".spt_pipeline_wrapper");
        spt.pipeline.init_cbk(wrapper);
        var order_code = '%s';
        var order_sk = '%s';
        var user_name = '%s';
        proj_transfers = server.eval("@SOBJECT(twog/proj_transfer['login','" + user_name + "'])");
        wo_transfers = server.eval("@SOBJECT(twog/work_order_transfer['login','" + user_name + "'])");
        for(var r = 0; r < proj_transfers.length; r++){
            server.delete_sobject(proj_transfers[r].__search_key__);
        }
        for(var r = 0; r < wo_transfers.length; r++){
            server.delete_sobject(wo_transfers[r].__search_key__);
        }
        clone_actions = server.eval("@SOBJECT(twog/action_tracker['login','" + user_name + "']['action','cloning'])");
        for(var r = 0; r < clone_actions.length; r++){
            server.delete_sobject(clone_actions[r].__search_key__);
        }
        var current_group_name = spt.pipeline.get_current_group();
        var top_el = document.getElementsByClassName('twog_order_builder_' + order_sk)[0];
        var holder = top_el.getElementsByClassName("spt_pipeline_tool_top")[0];
        var st2 = holder.getAttribute('st2');
        //alert('st2 = ' + st2);
        var sob_sk = top_el.getAttribute('pipefocus_sob_sk');
        var sob_code = sob_sk.split('code=')[1];
        var class_type = top_el.getAttribute('pipefocus_class_type');
        var client_code = top_el.get('client');
        expr = "@GET(twog/client['code','" + client_code + "'].name)";
        var client = server.eval(expr)[0];
        var group_count = 0;
        var groups = spt.pipeline.get_groups();
        for(group_name in groups){
            group_count = group_count + 1;
        }
        ord = server.eval("@SOBJECT(twog/order['code','" + order_code + "'])")[0];
        classification = ord.classification;
        is_master = false;
        if(classification == 'master' || classification == 'Master'){
            is_master = true;
        }
        if (is_master && group_count < 2 && current_group_name != 'default') {
            var action = server.insert('twog/action_tracker', {'login': user_name, 'action': 'cloning'});
            pipe = server.eval("@SOBJECT(sthpw/pipeline['code','" + current_group_name + "'])")[0];
            //Assign new name to title pipeline
            name_prompt = prompt('Please give the pipeline a new name. Current name is: ' + current_group_name);
            if(name_prompt != '' && name_prompt != null){
                if(name_prompt != current_group_name){
                    pipeline_data = {'code': name_prompt, 'pipeline': pipe.pipeline, 'search_type': pipe.search_type, 'project_code': pipe.project_code, 'description': pipe.description, 'color': pipe.color}; 
                    pipeline_data = kill_nulls(pipeline_data);
                    server.insert('sthpw/pipeline', pipeline_data); 
                    if(pipe.search_type == 'twog/title'){
                       //Attach pipeline_prereqs for future titles
                        old_pres_expr = "@SOBJECT(twog/pipeline_prereq['pipeline_code','" + current_group_name + "'])";
                        old_pres = server.eval(old_pres_expr);
                        for(var q = 0; q < old_pres.length; q++){
                            pipe_prereq_data = {'pipeline_code': name_prompt, 'prereq': old_pres[q].prereq};
                            pipe_prereq_data = kill_nulls(pipe_prereq_data);
                            server.insert('twog/pipeline_prereq', pipe_prereq_data);
                        }
                    }
                    //alert('inserted...now looking for old processes');
                    old_expr = "@SOBJECT(config/process['pipeline_code','" + current_group_name + "'])";
                    //alert(old_expr);
                    old_processes = server.eval(old_expr);
                    //alert('len old_p = ' + old_processes.length);
                    for(var w = 0; w < old_processes.length; w++){
                        op = old_processes[w];
                        //alert('op process = ' + op.process);
                        conf_pro_data = {'pipeline_code': name_prompt, 'process': op.process, 'color': op.color, 'sort_order': op.sort_order, 'context_options': op.context_options, 'subcontext_options': op.subcontext_options, 'checkin_mode': op.checkin_mode, 'checkin_validate_script_path': op.checkin_validate_script_path, 'sandbox_create_script_path': op.sandbox_create_script_path, 'checkin_options_view': op.checkin_options_view, 'description': op.description, 'repo_type': op.repo_type};
                        conf_pro_data = kill_nulls(conf_pro_data);
                        //insert spt_processes with the new pipeline code
                        server.insert('config/process', conf_pro_data);
                    }
                    //alert(pipe.search_type);
                    do_work_orders = false;
                    if(pipe.search_type == 'twog/title'){
                        old_proj_templs = server.eval("@SOBJECT(twog/proj_templ['parent_pipe','" + current_group_name + "'])"); 
                        new_proj_templs = server.eval("@SOBJECT(twog/proj_templ['parent_pipe','" + name_prompt + "'])"); 
                        //alert('old len = ' + old_proj_templs.length + ' npt len = ' + new_proj_templs.length);
                        for(var t = 0; t < old_proj_templs.length; t++){
                            opt = old_proj_templs[t];
                            for(var y = 0; y < new_proj_templs.length; y++){
                                npt = new_proj_templs[y];
                                if(npt.process == opt.process){
                                    //alert('doing an update');
                                    npt_data =  {'description': opt.description, 'pipeline_code': opt.pipeline_code, 'keywords': opt.keywords, 'is_billable': opt.is_billable, 'specs': opt.specs, 'rate_card_price': opt.rate_card_price, 'flat_pricing': opt.flat_pricing, 'client_code': opt.client_code, 'projected_overhead_pct': opt.projected_overhead_pct, 'projected_markup_pct': opt.projected_markup_pct, 'wiki_page': opt.wiki_page};
                                    npt_data = kill_nulls(npt_data);
                                    server.update(npt.__search_key__, npt_data);
                                    do_work_orders = true;
                                }
                            }
                        }
                    }else{
                        do_work_orders = true;
                    }
                    //alert('do work orders? ' + do_work_orders);
		    nodes = spt.pipeline.get_all_nodes();
                    ok_proj_names = ''
                    for(var tg = 0; tg < nodes.length; tg++){
                        var p_name = spt.pipeline.get_node_name(nodes[tg]);
                        if(ok_proj_names == ''){
                            ok_proj_names = p_name;
                        }else{
                            ok_proj_names = ok_proj_names + '|' + p_name;
                        }
                    }
                    if(do_work_orders){
                        if(st2 == 'twog/title'){
                                opt_expr = "@SOBJECT(twog/proj_templ['parent_pipe','" + current_group_name + "']['process','in','" + ok_proj_names + "'])"; 
                                //alert(opt_expr);
				old_proj_templs = server.eval(opt_expr); 
				//alert("old_proj_templs len = " + old_proj_templs.length);
                                npt_expr = "@SOBJECT(twog/proj_templ['parent_pipe','" + name_prompt + "'])"; 
                                //alert(npt_expr);
				new_proj_templs = server.eval(npt_expr); 
				//alert("new_proj_templs len = " + new_proj_templs.length);
				seen_opts = [];
				for(var p = 0; p < old_proj_templs.length; p++){
					opt = old_proj_templs[p];
					//alert('seen_opts = ' + seen_opts);
					if(!(opt.process in oc(seen_opts))){
					    seen_opts.push(opt.process); 
					    //alert('opt = ' + opt);
					    apc_expr = "@GET(twog/client_pipes['pipeline_code','" + current_group_name + "']['process_name','" + opt.process + "'].pipe_to_assign)";
					    //alert('APC EXPR = ' + apc_expr);
					    assign_pipe_code = server.eval(apc_expr);
					    //alert('assign_pipe_code = ' + assign_pipe_code);
					    if(assign_pipe_code != '' && assign_pipe_code != null){
						assign_pipe_code = assign_pipe_code[0];                       
						assign_pipe_expr = "@SOBJECT(sthpw/pipeline['code','" + assign_pipe_code + "'])";
						assign_pipe = server.eval(assign_pipe_expr)[0];
						//alert('2 ' + assign_pipe_code);
						pipe_created = false;
						proj_name_prompt = '';
                                                fail_reason = ''
						while(!pipe_created){
						    proj_name_prompt = prompt('Please give this project pipeline a new name. Current name is: ' + assign_pipe.code);
                                                    exist_already = server.eval("@SOBJECT(sthpw/pipeline['code','" + proj_name_prompt + "'])");
                                                    failer = false;
                                                    if(proj_name_prompt == assign_pipe.code){
                                                        failer = true;
                                                        fail_reason = 'This pipeline code (' + proj_name_prompt + ') is the same as the one you are cloning. Please choose a different name.';
                                                    }
                                                    if(exist_already.length > 0){
                                                        failer = true;
                                                        fail_reason = 'This pipeline code (' + proj_name_prompt + ') is already being used.';
                                                    }
						    if(proj_name_prompt != '' && proj_name_prompt != null && failer == false){
							pipe2_data = {'code': proj_name_prompt, 'pipeline': assign_pipe.pipeline, 'search_type': assign_pipe.search_type, 'project_code': assign_pipe.project_code, 'description': assign_pipe.description, 'color': assign_pipe.color};
							pipe2_data = kill_nulls(pipe2_data);
							server.insert('sthpw/pipeline', pipe2_data);
							client_pipes_data = {'pipeline_code': name_prompt, 'process_name': opt.process, 'pipe_to_assign': proj_name_prompt};
							client_pipes_data = kill_nulls(client_pipes_data);
							server.insert('twog/client_pipes', client_pipes_data);
							old_expr = "@SOBJECT(config/process['pipeline_code','" + assign_pipe.code + "'])";
							old_prcs = server.eval(old_expr);
							for(var w = 0; w < old_prcs.length; w++){
							    op = old_prcs[w];
							    //alert('op process = ' + op.process);
							    conf_pro_data2 = {'pipeline_code': proj_name_prompt, 'process': op.process, 'color': op.color, 'sort_order': op.sort_order, 'context_options': op.context_options, 'subcontext_options': op.subcontext_options, 'checkin_mode': op.checkin_mode, 'checkin_validate_script_path': op.checkin_validate_script_path, 'sandbox_create_script_path': op.sandbox_create_script_path, 'checkin_options_view': op.checkin_options_view, 'description': op.description, 'repo_type': op.repo_type};
							    conf_pro_data2 = kill_nulls(conf_pro_data2);
							    server.insert('config/process', conf_pro_data2);
							}
							pipe_created = true;
							for(var z = 0; z < new_proj_templs.length; z++){
							    if(new_proj_templs[z].process == old_proj_templs[p].process){
								server.update(new_proj_templs[z].__search_key__, {'pipeline_code': proj_name_prompt})
							    }
							}
						    }else{
							alert("Hmm. Yeah. That won't work. " + fail_reason);
                                                        fail_reason = '';
						    } 
						}
						look_pipe = opt.pipeline_code;
						if(look_pipe == 'twog/proj_templ'){
						    look_pipe = "Dont find anything ok"
						}
						old_wots_expr = "@SOBJECT(twog/work_order_templ['parent_pipe','" + look_pipe + "'])";
						//alert('**** old wots expr ****' + old_wots_expr);
						old_wots = server.eval(old_wots_expr);
						//alert('old_wots len = ' + old_wots.length); 
						deliv_trade = {};
						deliv_seen = [];
						inter_trade = {};
						inter_seen = []
						//alert('doing next part');
						new_proj_templs = server.eval("@SOBJECT(twog/proj_templ['parent_pipe','" + name_prompt + "'])"); 
						for(var k = 0; k < new_proj_templs.length; k++){
						    npt = new_proj_templs[k];
						    Okeys = Object.keys(npt);
						    for(var lk = 0; lk < Okeys.length; lk++){
							//alert('*** new_proj_templs instance. Field = "' + Okeys[lk] + '", Value = "' + npt[Okeys[lk]] + ' ***'); 
						    }
						    look_pipe2 = npt.pipeline_code;
						    if(look_pipe2 == 'twog/proj_templ'){
							look_pipe2 = "Dont find anything ok"
						    }
						    new_wots_expr = "@SOBJECT(twog/work_order_templ['parent_pipe','" + look_pipe2 + "'])";
						    //alert('**** New wots expr **** = ' + new_wots_expr);
						    new_wots = server.eval(new_wots_expr);
						    //alert('*** new_wots len *** = ' + new_wots.length);
						    //alert('NPT.PROCESS = ' + npt.process + ' OPT.PROCESS = ' + opt.process);
						    if(npt.process == opt.process){
							//alert('2 THEY ARE EQUAL')
							for(var h = 0; h < old_wots.length; h++){
							    ow = old_wots[h];
							    //alert('**** 2.5 ow.code **** = ' + ow.code);
							    for(var f = 0; f < new_wots.length; f++){
								nw = new_wots[f];
								//alert('3 ow.process = ' + ow.process + ' nw.process = ' + nw.process);
								if(ow.process == nw.process){
								    //alert('3 They Are Equal');
								    // need to do the intermediates and deliverables here, build up their new comma separated code strings and then include them in the update
								    new_inter_codes = '';
								    new_deliv_codes = '';
								    old_deliv_codes = ow.deliverable_templ_codes.split(',');
								    odtc = ow.deliverable_templ_codes;
								    //alert('old deliv codes = ' + old_deliv_codes);
								    if(odtc != '' && odtc != null){
									    for(var v = 0; v < old_deliv_codes.length; v++){
										odc = old_deliv_codes[v]; 
										//alert('ODC = ' + odc);
										deliverable_templ_expr = "@SOBJECT(twog/deliverable_templ['code','" + odc + "'])";
										//alert('deliverable_templ expr = ' + deliverable_templ_expr);
										old_deliv_t = server.eval(deliverable_templ_expr);
										//alert('old_deliv_t length = ' + old_deliv_t.length);
										if(old_deliv_t.length > 0){
											old_deliv_t = old_deliv_t[0];
											//alert('inserting new deliverable_templ');
											//alert(Object.keys(old_deliv_t));
											d_templ_data = {'description': old_deliv_t.description, 'keywords': old_deliv_t.keywords, 'name': old_deliv_t.name, 'aspect_ratio': old_deliv_t.aspect_ratio, 'color_space': old_deliv_t.color_space, 'file_type': old_deliv_t.file_type, 'standard': old_deliv_t.standard, 'total_run_time': old_deliv_t.total_run_time, 'source_type': old_deliv_t.source_type, 'subtitles': old_deliv_t.subtitles, 'captioning': old_deliv_t.captioning, 'textless': old_deliv_t.textless, 'generation': old_deliv_t.generation, 'audio_ch_1': old_deliv_t.audio_ch_1, 'audio_ch_2': old_deliv_t.audio_ch_2, 'audio_ch_3': old_deliv_t.audio_ch_3, 'audio_ch_4': old_deliv_t.audio_ch_4, 'audio_ch_5': old_deliv_t.audio_ch_5, 'audio_ch_6': old_deliv_t.audio_ch_6, 'audio_ch_7': old_deliv_t.audio_ch_7, 'audio_ch_8': old_deliv_t.audio_ch_8, 'audio_ch_9': old_deliv_t.audio_ch_9, 'audio_ch_10': old_deliv_t.audio_ch_10, 'audio_ch_11': old_deliv_t.audio_ch_11, 'audio_ch_12': old_deliv_t.audio_ch_12, 'audio_ch_13': old_deliv_t.audio_ch_13, 'audio_ch_14': old_deliv_t.audio_ch_14, 'audio_ch_15': old_deliv_t.audio_ch_15, 'audio_ch_16': old_deliv_t.audio_ch_16, 'audio_ch_17': old_deliv_t.audio_ch_17, 'audio_ch_18': old_deliv_t.audio_ch_18, 'audio_ch_19': old_deliv_t.audio_ch_19, 'audio_ch_20': old_deliv_t.audio_ch_20, 'audio_ch_21': old_deliv_t.audio_ch_21, 'audio_ch_22': old_deliv_t.audio_ch_22, 'audio_ch_23': old_deliv_t.audio_ch_23, 'audio_ch_24': old_deliv_t.audio_ch_24, 'format': old_deliv_t.format, 'frame_rate': old_deliv_t.frame_rate, 'work_order_templ_code': nw.code, 'title': old_deliv_t.title, 'attn': old_deliv_t.attn, 'deliver_to': old_deliv_t.deliver_to};
											//alert('going into kill nulls');
											d_templ_data = kill_nulls(d_templ_data);
											//alert('back from kill_nulls');
											d_keys = Object.keys(d_templ_data);
											new_deliv = server.insert('twog/deliverable_templ', d_templ_data)
											//alert('Inserted d_templ');
											if(new_deliv_codes == ''){
											    new_deliv_codes = new_deliv.code;
											}else{
											    new_deliv_codes = new_deliv_codes + ',' + new_deliv.code;
											}
											deliv_trade[old_deliv_t.code] = new_deliv.code
											deliv_seen.push(old_deliv_t.code);
										}
									    }
								    }
								    old_inter_codes = ow.intermediate_file_templ_codes.split(',');
								    //alert('old_inter_codes = ' + old_inter_codes);
								    oiftc = ow.intermediate_file_templ_codes;
								    if(oiftc != '' && oiftc != null){
									    for(var v = 0; v < old_inter_codes.length; v++){
										oic = old_inter_codes[v];
										old_inter_t = server.eval("@SOBJECT(twog/intermediate_file_templ['code','" + oic + "'])");
										if(old_inter_t.length > 0){
											old_inter_t = old_inter_t[0];
											//alert('inserting intermediate_file_templ');
											inter_templ_data = {'description': old_inter_t.description, 'keywords': old_inter_t.keywords, 'title': old_inter_t.title}; 
											inter_templ_data = kill_nulls(inter_templ_data);
											new_inter = server.insert('twog/intermediate_file_templ', inter_templ_data) 
											if(new_inter_codes == ''){
											    new_inter_codes = new_inter.code;
											}else{
											    new_inter_codes = new_inter_codes + ',' + new_inter.code;
											}
											inter_trade[old_inter_t.code] = new_inter.code
											inter_seen.push(old_inter_t.code);
										}
									    }  
								    }
								    nw_data = {'description': ow.description, 'keywords': ow.keywords, 'process': ow.process, 'instructions': ow.instructions, 'proj_templ_code': npt.code, 'parent_pipe': proj_name_prompt, 'wiki_page': ow.wiki_page, 'work_group': ow.work_group, 'estimated_work_hours': ow.estimated_work_hours, 'deliverable_templ_codes': new_deliv_codes, 'intermediate_file_templ_codes': new_inter_codes};
								    //alert('nw data = ' + nw_data);
								    nw_data = kill_nulls(nw_data);
								    //alert('nw.code = ' + nw.code);
								    server.update(nw.__search_key__, nw_data);
								    //now do equipment_used_templs, wo_passin_templs and wo_prereq_templs
								    eq_templs = server.eval("@SOBJECT(twog/equipment_used_templ['work_order_templ_code','" + ow.code + "'])");
								    for(var v = 0; v < eq_templs.length; v++){
									eq = eq_templs[v];
									//alert('inserting equipment_used_templ');
									eq_used_templ_data = {'description': eq.description, 'keywords': eq.keywords, 'name': eq.name, 'units': eq.units, 'equipment_code': eq.equipment_code, 'expected_duration': eq.expected_duration, 'expected_quantity': eq.expected_quantity, 'expected_cost': eq.expected_cost, 'work_order_templ_code': nw.code};
									eq_used_templ_data = kill_nulls(eq_used_templ_data);
									server.insert('twog/equipment_used_templ', eq_used_templ_data);
								    } 
								    wopts = server.eval("@SOBJECT(twog/work_order_passin_templ['work_order_templ_code','" + ow.code + "'])");
								    for(var v = 0; v < wopts.length; v++){
									wopt = wopts[v];
									inter_code = '';
									deliv_code = '';
									if(wopt.intermediate_file_templ_code in oc(inter_seen)){
									    inter_code = inter_trade[wopt.intermediate_file_templ_code];
									}
									if(wopt.deliverable_templ_code in oc(deliv_seen)){
									    deliv_code = deliv_trade[wopt.deliverable_templ_code]; 
									}
									//alert('inserting work_order_passin_templ');
									wopt_data = {'keywords': wopt.keywords, 'work_order_templ_code': nw.code, 'intermediate_file_templ_code': inter_code, 'deliverable_templ_code': deliv_code};
									wopt_data = kill_nulls(wopt_data);
									server.insert('twog/work_order_passin_templ', wopt_data)
								    }
								    wpres = server.eval("@SOBJECT(twog/work_order_prereq_templ['work_order_templ_code','" + ow.code + "'])");
								    for(var v = 0; v < wpres.length; v++){
									wpre = wpres[v];
									//alert('inserting work_order_prereq_templ');
									wopret_data = {'description': wpre.description, 'keywords': wpre.keywords, 'prereq': wpre.prereq, 'work_order_templ_code': nw.code}; 
									wopret_data = kill_nulls(wopret_data);
									server.insert('twog/work_order_prereq_templ', wopret_data); 
								    }
								    //alert('4 The End..going back to top');
								}
								//alert('End 2');
							    } 
							    //alert('End 3');
							}  
						       //alert('End 4');
						    }
						    //alert('End 5');
						}
					       //alert('End 6');
					    }
					   //alert('End 7');
					}
				      //alert('End 8');
				}
			       //alert('End 9');
			    
				}else if(st2 == 'twog/proj'){
                                    look_pipe = current_group_name;
                                    old_wots_expr = "@SOBJECT(twog/work_order_templ['parent_pipe','" + look_pipe + "'])";
                                    //alert('**** old wots expr ****' + old_wots_expr);
                                    old_wots = server.eval(old_wots_expr);
                                    //alert('old_wots len = ' + old_wots.length); 
                                    deliv_trade = {};
                                    deliv_seen = [];
                                    inter_trade = {};
                                    inter_seen = []
                                    //alert('doing next part');
                                    new_proj_templs = server.eval("@SOBJECT(twog/proj_templ['parent_pipe','" + name_prompt + "'])"); 
                                    look_pipe2 = name_prompt;
                                    new_wots_expr = "@SOBJECT(twog/work_order_templ['parent_pipe','" + look_pipe2 + "'])";
                                    //alert('**** New wots expr **** = ' + new_wots_expr);
                                    new_wots = server.eval(new_wots_expr);
                                    //alert('*** new_wots len *** = ' + new_wots.length);
                                    //alert('NPT.PROCESS = ' + npt.process + ' OPT.PROCESS = ' + opt.process);
                                    //alert('2 THEY ARE EQUAL')
                                    for(var h = 0; h < old_wots.length; h++){
                                        ow = old_wots[h];
                                        //alert('**** 2.5 ow.code **** = ' + ow.code);
                                        for(var f = 0; f < new_wots.length; f++){
                                            nw = new_wots[f];
                                            //alert('3 ow.process = ' + ow.process + ' nw.process = ' + nw.process);
                                            if(ow.process == nw.process){
                                                //alert('3 They Are Equal');
                                                // need to do the intermediates and deliverables here, build up their new comma separated code strings and then include them in the update
                                                new_inter_codes = '';
                                                new_deliv_codes = '';
                                                old_deliv_codes = ow.deliverable_templ_codes.split(',');
                                                odtc = ow.deliverable_templ_codes;
                                                //alert('old deliv codes = ' + old_deliv_codes);
                                                if(odtc != '' && odtc != null){
                                                    for(var v = 0; v < old_deliv_codes.length; v++){
                                                        odc = old_deliv_codes[v]; 
                                                        //alert('ODC = ' + odc);
                                                        deliverable_templ_expr = "@SOBJECT(twog/deliverable_templ['code','" + odc + "'])";
                                                        //alert('deliverable_templ expr = ' + deliverable_templ_expr);
                                                        old_deliv_t = server.eval(deliverable_templ_expr);
                                                        //alert('old_deliv_t length = ' + old_deliv_t.length);
                                                        if(old_deliv_t.length > 0){
                                                            old_deliv_t = old_deliv_t[0];
                                                            //alert('inserting new deliverable_templ');
                                                            //alert(Object.keys(old_deliv_t));
                                                            d_templ_data = {'description': old_deliv_t.description, 'keywords': old_deliv_t.keywords, 'name': old_deliv_t.name, 'aspect_ratio': old_deliv_t.aspect_ratio, 'color_space': old_deliv_t.color_space, 'file_type': old_deliv_t.file_type, 'standard': old_deliv_t.standard, 'total_run_time': old_deliv_t.total_run_time, 'source_type': old_deliv_t.source_type, 'subtitles': old_deliv_t.subtitles, 'captioning': old_deliv_t.captioning, 'textless': old_deliv_t.textless, 'generation': old_deliv_t.generation, 'audio_ch_1': old_deliv_t.audio_ch_1, 'audio_ch_2': old_deliv_t.audio_ch_2, 'audio_ch_3': old_deliv_t.audio_ch_3, 'audio_ch_4': old_deliv_t.audio_ch_4, 'audio_ch_5': old_deliv_t.audio_ch_5, 'audio_ch_6': old_deliv_t.audio_ch_6, 'audio_ch_7': old_deliv_t.audio_ch_7, 'audio_ch_8': old_deliv_t.audio_ch_8, 'audio_ch_9': old_deliv_t.audio_ch_9, 'audio_ch_10': old_deliv_t.audio_ch_10, 'audio_ch_11': old_deliv_t.audio_ch_11, 'audio_ch_12': old_deliv_t.audio_ch_12, 'audio_ch_13': old_deliv_t.audio_ch_13, 'audio_ch_14': old_deliv_t.audio_ch_14, 'audio_ch_15': old_deliv_t.audio_ch_15, 'audio_ch_16': old_deliv_t.audio_ch_16, 'audio_ch_17': old_deliv_t.audio_ch_17, 'audio_ch_18': old_deliv_t.audio_ch_18, 'audio_ch_19': old_deliv_t.audio_ch_19, 'audio_ch_20': old_deliv_t.audio_ch_20, 'audio_ch_21': old_deliv_t.audio_ch_21, 'audio_ch_22': old_deliv_t.audio_ch_22, 'audio_ch_23': old_deliv_t.audio_ch_23, 'audio_ch_24': old_deliv_t.audio_ch_24, 'format': old_deliv_t.format, 'frame_rate': old_deliv_t.frame_rate, 'work_order_templ_code': nw.code, 'title': old_deliv_t.title, 'attn': old_deliv_t.attn, 'deliver_to': old_deliv_t.deliver_to};
                                                            //alert('going into kill nulls');
                                                            d_templ_data = kill_nulls(d_templ_data);
                                                            //alert('back from kill_nulls');
                                                            d_keys = Object.keys(d_templ_data);
                                                            new_deliv = server.insert('twog/deliverable_templ', d_templ_data)
                                                            //alert('Inserted d_templ');
                                                            if(new_deliv_codes == ''){
                                                                new_deliv_codes = new_deliv.code;
                                                            }else{
                                                                new_deliv_codes = new_deliv_codes + ',' + new_deliv.code;
                                                            }
                                                            deliv_trade[old_deliv_t.code] = new_deliv.code
                                                            deliv_seen.push(old_deliv_t.code);
                                                        }
                                                    }
                                                }
                                                old_inter_codes = ow.intermediate_file_templ_codes.split(',');
                                                //alert('old_inter_codes = ' + old_inter_codes);
                                                oiftc = ow.intermediate_file_templ_codes;
                                                if(oiftc != '' && oiftc != null){
                                                    for(var v = 0; v < old_inter_codes.length; v++){
                                                        oic = old_inter_codes[v];
                                                        old_inter_t = server.eval("@SOBJECT(twog/intermediate_file_templ['code','" + oic + "'])");
                                                        if(old_inter_t.length > 0){
                                                            old_inter_t = old_inter_t[0];
                                                            //alert('inserting intermediate_file_templ');
                                                            inter_templ_data = {'description': old_inter_t.description, 'keywords': old_inter_t.keywords, 'title': old_inter_t.title}; 
                                                            inter_templ_data = kill_nulls(inter_templ_data);
                                                            new_inter = server.insert('twog/intermediate_file_templ', inter_templ_data) 
                                                            if(new_inter_codes == ''){
                                                                new_inter_codes = new_inter.code;
                                                            }else{
                                                                new_inter_codes = new_inter_codes + ',' + new_inter.code;
                                                            }
                                                            inter_trade[old_inter_t.code] = new_inter.code
                                                            inter_seen.push(old_inter_t.code);
                                                        }
                                                    }  
                                                }
                                                nw_data = {'description': ow.description, 'keywords': ow.keywords, 'process': ow.process, 'instructions': ow.instructions, 'parent_pipe': name_prompt, 'wiki_page': ow.wiki_page, 'work_group': ow.work_group, 'estimated_work_hours': ow.estimated_work_hours, 'deliverable_templ_codes': new_deliv_codes, 'intermediate_file_templ_codes': new_inter_codes};
                                                //alert('nw data = ' + nw_data);
                                                nw_data = kill_nulls(nw_data);
                                                //alert('nw.code = ' + nw.code);
                                                server.update(nw.__search_key__, nw_data);
                                                //now do equipment_used_templs, wo_passin_templs and wo_prereq_templs
                                                eq_templs = server.eval("@SOBJECT(twog/equipment_used_templ['work_order_templ_code','" + ow.code + "'])");
                                                for(var v = 0; v < eq_templs.length; v++){
                                                    eq = eq_templs[v];
                                                    //alert('inserting equipment_used_templ');
                                                    eq_used_templ_data = {'description': eq.description, 'keywords': eq.keywords, 'name': eq.name, 'units': eq.units, 'equipment_code': eq.equipment_code, 'expected_duration': eq.expected_duration, 'expected_quantity': eq.expected_quantity, 'expected_cost': eq.expected_cost, 'work_order_templ_code': nw.code};
                                                    eq_used_templ_data = kill_nulls(eq_used_templ_data);
                                                    server.insert('twog/equipment_used_templ', eq_used_templ_data);
                                                } 
                                                wopts = server.eval("@SOBJECT(twog/work_order_passin_templ['work_order_templ_code','" + ow.code + "'])");
                                                for(var v = 0; v < wopts.length; v++){
                                                    wopt = wopts[v];
                                                    inter_code = '';
                                                    deliv_code = '';
                                                    if(wopt.intermediate_file_templ_code in oc(inter_seen)){
                                                        inter_code = inter_trade[wopt.intermediate_file_templ_code];
                                                    }
                                                    if(wopt.deliverable_templ_code in oc(deliv_seen)){
                                                        deliv_code = deliv_trade[wopt.deliverable_templ_code]; 
                                                    }
                                                    //alert('inserting work_order_passin_templ');
                                                    wopt_data = {'keywords': wopt.keywords, 'work_order_templ_code': nw.code, 'intermediate_file_templ_code': inter_code, 'deliverable_templ_code': deliv_code};
                                                    wopt_data = kill_nulls(wopt_data);
                                                    server.insert('twog/work_order_passin_templ', wopt_data)
                                                }
                                                wpres = server.eval("@SOBJECT(twog/work_order_prereq_templ['work_order_templ_code','" + ow.code + "'])");
                                                for(var v = 0; v < wpres.length; v++){
                                                    wpre = wpres[v];
                                                    //alert('inserting work_order_prereq_templ');
                                                    wopret_data = {'description': wpre.description, 'keywords': wpre.keywords, 'prereq': wpre.prereq, 'work_order_templ_code': nw.code}; 
                                                    wopret_data = kill_nulls(wopret_data);
                                                    server.insert('twog/work_order_prereq_templ', wopret_data); 
                                                }
                                                //alert('4 The End..going back to top');
                                            }
                                           //alert('End 2');
                                        } 
                                        //alert('End 3');
                                    }  

                                }
                    }
                    //alert('End 10');
                }else{
                    alert('The name you assigned is the same as the original. Please change the pipeline name.');
                }
                //alert('End 11');
            } 
            server.delete_sobject(action.__search_key__);
        }else{
            alert("Sorry. You can't clone a pipeline from an order that is not a Master. Also make sure there are not 2 or more pipelines loaded in the editor and that this isn't the first time the pipeline has been created.");
        }
       //alert('End 12');
       alert('Done');

        spt.app_busy.hide();

        ''' % (my.order_code, my.order_sk, user_name)
        } )

        button = ButtonNewWdg(title="Add Node", icon=IconWdg.ADD)
        button_row.add(button)

        button.add_behavior( {
        'type': 'click_up',
        'cbjs_action': '''
        var top = bvr.src_el.getParent(".spt_pipeline_editor_top");
        var wrapper = top.getElement(".spt_pipeline_wrapper");
        spt.pipeline.init_cbk(wrapper);
        spt.pipeline.add_node();

        top.addClass("spt_has_changes");
        '''
        } )

        button = ButtonNewWdg(title="Delete Selected", icon=IconWdg.DELETE)
        button_row.add(button)

        button.add_behavior( {
        'type': 'click_up',
        'cbjs_action': '''
        var top = bvr.src_el.getParent(".spt_pipeline_editor_top");
        var wrapper = top.getElement(".spt_pipeline_wrapper");
        spt.pipeline.init_cbk(wrapper);

        spt.pipeline.delete_selected();

        var nodes = spt.pipeline.get_selected_nodes();
        for (var i = 0; i < nodes.length; i++) {
            spt.pipeline.remove_node(nodes[i]);
        }
        '''
        } )



        button = ButtonNewWdg(title="Clear Canvas", icon=IconWdg.KILL)
        button_row.add(button)

        button.add_behavior( {
        'type': 'click_up',
        'cbjs_action': '''

        var ok = function() {
            var top = bvr.src_el.getParent(".spt_pipeline_editor_top");
            var wrapper = top.getElement(".spt_pipeline_wrapper");
            spt.pipeline.init_cbk(wrapper);

            spt.pipeline.clear_canvas();
            var tool_top = document.getElementsByClassName('spt_pipeline_tool_top')[0];
            tool_top.setAttribute('pipe_xmls','');

            // set the current group to default
            var current = top.getElement(".spt_pipeline_editor_current");
            current.value = "default";
            spt.pipeline.set_current_group("default")
        }
        spt.confirm("Are you sure you wish to clear the canvas?", ok, null ); 

        '''
        } )

 


        button = ButtonNewWdg(title="Edit Properties", icon=IconWdg.INFO)
        button_row.add(button)
        button.add_dialog(my.properties_dialog)


        return button_row



    def get_zoom_buttons_wdg(my):
        from pyasm.widget import IconWdg
        from tactic.ui.widget.button_new_wdg import ButtonNewWdg, ButtonRowWdg, IconButtonWdg, SingleButtonWdg

        button_row = DivWdg()
        button_row.add_border()
        button_row.set_round_corners(5)
        button_row.add_style("padding: 6px 10px 9px 5px")

        button = SingleButtonWdg(title="Zoom In", icon=IconWdg.ZOOM_IN, show_out=False)
        button_row.add(button)
        button.add_style("float: left")
        button.add_behavior( {
        'type': 'click_up',
        'cbjs_action': '''
        var top = bvr.src_el.getParent(".spt_pipeline_editor_top");
        var wrapper = top.getElement(".spt_pipeline_wrapper");
        spt.pipeline.init_cbk(wrapper);

        var scale = spt.pipeline.get_scale();
        scale = scale * 1.05;
        spt.pipeline.set_scale(scale);
        '''
        } )



        button = SingleButtonWdg(title="Zoom Out", icon=IconWdg.ZOOM_OUT, show_out=False)
        button_row.add(button)
        button.add_style("float: left")

        button.add_behavior( {
        'type': 'click_up',
        'cbjs_action': '''
        var top = bvr.src_el.getParent(".spt_pipeline_editor_top");
        var wrapper = top.getElement(".spt_pipeline_wrapper");
        spt.pipeline.init_cbk(wrapper);

        var scale = spt.pipeline.get_scale();
        scale = scale / 1.05;
        spt.pipeline.set_scale(scale);
        '''
        } )

        select = SelectWdg("zoom")
        select.add_style("width: 55px")
        select.set_option("labels", ["10%", "25%", "50%", "75%", "100%", "125%", "150%", "----", "Fit to Current Group", "Fit To Canvas"])
        select.set_option("values", ["0.1", "0.25", "0.50", "0.75", "1.0", "1.25", "1.5", "", "fit_to_current", "fit_to_canvas"])
        select.add_empty_option("Zoom")
        button_row.add(select)
        #select.set_value("1.0")
        select.add_behavior( {
        'type': 'change',
        'cbjs_action': '''
        var top = bvr.src_el.getParent(".spt_pipeline_editor_top");
        var wrapper = top.getElement(".spt_pipeline_wrapper");
        spt.pipeline.init_cbk(wrapper);

        var value = bvr.src_el.value;
        if (value == '') {
            return;
        }
        else if (value == 'fit_to_canvas') {
            spt.pipeline.fit_to_canvas();
        }
        else if (value == 'fit_to_current') {
            var group_name = spt.pipeline.get_current_group();
            spt.pipeline.fit_to_canvas(group_name);
        }
        else {
            var scale = parseFloat(value);
            spt.pipeline.set_scale(scale);
        }
        bvr.src_el.value = '';
        '''
        } )

        return button_row



    def get_schema_buttons_wdg(my):
        from pyasm.widget import IconWdg
        from tactic.ui.widget.button_new_wdg import ButtonNewWdg, ButtonRowWdg, SingleButtonWdg

        button_row = DivWdg()
        button_row.add_style("padding-top: 5px")

        project_code = Project.get_project_code()

        button = SingleButtonWdg(title="Show Schema for Reference", icon=IconWdg.DEPENDENCY)
        button_row.add(button)
        button.add_style("float: left")
        button.add_behavior( {
        'type': 'click_up',
        'project_code': project_code,
        'cbjs_action': '''
        var top = bvr.src_el.getParent(".spt_pipeline_editor_top");
        var schema_editor = top.getElement(".spt_schema_wrapper");
        spt.pipeline.init_cbk(schema_editor);
        spt.toggle_show_hide(schema_editor);

        var group = spt.pipeline.get_group(bvr.project_code);
        if (group != null) {
            return;
        }

        spt.pipeline.import_schema( bvr.project_code );
        '''
        } )

        return button_row





    def get_pipeline_select_wdg(my):
        div = DivWdg()
        div.add_border(modifier=10)
        div.add_style("padding: 7px")
        div.add_style("-moz-border-radius: 5px")
        div.add("Current Pipeline: " )
        pipeline_select = SelectWdg("current_pipeline")
        div.add(pipeline_select)
        pipeline_select.add_class("spt_pipeline_editor_current")
        pipeline_select.set_option("values", "default")
        pipeline_select.set_option("labels", "-- NEW --")

        pipeline_select.add_behavior( {
            'type': 'change',
            'cbjs_action': '''
            var top = bvr.src_el.getParent(".spt_pipeline_editor_top");
            var wrapper = top.getElement(".spt_pipeline_wrapper");
            spt.pipeline.init_cbk(wrapper);

            var group_name = bvr.src_el.value;
            spt.pipeline.set_current_group(group_name);
            '''
        } )


        # Button to add a new pipeline to the canvas
        # NOTE: this is disabled ... workflow is not up to the level we
        # need it to be.
        button = IconButtonWdg(title="Add Pipeline to Canvas", icon=IconWdg.ARROWHEAD_DARK_DOWN)
        #div.add(button)
        button.add_style("float: right")
        dialog = DialogWdg()
        div.add(dialog)
        dialog.add_title("Add Pipeline to Canvas")


        dialog_div = DivWdg()
        dialog_div.add_style("padding: 5px")
        dialog_div.add_color("background", "background")
        dialog_div.add_border()
        dialog.add(dialog_div)

        table = Table()
        table.add_color("color", "color")
        table.add_style("margin: 10px")
        table.add_style("width: 270px")
        dialog_div.add(table)

        table.add_row()
        td = table.add_cell()
        td.add("Pipeline code: ")
        text = TextWdg("new_pipeline")
        td = table.add_cell()
        td.add(text)
        text.add_class("spt_new_pipeline")

        from tactic.ui.input import ColorInputWdg


        table.add_row()
        td = table.add_cell()
        td.add("Color: ")
        color_input = ColorInputWdg(name="spt_color")
        color_input.add_style("float: left")
        td = table.add_cell()
        td.add(color_input)


        dialog_div.add("<hr/>")



        add_button = ActionButtonWdg(title='Add', tip='Add New Pipeline to Canvas')
        dialog_div.add(add_button)
        add_button.add_behavior( {
        'type': 'click_up',
        'dialog_id': dialog.get_id(),
        'cbjs_action': '''
        var dialog_top = bvr.src_el.getParent(".spt_dialog_top");
        var close_event = bvr.dialog_id + "|dialog_close";

        var values = spt.api.get_input_values(dialog_top, null, false);
        var value = values.new_pipeline;
        if (value == '') {
            alert("Cannot add empty pipeline");
            return;
        }

        var top = bvr.src_el.getParent(".spt_pipeline_editor_top");
        var select = top.getElement(".spt_pipeline_editor_current");

        for ( var i = 0; i < select.options.length; i++) {
            var select_value = select.options[i].value;
            if (select_value == value) {
                alert("Pipeline ["+value+"] already exists");
                return;
            }
        }


        var option = new Option(value, value);
        select.options[select.options.length] = option;

        select.value = value;
        spt.pipeline.set_current_group(value);

        // Add this to the colors
        var colors = spt.pipeline.get_data().colors;
        if (values.spt_color != '') {
            colors[value] = values.spt_color;
        }
        else {
            colors[value] = '#333333';
        }

        spt.named_events.fire_event(close_event, {});

        spt.pipeline.add_node();

        '''
        } )
        dialog.set_as_activator(button)

        button.add_behavior( {
        'type': 'click_up',
        'dialog_id': dialog.get_id(),
        'cbjs_action': '''
        spt.api.Utility.clear_inputs( $(bvr.dialog_id) );
        '''
        } )



        return div


class CustomPipelinePropertyWdg(BaseRefreshWdg):

    def get_display(my):
        div = DivWdg()
        div.add_class("spt_pipeline_properties_top")

        process = my.kwargs.get("process")
        pipeline_code = my.kwargs.get("pipeline_code")
        from tactic.ui.app import HelpButtonWdg
        help_button = HelpButtonWdg(alias='pipeline-process-options|project-workflow-introduction')
        div.add( help_button )
        help_button.add_style("float: right")



        pipeline = Pipeline.get_by_code(pipeline_code)
        if not pipeline:
            attrs = {}
        else:
            attrs = pipeline.get_process_attrs(process)
        web = WebContainer.get_web()

        div.add_color('background', 'background')

        #div.set_id("properties_editor")
        #div.add_style("display", "none")



        title_div = DivWdg()
        div.add(title_div)
        title_div.add_style("height: 20px")
        title_div.add_gradient("background", "background", -20)
        title_div.add_class("spt_property_title")
        if not process:
            title_div.add("Process: <i>--None--</i>")
        else:
            title_div.add("Process: %s" % process)
        title_div.add_style("font-weight: bold")
        title_div.add_style("margin-bottom: 5px")
        title_div.add_style("padding: 5px")


        # add a no process message
        no_process_wdg = DivWdg()
        no_process_wdg.add_class("spt_pipeline_properties_no_process")
        div.add(no_process_wdg)
        no_process_wdg.add( "No process node or connector selected")
        no_process_wdg.add_style("padding: 30px")



        # get a list of known properties
        properties = ['group', "completion", "task_pipeline", 'assigned_login_group', 'supervisor_login_group',\
                'duration', 'bid_duration']


        # show other properties
        table = Table()
        table.add_class("spt_pipeline_properties_content")
        table.add_style("margin: 10px")
        table.add_color('color', 'color')
        table.add_row()
        #table.add_header("Property")
        #table.add_header("Value")


        if process:
            no_process_wdg.add_style("display: none")
        else:
            table.add_style("display: none")



        table.add_behavior( {
        'type': 'load',
        'cbjs_action': my.get_onload_js()
        } )

        
        # group
        # Making invisible to ensure that it still gets recorded if there.
        tr = table.add_row()
        tr.add_style("display: none")
        td = table.add_cell('Group: ')
        td.add_style("width: 250px")
        td.add_attr("title", "Nodes can grouped together within a pipeline")
        td.add_style("width: 200px")
        text_name = "spt_property_group"
        text = TextWdg(text_name)
        text.add_class(text_name)
        text.add_event("onBlur", "spt.pipeline_properties.set_properties()")

        th = table.add_cell(text)
        
        # completion (visibilitty depends on sType)
        table.add_row(css='spt_property_status_completion')
        td = table.add_cell('Completion (0 to 100):')
        td.add_attr("title", "Determines the completion level that this node represents.")

        text_name = "spt_property_completion"
        text = TextWdg(text_name)
        text.add_class(text_name)
        text.add_event("onBlur", "spt.pipeline_properties.set_properties()")

        th = table.add_cell(text)
        
        # These searchs are needed for the task_pipeline select widget
        task_pipeline_search = Search('sthpw/pipeline')
        task_pipeline_search.add_filter('search_type', 'sthpw/task')
        task_pipeline_search.add_project_filter()
        task_pipelines = task_pipeline_search.get_sobjects()
        
        normal_pipeline_search = Search('sthpw/pipeline')
        normal_pipeline_search.add_filter('search_type', 'sthpw/task', '!=')
        normal_pipelines = normal_pipeline_search.get_sobjects()
       

        # task_pipeline  (visibilitty depends on sType)
        table.add_row(css='spt_property_task_status_pipeline')
        td = table.add_cell('Task Status Pipeline')
        td.add_attr("title", "The task status pipeline determines all of the statuses that occur within this process")

        text_name = "spt_property_task_pipeline"
        select = SelectWdg(text_name)
        #select.append_option('<< sthpw/task pipelines >>', '')
        
        for pipeline in task_pipelines:
            select.append_option(pipeline.get_value('code'), pipeline.get_value('code'))
        #select.append_option('', '')
        #select.append_option('<< all other pipelines >>', '')
        #for pipeline in normal_pipelines:
        #    select.append_option('%s (%s)'%(pipeline.get_value('code'), pipeline.get_value('search_type')), pipeline.get_value('code'))
        
        select.add_empty_option('-- Select --')
        select.add_class(text_name)
        select.add_event("onBlur", "spt.pipeline_properties.set_properties()")

        th = table.add_cell(select)
        
        # The search needed for the login_group select widgets
        login_group_search = Search('sthpw/login_group')
        
        # assigned_login_group
        table.add_row()
        td = table.add_cell('Assigned Login Group:')
        td.add_attr("title", "Used for limiting the users displayed when this process is chosen in a task view.")

        text_name = "spt_property_assigned_login_group"
        select = SelectWdg(text_name)
        select.set_search_for_options(login_group_search, 'login_group', 'login_group')
        select.add_empty_option('-- Select --')
        select.add_class(text_name)
        select.add_event("onBlur", "spt.pipeline_properties.set_properties()")

        th = table.add_cell(select)
        
        # supervisor_login_group
        table.add_row()
        td = table.add_cell('Supervisor Login Group:')
        td.add_attr("title", "Used for limiting the supervisors displayed when this process is chosen in a task view.")
        text_name = "spt_property_supervisor_login_group"
        select = SelectWdg(text_name)
        select.set_search_for_options(login_group_search, 'login_group', 'login_group')
        select.add_empty_option('-- Select --')
        select.add_class(text_name)
        select.add_event("onBlur", "spt.pipeline_properties.set_properties()")

        th = table.add_cell(select)
        
        # duration
        table.add_row()
        td = table.add_cell('Default Duration:')
        td.add_attr("title", "The default duration determines the starting duration of a task that is generated for this process")

        text_name = "spt_property_duration"
        text = TextWdg(text_name)
        text.add_style("width: 30px")
        text.add_class(text_name)
        text.add_event("onBlur", "spt.pipeline_properties.set_properties()")

        th = table.add_cell(text)
        th.add(" days")

        # bid duration in hours
        table.add_row()
        td = table.add_cell('Default Bid Duration:')
        td.add_attr("title", "The default bid duration determines the estimated number of hours will be spent on this task.")

        text_name = "spt_property_bid_duration"
        text = TextWdg(text_name)
        text.add_style("width: 30px")
        text.add_class(text_name)
        text.add_event("onBlur", "spt.pipeline_properties.set_properties()")

        th = table.add_cell(text)
        th.add(" hours")
        
        # color
        table.add_row()
        td = table.add_cell('Color:')
        td.add_attr("title", "Used by various parts of the interface to show the color of this process.")

        text_name = "spt_property_color"
        from tactic.ui.input import ColorInputWdg
        text = TextWdg(text_name)
        color = ColorInputWdg(text_name)
        color.set_input(text)
        text.add_class(text_name)
        text.add_event("onBlur", "spt.pipeline_properties.set_properties()")

        table.add_cell(color)

        # label
        table.add_row()
        td = table.add_cell('Label:')

        text_name = "spt_property_label"
        text = TextWdg(text_name)
        text.add_class(text_name)
        text.add_event("onChange", "spt.pipeline_properties.set_properties()")

        table.add_cell(text)

        table.add_row()
        td = table.add_cell('Description:')

        text_name = "spt_property_description"
        text = TextWdg(text_name)
        text.add_class(text_name)
        text.add_event("onBlur", "spt.pipeline_properties.set_properties()")

        table.add_cell(text)

        tr, td = table.add_row_cell()

        button = ActionButtonWdg(title="OK", tip="Confirm properties change. Remember to save pipeline at the end.")
        td.add("<hr/>")
        td.add(button)
        button.add_style("float: right")
        button.add_style("margin-right: 20px")
        td.add("<br clear='all'/>")
        button.add_behavior( {
        'type': 'click_up',
        'cbjs_action': '''
        spt.pipeline_properties.set_properties();
        var top = bvr.src_el.getParent(".spt_dialog_top");
        spt.hide(top);
        spt.named_events.fire_event('pipeline|change', {});
        '''
        } )


        div.add(table)

        return div

    def get_onload_js(my):
        return r'''

spt.pipeline_properties = {};
spt.pipeline_properties.set_properties = function() {

    var top = bvr.src_el.getParent(".spt_pipeline_editor_top");
    var wrapper = top.getElement(".spt_pipeline_wrapper");
    spt.pipeline.init_cbk(wrapper);

    var prop_top = spt.get_element(top, ".spt_pipeline_properties_top");
    var connector_top = spt.get_element(top, ".spt_connector_properties_top");

    var selected_nodes = spt.pipeline.get_selected_nodes();
    var selected = spt.pipeline.get_selected();
    if (selected_nodes.length > 1) {
        alert('Please select only 1 node to set property');
        return;
    }
        
    if (selected_nodes.length==1) {
        var title_el = spt.get_element(top, ".spt_property_title");
        var node_name = title_el.node_name;
        var node = spt.pipeline.get_node_by_name(node_name);
        if (node)
        {
            var properties = ['group', 'completion', 'task_pipeline', 'assigned_login_group', 'supervisor_login_group','duration', 'bid_duration','color', 'label', 'description'];

            for ( var i = 0; i < properties.length; i++ ) {
                var el = prop_top.getElement(".spt_property_" + properties[i]);
                spt.pipeline.set_node_property( node, properties[i], el.value );
            }
        }
    }
    else if (selected.length==1 && selected[0].type == 'connector') {
        var el = connector_top.getElement(".spt_connector_context");
        selected[0].set_attr('context', el.value);
        
    }
            
}



spt.pipeline_properties.show_node_properties = function(node) {

    var top = node.getParent(".spt_pipeline_tool_top");
    var prop_top = spt.get_element(top, ".spt_pipeline_properties_top");
    var connect_top = spt.get_element(top, ".spt_connector_properties_top");

    var content = spt.get_element(prop_top, ".spt_pipeline_properties_content");
    var no_process = spt.get_element(prop_top, ".spt_pipeline_properties_no_process");
    var connector_prop = spt.get_element(connect_top, ".spt_connector_properties_content");
    spt.show(prop_top);
    spt.show(content);
    spt.hide(no_process);
    spt.hide(connector_prop);


    var node_name = spt.pipeline.get_node_name(node);
    var group = spt.pipeline.get_group_by_node(node);
    var group_name = group.get_name();

    // must set current group
    spt.pipeline.set_current_group(group_name);
    var stype = spt.pipeline.get_search_type(group_name);
    var task_pipe_tr = spt.get_element(prop_top, ".spt_property_task_status_pipeline");
    var status_completion_tr = spt.get_element(prop_top, ".spt_property_status_completion");
    if (stype && stype =='sthpw/task') { 
        spt.hide(task_pipe_tr);
        spt.show(status_completion_tr);

    }
    else {
        spt.show(task_pipe_tr);
        spt.hide(status_completion_tr);
    }

    var title = prop_top.getElement(".spt_property_title");
    title.innerHTML = "Node: " + node_name;
    title.node_name = node_name;

    var properties = ['group', 'completion', 'task_pipeline', 'assigned_login_group', 'supervisor_login_group','duration', 'bid_duration','color', 'label', 'description'];

    for ( var i = 0; i < properties.length; i++ ) {
        var el = prop_top.getElement(".spt_property_" + properties[i]);
        var value = node.properties[properties[i]];
        if (typeof(value) == 'undefined') {
            el.value = '';
        }
        else {
            el.value = node.properties[properties[i]];
            if (properties[i] == 'color')
                el.setStyle('background',el.value);
        }
    }
    // set the current pipeline
    current = top.getElement(".spt_pipeline_editor_current");
    current.value = group_name;



}

        '''


class CustomConnectorPropertyWdg(CustomPipelinePropertyWdg):

    def get_display(my):
        div = DivWdg()
        div.add_class("spt_connector_properties_top")

        web = WebContainer.get_web()

        div.add_color('background', 'background')


        title_div = DivWdg()
        div.add(title_div)
        title_div.add_style("height: 20px")
        title_div.add_gradient("background", "background", -20)
        title_div.add_class("spt_property_title")
      
        title_div.add_style("font-weight: bold")
        title_div.add_style("margin-bottom: 5px")
        title_div.add_style("padding: 5px")





        # show other properties
        table = Table()
        table.add_class("spt_connector_properties_content")
        table.add_style("margin: 10px")
        table.add_color('color', 'color')


        table.add_style("display: none")



        table.add_behavior( {
        'type': 'load',
        'cbjs_action': my.get_onload_js()
        } )

        
        # group
        table.add_row()
        td = table.add_cell('context')
        td.add_style("width: 200px")
        text_name = "spt_connector_context"
        text = TextWdg(text_name)
        text.add_class(text_name)
        text.add_event("onBlur", "spt.pipeline_properties.set_properties()")

        th = table.add_cell(text)
        
        tr, td = table.add_row_cell()
       

        button = ActionButtonWdg(title="OK", tip="Confirm connector properties change. Remember to save pipeline at the end.")
        td.add("<hr/>")
        td.add(button)
        button.add_style("float: right")
        button.add_style("margin-right: 20px")
        td.add("<br clear='all'/>")
        button.add_behavior( {
        'type': 'click_up',
        'cbjs_action': '''spt.pipeline_properties.set_properties();
                         var top = bvr.src_el.getParent(".spt_dialog_top");
                        spt.hide(top);
                        spt.named_events.fire_event('pipeline|change', {});'''
        } )

        div.add(table)

        return div


class CustomPipelineToolCanvasWdg(CustomPipelineCanvasWdg):


    def get_node_behaviors(my):
        behavior = {
        'type': 'click_up',
        'cbjs_action': '''
        spt.pipeline.init(bvr);
        var node = bvr.src_el;
        spt.pipeline_properties.show_node_properties(node);
        '''
        }
 

        return [behavior]


    def get_canvas_behaviors(my):
        behavior = {
        'type': 'click_up',
        'cbjs_action': '''
        spt.pipeline.init(bvr);
        var node = bvr.src_el;

        var top = bvr.src_el.getParent(".spt_pipeline_tool_top");
        var prop_top = spt.get_element(top, ".spt_pipeline_properties_top");
        var connect_top = spt.get_element(top, ".spt_connector_properties_top");

        var pipeline_prop = spt.get_element(prop_top, ".spt_pipeline_properties_content");
        var no_process = spt.get_element(prop_top, ".spt_pipeline_properties_no_process");
        var connector_prop = spt.get_element(connect_top, ".spt_connector_properties_content");

        var selected = spt.pipeline.get_selected();
        
        if (selected.length > 0) {

            if  (selected[0].type == 'connector') {
                var connector = selected[0];
                var context = connector.get_attr('context');
                var text = spt.get_element(connector_prop, ".spt_connector_context");
                if (context) {
                    text.value = context;
                }
                else {
                    text.value = '';
                }
                spt.hide(prop_top);
                spt.show(connector_prop);
            }
        }
        else {
                spt.hide(pipeline_prop);
                spt.show(no_process);
                spt.hide(connector_prop);
            }
     
        
        '''
        }

        return [behavior]




    def get_node_context_menu(my):

        #menu = Menu(width=180)
        #menu.set_allow_icons(False)
        #menu.set_setup_cbfn( 'spt.dg_table.smenu_ctx.setup_cbk' )
        menu = super(CustomPipelineToolCanvasWdg, my).get_node_context_menu()


        project_code = Project.get_project_code()

        menu_item = MenuItem(type='title', label='Details')
        menu.add(menu_item)

        #menu_item = MenuItem(type='action', label='Show Properties')
        #menu.add(menu_item)


        menu_item = MenuItem(type='action', label='Edit Properties')
        menu.add(menu_item)
        menu_item.add_behavior( {
            'cbjs_action': '''
            var node = spt.smenu.get_activator(bvr);
            spt.named_events.fire_event('pipeline|show_properties', {src_el: node});

            '''
        } )



        menu_item = MenuItem(type='action', label='Show Triggers/Notifications')
        menu.add(menu_item)
        menu_item.add_behavior( {
            'cbjs_action': '''
            var node = spt.smenu.get_activator(bvr);

            var top = node.getParent(".spt_pipeline_tool_top");
            spt.tab.top = top.getElement(".spt_tab_top");

            var process = node.getAttribute("spt_element_name");
            var pipeline_code = node.spt_group;
            var search_type = spt.pipeline.get_search_type(pipeline_code);

            var class_name = 'tactic.ui.tools.trigger_wdg.TriggerToolWdg';
            var kwargs = {
                search_type: search_type,
                pipeline_code: pipeline_code,
                process: process
            }

            element_name = 'trigger_'+process;
            title = 'Triggers ['+process+']';
            spt.tab.add_new(element_name, title, class_name, kwargs);

            '''
        } )

        menu_item = MenuItem(type='action', label='Show Naming')
        #menu.add(menu_item)
        menu_item.add_behavior( {
            'cbjs_action': '''
            var node = spt.smenu.get_activator(bvr);

            var top = node.getParent(".spt_pipeline_tool_top");
            spt.tab.top = top.getElement(".spt_tab_top");

            var process = node.getAttribute("spt_element_name");
            var pipeline_code = node.spt_group;

            var class_name = 'tactic.ui.tools.trigger_wdg.NamingToolWdg';
            var kwargs = {
                pipeline_code: pipeline_code,
                process: process
            }

            element_name = 'naming'+process;
            title = 'Naming ['+process+']';
            spt.tab.add_new(element_name, title, class_name, kwargs);

            '''
        } )


        menu_item = MenuItem(type='action', label='Show Processes')
        menu.add(menu_item)
        menu_item.add_behavior( {
        'cbjs_action': '''

        var node = spt.smenu.get_activator(bvr);
        var process = node.getAttribute("spt_element_name");
        var pipeline_code = node.spt_group;

        var expr = "@SOBJECT(config/process['@ORDER_BY','sort_order']['pipeline_code','"+pipeline_code+"'])"

        var class_name = 'tactic.ui.panel.ViewPanelWdg';
        var kwargs = {
            search_type: 'config/process',
            view: 'table',
            // NOTE: order by does not work here
            expression: expr
        }

        var top = node.getParent(".spt_pipeline_tool_top");
        spt.tab.top = top.getElement(".spt_tab_top");
        spt.tab.add_new("processes", "Processes", class_name, kwargs);
        '''
        } )




        menu_item = MenuItem(type='action', label='Customize Task Status')
        menu.add(menu_item)
        menu_item.add_behavior( {
        'cbjs_action': '''

        // check if there is a custom task status pipeline defined
        var node = spt.smenu.get_activator(bvr);
        spt.pipeline.init(node);
        var group_name = node.spt_group;
        var node_name = spt.pipeline.get_node_name(node);

        var search_type = "sthpw/pipeline";

        var server = TacticServerStub.get();
        var project_code = server.get_project();
        var code = project_code + '_' + node_name;

        // get the color
        var color = server.eval("@GET(sthpw/pipeline['code','"+group_name+"'].color)");

        var data = {
            code: code,
            search_type: 'sthpw/task',
            project_code: project_code
        };
        var task_pipeline = server.get_unique_sobject(search_type, data);
        var xml = task_pipeline.pipeline;
        //alert('strange spot ' + xml);
        if (xml != '') {
            spt.pipeline.import_pipeline(code);
            return;
        }

        if (!confirm("Confirm to create a custom task status pipeline") ) {
            return;
        }

 
        var xml = '';
        xml += '<pipeline>\\n';
        xml += '  <process name="Pending"/>\\n';
        xml += '  <process name="In_Progress"/>\\n';
        xml += '  <process name="Complete"/>\\n';
        xml += '  <connect from="Pending" to="In_Progress"/>\\n';
        xml += '  <connect from="In_Progress" to="Complete"/>\\n';
        xml += '</pipeline>\\n';

        server.update(task_pipeline, {pipeline: xml, color: color} );
        '''
        } )



        return menu


class CustomPipeEditWdg(BaseRefreshWdg):

    CLOSE_WDG = "close_wdg"

    ARGS_KEYS = {
            "mode": {
            'description': "The mode of this widget",
            'type': 'SelectWdg',
            'values': 'insert|edit|view',
            'default': 'insert',
            'category': 'Options'
        },
        "search_type": {
            'description': "SType that will be inserted or edited",
            'category': 'Options',
            'order': 0,
        },
        "title": {
            'description': "The title to appear at the top of the layout",
            'category': 'Options',
        },
        "view": {
            'description': "View of item to be edited",
            'category': 'Options',
            'order': 1,
        },
        "width": {
            'description': "Width of the widget",
            'category': 'Options',
        },


        "search_id": "id of the sobject to be edited",
        "code": "code of the sobject to be edited",

        "search_key": "search key of the sobject to be edited",

        "input_prefix": "prefix of any input widget",
        "access": 'override the default access',

        'cbjs_insert_path': 'override script path for the insert callback',
        'cbjs_edit_path': 'override script path for the edit callback',
        'cbjs_cancel': 'override for the cancel callback',

        "config_base": "view (DEPRECATED)",

        "default": "default data",
        "single": "when in insert mode, determine if only one entry can be inserted",
        "ignore": "A list of element names to ignore"
        }


    def init(my):
        my.is_refresh = my.kwargs.get("refresh")
        my.search_key = my.kwargs.get("search_key")
        my.ticket_key = my.kwargs.get("ticket")
        my.parent_key = my.kwargs.get("parent_key")
        my.expression = my.kwargs.get("expression")
        my.st2 = my.kwargs.get('st2')
        my.order_code = my.kwargs.get('order_code')
        my.client_name = my.kwargs.get('client_name')
        clone = False
        if 'clone' in my.kwargs.keys():
            clone = True

        # This assumed parent can cause errors as it tries to find a
        # relationship between to stypes that don't exist ... or worse,
        # try to bind them when one stype does not have the sufficent columns
        # ie: pipeline_code
        #if not my.parent_key:
        #    project = Project.get()
        #    my.parent_key = project.get_search_key()


        my.code = my.kwargs.get("code")
        # PREPEND HERE. MAKE MY.CODE = My.CLIENT_NAME + MY.CODE
        sobject = None
        if my.search_key:
            sobject = Search.get_by_search_key(my.search_key)
            my.search_id = sobject.get_id()
            my.search_type = sobject.get_base_search_type()
            my.mode = 'edit'

        elif my.expression:
            sobject = Search.eval(my.expression, single=True)
            my.search_id = sobject.get_id()
            my.search_type = sobject.get_base_search_type()
            my.mode = 'edit'


        elif my.ticket_key:
            from pyasm.security import Ticket, Login
            ticket = Ticket.get_by_valid_key(my.ticket_key)
            if not ticket:
                raise TacticException("No valid ticket")
            login_code = ticket.get_value("login")
            login = Login.get_by_code(login_code)
            my.search_type = "sthpw/login"
            my.search_id = login.get_id()
            my.mode = 'edit'

        elif my.code:
            my.search_type = my.kwargs.get("search_type")
            search = Search(my.search_type)
            search.add_filter("code", my.code)
            sobject = search.get_sobject()
            
            my.search_id = sobject.get_id()
            my.search_type = sobject.get_base_search_type()
            my.mode = 'edit'


        else:
            my.search_type = my.kwargs.get("search_type")
            my.search_id = my.kwargs.get("search_id")
            if not my.search_id:
                my.search_id = -1
            my.search_id = int(my.search_id)
            if my.search_id != -1:
                my.mode = "edit"
            else:
                my.mode = "insert"
                

        # explicit override
        if my.kwargs.get("mode"):
            my.mode = my.kwargs.get("mode")


        my.view = my.kwargs.get("view")
        if not my.view:
            my.view = my.kwargs.get("config_base")
        if not my.view:
            my.view = "edit"


        default_data = my.kwargs.get('default')
        
        if not default_data:
            default_data = {}
        elif isinstance(default_data, basestring):
            try:
                default_data = jsonloads(default_data)
            except:
                #may be it's regular dictionary
                try:
                    default_data = eval(default_data)
                except:
                    print "Warning: Cannot evaluate [%s]" %default_data
                    default_data = {}

        if sobject:
            my.set_sobjects([sobject], None)
        else:
            my.do_search()

        # TODO: get_config() is going the right direction (less features) but the more complicated method is biased 
        # towards edit and insert view.. and so it needs improvement as well

        if my.view not in ["insert", "edit"]:
            # try a new smaller way to get config only when an explicit view
            # is set
            my.config = my.get_config()
        else:
            my.config = WidgetConfigView.get_by_search_type(my.search_type, my.view)

        
        my.skipped_element_names = []
        my.element_names = my.config.get_element_names()
        ignore = my.kwargs.get("ignore")
        if isinstance(ignore, basestring):
            ignore = ignore.split("|")
        if not ignore:
            ignore = []

        my.element_titles = my.config.get_element_titles()  
        my.element_descriptions = my.config.get_element_descriptions()  
        my.input_prefix = my.kwargs.get('input_prefix')
        if not my.input_prefix:
            my.input_prefix = 'edit'
        
        security = Environment.get_security()
        default_access = "edit"
        project_code = Project.get_project_code()
        for i, element_name in enumerate(my.element_names):

            if element_name in ignore:
                my.skipped_element_names.append(element_name)
                continue
            # check security access
            access_key2 = {
                'search_type': my.search_type,
                'project': project_code
            }
            access_key1 = {
                'search_type': my.search_type,
                'key': element_name, 
                'project': project_code

            }
            access_keys = [access_key1, access_key2]
            is_editable = security.check_access('element', access_keys, "edit", default=default_access)

            
            if not is_editable:
                my.skipped_element_names.append(element_name)
                continue
            widget = my.config.get_display_widget(element_name, kbd_handler=False)
            widget.set_sobject(my.sobjects[0])

            default_value = default_data.get(element_name)
            if default_value:
                widget.set_value(default_value)
            if element_name in ['search_type','stype']:
                widget.set_value(my.st2) 
            attrs = my.config.get_element_attributes(element_name)
            editable = widget.is_editable()
            if editable:
                editable = attrs.get("edit")
                editable = editable != "false"
            
            if not editable:
                continue

            # set parent
            widget.set_parent_wdg(my)
            
            # set parent_key in insert mode for now
            if my.mode =='insert' and my.parent_key:
                widget.set_option('parent_key', my.parent_key)
            
            
            title = my.element_titles[i]
            if title:
                widget.set_title(title)
            my.widgets.append(widget)


            description = my.element_descriptions[i]
            widget.add_attr("title", description)




    def get_config(my):
        # look in the db first
        configs = []
        config = WidgetDbConfig.get_by_search_type(my.search_type, my.view)
        get_edit_def = False
        if config:
            configs.append(config)
            get_edit_def = True
            config = WidgetDbConfig.get_by_search_type(my.search_type, "edit_definition")
            if config:
                configs.append(config)

        #if my.mode == 'insert':
        #    config = WidgetDbConfig.get_by_search_type(my.search_type, "insert")
        #    if config:
        #        configs.append(config)
        # look for a definition
        #config = WidgetDbConfig.get_by_search_type(my.search_type, "edit")
        #if config:
        #    configs.append(config)

        file_configs = WidgetConfigView.get_configs_from_file(my.search_type, my.view)
        configs.extend(file_configs)

        file_configs = WidgetConfigView.get_configs_from_file(my.search_type, "edit")
        configs.extend(file_configs)

        #TODO: add edit_definition    
        #file_configs = WidgetConfigView.get_configs_from_file(my.search_type, "edit_definition")
        #configs.extend(file_configs)
        if not get_edit_def:
            config = WidgetDbConfig.get_by_search_type(my.search_type, "edit_definition")
            if config:
                configs.append(config)
    
        config = WidgetConfigView(my.search_type, my.view, configs)
        return config


 


    def get_display(my):

        search_type_obj = SearchType.get(my.search_type)
        sobj_title = search_type_obj.get_title()

        top_div = DivWdg()
        if not my.is_refresh:
            my.set_as_panel(top_div)
        content_div = DivWdg()
        content_div.add_class("spt_edit_top")
        content_div.set_attr("spt_search_key", my.search_key)


        # add close listener
        # FIXME: this is an absolute search, but is here for backwards
        # compatibility
        content_div.add_named_listener('close_CustomPipeEditWdg', '''
            var popup = bvr.src_el.getParent( ".spt_popup" );
            if (popup)
                spt.popup.close(popup);
        ''')


        attrs = my.config.get_view_attributes()
        default_access = attrs.get("access")

        if not default_access:
            default_access = "edit"

        project_code = Project.get_project_code()

        security = Environment.get_security()
        base_key =  search_type_obj.get_base_key()
        key = {
            'search_type': base_key,
            'project': project_code
        }
        access = security.check_access("sobject", key, "edit", default=default_access)
        if not access:
            my.is_disabled = True
        else:
            my.is_disabled = False

        disable_wdg = None
        if my.is_disabled:
            # TODO: This overlay doesn't work in IE, size, position, 
            # and transparency all fail. 
            disable_wdg = DivWdg(id='edit_wdg')
            disable_wdg.add_style("position: absolute")
            disable_wdg.add_style("height: 90%")
            disable_wdg.add_style("width: 100%")
            disable_wdg.add_style("left: 0px")
            #disable_wdg.add_style("bottom: 0px")
            #disable_wdg.add_style("top: 0px")

            disable_wdg.add_style("opacity: 0.2")
            disable_wdg.add_style("background: #fff")
            #disable_wdg.add_style("-moz-opacity: 0.2")
            disable_wdg.add_style("filter: Alpha(opacity=20)")
            disable_wdg.add("<center>EDIT DISABLED</center>")
            content_div.add(disable_wdg)


        attrs = my.config.get_view_attributes()

        inner = DivWdg()
        content_div.add(inner)
        menu = my.get_header_context_menu()
        menus = [menu.get_data()]
        menus_in = {
            'HEADER_CTX': menus,
        }
        SmartMenu.attach_smart_context_menu( inner, menus_in, False )






        table = Table()
        inner.add(table)
        table.add_color("background", "background")
        table.add_border()
        table.add_color("color", "color")



        width = attrs.get('width')
        if not width:
            width = my.kwargs.get("width")
        if not width:
            width = 500
        table.add_style("width: %s" % width)

        height = attrs.get('height')
        if height:
            table.add_style("height: %s" % height)

        
        tr = table.add_row()
        tr.add_border()


        my.add_header(table, sobj_title)

        single = my.kwargs.get("single")
        if single in ['false', False] and my.mode == 'insert':
            multi_div = DivWdg()
            multi_div.add_style("text-align: left")

            multi_div.add("Specify the number of items that will be added with this form:<br/><br/>")


            multi_div.add("<b># of new items to add: </b>")
            multi_div.add("&nbsp;"*4)


            multi_text = TextWdg("multiplier")
            multi_text.add_style("width: 30px")
            multi_div.add(multi_text)

            tr, td = table.add_row_cell( multi_div )


            td.add_color("border-color", "table_border", default="border")
            td.add_style("border-width: 1px")
            td.add_style("border-style: solid")
            td.add_style("padding: 8 3 8 3")
            td.add_color("background", "background3")
            td.add_color("color", "color3")
        
        security = Environment.get_security()

        # break the widgets up in columns
        num_columns = attrs.get('num_columns')
        if not num_columns:
            num_columns = my.kwargs.get('num_columns')

        if not num_columns:
            num_columns = 1
        else:
            num_columns = int(num_columns)

        # go through each widget and draw it
        for i, widget in enumerate(my.widgets):

            # since a widget name called code doesn't necessariy write to code column, it is commented out for now
            """
            key = { 'search_type' : search_type_obj.get_base_key(),
                'column' : widget.get_name(),
                'project': project_code}
            # check security on widget
            if not security.check_access( "sobject_column",\
                key, "edit"):
                my.skipped_element_names.append(widget.get_name())
                continue
            """

            if not hasattr(widget, 'set_input_prefix'): 
                msg = DivWdg("Warning: The widget definition for [%s] uses [%s] and is not meant for use in Edit Layout. Please revise the edit_definition in widget config."% (widget.get_name(), widget.__class__.__name__ ))
                msg.add_style('color: orange')
                content_div.add(msg)
                content_div.add(HtmlElement.br())
                continue
                """
                raise TacticException('The widget definition for [%s] uses [%s] and is not meant for use in Edit. Please revise the definition in widget config'% (widget.__class__.__name__, widget.get_name()))
                """
            if my.input_prefix:
                widget.set_input_prefix(my.input_prefix)

           
            if isinstance(widget, HiddenWdg):
                content_div.add(widget)
                continue


            # Set up any validations configured on the widget ...
            from tactic.ui.app import ValidationUtil
            v_util = ValidationUtil( widget=widget )
            v_bvr = v_util.get_validation_bvr()
            if v_bvr:
                if (isinstance(widget, CalendarInputWdg)):
                    widget.set_validation( v_bvr.get('cbjs_validation'), v_bvr.get('validation_warning') );
                else:
                    widget.add_behavior( v_bvr )
                    widget.add_behavior( v_util.get_input_onchange_bvr() )
                  



            new_row = i % num_columns == 0
            if new_row:
                tr = table.add_row()
           
            show_title = (widget.get_option("show_title") != "false")
            if show_title:
                title = widget.get_title()

                td = table.add_cell(title)
                td.add_style("padding: 5px")
                td.add_style("vertical-align: top")

                security = Environment.get_security()
                if security.check_access("builtin", "view_site_admin", "allow"):
                    SmartMenu.assign_as_local_activator( td, 'HEADER_CTX' )

                td.add_color("background", "background", -12)
                td.add_style("width: 100px")

                td.add_color("border-color", "table_border", default="border")
                td.add_style("border-width: 1" )
                td.add_style("border-style: solid" )
 

            if not show_title:
                th, td = table.add_row_cell( widget )
                td.add_border()

                continue
            else:
                td = table.add_cell( widget )
                #td = table.add_cell( widget.get_value() )
                td.add_style("min-width: 300px")
                td.add_style("padding: 5px")
                td.add_style("vertical-align: top")

                td.add_color("border-color", "table_border", default="border")
                td.add_style("border-width: 1" )
                td.add_style("border-style: solid" )

                hint = widget.get_option("hint")
                if hint:
                    table.add_data( HintWdg(hint) ) 


            if i % 2 == 0:            
                td.add_color("background", "background")
            else:
                td.add_color("background", "background", -7)


        if not my.is_disabled and not my.mode == 'view':
            tr, td = table.add_row_cell( my.get_action_html() )
        
        if my.input_prefix:
            prefix = HiddenWdg("input_prefix", my.input_prefix)
            tr, td = table.add_row_cell()
            td.add(prefix)

        top_div.add(content_div) 
        return top_div

    
    def get_header_context_menu(my):

        menu = Menu(width=180)
        menu.set_allow_icons(False)
        menu.set_setup_cbfn( 'spt.dg_table.smenu_ctx.setup_cbk' )

        menu_item = MenuItem(type='title', label='Actions')
        menu.add(menu_item)


        menu_item = MenuItem(type='action', label='Edit Column Definition')
        menu_item.add_behavior( {
            'args' : {
                'search_type': my.search_type,
                'options': {
                    'class_name': 'tactic.ui.manager.ElementDefinitionWdg',
                    'popup_id': 'edit_column_defn_wdg',
                    'title': 'Edit Column Definition'
                }
            },
            'cbjs_action': '''
            spt.alert("Not yet implemented");
            return


            var activator = spt.smenu.get_activator(bvr);
            bvr.args.element_name = activator.getProperty("spt_element_name");
            bvr.args.view = activator.getAttribute('spt_view');
            var popup = spt.popup.get_widget(evt,bvr);
            popup.activator = activator;
            '''
        } )
        menu.add(menu_item)


        return menu



    def add_header(my, table, sobj_title):
        title_str = my.kwargs.get("title")

        if not title_str:
            if my.mode == 'insert':
                action = 'Add New Item'
            elif my.mode == 'edit':
                action = 'Save Changes'
            else:
                action = my.mode
            
            title_str =  action.capitalize() + " to " + sobj_title
            if my.mode == 'edit':
                title_str = '%s (%s)' %(title_str, my.sobjects[0].get_code())
            

        th = table.add_header()
        
        title_div = DivWdg()
        title_div.set_attr('title', my.view)
        th.add(title_div)
        title_div.add(title_str)
        th.add_gradient("background", "background3", -10)
        #th.add_border()
        th.add_color("border-color", "table_border", default="border")
        th.add_style("border-width: 1px")
        th.add_style("border-style: solid")
        th.set_attr("colspan", "2")
        th.add_style("height: 30px")


    def add_hidden_inputs(my, div):
        '''TODO: docs ... what is this for???'''
        pass


    def do_search(my):
        '''this widget has its own search mechanism'''

        web = WebContainer.get_web()
        
        # get the sobject that is to be edited
        id = my.search_id

        # if no id is given, then create a new one for insert
        search = None
        sobject = None
        search_type_base = SearchType.get(my.search_type).get_base_key()
        if my.mode == "insert":
            sobject = SearchType.create(my.search_type)
            my.current_id = -1
            # prefilling default values if available
            value_keys = web.get_form_keys()
            if value_keys:
                
                for key in value_keys:
                    value = web.get_form_value(key)
                    sobject.set_value(key, value)
        else:
            search = Search(my.search_type)

            # figure out which id to search for
            if web.get_form_value("do_edit") == "Edit/Next":
                search_ids = web.get_form_value("%s_search_ids" %search_type_base)
                if search_ids == "":
                    my.current_id = id
                else:
                    search_ids = search_ids.split("|")
                    next = search_ids.index(str(id)) + 1
                    if next == len(search_ids):
                        next = 0
                    my.current_id = search_ids[next]

                    last_search = Search(my.search_type)
                    last_search.add_id_filter( id )
                    my.last_sobject = last_search.get_sobject()

            else:
                my.current_id = id

            search.add_id_filter( my.current_id )
            sobject = search.get_sobject()

        if not sobject and my.current_id != -1:
            raise EditException("No SObject found")

        # set all of the widgets to contain this sobject
        my.set_sobjects( [sobject], search )


    def get_action_html(my):


        search_key = SearchKey.get_by_sobject(my.sobjects[0])
        search_type = my.sobjects[0].get_base_search_type()


        div = DivWdg(css='centered')
        div.add_behavior( {
            'type': 'load',
            'cbjs_action': my.get_onload_js(my.order_code)
        } )

 
        div.add_styles('height: 35px; margin-top: 5px;')
        div.add_named_listener('close_CustomPipeEditWdg', '''
            var popup = spt.popup.get_popup( $('edit_popup') );
            if (popup != null) {
                spt.popup.destroy(popup);
            }
            ''')

     
        # custom callbacks
        cbjs_cancel = my.kwargs.get('cbjs_cancel')
        if not cbjs_cancel:
            cbjs_cancel = '''
            spt.named_events.fire_event('preclose_edit_popup', {});
            spt.named_events.fire_event('close_CustomPipeEditWdg', {})
            '''

        # custom callbacks
        cbjs_insert_path = my.kwargs.get('cbjs_%s_path' % my.mode)
        cbjs_insert = None
        if cbjs_insert_path:
            script_obj = CustomScript.get_by_path(cbjs_insert_path)
            if script_obj:
                cbjs_insert = script_obj.get_value("script")

        # get it inline
        if not cbjs_insert:
            cbjs_insert = my.kwargs.get('cbjs_%s' % my.mode)

        # use a default
        if not cbjs_insert:
            mode_label = my.mode.capitalize()
            cbjs_insert = '''
            //spt.app_busy.show("%sing items", "");
            spt.edit.edit_form_cbk(evt, bvr);
            //spt.app_busy.hide();
            '''%mode_label

        save_event = my.kwargs.get('save_event')
        if not save_event:
            save_event = div.get_unique_event("save")

        element_names = my.element_names[:]
        for element_name in my.skipped_element_names:
            element_names.remove(element_name)

        bvr =  {
            'type': 'click_up',
            'mode': my.mode,
            'save_event': save_event,
            'cbjs_action': cbjs_insert,
         
            'named_event': 'edit_pressed',
            'element_names': element_names,
            'search_key': search_key,
            'input_prefix': my.input_prefix,
            'view': my.view
        }
        if my.mode == 'insert':
            bvr['refresh'] = 'true'
            # for adding parent relationship in EditCmd
            if my.parent_key:
                bvr['parent_key'] = my.parent_key
        
        ok_btn_label = my.mode.capitalize()
        if ok_btn_label == 'Edit':
            ok_btn_label = 'Save'
        if ok_btn_label == 'Insert':
            ok_btn_label = 'Add'

        if my.kwargs.get('ok_btn_label'):
            ok_btn_label = my.kwargs.get('ok_btn_label')

        ok_btn_tip = ok_btn_label
        if my.kwargs.get('ok_btn_tip'):
            ok_btn_tip = my.kwargs.get('ok_btn_tip')


        cancel_btn_label = 'Cancel'
        if my.kwargs.get('cancel_btn_label'):
            cancel_btn_label = my.kwargs.get('cancel_btn_label')

        cancel_btn_tip = cancel_btn_label
        if my.kwargs.get('cancel_btn_tip'):
            cancel_btn_tip = my.kwargs.get('cancel_btn_tip')


        # create the buttons
        insert_button = ActionButtonWdg(title=ok_btn_label, tip=ok_btn_tip)
        insert_button.add_behavior(bvr)



        cancel_button = ActionButtonWdg(title=cancel_btn_label, tip=cancel_btn_tip)
        cancel_button.add_behavior({
        'type': 'click_up',
        'cbjs_action': cbjs_cancel
        })

        table = Table()
        table.add_style("margin-left: auto")
        table.add_style("margin-right: auto")
        table.add_row()
        table.add_cell(insert_button)
        table.add_cell(cancel_button)
        div.add(table)


        #div.add(SpanWdg(edit, css='med'))
        #div.add(SpanWdg(edit_close, css='med'))
        #div.add(SpanWdg(cancel, css='med'))

        return div


    def get_default_display_handler(cls, element_name):
        # This is handlerd in get_default_display_wdg
        return None
    get_default_display_handler = classmethod(get_default_display_handler)


    def get_default_display_wdg(cls, element_name, display_options, element_type, kbd_handler=False):
        from pyasm.widget import TextAreaWdg, CheckboxWdg, SelectWdg, TextWdg
        if element_type == 'int(11)':
            dsffas

        if element_type in ["integer", "smallint", "bigint", "int"]:
            behavior = {
                'type': 'keyboard',
                'kbd_handler_name': 'DgTableIntegerTextEdit'
            }
            input = TextWdg("main")
            input.set_options(display_options)
            if kbd_handler:
                input.add_behavior(behavior)

        elif element_type in ["float"]:
            behavior = {
                'type': 'keyboard',
                'kbd_handler_name': 'DgTableFloatTextEdit'
            }
            input = TextAreaWdg("main")
            input.set_options(display_options)
            if kbd_handler:
                input.add_behavior(behavior)

        elif element_type in ["string", "link", "varchar", "character", "timecode"]:
            behavior = {
                'type': 'keyboard',
                'kbd_handler_name': 'DgTableMultiLineTextEdit'
            }
            input = TextWdg('main')
            input.set_options(display_options)
            if kbd_handler:
                input.add_behavior(behavior)


        elif element_type in ["text"]:
            behavior = {
                'type': 'keyboard',
                'kbd_handler_name': 'DgTableMultiLineTextEdit'
            }
            input = TextAreaWdg('main')
            input.set_options(display_options)
            if kbd_handler:
                input.add_behavior(behavior)

        elif element_type == "boolean":
            input = CheckboxWdg('main')
            input.set_options(display_options)

        elif element_type in  ["timestamp", "date", "time", "datetime2"]:
            from tactic.ui.widget import CalendarInputWdg, CalendarWdg, TimeInputWdg
            # FIXME: take wild guess for the time
            if element_name.endswith("_time"):
                behavior = {
                    'type': 'keyboard',
                    'kbd_handler_name': 'DgTableMultiLineTextEdit'
                }
                input = TextWdg('main')
                input.set_options(display_options)
                if kbd_handler:
                    input.add_behavior(behavior)

            else:
                input = CalendarInputWdg()
                input.set_option('show_activator', False)

        elif element_type == 'datetime':
            #3.9 from tactic.ui.widget import CalendarTimeInputWdg
            #3.9 input = CalendarTimeInputWdg()
            from tactic.ui.widget import CalendarTimeWdg
            input = CalendarTimeWdg()
            input.set_option('show_activator', False)

        elif element_type == "color":
            from tactic.ui.widget import ColorInputWdg
            input = ColorInputWdg()
            input.set_options(display_options)

        else:
            # else try to instantiate it as a class
            print "WARNING: Could not instantiate [%s]" %element_type
            input = TextWdg()
            input.add("No input defined")

        return input 
    get_default_display_wdg = classmethod(get_default_display_wdg)



    def get_onload_js(my, order_code):
    #nodes = spt.pipeline.get_nodes_by_group(); 
        return r'''

spt.edit = {}

// Called when the form is submitted
//
spt.edit.edit_form_cbk = function( evt, bvr )
{
    //alert('in get onload js');
    var order_code = '%s';
    // first fire a named event
    var named_event = bvr.named_event;
    spt.named_events.fire_event(named_event, bvr);
    var content = bvr.src_el.getParent(".spt_edit_top");
    if (content == null) {
        content = bvr.src_el.getParent(".spt_popup_content");
    }

    var values = spt.api.Utility.get_input_values(content, null, true, false, {cb_boolean: true});
    var server = TacticServerStub.get();
    var order_sk = server.build_search_key('twog/order', order_code);
    var top_el = document.getElementsByClassName('twog_order_builder_' + order_sk)[0];
    var classification = top_el.get('classification');
    var is_master = false;
    if(classification == 'master' || classification == 'Master'){
        is_master = true;
    }
    //var class_name = "pyasm.command.EditCmd";
    var class_name = "tactic.ui.panel.EditCmd";
    var args = {};

    args['element_names'] = bvr.element_names;
    args['search_key'] = bvr.search_key;
    if (bvr.parent_key)
        args['parent_key'] = bvr.parent_key;
    args['input_prefix'] = bvr.input_prefix;
    args['view'] = bvr.view;
    nodes = spt.pipeline.get_all_nodes();
    desc_dict = {};
    if(is_master){
        desc_dict['is_master'] = 'True';
    }
    for (var i=0; i<nodes.length; i++) {
        var name = spt.pipeline.get_node_name(nodes[i]);
        var desc = spt.pipeline.get_node_property(nodes[i], 'description');
        if(desc == 'undefined' || desc == 'NULL' || desc == null){
            desc = 'No Description';
            //new_desc = prompt('Please enter the Description for ' + name);
            //if(new_desc != ''){
            //    desc = new_desc;
            //}
        }
        desc_dict[name] = spt.pipeline.kill_bad_chars(desc);
    }

    // this is needed as bvr turns null on error
    var src_el = bvr.src_el;
    try {

        var info = server.execute_cmd(class_name, args, values);

        // add a callback after save
        var popup = bvr.src_el.getParent(".spt_popup");
        if (popup && popup.on_save_cbk ) {
            popup.on_save_cbk();
        }

        if (bvr.refresh == "true") {
            //refresh the panel above content
            var panel = spt.get_parent(content,'.spt_panel');
            if (panel) spt.panel.refresh(panel);
        }
        else {
        }
        spt.named_events.fire_event('close_CustomPipeEditWdg', {});
        // refresh the row
        if (bvr.mode == 'edit') {
            update_event = "update|" + bvr.search_key;
            
            spt.named_events.fire_event(update_event, {});
            // for fast table
            tmps = spt.split_search_key(bvr.search_key)
            update_st_event = "update|" + tmps[0];
            var bvr_fire = {};
            //var input = {'search_key': bvr.search_key };
            var input = {'search_key': bvr.search_key, 'desc_dict': desc_dict };
            bvr_fire.options = input;
            spt.named_events.fire_event(update_st_event, bvr_fire);


        }
        else {
            // update the table
            if (bvr.save_event) {
                spt.named_events.fire_event(bvr.save_event, bvr);
            }
        }
        var topper = '';
        var toppers = document.getElementsByClassName('twog_order_builder');
        for(var x = 0; x < toppers.length; x++){
            if(toppers[x].getAttribute('order_code') == order_code){
                topper  = toppers[x];
            }
        }
        var focus_name = topper.getAttribute('pipefocus_name');
        //var focus_name = topper.get('pipefocus_name');
        var cb_code = values['edit|code']; 
        var cb_xml = values['edit|pipeline'];
        var cb_color = values['edit|color'];
        var cb_sk = server.build_search_key('sthpw/pipeline', cb_code);


        if(cb_xml != null && cb_xml != ''){
            spt.app_busy.show('Saving Pipeline ' + cb_code ,'Attaching Pipeline to ' + focus_name + '...'); 
            try { // I added this crap. Stole from another function, above
                var args = {search_key: cb_sk, pipeline:cb_xml, color:cb_color, project_code: bvr.project_code, desc_dict: desc_dict};
                //server.execute_cmd('tactic.ui.tools.PipelineSaveCbk', args);
                server.execute_cmd('order_builder.CustomPipelineSaveCbk', args);
            } catch(e) {
                spt.alert(spt.exception.handler(e));
            }
            // The following code also exists in the 'else' portion of the generic save function for the pipeline editor, so saves of pipelines will save the pipeline code on the dude that launched the pipeline editor
            pipes_expr = "@SOBJECT(sthpw/pipeline['@ORDER_BY','timestamp desc'])";
            pipes = server.eval(pipes_expr);
            var same_pipe_code = pipes[0]['code'];
            var sob_sk = topper.getAttribute('pipefocus_sob_sk');
            //var sob_sk = topper.get('pipefocus_sob_sk');
            var sob_code = sob_sk.split('code=')[1];
            var class_type = topper.getAttribute('pipefocus_class_type');
            //var class_type = topper.get('pipefocus_class_type');
            var reload_cell = topper.getElementsByClassName('cell_' + sob_sk)[0];
            server.update(sob_sk, {'pipeline_code': same_pipe_code});
            spt.api.load_panel(reload_cell, 'order_builder.' + class_type, {sk: sob_sk, parent_sk: reload_cell.getAttribute('parent_sk'), order_sk: reload_cell.getAttribute('order_sk'), parent_sid: reload_cell.getAttribute('parent_sid'), allowed_titles: top_el.getAttribute('allowed_titles'), display_mode: top_el.getAttribute('display_mode'), classification: top_el.getAttribute('classification')});
            var bot = topper.getElementsByClassName('bot_' + sob_sk)[0];
            bot.style.display = 'table-row';
            spt.app_busy.hide();
        }
    }
    catch(e) {
        var ok = function() {};
        var cancel = function(bvr){

            if( spt.validation.has_invalid_entries( src_el, ".spt_edit_top" ) ){
                //alert('leaving get onload js - invalid entries part');
                return;
            }
            spt.named_events.fire_event('close_CustomPipeEditWdg', {});
           
        };

        var options = {}
        options.cancel_args = bvr;
           
        spt.confirm( "Error: " + spt.exception.handler(e) + "<br>Try again?", ok, cancel, options);
    }
    //alert('leaving get onload js');
    //alert('info = ' + info);
    return info;

}

        ''' % order_code


from pyasm.command import Command
class CustomPipelineSaveCbk(Command):
    '''Callback executed when the Save button or other Save menu items are pressed in Project Workflow'''
    def get_title(my):
        return "Save a pipeline"

    def execute(my):
        pipeline_sk = my.kwargs.get('search_key')

        pipeline_xml = my.kwargs.get('pipeline')
        if pipeline_xml in [None,'']:
            return ''
        pipeline_color = my.kwargs.get('color')
        project_code = my.kwargs.get('project_code')
        desc_dict = my.kwargs.get('desc_dict')
        is_master_str = desc_dict.get('is_master')
        is_master = False
        if is_master_str == 'true':
            is_master = True
        if pipeline_color in [None,'']:
            pipeline_color = '#dbdbdb'
        server = TacticServerStub.get(protocol='local')
        data =  {'pipeline':pipeline_xml, 'color':pipeline_color}
        if project_code:
            # force a pipeline to become site-wide
            if project_code == '__SITE_WIDE__':
                project_code = ''
            data['project_code'] = project_code
        server.insert_update(pipeline_sk, data = data)
        Pipeline.clear_cache(search_key=pipeline_sk)
        pipeline = SearchKey.get_by_search_key(pipeline_sk)
        pipeline_code = pipeline.get_code()

        # make sure to update process table
        process_names = pipeline.get_process_names()
        search = Search("config/process")
        search.add_filter("pipeline_code", pipeline_code)
        process_sobjs = search.get_sobjects()
        existing_names = SObject.get_values(process_sobjs, 'process')
        pipeline.on_insert()
        
        my.description = "Updated pipeline [%s]" % pipeline_code
        """ 
        count = 0
        for process_name in process_names:

            exists = False
            for process_sobj in process_sobjs:
                process_sobj.delete() #MTM ESTA BUENO
                # if it already exist, then update
                if process_sobj.get_value("process") == process_name:
                    exists = True
                    break
            if not exists:
                process_sobj = SearchType.create("config/process")
                process_sobj.set_value("pipeline_code", pipeline_code)
                process_sobj.set_value("process", process_name)
                #Here set desc
                process_sobj.set_value("description", desc_dict[process_name])
            
            attrs = pipeline.get_process_attrs(process_name)
            color = attrs.get('color')
            if color:
                process_sobj.set_value("color", color)

            process_sobj.set_value("sort_order", count)
            process_sobj.commit()
            count += 1


        # delete obsolete
        obsolete = set(existing_names) - set(process_names)
        if obsolete:
            for obsolete_name in obsolete:
                for process_sobj in process_sobjs:
                    # delete it
                    if process_sobj.get_value("process") == obsolete_name:
                        process_sobj.delete()
                        break
        """






