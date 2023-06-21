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

    def update(self, instance, validated_data):
        """to update data that are comming this is done in deserializer """
        instance.email = validated_data.get('email')
        instance.password = validated_data.get('password')
        instance.name = validated_data.get('name')
        instance.save()
        return instance
    
        # or

        # POP means remove the data form dictonary but if we user get it will get the data but remain in dictonary
        # password = validated_data.pop('password',None)
        # user = super().update(instance,validated_data)
        # if password :
        #     user.set_password(password)
        #     user.save()
        # return user


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
