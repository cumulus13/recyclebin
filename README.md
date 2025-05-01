# Recycle Bin Manager (Python)

A simple command-line tool to manage the Windows Recycle Bin (Windows) using Python.  
Features interactive mode, listing, restoring, deleting, and cleaning the recycle bin, with a colorful interface.

## Features

- List all items in the Recycle Bin with date, name, and full path.
- Restore or permanently delete items by number, range, or list.
- Clean (empty) the entire Recycle Bin.
- Interactive mode with search/filter by filename.
- Colorful output using `rich`.

## Requirements

- Python 3.7+
- [rich](https://pypi.org/project/rich/)
- [rich-argparse](https://pypi.org/project/rich-argparse/)
- [winshell](https://pypi.org/project/winshell/) (Windows only)

Install dependencies:
```sh
pip install rich rich-argparse winshell
```

## Usage

```sh
python recyclebin.py [options]
```

### Options

- `-l`, `--list`  
  List contents of the Recycle Bin.

- `-c`, `--clean`  
  Clean (empty) the Recycle Bin.

- `-i`, `--interactive`  
  Start interactive mode.

### Interactive Mode

You will see a list of items in the Recycle Bin and a prompt:

```
please select number, [n]r = to restore number, [n1-nX]r to restore number n1 to nX, n1,n2,n3..r = to restore number n1,n2,n3,...,[n]d = to delete number, [n1-nX]d to delete number n1 to nX, n1,n2,n3..d = to delete number n1,n2,n3,..., [c] = clean/clear recycle bin, [q]uit/e[x]it = exit/quit or just type any to search/filter what you want:
```

#### Examples

- `1r` — Restore item number 1
- `2-4d` — Delete items 2 to 4
- `1,3,5r` — Restore items 1, 3, and 5
- `c` — Clean (empty) the Recycle Bin
- `q` or `x` — Exit interactive mode
- Typing any text — Filter/search items by name

## License

MIT License

---

**Note:** This script works only on Windows, as it uses the `winshell` library.

## Author
[Hadi Cahyadi](mailto:cumulus13@gmail.com)
    

## Coffee
[![Buy Me a Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/cumulus13)

[![Donate via Ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/cumulus13)
 
 [Support me on Patreon](https://www.patreon.com/cumulus13)