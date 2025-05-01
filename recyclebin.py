from __future__ import print_function
import sys
import argparse
from rich.console import Console
from rich_argparse import RichHelpFormatter, _lazy_rich as rr
from typing import ClassVar
from rich.align import Align

console = Console()

console.print(
    Align("""[bold #00FFFF] _                                        _           _ _____ 
| |__  _   _    ___ _   _ _ __ ___  _   _| |_   _ ___/ |___ / 
| '_ \| | | |  / __| | | | '_ ` _ \| | | | | | | / __| | |_ \ 
| |_) | |_| | | (__| |_| | | | | | | |_| | | |_| \__ \ |___) |
|_.__/ \__, |  \___|\__,_|_| |_| |_|\__,_|_|\__,_|___/_|____/ 
       |___/                                                  [/]\n""")
)

class CustomRichHelpFormatter(RichHelpFormatter):
    """A custom RichHelpFormatter with modified styles."""

    styles: ClassVar[dict[str, rr.StyleType]] = {
        "argparse.args": "bold #FFFF00",  # Changed from cyan
        "argparse.groups": "#AA55FF",   # Changed from dark_orange
        "argparse.help": "bold #00FFFF",    # Changed from default
        "argparse.metavar": "bold #FF00FF", # Changed from dark_cyan
        "argparse.syntax": "underline", # Changed from bold
        "argparse.text": "white",   # Changed from default
        "argparse.prog": "bold #00AAFF italic",     # Changed from grey50
        "argparse.default": "bold", # Changed from italic
    }
    
try:
    import winshell
except ImportError:
    console.print("[white on red]Print winshell module not found ![/]")
    console.print("[white on blue]Please install first ![/]")
    sys.exit(0)

def list_recycle_bin():
    items = list(winshell.ShellRecycleBin().items())
    if not items:
        console.print("\n[#FFFF00 on #FF55FF]Recycle Bin is empty.[/]")
        return []
    console.print("[black on #00FFFF]Recycle Bin Contents:[/]")
    for idx, item in enumerate(items, 1):
        dt = item.recycle_date().strftime("%Y/%m/%d %H:%M:%S.%f")
        console.print(f"[bold #FF55FF]{idx}.[/] \[[bold #FFFF00]{dt}[/]] [bold #00FFFF]{item.name()}[/] - [bold #AAAAFF]{item.filename()}[/]")
    return items

def restore_items(items, indices):
    for i in indices:
        try:
            items[i].restore()
            console.print(f"[black on #FFFF00]Restored:[/] [white on #0000FF]{items[i].name()}[/]")
        except Exception as e:
            console.print(f"[white on red]Failed to restore[/] [white on #00007F]{items[i].name()}[/]: [black on #00FFFF]{e}[/]")

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
            "[00FFFF]please select number[/], "
            "[bold #AA55FF]\[n]r = to restore number[/], "
            "[bold #5555FF]\[n1-nX]r to restore number n1 to nX[/], "
            "[bold #5500FF]n1,n2,n3..r = to restore number n1,n2,n3,...[/], "
            "[bold #FF00FF]\[n]d = to -delete number[/], "
            "[bold #FF55FF]\[n1-nX]d to delete number n1 to nX[/], "
            "[bold #FF5500]n1,n2,n3..d = to delete number n1,n2,n3,...[/], "
            "[bold #FFFF00]\[c] = clean/clear recycle bin[/], "
            "[bold #FF0000]\[q]uit/e[x]it = exit/quit[/] "
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
        # winshell.ShellRecycleBin().empty()
        list_recycle_bin()
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