import React, { useState } from "react";
import axios from "axios";

const voiceOptions = [
    "alloy",
    "ash",
    "coral",
    "echo",
    "fable",
    "onyx",
    "nova",
    "sage",
    "shimmer",
];

const UploadToPlay = () => {
    const [pdfFile, setPdfFile] = useState(null);
    const [category, setCategory] = useState(null);
    const [script, setScript] = useState("");
    const [customPrompt, setCustomPrompt] = useState("");
    const [voice, setVoice] = useState("alloy");
    const [audioFiles, setAudioFiles] = useState([]);

    // Handle file selection
    const handleFileChange = (event) => {
        setPdfFile(event.target.files[0]);
    };

    // Handle category selection (Presentation or Podcast)
    const handleCategorySelect = (selectedCategory) => {
        setCategory(selectedCategory);
        if (selectedCategory === "podcast") {
            setVoice(null); // Podcast mode doesn't require a single voice
        } else {
            setVoice("alloy"); // Default voice for presentation mode
        }
    };

    // Handle voice selection for Presentation mode
    const handleVoiceChange = (event) => {
        setVoice(event.target.value);
    };

    // Upload PDF and generate script
    const handleUpload = async () => {
        if (!pdfFile || !category) {
            alert("Please select a PDF and a category.");
            return;
        }

        const formData = new FormData();
        formData.append("pdf", pdfFile);
        formData.append("category", category);
        formData.append("custom", customPrompt);

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
                console.log("Script generated:", response.data.script);
            } else {
                console.error("Error generating script:", response.data);
            }
        } catch (error) {
            console.error("Error uploading PDF:", error);
        }
    };

    // Convert script to audio
    const handleGetAudio = async () => {
        if (!script || !category) {
            alert("No script available or category not selected.");
            return;
        }

        console.log(script, category);
        const formData = new FormData();
        formData.append("script", script);
        formData.append("category", category);

        // Include voice choices only if Presentation mode is selected
        if (category === "Presentation") {
            formData.append("voice_opt1", voice);
        }
        formData.append("voice_opt1", "alloy");
        formData.append("voice_opt2", "sage");

        console.log("This is the formData:", formData);

        try {
            const response = await axios.post(
                "http://127.0.0.1:8000/get-audio-gpt/",
                formData,
                {
                    responseType: "blob", // To handle audio files
                },
            );

            const audioURL = URL.createObjectURL(response.data);
            setAudioFiles([
                ...audioFiles,
                { id: audioFiles.length + 1, src: audioURL },
            ]);
            console.log("Audio generated successfully!");
        } catch (error) {
            console.error("Error fetching audio:", error);
        }
    };

    // Remove an audio file from the list
    const handleRemoveAudio = (index) => {
        const updatedFiles = audioFiles.filter((_, i) => i !== index);
        setAudioFiles(updatedFiles);
    };

    return (
        <div style={{ padding: "20px", maxWidth: "600px", margin: "auto" }}>
            <h2>Upload PDF and Generate Audio</h2>

            {/* Mode Selection Buttons */}
            <div>
                <button
                    onClick={() => handleCategorySelect("Presentation")}
                    style={{
                        backgroundColor:
                            category === "Presentation" ? "#4CAF50" : "#f1f1f1",
                        marginRight: "10px",
                    }}
                >
                    Presentation
                </button>
                <button
                    onClick={() => handleCategorySelect("Podcast")}
                    style={{
                        backgroundColor: category === "Podcast" ? "#4CAF50" : "#f1f1f1",
                    }}
                >
                    Podcast
                </button>
            </div>

            {/* Voice Selection for Presentation Mode */}
            {category === "Presentation" && (
                <div>
                    <label>Select Voice: </label>
                    <select value={voice} onChange={handleVoiceChange}>
                        {voiceOptions.map((v) => (
                            <option key={v} value={v}>
                                {v}
                            </option>
                        ))}
                    </select>
                </div>
            )}

            {/* Custom Prompt Input */}
            <div>
                <label>Custom Script Instructions (Optional):</label>
                <input
                    type="text"
                    value={customPrompt}
                    onChange={(e) => setCustomPrompt(e.target.value)}
                    placeholder="Add custom script modifications..."
                    style={{ width: "100%", padding: "5px", marginTop: "5px" }}
                />
            </div>

            {/* File Upload */}
            <div>
                <input
                    type="file"
                    accept="application/pdf"
                    onChange={handleFileChange}
                />
                <button onClick={handleUpload}>Upload PDF</button>
            </div>

            {/* Display Generated Script */}
            {script && (
                <div>
                    <h3>Generated Script</h3>
                    <p>{script}</p>
                    <button onClick={handleGetAudio}>Convert to Audio</button>
                </div>
            )}

            {/* Display Generated Audio Files */}
            {audioFiles.length > 0 && (
                <div>
                    <h3>Generated Audio Files</h3>
                    <ul>
                        {audioFiles.map((file, index) => (
                            <li key={file.id}>
                                <audio controls>
                                    <source src={file.src} type="audio/mp3" />
                                    Your browser does not support the audio element.
                                </audio>
                                <button onClick={() => handleRemoveAudio(index)}>Remove</button>
                                <a href={file.src} download={`audio-${file.id}.mp3`}>
                                    Download
                                </a>
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
};

export default UploadToPlay;
