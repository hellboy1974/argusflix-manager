import json

from rest_framework import serializers
from django.contrib.auth.models import Group, Permission
from .models import User
from apps.channels.models import ChannelProfile


# Valid navigation item IDs for validation
VALID_NAV_ITEM_IDS = {
    'channels', 'vods', 'sources', 'guide', 'dvr',
    'stats', 'plugins', 'integrations', 'system', 'settings', 'stalker'
}
MAX_CUSTOM_PROPS_SIZE = 102400  # 100KB limit


def validate_nav_array(value, field_name):
    """Validate that a value is an array of valid nav item ID strings."""
    if not isinstance(value, list):
        raise serializers.ValidationError(f"{field_name} must be an array")
    if len(value) > 50:
        raise serializers.ValidationError(f"{field_name} exceeds maximum length of 50 items")
    for item in value:
        if not isinstance(item, str):
            raise serializers.ValidationError(f"{field_name} items must be strings")
        if item not in VALID_NAV_ITEM_IDS and not item.startswith("plugin-"):
            raise serializers.ValidationError(f"'{item}' is not a valid navigation item ID")


# 🔹 Fix for Permission serialization
class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ["id", "name", "codename"]


# 🔹 Fix for Group serialization
class GroupSerializer(serializers.ModelSerializer):
    permissions = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Permission.objects.all()
    )  # ✅ Fixes ManyToManyField `_meta` error

    class Meta:
        model = Group
        fields = ["id", "name", "permissions"]


# 🔹 Fix for User serialization
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    channel_profiles = serializers.PrimaryKeyRelatedField(
        queryset=ChannelProfile.objects.all(), many=True, required=False
    )
    api_key = serializers.CharField(read_only=True, allow_null=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "api_key",
            "email",
            "user_level",
            "password",
            "channel_profiles",
            "custom_properties",
            "avatar_config",
            "stream_limit",
            "is_staff",
            "is_superuser",
            "last_login",
            "date_joined",
            "first_name",
            "last_name",
        ]

    def validate_custom_properties(self, value):
        """Validate custom_properties structure and size."""
        if value is None:
            return {}
        if not isinstance(value, dict):
            raise serializers.ValidationError("custom_properties must be a dictionary")

        # Size limit check
        try:
            if len(json.dumps(value)) > MAX_CUSTOM_PROPS_SIZE:
                raise serializers.ValidationError(
                    f"custom_properties exceeds maximum size of {MAX_CUSTOM_PROPS_SIZE} bytes"
                )
        except (TypeError, ValueError):
            raise serializers.ValidationError("custom_properties contains non-serializable data")

        # Validate navOrder if present
        if 'navOrder' in value:
            validate_nav_array(value['navOrder'], 'navOrder')

        # Validate hiddenNav if present
        if 'hiddenNav' in value:
            validate_nav_array(value['hiddenNav'], 'hiddenNav')

        # Validate navLabels if present
        if 'navLabels' in value:
            labels = value['navLabels']
            if not isinstance(labels, dict):
                raise serializers.ValidationError("navLabels must be a dictionary")
            for k, v in labels.items():
                if not isinstance(k, str) or not isinstance(v, str):
                    raise serializers.ValidationError("navLabels keys and values must be strings")
                if k not in VALID_NAV_ITEM_IDS and not k.startswith("plugin-"):
                    raise serializers.ValidationError(f"'{k}' is not a valid navigation item ID in navLabels")

        # Validate navIcons if present
        if 'navIcons' in value:
            icons = value['navIcons']
            if not isinstance(icons, dict):
                raise serializers.ValidationError("navIcons must be a dictionary")
            for k, v in icons.items():
                if not isinstance(k, str) or not isinstance(v, str):
                    raise serializers.ValidationError("navIcons keys and values must be strings")
                if k not in VALID_NAV_ITEM_IDS and not k.startswith("plugin-"):
                    raise serializers.ValidationError(f"'{k}' is not a valid navigation item ID in navIcons")

        return value

    def create(self, validated_data):
        channel_profiles = validated_data.pop("channel_profiles", [])

        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.save()

        user.channel_profiles.set(channel_profiles)

        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        channel_profiles = validated_data.pop("channel_profiles", None)

        # Merge custom_properties instead of replacing (prevents data loss)
        # null values are explicit deletions; all other values overwrite existing
        custom_properties = validated_data.pop("custom_properties", None)
        if custom_properties is not None:
            existing = instance.custom_properties or {}
            merged = dict(existing)
            for k, v in custom_properties.items():
                if v is None:
                    merged.pop(k, None)
                else:
                    merged[k] = v
            # Scrub stale nav IDs so the DB self-heals on next save
            for nav_field in ('navOrder', 'hiddenNav'):
                if nav_field in merged and isinstance(merged[nav_field], list):
                    merged[nav_field] = [
                        item for item in merged[nav_field]
                        if item in VALID_NAV_ITEM_IDS or item.startswith("plugin-")
                    ]
            # Scrub stale nav IDs for navLabels and navIcons
            for nav_dict_field in ('navLabels', 'navIcons'):
                if nav_dict_field in merged and isinstance(merged[nav_dict_field], dict):
                    merged[nav_dict_field] = {
                        k: v for k, v in merged[nav_dict_field].items()
                        if (k in VALID_NAV_ITEM_IDS or k.startswith("plugin-")) and isinstance(v, str)
                    }
            instance.custom_properties = merged

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()

        if channel_profiles is not None:
            instance.channel_profiles.set(channel_profiles)

        return instance
