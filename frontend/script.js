async function analyzeResume() {
  const file = document.getElementById("resume").files[0];
  const role = document.getElementById("role").value;

  if (!file) {
    alert("Please upload resume");
    return;
  }

  const formData = new FormData();
  formData.append("resume", file);
  formData.append("jd", role);

  const progressWrapper = document.getElementById("progressWrapper");
  const progressBar = document.getElementById("progressBar");

  progressWrapper.style.display = "block";

  let progress = 0;
  const interval = setInterval(() => {
    progress += 10;
    progressBar.style.width = progress + "%";
    progressBar.innerText = progress + "%";
    if (progress >= 90) clearInterval(interval);
  }, 300);

  try {
    const res = await fetch("https://ai-resume-analyzer-j0tt.onrender.com/analyze", {
      method: "POST",
      body: formData
    });

    const data = await res.json();

    localStorage.setItem("atsResult", JSON.stringify(data));

    progressBar.style.width = "100%";
    progressBar.innerText = "100%";

    setTimeout(() => {
      window.location.href = "result.html";
    }, 500);

  } catch (err) {
    console.error(err);
    alert("Backend error");
  }
}

function toggleFAQ(el) {
  const p = el.querySelector("p");
  p.style.display = p.style.display === "none" ? "block" : "none";
}
