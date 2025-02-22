// ViewPDF.js
import React, { useState, useEffect } from 'react';

function ViewPDF({ pdfId }) {
  const [pdfUrl, setPdfUrl] = useState(null);

  useEffect(() => {
    async function fetchPDF() {
      try {
        const response = await fetch(`http://127.0.0.1:8000/view_pdf/${pdfId}/`);
        if (!response.ok) {
          throw new Error('Failed to fetch PDF');
        }
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        setPdfUrl(url);
      } catch (error) {
        console.error('Error fetching PDF:', error);
      }
    }

    fetchPDF();

    // Clean up the object URL when the component unmounts
    return () => {
      if (pdfUrl) URL.revokeObjectURL(pdfUrl);
    };
  }, [pdfId]);

  return (
    <div>
      <h2>View PDF</h2>
      {pdfUrl ? (
        <iframe
          src={pdfUrl}
          width="100%"
          height="600px"
          title="PDF Viewer"
        />
      ) : (
        <p>Loading PDF...</p>
      )}
    </div>
  );
}

export default ViewPDF;
