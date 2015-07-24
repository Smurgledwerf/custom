import os, sys, math, hashlib, getopt, tacticenv
from tactic_client_lib import TacticServerStub
opts, last_passed_in = getopt.getopt(sys.argv[1], '-m')
print "LAST PASSED IN = %s" % last_passed_in
last_passed_in = int(last_passed_in)
server = TacticServerStub.get(protocol="xmlrpc")
title_pipes = server.eval("@SOBJECT(sthpw/pipeline['search_type','twog/title']['@ORDER_BY','code'])")
pipes = {}
tp_count = 0
for tp in title_pipes:
    tp_name = tp.get('code')
    print "PIPELINE = %s (%s)" % (tp_name, tp_count)
    if tp_count >= last_passed_in:
        if tp_name not in pipes.keys():
            pipes[tp_name] = {'titles_with_pipe': 0, 'nohack_wo_count': 0, 'nohack_qc_wo_count': 0, 'hack_wo_count': 0, 'hack_qc_wo_count': 0, 'avg_nohack_wo_count': 0.0, 'avg_nohack_qc_wo_count': 0.0, 'avg_hack_wo_count': 0.0, 'avg_hack_qc_wo_count': 0.0, 'oldest_date': '', 'newest_date': ''} 
        titles = server.eval("@SOBJECT(twog/title['pipeline_code','%s']['@ORDER_BY','code'])" % tp_name)
        pipes[tp_name]['titles_with_pipe'] = len(titles)
        highest_nhwc = 0
        highest_nhqwc = 0
        highest_hwc = 0
        highest_hqwc = 0
        sum_nhwc = 0
        sum_nhqwc = 0
        sum_hwc = 0
        sum_hqwc = 0
        newest_date = '2000-01-01 00:00:00'
        oldest_date = '2020-01-01 00:00:00'
        count = 1
        titlen = len(titles)
        for title in titles:
            timestamp = title.get('timestamp')
            if timestamp < oldest_date:
                oldest_date = timestamp
            if timestamp > newest_date:
                newest_date = timestamp
            title_code = title.get('code')
            print "DOING %s of %s (%s)" % (count, titlen, title_code)

            nwos = server.eval("@GET(twog/proj['title_code','%s'].twog/work_order['creation_type','N'].work_group)" % title_code)
            nwos_len = len(nwos)
            nwos_qc_len = 0
            for n in nwos:
                if n in ['qc','qc supervisor']:
                    nwos_qc_len = nwos_qc_len + 1
            sum_nhwc = sum_nhwc + nwos_len
            sum_nhqwc = sum_nhqwc + nwos_qc_len

            hwos = server.eval("@GET(twog/proj['title_code','%s'].twog/work_order['creation_type','hackup'].work_group)" % title_code)
            hwos_len = len(hwos)
            hwos_qc_len = 0
            for h in hwos:
                if h in ['qc','qc supervisor']:
                    hwos_qc_len = hwos_qc_len + 1
            sum_hwc = sum_hwc + hwos_len
            sum_hqwc = sum_hqwc + hwos_qc_len

            if nwos_len > highest_nhwc:
                highest_nhwc = nwos_len
            if nwos_qc_len > highest_nhqwc:
                highest_nhqwc = nwos_qc_len
            if hwos_len > highest_hwc:
                highest_hwc = hwos_len
            if hwos_qc_len > highest_hqwc:
                highest_hqwc = hwos_qc_len

            count = count + 1
        actual_count = count - 1
        if actual_count == 0:
            actual_count = 1
        pipes[tp_name]['nohack_wo_count'] = highest_nhwc
        pipes[tp_name]['nohack_qc_wo_count'] = highest_nhqwc
        pipes[tp_name]['hack_wo_count'] = highest_hwc
        pipes[tp_name]['hack_qc_wo_count'] = highest_hqwc
        pipes[tp_name]['avg_nohack_wo_count'] = float(float(sum_nhwc)/float(actual_count))
        pipes[tp_name]['avg_nohack_qc_wo_count'] = float(float(sum_nhqwc)/float(actual_count))
        pipes[tp_name]['avg_hack_wo_count'] = float(float(sum_hwc)/float(actual_count))
        pipes[tp_name]['avg_hack_qc_wo_count'] = float(float(sum_hqwc)/float(actual_count))
        pipes[tp_name]['newest_date'] = newest_date
        pipes[tp_name]['oldest_date'] = oldest_date
        
        os.system('''echo "\n%s: %s Titles [ (%s) - (%s) ]\n" >> pipes_info''' % (tp_name, titlen, oldest_date, newest_date))
        os.system('''echo "HIGHS\t\tAVG\n" >> pipes_info''')
        os.system('''echo "NORMAL WO Count: %s\t\t%s" >> pipes_info''' % (pipes[tp_name]['nohack_wo_count'], pipes[tp_name]['avg_nohack_wo_count']))
        os.system('''echo "NORMAL QC WO Count: %s\t\t%s" >> pipes_info''' % (pipes[tp_name]['nohack_qc_wo_count'], pipes[tp_name]['avg_nohack_qc_wo_count']))
        os.system('''echo "MANUAL WO Count: %s\t\t%s" >> pipes_info''' % (pipes[tp_name]['hack_wo_count'], pipes[tp_name]['avg_hack_wo_count']))
        os.system('''echo "MANUAL QC WO Count: %s\t\t%s" >> pipes_info''' % (pipes[tp_name]['hack_qc_wo_count'], pipes[tp_name]['avg_hack_qc_wo_count']))
    tp_count = tp_count + 1

print "PRINTING..."
out = open('pipes_info2', 'w')
pipes_sorted = pipes.keys()
pipes_sorted.sort()
for p in pipes_sorted:
    pipe = pipes[p]
    out.write('%s: %s Titles\n [ (%s) - (%s) ]' % (p, pipe['titles_with_pipe'], pipe['oldest_date'], pipe['newest_date']))
    out.write('HIGHS\t\t\t\t\tAVG\n')
    out.write('Normal WO Count: %s\t' % pipe['nohack_wo_count'])  
    out.write('Normal QC WO Count: %s\t' % pipe['nohack_qc_wo_count'])  
    out.write('Manual WO Count: %s\t' % pipe['hack_wo_count'])  
    out.write('Manual QC WO Count: %s\t' % pipe['hack_qc_wo_count'])  
    out.write('Normal WO Count: %s\t' % pipe['avg_nohack_wo_count'])  
    out.write('Normal QC WO Count: %s\t' % pipe['avg_nohack_qc_wo_count'])  
    out.write('Manual WO Count: %s\t' % pipe['avg_hack_wo_count'])  
    out.write('Manual QC WO Count: %s\t' % pipe['avg_hack_qc_wo_count'])  
    out.write('\n')
out.close()
    

    
