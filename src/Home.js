import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./App.css";

function Home() {
  const [resume, setResume] = useState(null);
  const [role, setRole] = useState("");
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);

  const navigate = useNavigate();

  const roles = [
    "Java Developer",
    "Frontend Developer",
    "Backend Developer",
    "Full Stack Developer",
    "Data Analyst",
    "Software Engineer",
    "DevOps Engineer",
    "AI Engineer",
    "Cloud Engineer",
    "Cyber Security Analyst",
  ];

  const handleAnalyze = async () => {
  if (!resume) {
    alert("Please upload resume");
    return;
  }

  setLoading(true);
  setProgress(30);

  try {
    const formData = new FormData();
    formData.append("resume", resume);
    formData.append("jd", role || "Software Engineer");

    const res = await fetch("http://127.0.0.1:8000/analyze", {
      method: "POST",
      body: formData,
    });

    if (!res.ok) {
      throw new Error("Backend failed");
    }

    setProgress(80);

    const data = await res.json();

    setProgress(100);

    navigate("/result", { state: data });
  } catch (err) {
    console.error(err);
    alert("Backend failed. Check backend terminal.");
  } finally {
    setLoading(false);
  }
};

  return (
    <div className="app">
      <h1 className="hero">
        Automated <br /> Resume <br /> Filtering
      </h1>

      <select value={role} onChange={(e) => setRole(e.target.value)}>
        <option value="">Select Role</option>
        {roles.map((r, i) => (
          <option key={i} value={r}>
            {r}
          </option>
        ))}
      </select>

      <input
        type="file"
        accept=".pdf"
        onChange={(e) => setResume(e.target.files[0])}
      />

      <button onClick={handleAnalyze}>Analyze Resume</button>

      {loading && (
        <div className="progress-bar">
          <div style={{ width: `${progress}%` }}></div>
        </div>
      )}
    </div>
  );
}

export default Home;