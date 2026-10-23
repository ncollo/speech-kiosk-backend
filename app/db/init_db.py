import json
import logging
from app.db.session import engine, SessionLocal, Base
from app.db.models import HospitalUser, TriagePatient, KioskTerminal, AuditLog

logger = logging.getLogger("clearcaption.init_db")

SEED_USERS = [
    {"id": "USR-01", "name": "Dr. Geoffrey Mutiso", "role": "Hospital Administrator", "department": "Executive Medical Operations", "email": "g.mutiso@knh.or.ke", "phone": "+254 711 001 001", "status": "Active", "last_login": "10 mins ago", "badge_id": "ADMIN-001", "pin": "9900"},
    {"id": "USR-02", "name": "Sarah Wambui", "role": "Hospital Administrator", "department": "Health Information & Systems", "email": "s.wambui@knh.or.ke", "phone": "+254 711 001 002", "status": "Active", "last_login": "25 mins ago", "badge_id": "ADMIN-002", "pin": "9900"},
    {"id": "USR-03", "name": "David Kiprono", "role": "Hospital Administrator", "department": "Clinical Quality & Accessibility", "email": "d.kiprono@knh.or.ke", "phone": "+254 711 001 003", "status": "On-Duty", "last_login": "1 hour ago", "badge_id": "ADMIN-003", "pin": "9900"},
    {"id": "USR-04", "name": "Nurse Joyce Mwangi", "role": "Triage Nurse", "department": "Desk 3 · Outpatient Reception", "email": "j.mwangi@knh.or.ke", "phone": "+254 722 002 001", "status": "On-Duty", "last_login": "Active now", "badge_id": "NURSE-4029", "pin": "4821"},
    {"id": "USR-05", "name": "Nurse Beatrice Akinyi", "role": "Triage Nurse", "department": "Desk 1 · Emergency Triage", "email": "b.akinyi@knh.or.ke", "phone": "+254 722 002 002", "status": "On-Duty", "last_login": "12 mins ago", "badge_id": "NURSE-4030", "pin": "4821"},
    {"id": "USR-06", "name": "Nurse Grace Njeri", "role": "Triage Nurse", "department": "Desk 2 · Pediatric Reception", "email": "g.njeri@knh.or.ke", "phone": "+254 722 002 003", "status": "On-Duty", "last_login": "30 mins ago", "badge_id": "NURSE-4031", "pin": "4821"},
    {"id": "USR-07", "name": "Nurse Mercy Korir", "role": "Triage Nurse", "department": "Desk 4 · Specialized Clinics", "email": "m.korir@knh.or.ke", "phone": "+254 722 002 004", "status": "Break", "last_login": "2 hours ago", "badge_id": "NURSE-4032", "pin": "4821"},
    {"id": "USR-08", "name": "Nurse Agnes Wanjiku", "role": "Triage Nurse", "department": "Desk 3 · Outpatient Reception", "email": "a.wanjiku@knh.or.ke", "phone": "+254 722 002 005", "status": "Active", "last_login": "45 mins ago", "badge_id": "NURSE-4033", "pin": "4821"},
    {"id": "USR-09", "name": "Nurse Esther Moraa", "role": "Triage Nurse", "department": "Desk 5 · Maternity Reception", "email": "e.moraa@knh.or.ke", "phone": "+254 722 002 006", "status": "On-Duty", "last_login": "15 mins ago", "badge_id": "NURSE-4034", "pin": "4821"},
    {"id": "USR-10", "name": "Nurse Lilian Chepkemoi", "role": "Triage Nurse", "department": "Desk 6 · Surgical Outpatient", "email": "l.chepkemoi@knh.or.ke", "phone": "+254 722 002 007", "status": "Offline", "last_login": "Yesterday", "badge_id": "NURSE-4035", "pin": "4821"},
    {"id": "USR-11", "name": "Nurse Catherine Nduta", "role": "Triage Nurse", "department": "Emergency Rapid Response", "email": "c.nduta@knh.or.ke", "phone": "+254 722 002 008", "status": "On-Duty", "last_login": "5 mins ago", "badge_id": "NURSE-4036", "pin": "4821"},
    {"id": "USR-12", "name": "Kevin Otieno", "role": "Reception Officer", "department": "Desk 1 · Emergency Front Counter", "email": "k.otieno@knh.or.ke", "phone": "+254 733 003 001", "status": "On-Duty", "last_login": "Active now", "badge_id": "RECEP-101", "pin": "1234"},
    {"id": "USR-13", "name": "Maryanne Achieng", "role": "Reception Officer", "department": "Desk 3 · Main Outpatient Lobby", "email": "m.achieng@knh.or.ke", "phone": "+254 733 003 002", "status": "On-Duty", "last_login": "3 mins ago", "badge_id": "RECEP-102", "pin": "1234"},
    {"id": "USR-14", "name": "Samuel Kilonzo", "role": "Reception Officer", "department": "Desk 2 · Pediatric Registration", "email": "s.kilonzo@knh.or.ke", "phone": "+254 733 003 003", "status": "Active", "last_login": "18 mins ago", "badge_id": "RECEP-103", "pin": "1234"},
    {"id": "USR-15", "name": "Brenda Mutheu", "role": "Reception Officer", "department": "Desk 4 · ENT & Specialized Desk", "email": "b.mutheu@knh.or.ke", "phone": "+254 733 003 004", "status": "On-Duty", "last_login": "22 mins ago", "badge_id": "RECEP-104", "pin": "1234"},
    {"id": "USR-16", "name": "Collins Nderitu", "role": "Reception Officer", "department": "Desk 5 · Maternity Wing Desk", "email": "c.nderitu@knh.or.ke", "phone": "+254 733 003 005", "status": "Break", "last_login": "1 hour ago", "badge_id": "RECEP-105", "pin": "1234"},
    {"id": "USR-17", "name": "Halima Abdi", "role": "Reception Officer", "department": "Desk 6 · Imaging & Lab Front Counter", "email": "h.abdi@knh.or.ke", "phone": "+254 733 003 006", "status": "Offline", "last_login": "Yesterday", "badge_id": "RECEP-106", "pin": "1234"},
    {"id": "USR-18", "name": "Dr. Patrick Kariuki", "role": "Medical Doctor", "department": "Consultation Room 1 · General Medicine", "email": "p.kariuki@knh.or.ke", "phone": "+254 744 004 001", "status": "On-Duty", "last_login": "20 mins ago", "badge_id": "DOC-201", "pin": "1234"},
    {"id": "USR-19", "name": "Dr. Amina Hassan", "role": "Medical Doctor", "department": "Consultation Room 2 · Urgent Care", "email": "a.hassan@knh.or.ke", "phone": "+254 744 004 002", "status": "On-Duty", "last_login": "8 mins ago", "badge_id": "DOC-202", "pin": "1234"},
    {"id": "USR-20", "name": "Dr. Kennedy Omondi", "role": "Medical Doctor", "department": "Cardiology & Chest Clinic", "email": "k.omondi@knh.or.ke", "phone": "+254 744 004 003", "status": "Active", "last_login": "1 hour ago", "badge_id": "DOC-203", "pin": "1234"},
    {"id": "USR-21", "name": "Dr. Jane Muthoni", "role": "Medical Doctor", "department": "Pediatric Medical Officer", "email": "j.muthoni@knh.or.ke", "phone": "+254 744 004 004", "status": "On-Duty", "last_login": "35 mins ago", "badge_id": "DOC-204", "pin": "1234"},
    {"id": "USR-22", "name": "Dr. Victor Koech", "role": "Medical Doctor", "department": "Emergency Medicine Registrar", "email": "v.koech@knh.or.ke", "phone": "+254 744 004 005", "status": "On-Duty", "last_login": "14 mins ago", "badge_id": "DOC-205", "pin": "1234"},
    {"id": "USR-23", "name": "Dr. Rose Nyambura", "role": "Medical Doctor", "department": "Obstetrics & Gynaecology", "email": "r.nyambura@knh.or.ke", "phone": "+254 744 004 006", "status": "Break", "last_login": "3 hours ago", "badge_id": "DOC-206", "pin": "1234"},
    {"id": "USR-24", "name": "George Wafula", "role": "KSL Interpreter", "department": "Hospital Deaf Inclusion & KSL Unit", "email": "g.wafula@knh.or.ke", "phone": "+254 755 005 001", "status": "On-Duty", "last_login": "Active now", "badge_id": "KSL-301", "pin": "1234"},
    {"id": "USR-25", "name": "Susan Makena", "role": "KSL Interpreter", "department": "Hospital Deaf Inclusion & KSL Unit", "email": "s.makena@knh.or.ke", "phone": "+254 755 005 002", "status": "On-Duty", "last_login": "6 mins ago", "badge_id": "KSL-302", "pin": "1234"},
    {"id": "USR-26", "name": "Dennis Kipchumba", "role": "KSL Interpreter", "department": "Emergency On-Call KSL Network", "email": "d.kipchumba@knh.or.ke", "phone": "+254 755 005 003", "status": "Active", "last_login": "40 mins ago", "badge_id": "KSL-303", "pin": "1234"},
    {"id": "USR-27", "name": "Pauline Adhiambo", "role": "KSL Interpreter", "department": "Hospital Deaf Inclusion & KSL Unit", "email": "p.adhiambo@knh.or.ke", "phone": "+254 755 005 004", "status": "Offline", "last_login": "Yesterday", "badge_id": "KSL-304", "pin": "1234"},
    {"id": "USR-28", "name": "Dr. Evans Muli", "role": "Audiology Specialist", "department": "Audiology & Speech Sciences", "email": "e.muli@knh.or.ke", "phone": "+254 766 006 001", "status": "Active", "last_login": "50 mins ago", "badge_id": "SPEC-501", "pin": "1234"},
    {"id": "USR-29", "name": "Rachel Jerop", "role": "Audiology Specialist", "department": "Assistive Communication Lab", "email": "r.jerop@knh.or.ke", "phone": "+254 766 006 002", "status": "On-Duty", "last_login": "2 hours ago", "badge_id": "SPEC-502", "pin": "1234"},
    {"id": "USR-30", "name": "Anthony Musyoka", "role": "Audiology Specialist", "department": "ENT Diagnostic Center", "email": "a.musyoka@knh.or.ke", "phone": "+254 766 006 003", "status": "Offline", "last_login": "2 days ago", "badge_id": "SPEC-503", "pin": "1234"}
]

