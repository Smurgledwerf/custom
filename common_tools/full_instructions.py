"""
This module handles the full instructions on an order. It will get all the instructions
from the order, titles, projects, and work orders and display them in a popup window.
There will also be a button to acknowledge that an operator has read the instructions.
When an order's instructions have been updated, the operators will be notified of the changes.
"""

# Figure out if the statement below is necessary
# __all__ = ['FullInstructionsLauncherWdg', 'FullOrderInstructionsWdg']
__author__ = 'topher.hughes'
__date__ = '21/09/2015'

from tactic_client_lib import TacticServerStub
from pyasm.web import Table, DivWdg
from tactic.ui.table import ButtonElementWdg
from tactic.ui.container import PopupWdg
from tactic.ui.common import BaseTableElementWdg, BaseRefreshWdg
from tactic.ui.widget import ActionButtonWdg

import common_tools.utils as ctu


class FullInstructionsLauncherWdg(ButtonElementWdg):
    """
    The button class that launches the popup window that shows the full instructions.
    """

    def init(self):
        """

        :return: None
        """
        super(FullInstructionsLauncherWdg, self).init()
        # noinspection PyAttributeOutsideInit
        self.server = TacticServerStub.get()

    def get_this_order(self, sobject):
        """

        :param sobject:
        :return:
        """
        sobject_type = ctu.get_sobject_type(sobject.get('__search_key__'))
        if sobject_type == 'order':
            return sobject

        order = self.server.query('twog/order', filters=[('code', sobject.get('order_code'))])
        if order:
            return order[0]

    def get_launch_behavior(self, order):
        """

        :param order:
        :return:
        """
        search_key = order.get('__search_key__')
        behavior = '''
        try{
            var class_name = 'common_tools.full_instructions.FullOrderInstructionsWdg';
            kwargs = {
                'search_key': {0}
            };
            spt.panel.load_popup('Full Instructions', class_name, kwargs);
        }
        catch(err){
            spt.app_busy.hide();
            spt.alert(spt.exception.handler(err));
        }
        '''
        # behavior = '''
        # var kwargs = bvr.kwargs;
        # kwargs['search_key'] = {0};
        #
        # spt.app_busy.show("Opening Check-In Widget...");
        #
        # // sobject specific data
        # var layout = bvr.src_el.getParent(".spt_tool_top");
        # if (layout != null) {
        #     var class_name = 'tactic.ui.widget.CheckinWdg';
        #     spt.app_busy.show("Loading ...");
        #     var layout = bvr.src_el.getParent(".spt_tool_top");
        #     var element = layout.getElement(".spt_tool_content");
        #     spt.panel.load(element, class_name, kwargs);
        #     spt.app_busy.hide();
        # }
        # else {
        #     var options=  {
        #         title: "Check-in Widget",
        #         class_name: 'tactic.ui.widget.CheckinWdg',
        #         popup_id: 'checkin_widget'
        #     };
        #     var bvr2 = {};
        #     bvr2.options = options;
        #     bvr2.args = kwargs;
        #     var table_layout = spt.table.get_layout();
        #     var popup = spt.popup.get_widget({}, bvr2);
        #     popup.layout = table_layout;
        #     spt.app_busy.hide();
        # }
        # '''
        return behavior.format(search_key)

    def get_display(self):
        """

        :return:
        """
        self.set_option('icon', "DOCUMENTATION")
        sobject = self.get_current_sobject()
        order = self.get_this_order(sobject)
        self.add_to_button_behavior('cbjs_action', self.get_launch_behavior(order))

        div = super(FullInstructionsLauncherWdg, self).get_display()
        return div


class FullOrderInstructionsWdg(BaseRefreshWdg):
    """
    A popup window that shows all the instructions for an order.
    Operators are required to read it before starting to work on it.
    """
    # TODO: fill out table styles
    TABLE_STYLES = {'order': {'width': '100%'},
                    'title': {'width': '100%'},
                    'proj': {'width': '100%'},
                    'work_order': {'width': '100%'},
                    }

    def init(self):
        """

        :return: None
        """
        super(FullOrderInstructionsWdg, self).init()
        # noinspection PyAttributeOutsideInit
        self.server = TacticServerStub.get()
        # noinspection PyAttributeOutsideInit
        self.gui = {}

    def get_this_order(self):
        """

        :return:
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
        for attr in ['name', 'title', 'process', 'code']:
            sobject_name = sobject.get(attr)
            if sobject_name:
                break
        instructions = sobject.get('instructions', '')

        table = Table(name=sobject_code)
        table.add_styles(self.TABLE_STYLES.get(sobject_type))
        self.gui[sobject_code] = table
        table.add_row()
        table.add_cell("<b><u>{0}: {1}</u></b>".format(sobject_type.replace('_', ' ').title(), sobject_name))
        if instructions:
            table.add_row()
            table.add_cell(instructions)

        parent_table.add_row()
        parent_table.add_cell(table)

    def get_full_instructions(self, order):
        """

        :param order:
        :return:
        """
        order_code = order.get('code')
        columns = ['code', 'instructions', 'title_code', 'proj_code', 'title', 'process']
        titles = self.server.query('twog/title', filters=[('order_code', order_code)], columns=columns)
        projects = self.server.query('twog/proj', filters=[('order_code', order_code)], columns=columns)
        work_orders = self.server.query('twog/work_order', filters=[('order_code', order_code)], columns=columns)

        # organize the instructions like an outline
        order_name = order.get('name')
        order_name = order_name if order_name else order.get('code')
        instructions = order.get('instructions')

        table = Table(name=order_code)
        table.add_styles(self.TABLE_STYLES.get('order'))
        self.gui[order_code] = table
        table.add_row()
        table.add_cell("<b><u>Order: {0}</u></b>".format(order_name))
        if instructions:
            table.add_row()
            table.add_cell(instructions)

        for title in titles:
            self.add_instructions(title)
        for project in projects:
            self.add_instructions(project)
        for work_order in work_orders:
            self.add_instructions(work_order)

        return table

        # create an ordered dictionary structure with {code: sobject} for each type
        # titles_dict = {}
        # for title in titles:
        #     titles_dict[title.get('code')] = title
        #
        # projects_dict = {}
        # for project in projects:
        #     projects_dict[project.get('code')] = project
        #
        # work_orders_dict = {}
        # for work_order in work_orders:
        #     work_orders_dict[work_order.get('code')] = work_order

        # for title_code, title in titles_dict.items():
        #     title_instructions = title.get('instructions')
        #     for project_code, project in projects_dict.items():
        #         if project.get('title_code') != title_code:
        #             continue
        #         project_instructions = project.get('instructions')
        #         for work_order_code, work_order in work_orders_dict.items():
        #             if work_order.get('proj_code') != project_code:
        #                 continue
        #             work_order_instructions = work_order.get('instructions')

    def get_accept_behavior(self, order):
        """

        :param order:
        :return:
        """
        return ''

    def get_display(self):
        """

        :return:
        """
        top = DivWdg()
        order = self.get_this_order()
        if not order:
            return top

        order_name = order.get('name')
        order_name = order_name if order_name else order.get('code')
        # self.add('Instructions for {0}'.format(order_name), name='title')

        table = Table()
        table.add_row()
        table.add_cell(self.get_full_instructions(order))
        accept_button = ActionButtonWdg(title='Accept')
        accept_button.add_behavior(self.get_accept_behavior(order))
        table.add_row()
        table.add_cell(accept_button)
        top.add_widget(table)

        # div = super(FullOrderInstructionsWdg, self).get_display()
        return top
