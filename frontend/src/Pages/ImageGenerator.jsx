// frontend/src/pages/ImageGenerator.jsx
import React, { useState } from "react";

export default function ImageGenerator() {
  const [prompt, setPrompt] = useState("A cinematic portrait, ultra-detailed");
  const [imageUrl, setImageUrl] = useState("");

  const generate = async () => {
    const res = await fetch("/api/image/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt })
    });
    const j = await res.json();
    if (res.ok) {
      setImageUrl(j.url || j.path || "");
    } else {
      alert(j.detail || "Failed to generate image");
    }
  };

  return (
    <div>
      <h2>Image / Thumbnail Generator</h2>
      <textarea rows={4} style={{ width: "100%" }} value={prompt} onChange={e => setPrompt(e.target.value)} />
      <div style={{ marginTop: 8 }}>
        <button onClick={generate}>Generate Image</button>
      </div>
      {imageUrl && <div style={{ marginTop: 12 }}><img src={imageUrl} alt="ai" style={{ maxWidth: "100%" }} /></div>}
    </div>
  );
}
