
import { useState } from 'react';
import axios from 'axios';

function App() {
  const [script, setScript] = useState('');
  const [videoUrl, setVideoUrl] = useState('');
  const [loading, setLoading] = useState(false);

  const generateVideo = async () => {
    setLoading(true);
    try {
      const response = await axios.post(`${import.meta.env.VITE_API_URL}/generate`, { script });
      setVideoUrl(response.data.video_url);
    } catch (err) {
      alert('Error generating video');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4 max-w-xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">AI Video Generator</h1>
      <textarea
        className="w-full p-2 border mb-4"
        rows="6"
        placeholder="Enter script here..."
        value={script}
        onChange={(e) => setScript(e.target.value)}
      ></textarea>
      <button
        className="bg-blue-600 text-white px-4 py-2 rounded"
        onClick={generateVideo}
        disabled={loading}
      >
        {loading ? 'Generating...' : 'Generate Video'}
      </button>
      {videoUrl && (
        <div className="mt-6">
          <h2 className="font-semibold mb-2">Generated Video:</h2>
          <video src={videoUrl} controls className="w-full" />
        </div>
      )}
    </div>
  );
}

export default App;
