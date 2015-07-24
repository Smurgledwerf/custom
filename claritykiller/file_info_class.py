import hashlib, os
class FileInfo:

    def __init__(self, filename, filepath):
        
        self.filename = filename
        self.filepath = filepath
        self.fullpath = '%s/%s' % (filepath, filename)
        #self.mdd = hashlib.md5()
        #self.mdd.update(open(self.fullpath,'r').read())
        #self.md5 = self.mdd.hexdigest()
        self.filesize = os.path.getsize(self.fullpath)
        self.stats = os.stat(self.fullpath)
