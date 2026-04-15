import React from "react";

function UploadResume({ setResume }) {
  return (
    <div className="upload-box">
      <input
        type="file"
        accept=".pdf"
        onChange={(e) => setResume(e.target.files[0])}
      />
    </div>
  );
}

export default UploadResume;