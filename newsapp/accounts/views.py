from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User

# request method : GET, POST, PUT, DELETE, UPDATE

# Create your views here.
def signup(request):
  '''회원가입'''
  if request.method == "GET":
    return render(request, "signup.html")
  
  elif request.method == "POST":
    username = request.POST.get("UserName")
    useremail = request.POST.get("UserEmail")
    password = request.POST.get("UserPassword")
    password2 = request.POST.get("UserPassword2")
    
    try:
      new_user = User.objects.create_user(username, useremail, password)
      
      if password != password2:
        return render(request, 'accounts/signup.html', {'error': '비밀번호가 일치하지 않습니다.'})

      if User.objects.filter(username=username).exists():
        return render(request, 'accounts/signup.html', {'error': '이미 존재하는 사용자입니다.'})
      
      new_user.save()
      return redirect("index")
    
    except Exception as e:
      print("Error: ", e)
      template = loader.get_template("signup.html")
      context  = {
        'error': '이미 존재하는 사용자입니다.'
      }
      return HttpResponse(template.render(context, request))
    
  else:
    # GET, POST가 아닌 다른 메소드로 요청이 들어온 경우
    template = loader.get_template("signup.html")
    context  = {
      'error': '잘못된 접근입니다.' 
    }
    return HttpResponse(template.render(context, request))
    
  
def login(request):
  pass


def logout(request):
  pass
