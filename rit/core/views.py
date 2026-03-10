from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q
import json, random

from .models import (
    Hospital, Resource, Ambulance, Doctor, Appointment,
    MedicalRecord, GovernmentHelpline, PatientProfile, Payment
)
from .forms import PatientRegistrationForm, AppointmentForm, ProfileUpdateForm


# ─── PUBLIC VIEWS ───────────────────────────────────────────────────────────────

def home(request):
    hospitals = Hospital.objects.filter(is_active=True).prefetch_related('resource')[:6]
    helplines = GovernmentHelpline.objects.filter(is_active=True)
    available_ambulances = Ambulance.objects.filter(status='available').count()
    stats = {
        'hospitals': Hospital.objects.filter(is_active=True).count(),
        'ambulances': available_ambulances,
        'doctors': sum(h.resource.available_doctors for h in hospitals if hasattr(h, 'resource')),
    }
    context = {
        'hospitals': hospitals,
        'helplines': helplines,
        'stats': stats,
        'page': 'home',
    }
    return render(request, 'core/home.html', context)


def hospitals_list(request):
    query = request.GET.get('q', '')
    city = request.GET.get('city', '')
    hospitals = Hospital.objects.filter(is_active=True).prefetch_related('resource')
    if query:
        hospitals = hospitals.filter(Q(name__icontains=query) | Q(address__icontains=query))
    if city:
        hospitals = hospitals.filter(city__icontains=city)
    cities = Hospital.objects.filter(is_active=True).values_list('city', flat=True).distinct()
    context = {'hospitals': hospitals, 'query': query, 'city': city, 'cities': cities, 'page': 'hospitals'}
    return render(request, 'core/hospitals.html', context)


def hospital_detail(request, pk):
    hospital = get_object_or_404(Hospital, pk=pk, is_active=True)
    ambulances = hospital.ambulances.filter(status='available')
    doctors = hospital.doctors.filter(is_active=True).order_by('specialization', 'name')
    # Group doctors by specialization
    from itertools import groupby
    doctors_by_spec = {}
    for doc in doctors:
        spec = doc.get_specialization_display()
        doctors_by_spec.setdefault(spec, []).append(doc)
    context = {
        'hospital': hospital,
        'ambulances': ambulances,
        'doctors': doctors,
        'doctors_by_spec': doctors_by_spec,
        'page': 'hospitals',
    }
    return render(request, 'core/hospital_detail.html', context)


def ambulance_tracking(request):
    ambulances = Ambulance.objects.select_related('hospital').all()
    context = {'ambulances': ambulances, 'page': 'ambulance'}
    return render(request, 'core/ambulance.html', context)


# ─── AUTH VIEWS ─────────────────────────────────────────────────────────────────

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.first_name}! Your account has been created.')
            return redirect('dashboard')
    else:
        form = PatientRegistrationForm()
    return render(request, 'core/register.html', {'form': form, 'page': 'register'})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect(request.GET.get('next', 'dashboard'))
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form, 'page': 'login'})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


# ─── PATIENT DASHBOARD ──────────────────────────────────────────────────────────

@login_required
def dashboard(request):
    appointments = Appointment.objects.filter(patient=request.user).select_related('hospital')[:5]
    records = MedicalRecord.objects.filter(patient=request.user).select_related('hospital')[:3]
    upcoming = Appointment.objects.filter(
        patient=request.user,
        status__in=['pending', 'confirmed'],
        scheduled_at__gte=timezone.now()
    ).count()
    context = {
        'appointments': appointments,
        'records': records,
        'upcoming': upcoming,
        'page': 'dashboard',
    }
    return render(request, 'core/dashboard.html', context)


@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appt = form.save(commit=False)
            appt.patient = request.user
            appt.save()
            # Decrement 1 available bed for every booking
            try:
                res = appt.hospital.resource
                if res.available_beds > 0:
                    res.available_beds -= 1
                    res.save()
            except Resource.DoesNotExist:
                pass
            messages.success(request, 'Appointment booked! We will notify you and your relative shortly.')
            return redirect('dashboard')
    else:
        form = AppointmentForm()
        hospital_id = request.GET.get('hospital')
        if hospital_id:
            form.fields['hospital'].initial = hospital_id
    return render(request, 'core/book_appointment.html', {'form': form, 'page': 'book'})


@login_required
def my_appointments(request):
    appointments = Appointment.objects.filter(patient=request.user).select_related('hospital')
    context = {'appointments': appointments, 'page': 'dashboard'}
    return render(request, 'core/appointments.html', context)


@login_required
def cancel_appointment(request, pk):
    appt = get_object_or_404(Appointment, pk=pk, patient=request.user)
    if appt.status not in ['completed', 'cancelled']:
        appt.status = 'cancelled'
        appt.save()
        messages.success(request, 'Appointment cancelled.')
    return redirect('my_appointments')


@login_required
def medical_records(request):
    records = MedicalRecord.objects.filter(patient=request.user).select_related('hospital')
    context = {'records': records, 'page': 'dashboard'}
    return render(request, 'core/medical_records.html', context)


