"""prompt_to_clip.py
Contains helper functions to convert a script prompt into a clip spec
(duration, style, seed, model choice). This is where you'd call an LLM
(OpenAI/GPT) to split and enrich prompts.
"""
from typing import Dict

def segment_script(script: str, max_segments: int = 20):
    """Very simple segmentation: split by double newlines or sentences.
    Replace with a robust NLP/LLM segmentation for production.
    """
    parts = [p.strip() for p in script.split('\n\n') if p.strip()]
    if len(parts) == 0:
        parts = [script.strip()]
    if len(parts) > max_segments:
        parts = parts[:max_segments]
    return parts

def build_clip_spec(segment: str, index: int, options: Dict):
    """Return a dict describing how to generate this clip."""
    return {
        "index": index,
        "prompt": segment,
        "duration": options.get("duration", 4),
        "style": options.get("style", "cinematic"),
        "model": options.get("model", "sdxl"),
    }
