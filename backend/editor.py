# Minimal editor stubs adapting MoviePy imports for compatibility
# Export names expected by backend.main
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import ( # moviepy top-level exports many classes
    TextClip, CompositeVideoClip, concatenate_videoclips,
    ImageClip
)
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.audio.AudioClip import CompositeAudioClip
