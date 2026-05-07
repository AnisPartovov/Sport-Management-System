import os
import django
from django.utils import timezone
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from ucasports.models import Event, Sport, CustomUser
from ucasports.views import get_events_and_competitions_this_week
from ucasports.api.views import EventAPIView

def verify_event_filtering():
    print("Verifying event filtering...")
    
    # Setup
    user = CustomUser.objects.first()
    if not user:
        user = CustomUser.objects.create(username="testuser", email="test@test.com", name="Test User")
        
    sport = Sport.objects.first()
    if not sport:
        sport = Sport.objects.create(name="Test Sport", sport_type="Single-Player")

    now = timezone.now()
    
    # 1. Create a future event (Ongoing or future)
    future_event = Event.objects.create(
        name="Future Event",
        sport=sport,
        start_date_time=now + timedelta(hours=1),
        end_date_time=now + timedelta(hours=2),
        location="Test Loc",
        description="Test Desc",
        creator=user
    )
    
    # 2. Create a past event
    past_event = Event.objects.create(
        name="Past Event",
        sport=sport,
        start_date_time=now - timedelta(hours=2),
        end_date_time=now - timedelta(hours=1),
        location="Test Loc",
        description="Test Desc",
        creator=user
    )
    
    # 3. Create an ongoing event (should be visible)
    ongoing_event = Event.objects.create(
        name="Ongoing Event",
        sport=sport,
        start_date_time=now - timedelta(minutes=30),
        end_date_time=now + timedelta(minutes=30),
        location="Test Loc",
        description="Test Desc",
        creator=user
    )

    print(f"Created events: \n  Future: {future_event} (Ends {future_event.end_date_time})\n  Past: {past_event} (Ends {past_event.end_date_time})\n  Ongoing: {ongoing_event} (Ends {ongoing_event.end_date_time})")

    # Verify Dashboard Logic (get_events_and_competitions_this_week)
    # Note: This function also filters by "this week", so ensures start date is this week. All our events are today.
    
    dashboard_events = get_events_and_competitions_this_week()
    dashboard_ids = [e.id for e in dashboard_events if isinstance(e, Event)]
    
    print(f"\nDashboard Events IDs: {dashboard_ids}")
    
    if past_event.id in dashboard_ids:
        print("[FAIL] Past event is visible on Dashboard.")
    else:
        print("[PASS] Past event is hidden on Dashboard.")
        
    if future_event.id in dashboard_ids:
        print("[PASS] Future event is visible on Dashboard.")
    else:
        print("[FAIL] Future event is hidden on Dashboard.")

    if ongoing_event.id in dashboard_ids:
        print("[PASS] Ongoing event is visible on Dashboard.")
    else:
        print("[FAIL] Ongoing event is hidden on Dashboard.")

    # Verify API Logic
    view = EventAPIView()
    api_queryset = view.get_queryset()
    api_ids = list(api_queryset.values_list('id', flat=True))
    
    print(f"\nAPI Events IDs: {api_ids}")
    
    if past_event.id in api_ids:
        print("[FAIL] Past event is visible in API.")
    else:
        print("[PASS] Past event is hidden in API.")

    if future_event.id in api_ids:
        print("[PASS] Future event is visible in API.")
    else:
        print("[FAIL] Future event is hidden in API.")
        
    if ongoing_event.id in api_ids:
        print("[PASS] Ongoing event is visible in API.")
    else:
        print("[FAIL] Ongoing event is hidden in API.")

    # Cleanup
    future_event.delete()
    past_event.delete()
    ongoing_event.delete()

if __name__ == "__main__":
    verify_event_filtering()
