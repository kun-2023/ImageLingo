from typing import Literal
from pydantic import BaseModel, Field

class BoundingBox(BaseModel):
    left: int=Field(description="Left edge on a 0-1000 image scale.")
    top: int=Field(description="Top edge on a 0-1000 image scale.")
    right: int=Field(description="Right edge on a 0-1000 image scale.")
    bottom: int=Field(description="Bottom edge on a 0-1000 image scale.")

class TextRegion(BaseModel):
    box: BoundingBox
    original_text: str|None
    translated_text: str|None
    readability: Literal["readable", "partially_reable", "unbearable"]

class TranslationResult(BaseModel):
    regions: list[TextRegion]