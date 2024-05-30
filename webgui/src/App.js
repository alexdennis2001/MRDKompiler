import React, { useState } from 'react';
import './App.css';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [imagePreviewUrl, setImagePreviewUrl] = useState(null);
  const [prediction, setPrediction] = useState(null);

  const handleImageChange = (e) => {
    let file = e.target.files[0];
    setSelectedFile(file);

    let reader = new FileReader();
    reader.onloadend = () => {
      setImagePreviewUrl(reader.result);
    };
    reader.readAsDataURL(file);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await fetch('http://localhost:8000/predict', {
        method: 'POST',
        body: formData,
      });

      const result = await response.json();
      setPrediction(result.predicted_class);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <p>
          Fruit Aquinator
        </p>
      </header>
      <div className="upload-container">
        <p>Insert the image of the fruit you wish is predicted:</p>
        <form onSubmit={handleSubmit}>
          <input type="file" onChange={handleImageChange} />
          <button type="submit">Send</button>
        </form>
        {imagePreviewUrl && (
          <div className="image-preview">
            <img src={imagePreviewUrl} alt="Preview" />
          </div>
        )}
        {prediction !== null && (
          <div className="prediction-result">
            Predicted Class: {prediction}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
