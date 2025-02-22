import React, { useEffect, useState } from "react";
import axios from "axios";

const MessageFetcher = () => {
    const [message, setMessage] = useState("");
    const [error, setError] = useState(null);

    useEffect(() => {
        axios.get("http://127.0.0.1:8000/message/")
            .then(response => {
                setMessage(response.data.message);
            })
            .catch(error => {
                console.error("Error fetching the message:", error);
                setError("Failed to fetch message.");
            });
    }, []);

    return (
        <div style={{ padding: "20px", textAlign: "center" }}>
            <h2>Message from Django API</h2>
            {error ? <p style={{ color: "red" }}>{error}</p> : <p>{message}</p>}
        </div>
    );
};

export default MessageFetcher;
