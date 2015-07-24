__all__ = ["WorkOrderPrintLauncherWdg","WorkOrderPrintWdg","WorkOrderPrintExecutePages"]
import tacticenv
import os, datetime
from pyasm.biz import *
from pyasm.web import Table, DivWdg
from pyasm.widget import SelectWdg, IconWdg
from tactic.ui.common import BaseTableElementWdg
from tactic.ui.common import BaseRefreshWdg
from tactic.ui.panel import EditWdg
from tactic.ui.widget.button_new_wdg import ButtonSmallNewWdg, ButtonRowWdg
from pyasm.command import *

class WorkOrderPrintLauncherWdg(BaseTableElementWdg):

    def init(my):
        from tactic_client_lib import TacticServerStub
        my.server = TacticServerStub.get()

    def get_launch_behavior(my, code):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                          var server = TacticServerStub.get();
                          var code = '%s'; 
                          var class_name = 'order_builder.WorkOrderPrintWdg';
                          kwargs = {
                                           'code': code
                                   };
                          spt.panel.load_popup('Print Work Order Info Page for ' + code, class_name, kwargs);
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                          //alert(err);
                }
         ''' % code}
        return behavior

    def get_display(my):
        do_button = False
        if 'work_order_code' not in my.kwargs.keys(): 
            sobject = my.get_current_sobject()
            code = sobject.get_code()
        else:
            code = my.kwargs.get('work_order_code')    
            do_button = True
        
        widget = DivWdg()
        table = Table()
        table.add_attr('width', '50px')
        table.add_row()
        launch_behavior = my.get_launch_behavior(code)
        what_goes_in = '<img border="0" style="vertical-align: middle" title="" src="/context/icons/silk/printer.png">'
        if do_button:
           what_goes_in = ButtonSmallNewWdg(title="Print Work Order", icon=IconWdg.PRINTER)
           what_goes_in.add_behavior(launch_behavior) 
        cell1 = table.add_cell(what_goes_in)
        cell1.add_attr('code',code)
        cell1.add_style('cursor: pointer;')
        if not do_button:
            cell1.add_behavior(launch_behavior)
        widget.add(table)
        if do_button:
            return what_goes_in
        else:
            return widget

class WorkOrderPrintWdg(BaseRefreshWdg):

    def init(my):
        from client.tactic_client_lib import TacticServerStub
        from pyasm.common import Environment
        my.server = TacticServerStub.get()
        my.login = Environment.get_login()
        my.user = my.login.get_login()
        my.code = ''
        my.types = ['Full_Work_Order']
        my.template_files = {'Full_Work_Order': '/var/www/html/source_labels/work_order.html'}

    def fix_date(my, date):
        #This is needed due to the way Tactic deals with dates (using timezone info), post v4.0 
        from pyasm.common import SPTDate
        return_date = ''
        date_obj = SPTDate.convert_to_local(date)
        if date_obj not in [None,'']:
            return_date = date_obj.strftime("%Y-%m-%d  %H:%M")
        return return_date
    
    def get_display(my):   
        my.code = str(my.kwargs.get('code'))
        table = Table()
        table.add_attr('class','print_wo_wdg')
        table.add_row()

        work_order = my.server.eval("@SOBJECT(twog/work_order['code','%s'])" % my.code)[0]
        process = work_order.get('process')
        proj_code = work_order.get('proj_code')
        instructions = work_order.get('instructions')
        #Not working in 4.2 - worked in 3.9
        #try:
        #    unicode(instructions, "ascii")
        #except UnicodeError:
        #    instructions = unicode(instructions, "utf-8")
        #else:
        #    # value was valid ASCII data
        #    pass
        login = work_order.get('login')
        

        proj = my.server.eval("@SOBJECT(twog/proj['code','%s'])" % proj_code)[0]
        title_code = proj.get('title_code')
        title = my.server.eval("@SOBJECT(twog/title['code','%s'])" % title_code)[0]
        title_title = '%s: %s' % (title.get('title'), title.get('episode'))
        client_code = title.get('client_code')
        client_name = ''
        client_name2 = my.server.eval("@GET(twog/client['code','%s'].name)" % client_code) 
        if client_name2:
            client_name = client_name2[0]
        pipeline_code = title.get('pipeline_code')

        order = my.server.eval("@SOBJECT(twog/order['code','%s'])" % title.get('order_code'))[0]
        po_number = order.get('po_number')

        task = my.server.eval("@SOBJECT(sthpw/task['code','%s'])" % work_order.get('task_code'))
        status = ''
        start_date = ''
        end_date = ''
        assigned_to = ''
        due_date = my.fix_date(work_order.get('due_date'))
        if due_date in [None,'']:
            due_date = ''
        if len(task) > 0:
            task = task[0]
            status = task.get('status')
            start_date = my.fix_date(task.get('actual_start_date'))
            end_date = my.fix_date(task.get('actual_end_date'))
            assigned_to = task.get('assigned')
           
        source_template_string = '<div id="source_item">[SOURCE_BARCODE] | [SOURCE_TYPE] [SOURCE_FRAME_RATE] [SOURCE_ASPECT_RATIO] [SOURCE_COLOR_SPACE] [SOURCE_VERSION] [SOURCE_STRAT2G_PART] [SOURCE_TITLE]</div>'
        work_order_sources = my.server.eval("@SOBJECT(twog/work_order_sources['work_order_code','%s'])" % my.code)
        work_order_passin = my.server.eval("@SOBJECT(twog/work_order_passin['work_order_code','%s'])" % my.code)  
        sources_str = ''
        for wos in work_order_sources:
            source_code = wos.get('source_code')
            source = my.server.eval("@SOBJECT(twog/source['code','%s'])" % source_code)[0]
            my_str = source_template_string
            my_str = my_str.replace('[SOURCE_BARCODE]', source.get('barcode'))
            my_str = my_str.replace('[SOURCE_TYPE]', source.get('source_type'))
            my_str = my_str.replace('[SOURCE_FRAME_RATE]', source.get('frame_rate'))
            my_str = my_str.replace('[SOURCE_ASPECT_RATIO]', source.get('aspect_ratio'))
            my_str = my_str.replace('[SOURCE_COLOR_SPACE]', source.get('color_space'))
            my_str = my_str.replace('[SOURCE_VERSION]', source.get('version'))
            my_str = my_str.replace('[SOURCE_STRAT2G_PART]', source.get('part'))
            my_str = my_str.replace('[SOURCE_TITLE]', '%s: %s' % (source.get('title'), source.get('episode')))
            sources_str = '%s%s' % (sources_str, my_str)
        for wop in work_order_passin:
            if wop.get('deliverable_source_code') not in [None,'']:
                source_code = wop.get('deliverable_source_code')
                source = my.server.eval("@SOBJECT(twog/source['code','%s'])" % source_code)[0]
                my_str = source_template_string
                my_str = my_str.replace('[SOURCE_BARCODE]', source.get('barcode'))
                my_str = my_str.replace('[SOURCE_TYPE]', source.get('source_type'))
                my_str = my_str.replace('[SOURCE_FRAME_RATE]', source.get('frame_rate'))
                my_str = my_str.replace('[SOURCE_ASPECT_RATIO]', source.get('aspect_ratio'))
                my_str = my_str.replace('[SOURCE_COLOR_SPACE]', source.get('color_space'))
                my_str = my_str.replace('[SOURCE_VERSION]', source.get('version'))
                my_str = my_str.replace('[SOURCE_STRAT2G_PART]', source.get('part'))
                my_str = my_str.replace('[SOURCE_TITLE]', '%s: %s' % (source.get('title'), source.get('episode')))
                sources_str = '%s%s' % (sources_str, my_str)
                


#        deliverable_source_template_string = '<div id="result_item">[RESULT_BARCODE] | [RESULT_TYPE] [RESULT_FRAME_RATE] [RESULT_ASPECT_RATIO] [RESULT_COLOR_SPACE] [RESULT_VERSION] [RESULT_STRAT2G_PART] [RESULT_TITLE]</div>'
#        work_order_deliverables = my.server.eval("@SOBJECT(twog/work_order_deliverables['work_order_code','%s'])" % my.code)
#        results_str = ''
#        for wod in work_order_deliverables:
#            if wod.get('deliverable_source_code') not in [None,'']:
#                source_code = wod.get('deliverable_source_code')
#                source = my.server.eval("@SOBJECT(twog/source['code','%s'])" % source_code)[0]
#                my_str = deliverable_source_template_string
#                my_str = my_str.replace('[RESULT_BARCODE]', source.get('barcode'))
#                my_str = my_str.replace('[RESULT_TYPE]', source.get('source_type'))
#                my_str = my_str.replace('[RESULT_FRAME_RATE]', source.get('frame_rate'))
#                my_str = my_str.replace('[RESULT_ASPECT_RATIO]', source.get('aspect_ratio'))
#                my_str = my_str.replace('[RESULT_COLOR_SPACE]', source.get('color_space'))
#                my_str = my_str.replace('[RESULT_VERSION]', source.get('version'))
#                my_str = my_str.replace('[RESULT_STRAT2G_PART]', source.get('part'))
#                my_str = my_str.replace('[RESULT_TITLE]', '%s: %s' % (source.get('title'), source.get('episode')))
#                results_str = '%s%s' % (results_str, my_str)

        #print "WORK ORDER = %s" % work_order
        #notes_expr = "@SOBJECT(sthpw/note['search_id','%s']['search_type','twog/proj?project=twog']['context','in','%s|Billing'])" % (work_order.get('id'), process.strip())
        #print 'USER = %s' % my.user
        #print "WORK ORDER ID = %s" % work_order.get('id')
        #print "PROCESS = %s" % process
        #print "NOTES EXPR = %s" % notes_expr
        #notes = my.server.eval(notes_expr)
        #print "NOTES = %s" % notes
        notes_str = ''
        # They said that this sould just be empty, so....
#        for note in notes:
#            if note.get('search_id') == work_order.get('id') and note.get('search_type') == 'twog/proj?project=twog':
#                my_str = '%s: %s at %s<br/>%s' % (note.get('context'), note.get('login'), note.get('timestamp'), note.get('note'))
#                if notes_str == '':
#                    notes_str = my_str
#                else:
#                    notes_str = '%s<br/>%s' % (notes_str, my_str)    

        
        select = SelectWdg('print_type')
        for guy in my.types:
            select.append_option(guy,guy)  
        selly = table.add_cell(select)
        selly.add_attr('align','center')
        table.add_row()
        date = str(datetime.datetime.now()).split(' ')[0]
        for guy in my.types:
            result = ''
            f = open(my.template_files[guy], 'r')
            for line in f:
                if not line.strip():
                    continue
                else:
                    line = line.rstrip('\r\n')
                    line =line.replace('[WORK_ORDER_CODE]',my.code)
                    line =line.replace('[DUE_DATE]',due_date)
                    line =line.replace('[PROJECT_CODE]',proj_code)
                    line =line.replace('[PO_NUMBER]',po_number)
                    line =line.replace('[TITLE]',title_title)
                    line =line.replace('[CLIENT]',client_name)
                    line =line.replace('[PIPELINE_CODE]',pipeline_code)
                    line =line.replace('[STATUS]',status)
                    line =line.replace('[SOURCES]', sources_str)
                    #line =line.replace('[RESULTS]', results_str)
                    line =line.replace('[INSTRUCTIONS]', instructions)
                    line =line.replace('[NOTES]', notes_str)
                    line =line.replace('[START DATE/TIME]', start_date)
                    line =line.replace('[END DATE/TIME]', end_date)
                    line =line.replace('[LOGIN]',login)
                    line =line.replace('[ASSIGNED_TO]', assigned_to)
                    
                    result = '%s%s' % (result,line)
            f.close()
            new_wo_file = '/var/www/html/source_labels/work_orders/%s_%s.html' % (my.code, guy)
            if os.path.exists(new_wo_file):
                os.system('rm -rf %s' % new_wo_file)
            new_guy = open(new_wo_file, 'w') 
            new_guy.write(result.encode('utf-8'))
            new_guy.close()
        t1 = table.add_cell('')
        t1.add_style('width: 100%s;' % '%')
        do_it = table.add_cell('<input type="button" value="Get Work Order Info Page For %s"/>' % (process)) 
        do_it.add_behavior(my.get_open_work_order_print_page())
        t2 = table.add_cell('')
        t2.add_style('width: 100%s;' % '%')
        return table

    def get_open_work_order_print_page(my):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        function printExternal(url) {
                            var printWindow = window.open( url, 'Print', 'toolbar=1,location=1,directories=1,status=1,menubar=1,scrollbars=0,resizable=0');
                            printWindow.addEventListener('load', function(){
                                printWindow.print();
                                printWindow.close();
                            }, true);
                        }
                        try{
                          var code = '%s';
                          var top_el = spt.api.get_parent(bvr.src_el, '.print_wo_wdg');
                          var sels = top_el.getElementsByTagName('select');
                          var type_sel = '';
                          for(var r = 0; r < sels.length; r++){
                              if(sels[r].name == 'print_type'){
                                  type_sel = sels[r];
                              }
                          } 
                          var type = type_sel.value;
                          var url = 'http://tactic01/source_labels/work_orders/' + code + '_' + type + '.html';
                          printExternal(url);
                          //new_win = window.open(url,'_blank','toolbar=1,location=1,directories=1,status=1,menubar=1,scrollbars=0,resizable=0'); 
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                          //alert(err);
                }
         ''' % (my.code)
        }
        return behavior
    


