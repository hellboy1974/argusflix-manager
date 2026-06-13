from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import AppProfile, AppPage, AppWidget
from apps.accounts.models import Profile

class LayoutExportViewSet(viewsets.ViewSet):
    """
    Endpoint for the Android TV App to fetch its UI layout configuration dynamically.
    The Android app calls /api/v1/appbuilder/export/?profile_id=<id>
    """

    def list(self, request):
        profile_id = request.query_params.get('profile_id')
        layout_profile = None

        if profile_id:
            try:
                user_profile = Profile.objects.get(id=profile_id, user=request.user)
                layout_profile = user_profile.layout_profile
            except Profile.DoesNotExist:
                pass

        if not layout_profile:
            layout_profile = AppProfile.objects.filter(is_default=True).first()

        if not layout_profile:
            return Response([])

        # Flat output mapped to the legacy AppPageLayout format for backward compatibility
        # while taking advantage of the new profile-aware builder.
        layouts = []
        
        pages = AppPage.objects.filter(profile=layout_profile)
        for page in pages:
            widgets = AppWidget.objects.filter(page=page).order_by('order')
            for widget in widgets:
                # We map the widget settings to the expected flat format
                settings = widget.settings or {}
                
                # Transform widget_type to section_type
                section_type = "CAROUSEL_ROW"
                if widget.widget_type == "hero":
                    section_type = "HERO_BANNER"
                elif widget.widget_type == "grid":
                    section_type = "GRID"

                content_source = settings.get("content_source", "RECENTLY_ADDED")
                if widget.widget_type == "continue_watching":
                    content_source = "CONTINUE_WATCHING"
                elif widget.widget_type == "favorites":
                    content_source = "FAVORITES"

                layouts.append({
                    "id": widget.id,
                    "title": settings.get("title", widget.get_widget_type_display()),
                    "page": page.page_type.upper(),
                    "section_type": section_type,
                    "content_source": content_source,
                    "provider_id": settings.get("provider_id", ""),
                    "category_id": settings.get("category_id", ""),
                    "filter_criteria": settings.get("filter_criteria", {}),
                    "sort_order": widget.order,
                    "is_active": settings.get("is_active", True)
                })

        return Response(layouts)
