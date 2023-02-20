Move/Copy Recyclebin Items to spesific directory
===================================================

## requirements
----------------
- winshell
- pywin32
- make_colors
- argparse
- progressbar2

## usage
--------------
```bash
usage: recyclebin [-h] [-a ACTION] [-o] [-g] [-ng] [-y] [-l LOGFILE] [-m MOVE_ALL] DIR

positional arguments:
  DIR                   Destionation directory

optional arguments:
  -h, --help            show this help message and exit
  -a ACTION, --action ACTION
                        Action "[m]ove" or "[c]opy", default is "move"
  -o, --overwrite       Overwrite exist file
  -g, --gui             Use windows Explorer Move/Copy gui, default = Yes
  -ng, --no-gui         Use command line tool
  -y, --quiet           No asking prompt/interactive
  -l LOGFILE, --logfile LOGFILE
                        If you want save logfile to different location, default is "C:\PROJECTS\recyclebin\recyclebin.log"
  -m MOVE_ALL, --move-all MOVE_ALL
                        run action "move" with no interactive/prompt/quiet with progress info

```

## author
--------------
[cumulus13](mailto:cumulus13@gmail.com)
