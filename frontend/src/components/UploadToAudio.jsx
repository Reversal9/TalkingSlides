import React, { useState } from "react";
import axios from "axios";

const UploadToPlay = () => {
  const [pdfFile, setPdfFile] = useState(null);
  const [script, setScript] = useState("");
  const [audioSrc, setAudioSrc] = useState("");
  const [category, setCategory] = useState(null);

  const handleCategorySelect = (category) => {
    setCategory(category);
  };

  const AudioCategoryComponent = () => {
    return (
      <div>
        <button
          onClick={() => handleCategorySelect("presentation")}
          style={{
            backgroundColor:
              category === "presentation" ? "#4CAF50" : "#f1f1f1",
          }}
        >
          Presentation
        </button>
        <button
          onClick={() => handleCategorySelect("podcast")}
          style={{
            backgroundColor: category === "podcast" ? "#4CAF50" : "#f1f1f1",
          }}
        >
          Podcast
        </button>
      </div>
    );
  };

  // Handle file selection
  const handleFileChange = (event) => {
    setPdfFile(event.target.files[0]);
  };

  // Upload PDF and get script
  const handleUpload = async () => {
    if (!pdfFile) {
      alert("Please select a PDF file first.");
      return;
    }

    if (!category) {
      alert("Please select a category first.");
      return;
    }

    const formData = new FormData();
    formData.append("pdf", pdfFile);
    formData.append("category", category);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/upload-pdf/",
        formData,
        {
          headers: { "Content-Type": "multipart/form-data" },
        },
      );

      if (response.data.script) {
        setScript(response.data.script);
        console.log("Script received:", response.data.script);
      } else {
        console.error("Error retrieving script:", response.data);
      }
    } catch (error) {
      console.error("Error uploading PDF:", error);
    }
  };

  // Send script to get audio
  const handleGetAudio = async () => {
    if (!script) {
      alert("No script available to convert to audio.");
      return;
    }

    if (!category) {
      alert("Please select a category first.");
      return;
    }

    const formData = new FormData();
    formData.append("script", script);
    formData.append("category", category);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/get-audio-gpt/",
        formData,
        {
          responseType: "blob", // To handle audio files
        },
      );

      const audioURL = URL.createObjectURL(response.data);
      setAudioSrc(audioURL);
      console.log("Audio generated successfully!");
    } catch (error) {
      console.error("Error fetching audio:", error);
    }
  };

  return (
    <div>
      <h2>Upload PDF and Generate Audio</h2>
      <AudioCategoryComponent />
      <input type="file" accept="application/pdf" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload PDF</button>

      {script && (
        <div>
          <h3>Generated Script</h3>
          <p>{script}</p>
          <button onClick={handleGetAudio}>Convert to Audio</button>
        </div>
      )}

      {audioSrc && (
        <div>
          <h3>Generated Audio</h3>
          <audio controls>
            <source src={audioSrc} type="audio/mp3" />
            Your browser does not support the audio element.
          </audio>
        </div>
      )}
    </div>
  );
};

export default UploadToPlay;
