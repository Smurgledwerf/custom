import os, sys, calendar, dateutil, datetime, time, getopt, hashlib, pprint, stat
from file_info_class import FileInfo

def getInfos(currentDir):
    f = None
    root = None
    infos = []
    bad_guys = []
    try:
        for root, dirs, files in os.walk(currentDir): # Walk directory tree
            for f in files:
                infos.append(FileInfo(f,root))
    except:
        bad_guys.append("COULD NOT GET INFO FOR %s/%s" % (root,f))
        pass 
    return [infos,bad_guys]

def demystify_stats(stats_in):
    spit = str(stats_in).split(' ')
    info_pack = {}
    for s in spit:
        if '(' in s:
            s = s.split('(')[1]
        if ')' in s:
            s = s.split(')')[0]
        s = s.replace(',','')
        kv = s.split('=')
        key = kv[0]
        val = kv[1]
        if 'time' in key:
            val = datetime.datetime.fromtimestamp(int(val)).strftime('%Y-%m-%d %H:%M:%S') 
        #if 'mode' in key:
            #val = stat.filemode(int(val))
        info_pack[key.replace('st_','')] = val
    return info_pack

def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

def print_info(name, keys, dict, all_info):
    for k in keys:
        entry = dict[k]
        count = len(entry)
        print "%s: %s -- COUNT: %s" % (name, k, count)
        for e in entry:
            print "Size: %s\t File: %s" % (all_info[e]['size'], e)
        print "\n\n"

chunk = getInfos('/Volumes/Iris/CLIENTS/DREAMWORKS_ANIMATION')
infos = chunk[0]
badones = chunk[1]
seen = []
tab_count = 0
tabs = ''
all_info = {}
data_arr = []
for info in infos:
    if info.filepath not in seen:
        full_path = '%s%s' % (info.filepath, info.filename)
        print '\n'
        seen.append(info.filepath)
        print info.filepath
        tab_count = len(info.filepath)/8 + 1
        tabs = ''
        for i in range(0, tab_count):
            tabs = '%s\t' % tabs
        info_pack = demystify_stats(info.stats) 
        info_pack['size'] = sizeof_fmt(int(info.filesize))
        info_pack['file'] = full_path
        all_info[full_path] = info_pack 
        data_arr.append(info_pack)
    #print '%s%s\t%s\t%s\t%s' % (tabs, info.filename, info.filesize, info.md5, info.stats)
    print '%s%s\t%s\t%s' % (tabs, info.filename, info.filesize, info_pack)
from operator import itemgetter
newlist = sorted(data_arr, key=itemgetter('mtime')) 
newlist = newlist[::-1]
print all_info
print newlist
pp = pprint.PrettyPrinter(depth=3)
for dude in newlist:
    print dude['file']
    pp.pprint(dude)
by_atime = {}
by_ctime = {}
by_mtime = {}
by_size = {}
by_uid = {}
by_dev = {}
by_gid = {}
by_nlink = {}
by_mode = {}
by_ino = {}
for dude in newlist:
    full_path = dude['file']
    atime = dude['atime']
    try:
        by_atime[atime].append(full_path)
    except:
        by_atime[atime] = [full_path]    
        pass
    ctime = dude['ctime']
    try:
        by_ctime[ctime].append(full_path)
    except:
        by_ctime[ctime] = [full_path]    
        pass
    mtime = dude['mtime']
    try:
        by_mtime[mtime].append(full_path)
    except:
        by_mtime[mtime] = [full_path]    
        pass
    size = dude['size']
    try:
        by_size[size].append(full_path)
    except:
        by_size[size] = [full_path]    
        pass
    uid = dude['uid']
    try:
        by_uid[uid].append(full_path)
    except:
        by_uid[uid] = [full_path]    
        pass
    dev = dude['dev']
    try:
        by_dev[dev].append(full_path)
    except:
        by_dev[dev] = [full_path]    
        pass
    gid = dude['gid']
    try:
        by_gid[gid].append(full_path)
    except:
        by_gid[gid] = [full_path]    
        pass
    nlink = dude['nlink']
    try:
        by_nlink[nlink].append(full_path)
    except:
        by_nlink[nlink] = [full_path]    
        pass
    mode = dude['mode']
    try:
        by_mode[mode].append(full_path)
    except:
        by_mode[mode] = [full_path]    
        pass
        
atime_keys = by_atime.keys()
atime_keys = sorted(atime_keys)
ctime_keys = by_ctime.keys()
ctime_keys = sorted(ctime_keys)
mtime_keys = by_mtime.keys()
mtime_keys = sorted(mtime_keys)
size_keys = by_size.keys()
size_keys = sorted(size_keys)
uid_keys = by_uid.keys()
uid_keys = sorted(uid_keys)
dev_keys = by_dev.keys()
dev_keys = sorted(dev_keys)
gid_keys = by_gid.keys()
gid_keys = sorted(gid_keys)
nlink_keys = by_nlink.keys()
nlink_keys = sorted(nlink_keys)
mode_keys = by_mode.keys()
mode_keys = sorted(mode_keys)

print_info("ATIME", atime_keys, by_atime, all_info)    
print_info("CTIME", ctime_keys, by_ctime, all_info)    
print_info("MTIME", mtime_keys, by_mtime, all_info)    
print_info("SIZE", size_keys, by_size, all_info)    
print_info("UID", uid_keys, by_uid, all_info)    
print_info("DEV", dev_keys, by_dev, all_info)    
print_info("GID", gid_keys, by_gid, all_info)    
print_info("NLINK", nlink_keys, by_nlink, all_info)    
print_info("MODE", mode_keys, by_mode, all_info)    
print "COULD NOT READ: %s" % badones




