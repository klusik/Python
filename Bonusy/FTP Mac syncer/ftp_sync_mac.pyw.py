import os
import time
import ftplib
import json
import tkinter as tk
from tkinter import filedialog


class FTPConnection:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        self.connection = None

    def connect(self):
        try:
            self.connection = ftplib.FTP(self.host, self.username, self.password)
            print("Connected to FTP server")
        except Exception as e:
            print(f"Failed to connect to FTP server: {e}")

    def disconnect(self):
        if self.connection:
            self.connection.quit()
            print("Disconnected from FTP server")

    def upload_file(self, local_path, remote_path):
        if self.connection:
            with open(local_path, 'rb') as file:
                self.connection.storbinary(f'STOR {remote_path}', file)
                print(f"Uploaded: {local_path} -> {remote_path}")

    def download_file(self, remote_path, local_path):
        if self.connection:
            with open(local_path, 'wb') as file:
                self.connection.retrbinary(f'RETR {remote_path}', file.write)
                print(f"Downloaded: {remote_path} -> {local_path}")


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("FTP Sync App")

        self.local_folder = ""
        self.remote_folder = ""
        self.ftp_connection = None

        self.load_settings()
        self.create_widgets()
        self.root.after(10000, self.periodic_check)

    def create_widgets(self):
        self.local_button = tk.Button(self.root, text="Select Local Folder", command=self.select_local_folder)
        self.local_button.pack()

        self.remote_button = tk.Button(self.root, text="Connect to FTP and Set Remote Folder",
                                       command=self.connect_and_set_remote)
        self.remote_button.pack()

        self.status_label = tk.Label(self.root, text="Status: Waiting...")
        self.status_label.pack()

    def select_local_folder(self):
        self.local_folder = filedialog.askdirectory()
        self.status_label.config(text=f"Local folder set to: {self.local_folder}")
        self.save_settings()

    def connect_and_set_remote(self):
        if not self.ftp_connection:
            self.ftp_connection = FTPConnection(self.ftp_settings.get("host", "ftp.example.com"),
                                                self.ftp_settings.get("username", "user"),
                                                self.ftp_settings.get("password", "password"))
        self.ftp_connection.connect()
        self.remote_folder = "/remote/folder/path"  # Placeholder; could be made dynamic
        self.status_label.config(text=f"Remote folder set to: {self.remote_folder}")
        self.save_settings()
        self.sync_remote_to_local()

    def sync_remote_to_local(self):
        if self.ftp_connection.connection and self.local_folder:
            for filename in self.ftp_connection.connection.nlst(self.remote_folder):
                local_file_path = os.path.join(self.local_folder, os.path.basename(filename))
                self.ftp_connection.download_file(filename, local_file_path)

    def periodic_check(self):
        if self.local_folder and self.remote_folder:
            self.sync_local_to_remote()
        self.root.after(10000, self.periodic_check)

    def sync_local_to_remote(self):
        if self.ftp_connection.connection:
            for root, _, files in os.walk(self.local_folder):
                for file in files:
                    local_file_path = os.path.join(root, file)
                    remote_file_path = os.path.join(self.remote_folder,
                                                    os.path.relpath(local_file_path, self.local_folder)).replace('\\',
                                                                                                                 '/')
                    self.ftp_connection.upload_file(local_file_path, remote_file_path)

    def load_settings(self):
        try:
            with open("settings.json", "r") as file:
                settings = json.load(file)
                self.local_folder = settings.get("local_folder", "")
                self.remote_folder = settings.get("remote_folder", "")
                self.ftp_settings = settings.get("ftp_settings", {})
        except FileNotFoundError:
            self.ftp_settings = {}

    def save_settings(self):
        settings = {
            "local_folder": self.local_folder,
            "remote_folder": self.remote_folder,
            "ftp_settings": {
                "host": self.ftp_settings.get("host", "ftp.example.com"),
                "username": self.ftp_settings.get("username", "user"),
                "password": self.ftp_settings.get("password", "password")
            }
        }
        with open("settings.json", "w") as file:
            json.dump(settings, file)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = App()
    app.run()
