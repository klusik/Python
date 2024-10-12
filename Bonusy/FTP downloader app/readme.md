# FTP DOWNLOADER APP

## Description

This is a Python application that connects to an FTP server, analyzes the top-level directories, and allows you to download selected directories with a simple graphical user interface (GUI) built using Tkinter. The app supports multiple threads for faster downloading and includes filtering options to exclude certain file types.

## Features

- Connect to an FTP server with user-provided credentials.
- Analyze the `/www/domains` and `/www/subdom` directories to list available domains and subdomains.
- Select specific top-level directories to download.
- Exclude files based on specified patterns (e.g., exclude `*.mp4` or `*.jpg`).
- Use multi-threaded downloading for increased speed.

## Prerequisites

- Python 3.x
- Internet connection

## Installation

To run the application, you need to install the required dependencies. Run the following command to install them:

```sh
pip install -r requirements.txt
```

## Usage

1. Clone the repository and navigate to the project directory.
2. Run the script:

```sh
python ftp_downloader_app.py
```

3. Enter the FTP server credentials (server address, username, and password).
4. Select the target folder where the files should be downloaded.
5. Specify file patterns to exclude (optional).
6. Set the number of threads for concurrent downloading.
7. Click "Analyze" to get the list of top-level directories.
8. Choose the directories to download, then click "Start Download".

## File Overview

- **ftp\_downloader\_app.py**: The main Python script that runs the FTP Downloader application.
- **requirements.txt**: The file containing the list of dependencies for the project.

## Dependencies

- `ftplib`: Library to handle FTP operations.
- `fnmatch`: Provides support for Unix-style filename pattern matching.
- `tkinter`: Standard Python interface to the Tk GUI toolkit.

## License

This project is licensed under the MIT License.
