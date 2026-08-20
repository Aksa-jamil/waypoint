from django.test import TestCase
from django.urls import reverse

from trails.models import Park, Trail
from waypoint.distance import Distance


class TrailCatalogTests(TestCase):

    def setUp(self):
        self.park = Park.objects.create(
            name="Blue Mountain Park",
            region="Ontario",
        )

        self.open_trail = Trail.objects.create(
            name="Blue Mountain Trail",
            park=self.park,
            distance_km=8.50,
            elevation_gain=250,
            difficulty="moderate",
            is_open=True,
        )

        self.closed_trail = Trail.objects.create(
            name="Closed Mountain Trail",
            park=self.park,
            distance_km=10.00,
            elevation_gain=300,
            difficulty="hard",
            is_open=False,
        )

    def test_catalog_shows_open_trails_only(self):
        response = self.client.get(reverse("catalog"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Blue Mountain Trail")
        self.assertNotContains(response, "Closed Mountain Trail")

    def test_missing_trail_returns_404(self):
        response = self.client.get(
            reverse("trail-detail", args=[9999])
        )

        self.assertEqual(response.status_code, 404)


class DistanceTests(TestCase):

    def test_distance_rejects_negative_magnitude(self):
        with self.assertRaises(ValueError):
            Distance(-5, "km")