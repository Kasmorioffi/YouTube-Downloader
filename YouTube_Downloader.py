from pytube import YouTube
from moviepy.editor import VideoFileClip, AudioFileClip
import os

link = input("Enter link here: ")
filename = input("Enter desired filename here: ")

url = YouTube(link)

print("downloading....")

video = url.streams.filter(res="2160p", mime_type="video/webm").first()

if video is None:
    print("4K video not available, trying Full HD...")
    video = url.streams.filter(res="1080p", mime_type="video/webm").first()

audio = url.streams.filter(only_audio=True).order_by('abr').desc().first()

path_to_download_folder = "PATH..." #Put your output path here

if video is not None:
    video_file_path = video.download(path_to_download_folder, filename="video")
    print(f"Video downloaded at {video_file_path}")
else:
    print("No video stream found that matches the criteria.")

if audio is not None:
    audio_file_path = audio.download(path_to_download_folder, filename="audio")
    print(f"Audio downloaded at {audio_file_path}")
else:
    print("No audio stream found that matches the criteria.")

if video is not None and audio is not None:
    print("Merging audio and video....")

    videoclip = VideoFileClip(video_file_path)
    audioclip = AudioFileClip(audio_file_path)

    videoclip = videoclip.set_audio(audioclip)
    final_output_path = os.path.join(path_to_download_folder, f"{filename.replace('|', '-')}.mp4")
    videoclip.write_videofile(final_output_path)

    print("Merged successfully! :)")

    videoclip.close()
    audioclip.close()

    os.remove(video_file_path)
    os.remove(audio_file_path)
    print("Temporary files deleted.")
