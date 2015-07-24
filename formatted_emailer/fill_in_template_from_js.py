import os, getopt, sys
opts, message = getopt.getopt(sys.argv[1], '-m') 
opts, wo_code = getopt.getopt(sys.argv[2], '-m')
filler = '/var/www/html/formatted_emails/source_issue_%s.html' % wo_code
template = '/opt/spt/custom/formatted_emailer/fill_in_template.html'
just_see = '/var/www/html/formatted_emails/just_see'
#js = open(just_see, 'w')
#js.write(message)
#js.close()
out_arr = []
tp = open(template, 'r')
for line in tp:
    line = line.replace('[MESSAGE]', message)
    out_arr.append(line)
tp.close()

filled_in = open(filler, 'w')
for line in out_arr:
    filled_in.write(line);
filled_in.close()
