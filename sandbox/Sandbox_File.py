__all__ = ["MediaInfoFile"]

import time
import os, shutil
import hashlib
from pyasm.command import Command, CommandException

# Class: MediaInfoFile
# What it does: wait_for_it - waits for a file in case it is being uploaded to the server by comparing its size
# get_md5 - gets md5 of a whole file, not efficient
# get_md5_of_name - duh
# copy2 - wrapper around pythons shutil copy2 function
# get_barcode() - gets a barcode for a filename based on the new_file_name md5

class MediaInfoFile(Command):

    wait_time = 2

    def wait_for_it(my, filepath):

        while not os.path.exists(filepath):
            time.sleep(MediaInfoFile.wait_time)

        while True:
            try:
                old_size = os.stat(filepath).st_size
                time.sleep(MediaInfoFile.wait_time)
                new_size = os.stat(filepath).st_size

                if old_size == new_size:
                    break
            except IOError:
                continue
        return None

    def get_md5(my, file):
        # Hashing of a whole file, quite slow as need to download
        # the whole file
        BUF_SIZE = 512000000  # lets read stuff in 512MB chunks!

        md5 = hashlib.md5()
        sha1 = hashlib.sha1()

        with open(file, 'rb') as f:
            while True:
                data = f.read(BUF_SIZE)
                if not data:
                    break
                md5.update(data)
                sha1.update(data)

        return md5.hexdigest()

    def get_md5_of_name(my, file_name):

        hash_key = "Unknown"

        try:
            if file_name:
                md5 = hashlib.md5()
                md5.update(file_name.encode('utf-8'))
                hash_key = str(md5.hexdigest())

                return hash_key

        except TypeError:

            return hash_key

        finally:

            return hash_key

    def copytree(my, src, dst, symlinks=False, ignore=None):
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, symlinks, ignore)
            else:
                shutil.copy2(s, d)

    def copy2(my, origin = None, destination = None ):

        # Lets move it!
        print "IN COPY2 ORIGIN = %s, DESTINATION = %s" % (origin, destination)
        try:
            if not os.path.isdir(origin):
                shutil.copy2(origin, destination)
            else:
                last_chunk_s = origin.split('/')
                last_chunk = last_chunk_s[len(last_chunk_s) - 1]
                new_destination = '%s/%s' % (destination, last_chunk)
                if not os.path.exists(new_destination):
                    os.makedirs(new_destination)
                my.copytree(origin, new_destination)
        except shutil.Error as e:
            print "ERROR: %s" % e
            pass
        except IOError as e: 
            print "ERROR: %s" % e
            pass
        except:
            print "SOME OTHER ERROR"
            pass

      

    def get_barcode(my, file_name):
            
        # Return: BARCODE_ + file_name 
        new_file_name = str(file_name)

        if not file_name:
            return "Unknown"
        else:
            return 'BARCODE_' + my.get_md5_of_name(str(new_file_name))+'|'+new_file_name

    def execute(my):
        origin = my.kwargs.get('origin')
        destination = my.kwargs.get('destination')
        mode = my.kwargs.get('mode')
        if mode == 'copy2':
           my.copy2(origin=origin,destination=destination)  
        return 'poop'
