import tkinter as tk
from tkinter import filedialog, messagebox

# (Include all existing functions from snaptyx_v0.3.0.py here)

def gui_main():
    """
    Main function for the Tkinter GUI.
    """
    window = tk.Tk()
    window.title("Snaptyx GUI")
    window.geometry("500x300")
    window.resizable(False, False)

    # --- Create Snapshot Frame ---
    create_frame = tk.LabelFrame(window, text="Create Snapshot", padx=10, pady=10)
    create_frame.pack(padx=10, pady=10, fill="x")

    def select_source_dir():
        directory = filedialog.askdirectory()
        if directory:
            source_dir_entry.delete(0, tk.END)
            source_dir_entry.insert(0, directory)

    def select_output_file():
        file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file:
            output_file_entry.delete(0, tk.END)
            output_file_entry.insert(0, file)

    def create_snapshot_gui():
        source_dir = source_dir_entry.get()
        output_file = output_file_entry.get()
        if not source_dir or not output_file:
            messagebox.showerror("Error", "Please select both a source directory and an output file.")
            return

        try:
            create_snapshot(source_dir, output_file)
            messagebox.showinfo("Success", f"Snapshot created successfully at {output_file}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    source_dir_label = tk.Label(create_frame, text="Source Directory:")
    source_dir_label.pack(anchor="w")
    source_dir_entry = tk.Entry(create_frame, width=50)
    source_dir_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
    source_dir_button = tk.Button(create_frame, text="Browse", command=select_source_dir)
    source_dir_button.pack(side="left")

    output_file_label = tk.Label(create_frame, text="Output File:")
    output_file_label.pack(anchor="w")
    output_file_entry = tk.Entry(create_frame, width=50)
    output_file_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
    output_file_button = tk.Button(create_frame, text="Browse", command=select_output_file)
    output_file_button.pack(side="left")

    create_button = tk.Button(create_frame, text="Create Snapshot", command=create_snapshot_gui)
    create_button.pack(fill="x", pady=(10, 0))

    # --- Restore Snapshot Frame ---
    restore_frame = tk.LabelFrame(window, text="Restore Snapshot", padx=10, pady=10)
    restore_frame.pack(padx=10, pady=10, fill="x")

    def select_snapshot_file():
        file = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file:
            snapshot_file_entry.delete(0, tk.END)
            snapshot_file_entry.insert(0, file)

    def select_destination_dir():
        directory = filedialog.askdirectory()
        if directory:
            destination_dir_entry.delete(0, tk.END)
            destination_dir_entry.insert(0, directory)

    def restore_snapshot_gui():
        snapshot_file = snapshot_file_entry.get()
        destination_dir = destination_dir_entry.get()
        if not snapshot_file or not destination_dir:
            messagebox.showerror("Error", "Please select both a snapshot file and a destination directory.")
            return

        try:
            restore_snapshot(snapshot_file, destination_dir)
            messagebox.showinfo("Success", f"Snapshot restored successfully to {destination_dir}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    snapshot_file_label = tk.Label(restore_frame, text="Snapshot File:")
    snapshot_file_label.pack(anchor="w")
    snapshot_file_entry = tk.Entry(restore_frame, width=50)
    snapshot_file_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
    snapshot_file_button = tk.Button(restore_frame, text="Browse", command=select_snapshot_file)
    snapshot_file_button.pack(side="left")

    destination_dir_label = tk.Label(restore_frame, text="Destination Directory:")
    destination_dir_label.pack(anchor="w")
    destination_dir_entry = tk.Entry(restore_frame, width=50)
    destination_dir_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
    destination_dir_button = tk.Button(restore_frame, text="Browse", command=select_destination_dir)
    destination_dir_button.pack(side="left")

    restore_button = tk.Button(restore_frame, text="Restore Snapshot", command=restore_snapshot_gui)
    restore_button.pack(fill="x", pady=(10, 0))

    window.mainloop()

# --- Update the main function to include the GUI option ---
def main():
    """
    Main function to handle command-line arguments and dispatch commands.
    """
    parser = argparse.ArgumentParser(
        description="Snaptyx: A tool to create and restore project snapshots."
    )
    # Add a new subparsers for GUI
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    gui_parser = subparsers.add_parser(
        "gui",
        help="Launch the graphical user interface"
    )

    # (Keep the existing create and restore parsers here)
    create_parser = subparsers.add_parser(
        "create",
        help="Create a snapshot of a directory"
    )
    # ... (arguments for create_parser) ...
    create_parser.add_argument("source_directory", help="The directory to create a snapshot from")
    create_parser.add_argument("-o", "--output", required=True, help="The output file for the snapshot")

    restore_parser = subparsers.add_parser(
        "restore",
        help="Restore a directory from a snapshot file"
    )
    # ... (arguments for restore_parser) ...
    restore_parser.add_argument("snapshot_file", help="The snapshot file to restore from")
    restore_parser.add_argument("-d", "--destination", required=True, help="The destination directory to restore the project to")


    args = parser.parse_args()

    if args.command == "create":
        create_snapshot(args.source_directory, args.output)
    elif args.command == "restore":
        restore_snapshot(args.snapshot_file, args.destination)
    elif args.command == "gui":
        gui_main()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()