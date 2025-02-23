import { useState, useEffect } from "react";
import axios from "axios";

const AudioUploadAndPlay = () => {
    const [file, setFile] = useState(null);
    const [audios, setAudios] = useState([]);
    const [selectedAudio, setSelectedAudio] = useState(null);
    const [audioSrc, setAudioSrc] = useState("");

    // Fetch audio list on component mount
    useEffect(() => {
        fetchAudios();
    }, []);

    // Fetch list of uploaded audios
    const fetchAudios = async () => {
        try {
            const response = await axios.get("http://127.0.0.1:8000/api/audios/");
            setAudios(response.data);
        } catch (error) {
            console.error("Error fetching audios:", error);
            setAudios([]);
        }
    };

    // Handle file selection
    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
    };

    // Upload audio file
    const handleUpload = async () => {
        if (!file) {
            alert("Please select an audio file to upload.");
            return;
        }

        const formData = new FormData();
        formData.append("audio", file);

        try {
            await axios.post("http://127.0.0.1:8000/api/upload-audio/", formData, {
                headers: { "Content-Type": "multipart/form-data" },
            });

            alert("Upload successful!");
            fetchAudios(); // Refresh audio list
        } catch (error) {
            console.error("Error uploading audio:", error);
            alert("Failed to upload audio.");
        }
    };

    // Play selected audio
    const handlePlayAudio = async (fileId) => {
        try {
            const response = await axios.get(
                `http://127.0.0.1:8000/api/audio/${fileId}/`,
                {
                    responseType: "blob",
                },
            );

            const audioURL = URL.createObjectURL(response.data);
            setAudioSrc(audioURL);
            setSelectedAudio(fileId);
        } catch (error) {
            console.error("Error fetching audio:", error);
            alert("Failed to play audio.");
        }
    };

    // Delete audio file
    const handleDeleteAudio = async (fileId) => {
        const confirmDelete = window.confirm(
            "Are you sure you want to delete this audio?",
        );
        if (!confirmDelete) return;

        try {
            await axios.delete(`http://127.0.0.1:8000/api/delete-audio/${fileId}/`);
            alert("Audio deleted successfully!");
            fetchAudios(); // Refresh audio list
        } catch (error) {
            console.error("Error deleting audio:", error);
            alert("Failed to delete audio.");
        }
    };

    // Play selected audio
    const handleDownloadAudio = async (fileId) => {
        try {
            const response = await axios.get(
                `http://127.0.0.1:8000/api/audio/${fileId}/`,
                {
                    responseType: "blob",
                },
            );

            const audioURL = URL.createObjectURL(response.data);
            const link = document.createElement("a");
            link.href = audioURL;
            link.download = "audio.mp3"; // Optional: Specify the file name
            link.click(); // Trigger the download
        } catch (error) {
            console.error("Error fetching audio:", error);
            alert("Failed to play audio.");
        }
    };
    return (
        <div>
            <h2>Upload Audio</h2>
            <input type="file" accept="audio/*" onChange={handleFileChange} />
            <button onClick={handleUpload}>Upload</button>

            <h2>Available Audios</h2>
            <ul>
                {audios.length > 0 ? (
                    audios.map((audio) => (
                        <li key={audio.file_id}>
                            <button onClick={() => handlePlayAudio(audio.file_id)}>
                                🎵 Play Audio
                            </button>
                            <button onClick={() => handleDeleteAudio(audio.file_id)}>
                                ❌ Delete
                            </button>
                            <button onClick={() => handleDownloadAudio(audio.file_id)}>
                                Download
                            </button>
                        </li>
                    ))
                ) : (
                    <p>No audios available.</p>
                )}
            </ul>

            {selectedAudio && (
                <div>
                    <h3>Playing Audio</h3>
                    <audio key={selectedAudio} controls autoPlay>
                        <source src={audioSrc} type="audio/mp3" />
                        Your browser does not support the audio element.
                    </audio>
                </div>
            )}
        </div>
    );
};

export default AudioUploadAndPlay;
