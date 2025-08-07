from moviepy.editor import (
    VideoFileClip,
    AudioFileClip,
    TextClip,
    CompositeVideoClip,
    CompositeAudioClip,
    concatenate_videoclips
)
import os

def generate_video_with_text_and_music(video_paths, text, music_path, output_path):
    clips = []

    for path in video_paths:
        clip = VideoFileClip(path)
        clips.append(clip)

    final_clip = concatenate_videoclips(clips)

    txt_clip = TextClip(text, fontsize=70, color='white')
    txt_clip = txt_clip.set_position('center').set_duration(final_clip.duration)

    video = CompositeVideoClip([final_clip, txt_clip])

    if os.path.exists(music_path):
        music = AudioFileClip(music_path).volumex(0.2)
        final_audio = CompositeAudioClip([video.audio, music])
        video = video.set_audio(final_audio)

    video.write_videofile(output_path, codec="libx264", audio_codec="aac")
