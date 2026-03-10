from django.db import models
from django.contrib.auth.models import User


class Hospital(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    emergency_contact = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='hospitals/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def availability_status(self):
        try:
            r = self.resource
            if r.available_beds > 5:
                return 'high'
            elif r.available_beds > 0:
                return 'low'
            else:
                return 'full'
        except Resource.DoesNotExist:
            return 'unknown'


class Resource(models.Model):
    hospital = models.OneToOneField(Hospital, on_delete=models.CASCADE, related_name='resource')
    total_beds = models.IntegerField(default=0)
    available_beds = models.IntegerField(default=0)
    total_icu = models.IntegerField(default=0)
    available_icu = models.IntegerField(default=0)
    total_doctors = models.IntegerField(default=0)
    available_doctors = models.IntegerField(default=0)
    ventilators_available = models.IntegerField(default=0)
    operation_theaters = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Resources @ {self.hospital.name}"

    def bed_occupancy_pct(self):
        if self.total_beds == 0:
            return 0
        return round(((self.total_beds - self.available_beds) / self.total_beds) * 100)

    def icu_occupancy_pct(self):
        if self.total_icu == 0:
            return 0
        return round(((self.total_icu - self.available_icu) / self.total_icu) * 100)


class Ambulance(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('dispatched', 'Dispatched'),
        ('en_route', 'En Route'),
        ('at_hospital', 'At Hospital'),
        ('maintenance', 'Maintenance'),
    ]
    TYPE_CHOICES = [
        ('basic', 'Basic Life Support'),
        ('advanced', 'Advanced Life Support'),
        ('neonatal', 'Neonatal'),
        ('air', 'Air Ambulance'),
    ]
    vehicle_number = models.CharField(max_length=20, unique=True)
    driver_name = models.CharField(max_length=100)
    driver_phone = models.CharField(max_length=20)
    ambulance_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='basic')
    hospital = models.ForeignKey(Hospital, on_delete=models.SET_NULL, null=True, blank=True, related_name='ambulances')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    current_latitude = models.DecimalField(max_digits=9, decimal_places=6, default=18.5204)
    current_longitude = models.DecimalField(max_digits=9, decimal_places=6, default=73.8567)
    eta_minutes = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.vehicle_number} ({self.get_status_display()})"


class Doctor(models.Model):
    SPECIALIZATION_CHOICES = [
        ('cardiology', 'Cardiology'),
        ('neurology', 'Neurology'),
        ('orthopedics', 'Orthopedics'),
        ('pediatrics', 'Pediatrics'),
        ('gynecology', 'Gynecology & Obstetrics'),
        ('oncology', 'Oncology'),
        ('dermatology', 'Dermatology'),
        ('psychiatry', 'Psychiatry'),
        ('radiology', 'Radiology'),
        ('emergency', 'Emergency Medicine'),
        ('general', 'General Medicine'),
        ('surgery', 'General Surgery'),
        ('ent', 'ENT'),
        ('ophthalmology', 'Ophthalmology'),
        ('nephrology', 'Nephrology'),
        ('pulmonology', 'Pulmonology'),
        ('gastroenterology', 'Gastroenterology'),
        ('urology', 'Urology'),
        ('anesthesiology', 'Anesthesiology'),
        ('other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('busy', 'In Consultation'),
        ('on_leave', 'On Leave'),
        ('off_duty', 'Off Duty'),
    ]
    DAY_CHOICES = [
        ('Mon-Fri', 'Monday to Friday'),
        ('Mon-Sat', 'Monday to Saturday'),
        ('Mon-Sun', 'All Days'),
        ('Mon,Wed,Fri', 'Mon / Wed / Fri'),
        ('Tue,Thu,Sat', 'Tue / Thu / Sat'),
        ('Weekdays', 'Weekdays Only'),
        ('Weekends', 'Weekends Only'),
    ]

    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='doctors')
    name = models.CharField(max_length=150)
    specialization = models.CharField(max_length=50, choices=SPECIALIZATION_CHOICES, default='general')
    qualifications = models.CharField(max_length=300, blank=True, help_text='e.g. MBBS, MD, DM (Cardiology)')
    experience_years = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    timing_start = models.TimeField(help_text='Consultation start time')
    timing_end = models.TimeField(help_text='Consultation end time')
    available_days = models.CharField(max_length=50, choices=DAY_CHOICES, default='Mon-Sat')
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    consultation_fee = models.DecimalField(max_digits=8, decimal_places=2, default=500)
    room_number = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='doctors/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['specialization', 'name']

    def __str__(self):
        return f"Dr. {self.name} ({self.get_specialization_display()}) — {self.hospital.name}"

    def timing_display(self):
        start = self.timing_start.strftime('%I:%M %p').lstrip('0')
        end = self.timing_end.strftime('%I:%M %p').lstrip('0')
        return f"{start} – {end}"


class PatientProfile(models.Model):
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    phone = models.CharField(max_length=20)
    date_of_birth = models.DateField(null=True, blank=True)
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES, blank=True)
    address = models.TextField(blank=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    allergies = models.TextField(blank=True)
    chronic_conditions = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.get_full_name() or self.user.username}"


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    TYPE_CHOICES = [
        ('emergency', 'Emergency'),
        ('consultation', 'Consultation'),
        ('follow_up', 'Follow-Up'),
        ('diagnostic', 'Diagnostic'),
    ]
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='appointments')
    appointment_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='consultation')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    scheduled_at = models.DateTimeField()
    reason = models.TextField()
    notes = models.TextField(blank=True)
    ambulance_required = models.BooleanField(default=False)
    relative_contact = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.patient.username} @ {self.hospital.name} [{self.get_status_display()}]"

    class Meta:
        ordering = ['-created_at']


class MedicalRecord(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='medical_records')
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='medical_records')
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, blank=True)
    diagnosis = models.TextField()
    prescription = models.TextField(blank=True)
    test_reports = models.TextField(blank=True)
    doctor_name = models.CharField(max_length=100)
    follow_up_date = models.DateField(null=True, blank=True)
    is_confidential = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Record: {self.patient.username} | {self.created_at.strftime('%d %b %Y')}"

    class Meta:
        ordering = ['-created_at']


class GovernmentHelpline(models.Model):
    name = models.CharField(max_length=200)
    number = models.CharField(max_length=20)
    description = models.TextField()
    icon = models.CharField(max_length=50, default='phone')
    category = models.CharField(max_length=50, default='emergency')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.number})"


class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    METHOD_CHOICES = [
        ('upi', 'UPI'),
        ('card', 'Card'),
        ('net_banking', 'Net Banking'),
        ('insurance', 'Insurance'),
        ('cash', 'Cash'),
    ]
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=20, choices=METHOD_CHOICES, default='upi')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment ₹{self.amount} [{self.get_status_display()}]"