SEED_PATIENTS = [
    {"id": "PT-1042", "name": "Wanjiru Karanja", "symptom": "Chest Pain", "symptom_sw": "Maumivu ya Kifua", "places": json.dumps(["Chest, left", "Throat"]), "duration": "Since this morning", "urgent": True, "time": "2 mins ago", "desk": "Desk 3", "lang": "Kiswahili & KSL", "status": "Waiting"},
    {"id": "PT-1041", "name": "Brian Omondi", "symptom": "Fever or Chills", "symptom_sw": "Homa", "places": json.dumps(["Head"]), "duration": "A few days", "urgent": False, "time": "14 mins ago", "desk": "Desk 2", "lang": "English", "status": "In Triage"},
    {"id": "PT-1040", "name": "Faith Chebet", "symptom": "Abdominal Pain", "symptom_sw": "Maumivu ya Tumbo", "places": json.dumps(["Stomach"]), "duration": "More than a week", "urgent": False, "time": "28 mins ago", "desk": "Desk 3", "lang": "Kiswahili", "status": "With Doctor"},
    {"id": "PT-1039", "name": "Samuel Githinji", "symptom": "Shortness of Breath", "symptom_sw": "Pumzi Fupi", "places": json.dumps(["Chest, right"]), "duration": "Less than an hour", "urgent": True, "time": "35 mins ago", "desk": "Desk 1", "lang": "Kiswahili & KSL", "status": "With Doctor"},
    {"id": "PT-1038", "name": "Amina Mohamed", "symptom": "Dizziness", "symptom_sw": "Kizunguzungu", "places": json.dumps(["Head"]), "duration": "Since this morning", "urgent": False, "time": "42 mins ago", "desk": "Desk 3", "lang": "English", "status": "Completed"},
    {"id": "PT-1037", "name": "Kelvin Mutua", "symptom": "Headache", "symptom_sw": "Kuumwa na Kichwa", "places": json.dumps(["Head"]), "duration": "A few days", "urgent": False, "time": "50 mins ago", "desk": "Desk 4", "lang": "Kiswahili", "status": "Completed"},
    {"id": "PT-1036", "name": "Mercy Atieno", "symptom": "Swelling", "symptom_sw": "Kuvimba Mwili", "places": json.dumps(["Right leg", "Left leg"]), "duration": "More than a week", "urgent": False, "time": "1 hour ago", "desk": "Desk 2", "lang": "KSL Assisted", "status": "Completed"},
    {"id": "PT-1035", "name": "John Kamau", "symptom": "Nausea or Vomiting", "symptom_sw": "Kichefuchefu", "places": json.dumps(["Stomach"]), "duration": "Since this morning", "urgent": False, "time": "1 hour ago", "desk": "Desk 3", "lang": "English", "status": "Completed"},
    {"id": "PT-1034", "name": "Dorcas Wanjala", "symptom": "Fatigue", "symptom_sw": "Uchovu Mkubwa", "places": json.dumps(["Head", "Lower belly"]), "duration": "More than a week", "urgent": False, "time": "1.5 hours ago", "desk": "Desk 5", "lang": "Kiswahili", "status": "Completed"},
    {"id": "PT-1033", "name": "Geoffrey Rotich", "symptom": "Chest Pain", "symptom_sw": "Maumivu ya Kifua", "places": json.dumps(["Chest, left"]), "duration": "Less than an hour", "urgent": True, "time": "2 hours ago", "desk": "Desk 1", "lang": "English", "status": "Completed"},
    {"id": "PT-1032", "name": "Lydia Nyaboke", "symptom": "Fever or Chills", "symptom_sw": "Homa", "places": json.dumps(["Head"]), "duration": "A few days", "urgent": False, "time": "2 hours ago", "desk": "Desk 2", "lang": "Kiswahili & KSL", "status": "Completed"},
    {"id": "PT-1031", "name": "Erick Odhiambo", "symptom": "Abdominal Pain", "symptom_sw": "Maumivu ya Tumbo", "places": json.dumps(["Lower belly"]), "duration": "A few days", "urgent": False, "time": "2.5 hours ago", "desk": "Desk 3", "lang": "English", "status": "Completed"},
    {"id": "PT-1030", "name": "Priscilla Mutindi", "symptom": "Other Concern", "symptom_sw": "Shida Nyingine", "places": json.dumps(["Right arm"]), "duration": "Since this morning", "urgent": False, "time": "3 hours ago", "desk": "Desk 6", "lang": "Kiswahili", "status": "Completed"},
    {"id": "PT-1029", "name": "Paul Kiptoo", "symptom": "Shortness of Breath", "symptom_sw": "Pumzi Fupi", "places": json.dumps(["Chest, right"]), "duration": "Less than an hour", "urgent": True, "time": "3 hours ago", "desk": "Desk 1", "lang": "KSL Assisted", "status": "Completed"},
    {"id": "PT-1028", "name": "Grace Makau", "symptom": "Dizziness", "symptom_sw": "Kizunguzungu", "places": json.dumps(["Head"]), "duration": "Since this morning", "urgent": False, "time": "3.5 hours ago", "desk": "Desk 4", "lang": "Kiswahili", "status": "Completed"},
    {"id": "PT-1027", "name": "Victor Wanyama", "symptom": "Headache", "symptom_sw": "Kuumwa na Kichwa", "places": json.dumps(["Head"]), "duration": "A few days", "urgent": False, "time": "4 hours ago", "desk": "Desk 2", "lang": "English", "status": "Completed"},
    {"id": "PT-1026", "name": "Eunice Cherono", "symptom": "Swelling", "symptom_sw": "Kuvimba Mwili", "places": json.dumps(["Left arm"]), "duration": "More than a week", "urgent": False, "time": "4 hours ago", "desk": "Desk 3", "lang": "Kiswahili", "status": "Completed"},
    {"id": "PT-1025", "name": "Bernard Maina", "symptom": "Chest Pain", "symptom_sw": "Maumivu ya Kifua", "places": json.dumps(["Chest, right"]), "duration": "Since this morning", "urgent": True, "time": "4.5 hours ago", "desk": "Desk 1", "lang": "English", "status": "Completed"},
    {"id": "PT-1024", "name": "Judith Auma", "symptom": "Fever or Chills", "symptom_sw": "Homa", "places": json.dumps(["Head"]), "duration": "A few days", "urgent": False, "time": "5 hours ago", "desk": "Desk 2", "lang": "Kiswahili & KSL", "status": "Completed"},
    {"id": "PT-1023", "name": "Dennis Gitau", "symptom": "Abdominal Pain", "symptom_sw": "Maumivu ya Tumbo", "places": json.dumps(["Stomach"]), "duration": "Since this morning", "urgent": False, "time": "5.5 hours ago", "desk": "Desk 3", "lang": "Kiswahili", "status": "Completed"},
    {"id": "PT-1022", "name": "Sharon Chepkirui", "symptom": "Nausea or Vomiting", "symptom_sw": "Kichefuchefu", "places": json.dumps(["Stomach"]), "duration": "Less than an hour", "urgent": False, "time": "6 hours ago", "desk": "Desk 5", "lang": "English", "status": "Completed"},
    {"id": "PT-1021", "name": "Moses Mwangi", "symptom": "Shortness of Breath", "symptom_sw": "Pumzi Fupi", "places": json.dumps(["Throat"]), "duration": "Less than an hour", "urgent": True, "time": "6 hours ago", "desk": "Desk 1", "lang": "KSL Assisted", "status": "Completed"},
    {"id": "PT-1020", "name": "Esther Nekesa", "symptom": "Headache", "symptom_sw": "Kuumwa na Kichwa", "places": json.dumps(["Head"]), "duration": "More than a week", "urgent": False, "time": "6.5 hours ago", "desk": "Desk 4", "lang": "Kiswahili", "status": "Completed"},
    {"id": "PT-1019", "name": "Stephen Ndung’u", "symptom": "Other Concern", "symptom_sw": "Shida Nyingine", "places": json.dumps(["Left leg"]), "duration": "A few days", "urgent": False, "time": "7 hours ago", "desk": "Desk 6", "lang": "English", "status": "Completed"},
    {"id": "PT-1018", "name": "Caroline Moraa", "symptom": "Dizziness", "symptom_sw": "Kizunguzungu", "places": json.dumps(["Head"]), "duration": "Since this morning", "urgent": False, "time": "7.5 hours ago", "desk": "Desk 3", "lang": "Kiswahili & KSL", "status": "Completed"},
    {"id": "PT-1017", "name": "Martin Musyoka", "symptom": "Chest Pain", "symptom_sw": "Maumivu ya Kifua", "places": json.dumps(["Chest, left"]), "duration": "Less than an hour", "urgent": True, "time": "8 hours ago", "desk": "Desk 1", "lang": "English", "status": "Completed"},
    {"id": "PT-1016", "name": "Ann Wambui", "symptom": "Fever or Chills", "symptom_sw": "Homa", "places": json.dumps(["Head"]), "duration": "A few days", "urgent": False, "time": "8.5 hours ago", "desk": "Desk 2", "lang": "Kiswahili", "status": "Completed"},
    {"id": "PT-1015", "name": "Isaac Kipchoge", "symptom": "Swelling", "symptom_sw": "Kuvimba Mwili", "places": json.dumps(["Right arm"]), "duration": "More than a week", "urgent": False, "time": "9 hours ago", "desk": "Desk 3", "lang": "English", "status": "Completed"},
    {"id": "PT-1014", "name": "Purity Wairimu", "symptom": "Fatigue", "symptom_sw": "Uchovu Mkubwa", "places": json.dumps(["Head"]), "duration": "More than a week", "urgent": False, "time": "9.5 hours ago", "desk": "Desk 5", "lang": "Kiswahili", "status": "Completed"},
    {"id": "PT-1013", "name": "Collins Kibet", "symptom": "Chest Pain", "symptom_sw": "Maumivu ya Kifua", "places": json.dumps(["Chest, right"]), "duration": "Since this morning", "urgent": True, "time": "10 hours ago", "desk": "Desk 1", "lang": "English", "status": "Completed"}
]

