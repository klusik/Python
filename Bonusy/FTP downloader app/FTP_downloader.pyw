import os
import ftplib
import threading
import fnmatch
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, ttk
import time
from typing import List, Optional

class App:
    def __init__(self, root: tk.Tk) -> None:
        """
        Initialize the main application window and variables.
        :param root: (Tk) The root Tkinter window object.
        """
        self.root = root
        self.root.title("FTP Downloader App")

        self.server = tk.StringVar()
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.target_folder = tk.StringVar()
        self.exclude_filters = tk.StringVar()
        self.thread_count = tk.IntVar(value=1)
        self.directories: List[str] = []
        self.check_vars: dict[str, tk.BooleanVar] = {}

        self.create_widgets()

    def create_widgets(self) -> None:
        """
        Create and configure the widgets for the application.
        """
        tk.Label(self.root, text="FTP Server:").grid(row=0, column=0, sticky=tk.W)
        tk.Entry(self.root, textvariable=self.server).grid(row=0, column=1)

        tk.Label(self.root, text="Username:").grid(row=1, column=0, sticky=tk.W)
        tk.Entry(self.root, textvariable=self.username).grid(row=1, column=1)

        tk.Label(self.root, text="Password:").grid(row=2, column=0, sticky=tk.W)
        tk.Entry(self.root, textvariable=self.password, show="*").grid(row=2, column=1)

        tk.Label(self.root, text="Target Folder:").grid(row=3, column=0, sticky=tk.W)
        tk.Entry(self.root, textvariable=self.target_folder).grid(row=3, column=1)
        tk.Button(self.root, text="Browse", command=self.browse_folder).grid(row=3, column=2)

        tk.Label(self.root, text="Exclude Filters (comma separated, e.g., *.mp4, *.jpg):").grid(row=4, column=0, sticky=tk.W)
        tk.Entry(self.root, textvariable=self.exclude_filters).grid(row=4, column=1)

        tk.Label(self.root, text="Number of Threads:").grid(row=5, column=0, sticky=tk.W)
        tk.Entry(self.root, textvariable=self.thread_count).grid(row=5, column=1)

        tk.Button(self.root, text="Analyze", command=self.analyze_ftp).grid(row=6, column=0)
        tk.Button(self.root, text="Start Download", command=self.start_download).grid(row=6, column=1)

        self.check_frame = ttk.Frame(self.root)
        self.check_frame.grid(row=7, column=0, columnspan=3, sticky=tk.W)

        self.status_label = tk.Label(self.root, text="Status: Idle")
        self.status_label.grid(row=8, column=0, columnspan=3, sticky=tk.W)

        self.progress = ttk.Progressbar(self.root, orient="horizontal", mode="indeterminate")
        self.progress.grid(row=9, column=0, columnspan=3, sticky=tk.W+tk.E)

    def browse_folder(self) -> None:
        """
        Open a dialog to browse and select a target folder.
        """
        folder = filedialog.askdirectory()
        if folder:
            self.target_folder.set(folder)

    def analyze_ftp(self) -> None:
        """
        Analyze the FTP server to list the top-level directories available for download.
        """
        server = self.server.get()
        username = self.username.get()
        password = self.password.get()

        if not all([server, username, password]):
            messagebox.showerror("Error", "Please fill in FTP server details.")
            return

        self.status_label.config(text="Status: Connecting to FTP server...")
        self.progress.start()
        self.root.update()

        self.ftp_downloader = FTPDownloader(server, username, password, None, [], 1, self.status_label, self.progress)
        if not self.ftp_downloader.connect():
            self.progress.stop()
            self.status_label.config(text="Status: Failed to connect")
            return

        self.status_label.config(text="Status: Analyzing directories...")
        self.directories = self.ftp_downloader.get_top_level_directories(["/www/domains", "/www/subdom"])
        self.display_checkboxes()
        self.progress.stop()
        self.status_label.config(text="Status: Analysis completed")

    def display_checkboxes(self) -> None:
        """
        Display checkboxes for the top-level directories found on the FTP server.
        """
        for widget in self.check_frame.winfo_children():
            widget.destroy()

        self.check_vars = {}
        for directory in self.directories:
            var = tk.BooleanVar()
            chk = tk.Checkbutton(self.check_frame, text=directory, variable=var)
            chk.pack(anchor='w')
            self.check_vars[directory] = var

    def start_download(self) -> None:
        """
        Start downloading the selected directories from the FTP server.
        """
        server = self.server.get()
        username = self.username.get()
        password = self.password.get()
        target_folder = self.target_folder.get()
        exclude_filters = [f.strip() for f in self.exclude_filters.get().split(',')] if self.exclude_filters.get() else []
        thread_count = self.thread_count.get()

        selected_directories = [dir_ for dir_, var in self.check_vars.items() if var.get()]

        if not all([server, username, password, target_folder]) or not selected_directories:
            messagebox.showerror("Error", "Please fill in all fields and select directories to download.")
            return

        self.status_label.config(text="Status: Starting download...")
        self.progress.start()
        self.ftp_downloader = FTPDownloader(server, username, password, target_folder, exclude_filters, thread_count, self.status_label, self.progress)
        self.ftp_downloader.queue = selected_directories
        threading.Thread(target=self.ftp_downloader.start_download).start()

