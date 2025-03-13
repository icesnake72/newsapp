from django.http import HttpResponse
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from newsapp.models import Articles, Category
import pytz
from datetime import datetime

def index(request):
  print(request.user)
  # select * from articles;
  # 기사들을 최신 순으로 정렬하여 가져온다.
  articles = Articles.objects.all().order_by("-created_at") # 아직 쿼리 실행되지 않음 (lazy)
  return render_articles(request, articles)

  
def render_articles(request, articles, category=None):
  # 페이지네이션 설정
  page = request.GET.get("page", 1) # 페이지 번호
  paginator = Paginator(articles, 20) # 한 페이지에 보여줄 기사 수
  
  try:
    articles_page = paginator.page(page)
  except PageNotAnInteger:  # 페이지 번호가 정수가 아닐 경우 첫 페이지로 이동
    articles_page = paginator.page(1) 
  except EmptyPage:      # 페이지 번호가 너무 크거나 없을 경우 마지막 페이지로 이동
    articles_page = paginator.page(paginator.num_pages)
  
  # 한국 시간대로 변환 및 형식 지정
  kst = pytz.timezone('Asia/Seoul')
  for article in articles:
    if isinstance(article.published_at, str):
      article.published_at = datetime.fromisoformat(article.published_at.replace('Z', '+00:00'))
    article.published_at = article.published_at.astimezone(kst)
    article.published_at = article.published_at.strftime('%Y년 %m월 %d일 %p %I:%M:%S')
  
  # 템플릿 렌더링
  template = loader.get_template("index.html")
  context = {
    "news": articles_page,  # 해당 페이지의 기사들
    "paginator": paginator, # 페이지네이션 정보
    "page_obj": articles_page, # 템플릿에서 사용하기 편하도록...
    "is_paginated": articles_page.has_other_pages(), # 페이지네이션이 되었는지 여부
    'selected_category': category,
    'categories': Category.objects.all()
  }
  
  return HttpResponse(template.render(context, request))



def category_news(request, category_id):
  print(request.user)
  # select * from articles where category_id = category_id;
  articles = Articles.objects.filter(category_id=category_id).order_by("-created_at")
  
  category = Category.objects.get(id=category_id)
  
  return render_articles(request, articles, category)
  
  