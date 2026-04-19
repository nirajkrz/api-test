FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY examples/ ./examples/
COPY auth_config.json ./auth_config.json
COPY environments.json ./environments.json
COPY README.md ./README.md

ENTRYPOINT ["python", "src/main.py"]
