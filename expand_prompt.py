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


def expand_prompt(spec):
    """
    Convert one structured document specification
    into one concise image-generation prompt.

    The prompt language is determined by spec["language"].
    """

    required_fields = ", ".join(spec["image_text"])
    target_language = spec["language"]

    if target_language == "Chinese":
        output_instruction = (
            "Return exactly one Chinese image-generation prompt only. "
            "Do not return English. "
            "Do not add labels, explanations, headings, or bullet points. "
            "Length target: about 100-130 Chinese characters."
        )
    elif target_language == "English":
        output_instruction = (
            "Return exactly one English image-generation prompt only. "
            "Do not return Chinese. "
            "Do not add labels, explanations, headings, or bullet points. "
            "Length target: about 70-100 words."
        )
    else:
        raise ValueError(
            f"Unsupported language: {target_language}"
        )

    user_prompt = f"""
Document type: {spec["document_type"]}

Overall description:
{spec["overall_description"]}

Layout structure:
{spec["layout_structure"]}

Required image text fields:
{required_fields}

Language of document and output prompt:
{target_language}

Orientation:
{spec["orientation"]}

Text density:
{spec["text_density"]}

Capture style:
{spec["capture_style"]}

Layout style:
{spec["layout_style"]}

Visual condition:
{spec["visual_condition"]}

Document theme:
{spec["document_theme"]}

Background:
{spec["background"]}

Generate one concise image-generation prompt based strictly on this specification.

Requirements:
1. Preserve the document type, layout, visual style, and required fields.
2. Make the document text-rich and visually realistic.
3. Avoid unnecessary words such as "sample", "fictional", "synthetic", "demo", or "example".
4. The prompt should be a single paragraph.
5. {output_instruction}
"""

    print(
        f"[API] Sending request -> "
        f"{spec['document_type']} "
        f"({target_language})"
    )

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a prompt expansion assistant for a "
                    "text-rich document image dataset. "
                    "Convert structured document specifications into "
                    "concise image-generation prompts. "
                    "Do not change the underlying document category "
                    "or required fields."
                )
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        temperature=0.8
    )

    print(
        f"[API] Response received <- "
        f"{spec['document_type']} "
        f"({target_language})"
    )

    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    test_spec = {
        "document_type": "Laboratory Test Report",
        "overall_description":
            "A realistic medical laboratory test report with dense structured text and numerical results.",
        "layout_structure":
            "Hospital or laboratory name at the top, patient information below, a large multi-row test result table in the center, and doctor information and report date at the bottom.",
        "image_text": [
            "patient name",
            "patient ID",
            "sample type",
            "collection date",
            "test item",
            "result",
            "unit",
            "reference range",
            "abnormal flag",
            "doctor",
            "report date"
        ],
        "language": "Chinese",
        "orientation": "portrait",
        "text_density": "high",
        "capture_style": "scanned printed document",
        "layout_style": "table-dominant",
        "visual_condition": "slightly uneven lighting",
        "document_theme": "standard institutional",
        "background": "slightly off-white paper"
    }

    result = expand_prompt(test_spec)
    print(result)