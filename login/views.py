from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View


class LoginView(View):
   def get(self, request):
       return render(request, 'login/index.html')

   def post(self, request):
       return HttpResponse(f'<h1>Hello, World</h1>')