import React, { useState } from "react";
import axios from "axios";

const UploadAndPrompt = () => {
    const [file, setFile] = useState(null);
    const [responseText, setResponseText] = useState("");

    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
    };

    const handleUpload = async () => {
        if (!file) {
            alert("Please select a PDF file");
            return;
        }

        const formData = new FormData();
        formData.append("pdf", file);

        try {
            const uploadRes = await axios.post("http://127.0.0.1:8000/upload_pdf/", formData);
            const fileId = uploadRes.data.file_id;
            
            // Fetch generated text after upload
            const aiRes = await axios.get(`http://127.0.0.1:8000/generate_text/${fileId}/`);
            setResponseText(aiRes.data.generated_text);

        } catch (error) {
            console.error("Error uploading file:", error);
        }
    };

    return (
        <div>
            <h2>Upload PDF and Generate AI Text</h2>
            <input type="file" accept="application/pdf" onChange={handleFileChange} />
            <button onClick={handleUpload}>Upload & Generate</button>

            {responseText && (
                <div>
                    <h3>Generated Text:</h3>
                    <p>{responseText}</p>
                </div>
            )}
        </div>
    );
};

export default UploadAndPrompt;