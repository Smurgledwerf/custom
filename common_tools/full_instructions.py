"""
This module handles the full instructions on an order. It will get all the instructions
from the order, titles, projects, and work orders and display them in a popup window.
There will also be a button to acknowledge that an operator has read the instructions.
When an order's instructions have been updated, the operators will be notified of the changes.
"""

# __all__ = ['FullInstructionsLauncherWdg', 'FullOrderInstructionsWdg']
__author__ = 'topher.hughes'
__date__ = '21/09/2015'

from tactic_client_lib import TacticServerStub
from pyasm.web import Table, DivWdg
from pyasm.widget import CheckboxWdg
from tactic.ui.common import BaseRefreshWdg, BaseTableElementWdg
from tactic.ui.container.pop_window_wdg import ResizeScrollWdg
from tactic.ui.widget import ActionButtonWdg

import common_tools.utils as ctu
from widget.button_small_new_wdg import ButtonSmallNewWdg


class FullInstructionsLauncherWdg(BaseTableElementWdg):
    """
    The button class that launches the popup window that shows the full instructions.
    """

    def init(self):
        """
        The special tactic init function.

        :return: None
        """
        super(FullInstructionsLauncherWdg, self).init()
        # noinspection PyAttributeOutsideInit
        self.server = TacticServerStub.get()

    def get_this_order(self):
        """
        Get the order that this should open the instructions for.
        If a search_key kwarg isn't provided, it will try to get the current sobject.
        A title, proj, or work order will automatically get the order instead.

        :return: an order sobject
        """
        search_key = self.kwargs.get('search_key')
        if search_key:
            sobject = self.server.get_by_search_key(search_key)
            search_type = sobject.get('__search_type__')
        else:
            # This should be when the sobject is grabbed from the table itself
            sobject = self.get_current_sobject()
            search_type = sobject.get_search_type()
        sobject_type = ctu.get_sobject_type(search_type)
        if sobject_type == 'order':
            return sobject

        order = self.server.query('twog/order', filters=[('code', sobject.get('order_code'))])
        if order:
            return order[0]

    def get_launch_behavior(self, order):
        """
        Get the behavior to launch the FullOrderInstructionsWdg

        :param order: the order sobject to open
        :return: a behavior dict
        """
        if isinstance(order, dict):
            search_key = order.get('__search_key__')
        else:
            # This should be when the sobject is grabbed from the table itself
            search_key = order.get_search_key()
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''
        try{
            var class_name = 'common_tools.full_instructions.FullOrderInstructionsWdg';
            kwargs = {
                'search_key': '%s'
            };
            spt.panel.load_popup('Full Instructions', class_name, kwargs);
        }
        catch(err){
            spt.app_busy.hide();
            spt.alert(spt.exception.handler(err));
        }
        ''' % search_key}
        # Normally I prefer the {0} format over %s, but it doesn't work with injected javascript
        return behavior

    def get_display(self):
        """
        Handle how the widget is displayed.

        :return: a widget containing a launch button
        """
        button = ButtonSmallNewWdg(title=self.kwargs.get('title'))
        button.set_option('icon', "DOCUMENTATION")
        order = self.get_this_order()
        button.add_behavior(self.get_launch_behavior(order))

        return button


class FullOrderInstructionsWdg(BaseRefreshWdg):
    """
    A popup window that shows all the instructions for an order.
    Operators are required to read it before starting to work on it.
    """
    COMMON_STYLE = {'width': '100%', 'border-collapse': 'separate', 'border-spacing': '10px 5px',
                    'border-bottom-right-radius': '10px', 'border-bottom-left-radius': '10px',
                    'border-top-right-radius': '10px', 'border-top-left-radius': '10px',
                    }
    TABLE_STYLES = {'order': {'background-color': '#d9edf7'},
                    'title': {'background-color': '#d9edcf'},
                    'proj': {'background-color': '#d9ed8b'},
                    'work_order': {'background-color': '#c6eda0'},
                    }

    def init(self):
        """
        The special tactic init function.

        :return: None
        """
        super(FullOrderInstructionsWdg, self).init()
        # noinspection PyAttributeOutsideInit
        self.server = TacticServerStub.get()
        # noinspection PyAttributeOutsideInit
        self.gui = {}

    def get_this_order(self):
        """
        Get the order that this should open the instructions for.
        If a search_key kwarg isn't provided, it will try to get the current sobject.
        A title, proj, or work order will automatically get the order instead.

        :return: an order sobject
        """
        search_key = self.kwargs.get('search_key')
        sobject = self.server.get_by_search_key(search_key)
        sobject_type = ctu.get_sobject_type(search_key)
        if sobject_type == 'order':
            return sobject

        order = self.server.query('twog/order', filters=[('code', sobject.get('order_code'))])
        if order:
            return order[0]

    def add_instructions(self, sobject):
        """
        Adds the sobject and it's instructions to the table. The sobject's type, name,
        and instructions will be added under it's parent sobject.

        :param sobject: the sobject to add to the table
        :return: None
        """
        parent_code = ''
        for attr in ['proj_code', 'title_code', 'order_code']:
            parent_code = sobject.get(attr)
            if parent_code:
                break

        parent_table = self.gui.get(parent_code)
        if not parent_table:
            return

        sobject_code = sobject.get('code')
        sobject_type = ctu.get_sobject_type(sobject.get('__search_key__'))
        sobject_name = ''
        for attr in ['name', 'process', 'title', 'code']:
            sobject_name = sobject.get(attr)
            if sobject_name:
                break
        instructions = sobject.get('instructions', '')
        if instructions:
            instructions = instructions.replace('\n', '<br>')

        container = Table()
        container.add_styles({'width': '100%'})
        self.gui[sobject_code] = container
        table = Table(name=sobject_code)
        table.add_styles(self.COMMON_STYLE)
        table.add_styles(self.TABLE_STYLES.get(sobject_type))
        table.add_row()
        table.add_cell("<b><u>{0}: {1}</u></b>".format(sobject_type.replace('_', ' ').title(), sobject_name))
        if instructions:
            table.add_row()
            table.add_cell(instructions)
        container.add_row()
        container.add_cell(table)

        div = DivWdg()
        div.add_styles({'padding-left': '20px'})
        div.add_widget(container)
        parent_table.add_row()
        parent_table.add_cell(div)

    def get_full_instructions(self, order):
        """
        Get all the instructions for this order, organized like an outline.

        :param order: an order sobject
        :return: a widget containing the instructions
        """
        order_code = order.get('code')
        columns = ['code', 'instructions', 'order_code', 'title_code', 'proj_code', 'title', 'process']
        titles = self.server.query('twog/title', filters=[('order_code', order_code)], columns=columns)
        projects = self.server.query('twog/proj', filters=[('order_code', order_code)],
                                     columns=columns, order_bys=['order_in_pipe asc'])
        work_orders = self.server.query('twog/work_order', filters=[('order_code', order_code)],
                                        columns=columns, order_bys=['order_in_pipe asc'])

        # organize the instructions like an outline
        order_name = order.get('name')
        order_name = order_name if order_name else order.get('code')
        instructions = order.get('instructions', '')
        if instructions:
            instructions = instructions.replace('\n', '<br>')

        container = Table()
        container.add_styles({'width': '100%'})
        self.gui[order_code] = container
        table = Table(name=order_code)
        table.add_styles(self.COMMON_STYLE)
        table.add_styles(self.TABLE_STYLES.get('order'))
        table.add_row()
        table.add_cell("<b><u>Order: {0}</u></b>".format(order_name))
        if instructions:
            table.add_row()
            instructions = table.add_cell(instructions)
            instructions.add_styles({'font-weight': 'bold', 'color': '#ff0000'})
        container.add_row()
        container.add_cell(table)

        for title in titles:
            self.add_instructions(title)
        for project in projects:
            self.add_instructions(project)
        for work_order in work_orders:
            self.add_instructions(work_order)

        return container

    def get_accept_behavior(self, order):
        """
        Get the behavior for 'accepting' the instructions. This should set them
        as acknowledged and allow the user to start working.

        :param order: an order sobject
        :return: a behavior dict
        """
        # TODO: make this 'accept' that the user read the instructions
        # This functionality is still up for discussion.
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''
        try{
            var popup = spt.popup.get_popup(bvr.src_el);
            spt.named_events.fire_event('preclose_' + popup.id, {});
            spt.popup.destroy(popup);
        }
        catch(err){
            spt.app_busy.hide();
            spt.alert(spt.exception.handler(err));
        }
        '''}
        return behavior

    def get_display(self):
        """
        Handle how the widget is displayed.

        :return: the top widget for the popup
        """
        top = DivWdg()
        order = self.get_this_order()
        if not order:
            return top

        scroll_wdg = ResizeScrollWdg(width=1000, height=800)
        table = Table()
        table.add_row()
        table.add_cell(self.get_full_instructions(order))
        table.add_row()

        bottom_row = Table()
        bottom_row.add_styles({'margin': '3px'})
        checkbox = CheckboxWdg("accept")
        checkbox.add_styles({'margin': '5px'})
        # bottom_row.add_cell(checkbox)
        # bottom_row.add_cell('I have read all the instructions for this order.')
        accept_button = ActionButtonWdg(title='Accept')
        accept_button.add_behavior(self.get_accept_behavior(order))
        bottom_row.add_cell(accept_button)

        cell = table.add_cell(bottom_row)
        cell.add_attr('align', 'center')
        scroll_wdg.add(table)
        top.add_widget(scroll_wdg)

        return top
