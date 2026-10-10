from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import User, UserVerificationCode
from .serializers import RegisterUserSerializer, UserSerializer, VerifyUserSerializer
from .utils import generate_otp
from .permissions import IsAdmin, IsUser, IsUserOrIsAdmin


class RegisterView(APIView):

    def post(self, reqeust: Request) -> Response:
        serializer = RegisterUserSerializer(data=reqeust.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data

        email=validated_data['email'],
        username=validated_data['username'],

        # User mavjudligini tekshirish
        if User.objects.filter(email=email).exists():
            return Response(
                {
                    "error": "Bu email allaqachon ro'yxatdan o'tgan."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
            
        if User.objects.filter(username=username).exists():
            return Response(
                {
                    "error": "Bu username allaqachon band."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # User yaratish
        user = User(
            email=email,
            username=username,
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
        )

        # MUHIM:
        # make_password() kerak emas.
        # set_password() o'zi passwordni hash qiladi.
        user.set_password(validated_data["password"])

        user.save()

        # OTP yaratish
        otp = generate_otp()

        UserVerificationCode.objects.create(
            user=user,
            otp=otp,
        )

        # Email context
        context = {
            "app_name": "Django Custom User",
            "otp_code": otp,
            "year": 2026,
        }

        html_message = render_to_string(
            "otp.html",
            context,
        )

        plain_message = strip_tags(html_message)

        send_mail(
            subject="Tasdiqlash",
            message=plain_message,
            from_email="mardonovrakhimjon004@gmail.com",
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )

        # User'ni JSON formatga o'tkazish
        user_serializer = UserSerializer(user)

        return Response(
            {
                "message": "Tasdiqlash kodi emailingizga yuborildi.",
                "user": user_serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )


class VerifyView(APIView):

    def post(self, request: Request) -> Response:
        serializer = VerifyUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        otp = serializer.validated_data["otp"]

        user = User.objects.filter(email=email).first()

        if user is None:
            return Response(
                {
                    "error": "Bu email bilan user topilmadi."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        if user.otp.otp != otp:
            return Response(
                {
                    "error": "OTP kodi noto'g'ri."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # User'ni verify qilish
        user.is_verified = True
        user.save(update_fields=["is_verified"])

        return Response(
            {
                "message": "Email muvaffaqiyatli tasdiqlandi."
            },
            status=status.HTTP_200_OK,
        )


class DeleteItemView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, reqeust: Request) -> Response:
        return Response({'message': 'ok'})


class UpdateItemView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsUser]

    def post(self, reqeust: Request) -> Response:
        return Response({'message': 'ok'})


class AddItemView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsUserOrIsAdmin]

    def post(self, reqeust: Request) -> Response:
        return Response({'message': 'ok'})
        
