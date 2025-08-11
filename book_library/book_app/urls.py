from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index" ),
    path('about/', views.about, name="about" ),
    path('gallery/', views.gallery, name="gallery" ),
    path('contactform/', views.contactForm, name="contact_form" ),
    path('contactus/', views.contactUs, name="contact_us" ),

    path('loginform/', views.loginForm, name="login" ),
    path('loggedin/', views.loggedIn, name="loggedin" ),
    path('registeration/', views.registrationForm, name="registeration"),
    path('registered/', views.register, name="registered" ),
    path('logout/', views.logout, name="logout" ),

    path('catelog/', views.get_all_books, name="catelog" ),
    path('book/<int:id>/', views.book_detail, name='book_detail'),

    path('addform', views.book_form, name='book_form'),
    path('bookadded', views.add_book, name='book_added'),
    path('delete/<int:id>/', views.delete_book, name='delete_book'),
    path('update_form/<int:id>/', views.update_form, name='update_form'),
    path('update/<int:id>/', views.update_book, name='update_book'),

    path('request_book/<int:book_id>', views.request_book, name="request_book"),
    path('request_list/', views.request_list, name="request_list"),
    path('approve_request/<int:request_id>/', views.approve_request, name='approve_request'),
    path('reject_request/<int:request_id>/',views.reject_request, name='reject_request'),
    path('my_requests/', views.my_requests, name='my_requests'),
    path('contact_list/', views.contact_list, name='contact_list'),
]
