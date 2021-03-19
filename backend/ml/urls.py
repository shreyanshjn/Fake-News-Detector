from django.urls import path
from .views import FakeNewsCheckerView

urlpatterns = [
    path('check/', FakeNewsCheckerView.as_view()),
]
