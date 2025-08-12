from moviepy.editor import concatenate_videoclips, VideoFileClip, ColorClip

def stitch_clips(clips, output_path):
    real_clips = []
    for c in clips:
        try:
            if c.exists() and c.stat().st_size>0:
                real_clips.append(VideoFileClip(str(c)))
        except Exception:
            pass
    if not real_clips:
        cl = ColorClip(size=(1280,720), color=(0,0,0), duration=1)
        cl.write_videofile(str(output_path), fps=24, codec='libx264')
        return
    final = concatenate_videoclips(real_clips)
    final.write_videofile(str(output_path), fps=24, codec='libx264')
