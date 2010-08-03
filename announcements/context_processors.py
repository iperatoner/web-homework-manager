from announcements.models import Announcement


def announcements(request):
    """Add the announcement objects."""
    announcements = Announcement.objects.order_by('-date_created')
    return {'announcements': announcements}
