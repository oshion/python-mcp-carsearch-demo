FROM python:3.10-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# Smithery에서는 명령어를 smithery.yaml에서 제공하므로 CMD는 실제로 사용되지 않지만
# 로컬 테스트를 위해 유지
CMD ["python", "-m", "app.main"]