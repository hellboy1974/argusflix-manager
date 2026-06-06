from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from apps.m3u.models import M3UAccount
from apps.vod.models import (
    Movie, Series, Episode, VODCategory,
    M3UMovieRelation, M3USeriesRelation, M3UEpisodeRelation, M3UVODCategoryRelation
)
from apps.output.views import xc_get_vod_streams

User = get_user_model()


class VODCategoryVisibilityTests(TestCase):
    def setUp(self):
        # Create test users
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.user.user_level = 10
        self.user.save()

        self.admin = User.objects.create_user(username="adminuser", password="adminpass123")
        self.admin.user_level = 10
        self.admin.save()

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Create active and inactive accounts
        self.active_account = M3UAccount.objects.create(
            name="Active XC Account",
            server_url="http://active.com",
            account_type=M3UAccount.Types.XC,
            is_active=True
        )
        self.inactive_account = M3UAccount.objects.create(
            name="Inactive XC Account",
            server_url="http://inactive.com",
            account_type=M3UAccount.Types.XC,
            is_active=False
        )

        # Create movie categories
        self.enabled_movie_cat = VODCategory.objects.create(
            name="Enabled Movie Cat",
            category_type="movie"
        )
        self.disabled_movie_cat = VODCategory.objects.create(
            name="Disabled Movie Cat",
            category_type="movie"
        )
        self.inactive_movie_cat = VODCategory.objects.create(
            name="Inactive Movie Cat",
            category_type="movie"
        )
        self.custom_movie_cat = VODCategory.objects.create(
            name="Custom Movie Cat",
            category_type="movie"
        )

        # Create category relations
        M3UVODCategoryRelation.objects.create(
            m3u_account=self.active_account,
            category=self.enabled_movie_cat,
            enabled=True
        )
        M3UVODCategoryRelation.objects.create(
            m3u_account=self.active_account,
            category=self.disabled_movie_cat,
            enabled=False
        )
        M3UVODCategoryRelation.objects.create(
            m3u_account=self.inactive_account,
            category=self.inactive_movie_cat,
            enabled=True
        )
        # Note: self.custom_movie_cat has no relation, simulating custom manually added category

        # Create movies
        self.movie_enabled = Movie.objects.create(name="Enabled Movie", year=2021)
        self.movie_disabled = Movie.objects.create(name="Disabled Movie", year=2022)
        self.movie_inactive = Movie.objects.create(name="Inactive Movie", year=2023)

        M3UMovieRelation.objects.create(
            m3u_account=self.active_account,
            movie=self.movie_enabled,
            category=self.enabled_movie_cat,
            stream_id="101"
        )
        M3UMovieRelation.objects.create(
            m3u_account=self.active_account,
            movie=self.movie_disabled,
            category=self.disabled_movie_cat,
            stream_id="102"
        )
        M3UMovieRelation.objects.create(
            m3u_account=self.inactive_account,
            movie=self.movie_inactive,
            category=self.inactive_movie_cat,
            stream_id="103"
        )

        # Create series categories
        self.enabled_series_cat = VODCategory.objects.create(
            name="Enabled Series Cat",
            category_type="series"
        )
        self.disabled_series_cat = VODCategory.objects.create(
            name="Disabled Series Cat",
            category_type="series"
        )

        M3UVODCategoryRelation.objects.create(
            m3u_account=self.active_account,
            category=self.enabled_series_cat,
            enabled=True
        )
        M3UVODCategoryRelation.objects.create(
            m3u_account=self.active_account,
            category=self.disabled_series_cat,
            enabled=False
        )

        # Create series and episodes
        self.series_enabled = Series.objects.create(name="Enabled Series", year=2021)
        self.series_disabled = Series.objects.create(name="Disabled Series", year=2022)

        self.series_relation_enabled = M3USeriesRelation.objects.create(
            m3u_account=self.active_account,
            series=self.series_enabled,
            category=self.enabled_series_cat,
            external_series_id="201"
        )
        self.series_relation_disabled = M3USeriesRelation.objects.create(
            m3u_account=self.active_account,
            series=self.series_disabled,
            category=self.disabled_series_cat,
            external_series_id="202"
        )

        self.episode_enabled = Episode.objects.create(
            name="Enabled Episode",
            series=self.series_enabled,
            season_number=1,
            episode_number=1
        )
        self.episode_disabled = Episode.objects.create(
            name="Disabled Episode",
            series=self.series_disabled,
            season_number=1,
            episode_number=1
        )

        M3UEpisodeRelation.objects.create(
            m3u_account=self.active_account,
            episode=self.episode_enabled,
            series_relation=self.series_relation_enabled,
            stream_id="301"
        )
        M3UEpisodeRelation.objects.create(
            m3u_account=self.active_account,
            episode=self.episode_disabled,
            series_relation=self.series_relation_disabled,
            stream_id="302"
        )

    def test_category_list_visibility(self):
        """VODCategoryViewSet should only return custom categories or categories associated with enabled relations of active accounts."""
        response = self.client.get("/api/vod/categories/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        category_names = [cat["name"] for cat in response.data]

        # Enabled movie category and custom category should be visible
        self.assertIn("Enabled Movie Cat", category_names)
        self.assertIn("Enabled Series Cat", category_names)
        self.assertIn("Custom Movie Cat", category_names)

        # Disabled category and inactive account's category should NOT be visible
        self.assertNotIn("Disabled Movie Cat", category_names)
        self.assertNotIn("Disabled Series Cat", category_names)
        self.assertNotIn("Inactive Movie Cat", category_names)

    def test_movie_list_visibility(self):
        """MovieViewSet should only return movies whose relations have an enabled category and an active account."""
        response = self.client.get("/api/vod/movies/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # DRF response pagination format: results is a list of movies
        movie_names = [movie["name"] for movie in response.data["results"]]

        self.assertIn("Enabled Movie", movie_names)
        self.assertNotIn("Disabled Movie", movie_names)
        self.assertNotIn("Inactive Movie", movie_names)

    def test_series_list_visibility(self):
        """SeriesViewSet should only return series whose relations have an enabled category and an active account."""
        response = self.client.get("/api/vod/series/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        series_names = [s["name"] for s in response.data["results"]]

        self.assertIn("Enabled Series", series_names)
        self.assertNotIn("Disabled Series", series_names)

    def test_episode_list_visibility(self):
        """EpisodeViewSet should only return episodes belonging to series/relations in enabled categories and active accounts."""
        response = self.client.get("/api/vod/episodes/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        episode_names = [ep["name"] for ep in response.data["results"]]

        self.assertIn("Enabled Episode", episode_names)
        self.assertNotIn("Disabled Episode", episode_names)

    def test_xc_output_visibility(self):
        """xc_get_vod_streams should respect enabled categories."""
        # Create a mock request object
        class DummyRequest:
            GET = {}
        
        request = DummyRequest()
        movies_list = xc_get_vod_streams(request, self.user)
        
        movie_names = [m["name"] for m in movies_list]
        self.assertIn("Enabled Movie", movie_names)
        self.assertNotIn("Disabled Movie", movie_names)
        self.assertNotIn("Inactive Movie", movie_names)
