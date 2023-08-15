from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('', BooksHome.as_view(), name='home'),
    path('sub_cat/<slug:cat_slug>/', ShowSubcats.as_view(), name='sub_cat'),
    path('books/<slug:cat_slug>/', ShowBooks.as_view(), name='books_no_sub_cat'),
    path('books/<slug:cat_slug>/<str:sub_cat_name>/', ShowBooks.as_view(), name='books'),
    path('book/<int:pk>/', ShowBook.as_view(), name='book'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('search_result/', SearchView.as_view(), name='search_result'),
]


