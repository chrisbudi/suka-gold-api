

from django.contrib.auth import (
    get_user_model,
    authenticate
)
from django.utils.translation import ngettext_lazy as _

from rest_framework import serializers
from user.models import (
    UserKtp,
    UserProp,
    )



class UserPropSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
 
        # print(password, "password");
        if password:
            user.set_password(password)
            user.save()

        return user

class UserKtpSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserKtp
        fields = ('no_ktp', 'name', 'birth_date', 'birth_place', 'address', 'city', 'phone_number', 'email')
        