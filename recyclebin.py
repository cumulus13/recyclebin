#!/usr/bin/env python
#coding:utf-8
"""
  Author:  cumulus13 --<cumulus13@gmail.com>
  Purpose: Manage Recyclebin with Interactive or CLI
  Created: 02/20/23
"""

from __future__ import print_function, unicode_literals

import winshell
import os, sys, signal, argparse
from make_colors import make_colors
try:
    from pydebugger.debug import debug
except:
    def debug(*args, **kwargs):
        return None
try:
    from . import copyx
    from . import xmove
except:
    import copyx
    import xmove
    
import traceback
import shutil
from progressbar import ProgressBar
    
#from typing import List
if sys.version_info.major == 3:
    raw_input = input

class Recyclebin(object):
    
    INTERACTIVE = True
    MOVE_ALL = False
    DESTINATION_DIR = None
    SHOW_PROGRESS = True
    LOG_FILE = 'recyclebin.log'
    
    def __init__(self, interactive = True, move_all = False, desctination_dir = None, show_progress = True, log_file = None):
        if not interactive: self.INTERACTIVE = False
        self.MOVE_ALL = move_all or self.MOVE_ALL
        self.DESTINATION_DIR = desctination_dir or self.DESTINATION_DIR
        if not show_progress: self.SHOW_PROGRESS = False
        self.LOG_FILE = log_file or self.LOG_FILE
        
    @classmethod
    def parse_sequence(self, seq_str):
        """
        Parse a string of numbers and number ranges into a list of individual numbers.
    
        Parameters:
        - seq_str (str): String of numbers and number ranges (e.g., "1,2,4,5,6-10,12,13,14-19").
    
        Returns:
        - seq_list (list): List of individual numbers (e.g., [1, 2, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19]).
        """
        seq_list = []
        for item in seq_str.split(','):
            if '-' in item:
                start, end = item.split('-')
                seq_list.extend(range(int(start), int(end)+1))
            else:
                seq_list.append(int(item))
        return seq_list
    
    @classmethod
    def manage(self, destination_dir = None, gui = True, overwrite = False, interactive = True, show_progress = True, log_file = None, move_all = False, action = 'move'):
        debug(destination_dir = destination_dir)
        debug(gui = gui)
        debug(overwrite = overwrite)
        debug(interactive = interactive)
        debug(show_progress = show_progress)
        debug(log_file = log_file)
        debug(move_all = move_all)
        debug(action = action)
        
        recycle_bin = winshell.ShellRecycleBin()
        
        data = recycle_bin.items()
        items = list(data)
        show_progress = show_progress or self.SHOW_PROGRESS
        log_file = log_file or self.LOG_FILE
        self.LOG_FILE = log_file
        move_all = move_all or self.MOVE_ALL
        if move_all: interactive = False
        
        n = 1
        numbers = []
        
        for i in items:
            print(
                make_colors(str(n).zfill(3) + ".", 'lc') + " " + \
                make_colors(i.name(), 'ly')
            )
            n += 1
        if interactive:
            q = raw_input(
                make_colors("Select number to move/copy", 'lw', 'r') + ", " + \
                make_colors("[n1,n2,n3,n4-n9,n10][a][m/c]", 'b', 'lg') + ", " + \
                make_colors("n = number", 'lc') + ", " + \
                make_colors("m = move action", 'lw', 'bl') + ", " + \
                make_colors("c = copy action", 'lw', 'm') + ", " + \
                make_colors("a = move/copy all or just type 'c' or 'm' without numbers", 'r', 'lw') + ", " + \
                make_colors("[q]uit/e[x]it = quit/exit", 'lw', 'r') + ": "
            )
        else:
            numbers = list(range(len(items)))
            
        
        if q:
            if q == 'am':
                action = 'move'
            elif q == 'ac':
                action = 'copy'            
            if q[-1] == 'c' or q[-1] == 'm':
                if q[-1] == 'c': action = 'copy'
                if q[-1] == 'm': action = 'move'
                q = q[:-1]
                if not q == 'a':
                    try:
                        numbers = self.parse_sequence(q)
                    except ValueError:
                        print(make_colors("Invalid number !", 'lw', 'r'))
                        print(
                            make_colors("[n1,n2,n3,n4-n9,n10][m/c]", 'b', 'lg') + ", " + \
                            make_colors("n = number", 'lc') + ", " + \
                            make_colors("m = move action", 'lw', 'bl') + ", " + \
                            make_colors("c = copy action", 'lw', 'm')                    
                        )
                    if not numbers:
                        return False
                else:
                    numbers = list(range(len(items)))
            elif q == 'a':
                numbers = list(range(len(items)))
            elif q.lower() in ('quit', 'exit', 'q', 'x'):
                print(make_colors("exit ... !", 'lw', 'r'))
                os.kill(os.getpid(), signal.SIGTERM)
            else:
                try:
                    numbers = self.parse_sequence(q)
                except ValueError:
                    print(make_colors("Invalid number !", 'lw', 'r'))
                    print(
                        make_colors("[n1,n2,n3,n4-n9,n10][m/c]", 'b', 'lg') + ", " + \
                        make_colors("n = number", 'lc') + ", " + \
                        make_colors("m = move action", 'lw', 'bl') + ", " + \
                        make_colors("c = copy action", 'lw', 'm')                    
                    )
                if not numbers:
                    return False
            debug(numbers = numbers)
            print(make_colors("numbers selected:", 'b','lc'), make_colors(", ".join(str(i) for i in numbers), 'lc'))
            while 1:
                if not destination_dir:
                    destination_dir = raw_input(make_colors("save to dir [q/x = exit]:", 'b', 'y') + ": ")
                    if destination_dir:
                        if destination_dir in ('q', 'x'):
                            print(make_colors("exit ...", 'lw', 'r'))
                            os.kill(os.getpid(), signal.SIGTERM)
                        else:
                            break
                else:
                    break
            debug(len_items_0 = len(items))
            
            debug(destination_dir = destination_dir)
            debug(gui = gui)
            debug(overwrite = overwrite)
            debug(interactive = interactive)
            debug(show_progress = show_progress)
            debug(log_file = log_file)
            debug(move_all = move_all)
            debug(action = action)
            
            #os.kill(os.getpid(), signal.SIGTERM)
            
            if action == 'move':
                self.move(items, numbers, destination_dir, gui, overwrite, show_progress, log_file, move_all)
            elif action == 'copy':
                self.copy(items, numbers, destination_dir, gui, overwrite, show_progress, log_file, move_all)
    @classmethod
    def move(self, items, numbers, destination_dir, gui = True, overwrite = False, show_progress = True, log_file = None, move_all = False):
        
        PREFIX = '{variables.task} >> {variables.subtask}'
        VARIABLES = {'task': '--', 'subtask': '--',}
        BAR = ProgressBar(max_value = len(items), max_error = False, prefix = PREFIX, variables = VARIABLES)
        debug(len_items = len(items))
        for f in numbers:
            debug(f = f)
            debug(f1 = int(f) - 1)
            data_file = items[int(f) - 1]
            
            data = 'MOVE: "{0}": "{1}" --> "{2}"'.format(os.path.basename(data_file.name()), data_file.filename(), os.path.join(destination_dir,  os.path.basename(data_file.name())))
            xmove.logs(data, log_file)
            try:
                if show_progress:
                    print(
                        make_colors('MOVE', 'b', 'y') + ": " + \
                        make_colors('"' + os.path.basename(data_file.name()) + '"', 'lc') + ": " + \
                        make_colors('"' + data_file.filename() + '"', 'lg') + " " + \
                        make_colors("-->", 'lc') + " " + \
                        make_colors('"' + os.path.join(destination_dir,  os.path.basename(data_file.name())) + '"', 'lm')
                    )
                else:
                    task = make_colors('MOVE', 'b', 'y')
                    subtask = make_colors('"' + os.path.basename(data_file.name())[:5] + "..." + '"', 'lc')
                    BAR.update(items.index(f), task = task, subtask = subtask)
                if overwrite and os.path.isfile(os.path.join(destination_dir, os.path.basename(data_file.name()))):
                    try:
                        os.remove(os.path.join(destination_dir, os.path.basename(data_file.name())))
                    except:
                        try:
                            os.unlink(os.path.join(destination_dir, os.path.basename(data_file.name())))
                        except:
                            pass
                if gui:
                    xmove.win32_shellcopy(data_file.filename(), os.path.join(destination_dir,  os.path.basename(data_file.name())))
                else:
                    shutil.move(data_file.filename(), destination_dir)
            except:
                data = traceback.format_exc()
                xmove.logs(data)        
        BAR.finish(end='\n', dirty=True)
    
    @classmethod
    def copy(self, items, numbers, destination_dir, gui = True, overwrite = False, show_progress = True, log_file = None, move_all = False):
        
        PREFIX = '{variables.task} >> {variables.subtask}'
        VARIABLES = {'task': '--', 'subtask': '--',}
        BAR = ProgressBar(max_value = len(items), max_error = False, prefix = PREFIX, variables = VARIABLES)        
        for f in numbers:
            data_file = items[int(f) - 1]
            
            data = 'COPY: "{0}": "{1}" --> "{2}"'.format(os.path.basename(data_file.name()), data_file.filename(), os.path.join(destination_dir,  os.path.basename(data_file.name())))
            xmove.logs(data, log_file)
            debug(show_progress = show_progress)
            debug(gui = gui)
            try:
                if show_progress:
                    print(
                        make_colors('COPY', 'b', 'y') + ": " + \
                        make_colors('"' + os.path.basename(data_file.name()) + '"', 'lc') + ": " + \
                        make_colors('"' + data_file.filename() + '"', 'lg') + " " + \
                        make_colors("-->", 'lc') + " " + \
                        make_colors('"' + os.path.join(destination_dir,  os.path.basename(data_file.name())) + '"', 'lm')
                    )
                else:
                    task = make_colors('COPY', 'b', 'y')
                    subtask = make_colors('"' + os.path.basename(data_file.name())[:5] + "..." + '"', 'lc')
                    BAR.update(items.index(f), task = task, subtask = subtask)
                debug(overwrite = overwrite)
                if overwrite:
                    debug(destfile = os.path.join(destination_dir, os.path.basename(data_file.name())))
                    debug(check_destfile = os.path.isfile(os.path.join(destination_dir, os.path.basename(data_file.name()))))
                if overwrite and os.path.isfile(os.path.join(destination_dir, os.path.basename(data_file.name()))):
                    try:
                        os.remove(os.path.join(destination_dir, os.path.basename(data_file.name())))
                    except:
                        #print(traceback.format_exc())
                        try:
                            os.unlink(os.path.join(destination_dir, os.path.basename(data_file.name())))
                        except:
                            pass
                if gui:
                    copyx.win32_shellcopy(data_file.filename(), os.path.join(destination_dir,  os.path.basename(data_file.name())))
                else:
                    shutil.copy2(data_file.filename(), destination_dir)
            except:
                data = traceback.format_exc()
                xmove.logs(data)
        BAR.finish(end='\n', dirty=True)
        
    
    @classmethod
    def usage(self):
        parser = argparse.ArgumentParser('recyclebin')
        parser.add_argument('DIR', help = 'Destionation directory', action = 'store')
        parser.add_argument('-a', '--action', help = 'Action "[m]ove" or "[c]opy", default is "move"', default = 'move')
        parser.add_argument('-o', '--overwrite', help = 'Overwrite exist file', action = 'store_true')
        parser.add_argument('-g', '--gui', help = 'Use windows Explorer Move/Copy gui, default = Yes', action = 'store_true')
        parser.add_argument('-ng', '--no-gui', help = 'Use command line tool', action = 'store_true')
        parser.add_argument('-y', '--quiet', help = 'No asking prompt/interactive', action = 'store_true')
        parser.add_argument('-l', '--logfile', help = 'If you want save logfile to different location, default is "{}"'.format(os.path.abspath(self.LOG_FILE)), action = 'store')
        parser.add_argument('-m', '--move-all', help = 'run action "move" with no interactive/prompt/quiet with progress info')
        if len(sys.argv) == 1:
            parser.print_help()
        else:
            args = parser.parse_args()
            gui = True
            interactive = True
            show_progress = True
            if args.no_gui: gui = False
            if args.action == 'c':
                action = 'copy'
            elif args.action == 'm':
                action = 'move'
            else:
                action = args.action
            if args.quiet:
                gui = False
                interactive = False
                show_progress = False
            self.manage(args.DIR, gui, args.overwrite, interactive, show_progress, args.logfile, args.move_all, action)
            
def usage():
    return Recyclebin.usage()
        
if __name__ == '__main__':
    #a =  Recyclebin.move(['one', 'two'], 'test')
    #print("a =", a)
    Recyclebin.usage()