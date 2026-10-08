# 파이썬 경량화 공식 이미지 사용
FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY . .

# Cloud Run 기본 포트 환경변수 설정
ENV PORT=8080

# Gunicorn을 사용하여 Flask 앱 실행 (멀티 스레드 지원)
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
