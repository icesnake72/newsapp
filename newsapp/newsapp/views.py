from django.http import HttpResponse
from django.template import loader
from newsapp.models import Articles
from django.core.paginator import Paginator

def index(request):
  # select * from articles;
  articles = Articles.objects.all().order_by("-published_at") # 최신 뉴스부터 출력
  
  paginator = Paginator(articles, 20)  # 한 페이지에 10개씩

  page = request.GET.get("page", 1)
  page = int(page)

  page_obj = paginator.get_page(page)  # 해당 페이지 데이터
  
  template = loader.get_template("index.html")
  context = {
      "news": page_obj,
  }
  
  return HttpResponse(template.render(context, request))

