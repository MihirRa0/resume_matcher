import google.generativeai as genai
import json
from ..core.config import settings

# ----------------------------
# Configure API key for Gemini
# ----------------------------
genai.configure(api_key=settings.GEMINI_API_KEY)

# ----------------------------
# Use correct model name
# ----------------------------
model = genai.GenerativeModel("models/gemini-2.0-flash")  # <-- FIX

# ----------------------------
# Function to create prompt
# ----------------------------
def create_gemini_prompt(resume_text: str, jd_text: str) -> str:
    """Creates a detailed, structured prompt for the Gemini API."""
    prompt = f"""
    Analyze the following resume and job description. Your goal is to provide a precise match score and actionable recommendations.

    **Instructions:**
    1.  **Analyze and Compare**: Read the resume and the job description carefully. Identify the key skills and qualifications required by the job and those present in the resume.
    2.  **Calculate Match Score**: Calculate a match score as a percentage ($S$). Provide only a float number for the score (e.g., 87.5).
    3.  **Identify Missing Skills**: List the top 5-7 critical skills from the job description that are missing from the resume.
    4.  **Suggest Courses**: Suggest 3-5 specific online courses to acquire these skills.
    5.  **Provide Project Suggestions**: Suggest 2-3 practical project ideas to demonstrate the missing skills.
    
    **Output Format:**
    Provide your response as a single, valid JSON object. Do not include any text outside of this JSON structure. The JSON object must have these exact keys: "match_score", "missing_skills", "recommended_courses", "project_suggestions", "full_analysis_text".
    - `missing_skills`: A JSON array of simple strings.
    - `recommended_courses`: A JSON array of simple strings.
    - `project_suggestions`: A JSON array of simple strings.
    - `full_analysis_text`: A single string containing a brief summary of your analysis.

    ---
    **Job Description Text:**
    ```
    {jd_text}
    ```
    ---
    **Resume Text:**
    ```
    {resume_text}
    ```
    ---
    **JSON Output:**
    """
    return prompt

# ----------------------------
# Async function to get analysis
# ----------------------------
async def get_analysis_from_gemini(resume_text: str, jd_text: str) -> dict:
    prompt = create_gemini_prompt(resume_text, jd_text)

    try:
        # Call Gemini API
        response = await model.generate_content_async(prompt)

        # Clean up Gemini output
        json_text = response.text.strip().lstrip("```json").rstrip("```").strip()

        return json.loads(json_text)

    except json.JSONDecodeError:
        print("Error: Gemini response was not valid JSON.")
        print("Raw response:", response.text)
        raise ValueError("Gemini returned invalid JSON.")

    except Exception as e:
        print(f"Error getting analysis from Gemini: {e}")
        raise ValueError("Failed to get a valid analysis from the AI model.")
