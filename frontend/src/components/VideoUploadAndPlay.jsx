import { useState, useEffect } from "react";
import axios from "axios";

const VideoUploadAndPlay = () => {
    const [file, setFile] = useState(null);
    const [videos, setVideos] = useState([]);
    const [selectedVideo, setSelectedVideo] = useState(null);

    useEffect(() => {
        fetchVideos();
    }, []);

    const fetchVideos = async () => {
        try {
            <source src={`http://127.0.0.1:8000/api/video/${selectedVideo}/`} type="video/mp4" />
            
            if (response.data.videos) {
                setVideos(response.data.videos); // Ensure the data exists
            } else {
                setVideos([]); // Set an empty array if data is missing
            }
        } catch (error) {
            console.error("Error fetching videos:", error);
            setVideos([]); // Prevents undefined state if request fails
        }
    };

    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
    };

    const handleUpload = async () => {
        if (!file) {
            alert("Please select a video to upload.");
            return;
        }

        const formData = new FormData();
        formData.append("video", file);

        try {
            await axios.post("http://127.0.0.1:8000/api/upload/", formData, {
                headers: { "Content-Type": "multipart/form-data" },
            });

            alert("Upload successful!");
            fetchVideos(); // Refresh video list
        } catch (error) {
            console.error("Error uploading video:", error);
            alert("Failed to upload video.");
        }
    };

    return (
        <div>
            <h2>Upload Video</h2>
            <input type="file" accept="video/*" onChange={handleFileChange} />
            <button onClick={handleUpload}>Upload</button>

            <h2>Available Videos</h2>
            <ul>
                {videos && videos.length > 0 ? (
                    videos.map((video) => (
                        <li key={video.file_id}>
                            <button onClick={() => setSelectedVideo(video.file_id)}>
                                {video.title}
                            </button>
                        </li>
                    ))
                ) : (
                    <p>No videos available.</p>
                )}
            </ul>

            {selectedVideo && (
                <div>
                    <h3>Playing: {selectedVideo}</h3>
                    <video controls width="640">
                        <source src={`http://127.0.0.1:8000/api/video//${selectedVideo}/`} type="video/mp4" />
                        Your browser does not support the video tag.
                    </video>
                </div>
            )}
        </div>
    );
};

export default VideoUploadAndPlay;
