from django.http import HttpResponse
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from newsapp.models import Articles


def index(request):
  # select * from articles;
  # 모든 기사를 최신 순으로 정렬하여 가져온다.
  articles = Articles.objects.all().order_by("-created_at")
  
  # 페이지네이션 설정
  page = request.GET.get("page", 1) # 페이지 번호
  paginator = Paginator(articles, 20) # 한 페이지에 보여줄 기사 수
  
  try:
    articles_page = paginator.page(page)
  except PageNotAnInteger:  # 페이지 번호가 정수가 아닐 경우 첫 페이지로 이동
    articles_page = paginator.page(1) 
  except EmptyPage:      # 페이지 번호가 너무 크거나 없을 경우 마지막 페이지로 이동
    articles_page = paginator.page(paginator.num_pages)
  
  
  template = loader.get_template("index.html")
  context = {
    "news": articles_page,  # 해당 페이지의 기사들
    "paginator": paginator, # 페이지네이션 정보
    "page_obj": articles_page, # 템플릿에서 사용하기 편하도록...
    "is_paginated": articles_page.has_other_pages(), # 페이지네이션이 되었는지 여부
  }
  
  return HttpResponse(template.render(context, request))

