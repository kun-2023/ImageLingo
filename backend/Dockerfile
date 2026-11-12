FROM python:3.12-slim

WORKDIR /image_lingo

COPY api-requirements.txt .
RUN python -m pip install --no-cache-dir -r api-requirements.txt

COPY app/ backend/app/

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