@login_required
def profile_view(request):
    try:
        profile = request.user.patient_profile
    except PatientProfile.DoesNotExist:
        profile = PatientProfile.objects.create(user=request.user, phone='')

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.email = form.cleaned_data['email']
            request.user.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=profile, initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        })
    return render(request, 'core/profile.html', {'form': form, 'profile': profile, 'page': 'profile'})


# ─── PAYMENT ────────────────────────────────────────────────────────────────────

@login_required
def payment_view(request, appt_id):
    appt = get_object_or_404(Appointment, pk=appt_id, patient=request.user)
    if request.method == 'POST':
        method = request.POST.get('method', 'upi')
        amount = request.POST.get('amount', '500')
        Payment.objects.update_or_create(
            appointment=appt,
            defaults={
                'amount': amount,
                'method': method,
                'status': 'completed',
                'transaction_id': f'TXN{random.randint(100000, 999999)}',
            }
        )
        messages.success(request, '💳 Payment successful! Your cashless transaction is complete.')
        return redirect('dashboard')
    return render(request, 'core/payment.html', {'appointment': appt, 'page': 'dashboard'})


# ─── ADMIN PORTAL ────────────────────────────────────────────────────────────────

def admin_login_view(request):
    """Separate login page restricted to staff/superusers."""
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_staff or user.is_superuser:
                login(request, user)
                messages.success(request, f'Welcome, Admin {user.username}!')
                return redirect('admin_dashboard')
            else:
                return render(request, 'core/admin_login.html', {
                    'form': form,
                    'error': 'Access denied. You do not have admin privileges.',
                })
    else:
        form = AuthenticationForm()
    return render(request, 'core/admin_login.html', {'form': form})


def admin_logout_view(request):
    logout(request)
    return redirect('admin_login')


def _require_admin(request):
    """Return None if ok, or a redirect response."""
    if not request.user.is_authenticated:
        return redirect('admin_login')
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'Admin access required.')
        return redirect('admin_login')
    return None


def admin_dashboard_view(request):
    guard = _require_admin(request)
    if guard:
        return guard

    # Filters
    filter_status = request.GET.get('status', '')
    filter_type = request.GET.get('type', '')
    bookings = Appointment.objects.select_related('patient', 'hospital').order_by('-created_at')
    if filter_status:
        bookings = bookings.filter(status=filter_status)
    if filter_type:
        bookings = bookings.filter(appointment_type=filter_type)

    hospitals = Hospital.objects.filter(is_active=True).prefetch_related('resource')

    context = {
        'bookings': bookings,
        'hospitals': hospitals,
        'total_bookings': Appointment.objects.count(),
        'confirmed_bookings': Appointment.objects.filter(status='confirmed').count(),
        'pending_bookings': Appointment.objects.filter(status='pending').count(),
        'emergency_bookings': Appointment.objects.filter(appointment_type='emergency').count(),
        'filter_status': filter_status,
        'filter_type': filter_type,
        'page': 'admin',
    }
    return render(request, 'core/admin_dashboard.html', context)


def admin_confirm_booking(request, pk):
    guard = _require_admin(request)
    if guard:
        return guard
    appt = get_object_or_404(Appointment, pk=pk)
    if appt.status == 'pending':
        appt.status = 'confirmed'
        appt.save()
        messages.success(request, f'Booking #{pk} confirmed.')
    return redirect('admin_dashboard')


def admin_cancel_booking(request, pk):
    guard = _require_admin(request)
    if guard:
        return guard
    appt = get_object_or_404(Appointment, pk=pk)
    if appt.status not in ['completed', 'cancelled']:
        appt.status = 'cancelled'
        appt.save()
        # Restore the bed
        try:
            appt.hospital.resource.available_beds += 1
            appt.hospital.resource.save()
        except Resource.DoesNotExist:
            pass
        messages.success(request, f'Booking #{pk} cancelled and bed restored.')
    return redirect('admin_dashboard')


# ─── AJAX / API ──────────────────────────────────────────────────────────────────

def api_hospital_resources(request, pk):
    hospital = get_object_or_404(Hospital, pk=pk)
    try:
        r = hospital.resource
        data = {
            'available_beds': r.available_beds,
            'total_beds': r.total_beds,
            'available_icu': r.available_icu,
            'total_icu': r.total_icu,
            'available_doctors': r.available_doctors,
            'updated_at': r.updated_at.strftime('%H:%M'),
        }
    except Resource.DoesNotExist:
        data = {'error': 'No resource data'}
    return JsonResponse(data)


def api_ambulance_locations(request):
    ambulances = Ambulance.objects.all()
    data = [{
        'id': a.id,
        'vehicle_number': a.vehicle_number,
        'status': a.status,
        'status_display': a.get_status_display(),
        'type': a.get_ambulance_type_display(),
        'lat': float(a.current_latitude),
        'lng': float(a.current_longitude),
        'eta': a.eta_minutes,
        'driver': a.driver_name,
        'phone': a.driver_phone,
        'hospital': a.hospital.name if a.hospital else 'Independent',
    } for a in ambulances]
    return JsonResponse({'ambulances': data})