class WorkOrderPrintExecutePages(Command):

    def __init__(my, **kwargs):
        from client.tactic_client_lib import TacticServerStub
        from pyasm.common import Environment
        super(WorkOrderPrintExecutePages, my).__init__(**kwargs)
        my.server = TacticServerStub.get()
        my.login = Environment.get_login()
        my.user = my.login.get_login()
        my.codes = str(kwargs.get('codes'))
        my.types = ['Full_Work_Order']
        my.template_files = {'Full_Work_Order': '/var/www/html/source_labels/work_order.html'}
        my.transaction = None

    def check(my):
        return True

    def fix_date(my, date):
        #This is needed due to the way Tactic deals with dates (using timezone info), post v4.0 
        from pyasm.common import SPTDate
        return_date = ''
        date_obj = SPTDate.convert_to_local(date)
        if date_obj not in [None,'']:
            return_date = date_obj.strftime("%Y-%m-%d  %H:%M")
        return return_date
    
    def execute(my):   
        codes = my.codes.split(',')
        for code in codes:
            work_order = my.server.eval("@SOBJECT(twog/work_order['code','%s'])" % code)[0]
            process = work_order.get('process')
            proj_code = work_order.get('proj_code')
            instructions = work_order.get('instructions')
            #Not working in 4.2 -- worked in 3.9
            #try:
            #    unicode(instructions, "ascii")
            #except UnicodeError:
            #    instructions = unicode(instructions, "utf-8")
            #else:
            #    # value was valid ASCII data
            #    pass
            login = work_order.get('login')
    
            proj = my.server.eval("@SOBJECT(twog/proj['code','%s'])" % proj_code)[0]
            title_code = proj.get('title_code')
            title = my.server.eval("@SOBJECT(twog/title['code','%s'])" % title_code)[0]
            title_title = '%s: %s' % (title.get('title'), title.get('episode'))
            client_code = title.get('client_code')
            client_name = ''
            client_name2 = my.server.eval("@GET(twog/client['code','%s'].name)" % client_code) 
            if client_name2:
                client_name = client_name2[0]
            pipeline_code = title.get('pipeline_code')
    
            order = my.server.eval("@SOBJECT(twog/order['code','%s'])" % title.get('order_code'))[0]
            po_number = order.get('po_number')
    
            task = my.server.eval("@SOBJECT(sthpw/task['code','%s'])" % work_order.get('task_code'))
            status = ''
            start_date = ''
            end_date = ''
            assigned_to = ''
            due_date = my.fix_date(work_order.get('due_date'))
            if due_date in [None,'']:
                due_date = ''
            if len(task) > 0:
                task = task[0]
                status = task.get('status')
                start_date = my.fix_date(task.get('actual_start_date'))
                end_date = my.fix_date(task.get('actual_end_date'))
                assigned_to = task.get('assigned')
               
            source_template_string = '<div id="source_item">[SOURCE_BARCODE] | [SOURCE_TYPE] [SOURCE_FRAME_RATE] [SOURCE_ASPECT_RATIO] [SOURCE_COLOR_SPACE] [SOURCE_VERSION] [SOURCE_STRAT2G_PART] [SOURCE_TITLE]</div>'
            work_order_sources = my.server.eval("@SOBJECT(twog/work_order_sources['work_order_code','%s'])" % code)
            work_order_passin = my.server.eval("@SOBJECT(twog/work_order_passin['work_order_code','%s'])" % code)  
            sources_str = ''
            for wos in work_order_sources:
                source_code = wos.get('source_code')
                source = my.server.eval("@SOBJECT(twog/source['code','%s'])" % source_code)[0]
                my_str = source_template_string
                my_str = my_str.replace('[SOURCE_BARCODE]', source.get('barcode'))
                my_str = my_str.replace('[SOURCE_TYPE]', source.get('source_type'))
                my_str = my_str.replace('[SOURCE_FRAME_RATE]', source.get('frame_rate'))
                my_str = my_str.replace('[SOURCE_ASPECT_RATIO]', source.get('aspect_ratio'))
                my_str = my_str.replace('[SOURCE_COLOR_SPACE]', source.get('color_space'))
                my_str = my_str.replace('[SOURCE_VERSION]', source.get('version'))
                my_str = my_str.replace('[SOURCE_STRAT2G_PART]', source.get('part'))
                my_str = my_str.replace('[SOURCE_TITLE]', '%s: %s' % (source.get('title'), source.get('episode')))
                sources_str = '%s%s' % (sources_str, my_str)
            for wop in work_order_passin:
                if wop.get('deliverable_source_code') not in [None,'']:
                    source_code = wop.get('deliverable_source_code')
                    source = my.server.eval("@SOBJECT(twog/source['code','%s'])" % source_code)[0]
                    my_str = source_template_string
                    my_str = my_str.replace('[SOURCE_BARCODE]', source.get('barcode'))
                    my_str = my_str.replace('[SOURCE_TYPE]', source.get('source_type'))
                    my_str = my_str.replace('[SOURCE_FRAME_RATE]', source.get('frame_rate'))
                    my_str = my_str.replace('[SOURCE_ASPECT_RATIO]', source.get('aspect_ratio'))
                    my_str = my_str.replace('[SOURCE_COLOR_SPACE]', source.get('color_space'))
                    my_str = my_str.replace('[SOURCE_VERSION]', source.get('version'))
                    my_str = my_str.replace('[SOURCE_STRAT2G_PART]', source.get('part'))
                    my_str = my_str.replace('[SOURCE_TITLE]', '%s: %s' % (source.get('title'), source.get('episode')))
                    sources_str = '%s%s' % (sources_str, my_str)
                    
    
    
