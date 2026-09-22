from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .ai_service import analyze_question


app = FastAPI(
    title="Question AI API"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "status": "running",
        "service": "Question AI API"
    }


@app.post("/analyze")
async def analyze(
    image: UploadFile = File(...)
):

    if not image.content_type:
        raise HTTPException(
            status_code=400,
            detail="Invalid image"
        )

    image_bytes = await image.read()

    if len(image_bytes) == 0:
        raise HTTPException(
            status_code=400,
            detail="Empty image"
        )

    try:

        answer = await analyze_question(
            image_bytes
        )

        return {
            "success": True,
            "answer": answer
        }

    except Exception as e:

        print("AI ERROR:", e)

        raise HTTPException(
            status_code=500,
            detail="AI processing failed"
        )
