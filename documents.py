"""
01_documents.py"""

DOCUMENTS = [
    {
        "document_id": "doc_01",
        "title": "Campus Printing Costs and Payment Methods",
        "category": "Services",
        "status": "CURRENT",
        "effective_date": "2024-09-01",
        "text": "Campus printing costs are updated for the academic year. Black-and-white printing is 5 cents per page, and color printing is 15 cents per page. Students can pay using their campus smart card or online student balance."
    },
    {
        "document_id": "doc_02",
        "title": "Legacy Printing Prices Policy",
        "category": "Services",
        "status": "OUTDATED",
        "effective_date": "2022-01-01",
        "text": "Campus printing costs are 10 cents for black-and-white pages and 25 cents for color pages. Payment is cash only at the central library desk."
    },
    {
        "document_id": "doc_03",
        "title": "Main Library Operating Hours",
        "category": "Facilities",
        "status": "CURRENT",
        "effective_date": "2024-08-15",
        "text": "The university library is open Monday through Thursday from 8:00 AM to 10:00 PM. On Fridays, the library operates from 8:00 AM to 6:00 PM, and on weekends it opens from 10:00 AM to 4:00 PM for quiet study."
    },
    {
        "document_id": "doc_04",
        "title": "Student Parking Permits and Garage Access",
        "category": "Transportation",
        "status": "CURRENT",
        "effective_date": "2024-07-01",
        "text": "Semester parking permits cost 150 dollars for commuter students. Vehicles must be registered online through the university transportation portal, and permits grant access to parking lots A, B, and the north parking garage."
    },
    {
        "document_id": "doc_05",
        "title": "Academic Advising and Course Registration",
        "category": "Academics",
        "status": "CURRENT",
        "effective_date": "2024-08-01",
        "text": "Undergraduate students must meet with their academic advisor before enrolling in classes. Course registration opens four weeks prior to the semester start date, and registration holds must be cleared with the registrar office."
    },
    {
        "document_id": "doc_06",
        "title": "Campus Health Clinic and Vaccinations",
        "category": "Health",
        "status": "CURRENT",
        "effective_date": "2024-06-15",
        "text": "The campus medical clinic provides routine primary care, emergency first aid, and annual flu vaccinations for enrolled students. Consultations are free of charge, but specialized lab tests may require health insurance co-pay."
    }
]

def load_documents():
    return DOCUMENTS