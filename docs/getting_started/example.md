# Example Application

The repository includes a full **bookshop** application that demonstrates all features of `django-object-detail`.

It contains three models — `Book`, `Author`, and `Publisher` — with detail views showcasing:

- Field type detection (text, numbers, booleans, dates, URLs)
- FK and OneToOne traversal (e.g. `publisher__website`, `publisher__address__city`)
- M2M relations (`authors`, `genres`)
- Model methods (`title_upper()`, `get_full_name()`, `book_count()`)
- Badges with dynamic colors
- Custom templates (star rating)
- The split-card layout (default)

## Setup

Clone the repository and set up the example:

```bash
git clone https://github.com/jacob-consulting/django-object-detail.git
cd django-object-detail/example
python -m venv venv
source venv/bin/activate
pip install django django-bootstrap5
pip install -e ..
```

## Initialize the database

Run migrations and load the sample data fixture:

```bash
python manage.py migrate
python manage.py loaddata catalog
```

The fixture includes 5 books, 4 authors, 3 publishers, and 5 genres.

## Run the server

```bash
python manage.py runserver
```

Then visit [http://localhost:8000](http://localhost:8000).

## Available pages

| URL | Description |
|---|---|
| `/` | Home — list of all books |
| `/books/` | Book list |
| `/books/<id>/` | Book detail — 7 property groups |
| `/authors/` | Author list |
| `/authors/<id>/` | Author detail — 3 property groups |
| `/publishers/` | Publisher list |
| `/publishers/<id>/` | Publisher detail — 3 property groups |

## Switching to Font Awesome icons

The example app ships with Bootstrap Icons by default. To switch to Font Awesome, edit `bookshop/settings.py`:

```python
OBJECT_DETAIL_ICONS_LIBRARY = "fontawesome"
OBJECT_DETAIL_ICONS_TYPE = "solid"
```

The `"solid"` type is included in Font Awesome's free tier. Other types (`"regular"`, `"light"`, `"thin"`, `"duotone"`) require a Font Awesome Pro license.

The example views in `catalog/views.py` automatically select the correct icon names for the active library — no view changes needed.

You also need to load the Font Awesome stylesheet in your base template instead of (or in addition to) Bootstrap Icons. For example, replace:

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css">
```

with:

```html
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
```

## Key files

| File | Description |
|---|---|
| `catalog/models.py` | Book, Author, Publisher, Genre models |
| `catalog/views.py` | Detail views using `ObjectDetailMixin` |
| `catalog/fixtures/catalog.json` | Sample data |
| `bookshop/settings.py` | Django settings with template pack config |
