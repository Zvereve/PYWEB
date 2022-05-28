from django.shortcuts import render
from django.views import View, generic

from .models import Note



class BlogView(View):
    def get(self, request):
        context = {
            'title': 'Добро пожаловать',
            'left': 'генератор списка',
            'right': 'записи из базы данных',
            'data': [{'id': i, 'name': f'Name {i}'} for i in range(3)],
            'notes': Note.objects.all(),
        }

        return render(request, ..., context)

class HomeTemplateView(generic.TemplateView):
    template_name = ...  # todo set template

    def get_context_data(self, **kwargs):
        ...  # todo context