"""
A generic edit/view widget that will show details of an sobject. It uses the columns defined
in the 'edit' view, and the mode (view|edit) is determined by the users department. This was
originally created to use with the custom url, /sobject/{search_type}/{sobject_code} to make
it easier to edit linked sobjects.
"""

__author__ = 'topher.hughes'
__date__ = '09/10/2015'

from tactic_client_lib import TacticServerStub
from pyasm.common import Environment
from pyasm.web import DivWdg
from tactic.ui.common import BaseTableElementWdg
from tactic.ui.panel import CustomLayoutWdg, EditWdg

import common_tools.utils as ctu


class SobjectEditLauncherWdg(BaseTableElementWdg):
    """
    The widget that launches the sobject edit wdg. This shows up just as bold, underlined text,
    but will popup the edit window when clicked.
    """

    ARGS_KEYS = {
        'search_type': {
            'description': 'The search type of the sobject.',
        },
        'sobject_code': {
            'description': "The sobject's code.",
        },
        # I hoped the expression could be something like {@GET(twog/client.code)}
        # but I don't think an expression arg type actually exists.
        # This works by inserting the sobject_code_expression into an expression like
        # "@GET(twog/title['code','TITLE1337']{sobject_code_expression})"
        # where it would be something like '.twog/client.code'
        'sobject_code_expression': {
            'description': "An expression to get the sobject code.",
            'type': 'expression',
        },
        'display_column': {
            'description': 'The column name to display.',
        },
        'display_mode': {
            'description': 'How to display the widget.',
            'type': 'SelectWdg',
            'values': 'Popup|Tab|Browser',
            'default': 'Popup'
        }
    }

    def init(self):
        """
        The special tactic init.

        :return: None
        """
        super(SobjectEditLauncherWdg, self).init()
        self.server = TacticServerStub.get()

    def get_sobject_code(self):
        """
        Get the sobject code that this launcher should use.
        This will only eval the expression if the sobject_code
        arg is not provided.

        :return: the code of the sobject to edit/view
        """
        sobject_code = self.kwargs.get('sobject_code')
        if not sobject_code:
            code_expression = self.kwargs.get('sobject_code_expression')
            this_sobject = self.get_current_sobject()
            search_type = this_sobject.get_search_type()
            expression = "@GET({0}['code','{1}']{2})"
            sobject_code = self.server.eval(expression.format(search_type, this_sobject.get('code'), code_expression))
            if sobject_code:
                sobject_code = sobject_code[0]
            else:
                return ''

        return sobject_code

    def get_browser_tab_behavior(self, url):
        """
        Gets the behavior for opening up the edit wdg
        in a new tab in the browser.

        :param url: the url to open
        :return: the open behavior
        """
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''
        try{
            window.open('%s');
        }
        catch(err){
            spt.app_busy.hide();
            spt.alert(spt.exception.handler(err));
        }
        ''' % url}
        return behavior

    def get_launch_behavior(self, search_type, sobject_code, display_mode):
        """
        Get the behavior for clicking the sobject's name. It will either popup
        the view/edit window, or open a new tab, depending on the display_mode.

        :param search_type: the search type of the sobject to edit
        :param sobject_code: the code of the sobject to edit
        :param display_mode: how to display the edit wdg, Popup|Tab
        :return: the click behavior
        """
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''
        try{
            var class_name = 'common_tools.sobject_edit_widget.SobjectEditWdg';
            var search_type = '%s';
            var sobject_code = '%s';
            var display_mode = '%s';
            kwargs = {
                'search_type': search_type,
                'sobject_code': sobject_code
            };
            if(display_mode == 'Tab'){
                spt.tab.add_new('edit_wdg_' + sobject_code, 'Edit ' + sobject_code, class_name, kwargs);
            }
            else if(display_mode == 'Popup'){
                spt.panel.load_popup('Edit ' + sobject_code, class_name, kwargs);
            }
            else{
                spt.panel.load_popup('Edit ' + sobject_code, class_name, kwargs);
            }
        }
        catch(err){
            spt.app_busy.hide();
            spt.alert(spt.exception.handler(err));
        }
        ''' % (search_type, sobject_code, display_mode)}
        # Normally I prefer the {0} format over %s, but it doesn't work with injected javascript
        return behavior

    def get_display(self):
        """
        Get the display for this edit wdg launcher. It should appear as
        the name of the sobject, bold and underlined.

        :return: the sobject edit launcher widget
        """
        search_type = self.kwargs.get('search_type')
        sobject_code = self.get_sobject_code()
        display_column = self.kwargs.get('display_column')
        if not display_column:
            display_column = 'code'
        display_name = self.server.eval("@GET({0}['code','{1}'].{2})".format(search_type, sobject_code, display_column))
        display_name = display_name[0] if display_name else sobject_code

        display_mode = self.kwargs.get('display_mode')
        if display_mode == 'Browser':
            url = ctu.get_edit_wdg_url(search_type, sobject_code, server=self.server)
            launch_behavior = self.get_browser_tab_behavior(url)
        else:
            launch_behavior = self.get_launch_behavior(search_type, sobject_code, display_mode)

        display_text = '<b><u>{0}</u></b>'.format(display_name)
        div = DivWdg(display_text)
        div.add_behavior(launch_behavior)
        div.add_styles({'cursor': 'pointer'})

        return div


class SobjectEditWdg(CustomLayoutWdg):
    """
    The main sobject view/edit widget.
    """

    def init(self):
        """
        The special tactic init function.

        :return: None
        """
        super(SobjectEditWdg, self).init()
        self.server = TacticServerStub.get()

    def get_display(self):
        """
        Get the code for displaying this widget.

        :return: the sobject edit widget
        """
        search_type = self.kwargs.get('search_type')
        sobject_code = self.kwargs.get('sobject_code')
        if not (search_type and sobject_code):
            return DivWdg('Could not display [{0}]: [{1}]'.format(search_type, sobject_code))

        mode = 'view'
        user_groups = Environment.get_group_names()
        if 'scheduling' in user_groups:
            mode = 'edit'
        sobject_type = ctu.get_sobject_type(search_type)
        # TODO: get a relevant display name
        display_name = sobject_code
        title = '{0} {1}: {2}'.format(mode.title(), sobject_type.title(), display_name)
        edit_widget = EditWdg(search_type=search_type, code=sobject_code, title=title, mode=mode,
                              view='edit', show_header='true')
        return edit_widget
