# -*- coding: utf-8 -*-

# Imports
from django.contrib.auth.models import User
from rest_framework import serializers

# Class declarations
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')