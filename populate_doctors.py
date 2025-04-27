from app import db
from app.models import Doctor


sample_doctors = [
    # General Practitioners (for general checkups)
    Doctor(name="Dr. Alice Harper", specialization="General Practitioner", experience=8, availability="MWF 8AM-12PM", rating=4.7),
    Doctor(name="Dr. Samuel Cole", specialization="General Practitioner", experience=12, availability="TThS 9AM-1PM", rating=4.8),
    Doctor(name="Dr. Fiona Grant", specialization="General Practitioner", experience=6, availability="MWF 1PM-5PM", rating=4.5),
    Doctor(name="Dr. Victor Patel", specialization="General Practitioner", experience=10, availability="TTh 2PM-6PM", rating=4.6),

    # Cardiologists
    Doctor(name="Dr. John Heartman", specialization="Cardiologist", experience=10, availability="MWF 9AM-1PM", rating=4.8),
    Doctor(name="Dr. Clara Veins", specialization="Cardiologist", experience=7, availability="TTh 2PM-6PM", rating=4.5),
    Doctor(name="Dr. Michael Arter", specialization="Cardiologist", experience=15, availability="MWF 2PM-5PM", rating=4.9),
    Doctor(name="Dr. Emma Pulse", specialization="Cardiologist", experience=4, availability="TThS 10AM-2PM", rating=4.3),

    # Pulmonologists
    Doctor(name="Dr. Steve Lungs", specialization="Pulmonologist", experience=9, availability="MWF 10AM-2PM", rating=4.6),
    Doctor(name="Dr. Rachel Breather", specialization="Pulmonologist", experience=6, availability="TThS 1PM-5PM", rating=4.4),
    Doctor(name="Dr. Alan Airway", specialization="Pulmonologist", experience=12, availability="MWF 8AM-12PM", rating=4.7),
    Doctor(name="Dr. Lily Breeze", specialization="Pulmonologist", experience=5, availability="TTh 3PM-7PM", rating=4.2),

    # Neurologists
    Doctor(name="Dr. Brainy Smith", specialization="Neurologist", experience=12, availability="MWF 11AM-3PM", rating=4.7),
    Doctor(name="Dr. Nerve Adams", specialization="Neurologist", experience=8, availability="TThS 9AM-1PM", rating=4.5),
    Doctor(name="Dr. Sophia Synapse", specialization="Neurologist", experience=14, availability="MWF 1PM-5PM", rating=4.8),
    Doctor(name="Dr. Ethan Neuron", specialization="Neurologist", experience=6, availability="TTh 10AM-3PM", rating=4.4),

    # Dermatologists
    Doctor(name="Dr. Skinna White", specialization="Dermatologist", experience=5, availability="MWF 2PM-6PM", rating=4.3),
    Doctor(name="Dr. Derma King", specialization="Dermatologist", experience=11, availability="TThS 10AM-2PM", rating=4.6),
    Doctor(name="Dr. Olivia Glow", specialization="Dermatologist", experience=9, availability="MWF 9AM-1PM", rating=4.5),
    Doctor(name="Dr. Lucas Derm", specialization="Dermatologist", experience=7, availability="TTh 1PM-5PM", rating=4.4),

    # Orthopedists
    Doctor(name="Dr. Jacob Bone", specialization="Orthopedist", experience=13, availability="MWF 10AM-3PM", rating=4.7),
    Doctor(name="Dr. Amelia Joint", specialization="Orthopedist", experience=8, availability="TThS 9AM-1PM", rating=4.5),
    Doctor(name="Dr. Thomas Spine", specialization="Orthopedist", experience=10, availability="MWF 1PM-5PM", rating=4.6),
    Doctor(name="Dr. Sarah Flex", specialization="Orthopedist", experience=6, availability="TTh 2PM-6PM", rating=4.3),

    # Pediatricians
    Doctor(name="Dr. Emily Childs", specialization="Pediatrician", experience=9, availability="MWF 8AM-12PM", rating=4.8),
    Doctor(name="Dr. David Kidd", specialization="Pediatrician", experience=12, availability="TThS 10AM-2PM", rating=4.7),
    Doctor(name="Dr. Mia Tots", specialization="Pediatrician", experience=5, availability="MWF 2PM-6PM", rating=4.4),
    Doctor(name="Dr. Noah Young", specialization="Pediatrician", experience=7, availability="TTh 1PM-5PM", rating=4.5),

    # Gastroenterologists
    Doctor(name="Dr. Henry Digest", specialization="Gastroenterologist", experience=11, availability="MWF 9AM-1PM", rating=4.6),
    Doctor(name="Dr. Grace Gut", specialization="Gastroenterologist", experience=8, availability="TThS 11AM-3PM", rating=4.4),
    Doctor(name="Dr. Oliver Tract", specialization="Gastroenterologist", experience=14, availability="MWF 1PM-5PM", rating=4.8),
    Doctor(name="Dr. Ava Colon", specialization="Gastroenterologist", experience=6, availability="TTh 10AM-2PM", rating=4.3),

    # Ophthalmologists
    Doctor(name="Dr. Clara Vision", specialization="Ophthalmologist", experience=10, availability="MWF 10AM-2PM", rating=4.7),
    Doctor(name="Dr. Liam Eyes", specialization="Ophthalmologist", experience=7, availability="TThS 9AM-1PM", rating=4.5),
    Doctor(name="Dr. Zoe Lens", specialization="Ophthalmologist", experience=12, availability="MWF 2PM-6PM", rating=4.8),
    Doctor(name="Dr. Isaac Sight", specialization="Ophthalmologist", experience=5, availability="TTh 1PM-5PM", rating=4.3),

    # Endocrinologists
    Doctor(name="Dr. Ella Hormone", specialization="Endocrinologist", experience=9, availability="MWF 9AM-1PM", rating=4.6),
    Doctor(name="Dr. Max Thyroid", specialization="Endocrinologist", experience=11, availability="TThS 10AM-2PM", rating=4.7),
    Doctor(name="Dr. Sophie Gland", specialization="Endocrinologist", experience=6, availability="MWF 1PM-5PM", rating=4.4),
    Doctor(name="Dr. Leo Balance", specialization="Endocrinologist", experience=8, availability="TTh 2PM-6PM", rating=4.5),

    # Psychiatrists
    Doctor(name="Dr. Hannah Mind", specialization="Psychiatrist", experience=12, availability="MWF 10AM-2PM", rating=4.8),
    Doctor(name="Dr. Owen Calm", specialization="Psychiatrist", experience=7, availability="TThS 9AM-1PM", rating=4.5),
    Doctor(name="Dr. Julia Mood", specialization="Psychiatrist", experience=10, availability="MWF 2PM-6PM", rating=4.7),
    Doctor(name="Dr. Ryan Peace", specialization="Psychiatrist", experience=5, availability="TTh 1PM-5PM", rating=4.3),

    # Internal Medicine Specialists
    Doctor(name="Dr. Laura Mendel", specialization="Internal Medicine", experience=14, availability="MWF 10AM-2PM", rating=4.9),
    Doctor(name="Dr. Robert Kline", specialization="Internal Medicine", experience=9, availability="TThS 11AM-3PM", rating=4.6),
    Doctor(name="Dr. Tara Singh", specialization="Internal Medicine", experience=7, availability="MWF 2PM-6PM", rating=4.5),

    # Oncologists
    Doctor(name="Dr. Nathan Cure", specialization="Oncologist", experience=15, availability="MWF 9AM-1PM", rating=4.9),
    Doctor(name="Dr. Chloe Hope", specialization="Oncologist", experience=10, availability="TThS 10AM-2PM", rating=4.7),
    Doctor(name="Dr. Daniel Ray", specialization="Oncologist", experience=8, availability="MWF 1PM-5PM", rating=4.6),

    # Urologists
    Doctor(name="Dr. Mark Stream", specialization="Urologist", experience=11, availability="MWF 10AM-2PM", rating=4.7),
    Doctor(name="Dr. Lisa Flow", specialization="Urologist", experience=7, availability="TThS 9AM-1PM", rating=4.5),
    Doctor(name="Dr. Paul Kidney", specialization="Urologist", experience=9, availability="MWF 2PM-6PM", rating=4.6),

    # Gynecologists
    Doctor(name="Dr. Rachel Bloom", specialization="Gynecologist", experience=12, availability="MWF 9AM-1PM", rating=4.8),
    Doctor(name="Dr. Susan Womb", specialization="Gynecologist", experience=8, availability="TThS 10AM-2PM", rating=4.6),
    Doctor(name="Dr. Karen Cycle", specialization="Gynecologist", experience=6, availability="MWF 1PM-5PM", rating=4.4),

    # ENT Specialists
    Doctor(name="Dr. Eric Sound", specialization="ENT Specialist", experience=10, availability="MWF 10AM-2PM", rating=4.7),
    Doctor(name="Dr. Nora Ear", specialization="ENT Specialist", experience=7, availability="TThS 9AM-1PM", rating=4.5),
    Doctor(name="Dr. Tom Throat", specialization="ENT Specialist", experience=9, availability="MWF 2PM-6PM", rating=4.6),

    # Top Heads (Department Chiefs)
    Doctor(name="Dr. Margaret Wells", specialization="Chief of General Medicine", experience=20, availability="MWF 9AM-12PM", rating=4.9),
    Doctor(name="Dr. Richard Holt", specialization="Chief of Cardiology", experience=22, availability="TTh 10AM-1PM", rating=5.0),
    Doctor(name="Dr. Evelyn Sage", specialization="Chief of Neurology", experience=18, availability="MWF 11AM-2PM", rating=4.9),
    Doctor(name="Dr. George Vance", specialization="Chief of Orthopedics", experience=19, availability="TThS 9AM-12PM", rating=4.8),
    Doctor(name="Dr. Patricia Dawn", specialization="Chief of Pediatrics", experience=17, availability="MWF 8AM-11AM", rating=4.9),
    Doctor(name="Dr. Steven Quill", specialization="Chief of Surgery", experience=21, availability="TTh 11AM-2PM", rating=5.0),
]

db.session.add_all(sample_doctors)
db.session.commit()
