# insert_candidates.py

import os
import django
import random
from faker import Faker

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ats_project.settings")
django.setup()

from candidates.models import Candidate

fake = Faker()

GENDERS = ['M', 'F', 'O']

def create_candidate():
    return Candidate(
        name=fake.name(),
        age=random.randint(20, 60),
        gender=random.choice(GENDERS),
        email=fake.unique.email(),
        phone_number=fake.unique.phone_number()
    )

def bulk_insert_candidates(n=100):
    candidates = [create_candidate() for _ in range(n)]
    Candidate.objects.bulk_create(candidates)
    print(f"✅ Inserted {n} fake candidates.")

if __name__ == "__main__":
    bulk_insert_candidates(100)
