import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("API_KEY")
base_url = os.getenv("BASE_URL")
model_name = os.getenv("MODEL_NAME")

client = OpenAI(
    api_key=api_key,
    base_url=base_url
)

response = client.chat.completions.create(
    model=model_name,
    messages=[
        {
            "role": "system",
            "content": (
                "You are a prompt expansion assistant. "
                "Rewrite structured document specifications into concise "
                "image-generation prompts."
            )
        },
        {
            "role": "user",
            "content": (
                "Document type: Medical Laboratory Test Report\n"
                "Overall description: realistic clinical report with dense text\n"
                "Layout: hospital header, patient information, result table, doctor footer\n"
                "Required fields: patient name, test item, result, unit, reference range\n\n"
                "Return one concise English image-generation prompt under 100 words."
            )
        }
    ]
)

print(response.choices[0].message.content)