from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post
from datetime import datetime

# Create your views here.
class NewsList(ListView):
	model = Post
	ordering = 'dateCreation'
	template_name = 'Newspaper.html'
	context_object_name = 'Newspaper'

	# def get_context_data(self, **kwargs):
	# 	context = super().get_context_data(**kwargs)
	# 	context['time_now'] = datetime.utcnow()
	# 	context['next_publication'] = None
	# 	return context

class NewsDetail(DetailView):
	model = Post
	template_name = 'News.html'
	context_object_name = 'News'