import React, { useEffect, useState } from "react";
import axios from "axios";

const VideoGallery = () => {
  const [videos, setVideos] = useState([]);

  useEffect(() => {
    axios.get("http://127.0.0.1:8000/videos/")
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
              src={`http://127.0.0.1:8000/media/${video.thumbnail}`}
              alt="Video Thumbnail"
              style={{ width: "200px", cursor: "pointer" }}
              onClick={() => window.open(`http://127.0.0.1:8000/video/${video.filename}`, "_blank")}
            />
            <p>{video.filename}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default VideoGallery;