#            deliverable_source_template_string = '<div id="result_item">[RESULT_BARCODE] | [RESULT_TYPE] [RESULT_FRAME_RATE] [RESULT_ASPECT_RATIO] [RESULT_COLOR_SPACE] [RESULT_VERSION] [RESULT_STRAT2G_PART] [RESULT_TITLE]</div>'
#            work_order_deliverables = my.server.eval("@SOBJECT(twog/work_order_deliverables['work_order_code','%s'])" % code)
#            results_str = ''
#            for wod in work_order_deliverables:
#                if wod.get('deliverable_source_code') not in [None,'']:
#                    source_code = wod.get('deliverable_source_code')
#                    source = my.server.eval("@SOBJECT(twog/source['code','%s'])" % source_code)[0]
#                    my_str = deliverable_source_template_string
#                    my_str = my_str.replace('[RESULT_BARCODE]', source.get('barcode'))
#                    my_str = my_str.replace('[RESULT_TYPE]', source.get('source_type'))
#                    my_str = my_str.replace('[RESULT_FRAME_RATE]', source.get('frame_rate'))
#                    my_str = my_str.replace('[RESULT_ASPECT_RATIO]', source.get('aspect_ratio'))
#                    my_str = my_str.replace('[RESULT_COLOR_SPACE]', source.get('color_space'))
#                    my_str = my_str.replace('[RESULT_VERSION]', source.get('version'))
#                    my_str = my_str.replace('[RESULT_STRAT2G_PART]', source.get('part'))
#                    my_str = my_str.replace('[RESULT_TITLE]', '%s: %s' % (source.get('title'), source.get('episode')))
#                    results_str = '%s%s' % (results_str, my_str)
    
            notes_expr = "@SOBJECT(sthpw/note['search_id','%s']['search_type','twog/proj?project=twog']['context','in','%s|Billing'])" % (work_order.get('id'), process.strip())
            notes_str = ''
            # They said that this sould just be empty, so....
    #        for note in notes:
    #            if note.get('search_id') == work_order.get('id') and note.get('search_type') == 'twog/proj?project=twog':
    #                my_str = '%s: %s at %s<br/>%s' % (note.get('context'), note.get('login'), note.get('timestamp'), note.get('note'))
    #                if notes_str == '':
    #                    notes_str = my_str
    #                else:
    #                    notes_str = '%s<br/>%s' % (notes_str, my_str)    
    
            date = str(datetime.datetime.now()).split(' ')[0]
            for guy in my.types:
                result = ''
                f = open(my.template_files[guy], 'r')
                for line in f:
                    if not line.strip():
                        continue
                    else:
                        line = line.rstrip('\r\n')
                        line =line.replace('[WORK_ORDER_CODE]',code)
                        line =line.replace('[DUE_DATE]',due_date)
                        line =line.replace('[PROJECT_CODE]',proj_code)
                        line =line.replace('[PO_NUMBER]',po_number)
                        line =line.replace('[TITLE]',title_title)
                        line =line.replace('[CLIENT]',client_name)
                        line =line.replace('[PIPELINE_CODE]',pipeline_code)
                        line =line.replace('[STATUS]',status)
                        line =line.replace('[SOURCES]', sources_str)
                        #line =line.replace('[RESULTS]', results_str)
                        line =line.replace('[INSTRUCTIONS]', instructions)
                        line =line.replace('[NOTES]', notes_str)
                        line =line.replace('[START DATE/TIME]', start_date)
                        line =line.replace('[END DATE/TIME]', end_date)
                        line =line.replace('[LOGIN]',login)
                        line =line.replace('[ASSIGNED_TO]', assigned_to)
                        
                        result = '%s%s' % (result,line)
                f.close()
                new_wo_file = '/var/www/html/source_labels/work_orders/%s_%s.html' % (code, guy)
                if os.path.exists(new_wo_file):
                    os.system('rm -rf %s' % new_wo_file)
                new_guy = open(new_wo_file, 'w') 
                new_guy.write(result.encode('utf-8'))
                new_guy.close()
        return ''


    def check_security(my):
        '''give the command a callback that allows it to check security'''
        return True

    def get_title(my):
        return "Print"
