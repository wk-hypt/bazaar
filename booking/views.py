from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

# Create your views here.
def all_user(request):
    return HttpResponse("All users")

class HelloWorldView(View):
    def get(self, request):
        return HttpResponse("Hello, World!")