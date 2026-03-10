from django.urls import path
from . import views

urlpatterns = [
    # Public
    path('', views.home, name='home'),
    path('hospitals/', views.hospitals_list, name='hospitals'),
    path('hospitals/<int:pk>/', views.hospital_detail, name='hospital_detail'),
    path('ambulance/', views.ambulance_tracking, name='ambulance'),

    # Auth
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Patient Portal
    path('dashboard/', views.dashboard, name='dashboard'),
    path('appointments/', views.my_appointments, name='my_appointments'),
    path('appointments/book/', views.book_appointment, name='book_appointment'),
    path('appointments/<int:pk>/cancel/', views.cancel_appointment, name='cancel_appointment'),
    path('appointments/<int:appt_id>/pay/', views.payment_view, name='payment'),
    path('records/', views.medical_records, name='medical_records'),
    path('profile/', views.profile_view, name='profile'),

    # APIs
    path('api/hospital/<int:pk>/resources/', views.api_hospital_resources, name='api_hospital_resources'),
    path('api/ambulances/', views.api_ambulance_locations, name='api_ambulance_locations'),

    # Admin Portal
    path('admin-portal/login/', views.admin_login_view, name='admin_login'),
    path('admin-portal/logout/', views.admin_logout_view, name='admin_logout'),
    path('admin-portal/dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('admin-portal/bookings/<int:pk>/confirm/', views.admin_confirm_booking, name='admin_confirm_booking'),
    path('admin-portal/bookings/<int:pk>/cancel/', views.admin_cancel_booking, name='admin_cancel_booking'),
]
