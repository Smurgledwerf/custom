###########################################################
#
# Copyright (c) 2005, Southpaw Technology
#                     All Rights Reserved
#
# PROPRIETARY INFORMATION.  This software is proprietary to
# Southpaw Technology, and is not to be reproduced, transmitted,
# or disclosed in any way without written permission.
#
#
#
__all__ = ['OrderEntryWdg', "MovementSelectWdg"]

from pyasm.common import Environment, TacticException, Common
from pyasm.search import Search, SearchKey
from pyasm.web import *
from pyasm.biz import *   # Project is part of pyasm.biz
from pyasm.widget import ThumbWdg, SelectWdg, ButtonWdg, TextWdg, CheckboxWdg, IconWdg, HiddenWdg, TableWdg


from tactic.ui.common import BaseRefreshWdg
from tactic.ui.container import PopupWdg, RoundedCornerDivWdg
from tactic.ui.popups import HelpPopupWdg, ActionBarWdg
from tactic.ui.widget import PageHeaderGearMenuWdg, TextBtnWdg, ActionButtonWdg

from tactic.ui.panel import EditWdg, FastTableLayoutWdg


class OrderEntryWdg(BaseRefreshWdg):

    def get_display(my):
        top = DivWdg()
     
        top.add_style("width: 100%")
        top.add_color("background", "background", -10)
        top.add_style("padding-top: 30px")
        top.add_style("padding-bottom: 50px")
        top.add_class("twog_wizard_top")

        inner = DivWdg()
        top.add(inner)

        # set the width and height here
        inner.add_style("width: 800px")
        inner.add_style("min-height: 600px")
        inner.add_style("float: center")
        inner.add_border()
        inner.center()
        inner.add_style("padding: 20px")
        inner.add_color("background", "background")


        from tactic.ui.container import WizardWdg


        title = DivWdg()
        title.add("Step 1")

        wizard = WizardWdg(title=title)
        my.wizard = wizard
        inner.add(wizard)


        help_button = ActionButtonWdg(title="?", tip="Step 1 Help", size='s')
        title.add(help_button)
        help_button.add_style("float: right")
        help_button.add_style("margin-top: -20px")
        help_button.add_style("margin-right: -10px")
        help_button.add_behavior({
            'type': 'click_up',
            'cbjs_action': '''
            spt.help.set_top();
            spt.help.load_alias("order_wdg");
            '''
        })

        page_one = my.get_page_one()
        wizard.add(page_one, 'Step 1')
        page_two = my.get_page_two()
        wizard.add(page_two, 'Step 2')
        page_three = my.get_page_three()
        wizard.add(page_three, 'Step 3')
        page_four = my.get_page_four()
        wizard.add(page_four, 'Step 4')


        return top

    def get_page_one(my):

        info_page = DivWdg()
        
        #info_page.add_class("spt_project_top")
        info_page.add_style("font-size: 12px")
        info_page.add_color("background", "background")
        info_page.add_color("color", "color")
        info_page.add_style("padding: 20px")



        from tactic.ui.input import TextInputWdg

        info_page.add("<b>Title:</b> &nbsp;&nbsp;")
    
        text = TextWdg("order_title")
        #text = TextInputWdg(title="project_title")
        info_page.add(text)
        text.add_style("width: 250px")
        info_page.add(HtmlElement.br(3))
        span = DivWdg()
        info_page.add(span)
        span.add_style("padding: 20px 20px 20px 20px")
        span.add(IconWdg("INFO", IconWdg.CREATE))
        span.add_color("background", "background3")
        span.add("The order title can be descriptive and contain spaces and special characters.")
        info_page.add("<br/><br/><hr/><br/><br/>")
        text.add_behavior( {
        'type': 'change',
        'cbjs_action': '''
        var title = bvr.src_el.value;
        var code = spt.convert_to_alpha_numeric(title);
        var top = bvr.src_el.getParent(".twog_wizard_top");
        var code_el = top.getElement(".spt_project_code");
        code_el.value = code;
        '''
        } )


        info_page.add("<b>Client Name: &nbsp;&nbsp;</b>")
        text = TextWdg("client_name")
        text.add_style("width: 250px")
        text.add_class("spt_client_name")
        info_page.add(text)

        # line breaks
        info_page.add(HtmlElement.br(2))

        info_page.add("<b>Special code: &nbsp;&nbsp;</b>")
        text = TextWdg("special code")
        text.add_style("width: 250px")

        # this is just meant for DOM element search covenience
        text.add_class("spt_special_code")

       
        # this behavior is go for eliminlating special symbols
        #MTM this will help get rid of the stupid ascii errors
        text.add_behavior( {
            'type': 'blur',
            'cbjs_action': '''
            var value = bvr.src_el.value;
            var code = spt.convert_to_alpha_numeric(value);
            bvr.src_el.value = code;
            '''
        } )

        info_page.add(text)

        
        info_page.add(HtmlElement.br(4))

        span = DivWdg()
        info_page.add(span)
        span.add_style("padding: 20px 20px 20px 20px")
        span.add(IconWdg("INFO", IconWdg.CREATE))
        span.add_color("background", "background3")
        span.add("Some more info here.")
     
        info_page.add(span)

        info_page.add("<br/>")


        return info_page

    def get_page_two(my):
        '''let's browse an optional image here'''
        info_page = DivWdg()
        # add an icon for this project
        image_div = DivWdg()
        
        image_div.add_class("spt_image_top")
        image_div.add_color("background", "background")
        image_div.add_color("color", "color")
        image_div.add_style("padding: 20px")


        image_div.add(HtmlElement.b("Order Image:"))
        image_div.add("<br/>"*3)
        button = ActionButtonWdg(title="Browse")
        image_div.add(button)
        button.add_style("margin-left: auto")
        button.add_style("margin-right: auto")
        button.add_behavior( {
        'type': 'click_up',
        'cbjs_action': '''
        var applet = spt.Applet.get();
        spt.app_busy.show("Browsing for order image");
        var path = applet.open_file_browser();

        var top = bvr.src_el.getParent(".spt_image_top");
        var text = top.getElement(".spt_image_path");
        var display = top.getElement(".spt_path_display");
        var check_icon = top.getElement(".spt_check_icon");

        text.value = path;

        applet.upload_file(path);


        display.innerHTML = "Uploaded: " + path;
        display.setStyle("padding", "10px");
        check_icon.setStyle("display", "");


        path = path + "";
        /*
        path = path.replace(/\\\\/g, "/");
        var parts = path.split("/");
        var filename = parts[parts.length-1];
        */
        var filename = spt.path.get_basename(path);
        filename = spt.path.get_filesystem_name(filename);
        var server = TacticServerStub.get();
        var kwargs = {
            filename: filename
        }
        try {
            var ret_val = server.execute_cmd("tactic.command.CopyFileToAssetTempCmd", kwargs);
            var info = ret_val.info;
            var path = info.path;

            display.innerHTML = display.innerHTML + "<br/><br/><div style='text-align: center'><img style='width: 80px;' src='"+path+"'/></div>";

        }
        catch(e) {
            spt.alert(spt.exception.handler(e));
        }
        spt.app_busy.hide();

        '''
        } )

        text = HiddenWdg("order_image_path")
        text.add_class("spt_image_path")
        image_div.add(text)

        check_div = DivWdg()
        image_div.add(check_div)
        check_div.add_class("spt_check_icon")
        check_icon = IconWdg("Image uploaded", IconWdg.CHECK)
        check_div.add(check_icon)
        check_div.add_style("display: none")
        check_div.add_style("float: left")
        check_div.add_style("padding-top: 8px")

        path_div = DivWdg()
        image_div.add(path_div)
        path_div.add_class("spt_path_display")

        image_div.add(HtmlElement.br(3))
        span = DivWdg()
        image_div.add(span)
        span.add_style("padding: 20px 20px 20px 20px")
        span.add_color("background", "background3")
        span.add(IconWdg("INFO", IconWdg.CREATE))
        span.add("This optional order image can be used in verious places as a visual representation of this order.")

        #info_page.add("<br/><br/>")
        return image_div


    def get_page_three(my):

        # draw a Movement insert page, followed by Add Tape and Add Physel at the bottom
        div = DivWdg()
        div.add_class('twog_order_top')
        edit_wdg = EditWdg(element_name='general', mode='insert', search_type='twog/movement',\
                title='Add Movement',view='insert', widget_key='edit_layout', cbjs_insert_path='movement/add_item')
        movement_div = edit_wdg

        div.add(movement_div)
        div.add(HtmlElement.br(2))
        add_div = DivWdg()
        add_div.add_class('move_add')
        div.add(add_div)
        table = Table()

        
        table.add_style('width','100%')
        add_div.add(table)
        
        table.add_row()

        select = MovementSelectWdg(name='movement_select')

       

        table.add_row_cell(select)

        table.add_row()
        td = table.add_cell('Add Tape(s)')
        td.add_style('width','300px')
        td = table.add_cell('Add Physel(s)')
        td.add_style('width','300px')
        table.add_row()
        text = TextWdg('add_tape')
        text.add_class('move_add_tape')
        text.add_style('float: left')
        td = table.add_cell(text)
        button = ActionButtonWdg(tip='add', title='+')
        
        bvr = {'type':'click_up',
                'cbjs_action': '''var parent = spt.api.get_parent(bvr.src_el, '.move_add');
                                 var text = spt.api.get_element(parent, '.move_add_tape');
                                 var movement_sel = spt.api.get_element(parent, '.twog_move_select');
                                 var server = TacticServerStub.get();
                                 try {
                                     if (!text.value) {
                                        spt.alert('Tape code is empty.');
                                        return;
                                     }
                                     else {
                                        var tape_sk = server.build_search_key('twog/tape', text.value);
                                        try {
                                        var tape = server.get_by_search_key(tape_sk);
                                        }
                                        catch(e) {
                                        // this above should raise an error already if it doesn't exist
                                        spt.error('This tape does not exist in the system.');
                                        return;
                                        }
                                     }
                                     if (!movement_sel.value) {
                                        spt.alert('You need to select a Movement.');
                                        return;
                                     }
                                
                                 
                                    server.insert('twog/asset_to_movement', {'tape_code':text.value,
                                        'movement_code':movement_sel.value});
                                 } catch(e) {
                                        spt.alert(spt.exception.handler(e));
                                 }'''}
        button.add_behavior(bvr)
        td.add(button)
        text = TextWdg('add_physel')
        text.add_style('float: left')
        td = table.add_cell(text)
        button = ActionButtonWdg(tip='add', title='+')
        button.add_behavior(bvr)
        td.add(button)

        div.add(HtmlElement.br(2))
        # finally add the asset_to_movement table layout
        association_div = DivWdg(HtmlElement.b('Assets in Movement'))
        div.add(association_div)
        div.add(HtmlElement.br())
        layout = FastTableLayoutWdg(search_type='twog/asset_to_movement', view='table')
        div.add(layout)

        return div

     

    def get_page_four(my):

        last_page = DivWdg()
        

        last_page.add_style("padding-top: 80px")
        last_page.add_style("padding-left: 30px")

        cb = CheckboxWdg('jump_to_tab', label='Jump to Tab')
        cb.set_checked()
        last_page.add(cb)
        last_page.add(HtmlElement.br(5))


        button_div = DivWdg()

        create_button = ActionButtonWdg(title="Create >>", tip="Create new project")
        my.wizard.add_submit_button(create_button)
        create_button.add_style("float: right")

        create_button.add_behavior({
        'type': "click_up",
        'cbjs_action': '''
            spt.alert('perform action here'); 
        '''


        })


        # you can even pass in a custom cacel_script like 
        # spt.info("You have cancelled")
        cancel_script = my.kwargs.get("cancel_script")
        if cancel_script:
            cancel_button = ActionButtonWdg(title="Cancel")
            cancel_button.add_style("float: left")

            cancel_button.add_behavior({
                'type': "click_up",
                'cbjs_action': cancel_script
            })

            button_div.add(cancel_button)

            create_button.add_style("margin-right: 15px")
            create_button.add_style("margin-left: 75px")


        button_div.add("<br clear='all'/>")

        last_page.add(button_div)
        return last_page

        #inner.add(HtmlElement.br())


   
class MovementSelectWdg(BaseRefreshWdg):

    def get_display(my):
       
        name = my.kwargs.get('name')
        select = SelectWdg(name)
        select.add_class('twog_move_select')
        select.set_option('empty','true')
        # limit to last 10
        select.set_options(my.kwargs)

        # if it's not set from kwargs, we have this default values/labels
        if not my.kwargs.get('values_expr'):
            select.set_option('values_expr', "@GET(twog/movement['@LIMIT','10']['@ORDER_BY','timestamp desc'].code)")
            select.set_option('labels_expr', "@GET(twog/movement['@LIMIT','10']['@ORDER_BY','timestamp desc'].code) + ':' + @GET(twog/movement['@LIMIT','10']['@ORDER_BY','timestamp desc'].name)")
        return select



 




