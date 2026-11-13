FROM python:3.12-slim

WORKDIR /app

COPY streamlit-requirements.txt .
RUN python -m pip install --no-cache-dir -r streamlit-requirements.txt

COPY streamlit_app.py .

EXPOSE 8501

CMD ["python", "-m", "streamlit", "run", "streamlit_app.py", "--server.address=0.0.0.0","--server.port=8501"]



