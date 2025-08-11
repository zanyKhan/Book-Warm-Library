from django.contrib import admin   # admin123 admin@gmail.com
from book_app.models import LibraryUser, ContactUs, Book, BookRequest

# Register your models here.
admin.site.register(LibraryUser)
admin.site.register(ContactUs)
admin.site.register(Book)
admin.site.register(BookRequest)

