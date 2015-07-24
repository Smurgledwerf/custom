import os, sys, getopt, shutil, re, time, hashlib

def compareFiles(file1,file2):
    """compares text and binary file content of two files by matching hashes,
    returns 1 if files are different 0 if identical"""
    #comparison is not recursive, sub directories are ignored
    if os.path.isfile(file1) and os.path.isfile(file2):
        x=hashlib.md5()
        y=hashlib.md5()
        x.update(open(file1,'r').read())
        y.update(open(file2,'r').read())
        if x.digest() == y.digest():
            return 0
        else:
            return 1

def any_list1_items_in_list2(list1, list2):
    found_one = False
    
    if isinstance(list1, str):
        temp = list1.split('/')
	if len(temp) < 2:
            temp = list1.split('\\')
	list1 = temp
    for l in list1:
        if l in list2:
            found_one = True
    return found_one

def main(args, login=None):
    folder1 = args[0]
    folder2 = args[1]
    IG_PATHS = 2
    IG_EXTS = 3
    ig_ig_paths = True
    ig_ig_exts = True
    if len(args) > 2:
        if 'ignore_paths=' in args[2]:
            IG_PATHS = 2
	    ig_ig_paths = False
	elif 'ignore_exts=' in args[2]:
	    IG_EXTS = 2
	    ig_ig_exts = False
	if len(args) > 3:
            if 'ignore_paths=' in args[3]:
                IG_PATHS = 3
		ig_ig_paths = False
	    elif 'ignore_exts=' in args[3]:
		ig_ig_exts = False
                IG_EXTS = 3

    ignore_paths = []
    ignore_exts = []
    if not ig_ig_paths:
        ignore_paths_str = args[IG_PATHS].replace('ignore_paths=','')
        ignore_paths = ignore_paths_str.split(',')
	print "USING IGNORE PATHS. ITEMS = %s" % ignore_paths
    if not ig_ig_exts:
        ignore_exts_str = args[IG_EXTS].replace('ignore_exts=','')
        ignore_exts = ignore_exts_str.split(',')
	print "USING IGNORE EXTS. ITEMS = %s" % ignore_exts

    folder1_paths = {}
    folder2_paths = {}
    folder1_seen = []
    folder2_seen = []
    matching = []
    different = []
    folder1_not_found_in_2 = []
    folder2_not_found_in_1 = []
    
    check_length = False
    if 'length' in ignore_exts:
        check_length = True

    for root, subfolders, files in os.walk(folder1):
        for file1 in files:
	    full_path = os.path.join(root, file1)
	    if not any_list1_items_in_list2(full_path, ignore_paths):
	        ext_s = file1.split('.')
	        ext = ext_s[len(ext_s) - 1]
                if not check_length or check_length and len(ext) < 5:
	            if ext not in ignore_exts:
	                x= hashlib.md5()
	                x.update(open(full_path,'r').read())
	                md5er = x.digest()
	                trimmed_path = folder1.join(full_path.split(folder1)[1:])
	                if trimmed_path not in folder1_paths.keys():
                            folder1_paths[trimmed_path] = md5er

    for root, subfolders, files in os.walk(folder2):
        for file2 in files:
	    full_path = os.path.join(root, file2)
	    if not any_list1_items_in_list2(full_path, ignore_paths):
	        ext_s = file2.split('.')
	        ext = ext_s[len(ext_s) - 1]
                if not check_length or check_length and len(ext) < 5:
	            if ext not in ignore_exts:
	                x= hashlib.md5()
	                x.update(open(full_path,'r').read())
	                md5er = x.digest()
	                trimmed_path = folder2.join(full_path.split(folder2)[1:])
	                if trimmed_path not in folder2_paths.keys():
                            folder2_paths[trimmed_path] = md5er

    f1s = folder1_paths.keys()
    f2s = folder2_paths.keys()
    for path in f1s:
        if path in f2s:
	    if folder1_paths[path] == folder2_paths[path]:
	        matching.append(path)
	    else:
	        different.append(path)
        else:
            folder1_not_found_in_2.append(path)

    for path in f2s:
        if path in f1s:
	    if folder2_paths[path] == folder1_paths[path]:
	        if path not in matching:
	            matching.append(path)
	    else:
	        if path not in different:
	            different.append(path)
        else:
            folder2_not_found_in_1.append(path)

    print "\n\nTHE FOLLOWING FILES WERE IN %s, and not in %s" % (folder1, folder2)
    for guy in folder1_not_found_in_2:
        print guy

    print "\n\nTHE FOLLOWING FILES WERE IN %s, and not in %s" % (folder2, folder1)
    for guy in folder2_not_found_in_1:
        print guy

    print "\n\nThe MD5's for the following files did not match. Total Count: %s" % len(different)
    for guy in different:
        print guy

    print "\n\nTHE following MD5's matched. Total Count: %s" % len(matching)
    for guy in matching:
        print guy

    print "\n\nEXECUTOR:"
    for guy in different:
        print 'vim -d "%s%s" "%s%s"' % (folder1, guy, folder2, guy)

    for guy in different:
        os.system('vim -d "%s%s" "%s%s"' % (folder1, guy, folder2, guy))
        #os.system('gvim -d "%s%s" "%s%s"' % (folder1, guy, folder2, guy)) # use this one for windows

if __name__ == '__main__':
    
    login = None
    try:
        opts, args = getopt.getopt(sys.argv[1:], "l:h", ["login=","help"])
        print args
    except getopt.error, msg:
        print msg
        sys.exit(2)
    # process options
    for o, a in opts:
        if o in ("-l", "--login"):
            login = a
            print 
        if o in ("-h", "--help"):
            print "python merger_md5s.py folder1 folder2 (optional ignore_paths=comma_seperated_list_of_folders_to_ignore and ignore_exts=comma_seperated_list_of_extensions_to_ignore)"
   
    if len(args) < 2:
        print "python merger_md5s.py folder1 folder2 (optional ignore_paths=comma_seperated_list_of_folders_to_ignore and ignore_exts=comma_seperated_list_of_extensions_to_ignore)"
        sys.exit(2)
    main(args, login=login)

