__all__ = ["DashboardReRunCmd"]
import os, subprocess
from pyasm.command import Command, CommandException

class DashboardReRunCmd(Command): 
    def execute(my):
        print "GOING TO RERUN REPORTS"
        #os.system('python /opt/spt/custom/reports/dashboard_reports/dashboard_report.py admin 10 20 > /tmp/spitout')
        subprocess.Popen(["python", "/opt/spt/custom/reports/dashboard_reports/dashboard_report.py", "admin", "10", "20"])
