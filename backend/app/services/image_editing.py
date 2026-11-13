from base64 import b64decode
from typing import Literal
from openai import OpenAI
from ..settings import Settings
import os
from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT=Path(__file__).resolve().parents[3]
file=PROJECT_ROOT/".env"
load_dotenv(file, override=True)

def edit_image(
        image_bytes: bytes,
        filename: str,
        target_language: Literal["English", "French", "Mandarin"],
        settings: Settings
)->bytes:

    language_for_prompt=(
        "Mandaine Chinese (Simplified Chinese characters)"
        if target_language=="Mandarin"
        else target_language
    )
    
    prompt = (
    f"Translate the visible text into {language_for_prompt} and place it "
    "where the original text appears. Translate every heading, paragraph,"
    "and caption in reading order. Preserve the meaning of each sentence "
    "and translate idioms naturally. Do not summarize or substitute a "
    "familiar title for the original. Keep names, dates, and numbers accurate. "
    "Adjust line breaks or reduce font size as needed so the full translation "
    "fits. Preserve the layout, logos, borders, and checkboxes. Remove shadows, "
    "improve lightings, and enhance texts readabilities if texts are blurred or difficult "
    "to recognize wherever it's possible and leave illegible text as-is."
)

    api_key=settings.openai_api_key.get_secret_value().strip()

    with OpenAI(api_key=api_key) as client:
        response=client.images.edit(
            model="gpt-image-2",
            image=(filename, image_bytes),
            prompt=prompt,
            output_format="png"
        )
    if not response.data or not response.data[0].b64_json:
        raise RuntimeError("OpenAI returned no edited image.")
    return b64decode(response.data[0].b64_json)