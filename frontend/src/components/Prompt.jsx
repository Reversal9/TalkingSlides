import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

const Prompt = () => {
  const [file, setFile] = useState(null);
  const [responseText, setResponseText] = useState("");

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file first.");
      return;
    }

    const formData = new FormData();
    formData.append("pdf", file);

    try {
      const response = await fetch("http://127.0.0.1:8000/api/generate-text/", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Failed to process the file");
      }

      const data = await response.json();
      setResponseText(data.generated_text);
    } catch (error) {
      console.error("Error:", error);
      alert("An error occurred while processing the file.");
    }
  };

  return (
    <div className="flex flex-col items-center p-6">
      <Card className="w-96 p-4">
        <CardContent className="flex flex-col items-center">
          <input type="file" accept="application/pdf" onChange={handleFileChange} />
          <Button className="mt-4" onClick={handleUpload}>
            Upload and Process
          </Button>
        </CardContent>
      </Card>
      {responseText && (
        <Card className="w-96 p-4 mt-6">
          <CardContent>
            <h2 className="text-lg font-bold">Generated Text:</h2>
            <p className="mt-2">{responseText}</p>
          </CardContent>
        </Card>
      )}
    </div>
  );
}

export default Prompt;