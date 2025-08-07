from moviepy.editor import VideoFileClip

# Load first 5 seconds of the bunny.webm video
clip = VideoFileClip("test_media/bunny.webm").subclip(0, 5)

# Export it to output.mp4 inside the test_media folder
clip.write_videofile("test_media/output.mp4", codec="libx264", audio_codec="aac")
