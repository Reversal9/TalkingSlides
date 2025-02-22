import React, { useEffect, useState } from "react";
import axios from "axios";

const VideoGallery = () => {
  const [videos, setVideos] = useState([]);

  useEffect(() => {
    axios.get("http://localhost:8000/api/videos/")
      .then(response => setVideos(response.data))
      .catch(error => console.error(error));
  }, []);

  return (
    <div>
      <h2>Video Gallery</h2>
      <div style={{ display: "flex", flexWrap: "wrap" }}>
        {videos.map(video => (
          <div key={video.filename} style={{ margin: "10px" }}>
            <img
              src={`http://localhost:8000/media/${video.thumbnail}`}
              alt="Video Thumbnail"
              style={{ width: "200px", cursor: "pointer" }}
              onClick={() => window.open(`http://localhost:8000/api/video/${video.filename}`, "_blank")}
            />
            <p>{video.filename}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default VideoGallery;
