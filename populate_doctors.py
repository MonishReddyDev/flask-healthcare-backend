from app import create_app, db
from app.models import Doctor
import json

app = create_app()

# Run within Flask context
with app.app_context():
    doctor1 = Doctor(
        name="Dr. John Smith",
        specialization="Cardiologist",
        experience=15,
        availability=json.dumps({"Mon": ["9:00-11:00", "14:00-16:00"], "Wed": ["10:00-12:00"]}),
        rating=4.8
    )

    doctor2 = Doctor(
        name="Dr. Emily Watson",
        specialization="Dermatologist",
        experience=8,
        availability=json.dumps({"Tue": ["13:00-16:00"], "Thu": ["9:00-11:30"]}),
        rating=4.5
    )

    doctor3 = Doctor(
        name="Dr. Robert Brown",
        specialization="Neurologist",
        experience=20,
        availability=json.dumps({"Fri": ["10:00-13:00"]}),
        rating=4.9
    )

    db.session.add_all([doctor1, doctor2, doctor3])
    db.session.commit()
    print("✅ Sample doctors added successfully!")
