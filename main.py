# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/")
# def read_root():
#     return {"message": "Sai's GenAI journey has started 🚀"}

# @app.get("/hello/{name}")
# def say_hello(name: str):
#     return {"message": f"Hello {name}, welcome to GenAI 🚀"}

# @app.get("/new/{name}")
# def say_new(name: str):
#     return {"message": f"Hello {name}, welcome to GenAI 🚀"}

# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel, Field
# from fastapi.middleware.cors import CORSMiddleware
# app = FastAPI()

# # Request model
# class ResumeRequest(BaseModel):
#     resume_text: str = Field(..., min_length=50, max_length=4000)

# # Success response model
# class ResumeData(BaseModel):
#     name: str | None
#     email: str | None
#     skills: list[str]
#     years_of_experience: int | None
#     education: list[str]
#     summary: str | None

# class ResumeResponse(BaseModel):
#     status: str
#     data: ResumeData | None = None
#     message: str | None = None

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # for development
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.post("/analyze", response_model=ResumeResponse)
# def analyze_resume(request: ResumeRequest):

#     # Simulated LLM output
#     mock_output = {
#         "name": "Sai Kumar",
#         "email": "sai@example.com",
#         "skills": ["Python", "FastAPI", "AI"],
#         "years_of_experience": 3,
#         "education": ["B.Tech Computer Science"],
#         "summary": "Backend developer with interest in AI systems."
#     }

#     return {
#         "status": "success",
#         "data": mock_output
#     }

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
import logging

app = FastAPI()

# -----------------------------
# Enable CORS
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # dev only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Logging Setup
# -----------------------------
logging.basicConfig(level=logging.INFO)

llm_call_count = 0

# -----------------------------
# Request Model
# -----------------------------
class ResumeRequest(BaseModel):
    resume_text: str = Field(..., min_length=50, max_length=4000)

# -----------------------------
# Response Models
# -----------------------------
class ResumeData(BaseModel):
    name: str | None
    email: str | None
    skills: list[str]
    years_of_experience: int | None
    education: list[str]
    summary: str | None

class ResumeResponse(BaseModel):
    status: str
    data: ResumeData | None = None
    message: str | None = None


# -----------------------------
# Fake LLM Extraction (Mock)
# -----------------------------
def fake_llm_extraction(resume_text: str):

    words = resume_text.strip().split()
    name = " ".join(words[:2]) if len(words) >= 2 else None

    skills = []
    if "Python" in resume_text:
        skills.append("Python")
    if "Machine Learning" in resume_text:
        skills.append("Machine Learning")
    if "AI" in resume_text:
        skills.append("AI")

    return {
        "name": name,
        "email": None,
        "skills": skills,
        "years_of_experience": None,
        "education": [],
        "summary": "Simulated extraction from resume text."
    }


# -----------------------------
# LLM Abstraction Layer
# -----------------------------
def call_llm(resume_text: str):
    global llm_call_count
    max_retries = 2
    attempt = 0

    while attempt < max_retries:
        try:
            logging.info(f"LLM attempt {attempt + 1}")

            result = fake_llm_extraction(resume_text)

            if result:
                
                llm_call_count += 1
                logging.info(f"Total LLM calls so far: {llm_call_count}")
                return result

        except Exception as e:
            logging.error(f"LLM error: {e}")

        attempt += 1

    


    return None



# -----------------------------
# Analyze Endpoint
# -----------------------------
@app.post("/analyze", response_model=ResumeResponse)
def analyze_resume(request: ResumeRequest):

    logging.info("Resume received for analysis")

    result = call_llm(request.resume_text)

    if result is None:
        return {
            "status": "error",
            "message": "Resume analysis failed."
        }

    try:
        validated_data = ResumeData(**result)
    except Exception as e:
        logging.error(f"Validation failed: {e}")
        return {
            "status": "error",
            "message": "Invalid data format from LLM."
        }

    return {
        "status": "success",
        "data": validated_data
    }


