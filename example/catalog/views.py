from django.views.generic import DetailView, ListView

from django_object_detail.conf import get_icons_library
from django_object_detail.config import BadgeConfig, x
from django_object_detail.views import ObjectDetailMixin

from .models import Author, Book, Publisher

_FA_ICONS = {
    "book": "book",
    "cart-check": "cart-shopping",
    "building": "building",
    "geo-alt": "location-dot",
    "people": "users",
    "tags": "tags",
    "gear": "gear",
    "person": "user",
    "calendar": "calendar",
    "journal-text": "file-lines",
    "info-circle": "circle-info",
}


def _icon(name):
    """Return the icon name for the active library."""
    if get_icons_library() == "fontawesome":
        return _FA_ICONS.get(name, name)
    return name


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
            "icon": _icon("book"),
            "description": "Core book details",
            "properties": [
                "title",
                x("pages", title="Page Count"),
                "price",
                x("rating", template="catalog/star_rating.html"),
                x(
                    "rating",
                    title="Rating Badge",
                    badge=BadgeConfig(
                        color_fn=lambda r: "success" if r >= 4 else "warning" if r >= 2.5 else "danger",
                    ),
                ),
            ],
        },
        {
            "title": "Availability",
            "icon": _icon("cart-check"),
            "description": "Stock and publication status",
            "properties": [
                x(
                    "is_available",
                    badge=BadgeConfig(
                        color_map={True: "success", False: "danger"},
                        label_map={True: "In Stock", False: "Out of Stock"},
                        pill=True,
                    ),
                ),
                "publication_date",
            ],
        },
        {
            "title": "Publisher",
            "icon": _icon("building"),
            "description": "Publishing house details",
            "properties": [
                x("publisher", link="publisher-detail"),
                x("publisher__website", title="Publisher Website"),
                x("publisher__founded_year", title="Founded"),
            ],
        },
        {
            "title": "Publisher Location",
            "icon": _icon("geo-alt"),
            "description": "Publisher address via FK→O2O traversal",
            "properties": [
                x("publisher__address__street", title="Street"),
                x("publisher__address__city", title="City"),
                x("publisher__address__country", title="Country"),
            ],
        },
        {
            "title": "Authors",
            "icon": _icon("people"),
            "description": "All authors of this book",
            "properties": [
                "authors",
            ],
        },
        {
            "title": "Genres",
            "icon": _icon("tags"),
            "description": "Book categories",
            "properties": [
                "genres",
            ],
        },
        {
            "title": "Methods & Computed",
            "icon": _icon("gear"),
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
            "icon": _icon("person"),
            "description": "Personal information",
            "properties": [
                "first_name",
                "last_name",
                x("get_full_name", title="Full Name"),
                x(
                    "book_count",
                    title="Number of Books",
                    type="integer",
                    badge=BadgeConfig(
                        color_fn=lambda n: "success" if n >= 5 else "info" if n >= 1 else "secondary",
                        pill=True,
                    ),
                ),
            ],
        },
        {
            "title": "Dates & Status",
            "icon": _icon("calendar"),
            "properties": [
                "date_of_birth",
                x(
                    "is_featured",
                    badge=BadgeConfig(
                        color_map={True: "primary", False: "secondary"},
                        label_map={True: "Featured", False: "Standard"},
                    ),
                ),
                "website",
            ],
        },
        {
            "title": "Biography",
            "icon": _icon("journal-text"),
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
            "icon": _icon("building"),
            "description": "Publisher details",
            "properties": [
                "name",
                "website",
                x("is_active", badge="success"),
                x(
                    "founded_year",
                    badge=BadgeConfig(
                        color_fn=lambda y: "dark" if y < 1950 else "info" if y < 2000 else "light",
                    ),
                ),
                x("years_in_business", title="Years in Business", type="integer"),
            ],
        },
        {
            "title": "Address",
            "icon": _icon("geo-alt"),
            "description": "Office location via reverse O2O",
            "properties": [
                x("address__street", title="Street"),
                x("address__city", title="City"),
                x("address__country", title="Country"),
            ],
        },
        {
            "title": "About",
            "icon": _icon("info-circle"),
            "properties": [
                "description",
            ],
        },
    ]
