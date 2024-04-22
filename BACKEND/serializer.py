from rest_framework import serializers
from BACKEND.models import User, Invite

class InviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invite
        fields = ('id', 'code', 'user')
        read_only_fields = ('id',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'phone', 'password', 'invited_by')
        read_only_fields = ('id',)

class UserNonInvitedSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'phone', 'password')
        read_only_fields = ('id',)
