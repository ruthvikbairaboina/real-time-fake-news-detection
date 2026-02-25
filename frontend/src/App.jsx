import { useState } from "react";
import "./App.css";

function App() {
  const [text, setText] = useState("");
  const [prediction, setPrediction] = useState(null);
  const [confidence, setConfidence] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async () => {
    if (!text.trim()) {
      alert("Please enter news text.");
      return;
    }

    setLoading(true);
    setError(null);
    setPrediction(null);

    try {
      const response = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });

      const data = await response.json();

      setPrediction(data.prediction);
      setConfidence((data.confidence * 100).toFixed(2));
    } catch (err) {
      setError("Failed to connect to backend.");
    }

    setLoading(false);
  };

  return (
    <div className="page">
      <div className="card">
        <h1>📰 Fake News Detector</h1>

        <textarea
          placeholder="Paste news article here..."
          value={text}
          onChange={(e) => setText(e.target.value)}
        />

        <button onClick={handleSubmit}>
          {loading ? "Analyzing..." : "Detect"}
        </button>

        {prediction && (
          <div className="result">
            <h2 className={prediction === "REAL" ? "real" : "fake"}>
              {prediction}
            </h2>
            <p>Confidence: {confidence}%</p>
          </div>
        )}

        {error && <p className="error">{error}</p>}
      </div>
    </div>
  );
}

export default App;