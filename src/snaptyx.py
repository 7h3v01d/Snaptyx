# snaptyx.py
# Updated to automatically detect and skip virtual environment folders.

import argparse
import os
import sys
import chardet

def detect_encoding(file_path):
    """Detects the encoding of a file."""
    try:
        with open(file_path, 'rb') as file:
            raw_data = file.read(20000)
            result = chardet.detect(raw_data)
            return result['encoding'] or 'utf-8'
    except:
        return 'utf-8'

def read_file_content(file_path):
    """Reads a file's content with detected encoding."""
    try:
        encoding = detect_encoding(file_path)
        with open(file_path, 'r', encoding=encoding, errors='ignore') as file:
            return file.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

def _build_map_recursive(tree_lines, current_path, all_visible_paths, prefix):
    """
    Recursively builds the tree structure string.
    Adapted from the user's file2tree_gui_v1.1.py.
    """
    try:
        children = sorted(os.listdir(current_path))
        visible_children = [
            child for child in children
            if os.path.join(current_path, child) in all_visible_paths
        ]
    except OSError:
        return

    for i, child_name in enumerate(visible_children):
        is_last = (i == len(visible_children) - 1)
        connector = "└── " if is_last else "├── "
        child_path = os.path.join(current_path, child_name)

        if os.path.isdir(child_path):
            tree_lines.append(f"{prefix}{connector}{child_name}/")
            new_prefix = prefix + ("    " if is_last else "│   ")
            _build_map_recursive(tree_lines, child_path, all_visible_paths, new_prefix)
        else:
            tree_lines.append(f"{prefix}{connector}{child_name}")


def _generate_file_map_string(source_dir, selected_files):
    """
    Generates the file map string for selected files.
    Adapted from the user's file_transcriberGUI_v1.4.py.
    """
    if not source_dir:
        return "Error: No source folder selected.\n"

    all_visible_paths = set(selected_files)
    for path in selected_files:
        parent = os.path.dirname(path)
        while len(parent) >= len(source_dir):
            all_visible_paths.add(parent)
            parent = os.path.dirname(parent)

    tree_lines = [f"File Map for: {os.path.basename(source_dir)}", "=" * 20, ""]

    _build_map_recursive(tree_lines, source_dir, all_visible_paths, "")

    return "\n".join(tree_lines)

def is_virtual_env(directory):
    """
    Checks if a given directory is a Python virtual environment.
    A virtual environment directory typically contains a pyvenv.cfg file.
    Additionally, it contains a 'bin' (for Unix) or 'Scripts' (for Windows)
    subdirectory with the python executable inside.
    """
    # Check for the pyvenv.cfg file, which is a strong indicator
    if os.path.exists(os.path.join(directory, 'pyvenv.cfg')):
        return True

    # Alternative check for older or different venv structures
    if sys.platform == 'win32':
        # On Windows, look for 'Scripts' and 'python.exe'
        if os.path.isdir(os.path.join(directory, 'Scripts')) and os.path.exists(os.path.join(directory, 'Scripts', 'python.exe')):
            return True
    else:
        # On Unix-like systems, look for 'bin' and 'python'
        if os.path.isdir(os.path.join(directory, 'bin')) and os.path.exists(os.path.join(directory, 'bin', 'python')):
            return True

    return False


