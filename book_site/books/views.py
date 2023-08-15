import os

from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from utils.mixins import ContextMixin
from .models import *
from .forms import *


class BooksHome(ContextMixin, ListView):
    model = Categories
    template_name = 'index.html'
    context_object_name = 'categories'


class ShowSubcats(ContextMixin, ListView):
    model = SubCategories
    template_name = 'sub_cats.html'
    context_object_name = 'sub_cats'

    def get(self, request, *args, **kwargs):
        if not self._sub_cats_exists():
            return redirect(reverse('books_no_sub_cat', kwargs={'cat_slug': self.kwargs['cat_slug']}))
        response = super().get(request, *args, **kwargs)
        return response

    def get_queryset(self):
        queryset = self._sub_cats_exists()
        return queryset

    def _sub_cats_exists(self):
        sub_categories = SubCategories.objects.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')
        return sub_categories


class ShowBooks(ContextMixin, ListView):
    model = Book
    paginate_by = os.getenv('PER_PAGE')
    template_name = 'books.html'
    context_object_name = 'books'

    def get_queryset(self):
        if 'sub_cat_name' in self.kwargs:
            queryset = Book.objects.filter(sub_cat__name=self.kwargs['sub_cat_name'], cat__slug=self.kwargs['cat_slug'])
        else:
            queryset = Book.objects.filter(cat__slug=self.kwargs['cat_slug'])
        return queryset


class ShowBook(ContextMixin, DetailView):
    model = Book
    template_name = 'book.html'
    context_object_name = 'book'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        book = Book.objects.filter(pk=self.kwargs['pk']).select_related('cat')
        sub_cat_title = book.values('sub_cat', 'title', 'cat')[0]
        another_books = Book.objects.filter(cat=sub_cat_title['cat']).exclude(title=sub_cat_title['title'])
        context['sub_cat'] = SubCategories.objects.filter(pk=sub_cat_title['sub_cat']).first()
        context['another_books'] = another_books
        return context

    def get_query_set(self):
        return Book.objects.select_related('cat')


class ContactView(LoginRequiredMixin, ContextMixin, CreateView):
    form_class = ContactMultiForm
    template_name = 'contact.html'
    success_url = reverse_lazy('home')


class RegisterUser(ContextMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(ContextMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'login.html'


def logout_user(request):
    logout(request)
    return redirect('login')


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


class SearchView(ContextMixin, ListView):
    model = Book
    paginate_by = os.getenv('PER_PAGE')
    template_name = 'search_result.html'
    context_object_name = 'search_result'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            queryset = Book.objects.filter(Q(author__name__icontains=query) | Q(title__icontains=query)).distinct()
            return queryset
        return super().get_queryset()
