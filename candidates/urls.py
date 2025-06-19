from django.urls import path
from .views import CandidateAPIView

urlpatterns = [
    path('candidates/', CandidateAPIView.as_view(), name='candidate-api'),
]