SEED_TERMINALS = [
    {"id": "TERM-01", "desk_number": "Desk 1", "facility": "St. Mary's Medical Center", "device_type": "Surface Pro 9 Kiosk Mount", "latency_ms": 174, "status": "Online"},
    {"id": "TERM-02", "desk_number": "Desk 2", "facility": "St. Mary's Medical Center", "device_type": "Dell 24 Touchscreen Terminal", "latency_ms": 192, "status": "Online"},
    {"id": "TERM-03", "desk_number": "Desk 3", "facility": "St. Mary's Medical Center", "device_type": "iPad Pro 12.9 Countertop", "latency_ms": 165, "status": "Active Session"},
    {"id": "TERM-04", "desk_number": "Desk 4", "facility": "St. Mary's Medical Center", "device_type": "Surface Pro 9 Kiosk Mount", "latency_ms": 204, "status": "Online"},
    {"id": "TERM-05", "desk_number": "Desk 5", "facility": "St. Mary's Medical Center", "device_type": "Dell 24 Touchscreen Terminal", "latency_ms": 188, "status": "Online"},
    {"id": "TERM-06", "desk_number": "Desk 6", "facility": "St. Mary's Medical Center", "device_type": "HP Engage One Pro", "latency_ms": 215, "status": "Maintenance"}
]

