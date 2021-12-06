from datetime import datetime
from unittest.mock import Mock

import pytest
from django.core.exceptions import ValidationError

from event.forms import EventForm


class TestEventForm:

    @pytest.mark.parametrize("price", [-1, -872.23132])
    def test_clean_price_negative(self, price):
        form_mock = Mock(cleaned_data={"price": price})

        with pytest.raises(ValidationError):
            EventForm.clean_price(self=form_mock)

    @pytest.mark.parametrize("price", [0,  3.14, 1111])
    def test_clean_price_positive(self, price):
        form_mock = Mock(cleaned_data={"price": price})

        result = EventForm.clean_price(self=form_mock)

        assert result == price

    @pytest.mark.parametrize("occupancy", [-1, -8.5, -13])
    def test_clean_max_occupancy_negative(self, occupancy):
        form_mock = Mock(cleaned_data={"max_occupancy": occupancy})

        with pytest.raises(ValidationError):
            EventForm.clean_max_occupancy(form_mock)

    @pytest.mark.parametrize("occupancy", [3.4, 13.6])
    def test_clean_max_occupancy_non_integer(self, occupancy):
        form_mock = Mock(cleaned_data={"max_occupancy": occupancy})

        with pytest.raises(ValidationError):
            EventForm.clean_max_occupancy(form_mock)

    @pytest.mark.parametrize("occupancy", [0, 6, 17])
    def test_clean_max_occupancy_positive(self, occupancy):
        form_mock = Mock(cleaned_data={"max_occupancy": occupancy})

        result = EventForm.clean_max_occupancy(form_mock)

        assert result == occupancy

    @pytest.mark.parametrize("start, end", [
        (datetime(2021, 5, 14, 15, 35, 00), datetime(2020, 5, 14, 15, 35, 00)),
        (datetime(2021, 6, 6, 14, 00, 30), datetime(2020, 6, 6, 14, 00, 30)),
        (datetime(2000, 3, 3, 14, 00, 31), datetime(2000, 3, 3, 14, 00, 30)),
    ])
    def test_clean_end_time_lower_than_start_time(self, start, end):
        form_mock = Mock(cleaned_data={"start_time": start, "end_time": end})

        with pytest.raises(ValidationError):
            EventForm.clean_end_time(form_mock)

    @pytest.mark.parametrize("start, end", [
        (datetime(2020, 6, 6, 14, 00, 30), datetime(2021, 6, 6, 14, 00, 30)),
        (datetime(2020, 3, 3, 14, 00, 30), datetime(2020, 6, 6, 14, 00, 31)),
    ])
    def test_clean_end_time_greater_than_start_time(self, start, end):
        form_mock = Mock(cleaned_data={"start_time": start, "end_time": end})

        result = EventForm.clean_end_time(form_mock)

        assert result == end

    @pytest.mark.parametrize("start, deadline", [
        (datetime(2020, 5, 14, 15, 35, 00), datetime(2021, 5, 14, 15, 35, 00)),
        (datetime(2020, 6, 6, 14, 00, 30), datetime(2021, 6, 6, 14, 00, 30)),
        (datetime(2000, 3, 3, 14, 00, 30), datetime(2000, 3, 3, 14, 00, 31)),
    ])
    def test_clean_registration_deadline_lower_than_start_time(self, start,
                                                               deadline):
        form_mock = Mock(cleaned_data={"start_time": start,
                                       "registration_deadline": deadline})

        with pytest.raises(ValidationError):
            EventForm.clean_registration_deadline(form_mock)

    @pytest.mark.parametrize("start, deadline", [
        (datetime(2021, 6, 6, 14, 00, 30), datetime(2020, 6, 6, 14, 00, 30)),
        (datetime(2020, 6, 6, 14, 00, 31), datetime(2020, 3, 3, 14, 00, 30)),
    ])
    def test_clean_registration_deadline_lower_than_start_time(self, start,
                                                               deadline):
        form_mock = Mock(cleaned_data={"start_time": start,
                                       "registration_deadline": deadline})

        result = EventForm.clean_registration_deadline(form_mock)

        assert result == deadline
