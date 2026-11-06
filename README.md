# Python CLI Tools

A colection os custom command-line tools written in Python.

## Tools included
- `mpd_fzf_player.py`: An interactive MPD (Music Player Daemon) manager. It uses `fzf` to search your library by title, artist, or album, allowing you to play a specific song (while shuffling the rest) or queue it next.
- `notes_manager.py`: A quick Markdown note-taking manager. Create, open, rename, or delete notes using interactive `fzf` menus.

## Dependencies

Make sure you have `fzf` installed on your system, then install the Python requirements:

```bash
pip install -r requirements.txt
```

## Usage

Make the scripts executable:

```bash
chmod +x mpd_fzf_player.py notes_manager.py
```

Then you can run them directly:

```bash
mpd_fzf_player.py -p
notes_manager.py -n "Note_3"
```
