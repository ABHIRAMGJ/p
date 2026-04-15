from skills import skills_list

def extract_skills(text):
    return [skill for skill in skills_list if skill in text]

def compare(resume_text, jd_text):
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)

    matched = list(set(resume_skills) & set(jd_skills))
    missing = list(set(jd_skills) - set(resume_skills))

    score = int((len(matched) / len(jd_skills)) * 100) if jd_skills else 0

    suggestions = []
    if "aws" in missing:
        suggestions.append("Add AWS project experience")
    if "docker" in missing:
        suggestions.append("Learn Docker basics")

    return {
        "score": score,
        "matched_skills": matched,
        "missing_skills": missing,
        "suggestions": suggestions
    }