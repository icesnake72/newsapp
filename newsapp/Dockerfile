# Python 기반 Django 애플리케이션
FROM python:3.11-slim

# 작업 디렉터리 설정
WORKDIR /app

# 환경 파일 복사 (선택, 컨테이너 내부에서 사용 시)
COPY .env.prod /app/.env.prod

# 의존성 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 앱 복사
COPY . .

# 크론 및 슈퍼바이저 설치
RUN apt-get update && apt-get install -y supervisor cron && apt-get clean && rm -rf /var/lib/apt/lists/*

# 크론 설정 복사 및 등록
COPY ./cronjob.txt /etc/cron.d/news_cron
RUN chmod 0644 /etc/cron.d/news_cron
RUN crontab /etc/cron.d/news_cron

# supervisor 설정 복사
COPY ./supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# 로그 폴더
RUN mkdir -p /app/logs

# 환경 변수 설정
ENV DJANGO_ENV=production

# collectstatic 명령 실행(static 파일들을 모아줌)
RUN python manage.py collectstatic --noinput

# # nginx 설치
# RUN apt-get update && apt-get install -y nginx && apt-get clean

# # nginx 설정 복사 (nginx 폴더 내에 nginx.conf 위치 필요)
# COPY nginx.conf /etc/nginx/nginx.conf

# 포트 노출 (nginx 기본 포트)
EXPOSE 8000

CMD ["/usr/bin/supervisord"]
# 실행 명령: gunicorn 백엔드와 nginx 동시 실행
# CMD ["gunicorn", "newsapp.wsgi:application", "--bind", "0.0.0.0:8000"]
# CMD /bin/sh -c "gunicorn newsapp.wsgi:application --bind 0.0.0.0:8000 & nginx -g 'daemon off;'"