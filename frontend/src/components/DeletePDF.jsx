// DeletePDF.js
import React from 'react';

function DeletePDF({ pdfId, onDelete }) {
  const handleDelete = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/delete_pdf/${pdfId}/`);
      if (response.ok) {
        alert('PDF deleted successfully!');
        // Optionally, call a callback to update the UI
        if (onDelete) onDelete();
      } else {
        alert('Failed to delete PDF');
      }
    } catch (error) {
      console.error('Error deleting PDF:', error);
    }
  };

  return (
    <button onClick={handleDelete}>Delete PDF</button>
  );
}

export default DeletePDF;
