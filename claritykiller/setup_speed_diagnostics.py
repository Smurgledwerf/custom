import os, sys, calendar, dateutil, datetime, time, getopt, hashlib
from file_info_class import FileInfo

def getInfos(currentDir):
    infos = []
    for root, dirs, files in os.walk(currentDir): # Walk directory tree
        for f in files:
            infos.append(FileInfo(f,root))
    return infos

def spaces(num):
    spc = ''
    for i in range(0,num):
        spc = '%s ' % spc
    return spc

infos = getInfos('/opt/spt/tactic_test')
seen = []
identity_number = 0
tally = '/var/www/html/tally_count'
for info in infos:
    if info.fullpath not in seen:
        seen.append(info.fullpath)
        if '.py' in info.filename and '.pyc' not in info.filename:
            print "INFO.FULLPATH = %s" % info.fullpath
            line_num = 0
            file = open(info.fullpath,'r')
            file_out = []
            commented = False 
            unset_commented = False
            search_found = False
            search_end_found = False
            search_tabs = 0
            build_line = ''
            eval_found = False
            added_import = False
            in_if = []
            if_tabs = 0
            return_found = False
            return_line = ''
            build_placed = False
            search_if_lock = [] 
            hash_beginning = False
            for line in file:
                line_num = line_num + 1
                line = line.rstrip('\r\n')
                line = line.replace('\t','        ')
                line2 = line
                print "%s: %s -- %s" % (line_num, in_if, line)
                #if line not in ['\n','\r','\r\n','']:
                line_tabs = 0
                for c in line:
                    if c == ' ':
                        line_tabs = line_tabs + 1  
                    elif c == '#' and not commented:
                        commented = True
                        unset_commented = True
                        hash_beginning = True
                        print "HASH BEGINNING: %s" % line
                        break
                    else:
                        hash_beginning = False
                        break
                if unset_commented:
                    commented = False
                    unset_commented = False
                if return_found:
                    return_found = False
                    search_end_found = True
                if not build_placed:
                    print "SEARCH IF LOCK = %s, IN IF = %s, line_tabs = %s" % (search_if_lock, in_if, line_tabs)
                    if search_end_found and line_tabs != 0 and line_tabs <= search_tabs and not hash_beginning and 'return' not in line:
                        if len(in_if) == 0 or (len(in_if) > 0 and line_tabs <= in_if[len(in_if) - 1] and search_if_lock == in_if and line_tabs <= search_tabs and not('else' in line or 'elif' in line)):
                            if len(in_if) > 0:
                                print "line_tabs = %s, in_if[len(in_if) - 1] = %s, search_if_lock = %s, in_if = %s" % (line_tabs, in_if[len(in_if) - 1], search_if_lock, in_if)
                            #append the print line here. Use search_tabs to know how far in it must be printed
                            timer_name = 'timer_%s_end_diff' % identity_number
                            build_line = '''%s TIME: %s%s""" >> %s' %s %s)''' % (build_line, '%', 's', tally, '%', timer_name)
                            file_out.append('%s%s = time.time() - timer_%s_begin' % (spaces(search_tabs), timer_name, identity_number))
                            file_out.append('%s%s' % (spaces(search_tabs), build_line))
                            if return_line != '':
                                file_out.append(return_line)
                                return_line = ''
                            search_found = False
                            search_end_found = False 
                            search_tabs = 0
                            build_line = ''
                            if len(in_if) > 0:
                                in_if.pop()
                            build_placed = True
                                
                    if eval_found:
                        #append the print line here. Use search_tabs to know how far in it must be printed
                        timer_name = 'timer_%s_end_diff' % identity_number
                        build_line = '''%s TIME: %s%s""" >> %s' %s %s)''' % (build_line, '%', 's', tally, '%', timer_name)
                        file_out.append('%s%s' % (spaces(search_tabs), build_line))
                        eval_found = False
                        search_tabs = 0
                        build_line = ''
                        build_placed = True
                    
                if not added_import:
                    if 'import ' in line:
                        file_out.append('%simport os, time' % spaces(line_tabs))
                        added_import = True

                trip_split = line.split("'''")
                #if len(trip_split) not in [1,3]:
                #    trip_split = line.split('"""')
                if len(trip_split) != 2:
                    trip_split = line.split('"""')
                if not commented and len(trip_split) == 2:
                    commented = True
                elif commented and len(trip_split) == 2:
                    unset_commented = True
                #if len(trip_split) in [0,2,4]:
                #    print "LEN = %s TRIP_SPLIT = %s" % (len(trip_split), trip_split) 
                #    print "LINE = %s" % line
                #    print "Commented = %s" % commented
                if 'if ' in line and ':' in line and 'elif ' not in line:
                    #in_if = True
                    if_tabs = line_tabs
                    if len(in_if) == 0:
                        in_if.append(if_tabs)
                    elif if_tabs > in_if[len(in_if) - 1]:
                        in_if.append(if_tabs)
                elif len(in_if) > 0 and line_tabs <= in_if[len(in_if) - 1] and not ('else' in line or 'elif' in line):
                    #in_if = False
                    in_if.pop()
                if not commented:
                    if 'server.eval' in line or '= Search(' in line or '=Search(' in line :
                        # surround the line with a timer and time the search
                        # grab the search expression or whatever
                        # print file, identity_number, expression and time to "/var/www/html/tally_count"
                        identity_number = identity_number + 1
                        build_line = '''os.system('echo """MTM-%s: MTM_%s [[''' % (info.fullpath, identity_number) 
                        #in_if = False
                        build_placed = False
                        search_end_found = False
                        if 'server.eval' in line:
                            search_tabs = line_tabs
                            search_if_lock = in_if
                            eval_found = True
                            split1 = line.split('server.eval(')[1]
                            split2 = split1.split(')')
                            search_str = ''.join(split2[0:len(split2) - 1])
                            search_str = search_str.replace("'","").replace('"','').replace('%','')
                            build_line = '%s%s' % (build_line, search_str)
                        else:
                            #add timer setup line above this line
                            build_line = '%s Search: ' % build_line
                            search_tabs = line_tabs
                            search_if_lock = in_if
                            search_found = True
                        if len(search_if_lock) > 0:
                            search_if_lock.pop()
                        file_out.append('%stimer_%s_begin = time.time()' % (spaces(line_tabs), identity_number))
                        file_out.append(line)
                        if 'server.eval' in line:
                            file_out.append('%stimer_%s_end_diff = time.time() - timer_%s_begin' % (spaces(search_tabs), identity_number, identity_number))
                    elif search_found and '.add_op_filters(' in line or '.add_filters(' in line or '.add_filter(' in line or '.add_regex_filter(' in line or '.add_where(' in line:
                        split1 = line.split('(')[1]
                        split2 = split1.split(')')
                        search_str = ''.join(split2[0:len(split2) - 1])
                        search_str = search_str.replace("'","").replace('"','').replace('%','')
                        build_line = '%s %s' % (build_line, search_str)
                        file_out.append(line)
                    elif search_found and '.get_sobjects(' in line or '.get_sobject(' in line or '.get_by_search(' in line:
                        build_line = '%s]]<-GET ' % build_line
                        search_end_found = True
                        file_out.append(line)
                    elif ('return ' in line or ' def ' in line) and search_found and len(in_if) == 0:
                        return_line = line
                        return_found = True
                    else:
                        file_out.append(line)
                else:
                    file_out.append(line)
            #else:
            #    file_out.append(line)
    
            #Here move the original file to .MTMBAK, then write the new file out to the old file name 
            file.close()
            os.system('mv %s %s.MTMBAK' % (info.fullpath, info.fullpath.replace('.py','')))
            new_file = open(info.fullpath, 'w')
            for line in file_out:
                new_file.write('%s\n' % line)
            new_file.close()
