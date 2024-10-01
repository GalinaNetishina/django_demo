from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from advertisements.models import Advertisement


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name")


class AdvertisementSerializer(serializers.ModelSerializer):
    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ("id", "title", "description", "creator", "status", "created_at")

    def create(self, validated_data):

        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        count_opened = (
            Advertisement.objects.all()
            .filter(creator=self.context["request"].user)
            .filter(status="OPEN")
            .count()
        )
        stat = self.initial_data.get("status", "OPEN")
        if count_opened > 10 and stat == "OPEN":
            raise ValidationError(
                'Слишком много активных объявлений, закройте одно из старых или укажите в запросе "status": "CLOSED" либо "DRAFT"'
            )

        return data
