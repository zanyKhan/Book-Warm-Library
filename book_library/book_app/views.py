from django.shortcuts import render, redirect, get_object_or_404
from book_app.models import LibraryUser, ContactUs, Book, BookRequest
from datetime import datetime
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db.models import Q

# Create your views here.

def check_expired_books():
    requests = BookRequest.objects.filter(status='A')
    for req in requests:
        req.check_expiry()


def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contactForm(request):
    return render(request, 'contact.html')

def contactUs(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        if username == "" or email=="" or subject=="" or message =="":
            messages.warning(request, "Please fill all fields")
            return redirect('contact_form')
        
        message = ContactUs(username= username, email=email, subject=subject, message=message)
        message.save()
        return redirect('index') 
    return redirect('contact_form')
    
def loginForm(request):
    return render(request, 'login.html')

def registrationForm(request):
    return render(request, 'register.html')

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('repeatpassword')
        role = request.POST.get('role')
        date = datetime.now()

        if username == "" or email=="" or password=="" or confirm_password =="" or role == "":
            messages.warning(request, "***** Please fill all fields *****")
            return redirect('registeration') 
        elif password != confirm_password:
            messages.warning(request, "Passwords do not match!")
            return redirect('registeration')
        elif LibraryUser.objects.filter(username=username).exists():
            messages.warning(request, "User already registered!")
            return redirect('registeration')
        
        hashed_password = make_password(password)
        user = LibraryUser(username= username, email=email, password=hashed_password, role=role, created_at=date)
        user.save()

        messages.success(request, "Registration successful! Please log in.")
        return redirect('/loginform/') 
    return render(request, 'register.html')

def loggedIn(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        try:
            user = LibraryUser.objects.get(username=username)
        except LibraryUser.DoesNotExist:
            messages.warning(request, 'Invalid username')
            return redirect('registeration') 

        if check_password(password, user.password):
            request.session['username'] = user.username
            request.session['role'] = user.role
            messages.success(request, 'You Logged in Successfully')
            return redirect('/catelog/')
        else:
            messages.warning(request, 'Invalid password')
            return redirect('/loginform/') 
    return redirect('/loginform/') 
        
def logout(request):
    request.session.flush() 
    return redirect('/loginform/')

def get_all_books(request):
    if 'username' not in request.session:
        messages.warning(request, "You are not logged in")
        return redirect('/loggedin/')  
    check_expired_books()  
    books = Book.objects.all()
    return render(request, 'catelog.html', {'books':books})

def book_detail(request, id):
    check_expired_books()  #
    book = get_object_or_404(Book, id=id)
    return render(request, 'book_detail.html', {'book': book})
    
def gallery(request):
    if 'username' not in request.session:
        messages.warning(request, "You are not logged in")
        return redirect('/loggedin/')  
    images = [
        {"path": "images/gallery1.jpg", "alt": "Library Photo 1"},
        {"path": "images/gallery3.avif", "alt": "Library Photo 2"},
        {"path": "images/gallery2.avif", "alt": "Library Photo 3"},
        {"path": "images/gallery4.jpg", "alt": "Library Photo 4"},
        {"path": "images/gallery5.avif", "alt": "Library Photo 5"},
        {"path": "images/gallery6.avif", "alt": "Library Photo 6"},
    ]
    return render(request, 'gallery.html', {'images' : images})

def book_form(request):
    return render(request, 'add_book.html')

def add_book(request):
    if request.method == 'POST':
        isbn = request.POST.get('isbn')
        title = request.POST.get('title')
        author = request.POST.get('author')
        publisher = request.POST.get('publisher')
        is_available = True if request.POST.get('is_available') == 'on' else False
        category = request.POST.get('category')
        desc = request.POST.get('desc')
        image = request.FILES.get('image')
        price = request.POST.get('price')

        # Validation check
        if not all([isbn, title, author, publisher, category, desc, image, price]):
            messages.warning(request, "Fill all input box")
            return redirect('book_form')
        
        book = Book(isbn_num = isbn, title=title, author=author, publisher = publisher, is_available=is_available,
                category=category, created_At = datetime.now(), desc = desc, img = image, price=price)  
        book.save()
        
        messages.success(request, "Book Added Successfully")
        return redirect('/catelog/')
    return render(request, 'add_book.html')

def delete_book(request, id):
    book = get_object_or_404(Book, id=id)
    book.delete()
    messages.success(request, "Book Deleted Successfully")
    return redirect('/catelog/')

def update_form(request, id):
    categories_string = "Fiction,Science,History,Biography,Technology,Children"
    category_list = categories_string.split(',')

    book = get_object_or_404(Book, id=id)
    return render(request, 'update_book.html', {"book": book, 'category_list': category_list})

def update_book(request, id):
    book = get_object_or_404(Book, id = id)
    if request.method == 'POST':
        book.isbn_num = request.POST.get('isbn')
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.publisher = request.POST.get('publisher')
        book.is_available = True if request.POST.get('is_available') == 'on' else False
        book.category = request.POST.get('category')
        book.desc = request.POST.get('desc')
        book.price = request.POST.get('price')

        # Only update image if user uploads a new one
        if request.FILES.get('image'):
            book.img = request.FILES.get('image')

        book.created_At = datetime.now()  # update timestamp if needed
        book.save()

        messages.success(request, "Book updated successfully")
        return redirect('/catelog/')
    return render(request, 'update_book.html', {'book': book})

def request_book(request, book_id):
    username = request.session.get('username')
    book = get_object_or_404(Book, id=book_id)
    user = get_object_or_404(LibraryUser, username=username)

    # Check agar book already requested hai by same user
    existing_request = BookRequest.objects.filter(user=user, book=book, status='P').first()
    request_count = BookRequest.objects.filter(Q(user=user) & Q(status__in=['P', 'A'])).count()
    if existing_request:
        messages.warning(request, "You have already requested this book!")
        return redirect('/catelog/')
    if request_count >= 2:
        messages.info(request, "You have already requested for two books")
        return redirect('/catelog/')
    
    BookRequest.objects.create(user=user, book=book)

    book.is_available = False
    book.save()
    
    messages.success(request, "Request sent to admin for approval!")
    return redirect('/catelog/')

def request_list(request): 
    check_expired_books()  # 
    books = BookRequest.objects.all()
    return render(request, 'request_list.html', {'books' : books})

@require_POST
def reject_request(request, request_id):
    check_expired_books()  
    book_req = get_object_or_404(BookRequest, id=request_id)

    if book_req.status != 'P':
        messages.warning(request, "This request is already processed.")
        return redirect('request_list')
    # Status reject karo
    book_req.status = 'R'
    book_req.save()

    book = book_req.book
    book.is_available = True
    book.save()

    messages.success(request, f"Request for '{book.title}' rejected successfully.")
    return redirect('request_list')

@require_POST
def approve_request(request, request_id):
    check_expired_books()  
    book_req = get_object_or_404(BookRequest, id=request_id)

    if book_req.status != 'P':
        messages.warning(request, "This request is already processed.")
        return redirect('request_list')

   # 2 din ka approval system
    book_req.approve_request()

    messages.success(request, f"Request for '{book_req.book.title}' approved successfully.")
    return redirect('request_list')

def my_requests(request):
    username = request.session.get('username')
    if not username:
        messages.warning(request, "You need to log in first.")
        return redirect('/loginform/')
    
    check_expired_books()  
    user = get_object_or_404(LibraryUser, username=username)
    requests_list = BookRequest.objects.filter(user=user)

    return render(request, 'my_requests.html', {'requests_list': requests_list}) 

def contact_list(request):
    contacts = ContactUs.objects.all()
    return render(request, 'contact_list.html', {'contacts': contacts})