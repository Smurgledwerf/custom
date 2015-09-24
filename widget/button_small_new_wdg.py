"""
Custom button that's smaller than the default. I have no idea why the size
is hard-coded instead of being a variable or keyword argument.
"""

__author__ = 'topher.hughes'
__date__ = '24/09/2015'

from pyasm.web import DivWdg, WebContainer
from pyasm.widget import IconWdg
from tactic.ui.widget import ButtonNewWdg, IconButtonWdg

BASE = '/context/themes2'


class ButtonSmallNewWdg(ButtonNewWdg):
    """
    Functions just like the default, but is smaller.
    """

    ARGS_KEYS = {
        'tip': 'The tool tip of the button',
        'title': 'The title of the button',
        'show_menu': 'True|False - determines whether or not to show the menu',
        'show_title': 'True|False - determines whether or not to show the title',
    }

    def init(self):
        """
        The special tactic init function.

        :return: None
        """
        self.dialog = None
        self.button = DivWdg()
        self.hit_wdg = DivWdg()
        self.arrow_div = DivWdg()
        self.arrow_menu = IconButtonWdg(title="More Options", icon=IconWdg.ARROWHEAD_DARK_DOWN)
        self.show_arrow_menu = False
        # for icon decoration
        self.icon_div = DivWdg()
        self.is_disabled = self.kwargs.get("is_disabled") in [True, "true"]

    def get_display(self):
        """
        Handles how the widget will be displayed.

        :return: a button widget
        """
        top = self.top
        top.add_style("white-space: nowrap")

        base = "{0}/{1}".format(BASE, self.top.get_theme())

        button = DivWdg()
        button.add_style("float: left")

        self.inner = button
        top.add(button)
        self.inner.add_class("hand")

        button.add_class("spt_button_top")
        button.add_style("position: relative")

        img_div = DivWdg()
        button.add(img_div)
        img_div.add_style("width: 20px")
        img_div.add_style("height: 20px")

        over_div = DivWdg()
        button.add(over_div)
        over_div.add_class("spt_button_over")
        over_img = "<img src='{0}/SmallButton_over.png'/>".format(base)
        over_div.add(over_img)
        over_div.add_style("position: absolute")
        over_div.add_style("top: -7px")
        over_div.add_style("left: -2px")
        over_div.add_style("display: none")

        click_div = DivWdg()
        button.add(click_div)
        click_div.add_class("spt_button_click")
        click_img = "<img src='{0}/SmallButton_click.png'/>".format(base)
        click_div.add(click_img)
        click_div.add_style("position: absolute")
        click_div.add_style("top: -7px")
        click_div.add_style("left: -2px")
        click_div.add_style("display: none")

        title = self.kwargs.get("title")
        tip = self.kwargs.get("tip")
        if not tip:
            tip = title

        icon_div = self.icon_div
        button.add(icon_div)
        icon_str = self.kwargs.get("icon")
        icon = IconWdg(tip, icon_str, right_margin=0)
        icon.add_class("spt_button_icon")
        icon_div.add(icon)
        icon_div.add_style("position: absolute")
        icon_div.add_style("top: 2px")
        icon_div.add_style("left: 2px")

        if self.is_disabled:
            icon_div.add_style("opacity: 0.5")

        self.icon_div = icon_div

        self.show_arrow = self.kwargs.get("show_arrow") in [True, 'true']
        if self.show_arrow or self.dialog:
            arrow_div = DivWdg()
            button.add(arrow_div)
            arrow_div.add_style("position: absolute")
            arrow_div.add_style("top: 24px")
            arrow_div.add_style("left: 20px")

            arrow = IconWdg(tip, IconWdg.ARROW_MORE_INFO)
            arrow_div.add(arrow)

        web = WebContainer.get_web()
        is_ie = web.is_IE()

        self.hit_wdg.add_style("width: 100%")
        if is_ie:
            self.hit_wdg.add_style("filter: alpha(opacity=0)")
            self.hit_wdg.add_style("height: 40px")
        else:
            self.hit_wdg.add_style("height: 100%")
            self.hit_wdg.add_style("opacity: 0.0")

        if self.is_disabled:
            self.hit_wdg.add_style("display: none")

        button.add(self.hit_wdg)

        self.hit_wdg.add_style("position: absolute")
        self.hit_wdg.add_style("top: 0px")
        self.hit_wdg.add_style("left: 0px")
        self.hit_wdg.add_attr("title", tip)
        self.hit_wdg.add_behavior({
            'type': 'hover',
            'cbjs_action_over': '''
                var top = bvr.src_el.getParent(".spt_button_top")
                var over = top.getElement(".spt_button_over");
                var click = top.getElement(".spt_button_click");
                over.setStyle("display", "");
                click.setStyle("display", "none");
            ''',
            'cbjs_action_out': '''
                var top = bvr.src_el.getParent(".spt_button_top")
                var over = top.getElement(".spt_button_over");
                var click = top.getElement(".spt_button_click");
                over.setStyle("display", "none");
                click.setStyle("display", "none");
            '''
            })

        self.hit_wdg.add_behavior({
            'type': 'click',
            'cbjs_action': '''
                var top = bvr.src_el.getParent(".spt_button_top")
                var over = top.getElement(".spt_button_over");
                var click = top.getElement(".spt_button_click");
                over.setStyle("display", "none");
                click.setStyle("display", "");
            '''
            })
        self.hit_wdg.add_behavior({
            'type': 'click_up',
            'cbjs_action': '''
                var top = bvr.src_el.getParent(".spt_button_top")
                var over = top.getElement(".spt_button_over");
                var click = top.getElement(".spt_button_click");
                over.setStyle("display", "");
                click.setStyle("display", "none");
            '''
            })

        # add a second arrow widget
        if self.show_arrow_menu:
            self.inner.add(self.arrow_div)
            self.arrow_div.add_attr("title", "More Options")
            self.arrow_div.add_style("position: absolute")
            self.arrow_div.add_style("top: 11px")
            self.arrow_div.add_style("left: 20px")
            self.arrow_div.add(self.arrow_menu)

        if self.dialog:
            top.add(self.dialog)
            dialog_id = self.dialog.get_id()
            self.hit_wdg.add_behavior({
                'type': 'click_up',
                'dialog_id': dialog_id,
                'cbjs_action': '''
                    var dialog = $(bvr.dialog_id);
                    var pos = bvr.src_el.getPosition();
                    var size = bvr.src_el.getSize();
                    //var dialog = $(bvr.dialog_id);
                    dialog.setStyle("left", pos.x);
                    dialog.setStyle("top", pos.y+size.y);
                    spt.toggle_show_hide(dialog);
                '''
                })

        return top