class FTPDownloader:
    def __init__(self, server: str, username: str, password: str, target_folder: Optional[str], exclude_filters: List[str],
                 thread_count: int, status_label: tk.Label, progress: ttk.Progressbar) -> None:
        """
        Initialize the FTPDownloader class.
        :param server: (str) The FTP server address.
        :param username: (str) The FTP username.
        :param password: (str) The FTP password.
        :param target_folder: (str) The local target folder for downloads.
        :param exclude_filters: (list) List of filename patterns to exclude.
        :param thread_count: (int) Number of threads to use for downloading.
        :param status_label: (Label) Label widget to show status messages.
        :param progress: (Progressbar) Progress bar widget for status updates.
        """
        self.server = server
        self.username = username
        self.password = password
        self.target_folder = target_folder
        self.exclude_filters = exclude_filters
        self.thread_count = thread_count
        self.ftp = ftplib.FTP()
        self.lock = threading.Lock()
        self.status_label = status_label
        self.progress = progress
        self.queue: List[str] = []

    def connect(self) -> bool:
        """
        Connect to the FTP server using the provided credentials.
        :return: (bool) True if connected successfully, False otherwise.
        """
        try:
            self.ftp.connect(self.server)
            self.ftp.login(self.username, self.password)
        except ftplib.all_errors as e:
            messagebox.showerror("FTP Error", f"Failed to connect: {e}")
            return False
        return True

    def get_top_level_directories(self, initial_paths: List[str]) -> List[str]:
        """
        Get the top-level directories from the specified initial paths on the FTP server.
        :param initial_paths: (list) List of initial paths to start gathering directories from.
        :return: (list) List of top-level directories.
        """
        directories: List[str] = []
        for path in initial_paths:
            self._gather_top_level_directories(path, directories)
        return directories

    def _gather_top_level_directories(self, path: str, directories: List[str]) -> None:
        """
        Gather top-level directories from the specified path.
        :param path: (str) The path to gather directories from.
        :param directories: (list) The list to append found directories to.
        """
        try:
            self.status_label.config(text=f"Status: Looking in {path}")
            self.progress.update()
            self.ftp.cwd(path)
            items = self.ftp.nlst()
            for item in items:
                item_path = f"{path}/{item}"
                if self.is_directory(item_path):
                    directories.append(item_path)
                    self.status_label.config(text=f"Status: Found {item_path}")
                    self.progress.update()
        except ftplib.error_perm:
            pass

    def start_download(self) -> None:
        """
        Start downloading the selected directories.
        """
        if not self.connect():
            self.progress.stop()
            self.status_label.config(text="Status: Failed to connect")
            return

        threads: List[threading.Thread] = []
        for _ in range(self.thread_count):
            thread = threading.Thread(target=self.download_worker)
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        self.ftp.quit()
        self.progress.stop()
        self.status_label.config(text="Status: Download completed!")
        messagebox.showinfo("Success", "Download completed!")

    def download_worker(self) -> None:
        """
        Worker thread function to download directories and files from the queue.
        """
        while self.queue:
            self.lock.acquire()
            if not self.queue:
                self.lock.release()
                break
            path = self.queue.pop(0)
            self.lock.release()
            self.download_path(path)

    def download_path(self, path: str) -> None:
        """
        Download the contents of the specified path.
        :param path: (str) The path to download.
        """
        try:
            self.status_label.config(text=f"Status: Downloading {path}")
            self.progress.update()
            self.ftp.cwd(path)
            items = self.ftp.nlst()
            for item in items:
                item_path = f"{path}/{item}"
                if self.is_excluded(item):
                    continue
                if self.is_directory(item_path):
                    self.lock.acquire()
                    self.queue.append(item_path)
                    self.lock.release()
                else:
                    self.download_file(item_path)
        except ftplib.error_perm:
            pass

    def is_directory(self, path: str) -> bool:
        """
        Check if the specified path is a directory.
        :param path: (str) The path to check.
        :return: (bool) True if the path is a directory, False otherwise.
        """
        current = self.ftp.pwd()
        try:
            self.ftp.cwd(path)
            self.ftp.cwd(current)
            return True
        except ftplib.error_perm:
            return False

    def is_excluded(self, filename: str) -> bool:
        """
        Check if the filename matches any of the exclude filters.
        :param filename: (str) The filename to check.
        :return: (bool) True if the filename is excluded, False otherwise.
        """
        return any([fnmatch.fnmatch(filename, pattern) for pattern in self.exclude_filters])

    def download_file(self, filepath: str) -> None:
        """
        Download a file from the FTP server to the local target folder.
        :param filepath: (str) The path of the file to download.
        """
        local_path = os.path.join(self.target_folder, *filepath.split('/')[2:])
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        with open(local_path, 'wb') as f:
            try:
                self.status_label.config(text=f"Status: Downloading file {filepath}")
                self.progress.update()
                self.ftp.retrbinary(f"RETR {filepath}", f.write)
            except ftplib.all_errors as e:
                print(f"Failed to download {filepath}: {e}")


def main() -> None:
    """
    Main function to start the Tkinter application.
    """
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()