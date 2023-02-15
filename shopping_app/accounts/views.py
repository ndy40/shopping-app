import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# from django.urls import reverse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.reverse import reverse

from .models import User
from .serializers import RegisterSerializer

# Create your views here.


class RegisterUserView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


@api_view(http_method_names=["GET"])
@permission_classes([AllowAny])
def confirm_email(request, key):
    verify_url = reverse("api:accounts:rest_verify_email", request=request)
    try:
        resp = requests.post(verify_url, data={"key": key})
        resp.raise_for_status()
        message = (True, "Email confirmed")
    except requests.exceptions.HTTPError:
        message = (False, "Unable to verify email")

    return render(
        request, "accounts/email/email_confirm.html", context={"data": message}
    )
