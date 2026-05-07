import os
import django
from datetime import datetime
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from ucasports.models import CustomUser, Event, Sport, Notification

# Create a test user if not exists
user_email = 'testuser_notify@example.com'
if not CustomUser.objects.filter(email=user_email).exists():
    user = CustomUser.objects.create_user(username='test_notify', email=user_email, name='Test Notify', password='password123')
else:
    user = CustomUser.objects.get(email=user_email)

# Create an admin user if not exists (to act as creator)
admin_email = 'admin_notify@example.com'
if not CustomUser.objects.filter(email=admin_email).exists():
    admin = CustomUser.objects.create_superuser(username='admin_notify', email=admin_email, name='Admin Notify', password='password123')
else:
    admin = CustomUser.objects.get(email=admin_email)

# Ensure a sport exists
sport, _ = Sport.objects.get_or_create(name='Test Sport', defaults={'sport_type': 'Single-Player'})

# Create an event manually - this SHOULD NOT trigger notification unless I call the function or if I use the function I created.
# I want to test the function specifically or the view logic.
# Since I cannot easily hit the view from script without test client, I will test the `send_event_notification` function.

from ucasports.utils import send_event_notification

event = Event.objects.create(
    name='Test Event Notification',
    sport=sport,
    start_date_time=timezone.now(),
    end_date_time=timezone.now(),
    location='Test Location',
    description='Test Description',
    creator=admin
)

print(f"Created event: {event.name}")

# Clear existing notifications for test user for clarity
Notification.objects.filter(user=user).delete()

# Trigger notification
send_event_notification(event)
print("Triggered notification")

# Check if user got notification
notifications = Notification.objects.filter(user=user, event=event)
if notifications.exists():
    print(f"SUCCESS: Notification found for user {user.name}")
    print(f"Message: {notifications.first().message}")
else:
    print(f"FAILURE: No notification found for user {user.name}")

# Clean up
event.delete()
# user.delete() # keep user for further manual testing if needed
