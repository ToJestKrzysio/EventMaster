from event.models import Event


class TestEventRegistrationCountManager:

    def test_get_queryset(self, event_db):
        events = Event.objects_with_registrations.all()
        events_all = Event.objects.all()

        assert len(events) == len(events_all) == 1
        assert events.first().title == events_all.first().title
        assert events.first().seats_taken == 1
