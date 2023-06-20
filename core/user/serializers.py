"""serializer the user """

from django.contrib.auth import (get_user_model,authenticate)
from django.utils.translation import gettext as _
from rest_framework import serializers


class UserSerializers(serializers.ModelSerializer):
    
    class Meta:
        model= get_user_model()
        fields = ['email','password','name']
        extra_kwargs = {
            'password':{'write_only':True,'min_length':10}
        }

    def create(self,validated_data):
        """create and return a user with encrypted password """
        return get_user_model().objects.create_user(**validated_data)


class AuthTokenSerializer(serializers.Serializer):
    '''serializers for auth token '''
    email = serializers.EmailField()
    password = serializers.CharField(
        max_length=128, 
        write_only=True, 
        style={'input_type': 'password'},
        trim_whitespace = False,
    )


    def validate(self,attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            # to make requsetis passed consistently but required 
            request=self.context.get('request'),
            # we are using email as username so 
            username=email,
            password=password
        )
        if not user:
            msg = _('unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg,code="authorization")
        attrs['user'] = user
        return attrs
