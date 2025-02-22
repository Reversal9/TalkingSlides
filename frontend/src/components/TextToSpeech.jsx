import { useState } from "react";
import axios from "axios";

const TextToSpeech = () => {
  const [text, setText] = useState("");
  const [audioUrl, setAudioUrl] = useState("");

  const handleGenerateSpeech = async () => {
    if (!text) {
      alert("Enter some text to convert to speech.");
      return;
    }

    const formData = new FormData();
    formData.append("text", text);

    try {
      const response = await axios.post("http://127.0.0.1:8000/text-to-speech/", formData, {
        responseType: "blob", // Receive audio as a binary blob
      });

      const audioBlob = new Blob([response.data], { type: "audio/mpeg" });
      const url = URL.createObjectURL(audioBlob);
      setAudioUrl(url);
    } catch (error) {
      console.error("Error generating speech:", error);
    }
  };

  return (
    <div>
      <h2>Text-to-Speech</h2>
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Enter text to convert to speech..."
      />
      <button onClick={handleGenerateSpeech}>Convert to Speech</button>
      {audioUrl && (
        <div>
          <h3>Generated Audio:</h3>
          <audio controls>
            <source src={audioUrl} type="audio/mpeg" />
            Your browser does not support the audio element.
          </audio>
        </div>
      )}
    </div>
  );
};

export default TextToSpeech;
