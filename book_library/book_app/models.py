from django.db import models
from datetime import timedelta, date

# Create your models here.

class LibraryUser(models.Model):
    user_type = [
        ('A', 'admin'),
        ('U', 'user')
    ]
    username = models.CharField(unique=True, max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=150)
    role = models.CharField(max_length=1, choices=user_type, default='U')
    created_at = models.DateTimeField()

    def __str__(self):
        return self.username
    
class ContactUs(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=150)
    message = models.TextField()

    def __str__(self):
        return self.subject

class Book(models.Model):
    isbn_num = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)
    is_available = models.BooleanField(default=True)
    category = models.CharField(max_length=100)
    created_At = models.DateTimeField()
    desc = models.TextField()
    img = models.ImageField(upload_to='images/')
    price = models.FloatField()

    def __str__(self):
        return self.title

class BookRequest(models.Model):
    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('A', 'Approved'),
        ('R', 'Rejected'),
    ]

    user = models.ForeignKey(LibraryUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    request_date = models.DateTimeField(auto_now_add=True)

    # New fields for issuing period
    issued_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)


    def approve_request(self):
        self.status = 'A'
        self.issued_date = date.today()
        self.return_date = date.today() + timedelta(days=2)  # 2 din ka period
        self.book.is_available = False
        self.book.save()
        self.save()

    def check_expiry(self):
        if self.return_date and date.today() > self.return_date:
            self.status = 'R'
            self.book.is_available = True
            self.book.save()
            self.delete()  # ya self.status = 'R' karke save() karo


    def __str__(self):
        return f"{self.user.username} → {self.book.title} ({self.status})"
