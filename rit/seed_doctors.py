# -*- coding: utf-8 -*-
"""
Seed doctors for Hospital Smart Connect
Run: python -X utf8 seed_doctors.py
"""
import sys, os
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_smart_connect.settings')
import django
django.setup()

from core.models import Hospital, Doctor

doctors_data = [
    # Ruby Hall Clinic (pk=1)
    {
        'hospital': 'Ruby Hall Clinic',
        'doctors': [
            ('Rajesh Mehta',      'cardiology',     'MBBS, MD, DM (Cardiology)',        22, '09:00', '14:00', 'Mon-Sat', '+91 9800001001', 'OPD-C1', 800,  'available'),
            ('Sunita Rao',        'neurology',      'MBBS, MD, DM (Neurology)',          18, '10:00', '15:00', 'Mon-Fri', '+91 9800001002', 'OPD-N1', 700,  'available'),
            ('Ankit Shah',        'orthopedics',    'MBBS, MS (Ortho)',                  12, '08:30', '13:00', 'Mon-Sat', '+91 9800001003', 'OPD-O1', 600,  'busy'),
            ('Priya Nair',        'gynecology',     'MBBS, MS (OBG)',                    10, '09:00', '12:00', 'Mon,Wed,Fri', '+91 9800001004', 'OPD-G1', 500, 'available'),
            ('Vikram Desai',      'general',        'MBBS, MD (Gen Medicine)',           8,  '11:00', '17:00', 'Mon-Sat', '+91 9800001005', 'OPD-GM1', 400, 'available'),
        ]
    },
    # KEM Hospital (pk=2)
    {
        'hospital': 'KEM Hospital',
        'doctors': [
            ('Aisha Khan',        'emergency',      'MBBS, MD (Emergency Medicine)',     14, '00:00', '08:00', 'Mon-Sun', '+91 9800002001', 'ER-1',   300,  'available'),
            ('Suresh Patil',      'surgery',        'MBBS, MS, MCh (Surgery)',           20, '08:00', '14:00', 'Mon-Sat', '+91 9800002002', 'OT-3',   750,  'busy'),
            ('Deepak Joshi',      'pulmonology',    'MBBS, MD (Pulm)',                   9,  '10:00', '16:00', 'Mon-Fri', '+91 9800002003', 'OPD-P1', 550,  'available'),
            ('Meena Sharma',      'pediatrics',     'MBBS, MD (Pediatrics)',             11, '09:00', '13:00', 'Tue,Thu,Sat', '+91 9800002004', 'OPD-K1', 450, 'on_leave'),
        ]
    },
    # Jehangir Hospital (pk=3)
    {
        'hospital': 'Jehangir Hospital',
        'doctors': [
            ('Rahul Verma',       'oncology',       'MBBS, MD, DM (Oncology)',           16, '09:00', '15:00', 'Mon-Fri', '+91 9800003001', 'OPD-H1', 900,  'available'),
            ('Neha Gupta',        'dermatology',    'MBBS, MD (Dermatology)',             7,  '11:00', '17:00', 'Mon-Sat', '+91 9800003002', 'OPD-D1', 600,  'available'),
            ('Mohit Sinha',       'gastroenterology','MBBS, MD, DM (Gastro)',             13, '08:00', '13:00', 'Mon-Sat', '+91 9800003003', 'OPD-GI1',700,  'busy'),
            ('Kavita Iyer',       'ophthalmology',  'MBBS, MS (Ophthalmology)',           9,  '09:30', '13:30', 'Mon,Wed,Fri', '+91 9800003004', 'OPD-E1', 500, 'available'),
        ]
    },
    # Sahyadri Hospital (pk=4)
    {
        'hospital': 'Sahyadri Hospital',
        'doctors': [
            ('Ajay Kulkarni',     'nephrology',     'MBBS, MD, DM (Nephrology)',         17, '09:00', '14:00', 'Mon-Sat', '+91 9800004001', 'OPD-R1', 750,  'available'),
            ('Sonia Bhat',        'psychiatry',     'MBBS, MD (Psychiatry)',              8,  '10:00', '16:00', 'Mon-Fri', '+91 9800004002', 'OPD-PS1',550,  'available'),
            ('Rajan Pillai',      'radiology',      'MBBS, MD (Radiology)',               11, '08:00', '15:00', 'Mon-Sat', '+91 9800004003', 'RAD-1',  600,  'busy'),
        ]
    },
    # Deenanath Mangeshkar Hospital (pk=5)
    {
        'hospital': 'Deenanath Mangeshkar Hospital',
        'doctors': [
            ('Aarav Jain',        'cardiology',     'MBBS, MD, DM (Interventional Cardio)',25, '08:00', '13:00', 'Mon-Sat', '+91 9800005001', 'CATH-1', 1000, 'available'),
            ('Pooja Menon',       'gynecology',     'MBBS, MS, Fellowship (MIS)',         12, '09:00', '14:00', 'Mon,Wed,Fri', '+91 9800005002', 'OPD-G2', 600, 'available'),
            ('Krish Nambiar',     'urology',        'MBBS, MS, MCh (Urology)',            15, '10:00', '16:00', 'Mon-Fri', '+91 9800005003', 'OPD-U1', 700,  'off_duty'),
            ('Tanuja Hegde',      'ent',            'MBBS, MS (ENT)',                     6,  '09:30', '13:30', 'Mon-Sat', '+91 9800005004', 'OPD-ENT1',450, 'available'),
        ]
    },
    # Aditya Birla Memorial Hospital (pk=6)
    {
        'hospital': 'Aditya Birla Memorial Hospital',
        'doctors': [
            ('Sameer Rathod',     'cardiology',     'MBBS, MD, DM, FACC',               28, '08:00', '14:00', 'Mon-Sat', '+91 9800006001', 'CARD-1', 1200, 'available'),
            ('Lalita Pandey',     'neurology',      'MBBS, MD, PhD (Neurology)',         20, '09:00', '15:00', 'Mon-Fri', '+91 9800006002', 'NEURO-1',900,  'available'),
            ('Deepak Bhosale',    'anesthesiology', 'MBBS, MD (Anaesthesia)',             14, '07:00', '15:00', 'Mon-Sat', '+91 9800006003', 'OT-A1', 700,   'busy'),
            ('Rashmi Joglekar',   'orthopedics',    'MBBS, MS, Fellowship (Sports Med)',  10, '10:00', '16:00', 'Mon-Fri', '+91 9800006004', 'OPD-SP1',650,  'available'),
            ('Vivek Deshpande',   'general',        'MBBS, MD (Internal Medicine)',       5,  '12:00', '18:00', 'Mon-Sat', '+91 9800006005', 'OPD-IM1',400,  'available'),
        ]
    },
]

created_count = 0
for h_block in doctors_data:
    try:
        hospital = Hospital.objects.get(name=h_block['hospital'])
    except Hospital.DoesNotExist:
        print('Hospital not found: ' + h_block['hospital'])
        continue

    for (name, spec, qual, exp, t_start, t_end, days, phone, room, fee, status) in h_block['doctors']:
        doc, created = Doctor.objects.get_or_create(
            hospital=hospital,
            name=name,
            specialization=spec,
            defaults={
                'qualifications': qual,
                'experience_years': exp,
                'timing_start': t_start,
                'timing_end': t_end,
                'available_days': days,
                'phone': phone,
                'room_number': room,
                'consultation_fee': fee,
                'status': status,
            }
        )
        if created:
            created_count += 1
            print('[OK] Dr. ' + name + ' | ' + spec + ' | ' + hospital.name)
        else:
            print('[--] Exists: Dr. ' + name)

print()
print('Done! ' + str(created_count) + ' doctors added.')
print('View at: http://127.0.0.1:8000/hospitals/1/')
