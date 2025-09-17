#!/usr/bin/env python3
"""
Elite Dangerous Log Viewer with:
 - Sortable Columns (clickable headers, asc/desc indicator, reset sort)
 - Double-click to view leftover "Parameters" in a nested tree structure
 - Better Date/Time Formatting (YYYY-MM-DD, HH:MM:SS)
 - Windows path fix (doubling backslashes in JSON)

When you double-click on a row in the main table, a new window opens
showing the leftover parameters in a hierarchical Treeview.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json


class LogParser:
    """
    Class responsible for parsing Elite Dangerous log lines.
    """

    def __init__(self):
        self.logs = []  # List to store parsed log entries

    def parse_line(self, line):
        """
        Parse a single log line of the form:
          YYYYMMDD.HHMMSS: { "action": "...", ... } ;
        """
        line = line.strip()
        if line.endswith(';'):
            line = line[:-1].strip()

        try:
            timestamp, json_part = line.split(':', 1)
            timestamp = timestamp.strip()
            json_part = json_part.strip()
            # Fix single backslashes (for Windows paths) by replacing with double
            json_part_fixed = json_part.replace('\\', '\\\\')
            log_data = json.loads(json_part_fixed)
        except Exception as e:
            print("Failed to parse line:", line)
            print("Error:", e)
            return None

        return {"timestamp": timestamp, "data": log_data}

    def parse_file(self, file_path):
        """
        Reads the file line by line and returns a list of parsed log entries.
        """
        self.logs.clear()
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        parsed = self.parse_line(line)
                        if parsed:
                            self.logs.append(parsed)
        except Exception as e:
            print("Error reading file:", e)
            messagebox.showerror("File Error", f"Could not read file: {e}")
        return self.logs


class LogViewerApp:
    """
    Tkinter GUI Application to display and sort Elite Dangerous logs.

    Columns in the main Treeview:
      - Timestamp (Raw)
      - Action
      - Date (formatted as YYYY-MM-DD)
      - Time (formatted as HH:MM:SS)
      - User
      - Parameters (brief 'key=value' string)
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Elite Dangerous Log Viewer")

        # Store original logs order and current sort details
        self.all_logs = []  # Original logs (as loaded)
        self.current_sort_col = None
        self.current_sort_reverse = False

        # For double-click details: store leftover dictionaries keyed by row-id
        self.row_data = {}

        # Main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Log parser instance
        self.log_parser = LogParser()

        # Buttons frame
        self.buttons_frame = ttk.Frame(self.main_frame)
        self.buttons_frame.pack(fill=tk.X, pady=(0, 5))

        # Load file button
        self.load_button = ttk.Button(self.buttons_frame, text="Load Log File", command=self.load_log_file)
        self.load_button.pack(side=tk.LEFT, padx=(0, 5))

        # Reset sort button
        self.reset_button = ttk.Button(self.buttons_frame, text="Reset Sort", command=self.reset_sort)
        self.reset_button.pack(side=tk.LEFT)

        # Define Treeview columns
        self.columns = ("timestamp", "action", "date", "time", "user", "parameters")
        self.tree = ttk.Treeview(self.main_frame, columns=self.columns, show='headings')

        # Setup column headings with click command for sorting and left-aligned text.
        for col in self.columns:
            self.tree.heading(col, text=col.capitalize(), command=lambda _col=col: self.sort_by_column(_col))
            if col == "timestamp":
                self.tree.column(col, width=140, anchor="w")
            elif col in ("date", "time"):
                self.tree.column(col, width=90, anchor="w")
            elif col == "parameters":
                self.tree.column(col, width=400, anchor="w")
            else:
                self.tree.column(col, width=120, anchor="w")

        # Vertical scrollbar
        self.scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Bind double-click event to open a nested tree view of leftover parameters
        self.tree.bind("<Double-1>", self.on_double_click)

    def load_log_file(self):
        """
        Opens a file dialog to select a log file, parses it, and displays the logs.
        """
        file_path = filedialog.askopenfilename(
            title="Select Log File",
            filetypes=[("Log Files", "*.log *.txt"), ("All Files", "*.*")]
        )
        if file_path:
            logs = self.log_parser.parse_file(file_path)
            self.all_logs = logs[:]  # Keep original order
            self.current_sort_col = None
            self.current_sort_reverse = False
            self.update_column_headers()
            self.display_logs(logs)

    def display_logs(self, logs):
        """
        Displays the given logs list in the Treeview.
        Also populates self.row_data for leftover fields.
        """
        # Clear existing rows and row_data
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.row_data.clear()

        for entry in logs:
            timestamp_raw = entry.get("timestamp", "")
            data = dict(entry.get("data", {}))

            # Extract known fields
            action_val = data.pop("action", "")
            date_str = data.pop("date", "")
            time_str = data.pop("time", "")
            user_val = data.pop("user", "")

            # Format date/time
            date_val = self.format_date(date_str)
            time_val = self.format_time(time_str)

            # Prepare leftover parameters for the main table (brief version)
            leftover_list = [f"{k}={v}" for k, v in data.items()]
            leftover_str = ", ".join(leftover_list)

            # Insert row into main Treeview
            row_id = self.tree.insert("", tk.END,
                                      values=(timestamp_raw, action_val, date_val, time_val, user_val, leftover_str))

            # Store the leftover dictionary for double-click detail
            # We'll keep the entire leftover 'data' so we can show it as a nested tree
            self.row_data[row_id] = data

    def on_double_click(self, event):
        """
        Opens a nested tree view window for the leftover parameters of the clicked row.
        """
        # Identify the row that was double-clicked
        row_id = self.tree.focus()
        if not row_id:
            return

        # Retrieve the leftover dictionary
        leftover_data = self.row_data.get(row_id, {})

        # Create a new Toplevel window to show the nested parameters
        detail_window = tk.Toplevel(self.root)
        detail_window.title("Parameters Detail")

        # Frame in the new window
        frame = ttk.Frame(detail_window, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        # A Treeview for nested display
        # We'll use the "#0" column as the tree column, plus one extra column "value"
        params_tree = ttk.Treeview(frame, columns=("value",), show="tree headings")
        params_tree.heading("#0", text="Key")
        params_tree.heading("value", text="Value")
        params_tree.column("#0", width=200, anchor="w")
        params_tree.column("value", width=400, anchor="w")

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=params_tree.yview)
        params_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        params_tree.pack(fill=tk.BOTH, expand=True)

        # Populate the nested tree
        self.populate_parameters_tree(params_tree, "", leftover_data, label="root")

        # Optionally, expand the top-level item
        for child in params_tree.get_children():
            params_tree.item(child, open=True)

    def populate_parameters_tree(self, tree, parent, data, label="root"):
        """
        Recursively populates a Treeview with nested data (dicts/lists/primitives).
        - 'tree' is the Treeview.
        - 'parent' is the parent node ID.
        - 'data' is the current data structure to display (dict, list, or primitive).
        - 'label' is the key or name to show in the tree's #0 column.
        """
        # If it's a dict, create a node for it, then recurse for each key
        if isinstance(data, dict):
            # Create a parent node representing this dict
            node_id = tree.insert(parent, "end", text=label, values=("<dict>",))
            # For each key, add a child
            for k, v in data.items():
                self.populate_parameters_tree(tree, node_id, v, label=str(k))

        # If it's a list, create a node for it, then recurse for each index
        elif isinstance(data, list):
            node_id = tree.insert(parent, "end", text=label, values=("<list>",))
            for i, item in enumerate(data):
                self.populate_parameters_tree(tree, node_id, item, label=f"[{i}]")

        # Otherwise, it's a primitive (str, int, bool, etc.)
        else:
            # Create a leaf node with label in #0, and the value in the "value" column
            # We also show the type in parentheses, if desired
            leaf_value = f"{data}"
            tree.insert(parent, "end", text=label, values=(leaf_value,))

    def sort_by_column(self, col):
        """
        Sort the Treeview data by the given column. Toggling sort order on successive clicks.
        Updates the header text to indicate the current sort column and order.
        """
        # Toggle sort order if the same column, otherwise default to ascending.
        if self.current_sort_col == col:
            self.current_sort_reverse = not self.current_sort_reverse
        else:
            self.current_sort_reverse = False
            self.current_sort_col = col

        reverse = self.current_sort_reverse

        # Get all items with the value in the specified column.
        data_list = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]
        # Sort the list (lexicographical). You can add custom numeric or date parse if needed.
        data_list.sort(reverse=reverse)

        # Rearrange items in sorted order
        for index, (val, k) in enumerate(data_list):
            self.tree.move(k, '', index)

        self.update_column_headers()

    def reset_sort(self):
        """
        Resets the sort order to the original file order.
        """
        if self.all_logs:
            self.current_sort_col = None
            self.current_sort_reverse = False
            self.update_column_headers()
            self.display_logs(self.all_logs)

    def update_column_headers(self):
        """
        Update header text for each column to include a sort indicator (▲/▼) if sorted.
        """
        for col in self.columns:
            header_text = col.capitalize()
            if col == self.current_sort_col:
                arrow = "▼" if self.current_sort_reverse else "▲"
                header_text += " " + arrow
            self.tree.heading(col, text=header_text, command=lambda _col=col: self.sort_by_column(_col))

    @staticmethod
    def format_date(date_str):
        """
        Convert YYYYMMDD to YYYY-MM-DD if length is 8; otherwise, return the original string.
        """
        if len(date_str) == 8:
            return f"{date_str[0:4]}-{date_str[4:6]}-{date_str[6:8]}"
        return date_str

    @staticmethod
    def format_time(time_str):
        """
        Convert HHMMSS to HH:MM:SS if length is 6; otherwise, return the original string.
        """
        if len(time_str) == 6:
            return f"{time_str[0:2]}:{time_str[2:4]}:{time_str[4:6]}"
        return time_str


def main():
    root = tk.Tk()
    app = LogViewerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
