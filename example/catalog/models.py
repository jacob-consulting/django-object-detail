from django.db import models
from django.utils import timezone


class Publisher(models.Model):
    name = models.CharField(max_length=200, help_text="Official publisher name")
    website = models.URLField(blank=True, help_text="Publisher website URL")
    founded_year = models.IntegerField(help_text="Year the publisher was founded")
    is_active = models.BooleanField(default=True, help_text="Currently accepting submissions")
    description = models.TextField(blank=True, help_text="About this publisher")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def years_in_business(self):
        return timezone.now().year - self.founded_year


class PublisherAddress(models.Model):
    publisher = models.OneToOneField(
        Publisher, on_delete=models.CASCADE, related_name="address"
    )
    street = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    class Meta:
        verbose_name = "publisher address"
        verbose_name_plural = "publisher addresses"

    def __str__(self):
        return f"{self.street}, {self.city}, {self.country}"


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True, help_text="Author's date of birth")
    biography = models.TextField(blank=True, help_text="Short biography")
    is_featured = models.BooleanField(default=False, help_text="Featured on the homepage")
    website = models.URLField(blank=True, help_text="Author's personal website")

    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def book_count(self):
        return self.books.count()


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=300, help_text="Full book title")
    summary = models.TextField(blank=True, help_text="Brief plot summary")
    price = models.DecimalField(max_digits=6, decimal_places=2, help_text="Retail price in USD")
    rating = models.FloatField(default=0.0, help_text="Average reader rating (0-5)")
    pages = models.IntegerField(default=0, help_text="Number of pages")
    is_available = models.BooleanField(default=True, help_text="Currently in stock")
    publication_date = models.DateField(
        null=True, blank=True, help_text="First publication date"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    publisher = models.ForeignKey(
        Publisher, on_delete=models.CASCADE, related_name="books"
    )
    authors = models.ManyToManyField(Author, related_name="books")
    genres = models.ManyToManyField(Genre, related_name="books")

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title

    def title_upper(self):
        return self.title.upper()

    def author_list(self):
        return ", ".join(str(a) for a in self.authors.all())
