from rest_framework import serializers 
from login.models import User


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id',
                    'name',
                    'password',
                    'email',
                    'balance',
                    'order_id',
                    'realname',
                    'user_id_number',
                    'user_phone')