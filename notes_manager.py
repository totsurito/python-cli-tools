#!/usr/bin/env python3

import argparse
import subprocess
import sys
from pathlib import Path

# ----- CONFIG -----
NOTE_DIR = Path.home()/'notes'
EDITOR = "nano"

def fzf(options) -> str:
    if not options:
        print("There is not notes.")
        sys.exit(-1)
    input_text = "\n".join(options)
    try:
        result = subprocess.run(
            ["fzf", "--prompt=Choose: ", "--height=75%", "--reverse", "--delimiter=|", "--exact"],
            input=input_text,
            text=True,
            capture_output=True,
            check=True
        )
        selection = result.stdout.strip()
        return selection
    except subprocess.CalledProcessError:
        print("No note selected. Canceled.")
        sys.exit(-1)

def get_files() -> list:
    paths = list(NOTE_DIR.glob('*.md'))
    return list(sorted(path.name for path in paths))

def create_note(name: str) -> None:
    filepath = NOTE_DIR / f"{name}.md"
    if name == '':
        counter = 1
        while True:
            filepath = NOTE_DIR / f"Untitle-{counter}.md"
            if not filepath.exists(): break
            counter += 1
    if filepath.exists(): 
        print(f"The file {name}.md already exists.")
        return
    subprocess.run(
        [EDITOR, "+-1", str(filepath)]
    )
    return

def open_note(file: str) -> None:
    filepath = NOTE_DIR / f"{file}"
    if not filepath.exists():
        print(f"The file {file} doesn't exists.")
        return 
    subprocess.run(
        [EDITOR, "+-1", str(filepath)]
    )
    return

def rename_note(names: list) -> None:
    if names[0] == names[1]:
        print("The names are the same.")
        return 
    old_filepath = NOTE_DIR / f"{names[0]}.md"
    new_filepath = NOTE_DIR / f"{names[1]}.md"
    if not old_filepath.exists():
        print(f"The file {names[0]}.md doesn't exists.")
        return
    if new_filepath.exists():
        print(f"The file {names[1]}.md already exists.")
        return 
    old_filepath.rename(new_filepath)
    return

def delete_note(file: str) -> None:
    filepath = NOTE_DIR / f"{file}"
    if not filepath.exists():
        print(f"The file {file} doesn't exists.")
        return
    filepath.unlink()
    print(f"The file {file} deleted.")
    return

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Notes Manager."
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-n", "--new",
        nargs="?",
        const="",
        metavar="NAME",
        help="Create and open a new note"
    )
    group.add_argument(
        "-o", "--open",
        nargs="?",
        const="",
        metavar="NAME",
        help="Open a note"
    )
    group.add_argument(
        "-r", "--rename",
        nargs=2,
        metavar=("OLD_NAME", "NEW_NAME"),
        help="Rename a note"
    )
    group.add_argument(
        "-d", "--delete",
        nargs="?",
        const="",
        metavar="NAME",
        help="Delete a note"
    )

    args = parser.parse_args()

    if args.new is None and args.open is None and args.rename is None and args.delete is None: print("usage: notes [-h] [-n [NAME] | -o [NAME] | -r OLD_NAME NEW_NAME | -d [NAME]]")
    if args.new is not None: create_note(name=args.new)
    if args.open is not None: 
        if args.open == '': args.open = fzf(get_files())
        else: args.open += '.md'
        open_note(file=args.open)
    if args.rename is not None: rename_note(names=args.rename)
    if args.delete is not None:
        if args.delete == '': args.delete = fzf(get_files())
        else: args.delete += '.md'
        delete_note(file=args.delete)
    return

if __name__ == "__main__": main()