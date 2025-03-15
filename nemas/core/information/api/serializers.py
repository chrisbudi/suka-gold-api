"""
Serializer for recipe api
"""

from rest_framework import serializers
from django_filters import rest_framework as filters
from datetime import datetime

from core.domain import (
    information_educational,
    information_promo,
    information_customer_service,
    information_rating,
    information_article,
)


# region Information Customer Service
class InformationCustomerServiceSerializer(serializers.ModelSerializer):
    """Serializer for information customer service object"""

    class Meta:
        model = information_customer_service
        fields = [
            "information_customer_service_id",
            "information_phone",
            "information_name",
        ]
        read_only_fields = [
            "information_customer_service_id",
        ]

    def create(self, validated_data):
        validated_data["create_user"] = self.context["request"].user
        validated_data["create_user_email"] = self.context["request"].user.email

        validated_data["upd_user"] = self.context["request"].user
        validated_data["upd_user_email"] = self.context["request"].user.email

        validated_data["create_time"] = datetime.now()
        validated_data["upd_time"] = datetime.now()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data["upd_user"] = self.context["request"].user
        validated_data["upd_time"] = datetime.now()
        validated_data["upd_user_email"] = self.context["request"].user.email
        return super().update(instance, validated_data)


class InformationCustomerServiceFilter(filters.FilterSet):
    class Meta:
        model = information_customer_service

        fields = {
            "information_name": ["icontains"],
        }


# endregion


# region Information Educational
class InformationEducationalSerializer(serializers.ModelSerializer):
    """Serializer for Information Educational object"""

    class Meta:
        model = information_educational
        fields = [
            "information_educational_id",
            "information_name",
            "information_notes",
            "information_url",
            "information_background",
        ]
        read_only_fields = [
            "information_educational_id",
        ]

    def create(self, validated_data):
        validated_data["create_user"] = self.context["request"].user
        validated_data["create_user_email"] = self.context["request"].user.email

        validated_data["upd_user"] = self.context["request"].user
        validated_data["upd_user_email"] = self.context["request"].user.email

        validated_data["create_time"] = datetime.now()
        validated_data["upd_time"] = datetime.now()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data["upd_user"] = self.context["request"].user
        validated_data["upd_time"] = datetime.now()
        validated_data["upd_user_email"] = self.context["request"].user.email
        return super().update(instance, validated_data)


class EducationalUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, value):
        if value.size > 10 * 1024 * 1024:  # 10MB limit
            raise serializers.ValidationError("File size exceeds 10MB")
        return value


class InformationEducationalServiceFilter(filters.FilterSet):
    class Meta:
        model = information_educational
        fields = {
            "information_name": ["icontains"],
            "information_background": ["icontains"],
        }


# endregion


# region Information Promo
class InformationPromoSerializer(serializers.ModelSerializer):
    """Serializer for information Promo object"""

    class Meta:
        model = information_promo
        fields = [
            "promo_id",
            "promo_code",
            "leveling_user",
            "promo_name",
            "promo_url",
            "promo_start_date",
            "promo_end_date",
            "promo_tag",
            "promo_diskon",
            "promo_cashback",
            "promo_cashback_tipe_user",
            "promo_url_background",
            "merchant_cashback",
            "show_banner",
            "create_time",
            "create_user",
            "upd_time",
            "upd_user",
        ]
        read_only_fields = [
            "promo_id",
        ]

    def create(self, validated_data):
        validated_data["create_user"] = self.context["request"].user
        validated_data["create_user_email"] = self.context["request"].user.email

        validated_data["upd_user"] = self.context["request"].user
        validated_data["upd_user_email"] = self.context["request"].user.email

        validated_data["create_time"] = datetime.now()
        validated_data["upd_time"] = datetime.now()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data["upd_user"] = self.context["request"].user
        validated_data["upd_time"] = datetime.now()
        validated_data["upd_user_email"] = self.context["request"].user.email
        return super().update(instance, validated_data)


class PromoUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, value):
        if value.size > 10 * 1024 * 1024:  # 10MB limit
            raise serializers.ValidationError("File size exceeds 10MB")
        return value


class InformationPromoFilter(filters.FilterSet):
    class Meta:
        model = information_promo

        fields = {
            "promo_code": ["icontains"],
            "promo_name": ["icontains"],
        }


# endregion


# region Information Rating
class InformationRatingSerializer(serializers.ModelSerializer):
    """Serializer for information Rating object"""

    class Meta:
        model = information_rating
        fields = [
            "information_rate_id",
            "information_rate_name",
            "rate",
            "message",
            "publish",
        ]
        read_only_fields = [
            "information_rate_id",
        ]

    def create(self, validated_data):
        validated_data["create_user"] = self.context["request"].user
        validated_data["create_user_email"] = self.context["request"].user.email

        validated_data["upd_user"] = self.context["request"].user
        validated_data["upd_user_email"] = self.context["request"].user.email

        validated_data["create_time"] = datetime.now()
        validated_data["upd_time"] = datetime.now()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data["upd_user"] = self.context["request"].user
        validated_data["upd_time"] = datetime.now()
        validated_data["upd_user_email"] = self.context["request"].user.email
        return super().update(instance, validated_data)


class InformationRatingFilter(filters.FilterSet):
    class Meta:
        model = information_rating

        fields = {
            "information_rate_name": ["icontains"],
        }


# endregion


# region Information Article
class InformationArticleSerializer(serializers.ModelSerializer):
    """Serializer for information Article object"""

    class Meta:
        model = information_article
        fields = [
            "information_article_id",
            "information_article_name",
            "information_article_body",
            "article_date",
            "article_publish_date",
            "article_updated_date",
            "article_author",
            "article_background",
            "article_source",
            "article_link",
        ]
        read_only_fields = [
            "information_rate_id",
        ]

    def create(self, validated_data):
        validated_data["create_user"] = self.context["request"].user
        validated_data["create_user_email"] = self.context["request"].user.email

        validated_data["upd_user"] = self.context["request"].user
        validated_data["upd_user_email"] = self.context["request"].user.email

        validated_data["create_time"] = datetime.now()
        validated_data["upd_time"] = datetime.now()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data["upd_user"] = self.context["request"].user
        validated_data["upd_time"] = datetime.now()
        validated_data["upd_user_email"] = self.context["request"].user.email
        return super().update(instance, validated_data)


class InformationArticleFilter(filters.FilterSet):
    class Meta:
        model = information_article

        fields = {
            "information_article_name": ["icontains"],
            "article_publish_date": ["exact", "gte", "lte"],
        }


class InformationArticleUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, value):
        if value.size > 10 * 1024 * 1024:  # 10MB limit
            raise serializers.ValidationError("File size exceeds 10MB")
        return value


# endregion
