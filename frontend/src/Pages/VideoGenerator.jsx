// frontend/src/pages/VideoGenerator.jsx
import React, { useState, useEffect } from "react";

export default function VideoGenerator() {
  const [script, setScript] = useState("A cinematic sunrise over a misty valley.");
  const [taskId, setTaskId] = useState(null);
  const [progress, setProgress] = useState(0);
  const [statusText, setStatusText] = useState("");
  const [videoUrl, setVideoUrl] = useState("");
  const [thumbnail, setThumbnail] = useState(null);
  const [isGenerating, setIsGenerating] = useState(false);

  useEffect(() => {
    let iv;
    if (taskId) {
      iv = setInterval(async () => {
        try {
          const r = await fetch(`/api/progress/${taskId}`);
          if (!r.ok) return;
          const j = await r.json();
          setProgress(j.progress || 0);
          if (j.statusText) setStatusText(j.statusText);
          if (j.final_video_path) {
            // final_video_path is a server path; adjust if you serve static files differently
            setVideoUrl(j.final_video_path);
            setIsGenerating(false);
            setTaskId(null);
            clearInterval(iv);
          }
        } catch (e) {
          // ignore
        }
      }, 2000);
    }
    return () => clearInterval(iv);
  }, [taskId]);

  const startGeneration = async () => {
    setIsGenerating(true);
    setProgress(0);
    setStatusText("Queueing job...");
    const fd = new FormData();
    fd.append("full_script", script);
    fd.append("clip_duration_sec", "60");
    fd.append("clip_count", "20");
    if (thumbnail) fd.append("thumbnail", thumbnail);

    const res = await fetch("/api/generate_realistic_clip", { method: "POST", body: fd });
    const j = await res.json();
    if (res.ok && j.task_id) {
      setTaskId(j.task_id);
      setStatusText("Started");
    } else {
      setStatusText("Failed to start generation");
      setIsGenerating(false);
    }
  };

  return (
    <div>
      <h2>Realistic Video Generator</h2>

      <label>Script / Prompt</label>
      <textarea value={script} onChange={e => setScript(e.target.value)} rows={8} style={{ width: "100%" }} />

      <div style={{ marginTop: 8 }}>
        <label>Optional thumbnail (upload)</label>
        <input type="file" accept="image/*" onChange={e => setThumbnail(e.target.files?.[0] || null)} />
      </div>

      <div style={{ marginTop: 12 }}>
        <button onClick={startGeneration} disabled={isGenerating || !script}>Generate (60s × 20 clips)</button>
      </div>

      {isGenerating && (
        <div style={{ marginTop: 12 }}>
          <p>{statusText}</p>
          <progress value={progress} max="100" style={{ width: "100%" }} />
          <p>{progress}%</p>
        </div>
      )}

      {videoUrl && (
        <div style={{ marginTop: 16 }}>
          <h3>Generated Video</h3>
          <video src={videoUrl} controls style={{ maxWidth: "100%" }} />
        </div>
      )}
    </div>
  );
}
