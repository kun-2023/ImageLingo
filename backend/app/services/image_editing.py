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
        target_language: Literal["English", "French"],
        settings: Settings
)->bytes:
    
    prompt = (
    f"Translate the visible text into {target_language} and place it "
    "where the original text appears. Reduce shadows and improve text "
    "readability where possible. Preserve the layout, names, numbers, "
    "dates, logos, lines, and checkboxes. Leave illegible text as-is."
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