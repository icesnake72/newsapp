#!/bin/bash
set -a
source /app/.env.prod  # 환경변수 로드
set +a

/usr/local/bin/python /app/get_news/get_news.py >> /app/logs/test.log 2>&1
