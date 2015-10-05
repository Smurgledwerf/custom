"""
This custom button copies a url to the clipboard. Technically it can copy any text
to the clipboard, but it is intended to copy custom urls.
"""

__author__ = 'topher.hughes'
__date__ = '05/10/2015'

from tactic.ui.common import BaseTableElementWdg

from widget.button_small_new_wdg import ButtonSmallNewWdg


class CopyUrlButton(BaseTableElementWdg):
    """
    The button that copies the specified url to the clipboard.
    """

    def get_url(self):
        """
        Gets the url to copy to the clipboard.

        :return: the url as a string
        """
        return self.kwargs.get('url')

    def get_click_behavior(self, url):
        """
        Gets the behavior that the button uses on click.
        This code was found on stackoverflow, edit with caution.

        NOTE: users MUST update to Chrome 44+, Firefox 41+, IE 11+
        Safari, Opera, etc. are untested

        :param url: the url as a string
        :return: a behavior dictionary
        """
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''
        try{
            var textArea = document.createElement("textarea");

            //
            // *** This styling is an extra step which is likely not required. ***
            //
            // Why is it here? To ensure:
            // 1. the element is able to have focus and selection.
            // 2. if element was to flash render it has minimal visual impact.
            // 3. less flakyness with selection and copying which **might** occur if
            //    the textarea element is not visible.
            //
            // The likelihood is the element won't even render, not even a flash,
            // so some of these are just precautions. However in IE the element
            // is visible whilst the popup box asking the user for permission for
            // the web page to copy to the clipboard.
            //

            // Place in top-left corner of screen regardless of scroll position.
            textArea.style.position = 'fixed';
            textArea.style.top = 0;
            textArea.style.left = 0;

            // Ensure it has a small width and height. Setting to 1px / 1em
            // doesn't work as this gives a negative w/h on some browsers.
            textArea.style.width = '2em';
            textArea.style.height = '2em';

            // We don't need padding, reducing the size if it does flash render.
            textArea.style.padding = 0;

            // Clean up any borders.
            textArea.style.border = 'none';
            textArea.style.outline = 'none';
            textArea.style.boxShadow = 'none';

            // Avoid flash of white box if rendered for any reason.
            textArea.style.background = 'transparent';

            textArea.value = '%s';

            document.body.appendChild(textArea);

            textArea.select();

            var successful = document.execCommand('copy');

            document.body.removeChild(textArea);
        }
        catch(err){
            spt.app_busy.hide();
            spt.alert(spt.exception.handler(err));
        }
        ''' % url}
        # Normally I prefer the {0} format over %s, but it doesn't work with injected javascript
        return behavior

    def get_display(self):
        """
        Handle how the widget is displayed.

        :return: a widget containing a copy button

        :return:
        """
        button = ButtonSmallNewWdg(title=self.kwargs.get('title', 'Copy URL to Clipboard'))
        button.set_option('icon', 'LINK')
        url = self.get_url()
        button.add_behavior(self.get_click_behavior(url))

        return button
