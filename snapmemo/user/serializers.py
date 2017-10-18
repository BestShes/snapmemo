from rest_framework import serializers

from user.models import Member


class UserViewSetSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, allow_blank=True, write_only=True)
    access_key = serializers.CharField(allow_blank=True, write_only=True)

    class Meta:
        model = Member
        fields = (
            'username',
            'password',
            'access_key',
            'created_date',
        )

