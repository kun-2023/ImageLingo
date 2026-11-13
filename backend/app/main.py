from typing import Literal
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import Response
from .services.image_editing import edit_image
from .settings import Settings

app=FastAPI(title="ImageLingo")
settings=Settings()

SUPPORTED_IMAGE_TYPES={"image/jpeg", "image/png", "image/webp"}

@app.get("/health")
def health()->dict[str, str]:
    return {"status": "ok"}

@app.post(
    "/translate",
    response_class=Response,
    responses={200: {"content":{"image/png": {}}}}
)
def translate(
    image: UploadFile=File(...),
    target_language: Literal["English", "French", "Mandarin"]=Form(...),
)->Response:
    if image.content_type not in SUPPORTED_IMAGE_TYPES:
        raise HTTPException(
            status_code=415,
            detail="Upload a JPEG, PNG, or WebP image"
        )
    image_bytes=image.file.read()
    if not image_bytes:
        raise HTTPException(status_code=400, detail="The upload file is empty.")
    edited_image=edit_image(
        image_bytes=image_bytes,
        filename=image.filename or "upload",
        target_language=target_language,
        settings=settings,
    )

    return Response(content=edited_image, media_type="image/png")