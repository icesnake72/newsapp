# Python 기반 Django 애플리케이션
FROM python:3.11-slim

# 작업 디렉터리 설정
WORKDIR /app

# 의존성 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY . .

# collectstatic 명령 실행
RUN python manage.py collectstatic --noinput

# nginx 설치
RUN apt-get update && apt-get install -y nginx && apt-get clean

# nginx 설정 복사 (nginx 폴더 내에 nginx.conf 위치 필요)
COPY nginx/nginx.conf /etc/nginx/nginx.conf

# 포트 노출 (nginx 기본 포트)
EXPOSE 80

# 실행 명령: gunicorn 백엔드와 nginx 동시 실행
CMD /bin/sh -c "gunicorn newsapp.wsgi:application --bind 0.0.0.0:8000 & nginx -g 'daemon off;'"