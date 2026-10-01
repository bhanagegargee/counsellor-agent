from django.urls import path
from .views import AdmissionChatView

urlpatterns = [
    path("chat/", AdmissionChatView.as_view(), name="admission-chat"),
]