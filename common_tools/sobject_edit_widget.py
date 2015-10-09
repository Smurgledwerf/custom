"""
A generic edit/view widget that will show details of an sobject. It uses the columns defined
in the 'edit' view, and the mode (view|edit) is determined by the users department. This was
originally created to use with the custom url, /sobject/{search_type}/{sobject_code} to make
it easier to edit linked sobjects.
"""

__author__ = 'topher.hughes'
__date__ = '09/10/2015'

from tactic_client_lib import TacticServerStub
from pyasm.web import DivWdg
from tactic.ui.panel import CustomLayoutWdg, EditWdg

import common_tools.utils as ctu


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

        # TODO: chmod depending on the users department
        mode = 'edit'
        sobject_type = ctu.get_sobject_type(search_type)
        # TODO: get a relevant display name
        display_name = sobject_code
        title = '{0} {1}: {2}'.format(mode.title(), sobject_type.title(), display_name)
        edit_widget = EditWdg(search_type=search_type, code=sobject_code, title=title, mode=mode,
                              view='edit', show_header='true')
        return edit_widget
