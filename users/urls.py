from django.urls import path

from rest_framework_simplejwt.views import(
    TokenObtainPairView as LoginView,
    TokenRefreshView
)

from .views import RegisterView, VerifyView, DeleteItemView, UpdateItemView, AddItemView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify/', VerifyView.as_view(), name='verify'),
    path('login/', LoginView.as_view(), name='login'),
    path('delete-item/', DeleteItemView.as_view(), name='delete-item'),
    path('update-item/', UpdateItemView.as_view(), name='update-item'),
    path('add-item/', AddItemView.as_view(), name='add-item'),
]
