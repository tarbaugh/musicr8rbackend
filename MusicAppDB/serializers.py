# MusicAppDB/serializers.py
#Currently not using serializers-- we may not need them?

from rest_framework import serializers
from .models import Users

# The serializer translates a Todo object into a format that
# can be stored in our database. We use the Todo model.
class UsersSerializer(serializers.ModelSerializer):
  class Meta:
    model = Users
    fields = ('id', 'username', 'password')