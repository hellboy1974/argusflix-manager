from rest_framework import viewsets, serializers
from apps.output.models import CustomPlaylist, CustomPlaylistLiveMapping, CustomPlaylistVODMapping
from rest_framework.permissions import IsAuthenticated

class CustomPlaylistSerializer(serializers.ModelSerializer):
    live_groups = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )
    vod_categories = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )

    mapped_live_groups = serializers.SerializerMethodField()
    mapped_vod_categories = serializers.SerializerMethodField()

    class Meta:
        model = CustomPlaylist
        fields = [
            'id', 'name', 'slug', 'token', 'is_active', 'custom_properties',
            'created_at', 'updated_at', 'live_groups', 'vod_categories',
            'mapped_live_groups', 'mapped_vod_categories'
        ]
        read_only_fields = ['id', 'slug', 'token', 'created_at', 'updated_at']

    def get_mapped_live_groups(self, obj):
        return list(obj.live_mappings.values_list('channel_group_id', flat=True))

    def get_mapped_vod_categories(self, obj):
        return list(obj.vod_mappings.values_list('vod_category_id', flat=True))

    def create(self, validated_data):
        live_groups = validated_data.pop('live_groups', [])
        vod_categories = validated_data.pop('vod_categories', [])
        playlist = super().create(validated_data)
        
        # Save mappings
        for order, group_id in enumerate(live_groups):
            CustomPlaylistLiveMapping.objects.create(playlist=playlist, channel_group_id=group_id, order=order)
        for order, cat_id in enumerate(vod_categories):
            CustomPlaylistVODMapping.objects.create(playlist=playlist, vod_category_id=cat_id, order=order)
            
        return playlist

    def update(self, instance, validated_data):
        live_groups = validated_data.pop('live_groups', None)
        vod_categories = validated_data.pop('vod_categories', None)
        playlist = super().update(instance, validated_data)

        if live_groups is not None:
            instance.live_mappings.all().delete()
            for order, group_id in enumerate(live_groups):
                CustomPlaylistLiveMapping.objects.create(playlist=playlist, channel_group_id=group_id, order=order)

        if vod_categories is not None:
            instance.vod_mappings.all().delete()
            for order, cat_id in enumerate(vod_categories):
                CustomPlaylistVODMapping.objects.create(playlist=playlist, vod_category_id=cat_id, order=order)

        return playlist


class CustomPlaylistViewSet(viewsets.ModelViewSet):
    queryset = CustomPlaylist.objects.all().order_by('name')
    serializer_class = CustomPlaylistSerializer
    permission_classes = [IsAuthenticated]
