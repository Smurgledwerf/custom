__all__ = ['SourceTypeIconWdg']
import tacticenv
from tactic.ui.common import BaseTableElementWdg
from pyasm.web import Table, DivWdg

class SourceTypeIconWdg(BaseTableElementWdg):
    #This is the button that launches the TitleSelectorWdg

    def init(my):
        nothing = 'true'
        my.lookups = {'File': '/context/images/media-file.png', 'CD': '/context/images/media-cd.png', 'DVD': '/context/images/media-dvd.png', 'Hard Drive': '/context/images/media-hard-drive.png', 'Blu-ray': '/context/images/media-blu-ray.png', 'Tape': '/context/images/media-tape.png'}

    def get_display(my):
        code = ''
        widget = DivWdg()
        table = Table()
        if 'code' in my.kwargs.keys():
            code = my.kwargs.get('code') 
        else: 
            sobject = my.get_current_sobject()
            code = sobject.get_code()
        if code not in [None,'',-1,'-1']:
            source_type = sobject.get_value('source_type')
            if source_type not in [None,'']:
                table.add_attr('width', '36px')
                table.add_row()
                cell1 = table.add_cell('<img border="0" style="vertical-align: middle" title="%s" name="%s" alt="%s" src="%s">' % (source_type, source_type, source_type, my.lookups[source_type]))
        widget.add(table)

        return widget
