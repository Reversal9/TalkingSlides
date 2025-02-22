import { useState, useEffect } from "react";
import axios from "axios";

const VideoUploadAndPlay = () => {
    const [file, setFile] = useState(null);
    const [videos, setVideos] = useState([]);
    const [selectedVideo, setSelectedVideo] = useState(null);
    const [lastPlayedIndex, setLastPlayedIndex] = useState(-1); // Track last played video index

    useEffect(() => {
        fetchVideos();
    }, []);

    const fetchVideos = async () => {
        try {
            const response = await axios.get("http://127.0.0.1:8000/list-video/");
            setVideos(response.data);
            setLastPlayedIndex(-1); // Reset index when new videos are fetched
        } catch (error) {
            console.error("Error fetching videos:", error);
            setVideos([]);
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

    const playDifferentVideo = (clickedVideoId) => {
        if (selectedVideo === clickedVideoId) {
            // If the same video is clicked again, pick a different one
            const availableVideos = videos.filter(video => video.file_id !== selectedVideo);
            if (availableVideos.length > 0) {
                const randomVideo = availableVideos[Math.floor(Math.random() * availableVideos.length)];
                setSelectedVideo(randomVideo.file_id);
            }
        } else {
            // Select the clicked video if it's different
            setSelectedVideo(clickedVideoId);
        }
    };

    return (
        <div>
            <h2>Upload Video</h2>
            <input type="file" accept="video/*" onChange={handleFileChange} />
            <button onClick={handleUpload}>Upload</button>

            <h2>Available Videos</h2>
            <ul>
                {videos.length > 0 ? (
                    videos.map((video) => (
                        <li key={video.file_id}>
                            <button onClick={() => playDifferentVideo(video.file_id)}>
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
                    <h3>Playing Video: {selectedVideo}</h3>
                    <video key={selectedVideo} controls width="640">
                        <source src={`http://127.0.0.1:8000/api/video/${selectedVideo}/`} type="video/mp4" />
                        Your browser does not support the video tag.
                    </video>
                </div>
            )}
        </div>
    );
};

export default VideoUploadAndPlay;
