from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q

# from .utils import get_mongodb

from .models import Author, Tag, Quote
from .forms import AuthorForm, TagForm, QuoteForm


# def main(request, page=1):
#     db = get_mongodb()
#     quotes = db.quotes.find()
#     per_page = 10
#     paginator = Paginator(list(quotes), per_page)
#     quotes_on_page = paginator.get_page(page)
#     return render(request, "quotes/index.html", context={"quotes": quotes_on_page})


def main(request, page=1):
    quotes = Quote.objects.all()
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.get_page(page)
    return render(request, "quotes/index.html", context={"quotes": quotes_on_page})


def info_author(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    return render(
        request,
        "quotes/info_author.html",
        context={"title": "Quotes: author", "author": author},
    )


def tag(request, tag_id):
    per_page = 5
    if isinstance(tag_id, int):
        quotes = Quote.objects.filter(tags=tag_id).all()
    elif isinstance(tag_id, str):
        tag_filter = Tag.objects.filter(name=tag_id).first()
        quotes = Quote.objects.filter(tags=tag_filter).all()
    paginator = Paginator(list(quotes), per_page)
    page_number = request.GET.get("page")
    quotes_on_page = paginator.get_page(page_number)
    top_tags = (
        Quote.objects.values("tags__id", "tags__name")
        .annotate(quote_count=Count("tags__name"))
        .order_by("-quote_count")[:10]
    )

    return render(
        request,
        "quotes/tag.html",
        context={"quotes": quotes_on_page, "tag_id": tag_id, "top_tags": top_tags},
    )


@login_required
def add_author(request):
    form = AuthorForm(instance=Author())
    authors = Author.objects.all()
    if request.method == "POST":
        form = AuthorForm(request.POST, request.FILES, instance=Author())
        if form.is_valid():
            form.save()
            author_name = form.cleaned_data["fullname"]
            messages.success(request, f"Author with {author_name} has been added!")
            return redirect(to="quotes:add_author")
    return render(
        request,
        "quotes/add_author.html",
        context={"title": "Quotes: Add author", "authors": authors, "form": form},
    )


@login_required
def add_quote(request):
    form = QuoteForm(instance=Quote())
    if request.method == "POST":
        form = QuoteForm(request.POST, request.FILES, instance=Quote())
        if form.is_valid():
            quote = form.save()
            selected_tags = Tag.objects.filter(name__in=request.POST.getlist("tags"))
            for tag in selected_tags.iterator():
                quote.tags.add(tag)
            quote.save()
            messages.success(request, f"Quote has been added!")
            return redirect(to="quotes:add_quote")
    return render(
        request,
        "quotes/add_quote.html",
        context={"title": "Quotes: Add quote", "form": form},
    )


@login_required
def add_tag(request):
    form = TagForm(instance=Tag())
    if request.method == "POST":
        form = TagForm(request.POST, request.FILES, instance=Tag())
        if form.is_valid():
            form.save()
            messages.success(request, f"Tag has been added!")
            return redirect(to="quotes:add_tag")
    return render(
        request,
        "quotes/add_tag.html",
        context={"title": "Quotes: Add tag", "form": form},
    )
