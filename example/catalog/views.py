from django.views.generic import DetailView, ListView

from django_object_detail.config import x
from django_object_detail.views import ObjectDetailMixin

from .models import Author, Book, Publisher


class HomeView(ListView):
    model = Book
    template_name = "catalog/home.html"
    context_object_name = "books"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["featured_authors"] = Author.objects.filter(is_featured=True)
        return context


# --- List Views ---


class BookListView(ListView):
    model = Book
    template_name = "catalog/book_list.html"
    context_object_name = "books"


class AuthorListView(ListView):
    model = Author
    template_name = "catalog/author_list.html"
    context_object_name = "authors"


class PublisherListView(ListView):
    model = Publisher
    template_name = "catalog/publisher_list.html"
    context_object_name = "publishers"


# --- Detail Views ---


class BookDetailView(ObjectDetailMixin, DetailView):
    model = Book
    template_name = "catalog/book_detail.html"
    context_object_name = "book"

    property_display = [
        {
            "title": "Basic Info",
            "icon": "book",
            "description": "Core book details",
            "properties": [
                "title",
                x("pages", title="Page Count"),
                "price",
                x("rating", template="catalog/star_rating.html"),
            ],
        },
        {
            "title": "Availability",
            "icon": "cart-check",
            "description": "Stock and publication status",
            "properties": [
                "is_available",
                "publication_date",
            ],
        },
        {
            "title": "Publisher",
            "icon": "building",
            "description": "Publishing house details",
            "properties": [
                "publisher",
                x("publisher__website", title="Publisher Website"),
                x("publisher__founded_year", title="Founded"),
            ],
        },
        {
            "title": "Publisher Location",
            "icon": "geo-alt",
            "description": "Publisher address via FK→O2O traversal",
            "properties": [
                x("publisher__address__street", title="Street"),
                x("publisher__address__city", title="City"),
                x("publisher__address__country", title="Country"),
            ],
        },
        {
            "title": "Authors",
            "icon": "people",
            "description": "All authors of this book",
            "properties": [
                "authors",
            ],
        },
        {
            "title": "Genres",
            "icon": "tags",
            "description": "Book categories",
            "properties": [
                "genres",
            ],
        },
        {
            "title": "Methods & Computed",
            "icon": "gear",
            "description": "Values computed from model methods",
            "properties": [
                x("title_upper", title="Title (uppercase)"),
                x("author_list", title="Author List (comma-separated)"),
            ],
        },
    ]


class AuthorDetailView(ObjectDetailMixin, DetailView):
    model = Author
    template_name = "catalog/author_detail.html"
    context_object_name = "author"

    property_display = [
        {
            "title": "Identity",
            "icon": "person",
            "description": "Personal information",
            "properties": [
                "first_name",
                "last_name",
                x("get_full_name", title="Full Name"),
                x("book_count", title="Number of Books", type="integer"),
            ],
        },
        {
            "title": "Dates & Status",
            "icon": "calendar",
            "properties": [
                "date_of_birth",
                "is_featured",
                "website",
            ],
        },
        {
            "title": "Biography",
            "icon": "journal-text",
            "properties": [
                "biography",
            ],
        },
    ]


class PublisherDetailView(ObjectDetailMixin, DetailView):
    model = Publisher
    template_name = "catalog/publisher_detail.html"
    context_object_name = "publisher"

    property_display = [
        {
            "title": "Company Info",
            "icon": "building",
            "description": "Publisher details",
            "properties": [
                "name",
                "website",
                "is_active",
                "founded_year",
                x("years_in_business", title="Years in Business", type="integer"),
            ],
        },
        {
            "title": "Address",
            "icon": "geo-alt",
            "description": "Office location via reverse O2O",
            "properties": [
                x("address__street", title="Street"),
                x("address__city", title="City"),
                x("address__country", title="Country"),
            ],
        },
        {
            "title": "About",
            "icon": "info-circle",
            "properties": [
                "description",
            ],
        },
    ]
