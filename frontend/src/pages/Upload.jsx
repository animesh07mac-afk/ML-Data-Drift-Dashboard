import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import "./Upload.css";

export default function Upload() {
  const [reference, setReference] = useState(null);
  const [current, setCurrent] = useState(null);

  const navigate = useNavigate();

  const analyzeData = async () => {
    if (!reference || !current) {
      alert("Please upload both CSV files.");
      return;
    }

    const formData = new FormData();
    formData.append("reference", reference);
    formData.append("current", current);

    try {
      const res = await axios.post(
        "https://ml-data-drift-dashboard-1.onrender.com/analyze",
        formData
      );

      localStorage.setItem(
        "driftResult",
        JSON.stringify(res.data)
      );

      // React Router navigation
      navigate("/dashboard");

    } catch (err) {
      console.error(err);
      alert("Error while analyzing.");
    }
  };

  return (
    <div className="upload-page">

      <div className="upload-header">
        <h1>Upload Datasets</h1>
        <p>
          Upload a reference dataset and a current dataset to detect
          data drift, validate schema, and generate reports.
        </p>
      </div>

      <div className="upload-card">

        <div className="upload-box">
          <h3>📄 Reference Dataset</h3>

          <label className="upload-btn">
            Choose CSV / Excel
            <input
              type="file"
              accept=".csv,.xlsx,.xls"
              onChange={(e) => setReference(e.target.files[0])}
              hidden
            />
          </label>

          {reference && (
            <p className="file-name">
              ✅ {reference.name}
            </p>
          )}
        </div>

        <div className="upload-box">
          <h3>📄 Current Dataset</h3>

          <label className="upload-btn">
            Choose CSV / Excel
            <input
              type="file"
              accept=".csv,.xlsx,.xls"
              onChange={(e) => setCurrent(e.target.files[0])}
              hidden
            />
          </label>

          {current && (
            <p className="file-name">
              ✅ {current.name}
            </p>
          )}
        </div>

        <button
          className="analyze-btn"
          onClick={analyzeData}
        >
          Analyze Dataset
        </button>

      </div>
    </div>
  );
}