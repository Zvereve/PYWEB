from django.views import View
from django.shortcuts import render


class Note(View):
    def get(self, request):
        return