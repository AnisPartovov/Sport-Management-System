from django.contrib.auth.tokens import PasswordResetTokenGenerator

#import six

class TokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return str(user.pk) + str(timestamp) + str(user.is_active)
        #return (six.text_type(user.pk)+six.text_type(timestamp)+six.text_type(user.is_active))

generate_token = TokenGenerator()

def send_event_notification(event):
    from .models import CustomUser, Notification
    users = CustomUser.objects.all()
    notifications = []
    for user in users:
        notifications.append(Notification(user=user, event=event, message=f"{event.creator.name} added new event."))
    Notification.objects.bulk_create(notifications)
