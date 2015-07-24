import tacticenv
from pyasm.web import Table, DivWdg
from tactic.ui.common import BaseTableElementWdg
from tactic.ui.common import BaseRefreshWdg
from tactic.ui.panel import EditWdg
class PlatformInspectLauncherWdg(BaseTableElementWdg):

    def init(my):
        from tactic_client_lib import TacticServerStub
        my.server = TacticServerStub.get()
    
    def get_launch_behavior(my, platform_sk):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                          var platform_sk = '%s';
                          platform_code = platform_sk.split('code=')[1];
                          var class_name = 'tactic.ui.panel.EditWdg';
                          kwargs = {
                                           'element_name': 'general',
                                           'mode': 'edit',
                                           'search_type': 'twog/platform',
                                           'code': platform_code,
                                           'title': 'Platform Information',
                                           'view': 'edit',
                                           'widget_key': 'edit_layout'
                                   };
                          spt.panel.load_popup('Platform Information', class_name, kwargs);
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                          //alert(err);
                }
         ''' % platform_sk}
        return behavior

    def get_display(my):
        #--print "IN OBLW"
        code = ''
        if 'search_key' in my.kwargs.keys():
            search_key = str(my.kwargs.get('search_key'))
            code = search_key.split('code=')[1]
            search_type = search_key.split('?')[0]
            sob_platform = my.server.eval("@GET(%s['code','%s'].platform)" % (search_type, code))
        else: 
            sobject = my.get_current_sobject()
            code = sobject.get_code()
            sob_platform = sobject.get_value('platform')

        platform_sk = ''
        if sob_platform not in [None,'']:
            platform_sk = my.server.eval("@GET(twog/platform['name','%s'].__search_key__)" % sob_platform)
            if len(platform_sk) > 0:
                platform_sk = platform_sk[0]
            else:
                platform_sk = ''
            
        widget = DivWdg()
        table = Table()
        if platform_sk not in [None,'']:
            table.add_attr('width', '50px')
            table.add_row()
            cell1 =  table.add_cell('<img border="0" style="vertical-align: middle" title="" src="/context/icons/silk/email.png">')
            launch_behavior = my.get_launch_behavior(platform_sk)
            cell1.add_style('cursor: pointer;')
            cell1.add_behavior(launch_behavior)
        widget.add(table)

        return widget
