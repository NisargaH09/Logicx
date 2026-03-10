from django.contrib import admin
from .models import (Hospital, Resource, Ambulance, Doctor, PatientProfile,
                     Appointment, MedicalRecord, GovernmentHelpline, Payment)


class ResourceInline(admin.StackedInline):
    model = Resource
    extra = 1


class AmbulanceInline(admin.TabularInline):
    model = Ambulance
    extra = 1
    fields = ['vehicle_number', 'driver_name', 'ambulance_type', 'status', 'eta_minutes']


class DoctorInline(admin.TabularInline):
    model = Doctor
    extra = 1
    fields = ['name', 'specialization', 'qualifications', 'status', 'timing_start', 'timing_end', 'available_days', 'consultation_fee', 'room_number']


@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'phone', 'is_active']
    list_filter = ['city', 'is_active']
    search_fields = ['name', 'city']
    inlines = [ResourceInline, DoctorInline, AmbulanceInline]


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['name', 'specialization', 'hospital', 'status', 'timing_start', 'timing_end', 'available_days', 'consultation_fee']
    list_filter = ['specialization', 'status', 'available_days', 'hospital']
    list_editable = ['status']
    search_fields = ['name', 'specialization', 'hospital__name']
    list_select_related = ['hospital']


@admin.register(Ambulance)
class AmbulanceAdmin(admin.ModelAdmin):
    list_display = ['vehicle_number', 'driver_name', 'ambulance_type', 'status', 'hospital', 'eta_minutes']
    list_filter = ['status', 'ambulance_type']
    list_editable = ['status', 'eta_minutes']


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'hospital', 'appointment_type', 'status', 'scheduled_at']
    list_filter = ['status', 'appointment_type']
    search_fields = ['patient__username', 'hospital__name']


@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ['patient', 'hospital', 'doctor_name', 'created_at']
    search_fields = ['patient__username', 'diagnosis']


@admin.register(GovernmentHelpline)
class GovernmentHelplineAdmin(admin.ModelAdmin):
    list_display = ['name', 'number', 'category', 'is_active']
    list_editable = ['is_active']


@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'blood_group']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['appointment', 'amount', 'method', 'status', 'transaction_id', 'created_at']
    list_filter = ['status', 'method']
