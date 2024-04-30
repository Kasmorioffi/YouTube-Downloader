from pytube import YouTube
from moviepy.editor import VideoFileClip, AudioFileClip
import os

link = input("Enter link here: ")

url = YouTube(link)

print("downloading....")

video = url.streams.filter(res="2160p", mime_type="video/webm").first()
audio = url.streams.filter(only_audio=True).order_by('abr').desc().first()

path_to_download_folder = "PATH..." #Insert Download Path here

video_file_path = video.download(path_to_download_folder, filename="video")
audio_file_path = audio.download(path_to_download_folder, filename="audio")

print(f"Video downloaded at {video_file_path}")
print(f"Audio downloaded at {audio_file_path}")

print("Merging audio and video....")

videoclip = VideoFileClip(video_file_path)
audioclip = AudioFileClip(audio_file_path)

videoclip = videoclip.set_audio(audioclip)
final_output_path = os.path.join(path_to_download_folder, f"{url.title}.mp4")
videoclip.write_videofile(final_output_path)

print("Merged successfully! :)")

# Delete the temporary video and audio files
os.remove(video_file_path)
os.remove(audio_file_path)
print("Temporary files deleted.")
