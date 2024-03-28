from django.urls import path

from . import views

app_name = "quotes"

urlpatterns = [
    path("", views.main, name="root"),
    path("<int:page>", views.main, name="root_paginate"),
    path("add_author/", views.add_author, name="add_author"),
    path("add_quote/", views.add_quote, name="add_quote"),
    path("add_tag/", views.add_tag, name="add_tag"),
    path("author/<int:author_id>", views.info_author, name="author"),
    path("tag/<int:tag_id>", views.tag, name="tag_id"),
    path("tag/<str:tag_id>", views.tag, name="tag_id"),
]
