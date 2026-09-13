#!/usr/bin/env python3

# File: recyclebin.py
# Author: Hadi Cahyadi <cumulus13@gmail.com>
# Date: 2026-01-09
# Description: A simple command-line tool to manage the Windows Recycle Bin (Windows) using Python.  
# License: MIT

from __future__ import print_function

import os
from config_get import ConfigGet  # type: ignore
CONFIGFILE = ConfigGet(config_dir = 'rcb', create=True)
if str(os.getenv('RCB_DEBUG', '0')).lower() in ('1', 'true', 'ok', 'on', 'yes'): print(f"CONFIGFILE: {CONFIGFILE}")

from envdot import load_env  # type: ignore
CONFIG = load_env(CONFIGFILE)


HAS_GNTPLIB = False
HAS_RICH = False
Align = None  # type: ignore

import sys
import argparse
try:
    from pathlib3 import Path  # type: ignore
except:
    from pathlib import Path

try:
    from rich.console import Console
    from rich.align import Align
    HAS_RICH = True
except:
    from make_colors import Console  # type: ignore

try:
    from rchf import CustomRichHelpFormatter  # type: ignore
except:
    from rich_argparse import RichHelpFormatter, _lazy_rich as rr
    class CustomRichHelpFormatter(RichHelpFormatter):
        """A custom RichHelpFormatter with modified styles."""

        styles: ClassVar[dict[str, rr.StyleType]] = {  # type: ignore
            "argparse.args": "bold #FFFF00",  # Changed from cyan
            "argparse.groups": "#AA55FF",   # Changed from dark_orange
            "argparse.help": "bold #00FFFF",    # Changed from default
            "argparse.metavar": "bold #FF00FF", # Changed from dark_cyan
            "argparse.syntax": "underline", # Changed from bold
            "argparse.text": "white",   # Changed from default
            "argparse.prog": "bold #00AAFF italic",     # Changed from grey50
            "argparse.default": "bold", # Changed from italic
        }

from typing import ClassVar

try:
    from gntplib import Publisher, Resource  # type: ignore
    HAS_GNTPLIB = True
except:
    pass

console = Console()

if Align:
    console.print(
        Align("""[bold #00FFFF] 
     _                                        _           _ _____ 
    | |__  _   _    ___ _   _ _ __ ___  _   _| |_   _ ___/ |___ / 
    | '_ \| | | |  / __| | | | '_ ` _ \| | | | | | | / __| | |_ \ 
    | |_) | |_| | | (__| |_| | | | | | | |_| | | |_| \__ \ |___) |
    |_.__/ \__, |  \___|\__,_|_| |_| |_|\__,_|_|\__,_|___/_|____/ 
           |___/                                                  [/]\n""")
    )
else:
    console.print(
       """[bold #00FFFF] 
     _                                        _           _ _____ 
    | |__  _   _    ___ _   _ _ __ ___  _   _| |_   _ ___/ |___ / 
    | '_ \| | | |  / __| | | | '_ ` _ \| | | | | | | / __| | |_ \ 
    | |_) | |_| | | (__| |_| | | | | | | |_| | | |_| \__ \ |___) |
    |_.__/ \__, |  \___|\__,_|_| |_| |_|\__,_|_|\__,_|___/_|____/ 
           |___/                                                  [/]\n"""
    )


def notify(title, message, name = 'cleanup', icon = None, host = None):
    if not HAS_GNTPLIB:
        console.print("WARNING: Install gntplib first !")
    icon = Path(__file__).parent / 'recyclebin.png'
    if icon.is_file(): icon = Resource(icon)  # type: ignore
    notifications = [name, "error"]

    def publish(host='127.0.0.1', port=23053):
        p = Publisher(  # type: ignore
                "RecycleBin",
                notifications,
                host=host,
                port=port
            )
        p.register()
        p.publish(name, title, message, icon);return True if name in notifications else print(f'{name} not in {notifications}');return False
        
    if host and isinstance(host, (list, tuple)):
        for i in host:
            if ":" in host:
                _host, _port = host.split(":")
            else:
                _host = i
                _port = 23053

            publish(_host, int(_port))
    elif host and isinstance(host, (str, bytes)):
        host = host.decode() if hasattr(host, 'decode') else host
        publish(host)
    else:
        print("Not send notification to growl !")


    return
    
