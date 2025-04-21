# Python 기반 Django 애플리케이션
FROM python:3.11-slim

# 작업 디렉터리 설정
WORKDIR /app

# 의존성 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 앱 복사
COPY . .

# supervisor 설치
RUN apt-get update && apt-get install -y supervisor procps && apt-get clean && rm -rf /var/lib/apt/lists/*

# supervisor 설정 복사
COPY ./supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# 로그 폴더
RUN mkdir -p /app/logs

# collectstatic 명령 실행(static 파일들을 모아줌)
RUN python manage.py collectstatic --noinput

# 포트 노출 (nginx 기본 포트)
EXPOSE 8000

CMD ["/usr/bin/supervisord"]