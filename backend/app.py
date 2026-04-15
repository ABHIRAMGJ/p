from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import pdfplumber
import tempfile
import json
from pathlib import Path
import google.generativeai as genai

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    key_path = Path(__file__).parent / "gemini_key.txt"
    with open(key_path, "r", encoding="utf-8") as f:
        gemini_key = f.read().strip()

    genai.configure(api_key=gemini_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    GEMINI_READY = True
except Exception as e:
    print("Gemini init failed:", e)
    GEMINI_READY = False


def extract_text(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text


def analyze_resume_fallback(resume_text, role):
    role_skills = {
        "Java Developer": ["java", "spring", "sql", "microservices", "rest api"],
        "Frontend Developer": ["html", "css", "javascript", "react", "bootstrap"],
        "Backend Developer": ["python", "fastapi", "sql", "api", "docker"],
        "Full Stack Developer": ["react", "node", "sql", "api", "javascript"],
        "Software Engineer": ["java", "python", "sql", "git", "api"],
        "AI Engineer": ["python", "machine learning", "nlp", "pandas", "tensorflow"],
        "DevOps Engineer": ["docker", "kubernetes", "aws", "jenkins", "linux"],
        "Cloud Engineer": ["aws", "azure", "docker", "terraform", "linux"]
    }

    target = role_skills.get(role, role_skills["Software Engineer"])
    resume_lower = resume_text.lower()

    strong = [s for s in target if s in resume_lower]
    missing = [s for s in target if s not in resume_lower]
    weak = missing[:2]
    ok = strong[1:3] if len(strong) > 2 else []

    score = min(
        92,
        max(40, int((len(strong) / len(target)) * 100) - len(missing) * 3)
    )

    return {
        "score": score,
        "strong_skills": strong,
        "ok_skills": ok,
        "weak_skills": weak,
        "missing_skills": missing,
        "format_feedback": "ATS score generated using deterministic fallback + optional Gemini enhancement.",
        "improvements": [
            f"Add experience with {m}" for m in missing[:3]
        ] + [
            "Improve project bullets with measurable outcomes",
            "Use stronger action verbs",
            "Add deployment or cloud proof"
        ]
    }


def gemini_resume_feedback(resume_text, role):
    if not GEMINI_READY:
        return []

    prompt = f"""
Analyze this resume for {role}.
Give ONLY 5 short improvement points as plain lines.
Resume:
{resume_text[:5000]}
"""

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()

        improvements = [
            line.strip("-• ").strip()
            for line in text.split("\n")
            if line.strip()
        ]

        return improvements[:5]

    except Exception as e:
        print("Gemini feedback failed:", e)
        return []


@app.post("/analyze")
async def analyze(resume: UploadFile = File(...), jd: str = Form(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp:
            temp.write(await resume.read())
            temp_path = temp.name

        resume_text = extract_text(temp_path)

        result = analyze_resume_fallback(resume_text, jd)

        semantic = gemini_resume_feedback(resume_text, jd)
        result["improvements"].extend(semantic)

        return result

    except Exception as e:
        print("Backend failed:", e)
        return {
            "score": 50,
            "strong_skills": [],
            "ok_skills": [],
            "weak_skills": [],
            "missing_skills": [],
            "format_feedback": f"Backend safe mode: {str(e)}",
            "improvements": ["Retry with a clean PDF"]
        }