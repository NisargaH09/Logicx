# -*- coding: utf-8 -*-
"""
Seed script for Hospital Smart Connect
Run: python seed_data.py
"""
import sys
import os

# Force UTF-8 output on Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_smart_connect.settings')

import django
django.setup()

from django.contrib.auth.models import User
from core.models import Hospital, Resource, Ambulance, GovernmentHelpline, PatientProfile

# --- Superuser ---
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@smartconnect.com', 'admin123')
    print('[OK] Superuser created: admin / admin123')
else:
    print('[--] Superuser already exists')

# --- Demo patient ---
if not User.objects.filter(username='patient').exists():
    patient = User.objects.create_user('patient', 'patient@example.com', 'patient123')
    patient.first_name = 'Raj'
    patient.last_name = 'Sharma'
    patient.save()
    PatientProfile.objects.create(
        user=patient,
        phone='+91 9876543210',
        blood_group='O+',
        emergency_contact_name='Priya Sharma',
        emergency_contact_phone='+91 9876543211',
        allergies='Penicillin',
        chronic_conditions='Hypertension',
    )
    print('[OK] Demo patient created: patient / patient123')
else:
    print('[--] Demo patient already exists')

# --- Hospitals ---
hospitals_data = [
    {
        'name': 'Ruby Hall Clinic', 'address': 'Sassoon Road', 'city': 'Pune',
        'phone': '020-66455555', 'emergency_contact': '020-66455000',
        'lat': 18.5314, 'lng': 73.8446,
        'beds': 300, 'avail_beds': 18, 'icu': 40, 'avail_icu': 5,
        'docs': 80, 'avail_docs': 12, 'vents': 8, 'ots': 6,
    },
    {
        'name': 'KEM Hospital', 'address': 'Rasta Peth', 'city': 'Pune',
        'phone': '020-26128000', 'emergency_contact': '020-26128999',
        'lat': 18.5166, 'lng': 73.8534,
        'beds': 450, 'avail_beds': 0, 'icu': 60, 'avail_icu': 0,
        'docs': 120, 'avail_docs': 8, 'vents': 10, 'ots': 8,
    },
    {
        'name': 'Jehangir Hospital', 'address': 'Sassoon Road', 'city': 'Pune',
        'phone': '020-66814444', 'emergency_contact': '020-66814000',
        'lat': 18.5298, 'lng': 73.8741,
        'beds': 280, 'avail_beds': 34, 'icu': 35, 'avail_icu': 8,
        'docs': 70, 'avail_docs': 20, 'vents': 6, 'ots': 5,
    },
    {
        'name': 'Sahyadri Hospital', 'address': 'Karve Road', 'city': 'Pune',
        'phone': '020-67210000', 'emergency_contact': '020-67210999',
        'lat': 18.5036, 'lng': 73.8343,
        'beds': 200, 'avail_beds': 7, 'icu': 25, 'avail_icu': 1,
        'docs': 55, 'avail_docs': 6, 'vents': 3, 'ots': 4,
    },
    {
        'name': 'Deenanath Mangeshkar Hospital', 'address': 'Erandwane', 'city': 'Pune',
        'phone': '020-49150000', 'emergency_contact': '020-49150999',
        'lat': 18.5089, 'lng': 73.8261,
        'beds': 360, 'avail_beds': 22, 'icu': 50, 'avail_icu': 11,
        'docs': 95, 'avail_docs': 18, 'vents': 9, 'ots': 7,
    },
    {
        'name': 'Aditya Birla Memorial Hospital', 'address': 'Chinchwad', 'city': 'Pune',
        'phone': '020-30710000', 'emergency_contact': '020-30710911',
        'lat': 18.6476, 'lng': 73.7756,
        'beds': 500, 'avail_beds': 45, 'icu': 70, 'avail_icu': 14,
        'docs': 130, 'avail_docs': 25, 'vents': 15, 'ots': 10,
    },
]

