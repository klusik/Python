import os
import yt_dlp

# Function to download a video using yt-dlp
def download_video(video_url, output_folder):
    try:
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',  # Choose the best quality available
            'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),
            'ffmpeg_location': '/opt/homebrew/bin/ffmpeg',  # Explicitly specify the path to ffmpeg
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        print(f"Downloaded: {video_url}\n")
    except Exception as e:
        print(f"Failed to download video {video_url}: {e}\n")

# Function to download an entire playlist using yt-dlp
def download_playlist(playlist_url, output_folder):
    try:
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',  # Choose the best quality available
            'outtmpl': os.path.join(output_folder, '%(playlist)s/%(title)s.%(ext)s'),
            'noplaylist': False,
            'ffmpeg_location': '/opt/homebrew/bin/ffmpeg',  # Explicitly specify the path to ffmpeg
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([playlist_url])
        print("\nAll videos have been downloaded!")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    playlist_url = input("Enter the YouTube playlist URL: ")
    output_folder = input("Enter the output folder path (leave empty for current directory): ") or '.'
    download_playlist(playlist_url, output_folder)
    # https://www.youtube.com/watch?v=urCzEnrdtck&list=PLS4sMq4fWIO8_iOpcLUPcs2zPtxlS9lWK
