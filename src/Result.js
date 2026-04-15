import React from "react";
import { useLocation } from "react-router-dom";

function Result() {
  const { state } = useLocation();

  if (!state) return <h2>No ATS data found</h2>;

  return (
    <div className="app">
      <h1>ATS Score: {state.score}%</h1>

      <h2>Strong Skills</h2>
      {state.strong_skills?.map((s, i) => <p key={i}>{s}</p>)}

      <h2>OK Skills</h2>
      {state.ok_skills?.map((s, i) => <p key={i}>{s}</p>)}

      <h2>Weak Skills</h2>
      {state.weak_skills?.map((s, i) => <p key={i}>{s}</p>)}

      <h2>Missing Skills</h2>
      {state.missing_skills?.map((s, i) => <p key={i}>{s}</p>)}

      <h2>Format Feedback</h2>
      <p>{state.format_feedback}</p>
    </div>
  );
}

export default Result;