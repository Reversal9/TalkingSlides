import React, { useState } from 'react';
import '../styles.css';

const Popup = ({ show, handleClose }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [error, setError] = useState('');

  if (!show) return null;

  const handleFileChange = (event) => {
    setError('');
    const file = event.target.files[0];
    if (file && file.type !== 'application/pdf') {
      setError('Only PDF files are allowed.');
      setSelectedFile(null);
    } else {
      setSelectedFile(file);
    }
  };

  const handleFileUpload = () => {
    if (selectedFile) {
      console.log("Uploading file:", selectedFile);
      // Insert your upload logic here (e.g., API call)
    } else {
      setError("Please select a valid PDF file.");
    }
  };

  return (
    <div className="popup-overlay">
      <div className="popup">
        <button className="close-button" onClick={handleClose}>X</button>
        <h2>Upload PDF File</h2>
        <input 
          type="file" 
          accept="application/pdf" 
          onChange={handleFileChange} 
        />
        {error && <p className="error">{error}</p>}
        <button onClick={handleFileUpload}>Upload</button>
      </div>
    </div>
  );
};

export default Popup;
