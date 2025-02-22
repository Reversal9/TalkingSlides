// UploadPDF.js
import React, { useState } from 'react';

function UploadPDF() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://127.0.0.1:8000/upload_pdf/', {
        method: 'POST',
        body: formData,
      });

      const text = await response.text();
      setMessage(text);
    } catch (error) {
      console.error('Error uploading PDF:', error);
      setMessage('Upload failed.');
    }
  };

  return (
    <div>
      <h2>Upload PDF</h2>
      <form onSubmit={handleUpload} encType="multipart/form-data">
        <input
          type="file"
          accept="application/pdf"
          onChange={handleFileChange}
        />
        <button type="submit">Upload</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
}

export default UploadPDF;
