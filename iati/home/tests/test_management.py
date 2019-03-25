"""A module of unit tests for management commands."""
import pytest
import requests
from io import StringIO
from django.core.management import call_command
from wagtail.core.models import Page
from home.management.commands.createdefaultpages import DEFAULT_PAGES
from home.management.commands.updatestatistics import (
    ACTIVITY_URL,
    ORGANISATION_URL,
)


@pytest.mark.django_db
class TestUpdateStatistics():
    """Unit tests for updatestatistics command."""

    def test_activity_endpoint(self):
        """Test status code for activity endpoint."""
        response = requests.get(ACTIVITY_URL)
        assert response.status_code == 200

    def test_organisation_endpoint(self):
        """Test status code for organisation endpoint."""
        response = requests.get(ORGANISATION_URL)
        assert response.status_code == 200

    def test_update_statistics_command(self, client):
        """Test result for called command returns expected response."""
        out = StringIO()
        call_command('updatestatistics', stdout=out)

        success_message = 'Successfully updated home page statistics.'
        error_messages = [
            'Unable to connect to IATI registry to query activities.',
            'Unable to connect to IATI registry to query organisations.',
        ]
        out_value = out.getvalue().rstrip()

        assert out_value == success_message
        assert out_value not in error_messages


@pytest.mark.django_db
class TestCreateDefaultPages():
    """Unit test to test createdefaultpages management command."""

    def test_create_default_pages_command(self):
        """Test result for called command returns expected response."""
        out = StringIO()
        call_command('createdefaultpages', stdout=out)
        success_message = 'Success.'
        out_value = out.getvalue().rstrip()

        expected_pages = [x['title'] for x in DEFAULT_PAGES]
        qs = Page.objects.filter(title__in=expected_pages).all()

        assert success_message in out_value
        assert len(qs) > 0
