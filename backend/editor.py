# backend/editor.py

from moviepy.editor import (
    VideoFileClip,
    TextClip,
    CompositeVideoClip,
    concatenate_videoclips,
    AudioFileClip,
    CompositeAudioClip,
    ImageClip,
)

# You can add any other helper functions or classes here if needed.

__all__ = [
    "VideoFileClip",
    "TextClip",
    "CompositeVideoClip",
    "concatenate_videoclips",
    "AudioFileClip",
    "CompositeAudioClip"
]
