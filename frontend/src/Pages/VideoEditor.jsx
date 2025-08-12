// frontend/src/pages/VideoEditor.jsx
import React, { useState } from "react";

export default function VideoEditor() {
  const [videoPath, setVideoPath] = useState("");
  const [start, setStart] = useState(0);
  const [end, setEnd] = useState(10);
  const [taskId, setTaskId] = useState(null);

  const doTrim = async () => {
    const res = await fetch("/api/editor/trim", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ video_path: videoPath, start, end })
    });
    const j = await res.json();
    if (res.ok) setTaskId(j.task_id);
    else alert(j.detail || "Failed to start trim");
  };

  const doStitch = async () => {
    const parts = prompt("Enter comma-separated server paths for clips to stitch (e.g. /tmp/.../clip1.mp4,/tmp/.../clip2.mp4)").split(",").map(s => s.trim());
    const res = await fetch("/api/editor/stitch", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ paths: parts })
    });
    const j = await res.json();
    if (res.ok) setTaskId(j.task_id);
    else alert(j.detail || "Failed to start stitch");
  };

  return (
    <div>
      <h2>AI Video Editor</h2>
      <p>Paste an internal server video path (or upload via media endpoint).</p>
      <input style={{ width: "100%" }} value={videoPath} onChange={e => setVideoPath(e.target.value)} placeholder="/tmp/vidcraft_jobs/....mp4" />
      <div style={{ marginTop: 8 }}>
        <label>Start (s): <input type="number" value={start} onChange={e => setStart(Number(e.target.value))} /></label>
        <label style={{ marginLeft: 12 }}>End (s): <input type="number" value={end} onChange={e => setEnd(Number(e.target.value))} /></label>
      </div>
      <div style={{ marginTop: 8 }}>
        <button onClick={doTrim}>Trim</button>
        <button onClick={doStitch} style={{ marginLeft: 8 }}>Stitch clips</button>
      </div>
      {taskId && <p>Editor task started: {taskId}</p>}
    </div>
  );
}
