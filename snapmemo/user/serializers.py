from rest_framework import serializers

from user.models import Member


class UserViewSetSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, required=False, write_only=True)
    access_key = serializers.CharField(required=False, write_only=True)

    class Meta:
        model = Member
        fields = (
            'username',
            'password',
            'user_type',
            'access_key',
            'created_date',
        )

    def create(self, validated_data):
        user = Member(**validated_data)
        try:
            password = validated_data.pop('password')
            user.set_password(password)
        except KeyError:
            pass
        user.save()
        return user

