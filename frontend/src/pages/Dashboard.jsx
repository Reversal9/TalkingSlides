import React, { useState } from 'react';
import Popup from "../components/Popup";
import '../styles.css';
import { useNavigate } from "react-router-dom";

const Dashboard = () => {
  const [isPopupOpen, setIsPopupOpen] = useState(false);
  const navigate = useNavigate();
  const openPopup = () => setIsPopupOpen(true);
  const closePopup = () => setIsPopupOpen(false);

  return (
    <div className="dashboard">
      <h1>Dashboard</h1>
      <button className="open-popup-button" onClick={openPopup}>
        Create Video
      </button>
      <Popup show={isPopupOpen} handleClose={closePopup} />
      <button onClick={() => navigate("/")}>Log out</button>
    </div>
  );
};

export default Dashboard;
