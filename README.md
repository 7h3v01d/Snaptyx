# 📸 Snaptyx (Archived)
**Snaptyx** is a lightweight tool that turns an entire project folder into a single, readable **snapshot text file** — then can rebuild the folder later from that snapshot.

Think: *“zip file meets human-readable transcript.”*

This repo is archived, but the core idea is solid and useful.

---

## ✨ What Snaptyx does

### ✅ Create snapshots
- Builds a **tree-style file map**
- Transcribes project files into one `.txt` file
- Wraps each file with clear markers:

--- Start of: relative/path/to/file.py ---
...file contents...
--- End of: relative/path/to/file.py ---

yaml
Copy code

### ✅ Restore snapshots
- Recreates the directory structure
- Writes each file back to disk from the snapshot text

---

## 🧠 Why this exists
Snaptyx was built for moments when you want to preserve or share a project without:
- zips that hide contents
- copying folders around
- losing the directory structure

Great for:
- archiving “known good” states
- sharing code in chats/emails
- keeping a portable text snapshot
- quick backups of small projects

---

## 🔥 Nice touches
- **Encoding detection** via `chardet` to reduce Unicode headaches
- **Automatically skips virtual environments** (detects venv structure like `pyvenv.cfg`)
- Excludes common noise folders (e.g. `.git`, `__pycache__`) and compressed files

---

## ▶️ Usage

#### 1) Create a snapshot
```bash
python snaptyx.py create . -o my_project_snapshot.txt

```
#### 2) Restore from a snapshot
```bash
python snaptyx.py restore my_project_snapshot.txt -d restored_project
```
#### 3) (Optional) Launch the GUI
```bash
python snaptyx.py gui
```
## ⚠️ Security note (important)
Snaptyx snapshots are trusted-input.

Only restore snapshots you created yourself or from people you trust.
A malicious snapshot could attempt to write files outside the destination folder.

## 🗂️ Repo contents

- snaptyx.py — CLI tool (create/restore + core logic)
- gui.py — Tkinter GUI wrapper (archived WIP integration)
- README.md — this doc

## 🧊 Project status
Archived / On Ice

This repo is preserved as a working snapshot-tool concept.
If revived, natural upgrades would be:

- configurable excludes (.snaptyxignore)
- path sanitization/hardening on restore
- dependency snapshotting (requirements.txt capture)
- packaging to PyPI

## 📜 License
Unlicensed (personal archive). Add a LICENSE before redistribution.
