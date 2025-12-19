import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gymapp.settings')
django.setup()

from gym.models import Member, GymClass
from datetime import time

print("Creating sample gym classes...")

classes_data = [
    {
        'name': 'Yoga Basics',
        'description': 'Perfect for beginners. Learn fundamental yoga poses and breathing techniques.',
        'instructor': 'Sarah Johnson',
        'day_of_week': 0,
        'start_time': time(9, 0),
        'duration_minutes': 60,
        'capacity': 15
    },
    {
        'name': 'HIIT Workout',
        'description': 'High-intensity interval training for maximum calorie burn and fitness gains.',
        'instructor': 'Mike Davis',
        'day_of_week': 1,
        'start_time': time(18, 0),
        'duration_minutes': 45,
        'capacity': 20
    },
    {
        'name': 'Spin Class',
        'description': 'Intense cycling workout with energizing music. Bring water and towel.',
        'instructor': 'Lisa Chen',
        'day_of_week': 2,
        'start_time': time(7, 0),
        'duration_minutes': 50,
        'capacity': 25
    },
    {
        'name': 'Strength Training',
        'description': 'Build muscle and increase strength with weight training exercises.',
        'instructor': 'Tom Rodriguez',
        'day_of_week': 3,
        'start_time': time(17, 30),
        'duration_minutes': 60,
        'capacity': 18
    },
    {
        'name': 'Pilates',
        'description': 'Core-focused workout improving flexibility, balance, and muscle tone.',
        'instructor': 'Emma Wilson',
        'day_of_week': 4,
        'start_time': time(10, 0),
        'duration_minutes': 55,
        'capacity': 12
    },
    {
        'name': 'Zumba Dance',
        'description': 'Fun dance fitness party with Latin-inspired music and moves.',
        'instructor': 'Maria Garcia',
        'day_of_week': 5,
        'start_time': time(11, 0),
        'duration_minutes': 60,
        'capacity': 30
    },
    {
        'name': 'Boxing Bootcamp',
        'description': 'Cardio boxing combined with strength training for a total body workout.',
        'instructor': 'Jake Thompson',
        'day_of_week': 2,
        'start_time': time(19, 0),
        'duration_minutes': 60,
        'capacity': 20
    },
    {
        'name': 'Morning Stretch',
        'description': 'Gentle stretching and mobility work to start your day energized.',
        'instructor': 'Sarah Johnson',
        'day_of_week': 6,
        'start_time': time(8, 0),
        'duration_minutes': 30,
        'capacity': 15
    }
]

for class_data in classes_data:
    gym_class, created = GymClass.objects.get_or_create(
        name=class_data['name'],
        day_of_week=class_data['day_of_week'],
        defaults=class_data
    )
    if created:
        print(f"✓ Created: {gym_class.name}")
    else:
        print(f"- Already exists: {gym_class.name}")

print(f"\nTotal classes in database: {GymClass.objects.count()}")
print("\nSample data populated successfully!")
print("\nYou can now:")
print("1. Visit the home page to see the gym app")
print("2. Sign up as a member")
print("3. Browse and register for classes")
print("4. Check in at the gym")
print("5. Access admin at /admin/ (create superuser first: python manage.py createsuperuser)")
