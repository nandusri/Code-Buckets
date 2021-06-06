from rest_framework import serializers
from users import models
from django.contrib.auth.hashers import make_password

class UserDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True, 'required': False}
                        ,'last_login': {'write_only': True, 'required': False}
                        ,'is_superuser': {'write_only': True, 'required': False}
                        ,'is_staff': {'write_only': True, 'required': False}
                        ,'date_joined': {'write_only': True, 'required': False}
                        ,'groups': {'write_only': True, 'required': False}
                        ,'user_permissions': {'write_only': True, 'required': False}}

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__'
        extra_kwargs = {'last_login': {'write_only': True, 'required': False}
                        ,'is_superuser': {'write_only': True, 'required': False}
                        ,'is_staff': {'write_only': True, 'required': False}
                        ,'date_joined': {'write_only': True, 'required': False}
                        ,'groups': {'write_only': True, 'required': False}
                        ,'user_permissions': {'write_only': True, 'required': False}}

    def create(self, validated_data):
        if validated_data.get('password'):
            validated_data['password'] = make_password(validated_data['password'])
        return super(UserSerializer, self).create(validated_data)