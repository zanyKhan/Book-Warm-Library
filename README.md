# 📚 Book-Warm-Library

**Book-Warm-Library** is a Django-based library management system that allows users to browse available books, request them, and manage their borrowing.  
It also provides an admin interface for managing books, approving/rejecting requests, and tracking returns.

---

## 🚀 Features

- **User Registration & Login**
- **Book Browsing**
- **Book Request System**
- **Admin Approval / Rejection**
- **Track Borrowed & Returned Books**
- **Contact Us Form**
- **Automatic Book Expiry Check**

---

## 📂 Project Structure

```
book_library/ # Main project folder
│
├── book_app/ # Django app containing models, views, and URLs
├── book_library/ # Django project settings, URLs, and WSGI
├── static/ # Static files (CSS, JS, Images)
├── templates/ # HTML templates for pages
├── .gitignore # Files/folders to ignore in Git
├── manage.py # Django management script
```

## ⚙️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/zanyKhan/Book-Warm-Library.git
   cd Book-Warm-Library
   cd book_library

2. **Create and activate a virtual environment**
   ```bash
    python -m venv env
    source env/bin/activate     # On Linux/Mac
    env\Scripts\activate        # On Windows

4. **Install dependencies**
   ```bash
    pip install -r requirements.txt

6. **Run database migrations**
   ```bash
    python manage.py makemigrations
    python manage.py migrate

8. **Start the development server**
   ```bash
    python manage.py runserver

**🛠️ Usage**

    Visit http://127.0.0.1:8000/ in your browser.
    Register a new user or log in.
    Browse books, send requests, and track your borrowed books.
    Login as admin to approve/reject book requests.

## 👩‍💻 Author

- **Name:** Zainab Khan  
- **GitHub:** [zanyKhan](https://github.com/zanyKhan)  
- **Email:** fatmazainab071@gmail.com
