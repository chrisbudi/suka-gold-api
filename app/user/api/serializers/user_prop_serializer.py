

from django.contrib.auth import (
    get_user_model,
)
from django.utils.translation import ngettext_lazy as _

from rest_framework import serializers
from user.models import (
    user_ktp,
    user_props,
    )



class UserPropSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    class Meta:
        model = user_props
        fields = (
            'wallet_amt',
            'gold_wgt',
            'invest_gold_wgt',
            'loan_wgt',
            'loan_amt',
            'photo',
            'bank',
            'rek_number',
            'npwp',
            'level',
            'address',
            'address_post_code',
            'create_time',
            'create_user',
        )

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
 
        if password:
            user.set_password(password)
            user.save()

        return user

class UserKtpSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = user_ktp
        fields = ('ktp_number', 
                  'ktp_photo',
                  'ktp_address',
                  'ktp_address_post_code',
                  'ktp_city_id',
                  )
        