import React, { useState } from "react";
import Popup from "../components/Popup";
import "../styles.css";
import { useNavigate } from "react-router-dom";
import { useAuth0 } from "@auth0/auth0-react"; // <-- Import Auth0 Hook
import TextToSpeech from "../components/TextToSpeech";
import VideoUploadAndPlay from "../components/VideoUploadAndPlay";
import UploadToPlay from "../components/UploadToAudio";
import AudioUploadAndPlay from "../components/AudioUploadAndPlay";

const Dashboard = () => {
    const { logout } = useAuth0(); // <-- Get logout function from Auth0
    const [isPopupOpen, setIsPopupOpen] = useState(false);
    const navigate = useNavigate();
    const openPopup = () => setIsPopupOpen(true);
    const closePopup = () => setIsPopupOpen(false);

    return (
        <div className="dashboard">
            <h1>Dashboard</h1>
            {/* <button className="open-popup-button" onClick={openPopup}>
                Create Video
            </button> */}
            <UploadToPlay></UploadToPlay>
            <AudioUploadAndPlay></AudioUploadAndPlay>
            <button onClick={() => logout({ returnTo: window.location.origin })}>
                Logout
            </button>
            {/* <VideoUploadAndPlay></VideoUploadAndPlay> */}
        </div>
    );
};

export default Dashboard;