SEED_AUDIT_LOGS = [
    {"event_type": "EPHEMERAL_WIPE_VERIFIED", "staff_id": "USR-04", "terminal_id": "TERM-03", "details": "Desk 3 session #SESS-9021 ended. RAM caption buffers and temp audio cache purged (0 bytes retained).", "dpa_compliant": True},
    {"event_type": "KSL_ASSIST_INVOKED", "staff_id": "USR-24", "terminal_id": "TERM-01", "details": "Certified KSL video prompt chest-pain-ksl.mp4 dispatched to patient at Desk 1.", "dpa_compliant": True},
    {"event_type": "ADMIN_CREDENTIAL_VERIFIED", "staff_id": "USR-01", "terminal_id": None, "details": "Hospital Administrator Dr. Geoffrey Mutiso unlocked Administrative Suite console.", "dpa_compliant": True},
    {"event_type": "TRIAGE_ESCALATION", "staff_id": "USR-05", "terminal_id": "TERM-01", "details": "Urgent chest pain intake escalated to Consultation Room 2 (Dr. Amina Hassan).", "dpa_compliant": True}
]

def init_database():
    """Create tables and seed initial records if empty."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(HospitalUser).count() == 0:
            logger.info("Seeding 30 hospital system staff members...")
            for user_data in SEED_USERS:
                db.add(HospitalUser(**user_data))
            db.commit()

        if db.query(TriagePatient).count() == 0:
            logger.info("Seeding 30 patient triage records...")
            for patient_data in SEED_PATIENTS:
                db.add(TriagePatient(**patient_data))
            db.commit()

        if db.query(KioskTerminal).count() == 0:
            logger.info("Seeding 6 kiosk terminals...")
            for term_data in SEED_TERMINALS:
                db.add(KioskTerminal(**term_data))
            db.commit()

        if db.query(AuditLog).count() == 0:
            logger.info("Seeding initial DPA compliance audit logs...")
            for audit_data in SEED_AUDIT_LOGS:
                db.add(AuditLog(**audit_data))
            db.commit()

        logger.info("Database initialization and seeding completed successfully.")
    except Exception as e:
        db.rollback()
        logger.error(f"Error initializing database: {e}")
        raise
    finally:
        db.close()
