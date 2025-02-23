import React, { useState } from "react";
import axios from "axios";

const Sync = () => {
  const [videoUrl, setVideoUrl] = useState("");
  const [audioUrl, setAudioUrl] = useState("");
  const [response, setResponse] = useState(null);

  const handleGenerate = async () => {
    if (!videoUrl || !audioUrl) {
      alert("Please enter both video and audio URLs.");
      return;
    }

    try {
      const res = await axios.post("http://127.0.0.1:8000/api/generate-lipsync/", {
        video_url: videoUrl,
        audio_url: audioUrl,
      });

      setResponse(res.data);
    } catch (error) {
      console.error("Error:", error);
      setResponse({ error: "Failed to generate lipsync" });
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Sync API Lipsync Generator</h2>
      <input
        type="text"
        placeholder="Enter Video URL"
        value={videoUrl}
        onChange={(e) => setVideoUrl(e.target.value)}
        style={{ width: "100%", marginBottom: "10px", padding: "8px" }}
      />
      <input
        type="text"
        placeholder="Enter Audio URL"
        value={audioUrl}
        onChange={(e) => setAudioUrl(e.target.value)}
        style={{ width: "100%", marginBottom: "10px", padding: "8px" }}
      />
      <button onClick={handleGenerate} style={{ padding: "10px", cursor: "pointer" }}>
        Generate Lipsync
      </button>

      {response && (
        <div style={{ marginTop: "20px" }}>
          <h3>Response:</h3>
          <pre>{JSON.stringify(response, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default Sync;
