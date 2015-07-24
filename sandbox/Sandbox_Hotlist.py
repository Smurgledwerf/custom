__all__ = ["SandboxBigBoardWdg"]
import tacticenv
import time, datetime
#from pyasm.common import Environment
#from pyasm.biz import *
from pyasm.web import Table, DivWdg
from tactic.ui.common import BaseTableElementWdg
from tactic.ui.common import BaseRefreshWdg
#from pyasm.search import Search
#from tactic.ui.widget import DiscussionWdg
#from operator import itemgetter


class SandboxBigBoardWdg(BaseRefreshWdg):
    def init(my):
        from pyasm.common import Environment
        from pyasm.search import Search
        my.login = Environment.get_login()
        my.user = my.login.get_login()

        my.sk = ''
        my.seen_groups = []
        my.bigdict = {}
        my.indi_pct = 0.0
        my.stat_colors = {'Pending':'#d7d7d7','In Progress':'#f5f3a4','In_Progress':'#f5f3a4','On Hold':'#e8b2b8','On_Hold':'#e8b2b8','Client Response': '#ddd5b8', 'Completed':'#b7e0a5','Need Buddy Check':'#e3701a','Ready':'#b2cee8','Internal Rejection':'#ff0000','External Rejection':'#ff0000','Fix Needed':'#c466a1','Failed QC':'#ff0000','Rejected': '#ff0000','DR In_Progress': '#d6e0a4', 'DR In Progress': '#d6e0a4','Amberfin01_In_Progress':'#D8F1A8', 'Amberfin01 In Progress':'#D8F1A8','Amberfin02_In_Progress':'#F3D291', 'Amberfin02 In Progress':'#F3D291','BATON In_Progress': '#c6e0a4', 'BATON In Progress': '#c6e0a4','Export In_Progress': '#796999','Export In Progress': '#796999', 'Buddy Check In_Progress': '#1aade3','Buddy Check In Progress': '#1aade3'}
        my.stat_relevance = {'Pending': 0,'In Progress': 4,'In_Progress': 4,'On Hold': 1,'On_Hold': 1,'Client Response': 2, 'Completed': -1,'Need Buddy Check': 10, 'Buddy Check In_Progress': 11, 'Buddy Check In Progress': 11, 'Ready': 3,'Internal Rejection': 12,'External Rejection': 13,'Failed QC': 14,'Fix Needed': 16,'Rejected': 15,'DR In_Progress': 5, 'DR In Progress': 5,'BATON In_Progress': 8, 'BATON In Progress': 8,'Export In_Progress': 9, 'Export In Progress': 9,'Amberfin01_In_Progress': 6, 'Amberfin01 In Progress': 6, 'Amberfin02_In_Progress':7, 'Amberfin02 In Progress':7 }
        my.timestamp = my.make_timestamp()
        my.date = my.timestamp.split(' ')[0]
        my.real_date = datetime.datetime.strptime(my.date, '%Y-%m-%d')
        my.all_groups = []
        my.big_user = False
        users_s = Search('sthpw/login')
        users_s.add_filter('location','internal')
        users = users_s.get_sobjects()
        my.username_lookup = {'': '', None: '', 'NOTHING': ''}
        for user in users: 
            login_name = user.get_value('login')
            fname = user.get_value('first_name')
            lname = user.get_value('last_name')
            my.username_lookup[login_name] = '%s %s' % (fname, lname)

    def make_timestamp(my):
        import datetime
        now = datetime.datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S")

    def get_title_cell(my):

        # Title:
        # Code:
        # Client:
        # Platform:
        # Deliver By:
        # Due Date:
        # Icon/Icon

        row = DivWdg()
        row.add_class('row')
        
        line_one = DivWdg()
        #line_one.add_style("word-wrap: break-word; word-break:break-all; ")
        line_one.add_class('col-md-10 bg-primary')
        line_one.add("Title: <strong>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</strong> ")
        
        line_two = DivWdg()
        line_two.add_class('col-md-10 bg-success')
        line_two.add("<p>Code: TILE123456789</p> ")
        
        line_three = DivWdg()
        line_three.add_class('col-md-10 bg-info ')
        line_three.add_style("word-wrap: break-word; word-break:break-all;")
        line_three.add("<p>Client: FOXFOXFOXOFXOFXOFOFOXOFOXFOFOXFOXFOXOFXOFXOFOFOXOFOXFO</p> ")

        line_four = DivWdg()
        line_four.add_class('col-md-10 bg-primary ')
        line_four.add_style("word-wrap: break-word; word-break:break-all;")
        line_four.add("<p>Platform: Apple</p> ")

        row.add(line_one)
        row.add(line_two)
        row.add(line_three)

        return row

    def get_container_with_top_row(my):

        # Getting [ Title| Machine Room | Blah | Blah table headings ]

        container = DivWdg()
        container.add_class('container')
        container.add_style('width: 1500px !important;')
        
        top_table_container = DivWdg()
        top_table_container.add_style('overflow-y: scroll !important;')

        top_table = Table()

        top_table.add_class('table table-bordered')
        top_table.add_style('table-layout: fixed;')
        top_table.add_row()
        
        title_cell = top_table.add_cell("Title")
        title_cell.add_class('col-md-1')
       
        second_cell = top_table.add_cell("Machine Room")
        second_cell.add_class('col-md-1')
        
        third_cell = top_table.add_cell("Compression")
        third_cell.add_class('col-md-1')

        fourth_cell = top_table.add_cell("Audio")
        fourth_cell.add_class('col-md-1')

        fifth_cell = top_table.add_cell("QC")
        fifth_cell.add_class('col-md-1')

        sixth_cell = top_table.add_cell("EDel")
        sixth_cell.add_class('col-md-1')

        top_table_container.add(top_table)

        container.add(top_table_container)
        
        return container
        
    

    def get_work_order_columns(my):
        pass

    def add_lower_table_row(my, table):
       
        table.add_row()
        title_column = my.get_title_cell()

        title_cell = table.add_cell()
        title_cell.add_class('col-md-1')
        title_cell.add(title_column)

        return table
 
      
    
    def get_display(my):  


        container = my.get_container_with_top_row()

        overflow_container = DivWdg()
        overflow_container.add_style('height: 600px !important;')
        overflow_container.add_style('overflow-y: scroll !important;')


        top_table_lower = Table()
        top_table_lower.add_class('table table-bordered')
        top_table_lower.add_style('table-layout: fixed;')

        top_table_lower.add_row()

        for i in range(0, 10):
            my.add_lower_table_row(top_table_lower)

        
        overflow_container.add(top_table_lower)

        container.add(overflow_container)
        return container



        



