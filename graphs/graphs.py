ll__ = ["GraphHoursWdg"]
import tacticenv, os
from datetime import date, timedelta as td
from pyasm.biz import *
from pyasm.web import Table, DivWdg, HtmlElement
from pyasm.common import jsonloads, jsondumps, Environment
from tactic.ui.common import BaseTableElementWdg
from tactic.ui.common import BaseRefreshWdg
from tactic.ui.widget import CalendarInputWdg


class GraphHoursWdg(BaseTableElementWdg):

    def init(my):
        from tactic_client_lib import TacticServerStub
        my.server = TacticServerStub.get()

    def get_title(my):
        div = DivWdg()
        div.add_behavior(my.get_load_behavior())
        return div

    def kill_mul_spaces(my, origstrg):
        newstrg = ''
        for word in origstrg.split():
            newstrg=newstrg+' '+word
        return newstrg
 
    def get_dates(my):
        import datetime
        rightnow = datetime.datetime.now()
        rnmo = str(rightnow.month)
        if len(rnmo) == 1:
            rnmo = '0%s' % rnmo 
        rnday = str(rightnow.day)
        if len(rnday) == 1:
            rnday = '0%s' % rnday 
        date2 = '%s-%s-%s' % (rightnow.year, rnmo, rnday)
        date1 = date.today()-td(days=31)
        #print "D1 = %s, D2 = %s" % (date1, date2)
        date1 = '2013-04-01'
        date2 = '2013-04-30'
        return [str(date1), str(date2)]
         
    
    def make_TV_data_dict(my, file_path):
        the_file = open(file_path, 'r')
        fields = []
        data_dict = {}
        count = 0
        boolio = True
        line_count = 0
        flen = 0
        for line in the_file:
            first_name = ''
            last_name = ''
            name = ''
            fixed_date = ''
            if line_count > 5:
                line = line.rstrip('\r\n')
                if line in [None,'',' ']:
                    boolio = False
                if boolio:
                    data = line.split('","')
                    if line_count == 6:
                        dc = 0
                        for field in data:
                            if dc == 0:
                                field = field[1:]
                            field = my.kill_mul_spaces(field)
                            field = field.strip(' ')
                            fields.append(field)
                            dc = dc + 1
                        flen = len(fields)
                        fields[flen - 1] = fields[flen - 1][:-1]
                    elif line_count > 6:
                        data_count = 0
                        this_code = ''
                        this_data = {}
                        this_time = 0
                        for val in data:
                            field = fields[data_count]
                            if data_count == 0:
                                val = val[1:]
                            val = my.kill_mul_spaces(val)
                            val = val.strip(' ')
                            if data_count == flen - 1:
                                val = val[:-1]
                            if field in ['First Name', 'Last Name', 'Date', 'Total Work Hours']:
                                if field == 'Total Work Hours':
                                    if val in ['-','',' ',None]:
                                        val = 0
                                this_data[field] = val
                            if field == 'First Name':
                                first_name = val
                            elif field == 'Last Name':
                                last_name = val
                            elif field == 'Date':
                                date_s = val.split('/')
                                fixed_date = '%s-%s-%s' % (date_s[2], date_s[0], date_s[1])    
                            data_count = data_count + 1 
                        this_data['fixed_date'] = fixed_date
                        name = '%s %s' % (first_name.lower(), last_name.lower())
                        if name not in data_dict.keys():
                            data_dict[name] = {'first_name': first_name, 'last_name': last_name, 'name': name, 'days': {}}
                        if fixed_date not in data_dict[name]['days'].keys():
                            data_dict[name]['days'][fixed_date] = float(this_data['Total Work Hours'])
                        else:
                            data_dict[name]['days'][fixed_date] = float(data_dict[name]['days'][fixed_date]) + float(this_data['Total Work Hours'])
                    count = count + 1  
            line_count = line_count + 1
        the_file.close()
        return data_dict

    def make_data_dict(my, file_name, mode):
        the_file = open(file_name, 'r')
        fields = []
        data_dict = {}
        count = 0
        boolio = True
        code_index = 0
        hours = {}
        for line in the_file:
            line = line.rstrip('\r\n')
            #data = line.split('\t')
            data = line.split('|')
            if boolio:
                if count == 0:
                    field_counter = 0
                    for field in data:
                        field = my.kill_mul_spaces(field)
                        field = field.strip(' ')
                        fields.append(field)
                        if mode == 'group':
                            if field == 'id':
                                code_index = field_counter
                        elif mode == 'hours':
                            if field == 'login':
                                code_index = field_counter
                        else:
                            if field == 'code':
                                code_index = field_counter
                        field_counter = field_counter + 1
                            
                elif count == 1:
                    nothing = True
                elif data[0][0] == '(':
                    boolio = False
                else:
                    data_count = 0
                    this_code = ''
                    this_data = {}
                    hour_data = {}
                    for val in data:
                        field = fields[data_count]
                        val = my.kill_mul_spaces(val)
                        val = val.strip(' ')
                        if data_count == code_index:
                            this_code = val
                            if mode == 'hours': 
                                if this_code not in hours.keys():
                                    hours[this_code] = []
                        elif mode == 'hours':
                            if field == 'straight_time':
                                if val in [None,'']:
                                    val = 0
                                hour_data['straight_time'] = float(val)
                            elif field == 'day':
                                hour_data['day'] = val.split(' ')[0]
                        this_data[field] = val
                        data_count = data_count + 1 
                    if mode == 'hours': 
                        hours[this_code].append(hour_data)
                    data_dict[this_code] = this_data
                count = count + 1  
        the_file.close()
        return [data_dict, hours]

    def make_string_dict(my, data_arr):
        out_str = ''
        for data in data_arr:
            if out_str == '':
                out_str = '|||'
            else:
                out_str = '%s|||' % out_str
            for key, val in data.iteritems():
                out_str = '%sWvWXsKEYsX:%sXsVALsX:%sWvW' % (out_str, key, val)
            out_str = '%s|||' % out_str
        return out_str
    
    def get_toggle_row_behavior(my, group):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                          var group = '%s';
                          var top_el = spt.api.get_parent(bvr.src_el, '.graph_top');
                          row = top_el.getElementById('graphs_' + group + '_row');
                          if(row.style.display == 'none'){
                              row.style.display = 'table-row';
                              bvr.src_el.innerHTML = '<b><u>Hide Users</u></b>';
                          }else{
                              row.style.display = 'none';
                              bvr.src_el.innerHTML = '<b><u>Show Users</u></b>';
                          } 
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                          //alert(err);
                }
         ''' % (group)}
        return behavior

    def get_load_again(my):
        behavior = {'css_class': 'clickme', 'type': 'click_up', 'cbjs_action': '''        
                        try{
                          var top_el = spt.api.get_parent(bvr.src_el, '.graph_surrounder');
                          var inputs = top_el.getElementsByTagName('input');
                          date1 = '';
                          date2 = '';
                          for(var r = 0; r < inputs.length; r++){
                              if(inputs[r].getAttribute('name') == 'wh_graph_date1'){
                                  date1 = inputs[r].value;
                              }else if(inputs[r].getAttribute('name') == 'wh_graph_date2'){
                                  date2 = inputs[r].value;
                              }
                          }
                          alert(date1 + ' ||||| ' + date2);
                          spt.api.load_panel(top_el, 'graphs.GraphHoursWdg', {'date1': date1.split(' ')[0], 'date2': date2.split(' ')[0]});
                }
                catch(err){
                          spt.app_busy.hide();
                          spt.alert(spt.exception.handler(err));
                          //alert(err);
                }
         '''}
        return behavior



    def draw_chart3(my, div, idx, title):
        behavior = {'type': 'load', 'cbjs_action':
        
        '''
            function decode_string_dict(data)
            {
                ret_arr = [];
                pts = data.split('|||');
                for(var r = 0; r < pts.length; r++){
                    chunk = pts[r];
                    if(chunk != '' && chunk != null){
                        dict = {};
                        corrs = chunk.split('WvW');
                        for(var t = 0; t < corrs.length; t++){
                            corr = corrs[t];
                            if(corr != '' && corr != null){
                                rightmost = corr.split('XsKEYsX:')[1];
                                segged = rightmost.split('XsVALsX:');
                                key = segged[0];
                                val = segged[1];
                                dict[key] = val;
                            }
                        }
                        ret_arr.push(dict);
                    }
                }
                return ret_arr;
            }
            var clicking = function(idx) {
            title = '%s';
            idx_data_el = document.getElementById('chartdiv_' + idx);
            idx_data = idx_data_el.getAttribute('datastr');
            var chartData = decode_string_dict(idx_data);
            var chart;
                chart = new AmCharts.AmSerialChart();
                chart.dataProvider = chartData;
                chart.categoryField = "cat";
                chart.marginTop = 5;
                chart.plotAreaFillAlphas = 0.2;


                //chart.rotate = true;
                // the following two lines makes chart 3D
                chart.depth3D = 30;
                chart.angle = 20;


                // AXES
                // category axis
                var dateAxis = chart.categoryAxis;
                dateAxis.parseDates = false; // as our data is date-based, we set parseDates to true
                dateAxis.minPeriod = "DD"; // our data is daily, so we set minPeriod to DD                
                dateAxis.autoGridCount = false;
                dateAxis.gridCount = 50;
                dateAxis.gridAlpha = 0.2;
                dateAxis.gridColor = "#000000";
                dateAxis.axisColor = "#555555";
                dateAxis.labelRotation = 30;
                // we want custom date formatting, so we change it in next line

                var hoursAxis = new AmCharts.ValueAxis();
                hoursAxis.title = title;
                hoursAxis.gridAlpha = 0.2;
                hoursAxis.dashLength = 5;
                hoursAxis.axisAlpha = 0.5;
                hoursAxis.inside = false;
                hoursAxis.position = "left";
                chart.addValueAxis(hoursAxis);

                var pctAxis = new AmCharts.ValueAxis();
                pctAxis.title = 'Efficiency %%'; 
                //pctAxis.stackType = "100%%";
                pctAxis.gridAlpha = 0.2;
                pctAxis.axisAlpha = 0.5;
                //pctAxis.labelsEnabled = false;
                pctAxis.position = "right";
                pctAxis.min = 0;
                pctAxis.max = 100;
                chart.addValueAxis(pctAxis);

                // GRAPHS
                // duration graph
                var timevantageGraph = new AmCharts.AmGraph();
                timevantageGraph.title = "TimeVantage:";
                timevantageGraph.valueField = "tv";
                timevantageGraph.type = "column";
                timevantageGraph.valueAxis = hoursAxis; // indicate which axis should be used
                timevantageGraph.lineColor = "#CC0000";
                timevantageGraph.balloonText = "TimeVantage: [[value]] hrs";
                timevantageGraph.fillAlphas = 1;
                timevantageGraph.lineThickness = 1;
                timevantageGraph.legendValueText = " [[value]] Hrs";
                //timevantageGraph.bullet = "square";
                chart.addGraph(timevantageGraph);

                // distance graph
                var tacticGraph = new AmCharts.AmGraph();
                tacticGraph.valueField = "tactic";
                tacticGraph.title = "Tactic:";
                tacticGraph.type = "column";
                tacticGraph.fillAlphas = 1;
                //tacticGraph.valueAxis = distanceAxis; // indicate which axis should be used
                tacticGraph.valueAxis = hoursAxis; // indicate which axis should be used
                tacticGraph.balloonText = "Tactic: [[value]] hrs";
                tacticGraph.legendValueText = "[[value]] Hrs";
                //tacticGraph.lineColor = "#ffe0e0";
                tacticGraph.lineColor = "#2e0854";
                tacticGraph.lineThickness = 1;
                tacticGraph.lineAlpha = 0;
                chart.addGraph(tacticGraph);

                var pctGraph = new AmCharts.AmGraph();
                pctGraph.title = "Efficiency:";
                pctGraph.valueField = "percentage";
                pctGraph.type = "line";
                pctGraph.valueAxis = pctAxis; // indicate which axis should be used
                //pctGraph.valueAxis = hoursAxis; // indicate which axis should be used
                pctGraph.lineColor = "#00b200";
                pctGraph.balloonText = "Efficiency: [[value]]%%";
                pctGraph.fillAlphas = 0;
                pctGraph.lineThickness = .5;
                pctGraph.legendValueText = " Efficiency [[value]]%%";
                pctGraph.bullet = "square";
                chart.addGraph(pctGraph);

                // CURSOR                
                var chartCursor = new AmCharts.ChartCursor();
                chartCursor.zoomable = false;
                chartCursor.categoryBalloonDateFormat = "DD";
                chartCursor.cursorAlpha = 0;
                chart.addChartCursor(chartCursor);

                // LEGEND
                var legend = new AmCharts.AmLegend();
                legend.bulletType = "round";
                legend.equalWidths = false;
                legend.valueWidth = 40;
                legend.color = "#000000";
                chart.addLegend(legend);

                // WRITE                                
                chart.write("chartdiv_" + idx);
                }
        var js_files = ["amcharts/amcharts/amcharts.js"];
        spt.dom.load_js(js_files, clicking);
        
        clicking(%s);
        '''% (title, idx)
        }

        div.add_behavior(behavior)


    def get_load_behavior(my):
        idx = my.get_current_index()
        behavior = {'type': 'load', 'cbjs_action': ''' 
            //spt.graph = {};
            clicking = function(idx) {
            
            var chartData = [{ country: 'USA29', visits: 4252 },
                    { country: 'China', visits: 1882 },
                    { country: 'Japan', visits: 1809 },
                    { country: 'Poland', visits: 328}];

            
            var chart = new AmCharts.AmSerialChart();
            console.log(chart);
            chart.dataProvider = chartData;
            chart.categoryField = 'country';
            chart.marginTop = 15;
            chart.marginLeft = 55;
            chart.marginRight = 15;
            chart.marginBottom = 80;
            chart.angle = 30;
            chart.depth3D = 15;

            var catAxis = chart.categoryAxis;
            catAxis.gridCount = chartData.length;
            catAxis.labelRotation = 90;

            var graph = new AmCharts.AmGraph();
            graph.balloonText = '[[category]]: [[value]]';
            graph.valueField = 'visits'
            graph.type = 'column';
            graph.lineAlpha = 0;
            graph.fillAlphas = 0.8;
            chart.addGraph(graph);


            chart.invalidateSize()
            chart.write('chartdiv_' + idx);
            chart.validateData();
            chart.animateAgain();
            console.log("finished")

            var js_files = ["amcharts/amcharts/amcharts.js"];
            spt.dom.load_js(js_files, clicking);
           
            }
            
            console.log("done onload");
            
            
            '''
            }
        return behavior

    def get_snapshot_file_path(my,snapshot_code):
        what_to_ret = ''
        rel_paths = my.server.get_all_paths_from_snapshot(snapshot_code, mode='local_repo')
        if len(rel_paths) > 0:
            rel_path = rel_paths[0]
            splits = rel_path.split('/')
            if len(splits) < 2:
                splits = rel_path.split('\\')
            file_only = splits[len(splits) - 1]
            what_to_ret = rel_path
        return what_to_ret
  

    def get_display(my):
        logine = Environment.get_login()
        user_name = logine.get_login()
        all_days = {}
        group_days = {}
        user_days = {}
        tv_all_days = {}
        tv_group_days = {}
        tv_user_days = {}
        tv_obj = my.server.eval("@SOBJECT(twog/global_resource['name','TimeVantage'])")[0]
        snaps = my.server.eval("@SOBJECT(sthpw/snapshot['search_type','twog/global_resource?project=twog']['search_id','%s']['is_latest','true'])" % tv_obj.get('id'))
        #print "SNAPS = %s" % snaps
        file_path = my.get_snapshot_file_path(snaps[0].get('code'))
        date1, date2 = my.get_dates()
        if 'date1' in my.kwargs.keys():
            date1 = my.kwargs.get('date1')
        if 'date2' in my.kwargs.keys():
            date2 = my.kwargs.get('date2')
        #print "DATE1 = %s, DATE2 = %s" % (date1, date2)
        #file_path = '/opt/spt/custom/graphs/tv.csv'
        tv_data = my.make_TV_data_dict(file_path)
        login_file = '/opt/spt/custom/graphs/login_file'
        work_hour_file = '/opt/spt/custom/graphs/work_hour_file'
        login_in_group_file = '/opt/spt/custom/graphs/login_in_group_file'
        login_query = '/opt/spt/custom/graphs/login_query'
        login_in_group_query = '/opt/spt/custom/graphs/login_in_group_query'
        work_hour_query = '/opt/spt/custom/graphs/work_hour_query'
        os.system('''psql -U postgres sthpw < %s > %s''' % (login_query, login_file))
        os.system('''psql -U postgres sthpw < %s > %s''' % (work_hour_query, work_hour_file))
        os.system('''psql -U postgres sthpw < %s > %s''' % (login_in_group_query, login_in_group_file))
        login_data = my.make_data_dict(login_file, '')[0]
        work_hour_data = my.make_data_dict(work_hour_file, 'hours')[1]
        lig_data = my.make_data_dict(login_in_group_file, 'group')[0]
        login_groups = {}
        
        # Create login_group lookup by login name
        for key, val in login_data.iteritems():
            if key not in login_groups.keys():
                login_groups[key] = []
            for id, data in lig_data.iteritems():
                if data.get('login') == key:
                    login_groups[key].append(data.get('login_group'))
        # Match up TimeVantage names with tactic logins
        # Fill user_dates dict with all matched logins 
        user_dates = {} 
        name_to_login = {}
        for name, data in tv_data.iteritems():
            for ld, ldata in login_data.iteritems():
                lname = '%s %s' % (ldata.get('first_name').lower(), ldata.get('last_name').lower())
                if name == lname:
                    if name not in user_dates.keys():
                        user_dates[name] = {'login': ldata.get('login'), 'dates': {}}
                    if name not in name_to_login.keys():
                        name_to_login[name] = ldata.get('login')

        #print "TV-DATA = %s" % tv_data
        
        group_dates = {}
        all_dates = {}
        for name, data in user_dates.iteritems():
            tdata = tv_data[name]
            tlogin = data.get('login')
            ugroups = []
            if tlogin in login_groups.keys():
                ugroups = login_groups[tlogin]
                print "TLOGIN = %s, UGROUPS = %s" % (tlogin, ugroups)
            for tdate, ttime in tdata['days'].iteritems():
                if tdate < date2 and tdate > date1:
                    if tdate not in user_dates[name]['dates'].keys():
                        user_dates[name]['dates'][tdate] = {'cat': tdate, 'tv': ttime, 'tactic': 0}
                    else:
                        user_dates[name]['dates'][tdate]['tv'] = user_dates[name]['dates'][tdate]['tv'] + ttime 
                    for g in ugroups:
                        if g not in group_dates.keys():
                            group_dates[g] = {}
                        if tdate not in group_dates[g].keys():
                            group_dates[g][tdate] = {'cat': tdate, 'tv': ttime, 'tactic': 0}
                        else:
                            group_dates[g][tdate]['tv'] = group_dates[g][tdate]['tv'] + ttime
                    if tdate not in all_dates.keys():
                        all_dates[tdate] = {'cat': tdate, 'tv': ttime, 'tactic': 0}
                    else:
                        all_dates[tdate]['tv'] = all_dates[tdate]['tv'] + ttime
            if tlogin in work_hour_data.keys():
                for tdict in work_hour_data[tlogin]:
                    day = tdict.get('day')
                    amt = tdict.get('straight_time')
                    if day < date2 and day > date1:
                        if day not in user_dates[name]['dates'].keys():
                            user_dates[name]['dates'][day] = {'cat': day, 'tv': 0, 'tactic': amt}
                        else:
                            user_dates[name]['dates'][day]['tactic'] = user_dates[name]['dates'][day]['tactic'] + amt
                        for g in ugroups:
                            if g not in group_dates.keys():
                                group_dates[g] = {}
                            if day not in group_dates[g].keys():
                                print "DAY = %s, Group Dates Keys = %s" % (day, group_dates[g].keys())
                                group_dates[g][day] = {'cat': day, 'tv': 0, 'tactic': amt}
                                print "GROUP DATES KEYS = %s" % group_dates[g].keys()
                            else:
                                print "GROUP_DATES[%s][%s]['tactic'] = %s, amt = %s" % (g, day, group_dates[g][day]['tactic'], amt)
                                group_dates[g][day]['tactic'] = group_dates[g][day]['tactic'] + amt
                                print "GROUP_DATES[%s][%s]['tactic'] = %s" % (g, day, group_dates[g][day]['tactic'])
                        if day not in all_dates.keys():
                            all_dates[day] = {'cat': day, 'tv': 0, 'tactic': amt}
                        else:
                            all_dates[day]['tactic'] = all_dates[day]['tactic'] + amt
        print "GROUP DATES = %s" % group_dates
        d1s = date1.split('-')
        d2s = date2.split('-')
        d1 = date(int(d1s[0]),int(d1s[1]),int(d1s[2]))
        d2 = date(int(d2s[0]),int(d2s[1]),int(d2s[2]))

        delta = d2 - d1
        dates_to_fill = []
        for i in range(delta.days + 1):
            dates_to_fill.append('%s' % (d1 + td(days=i)))

        users = user_dates.keys()
        idx = 0
        for user in users:
            udkeys = user_dates[user]['dates'].keys()
            if len(udkeys) > 0:
                for dtf in dates_to_fill:
                    found = False
                    for d, l in user_dates[user]['dates'].iteritems():
                        if d == dtf:
                            found = True
                    if not found:
                        user_dates[user]['dates'][dtf] = {'cat': dtf, 'tactic': 0, 'tv': 0}
        for grp, gdata in group_dates.iteritems():
            for dtf in dates_to_fill:
                found = False
                for d, l in group_dates[grp].iteritems():
                    if d == dtf:
                        found = True
                if not found:
                    group_dates[grp][dtf] = {'cat': dtf, 'tactic': 0, 'tv': 0}
        for dtf in dates_to_fill:
            found = False
            for d, l in all_dates.iteritems():
                if d == dtf:
                    found = True
            if not found:
                all_dates[dtf] = {'cat': dtf, 'tactic': 0, 'tv': 0}
        #print "LOGIN GROUPS = %s" % login_groups
        filtbl = Table()
        filtbl.add_row()
        date1_el = CalendarInputWdg("wh_graph_date1")
        date1_el.set_option('show_activator',True) 
        date1_el.set_option('show_confirm', False)
        date1_el.set_option('show_text', True)
        date1_el.set_option('show_today', False)
        date1_el.set_option('show_value', True)
        date1_el.set_option('read_only', False)    
        if date1 not in [None,'']:
            date1_el.set_option('default', date1)
        date1_el.get_top().add_style('width: 150px')
        date1_el.set_persist_on_submit()
        
        date2_el = CalendarInputWdg("wh_graph_date2")
        date2_el.set_option('show_activator',True) 
        date2_el.set_option('show_confirm', False)
        date2_el.set_option('show_text', True)
        date2_el.set_option('show_today', False)
        date2_el.set_option('show_value', True)
        date2_el.set_option('read_only', False)    
        if date2 not in [None,'']:
            date2_el.set_option('default', date2)
        date2_el.get_top().add_style('width: 150px')
        date2_el.set_persist_on_submit()
 
        f1 = filtbl.add_cell(' ')
        f11 = filtbl.add_cell(' Date 1: ')
        f2 = filtbl.add_cell(date1_el)
        f21 = filtbl.add_cell(' Date 2: ')
        f3 = filtbl.add_cell(date2_el)
        f4 = filtbl.add_cell('<input type="button" value="Load Graph" name="not_yo_date"/>') 
        f4.add_style('cursor: pointer;')
        f4.add_behavior(my.get_load_again())
        f1.add_attr('width','40%%')
        f4.add_attr('width','40%%')
                

        surrounder = Table()
        surrounder.add_attr('width','100%%')
        surrounder.add_attr('class','graph_surrounder')
        surrounder.add_row()
        surrounder.add_cell(filtbl)
        
        table = Table()
        table.add_attr('width','100%%')
        table.add_attr('class','graph_top')
        table.add_style('background-color: #60ca9d;')
        lgroupkeys = login_groups.keys()
        arr = []
        # Need to show this one for elites only
        # Show supervisors their department's
        # Show individuals their own
        # Try to implement drop-downs
        for d, l in all_dates.iteritems():
            arr.append(l)
        if len(arr) > 0:
            arr2 = sorted(arr, key=lambda k: k['cat']) 
            acount = 0
            for a1 in arr2:
                percentage = 0
                tv = float(a1.get('tv'))
                tc = float(a1.get('tactic'))
                if tv != 0:
                    percentage = tc/tv * 100
                    pps = '%.2f' % percentage
                    percentage = float(pps)
                if percentage > 100:
                    percentage = 100
                a1['percentage'] = percentage
                arr2[acount] = a1
                acount = acount + 1
            widget = DivWdg("Chart area 2")
            widget.add_attr('id','chartdiv_%s'%idx)
            str_data = my.make_string_dict(arr2)
            widget.add_attr('datastr', str_data)
            widget.add_styles('width: 100%%;height: 200px;')
            my.draw_chart3(widget, idx, 'All')
            table.add_row()
            tc = table.add_cell(widget)
            tc.add_attr('width','100%%')
            tc.add_attr('title','ALL')
            idx = idx + 1
        groups = group_dates.keys()
        for group in groups:
            grptbl = Table()
            grptbl.add_attr('width','100%%')
            grptbl.add_style('background-color: #a1b3e6;')
            #print "GROUP = %s" % group
            arr = []
            for d, l in group_dates[group].iteritems():
                arr.append(l)
            if len(arr) > 0:
                arr2 = sorted(arr, key=lambda k: k['cat']) 
                acount = 0
                for a1 in arr2:
                    percentage = 0
                    tv = float(a1.get('tv'))
                    tc = float(a1.get('tactic'))
                    if tv != 0:
                        percentage = tc/tv * 100
                        pps = '%.2f' % percentage
                        percentage = float(pps)
                    if percentage > 100:
                        percentage = 100
                    a1['percentage'] = percentage
                    arr2[acount] = a1
                    acount = acount + 1
                     
                widget = DivWdg("Chart area 2")
                widget.add_attr('id','chartdiv_%s'%idx)
                str_data = my.make_string_dict(arr2)
                widget.add_attr('datastr', str_data)
                widget.add_styles('width: 100%%;height: 200px;')
                my.draw_chart3(widget, idx, group)
                grptbl.add_row()
                tc = grptbl.add_cell(widget)
                tc.add_attr('width','100%%')
                tc.add_attr('title',group)
                grptbl.add_row()
                opener = grptbl.add_cell('<b><u>Show Users</u></b>')
                opener.add_style('cursor: pointer;')
                toggle_row_behavior = my.get_toggle_row_behavior(group)
                opener.add_behavior(toggle_row_behavior)
                idx = idx + 1
            grpusers = 0
            usertbl = Table()
            usertbl.add_attr('width','100%%')
            usertbl.add_style('background-color: #c8d0e7;')
            for user in users:
                if user in name_to_login.keys():
                    login_name = name_to_login[user] 
                    #print "USER = %s, LOGIN NAME = %s" % (user, login_name)
                    if login_name in lgroupkeys:
                        lgroups = []
                        lgroups = login_groups[login_name]
                        #print "GROUP = %s, USER = %s, LGROUPS = %s" % (group, user, lgroups)
                        #print "LOGIN GROUPS = %s" % login_groups
                        if group in lgroups:
                            arr3 = []
                            for d, l in user_dates[user]['dates'].iteritems():
                                arr3.append(l)
                            if len(arr) > 0:
                                arr4 = sorted(arr3, key=lambda k: k['cat']) 
                                acount = 0
                                for a1 in arr4:
                                    percentage = 0
                                    tv = float(a1.get('tv'))
                                    tc = float(a1.get('tactic'))
                                    if tv != 0:
                                        percentage = tc/tv * 100
                                        pps = '%.2f' % percentage
                                        percentage = float(pps)
                                    if percentage > 100:
                                        percentage = 100
                                    a1['percentage'] = percentage
                                    arr4[acount] = a1
                                    acount = acount + 1
                                widget = DivWdg("Chart area 2")
                                widget.add_attr('id','chartdiv_%s'%idx)
                                str_data = my.make_string_dict(arr4)
                                widget.add_attr('datastr', str_data)
                                widget.add_styles('width: 100%%;height: 200px;')
                                my.draw_chart3(widget, idx, user)
                                if grpusers % 2 == 0:
                                    usertbl.add_row()
                                tc = usertbl.add_cell(widget)
                                tc.add_attr('width','50%%')
                                tc.add_attr('title',user)
                                idx = idx + 1
                                grpusers = grpusers + 1
            if grpusers % 2 == 1:
                te = usertbl.add_cell(' ')
                te.add_attr('width','50%%')
            grprow = grptbl.add_row()
            grprow.add_attr('id','graphs_%s_row' % group)
            grprow.add_style('display: table-row;')
            grptbl.add_cell(usertbl)
            table.add_row()
            table.add_cell(grptbl)
            surrounder.add_row()
            surrounder.add_cell(table)
        return surrounder
