from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User
from django.db.utils import IntegrityError  # 중복된 사용자가 있을 때 발생하는 에러
from django.contrib.auth import authenticate, login, logout

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
    print(username, useremail, password)
    
    try:
      new_user = User.objects.create_user(username, useremail, password)
      new_user.save()
      return redirect("index")
    
    except IntegrityError:
      template = loader.get_template("signup.html")
      context  = {
        'error': '이미 존재하는 사용자입니다.'
      }
      return HttpResponse(template.render(context, request))
    
    except Exception as e:
      print("Error: ", e)
      template = loader.get_template("signup.html")
      context  = {
        'error': e
      }
      return HttpResponse(template.render(context, request))
  else:
    # GET, POST가 아닌 다른 메소드로 요청이 들어온 경우
    template = loader.get_template("signup.html")
    context  = {
      'error': '잘못된 접근입니다.'
    }
    return HttpResponse(template.render(context, request))
    
  
def login_(request):
  if request.method == "GET":
    return render(request, "login.html")
  
  elif request.method == "POST":
    username = request.POST.get("UserName")
    password = request.POST.get("UserPassword")
    
    # auth_user 테이블에 저장된 사용자인지 체크
    auth_user = authenticate(username=username, password=password)
    if auth_user is not None:
      login(request, auth_user)
      return redirect("index")
    
    return redirect("login")
  


def logout_(request):
  logout(request)
  return redirect("index")  