from rest_framework import serializers

from .models import User


class RegisterUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        fields = ['email', 'username', 'first_name', 'last_name', 'password']
        model = User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
        ]


class VerifyUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.BigIntegerField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Bu email bilan user topilmadi."
            )

        return value
        