try:
    import winshell
except ImportError:
    console.print("[white on red]Print winshell module not found ![/]")
    console.print("[white on blue]Please install first ![/]")
    sys.exit(0)

def list_recycle_bin():
    items = list(winshell.ShellRecycleBin().items())
    if not items:
        console.print(":recycling_symbol: :cross_mark: [bold #FFFF00]Recycle Bin[/] [bold #FF00AA]is empty[/]")
        return []
    console.print("[black on #00FFFF]Recycle Bin Contents:[/]")
    for idx, item in enumerate(items, 1):
        dt = item.recycle_date().strftime("%Y/%m/%d %H:%M:%S.%f")  # type: ignore
        console.print(f"[bold #FF55FF]{idx}.[/] \[[bold #FFFF00]{dt}[/]] [bold #00FFFF]{item.name()}[/] - [bold #AAAAFF]{item.filename()}[/]")  # type: ignore
    return items

# def restore_items(items, indices):
#     for i in indices:
#         try:
#             items[i].restore()
#             console.print(f"[black on #FFFF00]Restored:[/] [white on #0000FF]{items[i].name()}[/]")
#         except Exception as e:
#             console.print(f"[white on red]Failed to restore[/] [white on #00007F]{items[i].name()}[/]: [black on #00FFFF]{e}[/]")

def restore_items_com(items, indices):
    import win32com.client
    shell = win32com.client.Dispatch("Shell.Application")
    recycle_bin = shell.NameSpace(10)  # 10 is CSIDL_BITBUCKET / Recycle Bin
    
    for i in indices:
        try:
            target_name = items[i].name()
            found = False
            for item in recycle_bin.Items():
                if item.Name == target_name:
                    # Execute the 'Restore' context menu verb (e.g. 'undelete' / 'restore')
                    for verb in item.Verbs():
                        if 'restore' in verb.Name.lower() or 'undelete' in verb.Name.lower() or 'estore' in verb.Name.lower():
                            verb.DoIt()
                            found = True
                            break
                    if found:
                        break
            if found:
                console.print(f"[black on #FFFF00]Restored:[/] [white on #0000FF]{target_name}[/]")
            else:
                console.print(f"[white on red]Failed to restore[/] [white on #00007F]{target_name}[/]: Restore verb not found")
        except Exception as e:
            console.print(f"[white on red]Failed to restore[/] [white on #00007F]{items[i].name()}[/]: [black on #00FFFF]{e}[/]")

def restore_items(items, indices):
    for i in indices:
        try:
            # Pass the item's original path to winshell.undelete()
            winshell.undelete(items[i].original_filename())
            console.print(f"[black on #FFFF00]Restored:[/] [white on #0000FF]{items[i].name()}[/]")
        except Exception as e:
            # console.print(f"[white on red]Failed to restore[/] [white on #00007F]{items[i].name()}[/]: [black on #00FFFF]{e}[/]")
            return restore_items_com(items, indices)

def delete_items(items, indices):
    for i in indices:
        try:
            items[i].delete()
            console.print(f"[white on red]Deleted:[/] [white on #550000]{items[i].name()}[/]")
        except Exception as e:
            console.print(f"[white on red]Failed to delete[/] [black on #FFFF00]{items[i].name()}[/]: [white on blue]{e}[/]")

def parse_indices(cmd, count):
    import re
    indices = set()
    # n1,n2,n3
    if ',' in cmd:
        parts = cmd.split(',')
        for p in parts:
            if p.isdigit():
                idx = int(p) - 1
                if 0 <= idx < count:
                    indices.add(idx)
    # n1-nX
    elif '-' in cmd:
        start, end = cmd.split('-')
        if start.isdigit() and end.isdigit():
            for idx in range(int(start)-1, int(end)):
                if 0 <= idx < count:
                    indices.add(idx)
    # single number
    elif cmd.isdigit():
        idx = int(cmd) - 1
        if 0 <= idx < count:
            indices.add(idx)
    return sorted(indices)