def create_snapshot(source_dir, output_file):
    """
    Creates a snapshot of a directory, including a file map and
    transcribed file contents. It excludes specific file types,
    directories, and virtual environments.
    """
    print(f"Creating snapshot of '{source_dir}' to '{output_file}'...")
    
    if not os.path.isdir(source_dir):
        print(f"Error: Source directory '{source_dir}' not found.")
        return

    selected_files = set()
    excluded_extensions = {'.zip', '.rar'}
    excluded_dirs = {'__pycache__', '.git'}

    for root, dirs, files in os.walk(source_dir):
        # Prune directories: first by hardcoded names, then by venv check
        dirs[:] = [d for d in dirs if d not in excluded_dirs and not is_virtual_env(os.path.join(root, d))]
        
        for file in files:
            file_extension = os.path.splitext(file)[1].lower()
            if file_extension not in excluded_extensions:
                full_path = os.path.join(root, file)
                selected_files.add(full_path)

    if not selected_files:
        print("Warning: No valid files found in the directory to snapshot.")
        return

    try:
        with open(output_file, 'w', encoding='utf-8') as outfile:
            # 1. Generate and write the file map first
            file_map_content = _generate_file_map_string(source_dir, selected_files)
            outfile.write("--- Start of File Map ---\n")
            outfile.write(file_map_content)
            outfile.write("\n\n--- End of File Map ---\n\n")

            # 2. Transcribe the contents of each file
            for file_path in sorted(list(selected_files)):
                relative_path = os.path.relpath(file_path, source_dir)
                content = read_file_content(file_path)

                header = f"--- Start of: {relative_path} ---\n\n"
                footer = f"\n--- End of: {relative_path} ---\n\n"

                outfile.write(header)
                outfile.write(content)
                outfile.write(footer)

        print("Snapshot created successfully.")
    except Exception as e:
        print(f"Error during snapshot creation: {str(e)}")


def restore_snapshot(snapshot_file, destination_dir):
    """
    Restores the folder and file structure from a Snaptyx snapshot file.
    """
    print(f"Restoring snapshot from '{snapshot_file}' to '{destination_dir}'...")

    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
        print(f"Created destination directory: {destination_dir}")

    state = "before_map"
    current_file_path = None
    current_file_content = []

    try:
        with open(snapshot_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()

                if line == "--- Start of File Map ---":
                    state = "in_map"
                    continue
                elif line == "--- End of File Map ---":
                    state = "after_map"
                    continue

                if state == "after_map":
                    if line.startswith("--- Start of:"):
                        if current_file_path:
                            full_path = os.path.join(destination_dir, current_file_path)
                            os.makedirs(os.path.dirname(full_path), exist_ok=True)
                            with open(full_path, 'w', encoding='utf-8') as out_f:
                                out_f.write("\n".join(current_file_content))
                            print(f"Restored file: {full_path}")
                            current_file_content = []

                        current_file_path = line.replace("--- Start of: ", "").replace(" ---", "")
                    elif line.startswith("--- End of:"):
                        if current_file_path:
                            full_path = os.path.join(destination_dir, current_file_path)
                            os.makedirs(os.path.dirname(full_path), exist_ok=True)
                            with open(full_path, 'w', encoding='utf-8') as out_f:
                                out_f.write("\n".join(current_file_content))
                            print(f"Restored file: {full_path}")
                            current_file_content = []
                            current_file_path = None
                    elif current_file_path:
                        current_file_content.append(line)
    
        if current_file_path:
            full_path = os.path.join(destination_dir, current_file_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'w', encoding='utf-8') as out_f:
                out_f.write("\n".join(current_file_content))
            print(f"Restored file: {full_path}")

        print("Snapshot restored successfully.")
    except Exception as e:
        print(f"Error during restoration: {str(e)}")

def main():
    """
    Main function to handle command-line arguments and dispatch commands.
    """
    parser = argparse.ArgumentParser(
        description="Snaptyx: A tool to create and restore project snapshots."
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Create command parser
    create_parser = subparsers.add_parser(
        "create",
        help="Create a snapshot of a directory"
    )
    create_parser.add_argument(
        "source_directory",
        help="The directory to create a snapshot from"
    )
    create_parser.add_argument(
        "-o", "--output",
        required=True,
        help="The output file for the snapshot"
    )

    # Restore command parser
    restore_parser = subparsers.add_parser(
        "restore",
        help="Restore a directory from a snapshot file"
    )
    restore_parser.add_argument(
        "snapshot_file",
        help="The snapshot file to restore from"
    )
    restore_parser.add_argument(
        "-d", "--destination",
        required=True,
        help="The destination directory to restore the project to"
    )

    args = parser.parse_args()

    if args.command == "create":
        create_snapshot(args.source_directory, args.output)
    elif args.command == "restore":
        restore_snapshot(args.snapshot_file, args.destination)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()