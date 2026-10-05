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
        "Return exactly one detailed Chinese image-generation prompt only. "
        "Do not return English. "
        "Do not add labels, explanations, headings, or bullet points. "
        "Write one coherent paragraph of approximately 450-550 Chinese characters, "
        "with a target length of about 500 Chinese characters. "
        "Describe the document in detail, including overall appearance, "
        "layout hierarchy, text density, required fields, table or section structure, "
        "typography, spacing, visual condition, paper or screen characteristics, "
        "and realistic document presentation. "
        "Keep all details consistent with the provided structured specification."
    )
        
    elif target_language == "English":
      output_instruction = (
        "Return exactly one detailed English image-generation prompt only. "
        "Do not return Chinese. "
        "Do not add labels, explanations, headings, or bullet points. "
        "Write one coherent paragraph of approximately 180-220 words, "
        "with a target length of about 200 words. "
        "Describe the document in detail, including overall appearance, "
        "layout hierarchy, text density, required fields, table or section structure, "
        "typography, spacing, visual condition, paper or screen characteristics, "
        "and realistic document presentation. "
        "Keep all details consistent with the provided structured specification."
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
1. Preserve the exact document type and all provided structured attributes.
2. Include every required image-text field naturally in the description.
3. Describe the page composition in detail, including header, body, tables, sections, footer, and information hierarchy when applicable.
4. Clearly describe typography, spacing, alignment, text density, and the distribution of structured text across the page.
5. Include realistic visual details based on the specified capture style, visual condition, background, and document theme.
6. Make the document visually realistic and strongly text-rich.
7. Do not invent a different document category or contradict the provided specification.
8. Avoid unnecessary words such as "sample", "fictional", "synthetic", "demo", or "example".
9. Do not explain the task or discuss the prompt-generation process.
10. The final prompt must be a single coherent paragraph.
11. {output_instruction}
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
                    "detailed image-generation prompts with rich layout, text, "
                    "and visual descriptions. "
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