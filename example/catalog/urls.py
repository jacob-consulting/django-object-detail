from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("books/", views.BookListView.as_view(), name="book-list"),
    path("books/<int:pk>/", views.BookDetailView.as_view(), name="book-detail"),
    path("authors/", views.AuthorListView.as_view(), name="author-list"),
    path("authors/<int:pk>/", views.AuthorDetailView.as_view(), name="author-detail"),
    path("publishers/", views.PublisherListView.as_view(), name="publisher-list"),
    path("publishers/<int:pk>/", views.PublisherDetailView.as_view(), name="publisher-detail"),
]