def interactive_recycle_bin():
    items = list_recycle_bin()
    if not items:
        return
    while True:
        console.print(
            "[#00FFFF]please select number[/], "
            "[bold #AA55FF]\\[n]r = to restore number[/], "
            "[bold #5555FF]\\[n1-nX]r to restore number n1 to nX[/], "
            "[bold #5500FF]n1,n2,n3..r = to restore number n1,n2,n3,...[/], "
            "[bold #FF00FF]\\[n]d = to -delete number[/], "
            "[bold #FF55FF]\\[n1-nX]d to delete number n1 to nX[/], "
            "[bold #FF5500]n1,n2,n3..d = to delete number n1,n2,n3,...[/], "
            "[bold #FFFF00]\\[c] = clean/clear recycle bin[/], "
            "[bold #FF0000]\\[q]uit/e[x]it = exit/quit[/] "
            "[bold #00FFFF]or just type any to search/filter what you want:[/] ", end=''
        )
        cmd = input().strip().lower()
        if not cmd:
            items = list_recycle_bin()
            continue
        elif cmd and cmd.lower() in ['q', 'x', 'exit', 'quit']:
            sys.exit()
        if cmd == 'c':
            try:
                winshell.ShellRecycleBin().empty()
                console.print("[bold #FFFF00]Recycle Bin cleared.[/]")
            except Exception as e:
                console.print(f"[white on red]Failed to clear Recycle Bin:[/] [white on blue]{e}[/]")
            items = list_recycle_bin()
            if not items:
                break
            continue
        if cmd.endswith('r') or cmd.endswith('d'):
            action = cmd[-1]
            num_part = cmd[:-1]
            indices = parse_indices(num_part, len(items))
            if not indices:
                console.print("[black on #FFFF00]Invalid selection.[/]")
                continue
            if action == 'r':
                restore_items(items, indices)
            elif action == 'd':
                delete_items(items, indices)
            # Refresh list after action
            items = list_recycle_bin()
            if not items:
                break
        else:
            # Filter/search by name
            filtered = []
            for idx, item in enumerate(items, 1):
                if cmd in item.name().lower():
                    dt = item.recycle_date().strftime("%Y/%m/%d %H:%M:%S.%f")
                    console.print(f"[bold #FF55FF]{idx}.[/] \[[bold #FFFF00]{dt}[/]] [bold #00FFFF]{item.name()}[/] - [bold #AAAAFF]")
                    filtered.append(item)
            if not filtered:
                console.print("[bold #00FFFF]No items found matching your search.[/]")
        # return interactive_recycle_bin()

def usage():
    parser = argparse.ArgumentParser(formatter_class=CustomRichHelpFormatter)
    parser.add_argument('-l', '--list', help='List content of recycle bin', action='store_true')
    parser.add_argument('-c', '--clean', help='Clean/Clear content of recycle bin', action='store_true')
    parser.add_argument('-i', '--interactive', help='Interactive recycle bin manager', action='store_true')
    if len(sys.argv) == 1:
        parser.print_help()
        try:
            winshell.ShellRecycleBin().empty()
        except Exception as e:
            console.print("\n:cross_mark: Failed to cleaning recycle bin !")
        try:
            list_recycle_bin()
        except Exception as e:
            console.print(":recycling_symbol: :white_check_mark: [bold #FFFF00]Recycle Bin[/] [bold #FF00AA]is empty[/]")
    else:
        args = parser.parse_args()
        if args.list:
            list_recycle_bin()
        elif args.clean:
            winshell.ShellRecycleBin().empty()
        elif args.interactive:
            interactive_recycle_bin()

if __name__ == "__main__":
    usage()