hospital_objects = []
for h_data in hospitals_data:
    h, created = Hospital.objects.get_or_create(name=h_data['name'], defaults={
        'address': h_data['address'],
        'city': h_data['city'],
        'phone': h_data['phone'],
        'emergency_contact': h_data['emergency_contact'],
        'latitude': h_data['lat'],
        'longitude': h_data['lng'],
    })
    hospital_objects.append(h)
    if created:
        Resource.objects.create(
            hospital=h,
            total_beds=h_data['beds'],
            available_beds=h_data['avail_beds'],
            total_icu=h_data['icu'],
            available_icu=h_data['avail_icu'],
            total_doctors=h_data['docs'],
            available_doctors=h_data['avail_docs'],
            ventilators_available=h_data['vents'],
            operation_theaters=h_data['ots'],
        )
        print('[OK] Hospital: ' + h.name)
    else:
        print('[--] Hospital exists: ' + h.name)

# --- Ambulances ---
ambulances_data = [
    ('MH-12-AB-3421', 'Suresh Kumar', '+91 9876501234', 'advanced', 18.5314, 73.8446, 'available', 0),
    ('MH-12-CD-5678', 'Ravi Patil',   '+91 9876502345', 'basic',    18.5200, 73.8567, 'available', 0),
    ('MH-12-EF-9012', 'Mohan Das',    '+91 9876503456', 'advanced', 18.5380, 73.8720, 'dispatched', 8),
    ('MH-12-GH-3456', 'Prakash Rao',  '+91 9876504567', 'neonatal', 18.5050, 73.8300, 'en_route',   4),
    ('MH-12-IJ-7890', 'Sanjay Mehta', '+91 9876505678', 'advanced', 18.6476, 73.7756, 'available', 0),
    ('MH-12-KL-2345', 'Anil Yadav',   '+91 9876506789', 'basic',    18.5089, 73.8261, 'available', 0),
    ('MH-12-MN-6789', 'Ramesh Nair',  '+91 9876507890', 'advanced', 18.5298, 73.8741, 'at_hospital', 0),
]

for i, (vnum, driver, phone, atype, lat, lng, status, eta) in enumerate(ambulances_data):
    amb, created = Ambulance.objects.get_or_create(vehicle_number=vnum, defaults={
        'driver_name': driver,
        'driver_phone': phone,
        'ambulance_type': atype,
        'hospital': hospital_objects[i % len(hospital_objects)],
        'status': status,
        'current_latitude': lat,
        'current_longitude': lng,
        'eta_minutes': eta,
    })
    if created:
        print('[OK] Ambulance: ' + vnum)
    else:
        print('[--] Ambulance exists: ' + vnum)

# --- Government Helplines ---
helplines_data = [
    ('ambulance',  'Ambulance Emergency',  '108',          'Call for ambulance dispatch across India', 'emergency'),
    ('emergency',  'National Emergency',   '112',          'Single emergency number for all services', 'emergency'),
    ('police',     'Police',               '100',          'Law enforcement and security emergency',   'police'),
    ('fire',       'Fire Brigade',         '101',          'Fire and rescue operations',               'fire'),
    ('medical',    'Medical Helpline',     '104',          'Non-emergency medical advice',             'medical'),
    ('covid',      'COVID-19 Helpline',    '1075',         'Ministry of Health COVID-19 helpline',     'medical'),
    ('senior',     'Senior Citizen',       '14567',        'Elder care helpline (Elder Line)',          'social'),
    ('pmjay',      'Ayushman Bharat',      '1800-111-565', 'PMJAY insurance helpline',                 'insurance'),
]

for icon, name, number, desc, cat in helplines_data:
    hl, created = GovernmentHelpline.objects.get_or_create(number=number, defaults={
        'name': name, 'icon': icon, 'description': desc, 'category': cat
    })
    if created:
        print('[OK] Helpline: ' + name + ' (' + number + ')')
    else:
        print('[--] Helpline exists: ' + name)

print()
print('Seed complete!')
print('Admin login: http://127.0.0.1:8000/admin/ | admin / admin123')
print('Patient login: patient / patient123')
