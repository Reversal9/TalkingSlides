import { useState } from "react";
import axios from "axios";

const UploadAndPrompt = () => {
    const [file, setFile] = useState(null);
    const [prompt, setPrompt] = useState("");
    const [response, setResponse] = useState("");

    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
    };

    const handleUpload = async () => {
        if (!file || !prompt) {
            alert("Please select a PDF and enter a question.");
            return;
        }

        const formData = new FormData();
        formData.append("pdf", file);
        formData.append("prompt", prompt);

        try {
            const res = await axios.post(
                "http://localhost:8000/upload_pdf_and_ask/",
                formData,
                {
                    headers: { "Content-Type": "multipart/form-data" },
                },
            );
            setResponse(res.data.response);
        } catch (error) {
            console.error("Error:", error);
            setResponse("Failed to process the PDF.");
        }
    };

    return (
        <div>
            <h2>Upload PDF & Ask a Question</h2>
            <input type="file" accept="application/pdf" onChange={handleFileChange} />
            <textarea
                placeholder="Enter your question..."
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
            />
            <button onClick={handleUpload}>Submit</button>
            <h3>Response:</h3>
            <p>{response}</p>
        </div>
    );
};

export default UploadAndPrompt;
