import base64
import os

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)
model_name = os.getenv("MODEL_NAME", "gpt-5.6-luna")

async def analyze_question(image_bytes: bytes) -> str:

    base64_image = base64.b64encode(image_bytes).decode("utf-8")

    response = client.responses.create(
        model=model_name,
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": """
Analyze this image as a practice/study question.

Identify the question and its visible answer choices.

Determine the correct answer.

Return ONLY this format:

ANSWER: <answer>

Do not provide a long explanation.
If it is multiple choice, return the option letter and short answer.

If the image is unreadable, return:

ANSWER: UNREADABLE
"""
                    },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{base64_image}",
                        "detail": "high"
                    }
                ]
            }
        ]
    )

    return response.output_text