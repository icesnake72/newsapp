from django.http import HttpResponse
from django.template import loader
from newsapp.models import Articles


def index(request):
  # select * from articles;
  articles = Articles.objects.all()
  print(articles)
  
  template = loader.get_template("index.html")
  context = {
      "news": articles,
  }
  
  return HttpResponse(template.render(context, request))

