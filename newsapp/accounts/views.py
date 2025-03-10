from django.shortcuts import render, redirect
from django.contrib.auth.models import User

# Create your views here.
def signup(request):
  if request.method == 'GET':
    return render(request, 'accounts/signup.html')
  
  elif request.method == 'POST':
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    password2 = request.POST['password2']
    
    if password != password2:
      return render(request, 'accounts/signup.html', {'error': '비밀번호가 일치하지 않습니다.'})

    if User.objects.filter(username=username).exists():
        return render(request, 'accounts/signup.html', {'error': '이미 존재하는 사용자입니다.'})

    user = User.objects.create_user(username=username, email=email, password=password)
    login(request, user)
    return redirect('/') 
  
def login(request):
    pass
  
def logout(request):
    pass