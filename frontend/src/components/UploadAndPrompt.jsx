import { useState } from "react";
import axios from "axios";

const UploadAndPrompt = () => {
    const [text, setText] = useState("");
    const [fileId, setFileId] = useState(""); // Optional: If using a file ID
    const [response, setResponse] = useState("");
    const [loading, setLoading] = useState(false);

    const handleSubmit = async () => {
        if (!text.trim()) {
            alert("Please enter a prompt.");
            return;
        }

        setLoading(true);

        try {
            // Construct URL with text or fileId as a parameter
            const apiUrl = `http://localhost:8000/upload_pdf_and_ask/${fileId}/`;

            const res = await axios.get(apiUrl); // Send request via GET method

            setResponse(res.data.response);
        } catch (error) {
            console.error("Error:", error);
            setResponse("Failed to process the request.");
        }

        setLoading(false);
    };

    return (
        <div>
            <h2>Enter a Prompt</h2>
            <textarea
                placeholder="Type your prompt here..."
                value={text}
                onChange={(e) => setText(e.target.value)}
                rows={4}
            />
            <input
                type="text"
                placeholder="Enter file ID (optional)"
                value={fileId}
                onChange={(e) => setFileId(e.target.value)}
            />
            <button onClick={handleSubmit} disabled={loading}>
                {loading ? "Processing..." : "Submit"}
            </button>
            {response && (
                <div>
                    <h3>Response:</h3>
                    <p>{response}</p>
                </div>
            )}
        </div>
    );
};

export default UploadAndPrompt;
