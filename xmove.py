#!c:/SDK/Anaconda2/pythonw.exe

from __future__ import print_function, unicode_literals

import os.path
from win32com.shell import shell, shellcon
import sys
import traceback
#import tracert
import datetime

LOGS_PATH = r''

def logs(data, logfile = None):
    logfile = logfile or os.path.join(os.path.dirname(__file__), 'xmove.log')
    if os.path.isfile(logfile):
        LOGS_PATH = logfile
    else:
        LOGS_PATH = open(logfile, 'wb')
        LOGS_PATH.close()
        LOGS_PATH = logfile
    f = open(LOGS_PATH, 'a')
    f.write(datetime.datetime.strftime(datetime.datetime.now(), '%d-%m-%Y %H:%M:%S') + " " + str(data) + "\n")
    f.close()

def win32_shellcopy(src, dest):
    """
    Move files and directories using Windows shell.

    :param src: Path or a list of paths to copy. Filename portion of a path
                (but not directory portion) can contain wildcards ``*`` and
                ``?``.
    :param dst: destination directory.
    :returns: ``True`` if the operation completed successfully,
              ``False`` if it was aborted by user (completed partially).
    :raises: ``WindowsError`` if anything went wrong. Typically, when source
             file was not found.

    .. seealso:
        `SHFileperation on MSDN <http://msdn.microsoft.com/en-us/library/windows/desktop/bb762164(v=vs.85).aspx>`
    """
    #if isinstance(src, basestring):  # in Py3 replace basestring with str
    if isinstance(src, str):  # in Py3 replace basestring with str
        src = os.path.abspath(src)
    else:  # iterable
        src = '\0'.join(os.path.abspath(path) for path in src)
    
    result, aborted = shell.SHFileOperation((
                               0,
                               shellcon.FO_MOVE,
                               src,
                               os.path.abspath(dest),
                               shellcon.FOF_NOCONFIRMMKDIR,  # flags
                                   None,
                                   None))
                           
    if not aborted and result != 0:
        # Note: raising a WindowsError with correct error code is quite
        # difficult due to SHFileOperation historical idiosyncrasies.
        # Therefore we simply pass a message.
        raise WindowsError('SHFileOperation failed: 0x%08x' % result)

    return not aborted

def start_move(path = None, dest = None, recursive = False):
    if not path:
        path = os.getcwd()
    if not dest:
        dest = sys.argv[-1]
    if not recursive:
        list_dir = os.listdir(path)
        data = 'MOVE: "{0}" --> "{1}"'.format("; ".join(list_dir), str(dest))
        logs(data)
        try:
            win32_shellcopy(list_dir, dest)
        except:
            data = traceback.format_exc()
            logs(data)
    else:
        list_dir = []
        for root, dirs, files in os.walk(path):
            if files:
                for i in files:
                    list_dir.append(os.path.join(root, i))
                    
        data = 'MOVE: "{0}" --> "{1}"'.format("; ".join(list_dir), str(dest))
        logs(data)
        try:
            win32_shellcopy(list_dir, dest)
        except:
            data = traceback.format_exc()
            logs(data)        
        

def usage():
    helper = "USAGE: %s FILE0 FILE1 DIR1 DIR2 FILEX DIRX DESTINATION" % os.path.basename(
        __file__)
    return helper

if __name__ == '__main__':
    list_argv = sys.argv[1:len(sys.argv)-1]
    
    if len(sys.argv) > 2:
        for i in list_argv:
            if i == '*':
                start_move()
                list_argv.remove(i)
            if len(i) > 1 and i[-1] == '*':
                start_move(i[0:-1])
                list_argv.remove(i)
        if list_argv > 2:
            #print "SRC =", sys.argv[1:len(sys.argv)-1]
            #print "DST =", sys.argv[-1]
            data = 'MOVE: "{0}" --> "{1}"'.format("; ".join(list_argv), str(sys.argv[-1]))
            logs(data)
            try:
                win32_shellcopy(list_argv, sys.argv[-1])
            except:
                data = traceback.format_exc()
                logs(data)
    else:
        if len(sys.argv) == 1:
            print (usage())
        else:
            data = 'MOVE: "{0}" --> "{1}"'.format("; ".join(sys.argv[1]), str(sys.argv[2]))
            logs(data)
            try:
                win32_shellcopy(sys.argv[1], sys.argv[2])
            except:
                data = traceback.format_exc()
                logs(data)
