# 이 Dockerfile은 Python 기반 Django 애플리케이션을 위한 Docker 이미지를 설정합니다.

## Base image

1. 공식 Python 이미지에서 가져온 이미지입니다.
2. 'slim' 버전을 사용하여 이미지 크기를 줄였습니다.

```docker
FROM python:3.11-slim
```

## Working directory 설정

- 컨테이너 내부의 작업 디렉터리를 /app으로 설정합니다.

```docker
WORKDIR /app
```

## Copy the requirements file

- Python 애플리케이션의 의존성을 나열한 requirements.txt 파일을 작업 디렉터리로 복사합니다.

```docker
COPY requirements.txt .
```

## Install dependencies

- requirements.txt에 나열된 의존성을 pip을 사용하여 설치합니다.

```docker
RUN pip install --no-cache-dir -r requirements.txt
```

## Copy the application code

- 애플리케이션 코드를 작업 디렉터리로 복사합니다.

```docker
COPY . .
```

## Install cron and supervisor

- cron 및 supervisor를 설치합니다.

```docker
RUN apt-get update && apt-get install -y supervisor cron && apt-get clean && rm -rf /var/lib/apt/lists/*
```

## Copy and register cron settings

- cron 설정 파일을 /etc/cron.d/news_cron으로 복사하고 권한을 설정합니다.

```docker
COPY ./cronjob.txt /etc/cron.d/news_cron
RUN chmod 0644 /etc/cron.d/news_cron
```

## Copy supervisor configuration

- supervisor 설정 파일을 /etc/supervisor/conf.d/supervisord.conf로 복사합니다.

```docker
COPY ./supervisord.conf /etc/supervisor/conf.d/supervisord.conf
```

## Create logs directory

- 로그 폴더를 생성합니다.

```docker
RUN mkdir -p /app/logs
```

## Run collectstatic command

- collectstatic 명령을 실행하여 static 파일들을 모아줍니다.

```docker
RUN python manage.py collectstatic --noinput
```

## Expose the application port

- Nginx 기본 포트인 8000번 포트를 노출합니다.

```docker
EXPOSE 8000
```

## Define the command to run the application

- supervisor를 사용하여 애플리케이션을 실행합니다.

```docker
CMD ["/usr/bin/supervisord"]
```